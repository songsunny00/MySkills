# BaseSkills

**中文** | [English](README.en.md)

推荐全局安装的Skill合集——用于发现、安装、创建、更新和汉化 skills，是使用其他任何 skill 合集的前置基础。

> **推荐全局安装。** 这些 skill 与具体项目无关，安装到全局后可在任意项目中使用。

## 包含的 Skill

| Skill                  | 说明                                                           | 来源                         |
| ---------------------- | -------------------------------------------------------------- | ---------------------------- |
| `using-superpowers`    | 对话开始时建立 skill 使用规范，要求在任何响应前调用 Skill 工具 | obra/superpowers             |
| `find-skills`          | 发现并安装 skills，支持 skills.sh CLI 和 skillsmp.com 双源搜索 | songsunny00/MySkills         |
| `update-skills`        | 一键更新全局和/或项目下的所有已安装 skills                     | songsunny00/MySkills         |
| `translate-skills`     | 批量为 skills 添加中文翻译                                     | songsunny00/MySkills         |
| `writing-skills`       | 创建或编辑 skill，遵循测试驱动的编写规范                       | obra/superpowers             |
| `skill-creator`        | 引导式创建新 skill，自动生成结构完整的 SKILL.md                | anthropics/skills            |
| `brainstorming`        | 任何创造性工作前必用，探索需求和设计后再动手                   | obra/superpowers             |
| `planning-with-files`  | 将多步骤任务拆解为带文件追踪的结构化计划                       | OthmanAdi/planning-with-files |
| `mcp-builder`          | 使用 Claude API 构建 MCP 服务器的全流程指导                    | anthropics/skills            |

## 来源

| 来源                                                                              | Skill 数量 |
| --------------------------------------------------------------------------------- | ---------- |
| [obra/superpowers](https://github.com/obra/superpowers)                           | 3          |
| [songsunny00/MySkills](https://github.com/songsunny00/MySkills)                   | 3          |
| [anthropics/skills](https://github.com/anthropics/skills)                         | 2          |
| [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) | 1          |

## 安装

**推荐：全局安装全部 skill**

```bash
# 来自 obra/superpowers
npx skills add obra/superpowers --skill using-superpowers brainstorming writing-skills -g -y

# 来自 songsunny00/MySkills
npx skills add songsunny00/MySkills --skill find-skills update-skills translate-skills -g -y

# 来自 anthropics/skills
npx skills add anthropics/skills --skill skill-creator mcp-builder -g -y

# 来自 OthmanAdi/planning-with-files
npx skills add OthmanAdi/planning-with-files -g -y
```

## 更新

**更新全局已安装的 skills：**

```bash
npx skills update
```

> **注意：** `npx skills update` 通过 hash 比对判断版本，若本地与远端一致会显示 "up to date"。如需强制拉取最新版本：
>
> ```bash
> npx skills add obra/superpowers --skill using-superpowers brainstorming writing-skills -g -y
> npx skills add songsunny00/MySkills --skill find-skills update-skills translate-skills -g -y
> npx skills add anthropics/skills --skill skill-creator mcp-builder -g -y
> npx skills add OthmanAdi/planning-with-files -g -y
> ```
