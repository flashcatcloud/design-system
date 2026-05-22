# Flashcat Design System

FC 前端设计规范与可落地的主题片段仓库。

## 表格分页（2026-05）

| 路径 | 说明 |
|------|------|
| `cat/design-system-table.md` | §8 分页产品/设计规范 |
| `cat/pagination-design-editor.html` | 设计师调参预览页 |
| `cat/pagination-design-snapshot.json` | Token 快照 |
| `cat/pagination-current-from-code.md` | 与线上一致的说明文档 |
| `theme/pagination-table.less` | 与 `n9e/fe` `default.less` 同步的 AntD 分页 patch |
| `rules/component-border-radius.mdc` | 圆角与分页 token 规则 |
| `patches/n9e-fe-table-design-system/*.patch` | 表格设计系统落地到 `n9e-fe` 的候选工程 patch，供开发同事评审后应用 |

研发合并到 `fe` 时：将 `theme/pagination-table.less` 内容并入 `src/theme/default.less`（或保持两处同步）。

浅/深色通过 `var(--fc-*)` 自动切换；**不包含**金拱门 `.theme-light-gold`。

## n9e-fe 表格设计系统候选 patch

当前候选 patch 不直接提交到真实产品仓库。开发同事需要时，在 `n9e-fe` 仓库中按顺序应用：

```bash
git am ../design-system/patches/n9e-fe-table-design-system/*.patch
```

应用后建议至少执行：

```bash
npm exec tsc -- --noEmit --pretty false
npm exec lessc -- src/theme/table-design-system.less /tmp/n9e-table-design-system.css
git diff --check
```
