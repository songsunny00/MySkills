# 断点续传使用指南

## 功能概述

断点续传功能允许你在小说生成过程中随时中断（如网络问题、API限额、手动停止等），并在之后从中断处继续生成，无需重新开始。

## 工作原理

系统会在每个关键节点自动保存进度：

1. **阶段级保存**：每完成一个阶段（世界观、角色、情节、大纲、章节、润色），状态会保存到 `metadata.json`
2. **章节级保存**：每生成一章，立即保存到 `chapters/chapter-XXX.md`
3. **润色标记**：每润色完一章，在 `metadata.json` 中标记该章节已润色

## 使用方式

### 方式一：CLI交互式恢复（推荐）

```bash
# 1. 启动CLI
python -m src.novel_generator.cli

# 2. 选择 "2. 恢复已有项目"

# 3. 从列表中选择项目
# 系统会显示：
#   - 项目ID
#   - 小说类型
#   - 目标字数
#   - 已生成章节数
#   - 当前阶段

# 4. 选择是否启用润色
# 5. 系统自动检测并继续生成
```

### 方式二：编程方式恢复

```python
import asyncio
from pathlib import Path
from src.novel_generator.config import LLMConfig, ProjectConfig
from src.novel_generator.generator import NovelGenerator

async def resume():
    # 配置
    project_config = ProjectConfig.create(".")
    llm_config = LLMConfig(provider="anthropic")

    # 创建生成器
    generator = NovelGenerator(project_config, llm_config)

    # 恢复生成
    project = await generator.resume_generation(
        project_id="novel_eb2d33af",  # 替换为你的项目ID
        enable_polish=True,
        polish_requirements="保持田园风格",
        on_progress=lambda msg: print(f"[进度] {msg}")
    )

    print(f"完成！项目路径: {project_config.output_dir / project.project_id}")

asyncio.run(resume())
```

### 方式三：查看项目进度

```python
from pathlib import Path
from src.novel_generator.context_manager import ContextManager

# 加载项目
ctx = ContextManager.load_from_project_id("novel_eb2d33af", Path("output"))
project = ctx.project

# 查看进度
print(f"当前阶段: {project.current_stage}")
print(f"阶段状态: {project.stage_status}")

# 章节进度
chapter_count = project.target_word_count // 2000
generated = ctx.get_generated_chapters()
missing = ctx.get_missing_chapters(chapter_count)
polished = ctx.get_polished_chapters()

print(f"\n章节进度: {len(generated)}/{chapter_count}")
print(f"缺失章节: {missing}")
print(f"已润色: {len(polished)}/{len(generated)}")
```

## 智能检测机制

恢复时，系统会自动检测：

### 1. 阶段完成情况

```python
stage_status = {
    "worldbuilding": "completed",  # ✓ 已完成
    "characters": "completed",     # ✓ 已完成
    "plot": "completed",           # ✓ 已完成
    "outline": "completed",        # ✓ 已完成
    "chapters": "in_progress",     # ⏳ 进行中
    "polish": "pending"            # ⏸️ 未开始
}
```

- **completed**：跳过该阶段
- **in_progress** 或 **pending**：重新执行该阶段

### 2. 章节生成进度

系统会扫描 `chapters/` 目录，检测已存在的章节文件：

```
chapters/
├── chapter-001.md  ✓ 已生成
├── chapter-002.md  ✓ 已生成
├── chapter-003.md  ✓ 已生成
├── chapter-005.md  ✓ 已生成
└── chapter-030.md  ✓ 已生成
```

恢复时会：
- 跳过已存在的章节（1, 2, 3, 5, 30）
- 只生成缺失的章节（4, 6-29）

### 3. 润色进度

系统会检查 `metadata.json` 中的 `polished_chapters` 字段：

```json
{
  "polished_chapters": [1, 2, 3]
}
```

恢复润色时会：
- 跳过已润色的章节（1, 2, 3）
- 只润色未处理的章节（4-30）

## 常见场景

### 场景1：生成到一半网络中断

```bash
# 生成过程中按 Ctrl+C 或网络断开
[进度] 生成关键章节: 第1章
[进度] 生成关键章节: 第21章
^C 用户中断生成

# 稍后恢复
python -m src.novel_generator.cli
# 选择 "2. 恢复已有项目"
# 系统会从第22章继续
```

### 场景2：只想补充缺失的章节

```python
# 手动删除了某些章节，想重新生成
await generator.resume_generation(
    project_id="novel_xxxxx",
    enable_polish=False  # 跳过润色，只生成章节
)
```

### 场景3：只想对已有章节润色

```python
# 章节已全部生成，只想润色
await generator.resume_generation(
    project_id="novel_xxxxx",
    enable_polish=True,
    polish_requirements="增加五感描写，减少形容词"
)
# 系统会检测到章节已完成，直接进入润色阶段
```

### 场景4：修改某章后重新生成后续

```bash
# 1. 手动编辑 chapter-010.md
# 2. 删除 chapter-011.md 到 chapter-030.md
# 3. 恢复生成
python -m src.novel_generator.cli
# 系统会保留 chapter-001 到 chapter-010
# 重新生成 chapter-011 到 chapter-030
```

## 注意事项

### ✅ 推荐做法

1. **定期备份**：虽然系统会自动保存，但建议定期备份 `output/` 目录
2. **分批生成**：对于超长篇（10万字+），可以分批生成，每次生成一部分章节
3. **先测试后量产**：先用小字数（2万字）测试流程，确认无误后再生成长篇

### ⚠️ 注意事项

1. **不要手动修改 metadata.json**：除非你清楚每个字段的含义
2. **章节编号要连续**：如果手动删除章节，确保编号连续（如删除 5-10，不要只删除 7）
3. **润色会覆盖原文**：润色阶段会覆盖原始章节，建议先备份
4. **API限额**：注意LLM提供商的API限额，避免超额

### 🐛 故障排查

**问题1：恢复时提示"项目不存在"**

```bash
# 检查项目ID是否正确
ls output/
# 应该能看到 novel_xxxxx 目录

# 检查 metadata.json 是否存在
ls output/novel_xxxxx/metadata.json
```

**问题2：恢复后重新生成了已有章节**

```bash
# 检查章节文件命名是否正确
ls output/novel_xxxxx/chapters/
# 应该是 chapter-001.md, chapter-002.md 格式
# 不是 chapter_1.md 或 第1章.md
```

**问题3：润色阶段重复处理同一章节**

```python
# 检查 polished_chapters 字段
import json
with open("output/novel_xxxxx/metadata.json") as f:
    data = json.load(f)
    print(data.get("polished_chapters", []))

# 如果为空，说明润色标记未生效
# 可能是旧版本代码，需要更新
```

## 高级用法

### 自定义恢复策略

```python
from src.novel_generator.context_manager import ContextManager

# 加载项目
ctx = ContextManager.load_from_project_id("novel_xxxxx", output_dir)

# 手动修改阶段状态（强制重新生成某阶段）
ctx.project.stage_status["outline"] = "pending"
ctx.save_metadata()

# 恢复生成（会重新生成大纲）
await generator.resume_generation(project_id="novel_xxxxx")
```

### 批量恢复多个项目

```python
from pathlib import Path

output_dir = Path("output")
for project_dir in output_dir.iterdir():
    if project_dir.is_dir() and (project_dir / "metadata.json").exists():
        try:
            await generator.resume_generation(
                project_id=project_dir.name,
                enable_polish=True
            )
            print(f"✓ {project_dir.name} 完成")
        except Exception as e:
            print(f"✗ {project_dir.name} 失败: {e}")
```

## 示例代码

完整示例见 [examples/resume_example.py](../examples/resume_example.py)

```bash
# 运行示例（需要先修改项目ID）
python examples/resume_example.py
```