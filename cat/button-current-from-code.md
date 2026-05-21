# FC 按钮 · 当前工程初值说明

> 交互调参：**`button-design-editor.html`**（支持浅色 / 深色 / 金拱门；可按 variant 组合收窄参数表）

## 分类（Figma 设计规范优先）

| 维度 | 取值 | 约束 |
|------|------|------|
| **variant** | soft · solid · surface · outline · ghost · text | 见 Figma「设计规范 - 按钮」 |
| **hierarchy** | primary · secondary · tertiary · quaternary | tertiary/quaternary 仅 ghost、text；**solid 仅 primary** |
| **size** | xs · sm · default · lg | 表格操作列已落地 **xs = 24px** |
| **icon** | none · inline-start · inline-end | 与 Figma 一致 |
| **destructive** | true / false | solid 仅 primary；ghost/text 仅 primary/secondary |
| **Link** | hierarchy + underline（hover / always） | 独立于 variant |

## Meow UI 对照（前端组件文档）

| Meow UI `variant` | 设计稿近似 |
|-------------------|------------|
| `default` | surface / soft secondary |
| `primary` | solid primary |
| `danger` | destructive（各 variant 的 danger 色） |
| `outline` | outline |
| `ghost` | ghost |
| `link` | Link 组 |

文档来源：`Button.webarchive`（`@flashcatcloud/meow-ui` 文档站）。

## 已从代码拉取的初值

### 尺寸（`table-design-system.less` · ghost 24px 等级）

| 变量 | 初值 | 来源 |
|------|------|------|
| `--btn-height-xs` | 24px | `.ant-btn-link` / `fc-ghost-*-xs` |
| `--btn-padding-x-xs` | 8px | ghost-primary `padding: 0 8px` |
| `--btn-radius-xs` | 6px | 与分页、表格一致（&lt;28px → 6） |
| `--btn-icon-size-xs` | 14px | lucide 表格头/操作列 |
| `--btn-height-default` | 32px | Ant Design 默认按钮高度 |
| `--btn-radius-default` | 8px | `--fc-border-radius-base` |

### 色值（ghost · primary · xs，浅色）

| 状态 | 背景 | 文字 |
|------|------|------|
| default | transparent | `var(--fc-violet-11)` |
| hover | `var(--fc-violet-3)` | `var(--fc-violet-11)` |
| pressed | `var(--fc-violet-4)` | `var(--fc-violet-12)` |
| disabled | transparent | `var(--fc-violet-6)` |

### 色值（ghost · quaternary · icon-only）

| 状态 | 背景 | 文字/icon |
|------|------|-----------|
| default | transparent | `var(--fc-text-4)` |
| hover | `rgb(var(--fc-fill-5-rgb) / 0.4)` | `var(--fc-text-2)` |
| pressed | `rgb(var(--fc-fill-5-rgb) / 0.7)` | `var(--fc-text-1)` |
| disabled | transparent | `var(--fc-text-5)` |

其余 variant × hierarchy × destructive 组合在调参页中已预填可编辑 token（命名：`--btn-{variant}-{hierarchy}[-destructive]-{state}-{bg|border|text}`）。

## 使用方式

1. 用浏览器打开 `design-system/cat/button-design-editor.html`（或 `fc-dev-docs/cat/` 下同名文件）。
2. 顶部选择 variant / hierarchy / size / icon / destructive，调「仅当前组合」下的参数。
3. 点 **预览** 看矩阵与状态条；点 **生效** 复制 CSS 变量块给研发（`variable.css` / Meow UI theme）。

重新生成 HTML（改默认 token 后）：`python3 design-system/cat/_gen_button_editor.py`
