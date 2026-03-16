# update-skills

**中文** | [English](README.en.md)

一键同步更新全局和当前项目下的所有已安装 skill。

## 背景

`npx skills update` 只更新全局安装的 skills，项目级 skills 需要单独处理。这个 skill 将两者合并为一步，并支持通过自然语言控制更新范围。

## 功能

| 用户说 | 执行操作 |
|--------|----------|
| "更新 skills"（默认） | 全局 + 项目 |
| "只更新全局" | 仅 `npx skills update` |
| "只更新项目" | 仅 `npx skills experimental_install` |

## 执行逻辑

**全局更新：**
```bash
npx skills update
```

**项目更新：**
1. 检查当前目录是否存在 `skills-lock.json`
2. 存在则执行 `npx skills experimental_install`
3. 不存在则跳过并提示

**结果汇报格式：**
```
✅ 全局 skills 更新完成
✅ 项目 skills 更新完成（基于 skills-lock.json）
❌ 项目更新失败：<错误信息>
```

任意步骤失败不中断流程，最终统一汇报。

## 注意事项

- `npx skills update` 通过 hash 比对判断是否需要更新，若本地与远端内容一致会显示 "up to date"，即使远端有新推送也如此。如需强制更新，请手动执行：
  ```bash
  npx skills add <来源> --skill <名称> -y
  ```
- `experimental_install` 为实验性命令，未来 CLI 版本中名称可能变更。

## 安装

```bash
npx skills add https://github.com/songsunny00/MySkills --skill update-skills -g -y
```
