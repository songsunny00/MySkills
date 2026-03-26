---
name: dingtalk-table-webhook
description: Use when the user wants to add a record into a DingTalk table through an automation webhook, especially when they describe the record in natural language, provide a Markdown file path as the content source, want Claude to summarize screenshots or convert flowchart images into structured text, or need field validation, payload preview, and explicit confirmation before sending.
---

# dingtalk-table-webhook

## Overview

Use this skill to turn natural-language record requests into a configured DingTalk table automation webhook payload.

The core principle is: **read project config, map into the configured payload shape, fill defaults when a Markdown file is provided, ask for missing required fields once, preview the exact payload, and only send after explicit user confirmation.**

When a Markdown file path is explicitly provided, the `原始内容` field is generated from that file instead of chat text, and controlled default filling applies to other business fields.

## When to Use

Use this skill when the user:
- wants to add one record to a DingTalk table with an automation webhook
- describes the record in natural language instead of handing over final JSON
- provides a Markdown file path as the content source
- wants Claude to summarize images or convert flowcharts into structured text
- refers to share submission, AI share, frontend share, knowledge sharing, or similar write-in workflows
- wants Claude to validate fields, enum values, dates, or member IDs before sending

Do not use this skill when:
- the task is only to explain DingTalk APIs or webhook docs
- the user wants bulk import as the primary workflow
- there is no project configuration for the target table and the user only wants a generic example

## Required Inputs

Before doing anything else:
1. Read the project config file at `skills/dingtalk-table-webhook/dingtalk-table-webhooks.json`.
2. If it does not exist, read `skills/dingtalk-table-webhook/dingtalk-table-webhooks.example.json` if present and tell the user to create the real config at `skills/dingtalk-table-webhook/dingtalk-table-webhooks.json`.
3. Do NOT read from `skills-config/dingtalk-table-webhooks.json`. That path must be ignored even if the file exists there.
4. Never guess the webhook schema. Follow config exactly.

## Config Rules

Each table config should define:
- label
- webhook source
- trigger phrases
- request wrapper keys
- field mapping
- required fields
- enum options where applicable
- optional `defaults` node (see Default Values below)

Webhook URL resolution order:
1. If `webhook.env` exists and that environment variable is non-empty, use it.
2. Otherwise, if `webhook.url` is non-empty, use it.
3. Otherwise stop and ask the user to configure the webhook.

Treat webhook URLs as secrets. Do not echo the full URL back to the user unless they explicitly ask.

## Default Values

A table config may include a `defaults` node at the table level:

```json
"defaults": {
  "sharer": ["257700519"],
  "trigger": "前端分享",
  "category": "技术动态"
}
```

### Default value rules

- `defaults.sharer` — fills `sharer` when no explicit user input is provided; the value must be a `stringArray`
- `defaults.category` — fills `category` when no explicit user input is provided; the value must be one of the options in `fields.category.options`
- `defaults.trigger` — fills `trigger` when no explicit user input is provided; must be a `string`

### Config validation for defaults

Validate these constraints when reading the config. If any constraint is violated, report a config error and block execution:

- If `defaults.sharer` is present but is not a stringArray → config error, block execution
- If `defaults.category` is present but its value is not in `fields.category.options` → config error, block execution
- If `defaults.sharer` is present but `fields.sharer` is absent or not type `stringArray` → config error, block execution
- If `defaults.category` is present but `fields.category` is absent or not type `enum` → config error, block execution
- If `defaults.trigger` is present but is not a string → config error, block execution
- If `defaults.trigger` is present but `fields.trigger` is absent or not type `string` → config error, block execution
- If `defaults.sharer` is absent and the user provides no explicit sharer → block with error asking the user to provide a sharer or configure `defaults.sharer`

Do not silently ignore an invalid default value. Every config error must be surfaced.

## Execution Flow

### 1. Select the target table

Match the user request against configured table triggers.

- If an exact trigger match identifies one table, that table wins over any other non-exact or broader trigger matches.
- If exactly one table matches a trigger, use it.
- If no trigger matches but there is only one table in the config, use that table.
- If no trigger matches and there are multiple tables, ask the user to choose.
- If multiple tables match a trigger and no single exact trigger match wins, ask the user to choose.

This rule ensures that "only a Markdown file" input can still resolve to a table unambiguously when the config has exactly one table.

### 2. Extract business fields from natural language

Extract only configured business fields.

For the share-record case, this often means values like:
- title
- sharer
- date
- category
- content

These are semantic business keys in the skill contract. The actual DingTalk field names in the final payload come from the selected table config's `fields` mapping.

Do not invent values.
Do not auto-correct enum values silently.
Do not infer member IDs beyond configured defaults.

### 3. Markdown file input

If the user explicitly provides `Markdown 文件：`, `Markdown 文件路径：`, or `md路径：`, treat the value after that label as `markdownFile`.

Do not extract `markdownFile` from:
- code blocks
- example text
- generic file mentions
- Markdown links or other URLs

If multiple explicit Markdown paths are present:
- normalize them first (strip surrounding quotes, unify path separators, resolve equivalent relative paths)
- if they resolve to the same file, continue
- otherwise stop and ask the user to choose one

If the explicit label is present but the value is empty, stop and tell the user they are missing a Markdown file path.

### 4. Markdown file path resolution

- Strip surrounding quotes from the path before resolving (e.g. `"D:\my notes\share.md"` → `D:\my notes\share.md`).
- If the path is absolute (Windows `D:\...` or Unix `/...`), use it directly.
- If the path is relative, resolve it against the workspace root first; fall back to the git repository root.
- If neither workspace root nor repo root is determinable, reject the relative path and ask the user to provide an absolute path.
- Do not guess paths by scanning directories, opening recent files, or using the currently open editor file.

### 5. Controlled default filling (markdownFile present)

When `markdownFile` is present, perform controlled default filling before the required-field validation step. This is supplementation using only the approved fallback rules below — it is not guessing.

Explicit user input always takes precedence over any default or inferred value.

#### Title fallback chain

Apply in order; use the first that succeeds:

1. Explicit title provided by the user
2. Markdown heading text from the first heading line (e.g. `# 标题` → extracts `标题`)
3. First non-empty plain-text fragment from the Markdown conversion result that comes from textual Markdown content (for example heading, paragraph, list, table, blockquote, or code text) rather than an image summary block or image failure note
4. Filename without the `.md` extension

Title is considered missing only if all four sources fail.

#### Sharer fallback chain

1. Explicit sharer provided by the user
2. `defaults.sharer` from config

If both are absent, block and ask the user to provide a sharer (or configure `defaults.sharer`).

#### Date fallback chain

1. Explicit date provided by the user
2. Today's local date in `YYYY-MM-DD` format (do not use the Markdown file's timestamp)

#### Category fallback chain

1. Explicit category provided by the user
2. `defaults.category` from config
3. Hardcoded last-resort: `技术动态` — only if `fields.category` exists with type `enum` and `技术动态` is in its `options`

The final category value must pass exact enum validation regardless of its source.

#### Trigger fallback chain

1. Explicit trigger provided by the user
2. `defaults.trigger` from config
3. Hardcoded last-resort: `前端分享` — only if `fields.trigger` exists with type `string`

If the target table has no `trigger` field in its config, do not inject a trigger value at all.

### 6. Content source precedence

When `markdownFile` is present, ignore any chat-provided `内容` field. The final `原始内容` must come only from the Markdown conversion result.

### 7. Markdown content generation

When `markdownFile` is present:
1. Validate the file path.
2. Read the Markdown file as UTF-8.
3. Convert visible Markdown content into plain text using the element rules below.
4. Replace each image at its original position with one of:
   - a flowchart relation block
   - a normal image summary block
   - a failure block
5. Assemble the final plain-text result using the spacing rules below.

If the Markdown file is unreadable, missing, not a `.md` file, empty, or converts to a blank result (no non-whitespace text and no image output), stop before payload preview.

Exception: if the file contains only images and all images fail, do NOT block — the failure notes themselves form the final content.

### 8. Markdown element conversion rules

| Markdown element | Plain-text rule |
|---|---|
| Heading | Keep heading text, on its own line |
| Paragraph | Keep text as-is |
| Unordered / ordered list | One item per line |
| Link | Keep visible text; if text is empty, keep URL |
| Inline code | Keep code text |
| Code block | Keep code content, prepend `代码块：` |
| Blockquote | Convert to `引用：...` |
| Table | Expand each row as `列名: 值；列名: 值` |
| Thematic break (---) | Treat as paragraph separator only, no symbol |
| Inline HTML | Keep visible text only; do not preserve markup |

Edge cases:
- First row of a Markdown table is treated as the header (column names).
- Empty table cells keep their position (empty value).
- Irregular tables and complex nested HTML use best-effort readable text; do not block.
- No requirement to reproduce every Markdown/HTML detail; stable, readable plain text is sufficient.

### 9. Content assembly rules

Assemble the ordered fragments into the final plain text:
- Separate adjacent paragraphs with a single blank line.
- Each list item on its own line.
- Each expanded table row on its own line.
- Insert image replacement text as an independent block, with one blank line before and after.
- Strip trailing spaces from each line.
- Collapse more than two consecutive newlines into exactly two.
- Do not concatenate adjacent text fragments without any whitespace.

### 10. Image handling

If an image can be understood and its main information is expressed as nodes + arrows + sequence/branch relations, output structured `节点 -> 节点` text.

If the image is readable but not a flowchart, output a normal summary.

If the image cannot be read or uses an unsupported source, do not block the whole request. Insert a failure note at that exact position instead.

If the image type is uncertain but the image is readable, fall back to a normal summary.

Supported image sources:
- Markdown inline images: `![alt](path)`
- Markdown inline images with title: `![alt](path "title")`
- Markdown reference-style images: `![alt][ref]` + `[ref]: path`
- Relative paths (relative to the Markdown file's directory)
- Absolute local paths

Unsupported image sources (produce failure note, do not block):
- `http://` / `https://` remote URLs
- `data:` URI embedded images
- HTML `<img>` tags

### 11. Validate

Validate before building the final request:
- required fields must all be present (after controlled default filling if markdownFile was provided)
- enum values must be exact configured options
- if a date field is present, it must be converted to the configured output format before payload build; if the user input is ambiguous or cannot be converted with confidence, stop and ask for a clearer date instead of guessing
- array fields must match the configured type

If fields are missing, ask for all missing required fields in one message.
If an enum is invalid, reject it and show the allowed values.

### 12. Build payload

Build the final request body strictly from config.

Default shape for many DingTalk table automation webhooks:

```json
{
  "records": [
    {
      "fields": {
        "分享标题": "文章标题",
        "分享人": ["257700519"],
        "分享时间": "2026-03-23",
        "类别": "技术动态",
        "原始内容": "富文本内容"
      }
    }
  ]
}
```

But do not assume this shape globally. Use configured keys like `recordsKey` and `fieldsKey`.

### 13. Confirm before writing

Always present a concise preview before sending:
- target table label
- field summary
- exact JSON body

Then ask for explicit confirmation.

Never send the webhook on implied intent.
Never skip confirmation for convenience.

When `markdownFile` was used, include in the field summary:
- `原始内容来源: Markdown 文件 <path>`
- `已忽略聊天中的内容字段` (if applicable)

Field values that came from defaults or auto-inference are shown as their final values. Per-field source labels are not required in the preview.

### 14. Send the webhook

After explicit confirmation:
- send HTTP POST
- set `Content-Type: application/json`
- send the constructed JSON body unchanged

### 15. Report result

Report:
- selected table
- whether request was sent
- HTTP status code
- brief response summary

If the request fails, include the likely failure point:
- missing config
- invalid enum
- malformed payload
- remote webhook rejection

## Interaction Rules

### Missing fields

Ask for all missing required fields at once.

Good:
- "还缺 3 个字段：分享人、分享时间、类别。请一次补齐。"

Bad:
- asking one field per turn unless the user asked for guided mode

### Enum fields

If the user gives an enum not in config:
- do not silently map it
- do not choose the "closest" option
- show the allowed options and ask them to pick one

### Sensitive values

- Do not expose full webhook URLs unnecessarily.
- Do not write webhook secrets into repo files unless the user explicitly wants that.

## Output Format

Before confirmation, use this structure:

````markdown
目标表：<label>

准备写入的记录：
- <field>: <value>
- <field>: <value>
- 原始内容来源: Markdown 文件 <path> (如适用)
- 已忽略聊天中的内容字段（如适用）

请求体：
```json
{...}
```

请确认是否发送。
````

After sending, use this structure:

```markdown
已发送到：<label>
- HTTP 状态：<status>
- 结果：<short summary>
```

## Common Mistakes

- Guessing category from trigger words like "前端分享" or "AI分享"
- Guessing member IDs
- Sending before confirmation
- Hardcoding `records` and `fields` when the config defines different keys
- Echoing full webhook URLs into chat output
- Accepting fuzzy enum values instead of exact configured options
- Extracting `markdownFile` from code blocks or example text
- Not ignoring chat content when Markdown file is provided
- Reading config from `skills-config/dingtalk-table-webhooks.json` — this path must be ignored even if the file exists
- Silently ignoring an invalid `defaults.*` value instead of reporting a config error
- Applying default filling when `markdownFile` is NOT present

## Minimal Checklist

- [ ] Config read from `skills/dingtalk-table-webhook/dingtalk-table-webhooks.json` (not from `skills-config/`)
- [ ] Config `defaults` validated (type checks, enum membership)
- [ ] Target table selected
- [ ] Controlled default filling applied (if markdownFile present)
- [ ] Missing required fields collected in one turn if needed
- [ ] Enum values validated exactly
- [ ] Markdown file path validated (if provided)
- [ ] Markdown content generated (if file provided)
- [ ] Chat content ignored when Markdown file is present
- [ ] Payload preview shown
- [ ] Explicit confirmation received
- [ ] POST sent
- [ ] Result reported
