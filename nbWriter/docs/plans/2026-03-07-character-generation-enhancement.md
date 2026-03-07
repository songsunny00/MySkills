# 角色生成系统增强设计

**日期**: 2026-03-07
**目标**: 实现分层角色生成，根据情节需要补充配角

## 问题分析

当前系统只生成4个角色（1个protagonist + 2个supporting + 1个antagonist），存在以下问题：

1. 硬编码角色数量，不适应不同字数规模的小说
2. 缺少男主生成（模板定义了male_protagonist但代码未调用）
3. 对于10万字小说，4个角色过少，缺乏群像感
4. antagonist生成的是"对立角色"而非男主

## 设计方案

### 整体架构

采用**分层生成策略**：
- **第一层（角色设定阶段）**: 生成核心角色（女主、男主、2个重要配角）
- **第二层（情节设计后）**: 根据情节需要，补充功能性配角

**新流程**：
```
世界观 → 核心角色(4个) → 情节设计 → 补充配角(6-10个) → 大纲生成 → 章节生成
```

### 组件设计

#### 1. CharacterCreationStage 修改

**职责**: 只生成核心4人

**修改内容**:
```python
class CharacterCreationStage(GenerationStage):
    async def execute(self, user_input: Optional[str] = None) -> list:
        """生成核心角色（4个）"""
        template_content = self.template_manager.get_template_content(
            "character_creation", self.project.genre
        )

        # 按模板定义的角色类型生成
        core_roles = [
            "protagonist",        # 女主
            "male_protagonist",   # 男主
            "supporting",         # 配角1（林杳或谷小满）
            "supporting"          # 配角2（林杳或谷小满）
        ]

        characters = []
        for role in core_roles:
            char = await self._create_character(role, template_content, user_input)
            characters.append(char)

        return characters
```

**关键变化**:
- 移除antagonist生成
- 添加male_protagonist生成
- 固定生成4个核心角色

#### 2. 新增 SupplementaryCharacterStage

**职责**: 在情节设计完成后，分析情节并补充功能性配角

**实现**:
```python
class SupplementaryCharacterStage(GenerationStage):
    """补充配角生成阶段"""

    def get_stage_name(self) -> str:
        return "补充配角"

    async def execute(self, user_input: Optional[str] = None) -> list:
        """根据情节设计补充配角"""
        template_content = self.template_manager.get_template_content(
            "supplementary_characters", self.project.genre
        )

        # 构建核心角色摘要
        core_chars_summary = "\n\n".join([
            f"### {i+1}. {self._extract_name(char)}\n{char[:300]}..."
            for i, char in enumerate(self.project.characters[:4])
        ])

        # 让LLM分析情节，决定需要哪些配角
        prompt = self.template_manager.render_string(
            template_content,
            world_building=self.project.world_building[:1000],  # 摘要
            core_characters=core_chars_summary,
            plot_design=self._get_plot_summary(),
            target_word_count=self.project.target_word_count
        )

        # LLM返回需要的配角列表和每个配角的档案
        response = await self.llm.generate(prompt)

        # 解析并保存每个配角
        supplementary_chars = self._parse_characters(response)

        if self.on_progress:
            self.on_progress(f"生成了 {len(supplementary_chars)} 个补充配角")

        for char_name, char_content in supplementary_chars:
            self.ctx.save_character(char_name, char_content)
            self.project.characters.append(char_content)

        return [char_content for _, char_content in supplementary_chars]

    def _get_plot_summary(self) -> str:
        """获取情节摘要"""
        if self.project.plot_lines:
            return "\n".join([f"- {line.description[:200]}"
                            for line in self.project.plot_lines[:5]])
        return "（情节设计未完成）"

    def _parse_characters(self, response: str) -> list:
        """解析LLM返回的多个角色（用---分隔）"""
        characters = []
        sections = response.split('---')

        for section in sections:
            section = section.strip()
            if len(section) < 100:  # 过滤掉太短的片段
                continue

            # 提取角色名
            char_name = self._extract_name(section)
            characters.append((char_name, section))

        return characters

    def _extract_name(self, content: str) -> str:
        """从内容中提取角色名称"""
        lines = content.split('\n')
        for line in lines[:10]:
            if '姓名' in line or '名字' in line or '**姓名**' in line:
                parts = line.split('：')
                if len(parts) < 2:
                    parts = line.split(':')
                if len(parts) >= 2:
                    name = parts[1].strip().replace('*', '').replace('#', '')
                    return name
        return f"配角_{len(self.project.characters)}"
```

#### 3. generator.py 流程调整

**修改 generate_novel() 方法**:
```python
async def generate_novel(self, ...):
    # ... 现有代码 ...

    # 阶段1: 世界观
    world_building_stage = WorldBuildingStage(...)
    await world_building_stage.run(...)

    # 阶段2: 核心角色（4个）
    character_stage = CharacterCreationStage(...)
    await character_stage.run(...)

    # 阶段3: 情节设计
    plot_stage = PlotDesignStage(...)
    await plot_stage.run(...)

    # 【新增】阶段4: 补充配角
    supplementary_stage = SupplementaryCharacterStage(
        project, context_manager, llm_client, template_manager
    )
    await supplementary_stage.run(on_progress=on_progress)

    # 阶段5: 大纲生成
    outline_stage = OutlineGenerationStage(...)
    await outline_stage.run(...)

    # ... 后续章节生成 ...
```

**修改 STAGE_ORDER**:
```python
STAGE_ORDER = [
    "世界观构建",
    "角色设定",
    "情节设计",
    "补充配角",      # 新增
    "大纲生成",
    "章节生成",
    "润色优化"
]
```

**修改 resume_generation()**:
在stage映射中添加新阶段的处理。

#### 4. 新建模板 supplementary_characters.jinja2

**位置**: `src/novel_generator/templates/tianyuan_yanqing/supplementary_characters.jinja2`

**内容**:
```jinja2
# 补充配角生成模板

你是擅长田园现代言情的资深作家。已有核心角色和情节设计，现在需要补充功能性配角。

---

## 已有信息

### 世界观（摘要）
{{ world_building }}

### 核心角色（已生成4个）
{{ core_characters }}

### 情节设计
{{ plot_design }}

### 目标字数
{{ target_word_count }} 字

---

## 任务

分析情节设计，识别需要补充的配角类型。对于田园现代言情，常见配角包括：

**村民角色**：
- 保守派村民（对公寓有疑虑）
- 开明派村民（支持新事物）
- 热心邻居（提供帮助和人情味）
- 村干部（代表基层治理）

**公寓过客**：
- 疗愈人群（抑郁、焦虑、职业倦怠）
- 远程工作者（数字游民）
- gap year青年（迷茫期）
- 短期避世者（逃离城市压力）

**城市关系**：
- 前同事（职场记忆）
- HR或领导（裁员相关）
- 仲裁律师（法律线索）
- 其他城市朋友

**其他**：
- 根据情节需要的特定角色

---

## 生成要求

1. **数量**：根据字数规模，建议生成 6-10 个配角
   - 6万字以下：6个
   - 6-10万字：8个
   - 10万字以上：10个

2. **每个配角包含**（500-800字）：
   - 姓名、年龄、身份
   - 外貌特征（100字）
   - 性格特点（150字）
   - 背景故事（200字）
   - 与主角的关系（100字）
   - 在情节中的作用（100字）

3. **写作原则**：
   - 拒绝脸谱化，每个人都有合理动机
   - 配角要为情节服务，不是凑数
   - 体现时代感和真实性
   - 语言克制，避免空泛形容

4. **输出格式**：
   - 每个角色用 `---` 分隔
   - Markdown格式
   - 按重要性排序（先写戏份多的）

---

请开始生成补充配角。
```

## 实施步骤

1. 修改 `stages.py`:
   - 修改 `CharacterCreationStage.execute()` 生成4个核心角色
   - 新增 `SupplementaryCharacterStage` 类

2. 修改 `generator.py`:
   - 在 `generate_novel()` 中插入新阶段
   - 更新 `STAGE_ORDER`
   - 修改 `resume_generation()` 支持新阶段

3. 创建模板:
   - `src/novel_generator/templates/tianyuan_yanqing/supplementary_characters.jinja2`
   - 可选：创建通用版 `src/novel_generator/templates/supplementary_characters.jinja2`

4. 测试:
   - 创建新项目验证核心角色生成
   - 验证补充配角阶段正常执行
   - 检查角色文件保存正确

## 预期效果

- 10万字小说将生成约12-14个角色（4核心 + 8-10配角）
- 角色更贴合情节需要
- 支持断点续传（新阶段可独立重试）
- 为后续大纲和章节生成提供充足的角色池