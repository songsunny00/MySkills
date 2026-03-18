# skill-vetter

**中文** | [English](README.en.md)

> 来源：[openclaw/skills](https://github.com/openclaw/skills/tree/main/skills/spclaudehome/skill-vetter)

安装 skill 前的安全审查协议。在安装任何来源不明的 skill 之前，先用它做一次全面的安全鉴定。

## 使用场景

- 安装来自 GitHub 仓库的 skill 之前
- 评估其他人分享的 skill 之前
- 任何被要求安装未知代码时

## 审查流程

skill-vetter 按四步执行审查：

| 步骤 | 内容 |
|------|------|
| **Step 1** 来源核查 | 作者是否可信？下载量/Star 数？最近更新时间？ |
| **Step 2** 代码审查 | 读取所有文件，检查危险行为（必须执行） |
| **Step 3** 权限范围 | 需要读写哪些文件？是否有网络调用？范围是否最小化？ |
| **Step 4** 风险定级 | 综合评估，输出风险等级和安装建议 |

### 危险行为红线（立即拒绝）

- 向未知 URL 发起 `curl`/`wget` 请求
- 读取 `~/.ssh`、`~/.aws` 等敏感目录
- 访问 `MEMORY.md`、`IDENTITY.md` 等身份文件
- 使用 `base64` 解码、`eval()`、`exec()` 处理外部输入
- 修改工作区外的系统文件
- 代码存在混淆（压缩、编码、最小化）

## 风险等级

| 等级 | 示例 | 处理方式 |
|------|------|----------|
| 🟢 低 | 笔记、格式化工具 | 基础审查，可安装 |
| 🟡 中 | 文件操作、API 调用 | 完整代码审查 |
| 🔴 高 | 凭证、系统操作 | 需人工确认 |
| ⛔ 极高 | root 权限、安全配置 | 禁止安装 |

## 输出报告

审查完成后自动生成结构化报告：

```
SKILL VETTING REPORT
═══════════════════════════════════════
Skill: [名称]
Source: [来源]
Author: [作者]
───────────────────────────────────────
RED FLAGS: [无 / 列出问题]
PERMISSIONS: Files / Network / Commands
RISK LEVEL: 🟢 LOW / 🟡 MEDIUM / 🔴 HIGH / ⛔ EXTREME
VERDICT: ✅ 可安装 / ⚠️ 谨慎安装 / ❌ 禁止安装
═══════════════════════════════════════
```

## 安装

```bash
npx skills add songsunny00/MySkills --skill skill-vetter -g -y
```

> 偏执是一种特性。🔒
