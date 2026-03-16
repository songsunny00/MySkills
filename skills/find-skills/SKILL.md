---
name: find-skills
description: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.
license: MIT
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

First check for the `SKILLSMP_API_KEY` environment variable:

```bash
echo $SKILLSMP_API_KEY   # if non-empty, it can be used directly
```

**Persistent configuration:** Add to the `env` field in `~/.claude/settings.json`:

```json
"SKILLSMP_API_KEY": "sk_live_skillsmp_xxx"
```

If not configured, follow the decision flow in Step 2 (prompt the user to provide it temporarily or configure it permanently).

### Prepare API Key (Windows-compatible, strip \r)

Before calling the API, always run the following command to get a clean key:

```bash
SKILLSMP_KEY=$(echo "$SKILLSMP_API_KEY" | tr -d '\r\n')
```

### Keyword Search

```bash
SKILLSMP_KEY=$(echo "$SKILLSMP_API_KEY" | tr -d '\r\n')
curl -s "https://skillsmp.com/api/v1/skills/search?q=QUERY&limit=10&sortBy=stars" \
  -H "Authorization: Bearer $SKILLSMP_KEY" | node -e "
let d='';
process.stdin.on('data',c=>d+=c);
process.stdin.on('end',()=>{
  const r=JSON.parse(d);
  if(r.success){
    const skills=r.data.skills||[];
    console.log('Found',skills.length,'skills:');
    skills.forEach(s=>console.log(JSON.stringify(s,null,2)));
  } else {
    console.log('Error:',JSON.stringify(r.error));
  }
});
"
```

### AI Semantic Search (Natural Language Query)

> **Note:** The `/ai-search` response structure differs from keyword search — the response contains a `data.data[]` array where each item has a `skill` sub-object.

```bash
SKILLSMP_KEY=$(echo "$SKILLSMP_API_KEY" | tr -d '\r\n')
curl -s "https://skillsmp.com/api/v1/skills/ai-search?q=QUERY" \
  -H "Authorization: Bearer $SKILLSMP_KEY" | node -e "
let d='';
process.stdin.on('data',c=>d+=c);
process.stdin.on('end',()=>{
  const r=JSON.parse(d);
  if(r.success){
    const items=r.data.data||[];
    console.log('Found',items.length,'results:');
    items.forEach(item=>console.log(JSON.stringify(item.skill,null,2)));
  } else {
    console.log('Error:',JSON.stringify(r.error));
  }
});
"
```

**Output parsing:** Commands output raw JSON objects. Claude dynamically extracts the name, description, install command, and other info from actual fields. Common fields include `name`, `description`, `installCommand`, `packageId`, `stars`, `author`, etc. — use whatever the actual response returns.

**Which search to use:**

| Situation                                          | Use                 |
| -------------------------------------------------- | ------------------- |
| Clear keywords (react, testing)                    | `/skills/search`    |
| Natural language description ("help me write a novel") | `/skills/ai-search` |

**Rate limit:** 500 requests per API key per day (resets at UTC midnight)

## How to Help Users Find Skills

### Step 1: Understand What They Need

Identify: domain, specific task, whether a skill likely exists.

### Step 2: Search Both Sources in Parallel

**skills.sh CLI (always run):**

```bash
npx skills find [keyword]
```

**skillsmp.com (follow the decision flow below):**

```
Did the user explicitly say "skip skillsmp" or "only use skills.sh"?
  → Yes: skip skillsmp, show only skills.sh results
  → No: continue

Check if SKILLSMP_API_KEY is configured:
  → Configured: call the API directly
  → Not configured: inform the user and ask for their preference (see prompt template below)
```

**Prompt template when API key is not configured:**

```
Searching skillsmp.com requires an API Key, but SKILLSMP_API_KEY was not detected.

You can choose to:
1. Provide temporarily: tell me your API Key and I'll use it for this search
2. Configure permanently: add to the env field in ~/.claude/settings.json:
   "SKILLSMP_API_KEY": "sk_live_skillsmp_xxx"
   or run in terminal: export SKILLSMP_API_KEY=sk_live_skillsmp_xxx
3. Skip: use only skills.sh search results

What would you like to do?
```

After the user provides a temporary key, assign it and strip extra whitespace (do not persist):

```bash
SKILLSMP_KEY=$(echo "user-provided-key" | tr -d '\r\n')
curl -s "https://skillsmp.com/api/v1/skills/search?q=QUERY..." \
  -H "Authorization: Bearer $SKILLSMP_KEY" | node -e "..."
```

- Keyword query → `/api/v1/skills/search?q=keyword&sortBy=stars`
- Natural language query → `/api/v1/skills/ai-search?q=description`

### Step 3: Present Merged Results

Label results by source when presenting:

```
From skills.sh:
  vercel-labs/agent-skills@vercel-react-best-practices (198.5K installs)
  Install: npx skills add vercel-labs/agent-skills@vercel-react-best-practices
  Details: https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices

From skillsmp.com:
  react-performance-toolkit — React performance optimization toolkit
  Install: npx skills add xxx/react-performance-toolkit
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

## Source And Installation

- GitHub: https://github.com/songsunny00/MySkills/tree/main/skills/find-skills
- Installation: npx skills add https://github.com/songsunny00/MySkills --skill find-skills
