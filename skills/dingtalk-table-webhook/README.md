# dingtalk-table-webhook

**中文**

通过钉钉表格自动化 Webhook 新增记录的 Claude Code skill。

---

## 功能

| 功能 | 说明 |
|------|------|
| 自然语言驱动 | 用自然语言描述，skill 自动提取字段 |
| 多表可配置 | 通过 `skills/dingtalk-table-webhook/dingtalk-table-webhooks.json` 配置多张表 |
| 字段校验 | 必填检查、枚举精确校验、日期格式检查 |
| 一次性补齐 | 缺字段时一次列出全部，不逐个追问 |
| 发前确认 | 总是展示字段摘要预览，等待明确确认后才 POST |
| 双源 URL | 支持环境变量优先 + 配置文件回退 |
| Markdown 内容源 | 支持显式传入 `.md` 文件路径生成 `原始内容` |
| 图片处理 | 普通图片输出摘要，流程图输出结构化节点关系，也支持按用户要求直接跳过图片识别 |

---

## 快速开始

### 1. 创建配置文件

```bash
cp skills/dingtalk-table-webhook/dingtalk-table-webhooks.example.json skills/dingtalk-table-webhook/dingtalk-table-webhooks.json
```

编辑 `skills/dingtalk-table-webhook/dingtalk-table-webhooks.json`，填入 webhook URL 或对应环境变量名。

迁移说明：旧的根目录配置路径 `skills-config/dingtalk-table-webhooks.json` 已不再被该 skill 使用；运行时会忽略该旧路径。

### 2. 配置 Webhook URL（二选一）

**方式 A：环境变量（推荐）**

```bash
export DT_SHARE_WEBHOOK_URL="https://your-dingtalk-webhook-url"
```

**方式 B：直接写入配置文件**（不建议提交到 Git）

```json
{
  "tables": {
    "share_records": {
      "webhook": {
        "url": "https://your-dingtalk-webhook-url"
      }
    }
  }
}
```

### 3. 添加 .gitignore 条目

```
skills/dingtalk-table-webhook/dingtalk-table-webhooks.json
```

---

## 使用示例

### 基本用法（聊天内容）

```
帮我记一条前端分享：
标题：Claude Code 在代码审查中的应用
分享人：257700519
时间：2026-03-25
类别：使用心得
内容：今天分享了如何用 Claude Code review PR，效率提升明显。
```

### Markdown 文件作为内容源

```
帮我记一条前端分享：
标题：Claude Code 处理 Markdown 图片总结
分享人：257700519
时间：2026-03-25
类别：使用心得
Markdown 文件：skills/dingtalk-table-webhook/examples/markdown/basic-share.md
```

### 仅提供 Markdown 文件（使用默认值自动补齐）

```
帮我记一条分享：
Markdown 文件：skills/dingtalk-table-webhook/examples/markdown/basic-share.md
```

当提供 Markdown 文件路径时：
- `原始内容` 字段由 Markdown 文件内容生成
- 聊天中的 `内容` 字段会被忽略
- 若未显式提供，`分享人` 可由 `defaults.sharer` 自动补齐
- 若未显式提供，`类别` 可优先使用 `defaults.category`，否则在分享记录兼容场景下回退为 `技术动态`
- 若未显式提供，`触发词` 可优先使用 `defaults.trigger`（前提是表中定义了 `fields.trigger`），否则在分享记录兼容场景下回退为 `前端分享`
- 若未显式提供，`分享时间` 默认使用当天日期（`YYYY-MM-DD`）
- `标题` 会按“显式标题 -> Markdown 标题 -> Markdown 纯文本首段 -> 文件名”顺序回退
- 普通图片会被总结为文字描述
- 流程图图片会被转换为 `节点 -> 节点` 结构化文本
- 如果用户明确说可以不用识别图片，则图片会被完全跳过，不输出任何占位或失败说明
- 图片读取失败时输出失败说明，但不阻断整体流程
- 构造请求体时必须使用合法 JSON 序列化；即使内容里有引号、反斜杠或换行，也不能生成非法请求体

---

## Markdown 图片处理规则

| 图片类型 | 输出格式 |
|---------|---------|
| 流程图 | `[流程图识别]` + `节点 -> 节点` 关系行 |
| 普通图片 | `[图片总结：...]` |
| 失效图片 | `[图片处理失败：...]` |
| 远程 URL | `[图片处理失败：当前不支持远程图片 ...]` |
| 用户明确要求跳过图片 | 完全忽略图片，不输出任何占位文本 |

支持的图片来源：
- Markdown 行内图片 `![alt](path)`
- 相对路径（相对于 Markdown 文件所在目录）
- 本地绝对路径

不支持的图片来源（输出失败说明，不阻断）：
- `http://` / `https://` 远程 URL
- `data:` URI
- HTML `<img>` 标签

如果用户明确说“不用识别图片”“跳过图片”“图片可忽略”之类的意思，则所有图片都按不存在处理：不识别、不总结、不写失败说明，也不保留占位。若因此导致最终内容为空，则在预览前阻断。

### 预览与发送

发送前只展示目标表和字段摘要，不展示完整请求体 JSON；仍然必须得到用户的明确确认后才会发送。

请求体必须通过标准 JSON 序列化生成，不要手工拼接字符串。这样即使 `原始内容` 里含有引号、反斜杠、换行、Tab 或其他控制字符，也应保持请求体合法。

---

## 配置字段说明

详见 [references/config-schema.md](references/config-schema.md)。

---

## 触发词

默认配置的触发词包含：`前端分享`、`AI分享`、`分享`。

可在配置文件的 `triggers` 字段自定义。这里的表级 `triggers` 只用于路由和选择目标表；写入记录时的 `trigger` 是业务字段，由 `fields.trigger` / `defaults.trigger` 控制。在仅 Markdown 或默认补齐场景下，落库的 `trigger` 可能来自配置默认值，而不一定是用户原话。

---

## 安装

```bash
npx skills add https://github.com/songsunny00/MySkills --skill dingtalk-table-webhook -g -y
```
