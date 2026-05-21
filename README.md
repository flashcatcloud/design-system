# Flashcat Design System

FC 前端设计规范与可落地的主题片段仓库。

## 按钮（2026-05）

| 路径 | 说明 |
|------|------|
| `cat/button-design-editor.html` | 设计师调参预览页（Figma variant × hierarchy × size） |
| `cat/button-current-from-code.md` | 与线上一致的初值说明 |
| `cat/_gen_button_editor.py` | 重新生成调参页（改默认 token 时） |

## 表格分页（2026-05）

| 路径 | 说明 |
|------|------|
| `cat/design-system-table.md` | §8 分页产品/设计规范 |
| `cat/pagination-design-editor.html` | 设计师调参预览页 |
| `cat/pagination-design-snapshot.json` | Token 快照 |
| `cat/pagination-current-from-code.md` | 与线上一致的说明文档 |
| `theme/pagination-table.less` | 与 `n9e/fe` `default.less` 同步的 AntD 分页 patch |
| `rules/component-border-radius.mdc` | 圆角与分页 token 规则 |

研发合并到 `fe` 时：将 `theme/pagination-table.less` 内容并入 `src/theme/default.less`（或保持两处同步）。

浅/深色通过 `var(--fc-*)` 自动切换；**不包含**金拱门 `.theme-light-gold`。
