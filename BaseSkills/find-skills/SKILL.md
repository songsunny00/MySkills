---
name: find-skills
description: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.
---

# Find Skills

This skill helps you discover and install skills from the open agent skills ecosystem via two sources: **skills.sh** (CLI) and **skillsmp.com** (API).

## When to Use This Skill

Use this skill when the user:

- Asks "how do I do X" where X might be a common task with an existing skill
- Says "find a skill for X" or "is there a skill for X"
- Asks "can you do X" where X is a specialized capability
- Expresses interest in extending agent capabilities
- Wants to search for tools, templates, or workflows
- Mentions they wish they had help with a specific domain (design, testing, deployment, etc.)

## Source 1: skills.sh CLI

The Skills CLI (`npx skills`) is the package manager for the open agent skills ecosystem.

**Key commands:**

- `npx skills find [query]` - Search for skills interactively or by keyword
- `npx skills add <package>` - Install a skill from GitHub or other sources
- `npx skills check` - Check for skill updates
- `npx skills update` - Update all installed skills

**Browse:** https://skills.sh/

## Source 2: skillsmp.com API

skillsmp.com provides a dedicated search API with two modes.

### API Key Configuration

优先读取环境变量 `SKILLSMP_API_KEY`：

```bash
echo $SKILLSMP_API_KEY   # 非空则可直接使用
```

**配置方式（持久化）：** 在 `~/.claude/settings.json` 的 `env` 字段中添加：
```json
"SKILLSMP_API_KEY": "sk_live_skillsmp_xxx"
```

若未配置，按 Step 2 的决策流程处理（提示用户选择临时提供或永久配置）。

### Keyword Search

```bash
curl -s "https://skillsmp.com/api/v1/skills/search?q=QUERY&limit=10&sortBy=stars" \
  -H "Authorization: Bearer $SKILLSMP_API_KEY" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if data.get('success'):
    skills = data['data']['skills']
    print(f'Found {len(skills)} skills:')
    for s in skills:
        print(json.dumps(s, ensure_ascii=False, indent=2))
else:
    print('Error:', data.get('error', {}).get('message'))
"
```

### AI 语义搜索（自然语言查询）

```bash
curl -s "https://skillsmp.com/api/v1/skills/ai-search?q=QUERY" \
  -H "Authorization: Bearer $SKILLSMP_API_KEY" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if data.get('success'):
    skills = data['data']['skills']
    print(f'Found {len(skills)} skills:')
    for s in skills:
        print(json.dumps(s, ensure_ascii=False, indent=2))
else:
    print('Error:', data.get('error', {}).get('message'))
"
```

**解析输出说明：** 命令输出原始 JSON 对象，Claude 根据实际字段动态提取名称、描述、安装命令等信息展示给用户。常见字段包括 `name`、`description`、`installCommand`、`packageId`、`stars`、`author` 等，以实际响应为准。

**选择哪种搜索：**

| 情况 | 使用 |
|------|------|
| 关键词明确（react, testing） | `/skills/search` |
| 自然语言描述需求（"帮我写小说"） | `/skills/ai-search` |

**速率限制：** 每个 API Key 每日 500 次（UTC 午夜重置）

## How to Help Users Find Skills

### Step 1: Understand What They Need

Identify: domain, specific task, whether a skill likely exists.

### Step 2: Search Both Sources in Parallel

**skills.sh CLI（始终执行）：**
```bash
npx skills find [keyword]
```

**skillsmp.com（按以下决策流程执行）：**

```
用户是否明确说"不需要查 skillsmp" 或 "只查 skills.sh"？
  → 是：跳过 skillsmp，仅展示 skills.sh 结果
  → 否：继续

检查 SKILLSMP_API_KEY 是否已配置：
  → 已配置：直接调用 API 搜索
  → 未配置：告知用户并询问意向（见下方提示模板）
```

**API Key 未配置时的提示模板：**

```
skillsmp.com 搜索需要 API Key，当前未检测到 SKILLSMP_API_KEY。

你可以选择：
1. 临时提供：直接告诉我你的 API Key，本次搜索使用
2. 永久配置：在 ~/.claude/settings.json 的 env 中添加：
   "SKILLSMP_API_KEY": "sk_live_skillsmp_xxx"
   或在终端执行：export SKILLSMP_API_KEY=sk_live_skillsmp_xxx
3. 跳过：只使用 skills.sh 搜索结果

你希望怎么做？
```

用户提供临时 Key 后，将其赋值给变量使用（不持久化）：
```bash
SKILLSMP_API_KEY="用户提供的key" curl -s "https://skillsmp.com/api/v1/skills/search?q=QUERY..." ...
```

- 关键词查询 → `/api/v1/skills/search?q=keyword&sortBy=stars`
- 自然语言查询 → `/api/v1/skills/ai-search?q=description`

### Step 3: Present Merged Results

展示时注明来源：

```
来自 skills.sh:
  vercel-labs/agent-skills@vercel-react-best-practices (198.5K installs)
  安装: npx skills add vercel-labs/agent-skills@vercel-react-best-practices
  详情: https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices

来自 skillsmp.com:
  react-performance-toolkit — React 性能优化工具集
  安装: npx skills add xxx/react-performance-toolkit
```

### Step 4: Offer to Install

```bash
npx skills add <owner/repo@skill> -g -y
```

The `-g` flag installs globally (user-level) and `-y` skips confirmation prompts.

## Common Skill Categories

| Category        | Example Queries                          |
| --------------- | ---------------------------------------- |
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing         | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| Documentation   | docs, readme, changelog, api-docs        |
| Code Quality    | review, lint, refactor, best-practices   |
| Design          | ui, ux, design-system, accessibility     |
| Productivity    | workflow, automation, git                |

## Tips for Effective Searches

1. **Use specific keywords**: "react testing" is better than just "testing"
2. **Try alternative terms**: If "deploy" doesn't work, try "deployment" or "ci-cd"
3. **Check popular sources**: Many skills come from `vercel-labs/agent-skills` or `ComposioHQ/awesome-claude-skills`
4. **Use AI search for natural language**: skillsmp `/ai-search` handles vague queries better than keyword matching
5. **Browse manually**: https://skillsmp.com/ for category browsing when API quota is exhausted

## When No Skills Are Found

1. Acknowledge that no existing skill was found from either source
2. Offer to help with the task directly using your general capabilities
3. Suggest the user could create their own skill with `npx skills init`

```
I searched both skills.sh and skillsmp.com for "xyz" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, you could create your own skill:
npx skills init my-xyz-skill
```
