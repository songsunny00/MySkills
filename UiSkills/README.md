# UiSkills

**中文** | [English](README.en.md)

面向 UI/UX 设计的 Skill 合集，涵盖前端界面设计、品牌视觉、设计系统、算法艺术等场景，适合需要 AI 辅助进行视觉创作和界面开发的用户。

## 包含的 Skill

### 来自 anthropics/skills

| Skill | 说明 |
|-------|------|
| `frontend-design` | 前端界面设计，生成高质量的 HTML/CSS/JS 页面 |
| `canvas-design` | 基于 Canvas 的图形绘制与视觉创作 |
| `algorithmic-art` | 算法驱动的生成艺术，创作程序化视觉作品 |

### 来自 nextlevelbuilder/ui-ux-pro-max-skill

| Skill | 说明 |
|-------|------|
| `ui-ux-pro-max` | UI/UX 专业设计主技能，提供完整的设计工作流 |
| `ckm:design` | 界面设计核心流程，从需求到视觉稿 |
| `ckm:design-system` | 设计系统构建，组件规范与样式统一 |
| `ckm:brand` | 品牌视觉设计，Logo、色彩、字体规范 |
| `ckm:ui-styling` | UI 样式细化，交互状态与视觉打磨 |
| `ckm:banner-design` | Banner 广告图与宣传物料设计 |
| `ckm:slides` | 演示文稿与幻灯片视觉设计 |

## 来源

| 来源 | Skill 数量 |
|------|------------|
| [anthropics/skills](https://github.com/anthropics/skills) | 3 |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 7 |

## 安装

进入 UiSkills 目录，一键恢复全部 skill：

```bash
cd UiSkills && npx skills experimental_install
```

或手动按来源安装：

```bash
# 来自 anthropics/skills
npx skills add anthropics/skills --skill frontend-design canvas-design algorithmic-art -g -y

# 来自 nextlevelbuilder/ui-ux-pro-max-skill（全部）
npx skills add nextlevelbuilder/ui-ux-pro-max-skill -g -y
```

## 更新

```bash
npx skills update
```

如需强制拉取最新版本：

```bash
npx skills add anthropics/skills --skill frontend-design canvas-design algorithmic-art -g -y
npx skills add nextlevelbuilder/ui-ux-pro-max-skill -g -y
```