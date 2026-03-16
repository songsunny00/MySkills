# update-skills

[zh-CN](README.md) | **English**

Update globally installed skills and current project skills in one step.

## Background

`npx skills update` only updates globally installed skills. Project-level skills require a separate command. This skill combines both into a single step and lets you control the update scope through natural language.

## Features

| User says | Action |
|-----------|--------|
| "update skills" (default) | Global + Project |
| "global only" | `npx skills update` only |
| "project only" | `npx skills experimental_install` only |

## Execution Logic

**Global update:**
```bash
npx skills update
```

**Project update:**
1. Check if `skills-lock.json` exists in the current directory
2. If found, run `npx skills experimental_install`
3. If not found, skip and notify the user

**Result report format:**
```
✅ Global skills updated
✅ Project skills updated (via skills-lock.json)
❌ Project update failed: <error message>
```

Any step that fails does not interrupt the flow — all steps run and results are reported together at the end.

## Notes

- `npx skills update` uses hash comparison to detect changes. If the installed content matches the remote, it reports "up to date" even after a new push. To force-reinstall, run manually:
  ```bash
  npx skills add <source> --skill <name> -y
  ```
- `experimental_install` is an experimental command; the name may change in future CLI versions.

## Installation

```bash
npx skills add https://github.com/songsunny00/MySkills --skill update-skills -g -y
```
