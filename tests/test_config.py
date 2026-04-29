import yaml
import os

# 加载配置文件（适配项目路径）
def load_config():
    # 定位到当前目录的config.yaml（因为运行时工作目录是sword-legend-explorer）
    config_path = os.path.join(os.getcwd(), "config.yaml")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        print("✅ 配置文件加载成功！")
        # 打印核心配置项验证
        print(f"窗口标题：{config['window_title']}")
        print(f"窗口区域：{config['window_region']}")
        print(f"战斗匹配阈值：{config['confidence_battle']}")
        return config
    except Exception as e:
        print(f"❌ 配置加载失败：{e}")
        # 打印当前工作目录帮助调试
        print(f"当前工作目录：{os.getcwd()}")
        return None

if __name__ == "__main__":
    load_config()