"""
简化版演示脚本
如果遇到模块导入问题，可以运行此脚本
"""

import cv2
import numpy as np
from ultralytics import YOLO


def main():
    """简化版主函数"""
    print("=== 车流量统计系统演示版 ===")
    
    # 检查是否有视频文件
    video_path = "data/3.mp4"
    if not cv2.VideoCapture(video_path).isOpened():
        video_path = "3.mp4"  # 回退到原始路径
    
    # 初始化YOLO模型
    print("加载YOLO模型...")
    model = YOLO("yolov8m.pt")
    
    # 打开视频
    cap = cv2.VideoCapture(video_path)
    print(f"打开视频文件: {video_path}")
    
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # 每5帧处理一次以提高性能
        if frame_count % 5 != 0:
            continue
        
        # YOLO检测
        results = model.track(frame, persist=True, classes=[2, 3, 5, 7], conf=0.3)
        
        # 绘制检测结果
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            ids = results[0].boxes.id.cpu().numpy()
            
            for box, track_id in zip(boxes, ids):
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"ID:{int(track_id)}", (x1, y1-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # 显示帧数
        cv2.putText(frame, f"Frame: {frame_count}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # 显示结果
        cv2.imshow("Vehicle Detection Demo", frame)
        
        if cv2.waitKey(1) & 0xFF == 27:  # ESC退出
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("演示结束")


if __name__ == "__main__":
    main()
