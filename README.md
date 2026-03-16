# MySkills

**中文** | [English](README.en.md)

个人 AI Agent Skill 仓库，包含自研的 skills 以及按场景整理的 skill 合集，适配 Claude Code、Cursor、Trae 等主流 AI 编程工具。

## 自研 Skills

存放于 `skills/` 目录，可单独安装使用。

| Skill | 说明 |
|-------|------|
| [`find-skills`](skills/find-skills/) | 发现并安装 agent skills，支持 skills.sh CLI 和 skillsmp.com 双源搜索 |
| [`update-skills`](skills/update-skills/) | 一键更新全局和/或项目下的所有已安装 skills |
| [`translate-skills`](skills/translate-skills/) | 批量为 skills 添加中文翻译 |
| [`review-prd`](skills/review-prd/) | 以开发视角审查产品需求文档，输出结构化问题报告 |
| [`standardize-wiki-docs`](skills/standardize-wiki-docs/) | 将 Wiki 导出的需求文档转换为标准化模板 |

**安装单个 skill：**

```bash
npx skills add songsunny00/MySkills --skill <skill-name> -g -y
```

**安装全部自研 skill：**

```bash
npx skills add songsunny00/MySkills -g -y
```

## Skill 合集

按使用场景预配置的 skill 组合，每个合集目录下有独立的 `skills-lock.json`，可一键恢复安装。

| 合集 | 说明 | 适用场景 |
|------|------|----------|
| [BaseSkills](BaseSkills/) | 推荐全局安装的基础合集，skill 生态管理工具 | 所有用户 |
| [CoderSkills](CoderSkills/) | 面向开发者的编程辅助合集，覆盖开发全流程 | 开发者 |
| [WriterSkills](WriterSkills/) | 面向写作者的创作辅助合集（规划中） | 写作者 |

**安装指定合集（进入对应目录后执行）：**

```bash
cd BaseSkills && npx skills experimental_install
```

## 目录结构

```
MySkills/
├── skills/                  # 自研 skills
│   ├── find-skills/
│   ├── update-skills/
│   ├── translate-skills/
│   ├── review-prd/
│   └── standardize-wiki-docs/
├── BaseSkills/              # 基础合集（推荐全局安装）
├── CoderSkills/             # 开发者合集
├── WriterSkills/            # 写作者合集（规划中）
└── skills-lock.json
```

## 相关链接

- **GitHub：** https://github.com/songsunny00/MySkills
- **Skills CLI：** https://skills.sh
- **Skill 市场：** https://skillsmp.com
