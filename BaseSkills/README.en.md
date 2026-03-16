# BaseSkills

[zh-CN](README.md) | **English**

A foundational skill management collection — for discovering, installing, creating, updating, and translating skills. A prerequisite for using any other skill collection.

> **Recommended for global installation.** These skills are project-agnostic and can be used across any project once installed globally.

## Included Skills

| Skill | Description | Source |
|-------|-------------|--------|
| `using-superpowers` | Establish skill usage conventions at the start of any conversation, requiring Skill tool invocation before any response | obra/superpowers |
| `find-skills` | Discover and install skills via dual-source search: skills.sh CLI and skillsmp.com API | songsunny00/MySkills |
| `update-skills` | Update all installed skills globally and/or in the current project in one step | songsunny00/MySkills |
| `translate-skills` | Batch-add Chinese translations to skills | songsunny00/MySkills |
| `writing-skills` | Create or edit skills following a test-driven authoring process | obra/superpowers |
| `brainstorming` | Required before any creative work — explore requirements and design before implementation | obra/superpowers |

## Sources

| Source | Skills |
|--------|--------|
| [obra/superpowers](https://github.com/obra/superpowers) | 3 |
| [songsunny00/MySkills](https://github.com/songsunny00/MySkills) | 3 |

## Installation

**Recommended: install all skills globally**

```bash
# From obra/superpowers
npx skills add obra/superpowers --skill using-superpowers brainstorming writing-skills -g -y

# From songsunny00/MySkills
npx skills add songsunny00/MySkills --skill find-skills update-skills translate-skills -g -y
```

## Updating

**Update globally installed skills:**

```bash
npx skills update
```

> **Note:** `npx skills update` uses hash comparison to detect changes. If the installed version matches the remote, it reports "up to date" even after a new push. To force-fetch the latest version:
>
> ```bash
> npx skills add obra/superpowers --skill using-superpowers brainstorming writing-skills -g -y
> npx skills add songsunny00/MySkills --skill find-skills update-skills translate-skills -g -y
> ```
