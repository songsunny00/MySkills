# 一键生成小说系统

自动化生成50,000-80,000字中长篇小说的智能系统。

## 特性

- 🚀 一键启动，分阶段确认
- 📚 支持多种小说类型（玄幻、都市、言情等）
- 🎯 双模式：快速模式 / 详细模式
- 🔄 智能章节生成策略（关键章节优先）
- ✏️ 全面的用户控制和编辑能力
- 📦 完整项目输出（世界观、人物、大纲、章节）

## 安装

```bash
pip install -r requirements.txt
```

## 配置

创建 `.env` 文件：

```env
ANTHROPIC_API_KEY=your_api_key_here
# 或
OPENAI_API_KEY=your_api_key_here
```

## 使用

### CLI方式

```bash
python -m src.novel_generator.cli
```

### 编程方式

```python
import asyncio
from src.novel_generator.models import NovelGenre, GenerationMode
from src.novel_generator.config import LLMConfig, ProjectConfig
from src.novel_generator.generator import NovelGenerator

async def generate():
    project_config = ProjectConfig.create(".")
    llm_config = LLMConfig()

    generator = NovelGenerator(project_config, llm_config)

    project = await generator.generate_novel(
        genre=NovelGenre.XUANHUAN,
        mode=GenerationMode.QUICK,
        target_word_count=60000
    )

    print(f"生成完成: {project.project_id}")

asyncio.run(generate())
```

## 项目结构

生成的小说项目结构：

```
output/novel_xxxxx/
├── metadata.json          # 项目元数据
├── worldbuilding/
│   └── world.md          # 世界观设定
├── characters/
│   ├── protagonist.md    # 主角档案
│   └── ...
├── plot/
│   ├── plot_design.md    # 情节设计
│   └── outline.md        # 完整大纲
├── chapters/
│   ├── chapter-001.md
│   ├── chapter-002.md
│   └── ...
└── exports/              # 导出文件
```

## 生成流程

1. **类型分析与参数设定** - 选择类型和模式
2. **世界观构建** - 生成世界观设定
3. **角色设定** - 创建主角、配角、反派
4. **情节设计** - 规划主线和副线
5. **大纲生成** - 生成详细章节大纲
6. **章节生成** - 智能生成所有章节
7. **润色与导出** - 最终处理和导出

## 开发

运行测试：

```bash
pytest tests/ -v
```

## License

MIT