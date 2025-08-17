# 车流量统计系统 - DeepSORT版本

基于 YOLO 检测和 DeepSORT 跟踪算法的智能车流量统计系统，支持多条检测线的车辆计数和分类统计。

## 与原版本的区别

本版本是原车流量统计系统的DeepSORT版本，主要改进：

- **跟踪算法**: 从YOLO内置的ByteTrack改为DeepSORT算法
- **跟踪精度**: DeepSORT使用深度学习特征提取，跟踪更准确
- **ID稳定性**: 减少ID切换，长时间跟踪更稳定
- **遮挡处理**: 更好地处理目标遮挡和重新出现的情况

## 功能特点

- 支持多种车辆类型检测（汽车、摩托车、公交车、卡车）
- 支持多条检测线设置
- 实时车辆计数和分类统计
- 高精度的车辆轨迹追踪（DeepSORT算法）
- 详细的统计报告生成
- 可视化检测结果

## DeepSORT算法优势

1. **深度特征提取**: 使用CNN提取目标外观特征
2. **卡尔曼滤波**: 预测目标运动轨迹
3. **匈牙利算法**: 优化数据关联
4. **级联匹配**: 多层次匹配策略，提高鲁棒性

## 安装要求

- Python 3.7+
- OpenCV
- Ultralytics YOLO
- DeepSORT Realtime
- PyTorch
- TorchVision
- NumPy

## 快速开始

### 方法一：使用批处理文件（Windows推荐）
```bash
# 进入项目目录
cd traffic_flow_deepsort

# 安装依赖
install.bat

# 运行程序
run.bat
```

### 方法二：手动安装
```bash
# 进入项目目录
cd traffic_flow_deepsort

# 安装依赖
pip install -r requirements.txt

# 运行程序
python main_deepsort.py
```

### 安装问题？
如果遇到安装问题，请查看详细的 [安装指南](INSTALL_GUIDE.md)

## 使用方法

1. 运行程序后会打开设置界面
2. 在视频第一帧上点击两点设置检测线
3. 可设置多条检测线，每条线用不同颜色标识
4. 按 Enter 完成设置，开始车流量统计

## 项目结构

```
traffic_flow_deepsort/
├── src/                           # 源代码
│   ├── line_drawer.py            # 检测线绘制模块
│   ├── vehicle_tracker_deepsort.py # DeepSORT车辆追踪模块
│   ├── counter.py                # 计数模块
│   ├── visualizer.py             # 可视化模块
│   └── __init__.py
├── main_deepsort.py              # 主程序
├── requirements.txt              # 依赖包列表
└── README.md                     # 项目说明
```

## 性能对比

| 特性 | 原版本(ByteTrack) | DeepSORT版本 |
|------|------------------|-------------|
| 跟踪精度 | 高 | 更高 |
| ID稳定性 | 好 | 更好 |
| 遮挡处理 | 一般 | 优秀 |
| 计算开销 | 低 | 中等 |
| 复杂场景适应性 | 好 | 更好 |

## 参数调优

DeepSORT关键参数：
- `max_age`: 轨迹最大存活时间（默认50帧）
- `n_init`: 确认轨迹需要的连续检测次数（默认3）
- `max_iou_distance`: IOU距离阈值（默认0.7）
- `max_cosine_distance`: 余弦距离阈值（默认0.2）

## 使用建议

1. **实时性要求高**: 考虑使用原版本的ByteTrack
2. **精度要求高**: 使用本DeepSORT版本
3. **复杂场景**: 推荐使用DeepSORT版本
4. **简单场景**: 两个版本都可以

## 许可证

MIT License