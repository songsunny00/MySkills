---
name: translate-skills
description: 当用户想为 Skills 批量添加中文翻译时使用，支持全局 agent 目录（~/.claude/skills、~/.cursor/skills、~/.trae-cn/skills 等）以及当前项目目录下的 .claude/skills、.cursor/skills 等。适用场景：用户说"给 skills 加中文"、"汉化所有 skill"、"翻译当前项目的 skill"。
license: MIT
---

# translate-skills

## 概述

扫描全局 agent 目录和当前项目目录，对 SKILL.md 的 frontmatter 中 `name` 和 `description` 尚无中文的 skill 自动添加中文翻译，仅修改这两个字段，不动其他内容。

## 扫描目录

### 全局目录（按顺序扫描，不存在则跳过）

```
~/.claude/skills/
~/.cursor/skills/
~/.trae-cn/skills/
~/.trae/skills/
~/.qoder/skills/
```

### 当前项目目录（在当前工作目录下查找）

```
<cwd>/.claude/skills/
<cwd>/.cursor/skills/
<cwd>/.trae-cn/skills/
<cwd>/.trae/skills/
<cwd>/.qoder/skills/
```

**scope 说明（默认扫描全部）：**

- **未指定 / 说"全部" / 说"所有"** → 全局目录 + 当前项目目录全部扫描，**直接开始，无需确认**
- 用户明确说"只翻 cursor" / "只翻 .cursor" → 只扫描所有目录中的 `.cursor/skills`
- 用户明确说"只翻 claude" / "只翻 .claude" → 只扫描所有目录中的 `.claude/skills`
- 用户明确说"当前项目" / "这个项目" → 只扫描 `<cwd>/` 下的所有 skills 目录
- 用户明确说"全局" → 只扫描 `~/` 下的所有 skills 目录

**除非用户明确指定范围，否则一律全量扫描。**

**每个目录下的结构：** `<skill-name>/SKILL.md`

## 执行流程

### ⚠️ 铁律：先扫描全量清单，再开始翻译

**禁止**只处理第一个找到的目录就汇报完成。必须先收集所有目录的完整文件列表，确认无遗漏后再翻译。

---

### 第一步：一次性扫描所有目录，输出完整清单

用**单条命令**扫描全部目标目录，输出所有 SKILL.md 路径：

```bash
# 全局目录（一条命令，2>/dev/null 忽略不存在的目录）
find ~/.claude/skills ~/.cursor/skills ~/.trae-cn/skills ~/.trae/skills ~/.qoder/skills \
  -name "SKILL.md" 2>/dev/null | sort

# 当前项目目录（先获取 CWD）
CWD=$(pwd)
find "$CWD/.claude/skills" "$CWD/.cursor/skills" "$CWD/.trae-cn/skills" \
  "$CWD/.trae/skills" "$CWD/.qoder/skills" \
  -name "SKILL.md" 2>/dev/null | sort
```

扫描完成后，**列出所有找到的路径**（按目录分组），**直接进入第二步，无需等待用户确认**。

### 第二步：批量读取 frontmatter，建立翻译清单

对第一步找到的**每一个**路径，读取其 frontmatter，检查 `name` 和 `description` 字段：

- **已有中文**（含 `\u4e00-\u9fff` 字符）→ 标记为「跳过」
- **无中文** → 标记为「待翻译」

**输出格式示例（必须列出全部，不能省略）：**

```
待翻译（5个）：
  ~/.claude/skills/canvas-design/SKILL.md
  ~/.trae-cn/skills/canvas-design/SKILL.md
  ~/.cursor/skills/docx/SKILL.md
  ...

跳过（已有中文，12个）：
  ~/.claude/skills/find-skills/SKILL.md
  ...
```

### 第三步：批量翻译并写入

**翻译规则：**

| 字段          | 原格式        | 翻译后格式             | 要求                                                        |
| ------------- | ------------- | ---------------------- | ----------------------------------------------------------- |
| `name`        | `find-skills` | `find-skills 技能查找` | 英文名保留，后加中文（**4-6 字**）                          |
| `description` | 英文描述      | 完整中文描述           | 保持原意，**中文写详细**，保留 "Use when..." 的触发条件语义 |

**翻译格式示例：**

```yaml
# ❌ 改前
name: find-skills
description: Helps users discover and install agent skills when they ask "how do I do X"

# ✅ 改后
name: find-skills 技能查找
description: 当用户询问"如何做 X"、"有没有 skill 能做 X"、或希望扩展 agent 能力时使用。此技能帮助用户在 skills.sh 和 skillsmp.com 等来源中搜索并安装合适的 agent 技能包。
```

**name 中文部分命名原则：**

- 动词优先：查找、审查、调试、翻译、构建
- 4-6 字，准确概括功能
- 不用"的"结尾

**description 翻译原则：**

- 保留触发条件（"Use when..." 对应"当...时使用"）
- 保留关键症状词、场景词
- 不翻译代码命令、文件名、包名
- 比英文原文稍详细，补充使用场景

### 第四步：写入文件

使用 Edit 工具只替换 frontmatter 中的 `name:` 和 `description:` 行，不修改其他内容。

```
old_string: "name: find-skills\ndescription: Helps users discover..."
new_string:  "name: find-skills 技能查找\ndescription: 当用户询问..."
```

**注意 description 引号格式**：若原 description 为 `description: "..."` 带引号格式，替换后去掉引号，改为普通格式：

```
description: 当用户...（无引号）
```

### 第五步：汇报结果

**汇报前必须确认：第一步扫描到的每个目录都已处理完毕，无遗漏。**

完成后输出汇总表，按目录分组：

```
## 翻译完成

| 来源目录 | Skill | 修改内容 |
|---------|-------|---------|
| ~/.claude/skills | find-skills | name + description |
| ~/.trae-cn/skills | canvas-design | name + description |
| ~/.cursor/skills | xlsx | name + description |
| <cwd>/.claude/skills | my-custom-skill | name + description |
| ...  | ...   | ...     |

共修改 X 个 skill，跳过 Y 个（已有中文）。
扫描目录：~/.claude/skills ✓  ~/.cursor/skills ✓  ~/.trae-cn/skills ✓  ~/.trae/skills -（不存在）  ~/.qoder/skills -（不存在）
```

## 注意事项

- **只改 frontmatter**：`---` 之间的 `name` 和 `description`，正文内容不动
- **description 多行处理**：若原 description 跨多行，替换时保持单行格式
- **跨目录去重**：同名 skill 在不同目录中独立处理（各自可能翻译状态不同）
- **不存在的目录**：静默跳过，不报错
- **同步翻译**：同一个 skill（如 canvas-design）在多个编辑器目录下各自独立存在，必须逐一翻译，不能只翻一个目录就停止

## 常见错误

| 错误                                 | 原因                                           | 修复                                                                      |
| ------------------------------------ | ---------------------------------------------- | ------------------------------------------------------------------------- |
| 只翻译了第一个目录就汇报完成         | 未先收集全量清单                               | 必须先执行第一步单条命令扫描全部目录                                      |
| name 中文超过 6 字                   | 过度描述                                       | 精简到 4-6 字动宾结构                                                     |
| description 只翻译了一句             | 省略触发条件                                   | 完整翻译，保留 "Use when..." 对应的中文句式                               |
| 把代码命令也翻译了                   | 误译技术术语                                   | 保留 `npx`、`skill add`、文件名等原文                                     |
| 修改了 frontmatter 之外的内容        | 替换范围过大                                   | 严格限定在 `---` 之间的两行                                               |
| description 写入后换行丢失           | 引号格式替换时 `\n` 被吞                       | 替换后检查 description 末尾是否有换行，若无则补上                         |
| description 末尾出现 `\x01` 控制字符 | Python `re.sub` 中 `\1` 反向引用被误当字面字符 | 写入后用 `repr()` 检查原始字节，发现则 `content.replace('\x01', '')` 清除 |

## 来源与更新

- GitHub: https://github.com/songsunny00/MySkills/tree/main/skills/find-skills
