"""
配置文件
包含系统的各种配置参数
"""

import cv2

# YOLO模型配置
MODEL_CONFIG = {
    "model_path": "yolov8m.pt",
    "confidence_threshold": 0.1,
    "low_confidence_threshold": 0.2,
    "vehicle_classes": [2, 3, 5, 7],  # car, motorcycle, bus, truck
    "tracker": "bytetrack.yaml"
}

# 检测线配置
LINE_CONFIG = {
    "colors": [
        (0, 0, 255),    # 红色
        (0, 255, 0),    # 绿色
        (255, 0, 0),    # 蓝色
        (255, 255, 0),  # 青色
        (255, 0, 255),  # 品红
        (0, 255, 255)   # 黄色
    ],
    "line_thickness": 3,
    "point_radius": 6
}

# 车辆追踪配置
TRACKING_CONFIG = {
    "max_track_length": 5,           # 保留的最大轨迹点数
    "distance_threshold": 8,         # 距离阈值（像素）
    "class_names": {
        2: 'car',
        3: 'motorcycle', 
        5: 'bus',
        7: 'truck'
    }
}

# 显示配置
DISPLAY_CONFIG = {
    "window_name": "Traffic Flow Counter",
    "font": cv2.FONT_HERSHEY_SIMPLEX,
    "font_scale": 0.8,
    "font_thickness": 2,
    "text_color": (255, 255, 255)
}

# 输出配置
OUTPUT_CONFIG = {
    "save_video": False,
    "output_path": "output/",
    "report_format": "txt"  # txt, json, csv
}
