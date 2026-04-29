# API 参考文档

本文档详细说明《杖剑传说》自动探索智能 Agent 的 API 接口和使用方法。

---

## 目录
1. [核心类](#核心类)
2. [枚举类型](#枚举类型)
3. [主要方法](#主要方法)
4. [配置参数](#配置参数)
5. [使用示例](#使用示例)

---

## 核心类

### GameAgent

游戏自动化智能 Agent 的核心类，负责状态管理、视觉感知、操作执行等功能。

#### 构造函数

```python
GameAgent(config_path: str = None)
```

**参数**：
- `config_path`（可选）：配置文件路径，默认为 `../config.yaml`

**示例**：
```python
# 使用默认配置
agent = GameAgent()

# 使用自定义配置
agent = GameAgent(config_path="/path/to/custom_config.yaml")
```

---

### GameStats

运行统计信息类，记录 Agent 的运行数据和性能指标。

#### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `explore_count` | int | 盲走探索次数 |
| `battle_count` | int | 战斗次数 |
| `pathfind_count` | int | 寻路次数 |
| `match_success` | int | 匹配成功次数 |
| `match_failed` | int | 匹配失败次数 |
| `start_time` | datetime | 开始运行时间 |
| `last_action_time` | datetime | 最后一次操作时间 |

#### 方法

##### report()

生成并输出统计报告。

```python
agent.stats.report()
```

**输出示例**：
```
==================================================
运行统计:
  探索次数: 123
  战斗次数: 45
  寻路次数: 78
  匹配成功: 234
  匹配失败: 12
  运行时长: 1800秒
==================================================
```

---

## 枚举类型

### GameState

游戏状态枚举，定义 Agent 的所有可能状态。

| 枚举值 | 说明 |
|--------|------|
| `GameState.IDLE` | 空闲扫描状态 |
| `GameState.PATHFINDING` | 寻路移动状态 |
| `GameState.BATTLE` | 战斗处理状态 |
| `GameState.BLIND_EXPLORE` | 盲走探索状态 |
| `GameState.WAIT` | 等待加载状态 |

**示例**：
```python
# 获取当前状态
current_state = agent.state

# 比较状态
if agent.state == GameState.IDLE:
    print("当前处于空闲扫描状态")
```

---

## 主要方法

### 运行控制

#### run()

启动 Agent 主循环，持续执行状态机逻辑。

```python
agent.run()
```

**异常**：
- `KeyboardInterrupt`：按 Ctrl+C 触发，优雅停止
- 其他异常：致命错误，会输出统计信息后退出

**示例**：
```python
try:
    agent.run()
except KeyboardInterrupt:
    print("Agent 已停止")
```

---

### 视觉感知

#### _screenshot()

截取游戏窗口区域，返回 OpenCV 格式的图像。

**返回值**：
- `np.ndarray`：截图图像（BGR 格式）
- `None`：截图失败

**说明**：
- 优先截取游戏窗口区域
- 失败时降级为全屏截图
- 支持配置降级策略

#### _multi_scale_match(template, screenshot)

多尺度模板匹配，返回最佳匹配值和位置。

**参数**：
- `template` (np.ndarray)：模板图片
- `screenshot` (np.ndarray)：截图

**返回值**：
- `Tuple[float, Tuple[int, int]]`：`(最佳匹配值, 最佳位置)`

**说明**：
- 在 `scale_range` 范围内进行多尺度匹配
- 返回的坐标为模板中心点
- 匹配值范围：0.0-1.0

**示例**：
```python
screenshot = agent._screenshot()
template = agent.templates['battle_button']
val, pos = agent._multi_scale_match(template, screenshot)

if val >= 0.8:
    print(f"检测到目标，置信度: {val:.3f}")
```

---

### 操作执行

#### _human_click(x, y)

模拟人类点击操作，包含随机偏移和贝塞尔曲线移动。

**参数**：
- `x` (int)：相对窗口的 x 坐标
- `y` (int)：相对窗口的 y 坐标

**说明**：
- 自动添加随机偏移（`click_offset`）
- 使用贝塞尔曲线模拟真人轨迹
- 包含随机延迟（`click_delay`）

**示例**：
```python
# 点击窗口中心
width, height = 1920, 1080
agent._human_click(width//2, height//2)
```

#### _bezier_move_to(x, y)

贝塞尔曲线鼠标移动，模拟真人轨迹。

**参数**：
- `x` (int)：目标 x 坐标（绝对屏幕坐标）
- `y` (int)：目标 y 坐标（绝对屏幕坐标）

**说明**：
- 使用二次贝塞尔曲线生成平滑轨迹
- 添加随机控制点增加自然感
- 移动时长随机（0.2-0.8秒）

---

### 状态管理

#### _transition_to(new_state, data=None)

状态转换，记录状态切换日志。

**参数**：
- `new_state` (GameState)：目标状态
- `data` (optional)：传递给目标状态的数据

**说明**：
- 记录状态转换日志
- 更新 Agent 当前状态
- 支持传递额外数据

**示例**：
```python
# 切换到战斗状态，传递目标位置
agent._transition_to(GameState.BATTLE, (100, 200))
```

---

### 异常处理

#### _report_stats()

定期报告统计信息，用于监控 Agent 运行状态。

**说明**：
- 每隔 `log_stats_interval` 秒报告一次
- 输出详细的运行统计
- 可手动调用强制报告

---

## 配置参数

完整的配置参数说明请参考 [config-guide.md](config-guide.md)。

### 常用配置项

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `window_title` | str | "杖剑传说" | 游戏窗口标题 |
| `confidence_map` | float | 0.6 | 地图匹配阈值 |
| `confidence_battle` | float | 0.8 | 战斗按钮匹配阈值 |
| `click_offset` | int | 5 | 点击偏移量（像素） |
| `click_delay` | list | [0.1, 0.5] | 点击延迟范围（秒） |
| `battle_delay` | list | [4.0, 6.0] | 战斗等待时间（秒） |
| `max_failed_attempts` | int | 3 | 最大失败尝试次数 |

---

## 使用示例

### 示例 1：基本使用

```python
from scripts.main import GameAgent

# 创建 Agent
agent = GameAgent()

# 启动 Agent
agent.run()
```

### 示例 2：自定义配置

```python
from scripts.main import GameAgent

# 使用自定义配置文件
agent = GameAgent(config_path="/path/to/custom_config.yaml")

# 启动 Agent
agent.run()
```

### 示例 3：监控统计信息

```python
from scripts.main import GameAgent
import time

agent = GameAgent()

# 启动 Agent
agent.run()

# 注意：run() 会阻塞，监控需要在另一个线程中执行
```

### 示例 4：手动执行单次操作

```python
from scripts.main import GameAgent

agent = GameAgent()

# 截图
screenshot = agent._screenshot()

# 匹配模板
if 'battle_button' in agent.templates:
    template = agent.templates['battle_button']
    val, pos = agent._multi_scale_match(template, screenshot)
    
    if val >= agent.config['confidence_battle']:
        # 点击目标
        agent._human_click(pos[0], pos[1])
```

### 示例 5：检查状态

```python
from scripts.main import GameAgent, GameState

agent = GameAgent()

# 获取当前状态
print(f"当前状态: {agent.state.value}")

# 检查是否在战斗中
if agent.state == GameState.BATTLE:
    print("Agent 正在处理战斗")

# 查看统计信息
agent.stats.report()
```

---

## 扩展开发

### 添加新的状态

如果需要添加新的游戏状态，可以按照以下步骤：

1. 在 `GameState` 枚举中添加新状态：
```python
class GameState(Enum):
    # ... 现有状态
    CUSTOM_STATE = "CUSTOM_STATE"  # 新状态
```

2. 在 `GameAgent` 类中实现状态处理方法：
```python
def _state_custom_state(self):
    """自定义状态处理逻辑"""
    # 你的逻辑
    self._transition_to(GameState.IDLE)
```

3. 在 `run()` 方法中添加状态分支：
```python
if self.state == GameState.CUSTOM_STATE:
    self._state_custom_state()
```

### 添加新的模板

在 `assets/` 目录下添加新的模板图片：

1. 截取目标图像
2. 保存为 PNG 或 JPG 格式
3. 放入 `assets/samples/` 目录
4. Agent 会自动加载

### 自定义匹配逻辑

如果需要更复杂的匹配逻辑，可以继承并重写 `_multi_scale_match` 方法：

```python
class CustomAgent(GameAgent):
    def _multi_scale_match(self, template, screenshot):
        # 自定义匹配逻辑
        # 例如：使用不同的匹配算法
        res = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF)
        min_val, _, min_loc, _ = cv2.minMaxLoc(res)
        return (1 - min_val, min_loc)
```

---

## 注意事项

1. **线程安全**：Agent 不是线程安全的，不要在多线程中同时调用
2. **资源释放**：Agent 不会自动释放资源，确保在退出前清理
3. **日志级别**：使用 `logging` 模块调整日志级别
4. **性能优化**：避免频繁调用 `_screenshot()`，尽量复用截图

---

**版本**：1.0.0  
**更新日期**：2026-02-06
