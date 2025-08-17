"""
车流量统计系统主程序 - DeepSORT版本
"""

import cv2
from ultralytics import YOLO
# 尝试多种DeepSORT导入方式
DeepSort = None
import_error_msg = ""

try:
    from deep_sort_realtime import DeepSort
    print("✓ DeepSort导入成功 (方式1)")
except ImportError as e1:
    import_error_msg += f"方式1失败: {e1}\n"
    try:
        from deep_sort_realtime.deepsort_tracker import DeepSort
        print("✓ DeepSort导入成功 (方式2)")
    except ImportError as e2:
        import_error_msg += f"方式2失败: {e2}\n"
        try:
            import sys
            sys.path.append('.')
            from deep_sort_realtime import DeepSort
            print("✓ DeepSort导入成功 (方式3)")
        except ImportError as e3:
            import_error_msg += f"方式3失败: {e3}\n"
            print("❌ DeepSORT包导入失败！")
            print("错误详情:")
            print(import_error_msg)
            print("\n解决方案:")
            print("1. pip uninstall deep-sort-realtime")
            print("2. pip install deep-sort-realtime")
            print("3. 或查看 INSTALL_GUIDE.md 获取详细安装指南")
            exit(1)
from src.line_drawer import LineDrawer
from src.vehicle_tracker_deepsort import VehicleTrackerDeepSORT
from src.counter import TrafficCounter
from src.visualizer import Visualizer


class TrafficFlowCounterDeepSORT:
    """车流量统计系统主类 - DeepSORT版本"""
    
    def __init__(self, model_path: str = "yolov8m.pt", video_path: str = None):
        self.yolo_model = YOLO(model_path)
        self.video_path = video_path
        self.line_drawer = LineDrawer()
        self.vehicle_tracker = VehicleTrackerDeepSORT()
        self.visualizer = Visualizer()
        
        # 初始化DeepSORT跟踪器
        self.deepsort = DeepSort(
            max_age=50,
            n_init=3,
            max_iou_distance=0.7,
            max_cosine_distance=0.2,
            nn_budget=100,
            embedder="mobilenet",
            half=True,
            bgr=True,
            embedder_gpu=True
        )
        
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
            
            # YOLO检测
            results = self.yolo_model(frame, classes=[2, 3, 5, 7], conf=0.1)
            
            # 低置信度检测（用于显示）
            all_detections = self.yolo_model(frame, classes=[2, 3, 5, 7], conf=0.2)
            
            detected_count = 0
            
            # 处理检测结果
            if results[0].boxes is not None and len(results[0].boxes) > 0:
                boxes = results[0].boxes.xyxy.cpu().numpy()
                confs = results[0].boxes.conf.cpu().numpy()
                clss = results[0].boxes.cls.cpu().numpy().astype(int)
                
                # 转换为DeepSORT格式
                detection_list = []
                for box, conf, cls_id in zip(boxes, confs, clss):
                    x1, y1, x2, y2 = box
                    w = x2 - x1
                    h = y2 - y1
                    detection_list.append(([x1, y1, w, h], conf, cls_id))
                
                # DeepSORT跟踪
                tracks = self.deepsort.update_tracks(detection_list, frame=frame)
                detected_count = len([t for t in tracks if t.is_confirmed()])
                
                # 处理跟踪结果
                for track in tracks:
                    if not track.is_confirmed():
                        continue
                    
                    track_id = track.track_id
                    ltrb = track.to_ltrb()
                    cls_id = track.get_det_class()
                    
                    x1, y1, x2, y2 = map(int, ltrb)
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
                    box = [x1, y1, x2, y2]
                    self.visualizer.draw_detection_box(frame, box, track_id, vehicle_type)
                    self.vehicle_tracker.draw_tracks(frame, track_id)
            
            # 绘制低置信度检测
            self.visualizer.draw_low_confidence_detections(frame, all_detections)
            
            # 绘制检测线和统计信息
            self.visualizer.draw_detection_lines(frame, lines, counter.line_counts)
            self.visualizer.draw_statistics(frame, lines, counter, detected_count)
            
            # 显示结果
            cv2.namedWindow("Traffic Flow Counter - DeepSORT", cv2.WINDOW_NORMAL)
            cv2.imshow("Traffic Flow Counter - DeepSORT", frame)
            
            if cv2.waitKey(1) & 0xFF == 27:  # ESC键退出
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        # 打印最终统计报告
        counter.print_report()


def main():
    """主函数"""
    print("车流量统计系统 - DeepSORT版本")
    print("="*30)
    
    # 可以在这里修改模型路径和视频路径
    system = TrafficFlowCounterDeepSORT(
        model_path="yolov8m.pt",
        video_path=r"data\3.mp4"
    )
    
    system.run()


if __name__ == "__main__":
    main()