"""
计数模块
用于统计车辆穿越检测线的数量和分类
"""

from typing import Dict, List, Set
from .vehicle_tracker_deepsort import VehicleTrackerDeepSORT


class TrafficCounter:
    """车流量计数器"""
    
    def __init__(self, lines: List[Dict]):
        self.lines = lines
        self.line_counts = [0] * len(lines)  # 每条线的计数
        self.line_passed_ids = [set() for _ in range(len(lines))]  # 每条线已通过的车辆ID
        
        # 车辆分类统计
        self.line_class_counts = []
        for _ in range(len(lines)):
            self.line_class_counts.append({
                'car': 0, 'motorcycle': 0, 'bus': 0, 'truck': 0
            })
    
    def check_crossing(self, track_id: int, current_pos, prev_pos, cls_id: int, 
                      vehicle_tracker: VehicleTrackerDeepSORT) -> None:
        """检查车辆是否穿越任意一条检测线"""
        vehicle_type = vehicle_tracker.get_vehicle_type(cls_id)
        
        for line_idx, line_data in enumerate(self.lines):
            line_points = line_data['points']
            line_start = line_points[0]
            line_end = line_points[1]
            
            # 只有当车辆ID未被此线计数过时才检查
            if track_id not in self.line_passed_ids[line_idx] and prev_pos is not None:
                # 使用轨迹穿越检测
                if vehicle_tracker.is_crossing_line(prev_pos, current_pos, line_start, line_end):
                    self._record_crossing(track_id, line_idx, line_data, vehicle_type)
                
                # 备用方案：距离检测
                else:
                    cx, cy = current_pos
                    dist = vehicle_tracker.point_to_line_distance(
                        cx, cy, line_start[0], line_start[1], line_end[0], line_end[1]
                    )
                    
                    if dist < 8:  # 8像素阈值
                        # 检查车辆是否从检测线的一侧移动到另一侧
                        if track_id in vehicle_tracker.vehicle_tracks and len(vehicle_tracker.vehicle_tracks[track_id]) >= 2:
                            prev_side = vehicle_tracker.get_line_side(
                                vehicle_tracker.vehicle_tracks[track_id][-2], line_start, line_end
                            )
                            curr_side = vehicle_tracker.get_line_side(current_pos, line_start, line_end)
                            
                            # 如果符号不同，说明穿越了检测线
                            if prev_side * curr_side < 0:
                                self._record_crossing(track_id, line_idx, line_data, vehicle_type)
    
    def _record_crossing(self, track_id: int, line_idx: int, line_data: Dict, vehicle_type: str) -> None:
        """记录车辆穿越检测线"""
        self.line_passed_ids[line_idx].add(track_id)
        self.line_counts[line_idx] += 1
        
        # 更新分类计数
        if vehicle_type in self.line_class_counts[line_idx]:
            self.line_class_counts[line_idx][vehicle_type] += 1
        
        print(f"车辆 ID-{track_id} ({vehicle_type}) 穿越了 {line_data['name']}! 该线计数: {self.line_counts[line_idx]}")
    
    def get_total_count(self) -> int:
        """获取总车辆数"""
        return sum(self.line_counts)
    
    def get_line_count(self, line_idx: int) -> int:
        """获取指定线的计数"""
        return self.line_counts[line_idx]
    
    def get_class_counts(self, line_idx: int) -> Dict[str, int]:
        """获取指定线的分类计数"""
        return self.line_class_counts[line_idx]
    
    def print_report(self) -> None:
        """打印统计报告"""
        print("\n" + "="*50)
        print("多线车辆分类统计报告 - DeepSORT版本")
        print("="*50)
        
        total_vehicles = self.get_total_count()
        total_by_class = {'car': 0, 'motorcycle': 0, 'bus': 0, 'truck': 0}
        
        print(f"总车辆数: {total_vehicles}")
        print("-" * 30)
        
        # 计算每条线的统计
        for line_idx, line_data in enumerate(self.lines):
            name = line_data['name']
            count = self.line_counts[line_idx]
            percentage = (count / total_vehicles * 100) if total_vehicles > 0 else 0
            class_count = self.line_class_counts[line_idx]
            
            print(f"{name}: {count} 辆 ({percentage:.1f}%)")
            
            # 显示分类详情
            for vehicle_class, class_count_val in class_count.items():
                if class_count_val > 0:
                    class_percentage = (class_count_val / count * 100) if count > 0 else 0
                    print(f"  {vehicle_class}: {class_count_val} 辆 ({class_percentage:.1f}%)")
                    total_by_class[vehicle_class] += class_count_val
            print()
        
        print("-" * 30)
        print("全部车辆类型统计:")
        for vehicle_class, total_class_count in total_by_class.items():
            if total_class_count > 0:
                class_percentage = (total_class_count / total_vehicles * 100) if total_vehicles > 0 else 0
                print(f"{vehicle_class}: {total_class_count} 辆 ({class_percentage:.1f}%)")
        
        print("="*50)