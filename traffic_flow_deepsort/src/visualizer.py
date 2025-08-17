"""
可视化模块
用于在视频帧上绘制检测结果和统计信息
"""

import cv2
from typing import List, Dict


class Visualizer:
    """可视化工具"""
    
    @staticmethod
    def draw_detection_box(frame, box, track_id: int, vehicle_type: str) -> None:
        """绘制车辆检测框"""
        x1, y1, x2, y2 = box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"ID:{track_id} ({vehicle_type})", 
                   (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # 绘制中心点
        cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
        cv2.circle(frame, (cx, cy), 4, (255, 0, 0), -1)
    
    @staticmethod
    def draw_low_confidence_detections(frame, detections) -> None:
        """绘制低置信度检测结果"""
        for detection in detections:
            boxes = detection.boxes
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = box.conf[0].cpu().numpy()
                    
                    # 只显示置信度在0.2-0.3之间的检测
                    if 0.2 <= conf < 0.3:
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (128, 128, 128), 1)
                        cv2.putText(frame, f"Low:{conf:.2f}", (x1, y1 - 5), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (128, 128, 128), 1)
    
    @staticmethod
    def draw_detection_lines(frame, lines: List[Dict], line_counts: List[int]) -> None:
        """绘制检测线和计数"""
        for line_idx, line_data in enumerate(lines):
            points = line_data['points']
            color = line_data['color']
            name = line_data['name']
            count = line_counts[line_idx]
            
            # 绘制检测线
            cv2.line(frame, points[0], points[1], color, 3)
            cv2.circle(frame, points[0], 6, color, -1)
            cv2.circle(frame, points[1], 6, color, -1)
            
            # 在线的中点显示计数
            mid_x = (points[0][0] + points[1][0]) // 2
            mid_y = (points[0][1] + points[1][1]) // 2
            cv2.putText(frame, f"{name}: {count}", (mid_x + 15, mid_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    
    @staticmethod
    def draw_statistics(frame, lines: List[Dict], counter, detected_count: int) -> None:
        """绘制统计信息"""
        y_offset = 30
        total_count = counter.get_total_count()
        cv2.putText(frame, f"Total Vehicles: {total_count} (DeepSORT)", (20, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # 显示每条线的详细计数和分类统计
        for line_idx, line_data in enumerate(lines):
            y_offset += 35
            count = counter.get_line_count(line_idx)
            color = line_data['color']
            name = line_data['name']
            class_count = counter.get_class_counts(line_idx)
            
            # 显示总计数
            cv2.putText(frame, f"{name}: {count} total", (20, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            
            # 显示分类计数（只显示非零的类别）
            y_offset += 25
            class_info = []
            for vehicle_class, class_count_val in class_count.items():
                if class_count_val > 0:
                    class_info.append(f"{vehicle_class}:{class_count_val}")
            
            if class_info:
                class_text = " | ".join(class_info)
                cv2.putText(frame, f"  {class_text}", (30, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)
        
        # 显示当前检测到的车辆数
        cv2.putText(frame, f"Detected: {detected_count}", 
                   (20, y_offset + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)