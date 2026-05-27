# FC Table 设计与落地规范

> 本文沉淀 Table 的可执行规范。讨论过程、未定问题和会议结论记录放在 `2026-05-09-table-style-discussion.md`。

## 1. 输入材料

| 材料 | 定位 | 用法 |
| --- | --- | --- |
| `Table.pdf` | 设计规范主体 | 视觉与交互模式来源 |
| Figma `设计规范` / Table page | 在线设计源 | 校验组件结构、密度、滚动条、分页与行内控件尺寸 |
| `5.9补充` | 设计规范 PDF 的 token 补充 | AntD Table token 取值来源 |
| `[WIP][PRD]flashcat-设计升级专项-表格统一` | PRD 改造范围 | 判断哪些 Table 需要手动改造 |
| 产品设计开发规范 / 详细版 | 产品交互原则 | 分页、排序、过滤、tooltip、删除确认等规则 |
| `cat/fe` main 分支 `/targets` 页面 | 已打磨业务主表样例 | 信息密集型业务表参考，不作为所有 Table 默认密度 |

## 2. 落地策略

Table 默认视觉升级采用 **Ant Design token + 少量全局结构修复优先**。不要把 `.fc-table` 当成所有 Table 的必加类。

| 层级 | 职责 | 落地方式 |
| --- | --- | --- |
| 默认 antd Table 皮肤 | 表格背景、表头、hover、selected、padding、字号、边框、分页基础态 | AntD Less token + `theme/default.less` 全局 patch |
| 页面工具栏 | 搜索、筛选、刷新、批量操作、列设置的布局和控件外观 | `.fc-toolbar`，或在旧页面按现有结构逐步收敛 |
| 复杂表格增强 | 操作列 hover、单元格操作、标签折叠、特殊滚动、固定列兼容 | `.fc-table` 或业务局部 class |
| 信息密集型业务表 | 字段多、状态多、需要压缩局部 padding 或满格状态色 | 业务表格 class，例如 targets 的 `.n9e-hosts-table` |

### 2.1 Figma 对齐口径

需要按 Figma Table 规范统一执行：

- 表头底色、文字色、字号、字重、分隔线和排序/筛选入口。
- 行 hover、selected、sort、fixed column 背景与阴影。
- 操作列三点入口使用 `ghost-quaternary-xs`，并统一 dropdown 触发与菜单样式。
- 宽表滚动时不挤压表头/单元格，不破坏固定列与操作列可见性。

不作为 Figma 统一改造项：

- 分页默认 pageSize。pageSize 仍按产品规范和业务页面历史逻辑处理，不因为 Figma 画板修改。
- Table 密度。Figma 画板中的紧凑行高、紧凑分页只作为具体页面可选规格，不强制所有表格统一成设计稿密度。

## 3. AntD Table Token 基线

5.9 设计规范补充 token 表给出的 Table 基线如下。工程里如果没有设计 token（如 `@text-base`），需要映射为明确像素值。

```ts
'table-bg': 'var(--fc-fill-2)',
'table-header-bg': 'var(--fc-fill-2-5)',
'table-header-color': 'var(--fc-text-3)',
'table-header-sort-bg': 'var(--fc-fill-2-5)',
'table-body-sort-bg': 'rgb(var(--fc-fill-5-rgb) / 0.1)',
'table-row-hover-bg': 'rgb(var(--fc-fill-5-rgb) / 0.2)',
'table-selected-row-color': 'inherit',
'table-selected-row-bg': 'rgb(var(--fc-fill-5-rgb) / 0.15)',
'table-body-selected-sort-bg': '@table-selected-row-bg',
'table-selected-row-hover-bg': 'rgb(var(--fc-fill-5-rgb) / 0.25)',
'table-expanded-row-bg': 'var(--fc-fill-2-5)',
'table-border-color': 'var(--fc-border-color)',
'table-padding-vertical': '16px',
'table-padding-horizontal': '16px',
'table-padding-vertical-md': '(@table-padding-vertical * 3 / 4)',
'table-padding-horizontal-md': '(@table-padding-horizontal / 2)',
'table-padding-vertical-sm': '(@table-padding-vertical / 2)',
'table-padding-horizontal-sm': '(@table-padding-horizontal / 2)',
'table-border-radius-base': '@border-radius-base',
'table-footer-bg': '@table-header-bg',
'table-footer-color': '@table-header-color',
'table-header-bg-sm': '@table-header-bg',
'table-font-size': '12px',
'table-font-size-md': '14px',
'table-font-size-sm': '@table-font-size',
'table-header-cell-split-color': 'var(--fc-border-color)',
'table-header-sort-active-bg': 'rgb(var(--fc-fill-5-rgb) / 0.4)',
'table-fixed-header-sort-active-bg': 'var(--fc-fill-3)',
```

同步位置：

- `fe/vite.config.ts`
- `fe/scripts/generate_antd_dark_less.js`
- `fe/scripts/generate_antd_gold_less.js`
- 如 `srm-fe` 有独立 AntD 构建配置，需要同步同一组 token。

## 4. 容器

```
border: 1px solid var(--fc-border-color)
border-radius: 8px
overflow: hidden
background: var(--fc-fill-2)
```

targets 页面参考：

```tsx
<div className='table-area fc-border rounded-lg'>
  <List />
</div>
```

`table-area` 使用 `padding: 16px`、`height: 100%`、`overflowY: auto`，外层与左侧业务组筛选区并排。

## 5. 表头

```
background: var(--fc-fill-2-5)
color: var(--fc-text-3)
font-size: 12px
font-weight: 500
padding: default 16px 16px / middle 12px 8px / small 8px 8px
sort active: rgb(var(--fc-fill-5-rgb) / 0.4)
```

表头原则：

- 表头高度 40px。
- 无名称图标必须有 tooltip。
- 可排序列不要把排序能力完全隐藏；至少需要三态表达：无排序、降序、升序。
- **排序覆盖**：除操作类的列、或值单一的列以外，其他列默认全部加表头排序。
- **筛选覆盖**：类型类的列（枚举/状态/类别）同时提供表头筛选。
- **表头不换行**：4 个或以内字数的表头不能出现换行；宽表用横向滚动或遮罩，不挤压表头。
- **遮罩 vs 挤压**：当页面压缩到一定程度后，表头/单元格采用遮罩（横向滚动 + 渐隐）的效果，而不是挤压换行。
- Figma Table 示例中，表头单元格内容采用 `8px` 左右内边距、`12px / 18px` 文本、排序/筛选图标 `24px` 点击区。AntD `small` 表格或信息密集场景可按这一组紧凑规格落地；普通主表仍以 token 的默认 padding 为准。
- 表头列分隔线只作为弱分隔使用：Figma 示例为 `1px` 宽、`18px` 高，垂直居中，不做贯穿整行的重分隔线。

### 5.1 表头排序入口

表头排序图标复用 `ghost-quaternary-xs` 的尺寸体系，尺寸见 [12.1.1 ghost-quaternary-xs](#1211-ghost-quaternary-xs)。注意：已排序常态只展示 icon，不展示按钮底色；已排序 icon 颜色使用 `var(--fc-text-3)`，只有 hover 到按钮时才展示 ghost 背景。

显隐规则：

- 无排序状态：表头常态隐藏排序图标，只在 hover 表头单元格时展示排序入口。
- 已生效排序状态：常态固定展示当前排序方向图标（升序或降序），不要只在 hover 时出现；常态无按钮底色。
- hover 已排序表头时：保留当前方向表达，同时允许用户感知可再次切换排序。
- 排序入口点击区为 `24px × 24px`，icon 为 `14px × 14px`，避免图标贴近表头文字或挤压标题。

### 5.2 表头过滤入口

表头过滤图标使用与排序入口相同的尺寸规则：复用 `ghost-quaternary-xs` 的尺寸体系，尺寸见 [12.1.1 ghost-quaternary-xs](#1211-ghost-quaternary-xs)。icon 从 lucide 图标库选择，优先使用能表达过滤的图标，例如 `Funnel`。注意：已过滤常态不展示按钮底色；funnel icon 描边使用 `var(--fc-violet-9)`，闭合 path 填充使用 `var(--fc-violet-4)`。过滤按钮 hover 背景仍使用 `ghost-quaternary-xs` 的 hover 背景，即 `rgb(var(--fc-fill-5-rgb) / 0.4)`。

已过滤状态的 funnel icon 需要使用闭合 path，以便同时支持描边和内部填充。SVG 色值必须使用 token，禁止写死 hex 或 rgb，确保深色模式可适配：

```tsx
<svg width='14' height='14' viewBox='0 0 14 14' fill='none' aria-hidden>
  <path
    d='M5.92074 10.8068C5.86376 10.7146 5.8336 10.6083 5.83365 10.4999V7.58322C5.83365 7.30116 5.73147 7.02866 5.54602 6.81614L2.48415 3.30742C2.40857 3.22367 2.35889 3.1198 2.34113 3.0084C2.32338 2.89699 2.33831 2.78282 2.38411 2.67973C2.42992 2.57664 2.50464 2.48904 2.59921 2.42754C2.69379 2.36604 2.80417 2.33329 2.91699 2.33325H11.0837C11.1964 2.33352 11.3066 2.36643 11.401 2.42802C11.4954 2.4896 11.5699 2.57721 11.6156 2.68026C11.6613 2.78331 11.6761 2.89738 11.6583 3.00868C11.6405 3.11998 11.5908 3.22374 11.5153 3.30742L8.45449 6.81618C8.26912 7.02867 8.16699 7.30112 8.16699 7.58311V11.0833C8.16703 11.1827 8.14165 11.2805 8.09326 11.3674C8.04487 11.4543 7.97508 11.5273 7.8905 11.5796C7.80593 11.6319 7.70939 11.6618 7.61004 11.6663C7.5107 11.6708 7.41186 11.6498 7.3229 11.6053L6.15624 11.022C6.05927 10.9735 5.97772 10.899 5.92074 10.8068Z'
    fill='var(--fc-violet-4)'
    stroke='var(--fc-violet-9)'
    strokeWidth={1.16667}
    strokeLinecap='round'
    strokeLinejoin='round'
  />
</svg>
```

显隐规则：

- 无过滤状态：表头常态隐藏过滤图标，只在 hover 表头单元格时展示过滤入口。
- 已添加过滤状态：常态固定展示过滤图标，并使用激活色 icon，让用户明确感知当前列已过滤；常态无按钮底色。
- hover 已过滤表头时：保留过滤已生效的识别，同时展示 ghost 背景，提示可再次操作。
- 过滤入口点击区为 `24px × 24px`，icon 为 `14px × 14px`，与排序入口保持一致。

过滤下拉交互：

- 点击无过滤状态的表头过滤按钮后，打开 shadcn/Radix 风格下拉选择框。
- 下拉内展示该列所有可筛选项，每个 item 左侧都有 checkbox。
- 当可筛选项超过 5 个时，下拉顶部展示带搜索功能的输入框。
- 下拉底部展示操作区：左侧/次要动作用“重置”，右侧/主动作用“确定”。
- “确定”按钮使用 `text-primary-xs`；“重置”按钮使用 `ghost-quaternary-xs` 的文字按钮形态。
- 下拉容器、item、separator、阴影和圆角沿用表格 dropdown menu 的 shadcn 骨架。
- 筛选下拉、操作菜单等浮层不能被表格容器裁剪；工程实现优先使用 Radix Portal 挂到 `body`，或确保表格外层不以 `overflow: hidden` 截断浮层。

## 6. 单元格

```
height: 40px（单行默认）
padding: default 16px 16px / middle 12px 8px / small 8px 8px
line-height: 1.5
border-bottom: 1px solid var(--fc-border-color)
background: var(--fc-fill-2)
color: var(--fc-text-2)
transition: background-color 0.2s ease
```

普通行内容驱动；如果单行内容确定，按 40px 作为默认行高。信息密集型业务表（如 targets）可局部覆盖到 1px padding + 满格状态色。

Figma Table 页面中的示例行高为 `37px`，内容区文本为 `12px / 18px`，文本距单元格左侧 `8px`，距顶部约 `9px`。这不是全局统一标准，只作为紧凑/嵌入式数据表的页面级选项，不直接覆盖全局 AntD Table 基线。落地时按以下方式区分：

| 场景 | 建议行高 | 说明 |
| --- | --- | --- |
| 路由级主表 / 普通业务表 | `40px` 或内容驱动 | 与 AntD token、可读性和现有主表基线一致 |
| 弹窗、卡片、图表下钻、嵌入式数据表 | `37px` / `small` | 可使用 Figma 紧凑规格：`8px` 水平 padding、`12px / 18px` 文本 |
| 信息密集型监控表 | 业务局部覆盖 | 如 targets 的满格状态色和极窄 padding |

Figma 示例中的列内分隔线为短竖线：`width: 1px`、`height: 18px`、垂直居中，用于强化宽表列边界。实现时优先复用 `table-header-cell-split-color` / `var(--fc-border-color)`，不要新增重色硬编码边框。

targets 页面是信息密集型业务表，局部覆盖为：

```less
.n9e-hosts-table {
  td {
    padding: 1px !important;
    line-height: unset !important;
  }

  .n9e-hosts-table-column-ident,
  .n9e-hosts-table-column-ip,
  .n9e-hosts-table-column-tags,
  .n9e-hosts-table-column-groups {
    text-align: left !important;
    padding: 8px 8px !important;
  }
}
```

不要把 targets 的 `td { padding: 1px !important; }` 提升为全局规范；它只服务于满格状态色单元格。

## 7. 行状态

| 状态 | 背景 |
| --- | --- |
| 默认 | `--fc-fill-2` |
| hover | `rgb(var(--fc-fill-5-rgb) / 0.2)` |
| 排序列 | `rgb(var(--fc-fill-5-rgb) / 0.1)` |
| 选中 | `rgb(var(--fc-fill-5-rgb) / 0.15)` |
| 选中+hover | `rgb(var(--fc-fill-5-rgb) / 0.25)` |
| 展开行 | `var(--fc-fill-2-5)` |

## 8. 分页

分页整体采用 Shadcn 风格（无 AntD 竖向步进条），组件高度固定 24px（旧 AntD 32px 仅作对照）。设计调参稿见 `pagination-design-editor.html`，对应 token 快照见 `pagination-design-snapshot.json`。

### 8.1 尺寸 Token

| Token | 值 | 说明 |
| --- | --- | --- |
| `--pagination-item-size` | `24px` | 页码按钮宽高（`box-sizing: border-box`，1px 描边在内部） |
| `--pagination-item-gap` | `2px` | 页码按钮间距 |
| `--pagination-item-radius` | `6px` | 页码按钮圆角 |
| `--pagination-font-size` | `12px` | 页码数字字号 |
| `--pagination-line-height` | `22px` | 格内行高（24px - 上下各 1px 描边） |
| `--pagination-select-height` | `24px` | 每页条数下拉框高度，与页码对齐 |
| `--pagination-select-radius` | `6px` | 下拉框圆角（高度 &lt;28px → 6px） |
| `--pagination-total-line-height` | `24px` | 总数行高 |
| `--pagination-border-width` | `1px` | 描边在 24px 内部，不外扩 |
| `--pagination-number-input-width` | `44px` | 跳页输入框宽度 |
| `--pagination-number-step-width` | `22px` | 跳页步进按钮宽度 |

**圆角规则（全局）**：组件高度 ≥28px → 圆角 8px；高度 &lt;28px → 圆角 6px。

### 8.2 颜色 Token（浅/深共用 `var(--fc-*)`）

浅色和深色模式共用一套色值变量，通过 `var(--fc-*)` 引用，切换模式自动变色。金拱门（`.theme-light-gold`）色值独立，不走这套 token。

**页码按钮**：

| 状态 | 背景 | 边框 | 文字 | 说明 |
| --- | --- | --- | --- | --- |
| default | `var(--fc-fill-2)` | `transparent` | `var(--fc-text-3)` | 与行背景融为一体 |
| hover | `rgb(var(--fc-fill-5-rgb) / 0.4)` | `transparent` | `var(--fc-text-1)` | 弱背景浮现 |
| pressed | `rgb(var(--fc-fill-5-rgb) / 0.7)` | `transparent` | `var(--fc-text-1)` | 按下加深 |
| active（选中） | `rgb(var(--fc-fill-5-rgb) / 0.2)` | `var(--fc-border-color2)` | `var(--fc-text-2)` | 浅紫底 + 描边 |
| active + hover | `rgb(var(--fc-fill-5-rgb) / 0.4)` | `var(--fc-border-color2)` | `var(--fc-text-1)` | 选中页 hover 加深 |
| disabled | `transparent` | `transparent` | `var(--fc-text-5)` | 不可点击 |
| brand | `transparent` | — | — | 主色不参与页码 |

**箭头 / 省略号**：

| Token | 值 | 说明 |
| --- | --- | --- |
| 箭头 default / hover | `var(--fc-text-3)` | 常态与 hover 同色 |
| 箭头 disabled | `var(--fc-text-5)` | 禁用的箭头 |
| 省略号 | `var(--fc-text-5)` | 「…」颜色 |

**总数 / 每页条数下拉**：

| Token | 值 |
| --- | --- |
| 总数文字 | `var(--fc-text-3)` |
| 下拉背景 | `var(--fc-fill-2)` |
| 下拉边框 | `var(--fc-border-color2)` |
| 下拉文字 | `var(--fc-text-2)` |
| 下拉 hover 背景 | `rgb(var(--fc-fill-5-rgb) / 0.2)` |
| 下拉 hover 边框 | `var(--fc-border-color2)` |

### 8.3 交互规范

- 页码区右侧放页码按钮，左侧放总数和 pageSize 下拉，中间弹性空白。
- pageSize 下拉和跳页输入均采用 Shadcn 风格（无 AntD 竖向步进条）。
- 向前/向后 5 页使用双箭头（`chevrons-left` / `chevrons-right`）；单页使用单箭头（`chevron-left` / `chevron-right`）。
- 页码过多时使用省略号（`…`），不可点击。
- 跳页输入框右侧设上/下步进按钮（`chevron-up` / `chevron-down`），每次 ±1 页。
- 所有图标使用 lucide，尺寸 14px × 14px（页码内）、12px × 12px（跳页步进按钮内），`stroke-width: 2`。

### 8.4 产品规范

- 主表默认要有分页、每页行数选项、总数统计。
- **每页默认 15 行**。每页行数选项必须可选。
- pageSize 改动应持久化，避免用户返回后丢失密度选择。
- targets 当前默认 30 行写入 localStorage，属于历史实现，纳入后续 PRD 改造范围。

targets 页面参考：

```tsx
const pagination = usePagination({ PAGESIZE_KEY: 'targets' });

<Table
  size='small'
  pagination={{
    ...tableProps.pagination,
    ...pagination,
    onChange(page, pageSize) {
      localStorage.setItem('targetsListPageSize', _.toString(pageSize));
    },
  }}
/>
```

## 9. 宽表与滚动

宽表优先使用横向滚动，不压缩列内容到不可读：

```tsx
<Table scroll={{ x: 'max-content' }} tableLayout='auto' />
```

滚动条如需常驻会增加视觉噪音；产品规范倾向常态隐藏、hover 表格区域后展示。是否全局做滚动条样式需要谨慎回归。

Figma Table 示例同时画出了横向和纵向滚动条，作为宽表/高表可滚动状态的显性表达：

| 项 | Figma 示例规格 | 落地建议 |
| --- | --- | --- |
| 滚动条占位 | `10px` | 只在滚动容器内出现，不挤压表头文字 |
| 滑块厚度 | `6px`，距轨道边 `2px` | 可用于 hover/active 状态；默认是否常驻按产品场景决定 |
| 横向滚动 | 表格底部 | 宽表必须可到达最右操作列，固定列阴影需保持可见 |
| 纵向滚动 | 表格右侧 | 高表区域内部滚动时，分页应保持在表格区域底部外侧 |

如果研发实现采用浏览器原生滚动条，不强制还原 Figma 的 `10px/6px` 几何；但需要保证滚动状态可发现、固定列背景不透明、滚动条不遮挡最后一行或分页。

## 10. Ant Design 表格修复

```less
tr.ant-table-measure-row {
  visibility: collapse;
}

.ant-table-cell-fix-left,
.ant-table-cell-fix-right {
  background: inherit;
}
```

这些修复可以先进入全局 patch；如果固定列、展开行或虚拟表出现副作用，再收敛到 `.fc-table` 或页面根 class。

## 11. 工具栏

工具栏推荐左右分区：左侧放刷新、全局搜索、主筛选；右侧放批量操作、探索、列设置。

**全局搜索是默认要求**：所有主表均需提供一个全局关键字搜索入口（位于工具栏左侧）。

```tsx
<div className='fc-toolbar flex flex-wrap items-center justify-between gap-3'>
  <div className='flex flex-wrap items-center gap-3'>
    <Button icon={<ReloadOutlined />} />
    <Select ... />
    <SearchInput ... />
  </div>
  <div className='flex flex-wrap items-center gap-3'>
    <Button type='primary'>新增</Button>
    <Button>批量操作</Button>
    <Button icon={<EyeOutlined />} />
  </div>
</div>
```

targets 页面当前还未使用 `.fc-toolbar`，但结构可作为迁移参考：

```tsx
<div style={{ display: 'flex', justifyContent: 'space-between' }}>
  <Space>{/* refresh/search/filter */}</Space>
  <Space>{/* batch actions/explorer/column settings */}</Space>
</div>
```

控件规格：

| 类型 | 规格 |
| --- | --- |
| 图标按钮 | 32×32，padding 0，icon font-size 12px |
| 文字按钮 | height 32px，padding-inline 12px |
| Input / Select | height 32px，边框 `var(--fc-border-color)` |

icon-only 操作必须有 tooltip。

## 12. 操作列

- 操作类型使用 ghost icon/text button，避免强填充按钮堆叠。
- icon-only 必须加 tooltip。
- 删除必须二次确认，Popconfirm 靠近按钮。
- 启停使用 switch，小号 icon。
- 操作较多时收进 dropdown/menu。
- 操作默认隐藏、row hover 才显示等交互不作为全局默认；复杂表 case by case。

### 12.1 操作列 dropdown

当操作项超过 2 个，或页面是一级列表页的业务主表时，操作列优先收进三点 dropdown。

### 12.1.1 ghost-quaternary-xs

`ghost-quaternary-xs` 是标准 `24px` 图标按钮等级，适用于弱入口、表格操作入口和表头排序入口。后续所有同等级按钮统一使用以下样式。

| 状态 | 按钮 | Icon |
| --- | --- | --- |
| default | `24px × 24px`，`border-radius: 6px`，无背景 | `14px × 14px`，`color: var(--fc-text-4)` |
| hover | `background: rgb(var(--fc-fill-5-rgb) / 0.4)` | `color: var(--fc-text-2)` |
| pressed / active | `background: rgb(var(--fc-fill-5-rgb) / 0.7)` | `color: var(--fc-text-1)` |
| disabled | 无背景 | `color: var(--fc-text-5)` |

参考样式：

```less
.fc-ghost-quaternary-xs {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  padding: 0;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: var(--fc-text-4);
  line-height: 1;
  transition: background-color 0.2s ease, color 0.2s ease;

  .fc-ghost-quaternary-xs-icon,
  svg {
    width: 14px;
    height: 14px;
    color: currentColor;
    font-size: 14px;
  }

  &:hover,
  &:focus-visible {
    background: rgb(var(--fc-fill-5-rgb) / 0.4);
    color: var(--fc-text-2);
  }

  &:active,
  &.is-active {
    background: rgb(var(--fc-fill-5-rgb) / 0.7);
    color: var(--fc-text-1);
  }

  &[disabled],
  &.is-disabled {
    background: transparent;
    color: var(--fc-text-5);
    cursor: not-allowed;
  }
}
```

### 12.1.2 text-primary-xs

`text-primary-xs` 是标准 `24px` 纯文字按钮等级（无背景、无边框），适用于表格操作列外露的低噪声文字操作（如 `Edit`、`Clone`、`Preview`）。后续所有同等级按钮统一使用以下样式。

| 状态 | 按钮 | 文字 / Icon |
| --- | --- | --- |
| default | 高度 `24px`，`padding: 0 8px`，`border-radius: 6px`，无背景 | `color: var(--fc-violet-11)` |
| hover | 无背景 | `color: var(--fc-violet-12)` |
| pressed / active | 无背景 | `color: var(--fc-violet-12)` |
| disabled | 无背景 | `color: var(--fc-violet-6)` |

结构规则：

- icon-only 的弱入口不用 `text-primary-xs`，继续使用 `ghost-quaternary-xs`。
- 文字按钮高度固定 `24px`，左右 padding 固定 `8px`。
- 当出现 icon + 文字组合时，gap 固定 `4px`；当前表格操作列通常不使用 icon + 文字同时出现。
- 操作列外露的普通文字动作使用 `text-primary-xs`；删除等危险动作不要套主色按钮，继续走危险色规则和二次确认。

#### 按钮样式与按钮编辑器的对应关系

表格中所有按钮均对应 `button-design-editor.html` 中的 token 体系：

| 表格按钮 class | 按钮编辑器 Token | 语义 |
| --- | --- | --- |
| `ghost-quaternary-xs` | `--btn-ghost-quaternary-*` | 弱图标按钮（三点、排序、过滤、拖拽） |
| `ghost-quaternary-text-xs` | `--btn-ghost-quaternary-*` | 弱文字按钮（过滤面板“重置”） |
| `text-primary-xs` | `--btn-text-primary-*` | 纯文字操作按钮（Edit、Clone、Preview） |
| `link-primary` | `--btn-link-primary-*` | 主链接（名称、标题等可点击文本） |
| `link-secondary` | `--btn-link-secondary-*` | 次要链接（辅助信息、关联实体） |
| `link-secondary-brand` | `--btn-link-secondary-brand-*` | 品牌色次要链接（页面色彩饱和时替代 primary） |
| `link-tertiary` | `--btn-link-tertiary-*` | 三级链接（需弱化视觉效果时使用） |

按钮编辑器中定义的完整 token 体系（solid / soft / surface / outline / ghost / text / link × primary / destructive / secondary / tertiary / quaternary）为按钮样式的唯一来源，表格中新增按钮类型需先在按钮编辑器中定义 token。

### 12.1.3 链接按钮

表格中所有可点击的链接文本（如实体名称、ID、关联对象等）统一使用按钮编辑器中的 link 按钮样式，默认 `defaultUnderline=false`（常态无下划线，hover 时出现下划线）。

**link-primary**（主链接，对应 `--btn-link-primary-*`）：

| 状态 | 文字色 | 下划线 |
| --- | --- | --- |
| default | `var(--fc-violet-11)` | 无 |
| hover | `var(--fc-violet-12)` | `var(--fc-violet-7)` |
| pressed | `var(--fc-violet-12)` | `var(--fc-violet-8)` |
| disabled | `var(--fc-violet-6)` | 无 |

适用场景：表格中的主实体名称、标题、ID 等作为主要导航入口的链接。

**link-secondary**（次要链接，对应 `--btn-link-secondary-*`）：

| 状态 | 文字色 | 下划线 |
| --- | --- | --- |
| default | `var(--fc-text-2)` | 无 |
| hover | `var(--fc-text-1)` | `var(--fc-text-5)` |
| pressed | `var(--fc-text-1)` | `var(--fc-text-4)` |
| disabled | `var(--fc-text-5)` | 无 |

适用场景：表格中的辅助信息链接、关联对象、数据源名称等作为次要入口的链接。

**link-secondary-brand**（品牌色次要链接，对应 `--btn-link-secondary-brand-*`）：

| 状态 | 文字色 | 下划线 |
| --- | --- | --- |
| default | `var(--fc-text-2)` | 无 |
| hover | `var(--fc-violet-11)` | `var(--fc-violet-6)` |
| pressed | `var(--fc-violet-12)` | `var(--fc-violet-7)` |
| disabled | `var(--fc-violet-6)` | 无 |

适用场景：当页面中已有大量红、橙、黄、绿、紫等标签和状态色，视觉色彩已经饱和时，主链接不适合使用 `link-primary`（紫色文字常态可见），可优先使用 `link-secondary-brand`。该样式默认呈灰色 `text-2` 与普通文字一致，仅在 hover 时才显露品牌紫色，既保留品牌识别，又避免颜色过载。

**link-tertiary**（三级链接，对应 `--btn-link-tertiary-*`）：

| 状态 | 文字色 | 下划线 |
| --- | --- | --- |
| default | `var(--fc-text-3)` | 无 |
| hover | `var(--fc-text-2)` | `var(--fc-text-5)` |
| pressed | `var(--fc-text-1)` | `var(--fc-text-4)` |
| disabled | `var(--fc-text-5)` | 无 |

适用场景：需要弱化链接视觉存在感时使用，例如表格中重复出现的次要字段链接、低优先级关联信息，或空间中已有多处 primary / secondary 链接、需要进一步降低层级的场景。

**规则**：
- 链接选择优先级：`link-primary` > `link-secondary-brand` > `link-secondary` > `link-tertiary`。
- 同一行内有多个链接时，优先级最高的使用 `link-primary`（页面色彩饱和时改用 `link-secondary-brand`），其余依次降级。
- 同一个表格内严禁出现两个及以上的 `link-primary`。
- `defaultUnderline` 统一设为 `false`，保持表格整洁。
- 链接按钮复用 `.fc-link` class 配合 `data-hierarchy="primary|secondary|secondary-brand|tertiary"` 属性。


### 12.1.4 行首拖拽排序 handle

表格行首如果提供拖拽排序入口，拖拽 handle 使用与操作列三点入口一致的 `ghost-quaternary-xs` 样式：

- 按钮尺寸 `24px × 24px`，`border-radius: 6px`。
- icon 尺寸 `14px × 14px`。
- default / hover / pressed / disabled 状态完全复用 `ghost-quaternary-xs`。
- icon 必须从 lucide 图标库选择，优先使用能表达拖拽排序的 grip 类图标，例如 `GripVertical`。
- 行首拖拽列只承载拖拽 handle，不放文字；icon-only 必须有 tooltip 或可访问标签，例如 `aria-label='拖拽排序'`。
- 拖拽中可使用 `is-active` / pressed 态，让用户感知当前行正在被拖动。

推荐实现约束：

- 操作列宽度按内容收窄，常规三点菜单列建议 `width: 64`，不要保留横向按钮时期的宽列。
- 如果表格使用 resizable column 并持久化列宽，调整默认操作列宽时需要同步更新 `persistenceKey` 或清理对应存储，避免旧列宽继续覆盖新配置。
- 图标优先使用 lucide，并按系统内已有同语义图标做映射，避免同一操作语义混用不一致的图形语言；只有 lucide 不能准确表达时再复用现有 AntD icon。
- 触发按钮使用 `ghost-quaternary-xs`，icon 使用 lucide 三点图标，例如 `MoreHorizontal` / `MoreVertical`，icon 尺寸固定为 `14px × 14px`，按钮尺寸固定为 `24px × 24px`。
- 行首拖拽排序 handle 使用 `ghost-quaternary-xs`，icon 从 lucide 选择，例如 `GripVertical`。
- 外露文字操作使用 `text-primary-xs`，例如 `Edit`、`Clone`、`Preview`；多个文字操作之间保持轻量间距，不使用实底按钮堆叠。
- dropdown menu 采用 shadcn/Radix `DropdownMenu` 的结构骨架：`Content` 承载浮层，`Item` 承载单个动作，`Separator` 分组高危操作。不要继续使用 AntD Menu 的默认视觉。
- dropdown 菜单项统一左对齐，且每项包含 lucide icon + 文字说明；同一菜单内避免不同操作使用重复 icon，避免某个业务组件内置按钮 padding 导致文本缩进不一致。
- 常见操作建议映射：预览 `Eye`，设置 `Settings`，克隆/复制 `Copy`，删除 `Trash2`；空间/可见性这类权限范围操作可用 `Network`，不要和预览重复使用 `Eye`。
- dropdown menu 宽度按内容自适应，最小宽度 `100px`。
- 菜单外层圆角 `10px`；菜单项高度固定 `32px`，菜单项圆角 `8px`；没给出的 padding、阴影等值暂时沿用当前 shadcn 骨架，等待设计 token 补齐。
- 菜单项文字字号 `12px`，行高 `18px`，普通文字颜色使用 `var(--fc-text-2)`。
- 普通菜单项 hover/focus 背景使用 `rgb(var(--fc-fill-5-rgb) / 0.2)`。
- 删除等危险操作与普通操作之间用 `DropdownMenuSeparator` 分组；分割线颜色使用 `var(--fc-border-color)`。separator 间距参考 shadcn：`height: 1px`，上下 `4px`，不要省略分割线。danger hover 背景使用 `var(--fc-red-3)`。
- 如果菜单项内部包了业务组件，该组件需要支持透传 `className`、`icon` 或改成统一按钮壳。
- `fe` / `srm-fe` 中新增或改造的一级菜单业务表操作列应优先复用 `@/components/TableActionDropdown`，统一使用 `TableActionButton`、`TableActionLink`、`TableActionTrigger` 和 `TableActionIcon`，不要在各页面重复写三点按钮、菜单按钮 class 和 icon 映射。

参考样式：

```less
.fc-table-action-dropdown {
  .fc-table-action-menu-content {
    width: max-content;
    min-width: 100px;
    padding: 6px;
    border: 1px solid var(--fc-border-color);
    border-radius: 10px;
    background: var(--fc-fill-2);
  }

  .fc-table-action-menu-item {
    display: flex;
    align-items: center;
    gap: 8px;
    min-height: 32px;
    padding: 0 12px 0 8px;
    border-radius: 8px;
    color: var(--fc-text-2);
    font-size: 12px;
    line-height: 18px;
    white-space: nowrap;
  }

  .fc-table-action-menu-item svg {
    flex: none;
    width: 16px;
    height: 16px;
    color: currentColor;
  }

  .fc-table-action-menu-item:hover,
  .fc-table-action-menu-item:focus-visible,
  .fc-table-action-menu-item[data-highlighted] {
    background: rgb(var(--fc-fill-5-rgb) / 0.2);
    color: var(--fc-text-2);
  }

  .fc-table-action-menu-separator {
    display: block;
    height: 1px;
    margin: 4px -6px;
    background: var(--fc-border-color);
  }

  .fc-table-action-menu-item.is-danger,
  .fc-table-action-menu-item[data-danger='true'] {
    color: var(--fc-red-11);
  }

  .fc-table-action-menu-item.is-danger:hover,
  .fc-table-action-menu-item.is-danger:focus-visible,
  .fc-table-action-menu-item.is-danger[data-highlighted],
  .fc-table-action-menu-item[data-danger='true']:hover,
  .fc-table-action-menu-item[data-danger='true']:focus-visible,
  .fc-table-action-menu-item[data-danger='true'][data-highlighted] {
    background: var(--fc-red-3);
  }

  .fc-table-action-menu-item[disabled],
  .fc-table-action-menu-item[aria-disabled='true'] {
    color: var(--fc-text-4);
  }
}
```

- 固定操作列背景应继承当前行状态，避免 hover/selected 断层。

### 12.1.5 单元格操作

单元格操作指不在末尾操作列内，而是对表格中其他列的某个单元格内容直接附加操作入口。与操作列不同，单元格操作常态隐藏，仅在 hover 单元格时浮现。

**单个操作**：

- 操作按钮常态隐藏，hover 单元格时显示。
- 按钮样式使用 `soft-quaternary-xs`（icon-only，`24px × 24px`，`border-radius: 6px`），icon 尺寸 `14px × 14px`。
- `soft-quaternary-xs` icon-only 按钮**必须**附带 Tooltip，显示操作名称，避免纯图标歧义。
- 操作按钮出现时，若单元格内容显示不全，文本自动截断为省略号（`…`），自动避让按钮区域；被截断的文本，鼠标悬停至文本上方时弹出 Tooltip 展示完整信息。

**两个及以上操作**：

- 通过「三点更多」按钮统一收纳，点击或 hover 展开下拉菜单。
- 三点按钮使用 `ghost-quaternary-xs`，icon 使用 lucide 三点图标（`MoreHorizontal` / `MoreVertical`），icon 尺寸 `14px × 14px`，按钮尺寸 `24px × 24px`。
- 下拉菜单的样式、交互规则与下拉菜单项与操作列 dropdown 完全一致，参见 [12.1 操作列 dropdown](#121-操作列-dropdown) 中的推荐实现约束及参考样式。
- 三点按钮同样**必须**附带 Tooltip，例如「更多操作」。

**显隐规则**：

- 常态：单元格仅显示内容，操作按钮不可见。
- hover 单元格：操作按钮（或三点按钮）浮现，单元格内容自动避让、必要时截断。
- 菜单展开时：三点按钮保持 pressed/active 态。


## 13. 内容、链接与标签

- 长文本使用 ellipsis + tooltip/popover/detail。
- 每行是否只保留一个强主链接仍需按业务确认；整行点击和单列点击不要混淆。
- 主副信息聚合不写成硬性规范，具体哪些列合并应 case by case 评审。
- 默认 tag、主题 tag、状态 tag 遵循主设计规范的 Tag 体系。
- 路由级主表中的元数据标签（业务组、用户组、团队、采集条件、labels/tags 等）优先使用统一 `TableTags` 展示，不在页面内重复手写 AntD `Tag` map。
- 元数据标签使用中性样式：`var(--fc-fill-2-5)` 背景、`var(--fc-border-color)` 边框、`var(--fc-text-2)` 文本，避免默认使用 purple。
- 多标签默认单行展示，常规列建议露出 2 个标签，剩余用 `+N` 折叠；`+N` hover/click 展开 popover 显示全部标签。
- 长标签在 tag 内 ellipsis，tooltip 展示完整内容；popover 中仍保留截断，避免长 label 撑开浮层。
- key-value 标签统一显示为 `key=value`；不要同类标签有的只显示 key、有的显示完整 key/value。
- 状态、等级、启停、错误等语义标签继续使用语义色，不强行改成元数据标签样式。

## 14. 状态表达

普通表格优先使用文字色、tag 或轻背景。

targets 当前使用 `table-td-fullBG` 满格状态色展示 CPU、内存、时间偏移和更新时间：

```less
.table-td-fullBG {
  height: 40px;
  color: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 8px;
}
```

这是信息密集型监控对象列表的局部模式，不建议作为所有 Table 的默认状态表达。

## 15. 暂不纳入默认 antd Table 皮肤的表

以下表格需要单独评估，不建议被默认 antd Table 规范直接约束：

- Dashboard `Table` / `TableNG` 渲染器。
- `VirtualTable` / `react-data-grid`。
- `ag-grid` 或自定义网格。
- Log/Trace 搜索结果中需要高密度、虚拟滚动、原始日志查看的表。
- 火图、事件墙等强业务可视化表。

## 16. 落地检查清单

- [ ] 默认样式是否优先通过 AntD token 覆盖，而不是逐页复制深层 CSS？
- [ ] 表格容器是否有 8px 圆角 + 1px 边框？
- [ ] 表头是否使用 `--fc-fill-2-5`、12px、text-3，高度 40px？
- [ ] hover/选中态是否使用规范背景色？
- [ ] 短表头（≤4 字）是否无换行？宽表是否横向滚动 + 遮罩，而不是压缩？
- [ ] icon-only 操作是否有 tooltip？
- [ ] 排序列是否有明确的无排序/降序/升序三态？
- [ ] 类型类列是否提供表头筛选？
- [ ] 工具栏是否提供全局关键字搜索？
- [ ] 分页是否默认 15 行 + 总数统计 + 每页行数选项？
- [ ] 操作隐藏、链接下划线、标签折叠、列聚合是否经过业务 case 评审？
- [ ] 信息密集型业务表的局部样式是否只限制在业务表格 class 内？

## 17. PRD 改造范围

来源：`[WIP][PRD]flashcat-设计升级专项-表格统一`。

### 17.1 页面分类

| 类别 | 含义 | 处理 |
| --- | --- | --- |
| **直接迁移** | 仅需套用本文档的默认 Table 皮肤即可，结构上不重排列 | 工程上更换 token / 容器样式即可 |
| **本 PRD 说明** | 列结构需要按下面 17.3 的位置规则重新组合 | 需要修改 columns 定义和单元格渲染 |
| **不迁移** | 业务可视化表（日志检索、活跃告警、即时查询 Table、Dashboard Table/TableNG、事件墙正文等） | 维持现状，不被默认皮肤约束 |
| **已迁移** | 设备列表 / targets | 局部高密度样式不推广为全局 |

### 17.2 命名约定

PRD 用 `Column1 / Column2 / Column3` 描述一行单元格的位置：

- `Column1`：行首列，常用于状态徽标或主标识缩略图。
- `Column2`：主信息列，可拆分为 `Column2Title`（主标题/链接）和 `Column2Content`（次要信息，多行或多 tag）。
- `Column3`：补充信息列（数据源、归属等）。
- 操作列固定在最右侧，沿用本文档的"操作列"规范。

### 17.3 需结构改造的页面（来源 p1-table-prd）

| 页面 | route | Column 位置说明 |
| --- | --- | --- |
| 告警管理 - 规则管理 - 告警规则 | `/alert-rules` | `Column1`：状态。`Column2Title`：名称。`Column2Content`：类型、业务组、级别。`Column3`：数据源。 |
| 告警管理 - 规则管理 - 屏蔽规则 | `/alert-mutes` | `Column1Title`：规则标题。`Column1Content`：数据源类型、业务组。 |
| 告警管理 - 规则管理 - 订阅规则 | `/alert-subscribes` | `Column1Title`：订阅名称。`Column1Content`：业务组。 |
| 告警管理 - 告警自愈 - 自愈脚本 | `/job-tpls` | `Column1Title`：标题。`Column1Content`：ID、业务组。 |
| 告警管理 - 告警自愈 - 历史任务 | `/job-tasks` | `Column1Title`：标题。`Column1Content`：ID、业务组。 |
| 基础设施 - 数据集成 - 采集规则 | `/settings/source/:type` | `Column1Title`：规则名称。`Column1Content`：组件、业务组、插件类型。 |
| 基础设施 - 设备列表 - 网络设备 | `/targets`（网络设备分支） | `Column1Title`：IP。`Column1Content`：设备名称、业务组、机房。 |
| 人员管理 - 用户管理 | `/users` | `Column1Title`：用户名。`Column1Content`：显示名、邮箱、手机号。 |

### 17.4 设计师待补齐的细节

下列页面"直接迁移"，但设计还需补齐部分元素的视觉规范，工程实现需等设计稿落地：

- 北极星 - 指标池：操作、多个超链接、开关。
- 北极星 - 状态概览：折叠/展开、表头排序、表头过滤。
- 灭火图 - 从模板生成规则：高亮单元格 - 展示 Tips。
- 事件墙 - 视图设置：可拖拽。
- 事件墙 - 视图设置 - 编辑视图 - 字段配置：添加行。
- 链路分析 - 应用列表：收藏、指标曲线。
- 告警管理 - 通知媒介、告警管理 - 工作流：当前操作/状态列未统一，特例处理。
- 指标分析 - 指标视图：操作列特例。
- 容器平台 - Kubernetes - 右侧弹窗：操作列特例。
- 系统配置 - 站内公告：富文本。
- 系统配置 - 告警引擎：合并单元格。
- 系统配置 - 关于：勾选（或复用开关）。

更细的 srm-fe 表格清单见 [2026-05-09-srm-fe-table-inventory.md](./2026-05-09-srm-fe-table-inventory.md)。
