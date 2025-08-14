# Excalidraw 系统架构图绘制规范

## 1. 概述

为了统一团队内部系统架构图的绘制风格，确保图表资产的**清晰性**、**可读性**与**可维护性**，特制定本规范。所有使用 Excalidraw 创建的系统架构图、数据流程图等技术图表，均应遵循此文档。

本规范的核心目标是，让每一张图都不仅仅是视觉呈现，更是一份**结构化、语义化、易于解析和二次开发的“活文档”**。

## 2. 核心设计原则

在开始绘制前，请理解并遵循以下核心设计原则：

*   **结构清晰，分层明确**: 复杂的系统应通过分层（Layering）来表达数据处理的阶段性。例如，自动驾驶系统常见的**输入层、感知层、融合层、决策规划层、输出层**。
*   **语义明确，善用颜色**: 颜色不是为了美观，而是为了传递信息。应建立一套统一的颜色编码体系，用以区分不同类型或功能的模块。
*   **数据流向，主次分明**: 使用箭头清晰、无歧义地表示数据或控制信号的流向。对于不同性质的流（如主要数据流 vs. 辅助信号），应使用不同线型加以区分。
*   **模块分组，体现层级**: 对于包含多个子模块的复杂功能单元，应使用分组（Grouping）或容器（Container）来体现其内部的层次结构和整体性。
*   **文本精准，信息核心**: 文本是图表的灵魂，必须准确无误地传达模块功能、数据内容等核心信息。

## 3. 具体绘制要求

### 3.1. 结构与布局 (Structure & Layout)

*   **分层表示**: 使用大型、半透明、置于底层的矩形来划分不同的逻辑层级，并为每个层级添加明确的文本标签（如：`输入层`）。
*   **对齐与间距**: 同一层级或同一分组内的模块应保持逻辑上的对齐（如顶部对齐、中心对齐），并保持适当、一致的间距，使布局整洁、匀称。

### 3.2. 节点/形状 (Nodes/Shapes)

*   **统一形状**: 功能模块统一使用 **圆角矩形 (Rectangle with rounded corners)**。
*   **颜色编码**: 严格遵守预定义的颜色规范。**建议**:
    *   **绿色**: 数据输入源 (e.g., Lidar, Camera, CAN)
    *   **浅蓝色**: 单一数据源的处理/感知模块 (e.g., Lidar Perception)
    *   **深蓝色/紫色**: 核心算法/处理单元 (e.g., SLAM, Fusion Core)
    *   **黄色**: 跨模块/跨传感器的融合模块
    *   **橙色**: 特定领域的业务逻辑模块 (e.g., Parking Slot Detection)
    *   **粉色/肉色**: 系统输出 (e.g., Planning Trajectory, Final Objects)
*   **逻辑容器**: 对于需要体现包含关系的复杂模块（如 `Super-Odom` 内部），应使用一个大的圆角矩形作为父容器，并将子模块和内部连线置于其中。
*   **逻辑分组框**: 对于非物理包含，仅为逻辑上相关的模块集合，可使用**虚线矩形框**进行框选，以示其关联性。

### 3.2.1. 形状通用属性 (General Shape Properties)

所有形状（包括 `rectangle`, `ellipse`, `diamond` 等）都共享一套通用的JSON属性，用于定义其外观和行为。以下是核心属性的说明，所有AI生成代码时必须遵循这些结构：

*   **`id`**: 字符串(string)。全局唯一的元素标识符。
*   **`type`**: 字符串(string)。定义元素类型，如 `"rectangle"`, `"text"`, `"arrow"`。
*   **`x`, `y`**: 数字(number)。元素左上角的绝对坐标。
*   **`width`, `height`**: 数字(number)。元素的尺寸。
*   **`strokeColor`**: 字符串(string)。边框颜色，十六进制代码 (e.g., `"#1e1e1e"`).
*   **`backgroundColor`**: 字符串(string)。背景填充色，十六进制代码 (e.g., `"#ffffff"`).
*   **`fillStyle`**: 字符串(string)。填充样式，通常为 `"solid"`。
*   **`strokeWidth`**: 数字(number)。边框宽度。
*   **`strokeStyle`**: 字符串(string)。边框样式，如 `"solid"` (实线), `"dashed"` (虚线)。
*   **`roundness`**: 对象(object)或null。定义圆角，对于圆角矩形，其结构为 `{"type": 3}`。
*   **`opacity`**: 数字(number)。透明度，范围 0-100。
*   **`boundElements`**: 数组(array)或null。用于记录与此形状绑定的其他元素的ID和类型。这是实现形状与文本、箭头关联的关键。
    *   例如: `[{"type": "text", "id": "AdagHdE5hX6gQ2fQeXF8F"}]` 表示一个文本元素绑定到了这个形状上。
*   **`containerId`**: 字符串(string)或null。**此属性属于子元素（如 `text`）**，指向其父容器形状的 `id`。

**示例 - 一个完整的矩形 (Rectangle) 元素:**

```json
{
  "id": "de0xEycws0RapoqB8dGjN",
  "type": "rectangle",
  "x": 259.55,
  "y": 223.44,
  "width": 520.44,
  "height": 388.44,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roundness": { "type": 3 },
  "opacity": 100,
  "boundElements": [
    {
      "type": "text",
      "id": "bn1LnTSiagS86i5y_90K9"
    }
  ],
  // ... 其他次要属性 ...
}
```

### 3.3. 连接线与箭头 (Connectors & Arrows)

*   **绑定节点**: 所有连接线的起点和终点**必须**与节点的边框进行**绑定 (bind)**。这确保在移动节点时，连接线能自动跟随调整。
*   **线条样式**:
    *   **实线箭头 (Solid Arrow)**: 用于表示主要的、持续的数据流。
    *   **虚线箭头 (Dashed Arrow)**: 用于表示辅助性、触发式或次要的信息流（如配置、状态反馈、辅助信号等）。
*   **路由清晰**: 优先使用**直角连接线 (orthogonal connectors)**，并手动调整路由，避免线条交叉和混乱，确保数据流向一目了然。
*   **线上标签**: 关键的数据流应在线条旁边或中间添加文本标签（如 `Odom Pose`, `Detected Objects`），以说明传递的数据内容。
*   **箭头平行**: 箭头应尽量保证**平行或垂直**，因此要求**箭头两侧的element**也应该尽量保持中心平行或垂直对齐。

### 3.4. 文本元素 (Text Elements)

这是本规范中**最重要**的技术要求，旨在确保图表的可解析性和自动化处理能力。

*   **核心要求：所有文本标签必须作为独立的 `text` 元素存在，并与相应的父形状（如矩形）进行链接（boundElements和containerId），而不是直接写入形状的 `text` 属性中。**

*   **目的**: 这样做可以确保文本和形状在数据层面解耦，便于脚本自动化处理、解析和修改图表内容，同时在 Excalidraw 编辑器中也能获得更好的编辑灵活性（例如，独立调整文本位置而不影响形状）。

*   **示例**:

    **✅ 正确示例：** 文本是一个独立的元素，通过 `containerId` 和 `boundElements` 字段互相指向父/子元素的 `id`。

    ```json
    // --- 形状元素 (父) ---
    {
      "id": "MacekLaswcvUl8kOFMZxd",
      "type": "rectangle",
      "boundElements": [
        {
          "type": "text",
          "id": "AdagHdE5hX6gQ2fQeXF8F"
        }
      ],
      // ...其他属性...
    },
    // --- 文本元素 (子) ---
    {
      "id": "AdagHdE5hX6gQ2fQeXF8F",
      "type": "text",
      "containerId": "MacekLaswcvUl8kOFMZxd",
      "text": "传感器时空匹配\n与对齐",
      "link": "Yd1B4v7wN", // 指向父元素的 id
      // ...其他属性...
    }
    ```

    **❌ 错误示例：** 文本直接作为矩形的一个属性存在。

    ```json
    // --- 矩形元素 (包含了不应有的文本) ---
    {
      "id": "Yd1B4v7wN",
      "type": "rectangle",
      "text": "鱼眼高精\n点线圆柱\n矩形检测", // 错误！文本不应在这里
      "link": null,
      // ...其他属性...
    }
    ```

*   **对于箭头的扩展**: 同样需要注意像arrow等的连接也要正确使用 `boundElements` 和 `startBinding`，示例：
   
    ```json
    // --- 形状元素 (父) ---
    {
      "id": "KFfSvxXOiHS-6cE7A4N3x",
      "type": "rectangle",
      "boundElements": [
        {
          "id": "JmkPcwyqkXxcu_70o_cQv",
          "type": "arrow"
        }
      ],
      // ...其他属性...
    },
        {
      "id": "4dhMjybHWtU3bsPS_JqA4",
      "type": "rectangle",
      "boundElements": [
        {
          "id": "JmkPcwyqkXxcu_70o_cQv",
          "type": "arrow"
        }
      ],
      // ...其他属性...
    },
    // --- 箭头元素 (子) ---
    {
      "startBinding": {
        "elementId": "KFfSvxXOiHS-6cE7A4N3x",// 指向父元素的 id
        "focus": -0.31267335386971307,
        "gap": 2.66668701171875
      },
      "endBinding": {
        "elementId": "4dhMjybHWtU3bsPS_JqA4",// 指向父元素的 id
        "focus": -0.2728629641329067,
        "gap": 1
      }, 
      // ...其他属性...
    }
    ```

*   **其他文本要求**:
    *   **准确性**: 文本内容必须一字不差，准确反映模块功能。
    *   **对齐**: 链接到形状的文本，应在视觉上保持**水平和垂直居中**。
    *   **字体**: 使用 Excalidraw 默认的无衬线手绘字体即可，保持整体风格统一。

### 3.5. 可编辑性与可维护性 (Editability & Maintainability)

*   **纯粹矢量**: 严禁在图表中粘贴或嵌入任何原始位图（截图）。整个图表必须由 Excalidraw 的矢量元素（形状、线条、文本）构成。
*   **善用分组**: 积极使用**组合 (Group)** 功能。将逻辑上强相关的单元（如一个完整的子系统、一个父容器及其所有子模块）组合在一起，方便整体移动、复制和编辑。
*   **对象整洁**: 避免创建无用的、重叠的或隐藏的对象。定期检查并清理图表，保持其数据结构的干净。

---

**总结**: 遵循此规范绘制的 Excalidraw 图，将成为团队宝贵的、可复用的工程资产。它不仅服务于当下的沟通演示，更能为未来的系统分析、文档自动化和知识沉淀打下坚实的基础。

## 4. 文件格式要求 (File Format Requirements)

为了确保 `.excalidraw` 文件可以被程序正确解析和加载，其顶层JSON结构必须遵循以下规范：

*   **根对象 (Root Object)**: 整个文件内容必须是一个合法的JSON对象。
*   **类型标识 (Type Identifier)**: JSON根对象必须包含一个`type`字段，其值必须为字符串 `"excalidraw"`，注意大小写要保持一致。这是识别文件的关键。
    *   `"type": "excalidraw"`
*   **元素数组 (Elements Array)**: 如果文件中存在 `elements` 字段，它必须是一个JSON数组 (Array)。该数组包含了画布上所有的形状、线条、文本等元素。
*   **应用状态 (App State)**: 如果文件中存在 `appState` 字段，它必须是一个JSON对象 (Object)。该对象存储了画布的视图状态，如缩放、滚动位置等。

**示例 - 一个合法的最小 .excalidraw 文件结构:**

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  }
}
```
