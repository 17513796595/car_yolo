"""
检测线绘制模块
用于在视频帧上绘制多条检测线
"""

import cv2
from typing import List, Tuple, Dict, Any


class LineDrawer:
    """检测线绘制器"""
    
    def __init__(self):
        self.drawing = False
        self.all_lines = []  # 存储所有检测线
        self.current_line_points = []  # 当前正在绘制的线的点
        self.line_colors = [
            (0, 0, 255), (0, 255, 0), (255, 0, 0), 
            (255, 255, 0), (255, 0, 255), (0, 255, 255)
        ]  # 不同线的颜色
        self.current_line_index = 0

    def mouse_callback(self, event: int, x: int, y: int, flags: int, param: Any) -> None:
        """鼠标回调函数"""
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.current_line_points) < 2:
                self.current_line_points.append((x, y))
                
                # 如果当前线已经有两个点，保存这条线
                if len(self.current_line_points) == 2:
                    color = self.line_colors[self.current_line_index % len(self.line_colors)]
                    self.all_lines.append({
                        'points': self.current_line_points.copy(),
                        'color': color,
                        'name': f'Line {self.current_line_index + 1}'
                    })
                    self.current_line_points = []  # 清空当前线的点
                    self.current_line_index += 1
                    print(f"Line {self.current_line_index} completed! Press 'n' for next line, 'Enter' to finish.")

    def draw_lines_on_frame(self, frame) -> None:
        """在帧上绘制所有检测线"""
        # 绘制所有已完成的线
        for line_data in self.all_lines:
            points = line_data['points']
            color = line_data['color']
            name = line_data['name']
            
            cv2.line(frame, points[0], points[1], color, 3)
            cv2.circle(frame, points[0], 6, color, -1)
            cv2.circle(frame, points[1], 6, color, -1)
            
            # 在线的中点显示线的名称
            mid_x = (points[0][0] + points[1][0]) // 2
            mid_y = (points[0][1] + points[1][1]) // 2
            cv2.putText(frame, name, (mid_x + 10, mid_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # 绘制当前正在设置的线的点
        for pt in self.current_line_points:
            current_color = self.line_colors[self.current_line_index % len(self.line_colors)]
            cv2.circle(frame, pt, 8, current_color, -1)

    def setup_lines(self, first_frame) -> List[Dict]:
        """设置检测线的交互界面"""
        cv2.namedWindow("Set Lines", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("Set Lines", self.mouse_callback)

        print("多线设置说明：")
        print("1. 点击两次来设置一条线")
        print("2. 每条线会自动保存并显示不同颜色")
        print("3. 按 'n' 键继续添加下一条线")
        print("4. 按 'Enter' 键完成所有线的设置")
        print("5. 按 'r' 键重置所有线")

        while True:
            temp_frame = first_frame.copy()
            
            self.draw_lines_on_frame(temp_frame)
            
            # 显示当前状态信息
            info_text = f"Setting Line {self.current_line_index + 1} - Points: {len(self.current_line_points)}/2"
            cv2.putText(temp_frame, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
            cv2.imshow("Set Lines", temp_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 13:  # 回车键完成设置
                break
            elif key == ord('r'):  # r键重置
                self.reset_lines()
                print("All lines reset!")
            elif key == ord('n'):  # n键继续下一条线
                if len(self.current_line_points) > 0:
                    self.current_line_points.clear()
                print(f"Ready to draw Line {self.current_line_index + 1}")

        cv2.destroyWindow("Set Lines")
        
        if len(self.all_lines) == 0:
            print("必须至少设置一条检测线")
            return []
        
        print(f"总共设置了 {len(self.all_lines)} 条检测线")
        return self.all_lines

    def reset_lines(self) -> None:
        """重置所有线"""
        self.all_lines.clear()
        self.current_line_points.clear()
        self.current_line_index = 0

    def get_lines(self) -> List[Dict]:
        """获取所有检测线"""
        return self.all_lines