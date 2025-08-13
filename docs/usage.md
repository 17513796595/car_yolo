# 使用指南

## 系统要求

- Python 3.7 或更高版本
- 至少 4GB RAM
- GPU（可选，用于加速推理）

## 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/yourusername/traffic-flow-counter.git
cd traffic-flow-counter
```

2. **创建虚拟环境（推荐）**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **下载YOLO模型**
系统会在首次运行时自动下载 `yolov8m.pt` 模型文件。

## 使用方法

### 基本使用

1. **准备视频文件**
   - 将视频文件放在 `data/` 目录下
   - 支持常见格式：mp4, avi, mov 等

2. **运行程序**
```bash
python main.py
```

3. **设置检测线**
   - 程序启动后会显示视频第一帧
   - 用鼠标点击两个点设置一条检测线
   - 可以设置多条检测线
   - 按 Enter 键完成设置

4. **开始统计**
   - 设置完成后自动开始车流量统计
   - 按 ESC 键退出程序

### 高级功能

#### 修改配置

编辑 `config/settings.py` 文件来自定义系统参数：

```python
# 修改置信度阈值
MODEL_CONFIG["confidence_threshold"] = 0.3

# 修改检测的车辆类型
MODEL_CONFIG["vehicle_classes"] = [2, 3, 5, 7]  # 2=car, 3=motorcycle, 5=bus, 7=truck
```

#### 使用自定义视频

在 `main.py` 中修改视频路径：

```python
system = TrafficFlowCounter(
    model_path="yolov8m.pt",
    video_path="data/your_video.mp4"
)
```

## 操作说明

### 设置检测线界面

- **鼠标左键**：点击两次设置一条检测线
- **N 键**：准备设置下一条线
- **R 键**：重置所有检测线
- **Enter 键**：完成设置，开始统计

### 统计界面

- **ESC 键**：退出程序并显示统计报告

## 输出说明

### 实时显示

- 绿色框：检测到的车辆
- 彩色线：检测线
- 黄色轨迹：车辆运动轨迹
- 灰色框：低置信度检测（不计数）

### 统计报告

程序结束时会打印详细的统计报告，包括：
- 总车辆数
- 各条检测线的车辆数
- 车辆类型分布
- 百分比统计

## 常见问题

### Q: 检测精度不高怎么办？
A: 可以调整配置文件中的置信度阈值，或使用更大的YOLO模型（如yolov8l.pt）。

### Q: 如何处理不同的视频分辨率？
A: 系统会自动适应不同分辨率，但建议调整距离阈值以获得最佳效果。

### Q: 能否检测其他类型的对象？
A: 可以修改 `MODEL_CONFIG["vehicle_classes"]` 来检测其他COCO类别的对象。

## 技术支持

如有问题，请提交 GitHub Issue 或联系项目维护者。
