---
name: update-skills
description: Use when the user wants to update installed skills — globally, for the current project, or both. Triggers on phrases like "update skills", "更新 skills", "更新全局", "更新项目", or similar intent.
license: MIT
---

# Update Skills

Update globally installed skills and/or project-level skills in one step.

## When to Use

| User says | Mode |
|-----------|------|
| "更新 skills" / "update skills" (no qualifier) | Global + Project (default) |
| "更新全局" / "global only" / "只更新全局" | Global only |
| "更新项目" / "project only" / "只更新项目" | Project only |

## Execution

### Global Update

```bash
npx skills update
```

### Project Update

First check if `skills-lock.json` exists in the current directory:

```bash
# Check
ls skills-lock.json 2>/dev/null && echo "found" || echo "not found"

# If found, run:
npx skills experimental_install
```

If `skills-lock.json` is not found, skip and inform the user:
> "No skills-lock.json found in current directory — skipping project update."

### Error Handling

Run all applicable steps regardless of individual failures. Report results at the end:

```
✅ Global skills updated
   (or: All global skills are up to date)

✅ Project skills updated (via skills-lock.json)

❌ Project update failed: <error message>
   Suggestion: run `npx skills experimental_install` manually
```

## Notes

- `npx skills update` compares a hash of installed files against the remote source. If they match, it reports "up to date" even after a remote push — use `npx skills add <source> --skill <name> -y` to force-reinstall.
- `experimental_install` is an experimental command; the name may change in future CLI versions.

## Source and Installation

- GitHub: https://github.com/songsunny00/MySkills/tree/main/skills/update-skills
- Installation: npx skills add https://github.com/songsunny00/MySkills --skill update-skills -g -y
