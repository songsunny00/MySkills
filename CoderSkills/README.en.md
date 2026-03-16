# CoderSkills

[zh-CN](README.md) | **English**

A curated collection of AI coding assistant skills for developers, covering the full development lifecycle: requirements & design → implementation → testing & debugging → code review → release.

## Included Skills

### Development Workflow

| Skill | Description | Source |
|-------|-------------|--------|
| `brainstorming` | Required before any creative work — explore requirements and design before writing code | obra/superpowers |
| `writing-plans` | Write an implementation plan before touching code when requirements have multiple steps | obra/superpowers |
| `executing-plans` | Execute a written implementation plan with review checkpoints | obra/superpowers |
| `subagent-driven-development` | Execute independent tasks in parallel using subagents in the current session | obra/superpowers |
| `dispatching-parallel-agents` | Dispatch 2+ independent tasks to multiple agents for parallel processing | obra/superpowers |
| `finishing-a-development-branch` | Guide branch completion after implementation (merge / PR / cleanup) | obra/superpowers |

### Quality Assurance

| Skill | Description | Source |
|-------|-------------|--------|
| `test-driven-development` | Write tests before implementation, watch them fail, then write minimal code to pass | obra/superpowers |
| `systematic-debugging` | Find the root cause before proposing fixes when encountering bugs or failures | obra/superpowers |
| `verification-before-completion` | Run verification commands before claiming work is complete — evidence before assertions | obra/superpowers |
| `requesting-code-review` | Request code review before completing tasks or merging | obra/superpowers |
| `receiving-code-review` | Verify before implementing review feedback — no blind execution | obra/superpowers |

### Requirements & Documentation

| Skill | Description | Source |
|-------|-------------|--------|
| `review-prd` | Review product requirement documents from a developer perspective, output structured issue reports | songsunny00/MySkills |
| `standardize-wiki-docs` | Convert Wiki-exported requirement documents into standardized templates | songsunny00/MySkills |

### Tooling & Foundations

| Skill | Description | Source |
|-------|-------------|--------|
| `using-superpowers` | Establish skill usage conventions at the start of any conversation | obra/superpowers |
| `using-git-worktrees` | Create isolated git worktrees when workspace isolation is needed | obra/superpowers |
| `writing-skills` | Use when creating or editing skills | obra/superpowers |

## Sources

| Source | Skills |
|--------|--------|
| [obra/superpowers](https://github.com/obra/superpowers) | 14 |
| [songsunny00/MySkills](https://github.com/songsunny00/MySkills) | 2 |

## Installation

**Install all:**

```bash
# From obra/superpowers
npx skills add obra/superpowers -g -y

# From songsunny00/MySkills
npx skills add songsunny00/MySkills --skill review-prd standardize-wiki-docs -g -y
```

**Restore from this project (via skills-lock.json):**

```bash
npx skills experimental_install
```

## Updating

**Update global skills:**

```bash
npx skills update
```

**Update project skills (via skills-lock.json):**

```bash
npx skills experimental_install
```

**Update both global and project in one step:**

```bash
npx skills update && npx skills experimental_install
```

> **Note:** `npx skills update` uses hash comparison to detect changes. If the installed version matches the remote content, it reports "up to date" even after a new push. To force-fetch the latest version, run manually:
>
> ```bash
> # Force update global
> npx skills add obra/superpowers -g -y
> npx skills add songsunny00/MySkills --skill review-prd standardize-wiki-docs -g -y
> ```
