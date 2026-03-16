# CoderSkills

**中文** | [English](README.en.md)

面向开发者的 AI 编程辅助 skill 合集，覆盖开发全流程：需求设计 → 编码实现 → 测试调试 → 代码审查 → 发布收尾。

## 包含的 Skill

### 开发流程

| Skill | 说明 | 来源 |
|-------|------|------|
| `brainstorming` | 任何创造性工作前必用——探索需求、设计方案，再动手实现 | obra/superpowers |
| `writing-plans` | 有多步骤需求时，先写实现计划，再触碰代码 | obra/superpowers |
| `executing-plans` | 执行已写好的实现计划，带审查检查点 | obra/superpowers |
| `subagent-driven-development` | 当前会话中用子 agent 并行执行独立任务 | obra/superpowers |
| `dispatching-parallel-agents` | 有 2+ 个独立任务时，分发给多个 agent 并行处理 | obra/superpowers |
| `finishing-a-development-branch` | 实现完成后，引导分支收尾（merge / PR / cleanup） | obra/superpowers |

### 质量保障

| Skill | 说明 | 来源 |
|-------|------|------|
| `test-driven-development` | 实现任何功能前先写测试，观察失败后再写代码 | obra/superpowers |
| `systematic-debugging` | 遇到 bug 或测试失败时，先找根因再修复 | obra/superpowers |
| `verification-before-completion` | 声明完成前必须运行验证命令，证据先于断言 | obra/superpowers |
| `requesting-code-review` | 完成任务或合并前，主动请求代码审查 | obra/superpowers |
| `receiving-code-review` | 收到审查反馈时，验证后再实施，避免盲目执行 | obra/superpowers |

### 需求文档

| Skill | 说明 | 来源 |
|-------|------|------|
| `review-prd` | 以开发视角审查产品需求文档，输出结构化问题报告 | songsunny00/MySkills |
| `standardize-wiki-docs` | 将 Wiki 导出的需求文档转换为标准化模板 | songsunny00/MySkills |

### 工具与基础

| Skill | 说明 | 来源 |
|-------|------|------|
| `using-superpowers` | 对话开始时建立 skill 使用规范 | obra/superpowers |
| `using-git-worktrees` | 需要隔离工作空间时，创建 git worktree | obra/superpowers |
| `writing-skills` | 创建或编辑 skill 时使用 | obra/superpowers |

## 来源

| 来源 | Skill 数量 |
|------|-----------|
| [obra/superpowers](https://github.com/obra/superpowers) | 14 |
| [songsunny00/MySkills](https://github.com/songsunny00/MySkills) | 2 |

## 安装

**全量安装：**

```bash
# 来自 obra/superpowers
npx skills add obra/superpowers -g -y

# 来自 songsunny00/MySkills
npx skills add songsunny00/MySkills --skill review-prd standardize-wiki-docs -g -y
```

**从当前项目恢复（基于 skills-lock.json）：**

```bash
npx skills experimental_install
```
