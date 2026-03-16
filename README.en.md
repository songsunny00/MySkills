# MySkills

[zh-CN](README.md) | **English**

A personal AI Agent Skill repository containing custom-built skills and curated skill collections for popular AI coding tools including Claude Code, Cursor, and Trae.

## Custom Skills

Located in the `skills/` directory. Each skill can be installed independently.

| Skill | Description |
|-------|-------------|
| [`find-skills`](skills/find-skills/) | Discover and install agent skills via dual-source search: skills.sh CLI and skillsmp.com API |
| [`update-skills`](skills/update-skills/) | Update all installed skills globally and/or in the current project in one step |
| [`translate-skills`](skills/translate-skills/) | Batch-add Chinese translations to skills |
| [`review-prd`](skills/review-prd/) | Review product requirement documents from a developer perspective, output structured issue reports |
| [`standardize-wiki-docs`](skills/standardize-wiki-docs/) | Convert Wiki-exported requirement documents into standardized templates |

**Install a single skill:**

```bash
npx skills add songsunny00/MySkills --skill <skill-name> -g -y
```

**Install all custom skills:**

```bash
npx skills add songsunny00/MySkills -g -y
```

## Skill Collections

Pre-configured skill bundles organized by use case. Each collection directory contains a `skills-lock.json` for one-command installation.

| Collection | Description | For |
|------------|-------------|-----|
| [BaseSkills](BaseSkills/) | Foundational skill management tools, recommended for global installation | Everyone |
| [CoderSkills](CoderSkills/) | Developer-focused coding assistant skills covering the full development lifecycle | Developers |
| [WriterSkills](WriterSkills/) | Writing assistant skills (coming soon) | Writers |

**Install a collection (run inside the collection directory):**

```bash
cd BaseSkills && npx skills experimental_install
```

## Directory Structure

```
MySkills/
├── skills/                  # Custom skills
│   ├── find-skills/
│   ├── update-skills/
│   ├── translate-skills/
│   ├── review-prd/
│   └── standardize-wiki-docs/
├── BaseSkills/              # Foundational collection (recommended global install)
├── CoderSkills/             # Developer collection
├── WriterSkills/            # Writer collection (coming soon)
└── skills-lock.json
```

## Links

- **GitHub:** https://github.com/songsunny00/MySkills
- **Skills CLI:** https://skills.sh
- **Skill Marketplace:** https://skillsmp.com
