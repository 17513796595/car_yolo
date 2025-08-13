"""
车流量统计系统主程序
"""

import cv2
from ultralytics import YOLO
from src.line_drawer import LineDrawer
from src.vehicle_tracker import VehicleTracker
from src.counter import TrafficCounter
from src.visualizer import Visualizer


class TrafficFlowCounter:
    """车流量统计系统主类"""
    
    def __init__(self, model_path: str = "yolov8m.pt", video_path: str = None):
        self.model = YOLO(model_path)
        self.video_path = video_path
        self.line_drawer = LineDrawer()
        self.vehicle_tracker = VehicleTracker()
        self.visualizer = Visualizer()
        
    def run(self):
        """运行车流量统计"""
        # 打开视频
        cap = cv2.VideoCapture(self.video_path or "3.mp4")
        
        # 获取第一帧设置检测线
        ret, first_frame = cap.read()
        if not ret:
            print("无法读取视频")
            return
        
        # 设置检测线
        lines = self.line_drawer.setup_lines(first_frame)
        if not lines:
            print("必须至少设置一条检测线")
            return
        
        # 初始化计数器
        counter = TrafficCounter(lines)
        
        # 重置视频到开头
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        print("开始车流量统计... 按 ESC 键退出")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # YOLO检测和追踪
            results = self.model.track(
                frame, 
                persist=True, 
                tracker="bytetrack.yaml", 
                classes=[2, 3, 5, 7], 
                conf=0.1
            )
            
            # 低置信度检测（用于显示）
            all_detections = self.model(frame, classes=[2, 3, 5, 7], conf=0.2)
            
            detected_count = 0
            
            # 处理检测结果
            if results[0].boxes.id is not None:
                ids = results[0].boxes.id.cpu().numpy().astype(int)
                boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
                clss = results[0].boxes.cls.cpu().numpy().astype(int)
                detected_count = len(ids)
                
                for box, track_id, cls_id in zip(boxes, ids, clss):
                    x1, y1, x2, y2 = box
                    cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
                    current_pos = (cx, cy)
                    
                    # 获取前一个位置
                    prev_pos = self.vehicle_tracker.get_previous_position(track_id)
                    
                    # 更新轨迹
                    self.vehicle_tracker.update_tracks(track_id, current_pos)
                    
                    # 检查是否穿越检测线
                    counter.check_crossing(track_id, current_pos, prev_pos, cls_id, self.vehicle_tracker)
                    
                    # 绘制检测框和轨迹
                    vehicle_type = self.vehicle_tracker.get_vehicle_type(cls_id)
                    self.visualizer.draw_detection_box(frame, box, track_id, vehicle_type)
                    self.vehicle_tracker.draw_tracks(frame, track_id)
            
            # 绘制低置信度检测
            self.visualizer.draw_low_confidence_detections(frame, all_detections)
            
            # 绘制检测线和统计信息
            self.visualizer.draw_detection_lines(frame, lines, counter.line_counts)
            self.visualizer.draw_statistics(frame, lines, counter, detected_count)
            
            # 显示结果
            cv2.namedWindow("Traffic Flow Counter", cv2.WINDOW_NORMAL)
            cv2.imshow("Traffic Flow Counter", frame)
            
            if cv2.waitKey(1) & 0xFF == 27:  # ESC键退出
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        # 打印最终统计报告
        counter.print_report()


def main():
    """主函数"""
    print("车流量统计系统")
    print("="*30)
    
    # 可以在这里修改模型路径和视频路径
    system = TrafficFlowCounter(
        model_path="yolov8m.pt",
        video_path=r"data\3.mp4"
    )
    
    system.run()


if __name__ == "__main__":
    main()
