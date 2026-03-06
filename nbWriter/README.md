# 一键生成小说系统

基于大语言模型的自动化小说生成系统，支持生成50,000-80,000字的中长篇网络小说。

## 核心特性

- 🚀 **一键生成**：CLI交互式引导，分阶段确认生成结果
- 📚 **多类型支持**：玄幻、都市、言情、科幻、武侠等主流网文类型
- 🎯 **双模式运行**：快速模式（自动生成）/ 详细模式（每阶段确认）
- 🔄 **智能断点续传**：中断后自动保存进度，可随时恢复继续生成
- 💎 **智能章节策略**：关键章节优先生成，确保情节连贯性
- ✨ **润色去AI化**：自动消除AI痕迹，让文字更有人味
- ✏️ **全程可控**：每个阶段可编辑、重新生成或跳过
- 📦 **完整输出**：世界观、人物档案、情节设计、章节大纲、正文内容

## 快速开始

### 1. 创建虚拟环境并安装依赖

```bash
# 创建虚拟环境（仅首次）
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 安装依赖（激活后执行）
pip install -r requirements.txt
```

### 2. 配置API密钥

创建 `.env` 文件：

```env
# Anthropic Claude（支持自定义代理地址）
ANTHROPIC_API_KEY=your_anthropic_api_key
ANTHROPIC_BASE_URL=https://api.anthropic.com  # 可选，私有代理时填写

# OpenAI
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=https://api.openai.com  # 可选

# DeepSeek
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com  # 可选，默认即此地址
```

### 3. 运行生成

**创建新项目**：

```bash
python -m src.novel_generator.cli
# 选择 "1. 创建新项目"
```

按照交互式提示选择：
1. 小说类型（如：田园现代言情）
2. 生成模式（快速/详细）
3. 目标字数（默认60,000字）

系统将自动完成6个生成阶段，最终输出完整小说项目。

**恢复中断的项目**：

```bash
python -m src.novel_generator.cli
# 选择 "2. 恢复已有项目"
# 从列表中选择要恢复的项目
```

系统会自动检测未完成的阶段和章节，从中断处继续生成。

> 💡 **提示**：生成过程可随时按 `Ctrl+C` 中断，所有进度会自动保存，下次恢复时会跳过已完成的部分。

## 系统架构

### 核心模块说明

```
src/novel_generator/
├── config.py              # 配置管理（生成参数、LLM配置、项目配置）
├── models.py              # 数据模型（小说项目、角色、章节、状态等）
├── context_manager.py     # 上下文管理（项目文件读写、状态持久化）
├── llm_client.py          # LLM客户端抽象（支持Anthropic/OpenAI）
├── prompt_templates.py    # 提示词模板管理（Jinja2模板系统）
├── stages.py              # 生成阶段实现（5个核心阶段的执行逻辑）
├── generator.py           # 生成器编排（协调各阶段执行流程）
└── cli.py                 # 命令行界面（交互式用户界面）
```

### 6个生成阶段（stages.py）

系统将小说生成拆解为6个独立阶段，每个阶段可单独执行、编辑和重新生成：

| 阶段 | 类名 | 功能 | 输出 |
|------|------|------|------|
| 1️⃣ 世界观构建 | `WorldBuildingStage` | 生成故事背景、时代设定、地理环境 | `worldbuilding/world.md` |
| 2️⃣ 角色创建 | `CharacterCreationStage` | 创建主角、配角、反派的详细档案 | `characters/*.md` |
| 3️⃣ 情节设计 | `PlotDesignStage` | 规划主线、副线、冲突点、高潮 | `plot/plot_design.md` |
| 4️⃣ 大纲生成 | `OutlineGenerationStage` | 生成每章标题、概要、关键情节点 | `plot/outline.md` |
| 5️⃣ 章节生成 | `ChapterGenerationStage` | 按大纲生成完整章节正文 | `chapters/chapter-*.md` |
| 6️⃣ 润色去AI化 | `PolishStage` | 逐章润色，消除AI痕迹，还原人味 | 覆盖更新原章节文件 |

每个阶段都继承自 `GenerationStage` 基类，实现了：
- `execute()`: 核心生成逻辑
- `run()`: 带状态管理的执行包装
- 自动保存结果到项目目录
- 支持回调函数报告进度

### 提示词模板系统

```
src/novel_generator/templates/
└── tianyuan_yanqing/              # 田园现代言情类型模板
    ├── worldbuilding.jinja2       # 世界观构建提示词
    ├── character_creation.jinja2  # 角色创建提示词
    ├── plot_design.jinja2         # 情节设计提示词
    ├── outline_generation.jinja2  # 大纲生成提示词
    ├── chapter_generation.jinja2  # 章节生成提示词
    └── polish.jinja2              # 润色去AI化提示词
```

每个类型都有独立的模板集，使用Jinja2语法支持动态内容注入。

## 生成的项目结构

```
output/novel_xxxxx/
├── metadata.json              # 项目元数据（类型、状态、配置）
├── worldbuilding/
│   └── world.md              # 世界观设定文档
├── characters/
│   ├── protagonist.md        # 主角档案
│   ├── male_protagonist.md   # 男主档案
│   └── supporting_*.md       # 配角档案
├── plot/
│   ├── plot_design.md        # 情节设计文档
│   └── outline.md            # 完整章节大纲
├── chapters/
│   ├── chapter-001.md        # 第1章正文
│   ├── chapter-002.md        # 第2章正文
│   └── ...
└── exports/                  # 导出文件（TXT/EPUB等）
```

## 编程方式使用

```python
import asyncio
from src.novel_generator.models import NovelGenre, GenerationMode
from src.novel_generator.config import LLMConfig, ProjectConfig
from src.novel_generator.generator import NovelGenerator

async def generate():
    # 配置项目和LLM（三选一）
    project_config = ProjectConfig.create("./output")

    # 方式一：Anthropic Claude（读取 .env 中的 KEY 和 BASE_URL）
    llm_config = LLMConfig(provider="anthropic", model="claude-sonnet-4-6")

    # 方式二：DeepSeek
    # llm_config = LLMConfig(provider="deepseek", model="deepseek-chat")

    # 方式三：OpenAI
    # llm_config = LLMConfig(provider="openai", model="gpt-4o")

    # 创建生成器
    generator = NovelGenerator(project_config, llm_config)

    # 定义进度回调
    def on_progress(message: str):
        print(f"[进度] {message}")

    # 执行生成
    project = await generator.generate_novel(
        genre=NovelGenre.TIANYUAN_YANQING,  # 田园现代言情
        mode=GenerationMode.QUICK,          # 快速模式
        target_word_count=60000,            # 目标6万字
        on_progress=on_progress
    )

    print(f"✅ 生成完成: {project.project_id}")
    print(f"📁 项目路径: {project_config.output_dir / project.project_id}")

asyncio.run(generate())
```

## 高级功能

### 润色与去AI化

第6阶段 `PolishStage` 会逐章处理，消除以下AI常见问题：

- **机械重复**：相同句式连续出现（如"她...，她...，她..."）
- **形容词堆砌**：一个名词挂多个修饰词
- **情绪标签**：直接写"她很高兴"而不是通过细节展现
- **过度流畅**：AI文本太"完美"，没有人类说话的停顿和省略
- **说教感**：总结式语言"她明白了什么什么道理"

润色时保持情节不变，字数控制在±15%范围内。

**跳过润色**（快速生成时）：

```python
project = await generator.generate_novel(
    genre=NovelGenre.TIANYUAN_YANQING,
    mode=GenerationMode.QUICK,
    enable_polish=False  # 跳过润色阶段
)
```

**对已有项目单独润色**：

```python
result = await generator.polish_project(
    project=project,
    ctx=ctx,
    requirements="保持田园风格，增加五感细节"
)
```

### 自定义提示词模板

1. 在 `src/novel_generator/templates/` 下创建新类型文件夹
2. 添加6个必需的Jinja2模板文件（含 `polish.jinja2`）
3. 在 `models.py` 的 `NovelGenre` 枚举中添加新类型
4. 在 `prompt_templates.py` 的 `BUILTIN_TEMPLATES` 中注册模板路径

### 智能章节生成策略

系统会优先生成关键章节（开篇、高潮、结局），确保故事主线完整，然后填充中间章节。可在 `generator.py` 的 `_generate_chapters_smart()` 中自定义策略。

### 断点续传

生成过程中断后，系统会自动保存进度。可通过以下方式恢复：

**CLI方式（推荐）**：

```bash
python -m src.novel_generator.cli
# 选择 "2. 恢复已有项目"
# 从列表中选择要恢复的项目
```

系统会智能检测：
- ✓ 已完成的阶段（世界观、角色、情节、大纲）
- ✓ 已生成的章节（自动跳过）
- ✓ 已润色的章节（避免重复润色）

**编程方式**：

```python
# 恢复项目生成
project = await generator.resume_generation(
    project_id="novel_eb2d33af",
    enable_polish=True,  # 是否启用润色
    polish_requirements="保持田园风格，增加五感细节",
    on_progress=print_progress
)
```

**查看项目进度**：

```python
from src.novel_generator.context_manager import ContextManager

ctx = ContextManager.load_from_project_id("novel_eb2d33af", output_dir)
project = ctx.project

print(f"当前阶段: {project.current_stage}")
print(f"阶段状态: {project.stage_status}")
print(f"已生成章节: {ctx.get_generated_chapters()}")
print(f"缺失章节: {ctx.get_missing_chapters(30)}")
print(f"已润色章节: {ctx.get_polished_chapters()}")
```

**断点续传特性**：
- 自动检测所有6个阶段的完成情况
- 跳过已完成的阶段，从中断处继续
- 章节生成支持智能续传（只生成缺失的章节）
- 润色阶段支持增量处理（只润色未处理的章节）
- 所有进度保存在 `metadata.json` 中
# 继续执行未完成的阶段...
```

## 开发与测试

```bash
# 安装开发依赖（含测试、格式化、类型检查工具）
pip install -r requirements-dev.txt

# 运行测试
pytest tests/ -v

# 代码格式化
black src/

# 类型检查
mypy src/
```

## 技术栈

- **Python 3.8+**
- **Pydantic**: 数据验证和模型定义
- **Jinja2**: 提示词模板引擎
- **Anthropic SDK / OpenAI SDK**: LLM API调用（DeepSeek 复用 OpenAI 兼容接口）
- **asyncio**: 异步生成流程

## License

MIT