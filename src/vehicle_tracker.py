"""
车辆追踪模块
用于追踪车辆轨迹和检测车辆穿越检测线
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional


class VehicleTracker:
    """车辆追踪器"""
    
    def __init__(self):
        self.vehicle_tracks = {}  # 存储每个车辆的历史位置
        self.class_names = {2: 'car', 3: 'motorcycle', 5: 'bus', 7: 'truck'}
    
    def update_tracks(self, track_id: int, position: Tuple[int, int]) -> None:
        """更新车辆轨迹"""
        if track_id not in self.vehicle_tracks:
            self.vehicle_tracks[track_id] = []
        
        self.vehicle_tracks[track_id].append(position)
        # 保留最近5个位置
        if len(self.vehicle_tracks[track_id]) > 5:
            self.vehicle_tracks[track_id].pop(0)
    
    def get_previous_position(self, track_id: int) -> Optional[Tuple[int, int]]:
        """获取车辆的前一个位置"""
        if track_id in self.vehicle_tracks and len(self.vehicle_tracks[track_id]) > 1:
            return self.vehicle_tracks[track_id][-2]
        return None
    
    def draw_tracks(self, frame, track_id: int) -> None:
        """绘制车辆轨迹"""
        if track_id in self.vehicle_tracks and len(self.vehicle_tracks[track_id]) > 1:
            for i in range(1, len(self.vehicle_tracks[track_id])):
                pt1 = self.vehicle_tracks[track_id][i-1]
                pt2 = self.vehicle_tracks[track_id][i]
                cv2.line(frame, pt1, pt2, (0, 255, 255), 1)
    
    @staticmethod
    def point_to_line_distance(px: int, py: int, x1: int, y1: int, x2: int, y2: int) -> float:
        """计算点到线段的距离"""
        return abs((y2 - y1) * px - (x2 - x1) * py + x2 * y1 - y2 * x1) / (
            ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
        )
    
    @staticmethod
    def is_crossing_line(prev_pos: Tuple[int, int], curr_pos: Tuple[int, int], 
                        line_start: Tuple[int, int], line_end: Tuple[int, int]) -> bool:
        """判断两个点之间的轨迹是否穿越了检测线"""
        if prev_pos is None or curr_pos is None:
            return False
        
        x1, y1 = prev_pos
        x2, y2 = curr_pos
        x3, y3 = line_start
        x4, y4 = line_end
        
        # 使用线段相交算法
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(denom) < 1e-10:
            return False
        
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
        
        # 检查是否在线段范围内相交
        return 0 <= t <= 1 and 0 <= u <= 1
    
    @staticmethod
    def get_line_side(point: Tuple[int, int], line_start: Tuple[int, int], 
                     line_end: Tuple[int, int]) -> float:
        """判断点在直线的哪一侧"""
        x, y = point
        x1, y1 = line_start
        x2, y2 = line_end
        return (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
    
    def get_vehicle_type(self, cls_id: int) -> str:
        """获取车辆类型名称"""
        return self.class_names.get(cls_id, 'unknown')
