# 表格分页 · 当前线上样式（设计师可读）

> 更新：2026-05-20  
> 交互调参：**`pagination-design-editor.html`**（支持浅色 / 深色 / 金拱门 切换预览）

---

## 先分清三套「主题」

| 类型 | body 类名 | 是否你要改的默认规格 |
|------|-----------|---------------------|
| **浅色模式** | `theme-light` | ✅ **是**（系统默认） |
| **深色模式** | `theme-dark` | ✅ **是**（与浅色成对） |
| **金拱门主题** | `theme-light` + `theme-light-gold` | ❌ **否**（独立客户主题，麦当劳等） |
| 蓝色主题（少见） | `theme-light` + `theme-light-blue` | ❌ 另一套独立覆盖 |

深浅模式在 `fe/src/utils/darkMode.ts` 里切换；金拱门在 `srm-fe` 等通过 `isMcDonalds` 额外挂 class，**不属于**深浅切换。

---

## 1. 浅色模式（默认）

来源：`fe/vite.config.ts` → `primary-color: #6C53B1`；`variable.css` `:root`

| 状态 | 背景 | 边框 | 文字 |
|------|------|------|------|
| 默认 | `#FFFFFF` | `#D9D9D9` | `rgba(0,0,0,0.85)` |
| Hover | `#FFFFFF` | `#6C53B1` | `#6C53B1` |
| 选中 | `#FFFFFF` | `#6C53B1` | `#6C53B1` |
| 选中+Hover | `#FFFFFF` | `#8162DC` | `#8162DC` |
| 禁用 | `#F5F5F5` | `#D9D9D9` | `rgba(0,0,0,0.25)` |

尺寸：页码 **32×32px**，圆角 **8px**，间距 **4px**。

---

## 2. 深色模式

来源：`fe/src/theme/antd.dark.less`（`primary-color: #8162DC`）

| 状态 | 背景 | 边框 | 文字 |
|------|------|------|------|
| 默认 | **透明** | `rgba(204,204,220,0.2)` | `rgba(255,255,255,0.85)` |
| Hover | 透明 | `#8162DC` | `#8162DC` |
| 选中 | 透明 | `#8162DC` | `#8162DC` |
| 选中+Hover | 透明 | `#5C4797` | `#5C4797` |
| 禁用 | `rgba(255,255,255,0.08)` | `rgba(204,204,220,0.2)` | `rgba(255,255,255,0.3)` |

尺寸与浅色相同（32px / 8px 圆角 / 4px 间距）。

---

## 3. 金拱门主题（仅作对照，非默认）

来源：`fe/src/theme/antd.light-gold.less`（`primary-color: #FFBC0D`）

| 状态 | 边框/文字主色 |
|------|----------------|
| Hover / 选中 | `#FFBC0D` |
| 选中+Hover | `#FFCD36` |

仍为 **白底 + 描边/文字**，不是紫底白字，也不是金底黑字块。

---

## 4. 与设计文档的差异

`design-system-table.md` §8 写「选中 = `--fc-fill-primary` 底 + 白字」——这是**规范目标**。  
**当前线上**（浅/深/金拱门）分页选中页均为 **描边 + 文字强调**，**没有实心填充块**。

---

## 5. 工程文件

| 模式 | 主要文件 |
|------|----------|
| 浅色 | `fe/vite.config.ts`（modifyVars）、`antd/dist/antd.less` |
| 深色 | `fe/scripts/generate_antd_dark_less.js` → `antd.dark.less` |
| 金拱门 | `fe/scripts/generate_antd_gold_less.js` → `antd.light-gold.less` |
| CSS 变量 | `fe/src/theme/variable.css`（`:root` / `.theme-dark` / `.theme-light-gold`） |

---

## 6. 之前调参稿为何像金拱门？

第一版误读了 `antd.light-gold.less`（金拱门），没有读默认的 `vite.config.ts` + `antd.dark.less`。  
现已修正：`pagination-design-editor.html` **默认打开为浅色模式（紫色 #6C53B1）**。
