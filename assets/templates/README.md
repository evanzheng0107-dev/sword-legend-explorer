# 模板图片目录

本目录用于存放《杖剑传说》关键界面元素的模板图片。

## 必需文件

### battle_button.png
- **用途**：识别战斗按钮，触发自动战斗
- **要求**：
  - 截取完整的战斗按钮
  - 包含按钮边缘和背景
  - 按钮处于未激活状态
  - 推荐使用 PNG 格式

## 可选文件

可根据需要添加其他模板：
- `menu_button.png`：菜单按钮
- `inventory_icon.png`：背包图标
- `quest_marker.png`：任务标记

## 使用方式

将模板图片放入此目录，并在 `config.yaml` 中配置对应路径。

例如：
```yaml
battle_button_path: "assets/templates/battle_button.png"
```

## 注意事项

1. 确保模板图片与实际游戏界面一致
2. 定期更新模板以适配游戏更新
3. 建议使用 PNG 格式保留透明度
