# UiSkills

[zh-CN](README.md) | **English**

A UI/UX design skill collection covering frontend interface design, brand identity, design systems, and algorithmic art — for users who want AI assistance with visual creation and interface development.

## Included Skills

### From anthropics/skills

| Skill | Description |
|-------|-------------|
| `frontend-design` | Generate high-quality HTML/CSS/JS interfaces and frontend layouts |
| `canvas-design` | Canvas-based graphics and visual composition |
| `algorithmic-art` | Programmatic generative art and algorithm-driven visual creation |

### From nextlevelbuilder/ui-ux-pro-max-skill

| Skill | Description |
|-------|-------------|
| `ui-ux-pro-max` | Core UI/UX professional skill providing a complete design workflow |
| `ckm:design` | UI design core process — from requirements to visual mockups |
| `ckm:design-system` | Build design systems with unified component specs and style guides |
| `ckm:brand` | Brand identity design — logo, color palette, and typography |
| `ckm:ui-styling` | UI style refinement — interaction states and visual polish |
| `ckm:banner-design` | Banner ads and promotional material design |
| `ckm:slides` | Presentation and slide deck visual design |

## Sources

| Source | Skills |
|--------|--------|
| [anthropics/skills](https://github.com/anthropics/skills) | 3 |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 7 |

## Installation

Run inside the UiSkills directory to restore all skills at once:

```bash
cd UiSkills && npx skills experimental_install
```

Or install manually by source:

```bash
# From anthropics/skills
npx skills add anthropics/skills --skill frontend-design canvas-design algorithmic-art -g -y

# From nextlevelbuilder/ui-ux-pro-max-skill (all)
npx skills add nextlevelbuilder/ui-ux-pro-max-skill -g -y
```

## Updating

```bash
npx skills update
```

To force-fetch the latest version:

```bash
npx skills add anthropics/skills --skill frontend-design canvas-design algorithmic-art -g -y
npx skills add nextlevelbuilder/ui-ux-pro-max-skill -g -y
```