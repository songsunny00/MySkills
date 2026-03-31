---
name: dingtalk-table-webhook
description: Use when the user wants to add a record into a DingTalk table through an automation webhook, especially when they describe the record in natural language, provide a Markdown file path as the content source, or need field validation, a field-summary preview, and explicit confirmation before sending. Image recognition is opt-in — only enabled when the user explicitly requests it.
---

# dingtalk-table-webhook

## Overview

Turn natural-language record requests into a configured DingTalk table automation webhook payload.

Core principle: **read project config → fill fields → validate → preview → confirm → send.**

When a Markdown file path is provided, `原始内容` comes from that file (content passed through as-is); controlled default filling applies to other business fields.

## When to Use

- User wants to add a record to a DingTalk table via automation webhook
- User describes the record in natural language or provides a Markdown file path
- User needs field validation, enum checking, or a preview before sending

Do not use when the task is only to explain DingTalk APIs, for bulk import, or when there is no project config.

## Required Inputs

1. Read config from `skills/dingtalk-table-webhook/dingtalk-table-webhooks.json`. Do NOT read from `skills-config/`.
2. If the file does not exist, tell the user to create it and stop.
3. Never guess the webhook schema — follow config exactly.

Webhook URL: use `webhook.env` env var if set; otherwise `webhook.url`; otherwise stop and ask.

Do not echo full webhook URLs to the user.

## Config Validation for Defaults

If a `defaults` node is present, validate before proceeding:

| Default key | Constraint |
|---|---|
| `sharer` | Must be `stringArray`; `fields.sharer` must exist and be type `stringArray` |
| `category` | Must be in `fields.category.options`; `fields.category` must be type `enum` |
| `trigger` | Must be a string; `fields.trigger` must exist and be type `string` |
| `creator` | Must be a string; `fields.creator` must exist and be type `string` |

Any violation → config error, block execution. Never silently ignore.

## Execution Flow

### 1. Select target table

Match user request against `triggers` in config (exact phrase match only, no fuzzy matching).

- Longer matching trigger phrase wins over shorter.
- One match → use it. No match + one table → use it. Otherwise → ask user.

### 2. Extract business fields

Extract only fields defined in the selected table's config. Do not invent values, auto-correct enums, or infer member IDs.

### 3. Markdown file input

Recognize `markdownFile` only from explicit labels: `Markdown 文件：`, `Markdown 文件路径：`, `md路径：`.

Do not extract from code blocks, example text, links, or generic file mentions.

If the label is present but value is empty → stop and ask. If multiple paths resolve to different files → ask user to choose.

### 4. Markdown file path resolution

- Strip surrounding quotes.
- Absolute paths: use directly. Relative paths: resolve from workspace root, then git root.
- Do not scan directories or use the currently open editor file.

### 5. Controlled default filling (markdownFile present only)

Read the Markdown file first so title/content values are available. Explicit user input always wins.

| Field | Fallback order |
|---|---|
| title | User input → first `#` heading → first non-empty text fragment → filename (without `.md`) |
| date | User input → today `YYYY-MM-DD` |
| sharer | User input → `defaults.sharer` → leave empty (optional) |
| creator | User input → `defaults.creator` → leave empty (optional) |
| category | User input → `defaults.category` → `技术动态` (only if in `options`) |
| trigger | User input → `defaults.trigger` → `前端分享` (only if `fields.trigger` exists) |

The `技术动态` and `前端分享` last-resorts are narrowly scoped share-record defaults, not generic fallbacks.
Final category must pass exact enum validation regardless of source.
If no `trigger` field in config, do not inject a trigger value.

### 6. Content source

When `markdownFile` is present, ignore any chat-provided content. `原始内容` must come only from the file.

### 7. Markdown content generation

1. Validate file path. Read as UTF-8.
2. **Images are skipped by default.** Enable image recognition only when the user explicitly requests it (e.g. `识别图片`, `需要识别图片`, `处理图片`).
3. If images are skipped: use file content as-is.
4. If images are enabled: replace each image reference at its original position with image output (see §8). All other content passes through unchanged — do not reformat or summarize non-image text.

Block if: file is unreadable, missing, not `.md`, or produces blank output.
Exception: file contains only images and all fail → keep failure notes, do not block.

### 8. Image handling (opt-in only)

When image recognition is enabled:

- Flowchart-like image → output structured `节点 -> 节点` relations.
- Other readable image → output a normal summary.
- Unreadable or unsupported source → insert failure note at that position, do not block.

Supported sources: local paths (relative to MD file or absolute), inline `![alt](path)`, reference-style.
Unsupported (failure note): `http://https://` URLs, `data:` URIs, HTML `<img>` tags.

### 9. Validate

- All required fields present (after default filling if markdownFile used)
- Enum values exactly match configured options
- Date fields in `YYYY-MM-DD`; if ambiguous → ask, do not guess
- Array fields match configured type

Ask for all missing fields in one message.

### 10. Build payload

Use config keys (`recordsKey`, `fieldsKey`). Build as structured data and serialize with `json.dump`. Do not hand-build JSON strings.

### 11. Confirm before sending

Show:
- Target table label
- All field values
- `原始内容来源: Markdown 文件 <path>` (if applicable)

Ask for explicit confirmation. Never send on implied intent.

### 12. Send the webhook

After confirmation, pipe payload via stdin to the send script — no temp file needed:

```python
import json, subprocess, sys
payload = { ... }
proc = subprocess.run(
    [sys.executable, "skills/dingtalk-table-webhook/scripts/send_webhook.py", "-", "<table_key>"],
    input=json.dumps(payload, ensure_ascii=False),
    capture_output=True, text=True
)
print(proc.stdout)
if proc.returncode != 0:
    print(proc.stderr)
```

Do NOT use the Write tool to produce a JSON file — it does not escape special characters correctly.

### 13. Report result

Report: table name, HTTP status, response summary. On failure, note likely cause (missing config, invalid enum, malformed payload, webhook rejection).

## Interaction Rules

- Ask for all missing required fields at once, not one per turn.
- For invalid enums: show allowed options, do not silently map.
- Do not expose full webhook URLs or write secrets to repo files.

## Output Format

**Before confirmation:**
```
目标表：<label>

准备写入的记录：
- <field>: <value>
- 原始内容来源: Markdown 文件 <path>（如适用）

请确认是否发送。
```

**After sending:**
```
已发送到：<label>
- HTTP 状态：<status>
- 结果：<short summary>
```

## Checklist

- [ ] Config from `skills/dingtalk-table-webhook/dingtalk-table-webhooks.json` (not `skills-config/`)
- [ ] `defaults` validated (types, enum membership)
- [ ] Target table selected
- [ ] Default filling applied (markdownFile present only)
- [ ] Missing required fields collected in one turn
- [ ] Enum values validated exactly
- [ ] Markdown file read; non-image content passed through as-is
- [ ] Images skipped unless user explicitly opted in
- [ ] Chat content ignored when markdownFile present
- [ ] Payload sent via stdin to `send_webhook.py` (no temp file, no Write tool for JSON)
- [ ] Preview shown; explicit confirmation received
- [ ] Result reported
