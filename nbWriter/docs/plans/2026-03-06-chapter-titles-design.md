# 章节标题功能设计文档

**日期**: 2026-03-06
**功能**: 为小说生成系统的章节添加标题

## 需求概述

当前章节文件只有 `# 第X章`，缺少具体标题。需要从大纲中提取标题并应用到章节文件中。

## 设计决策

### 1. 标题来源策略（混合方式）
- **优先级1**: 从大纲文件中提取标题
- **优先级2**: 如果提取失败，使用默认格式 `第X章`
- **降级机制**: 确保提取失败不影响生成流程

### 2. 标题格式
统一使用：`# 第X章 标题文字`

示例：
```markdown
# 第1章 桂花巷的旧信封

民国十五年，秋。
...
```

### 3. 已有章节处理
- 自动更新所有已生成章节的标题
- 在 `resume_generation()` 时提供选项让用户决定是否更新
- 提供独立的批量更新方法

## 技术实现

### 1. 标题提取函数

```python
def extract_chapter_title(outline: str, chapter_number: int) -> Optional[str]:
    """从大纲中提取章节标题

    支持的格式：
    - ## 第X章：标题
    - ## 第X章: 标题
    - ## 第X章 标题
    """
    import re

    patterns = [
        rf"##\s*第{chapter_number}章[：:]\s*(.+?)(?:\n|$)",
        rf"##\s*第{chapter_number}章\s+(.+?)(?:\n|$)",
    ]

    for pattern in patterns:
        match = re.search(pattern, outline)
        if match:
            title = match.group(1).strip()
            # 移除可能的标记符号
            title = re.sub(r'^[🔖\s]+', '', title)
            return title

    return None
```

### 2. 章节生成流程改进

在 `ChapterGenerationStage.execute()` 中：

1. 读取大纲文件
2. 调用 `extract_chapter_title()` 提取标题
3. 如果提取失败，使用默认格式并记录日志
4. 生成章节内容时，在开头插入带标题的一级标题
5. 保存章节文件

### 3. 批量更新已有章节

在 `ContextManager` 中添加：

```python
def update_chapter_titles(self, outline: str, on_progress: Optional[Callable] = None) -> dict:
    """批量更新已有章节的标题"""
    chapters_dir = self.project_dir / "chapters"
    if not chapters_dir.exists():
        return {"updated": 0, "failed": 0, "message": "章节目录不存在"}

    updated = 0
    failed = 0
    chapter_files = sorted(chapters_dir.glob("chapter-*.md"))

    for idx, chapter_file in enumerate(chapter_files, 1):
        chapter_number = int(chapter_file.stem.split('-')[1])

        # 提取标题
        title = extract_chapter_title(outline, chapter_number)
        if not title:
            failed += 1
            if on_progress:
                on_progress(f"⚠️  第{chapter_number}章未找到标题")
            continue

        # 读取章节内容
        content = chapter_file.read_text(encoding='utf-8')

        # 替换第一行标题
        lines = content.split('\n')
        if lines[0].startswith('# 第'):
            lines[0] = f"# 第{chapter_number}章 {title}"
            updated_content = '\n'.join(lines)
            chapter_file.write_text(updated_content, encoding='utf-8')
            updated += 1

            if on_progress:
                on_progress(f"✓ 已更新第{chapter_number}章标题 ({idx}/{len(chapter_files)})")

    return {
        "updated": updated,
        "failed": failed,
        "message": f"已更新 {updated} 章，失败 {failed} 章"
    }
```

### 4. CLI 集成

在 `resume_project()` 中添加：

```python
# 询问是否更新标题
print("\n是否更新已有章节的标题？")
print("1. 是（推荐，统一格式）")
print("2. 否（保持原样）")
update_titles_choice = input("请选择（默认1）: ").strip() or "1"

if update_titles_choice == "1":
    # 读取大纲
    outline_file = ctx.project_dir / "plot" / "outline.md"
    if outline_file.exists():
        outline = outline_file.read_text(encoding='utf-8')
        result = ctx.update_chapter_titles(outline, on_progress=print_progress)
        print(f"\n{result['message']}")
```

## 错误处理

1. **大纲文件不存在**: 跳过标题提取，使用默认格式
2. **标题提取失败**: 使用默认格式 `第X章`，记录警告日志
3. **文件读写错误**: 捕获异常，继续处理下一章节

## 向后兼容

- 旧项目不会因为标题功能而无法运行
- 如果大纲格式不规范，自动降级到默认标题
- 用户可以选择不更新已有章节

## 测试要点

1. 测试从标准格式大纲中提取标题
2. 测试大纲格式不规范时的降级机制
3. 测试批量更新已有章节
4. 测试新生成章节自动带标题
5. 测试中文冒号和英文冒号的兼容性

## 实施步骤

1. 在 `stages.py` 中添加 `extract_chapter_title()` 函数
2. 修改 `ChapterGenerationStage.execute()` 方法
3. 在 `context_manager.py` 中添加 `update_chapter_titles()` 方法
4. 修改 `cli.py` 中的 `resume_project()` 函数
5. 测试功能
6. 更新 README 文档
