# Flashcat Design System

FC 前端设计规范与可落地的主题片段仓库。

## 按钮（2026-05）

| 路径 | 说明 |
|------|------|
| `cat/button-design-editor.html` | 设计师调参预览页（§5.1 尺寸对齐 Meow；§5.2 状态色 token） |

**使用方式**

1. 用浏览器直接打开 `cat/button-design-editor.html`（或本地静态服务）。
2. §1–§4 选 variant / hierarchy / 尺寸 / 图标，§5.2 调 `--btn-*`；色值请保持 `var(--fc-*)`，勿改成 `rgb(...)` 硬编码。
3. 「预览」看效果；定稿后点「生效」会写入页面内 `:root` / `COLOR_DEFAULTS` 并下载 HTML，**以仓库本文件为准**时无需再覆盖下载件。
4. 浅/深在页内切换；金拱门为 `data-theme="gold"` 覆盖。与产品主题类名 `body.theme-dark` 不同，落地时 token 仍走 `--fc-*`。

**研发落地（Meow UI）**

- 设计矩阵：`variant`（solid / soft / surface / outline / ghost / text / link）× `hierarchy`（primary … quaternary / destructive）。
- Meow `Button` 仍为 `variant` + `size` + `data-icon`（见内网 Meow 文档）；上表矩阵通过 `--btn-*` → `var(--fc-*)` 映射，勿在业务里直接复制 `.fc-btn` 类名。
- 参考映射：`solid·primary` → `variant="primary"`；`destructive` → `variant="danger"`；`outline` / `ghost` / `link` 同名；`soft` / `surface` / `text` 需扩展或映射到 `default` / `ghost`。
- 尺寸档与 Meow `h-6/7/8/9` 已对齐，§5.1 勿随意改。

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
