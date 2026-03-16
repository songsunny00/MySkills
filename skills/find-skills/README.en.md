# find-skills

[中文](README.md) | **English**

> A customized version of `find-skills` based on [vercel-labs/skills](https://github.com/vercel-labs/skills)

## Original Source

- **Original project:** https://github.com/vercel-labs/skills
- **Install command:** `npx skills add vercel-labs/skills@find-skills`
- **Original skill page:** https://skills.sh/vercel-labs/skills/find-skills

---

## Original Features

| Feature | Description |
|---------|-------------|
| Trigger detection | Detects user queries like "how do I do X" or "is there a skill for X" and activates the skill discovery flow |
| CLI search | Searches the skills.sh registry by keyword via `npx skills find [query]` |
| Result display | Outputs skill name, install command (`npx skills add`), and detail link |
| One-click install | Provides `npx skills add <package> -g -y` to help users install skills |
| Not found handling | When no results are found, offers direct assistance or guides users to create custom skills with `npx skills init` |
| Category reference | Built-in category table (Web Dev, Testing, DevOps, Docs, Design, etc.) to assist keyword selection |

---

## New Features in This Fork

### 1. skillsmp.com as a Second Search Source

The original only supports skills.sh CLI search. This fork also integrates the [skillsmp.com](https://skillsmp.com/) REST API, enabling parallel dual-source search with merged result display.

**Two API endpoints:**

| Endpoint | Use case |
|----------|----------|
| `GET /api/v1/skills/search?q=keyword&sortBy=stars` | When keywords are clear (react, testing, etc.) |
| `GET /api/v1/skills/ai-search?q=description` | When describing needs in natural language |

**Authentication:** `Authorization: Bearer $SKILLSMP_API_KEY`

---

### 2. Smart API Key Guidance

When `SKILLSMP_API_KEY` is not configured, instead of silently skipping, the skill prompts the user with three options:

```
1. Provide temporarily  — used for this search only, not persisted
2. Configure permanently — write to the env field in ~/.claude/settings.json
3. Skip                 — use only skills.sh results
```

**Permanent configuration example (`~/.claude/settings.json`):**
```json
{
  "env": {
    "SKILLSMP_API_KEY": "sk_live_skillsmp_xxx"
  }
}
```

---

### 3. User Can Skip skillsmp Search

If the user explicitly says "skip skillsmp" or "only use skills.sh", the API call is bypassed to avoid unnecessary quota usage (500 requests/day limit).

---

### 4. Merged Results with Source Labels

Search results from both sources are displayed together with clear attribution:

```
From skills.sh:
  vercel-labs/agent-skills@vercel-react-best-practices (198.5K installs)
  Install: npx skills add vercel-labs/agent-skills@vercel-react-best-practices
  Details: https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices

From skillsmp.com:
  react-performance-toolkit — React performance optimization toolkit
  Install: npx skills add xxx/react-performance-toolkit
```

---

## Comparison: Original vs Fork

| Feature | Original | This Fork |
|---------|----------|-----------|
| Search sources | skills.sh (CLI) | skills.sh + skillsmp.com (API) |
| Search modes | Keyword only | Keyword + AI semantic search |
| API Key handling | None | Guides user with 3 options when not configured |
| User control | Cannot skip sources | Can explicitly skip skillsmp |
| Result display | Single source | Dual source, merged with labels |
| Rate limit notice | None | Shows skillsmp 500/day limit |
