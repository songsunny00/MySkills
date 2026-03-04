# 田园现代言情赛道 - 提示词模板使用指南

## 模板概述

本套模板专为田园现代言情赛道设计，包含5个核心模板，覆盖小说生成的全流程。

## 模板列表

### 1. worldbuilding.jinja2 - 世界观构建模板
**用途**: 生成乡村背景设定
**输出**: 1200-1500字的世界观文档
**包含内容**:
- 地理背景（位置、自然环境、气候）
- 村落设定（名称、规模、建筑）
- 经济产业（主要产业、特色产品）
- 社会文化（人际关系、传统习俗）
- 时代背景（政策、趋势）

### 2. character_creation.jinja2 - 角色创建模板
**用途**: 生成符合田园言情特色的角色
**输出**: 1500-2000字的角色档案
**包含内容**:
- 基本信息（姓名、年龄、职业）
- 外貌特征（清新自然、接地气）
- 性格特征（真实立体）
- 背景故事（返乡/来乡原因）
- 能力特长（专业+生活技能）
- 成长弧线（蜕变路径）
- 人际关系（与其他角色）
- 情感线索（仅主角）

### 3. plot_design.jinja2 - 情节设计模板
**用途**: 设计完整的情节框架
**输出**: 2000-2500字的情节设计
**包含内容**:
- 核心冲突（外部+内部+人际）
- 主线情节（5-7个关键情节点）
- 副线情节（2-3条副线）
- 情感线（感情发展阶段）
- 成长线（主角成长路径）
- 高潮设计（最大冲突）
- 结局方向（圆满HE）

### 4. outline_generation.jinja2 - 大纲生成模板
**用途**: 生成详细的章节大纲
**输出**: 完整的章节大纲（每章200-300字）
**包含内容**:
- 章节标题
- 章节概要
- 关键情节点
- 涉及角色
- 目标字数
- 章节类型
- 章末钩子

### 5. chapter_generation.jinja2 - 章节生成模板
**用途**: 生成具体章节内容
**输出**: 2000字左右的章节正文
**包含内容**:
- 开篇场景（200-300字）
- 主体情节（1500-2000字）
- 对话、描写、心理活动
- 结尾钩子（200-300字）

## 田园现代言情赛道特点

### 核心主题
- 🌾 乡村振兴、返乡创业
- 💚 自我成长、找到归属
- 💕 治愈系爱情
- 🏡 传统与现代融合

### 写作风格
- 语言清新自然、朴实
- 节奏舒缓、慢热
- 注重日常生活细节
- 温暖治愈、正能量

### 常见元素
- 田园风光（四季、农作物）
- 日常劳作（种地、做饭）
- 村民互动（邻里关系）
- 电商直播（现代元素）
- 特色产业（有机农业、民宿）

### 角色特点
- **女主**: 独立自强、有想法、能吃苦
- **男主**: 踏实可靠、有担当、接地气
- **配角**: 有特色的村民群像

### 情节特点
- 慢热型、不追求快节奏
- 基于现实的困难和挑战
- 感情发展自然、水到渠成
- 事业爱情双线并进

## 使用方法

### 方法1: 通过代码使用

```python
from src.novel_generator.prompt_templates import PromptTemplateManager
from pathlib import Path

# 创建模板管理器，指定田园言情模板目录
template_dir = Path("src/novel_generator/templates/tianyuan_yanqing")
manager = PromptTemplateManager(template_dir)

# 渲染世界观模板
world_prompt = manager.render(
    "worldbuilding.jinja2",
    mode="quick",
    user_input="江南水乡，茶园为主"
)

# 渲染角色模板
char_prompt = manager.render(
    "character_creation.jinja2",
    role="protagonist",
    world_building=world_content,
    user_input="女主，返乡创业"
)
```

### 方法2: 修改系统配置

修改 `src/novel_generator/prompt_templates.py`，添加类型映射：

```python
GENRE_TEMPLATE_MAPPING = {
    NovelGenre.YANQING: "tianyuan_yanqing",  # 言情类型使用田园言情模板
    # 其他类型...
}

def get_template_path(genre: NovelGenre, template_name: str) -> Path:
    """根据类型获取模板路径"""
    template_subdir = GENRE_TEMPLATE_MAPPING.get(genre, "default")
    return templates_dir / template_subdir / f"{template_name}.jinja2"
```

## 模板变量说明

### worldbuilding.jinja2
- `mode`: 生成模式（quick/detailed）
- `user_input`: 用户输入的额外要求（可选）

### character_creation.jinja2
- `role`: 角色类型（protagonist/supporting/antagonist）
- `world_building`: 世界观内容
- `user_input`: 用户输入的角色要求（可选）

### plot_design.jinja2
- `genre`: 小说类型
- `target_word_count`: 目标字数
- `world_building`: 世界观内容
- `characters`: 角色列表
- `user_input`: 用户输入的情节要求（可选）

### outline_generation.jinja2
- `genre`: 小说类型
- `target_word_count`: 目标字数
- `chapter_count`: 章节数
- `words_per_chapter`: 每章平均字数
- `world_building`: 世界观内容
- `plot_design`: 情节设计内容

### chapter_generation.jinja2
- `genre`: 小说类型
- `chapter_number`: 章节号
- `chapter_title`: 章节标题
- `chapter_outline`: 本章大纲
- `context_summary`: 上下文摘要
- `previous_chapter`: 上一章内容（可选）
- `target_word_count`: 目标字数

## 优化建议

### 1. 根据实际效果调整
- 如果生成内容过于理想化，强调"真实感"
- 如果节奏太快，强调"慢热"、"日常细节"
- 如果缺乏地方特色，增加地域要求

### 2. 添加示例
- 在模板中添加优秀段落示例
- 提供不同场景的写作范例
- 展示对话、描写的标准

### 3. 细化要求
- 针对不同章节类型提供不同模板
- 为关键章节（开篇、高潮、结局）单独优化
- 增加更多写作技巧指导

### 4. 迭代优化
- 根据生成效果持续调整
- 收集优秀案例，提炼规律
- 建立质量评估标准

## 注意事项

1. **保持一致性**: 确保各模板之间的风格和设定一致
2. **避免套路化**: 虽然有模板，但要鼓励创新和变化
3. **真实感**: 强调基于现实，避免过度理想化
4. **正能量**: 传递积极向上的价值观
5. **可读性**: 生成的内容要吸引人、有代入感

## 扩展方向

1. **细分子类型**:
   - 茶园言情
   - 果园言情
   - 民宿言情
   - 电商言情

2. **地域特色**:
   - 江南水乡版
   - 西南山区版
   - 东北乡村版
   - 沿海渔村版

3. **特殊主题**:
   - 非遗传承
   - 生态保护
   - 乡村教育
   - 养老产业

## 版本记录

- v1.0 (2026-03-04): 初始版本，包含5个核心模板