# 含表格与代码块的分享

这份文档用于验证表格、代码块和链接能被稳定转换为纯文本。

## 字段对照表

| 字段 | 类型 | 说明 |
|------|------|------|
| 标题 | string | 分享标题 |
| 分享人 | stringArray | 成员 ID 数组 |
| 类别 | enum | 技术动态 / 使用心得 / 推荐安利 |

## 配置示例

代码如下：

```json
{"tables": {"share_records": {"label": "分享记录表"}}}
```

更多文档见 [config-schema.md](../references/config-schema.md)。
