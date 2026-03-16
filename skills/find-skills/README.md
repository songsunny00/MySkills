# find-skills

**中文** | [English](README.en.md)

> 基于 [vercel-labs/skills](https://github.com/vercel-labs/skills) 的 `find-skills` 改造版本

## 原版来源

- **原始项目：** https://github.com/vercel-labs/skills
- **安装命令：** `npx skills add vercel-labs/skills@find-skills`
- **原始技能页：** https://skills.sh/vercel-labs/skills/find-skills

---

## 原版功能

| 功能 | 说明 |
|------|------|
| 触发场景识别 | 识别用户"如何做 X"、"有没有 skill 做 X"等场景，自动启用 skill 查找流程 |
| CLI 搜索 | 通过 `npx skills find [query]` 在 skills.sh 注册表中关键词搜索 |
| 结果展示 | 输出 skill 名称、安装命令（`npx skills add`）、详情链接 |
| 一键安装 | 提供 `npx skills add <package> -g -y` 命令帮助用户安装 |
| 未找到处理 | 搜索无结果时，提供直接帮助或引导用户用 `npx skills init` 创建自定义 skill |
| 分类参考表 | 内置常见分类（Web 开发、测试、DevOps、文档、设计等）辅助搜索关键词选择 |

---

## 改造新增功能

### 1. 新增 skillsmp.com 作为第二搜索来源

原版仅支持 skills.sh CLI 搜索。改造后同时支持 [skillsmp.com](https://skillsmp.com/) 的专属 REST API，实现双源并行搜索、结果合并展示。

**两个 API 端点：**

| 端点 | 适用场景 |
|------|----------|
| `GET /api/v1/skills/search?q=keyword&sortBy=stars` | 关键词明确时（react、testing 等） |
| `GET /api/v1/skills/ai-search?q=description` | 自然语言描述需求时（"帮我写小说"） |

**认证方式：** `Authorization: Bearer $SKILLSMP_API_KEY`

---

### 2. API Key 智能引导机制

当 `SKILLSMP_API_KEY` 未配置时，不再静默跳过，而是主动提示用户三选一：

```
1. 临时提供  — 本次搜索使用，不持久化
2. 永久配置  — 写入 ~/.claude/settings.json 的 env 字段
3. 跳过      — 只使用 skills.sh 结果
```

**永久配置示例（`~/.claude/settings.json`）：**
```json
{
  "env": {
    "SKILLSMP_API_KEY": "sk_live_skillsmp_xxx"
  }
}
```

---

### 3. 用户可跳过 skillsmp 搜索

若用户明确表示"不需要查 skillsmp"或"只查 skills.sh"，则跳过 API 调用，避免不必要的请求消耗（每日限额 500 次）。

---

### 4. 合并结果展示（注明来源）

搜索结果同时展示两个来源，并标注出处：

```
来自 skills.sh:
  vercel-labs/agent-skills@vercel-react-best-practices (198.5K installs)
  安装: npx skills add vercel-labs/agent-skills@vercel-react-best-practices
  详情: https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices

来自 skillsmp.com:
  react-performance-toolkit — React 性能优化工具集
  安装: npx skills add xxx/react-performance-toolkit
```

---

## 改造对比总览

| 特性 | 原版 | 改造版 |
|------|------|--------|
| 搜索来源 | skills.sh（CLI） | skills.sh + skillsmp.com（API） |
| 搜索方式 | 关键词 | 关键词 + AI 语义搜索 |
| API Key 处理 | 无 | 未配置时引导用户三选一 |
| 用户控制 | 无法跳过来源 | 可明确跳过 skillsmp |
| 结果展示 | 单源 | 双源合并，注明来源 |
| 速率限制提示 | 无 | 提示 skillsmp 每日 500 次上限 |
