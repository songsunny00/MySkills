# 字段类型说明

| type | 说明 | 示例 |
|------|------|------|
| `string` | 普通字符串 | `"Claude Code 使用心得"` |
| `stringArray` | 字符串数组，用于成员 ID | `["257700519"]` |
| `date` | 日期字符串，建议格式 YYYY-MM-DD | `"2026-03-23"` |
| `enum` | 枚举值，必须与 `options` 中的值完全一致 | `"技术动态"` |

## 配置文件路径

skill 默认读取：

```
skills/dingtalk-table-webhook/dingtalk-table-webhooks.json
```

此文件不应提交到 Git（包含 webhook 地址/密钥时）。

仓库中保留：

```
skills/dingtalk-table-webhook/dingtalk-table-webhooks.example.json
```

作为格式参考，`webhook.url` 置空即可，`webhook.env` 应填写环境变量名，例如 `DT_SHARE_WEBHOOK_URL`，而不是直接填写 webhook URL。

## Webhook URL 来源优先级

1. 环境变量（由 `webhook.env` 字段指定，如 `DT_SHARE_WEBHOOK_URL`）
2. 配置文件直写 URL（`webhook.url` 字段）

安全建议：正式环境建议使用环境变量，不要把真实 webhook URL 提交到仓库。

## 运行时输入说明

`markdownFile` / `Markdown 文件` 是 skill 调用时的运行时输入，不属于 `skills/dingtalk-table-webhook/dingtalk-table-webhooks.json` 配置结构。

配置文件仍只负责：
- webhook URL 来源
- request wrapper keys
- 字段映射
- required 约束
- enum options
- defaults 默认值规则

当用户显式提供 Markdown 文件路径时，skill 会把生成后的纯文本写入 `content` 对应的目标字段。

仅在 Markdown 导入流程中，如果提供了 `markdownFile`，skill 可以在 required 阻断前，先根据 defaults 和已文档化的回退规则自动补齐缺失的业务字段。
该行为只适用于 Markdown-only 场景；无效 defaults 属于配置错误，不能被静默忽略。

## defaults 配置说明

`defaults` 是可选对象，用于为 Markdown-only 导入流程提供业务字段默认值。

约束如下：
- `defaults.sharer` 必须为 `stringArray`，并与 `fields.sharer` 的类型保持一致
- `defaults.category` 必须匹配 `fields.category.options` 中的枚举值，且 `fields.category` 必须是 `enum`
- `defaults.trigger` 必须为字符串，且要求存在 `fields.trigger`，其类型必须为 `string`
- 任一 defaults 配置不合法时，应视为配置错误，不能静默忽略

## 完整配置示例

```json
{
  "tables": {
    "share_records": {
      "label": "分享记录表",
      "webhook": {
        "url": "",
        "env": "DT_SHARE_WEBHOOK_URL"
      },
      "triggers": ["前端分享", "AI分享", "分享"],
      "request": {
        "recordsKey": "records",
        "fieldsKey": "fields"
      },
      "fields": {
        "title": {
          "target": "分享标题",
          "type": "string",
          "required": true
        },
        "sharer": {
          "target": "分享人",
          "type": "stringArray",
          "required": true
        },
        "date": {
          "target": "分享时间",
          "type": "date",
          "required": true
        },
        "category": {
          "target": "类别",
          "type": "enum",
          "required": true,
          "options": ["技术动态", "使用心得", "推荐安利"]
        },
        "content": {
          "target": "原始内容",
          "type": "string",
          "required": true
        }
      }
    }
  }
}
```
