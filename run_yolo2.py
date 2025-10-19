import cv2
from ultralytics import YOLO
import time
import numpy as np


class HighAccuracyYOLOv8Detector:
    def __init__(self, model_path='yolov8x.pt', camera_id=0):
        """
        初始化高精度YOLOv8检测器

        参数:
            model_path: 模型路径，使用yolov8x.pt获得最高精度
            camera_id: 摄像头ID
        """
        # 加载YOLOv8x模型（最大、最精确的版本）
        self.model = YOLO(model_path)
        self.cap = cv2.VideoCapture(camera_id)

        # 设置高分辨率以获得更好的检测效果
        self.set_high_resolution()

        # 性能统计
        self.fps_history = []
        self.detection_times = []

        print(f"加载模型: {model_path}")
        print("使用最高精度配置")

    def set_high_resolution(self, width=1280, height=720):
        """设置高分辨率以提高检测精度"""
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        print(f"设置分辨率: {width}x{height}")

    def optimize_for_accuracy(self):
        """优化模型以获得最高精度"""
        # 这些设置会提高精度但可能降低速度
        self.model.overrides['conf'] = 0.25  # 较低的置信度阈值以检测更多对象
        self.model.overrides['iou'] = 0.45  # 较低的IOU阈值以提高召回率
        self.model.overrides['agnostic_nms'] = False
        self.model.overrides['max_det'] = 100  # 增加最大检测数量

    def calculate_metrics(self, start_time, end_time):
        """计算性能指标"""
        fps = 1.0 / (end_time - start_time)
        self.fps_history.append(fps)
        if len(self.fps_history) > 30:
            self.fps_history.pop(0)

        detection_time = end_time - start_time
        self.detection_times.append(detection_time)
        if len(self.detection_times) > 30:
            self.detection_times.pop(0)

        avg_fps = sum(self.fps_history) / len(self.fps_history)
        avg_detection_time = sum(self.detection_times) / len(self.detection_times) * 1000  # 转换为毫秒

        return avg_fps, avg_detection_time

    def draw_detailed_info(self, frame, results, fps, detection_time):
        """在画面上绘制详细信息"""
        # 基本信息
        cv2.putText(frame, f'FPS: {fps:.1f}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f'Detection Time: {detection_time:.1f}ms', (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # 检测统计
        detections_count = len(results[0].boxes)
        cv2.putText(frame, f'Objects: {detections_count}', (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # 显示检测到的类别和置信度
        if detections_count > 0:
            classes_detected = []
            for box in results[0].boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = self.model.names[class_id]
                classes_detected.append(f"{class_name}: {confidence:.2f}")

            # 显示前几个检测结果
            for i, class_info in enumerate(classes_detected[:5]):
                cv2.putText(frame, class_info, (10, 120 + i * 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        return frame

    def run_high_accuracy_detection(self):
        """运行高精度检测"""
        print("开始高精度实时监测")
        print("按 'q' 退出，按 's' 保存当前帧，按 'p' 暂停/继续")

        self.optimize_for_accuracy()
        paused = False

        while True:
            if not paused:
                start_time = time.time()

                ret, frame = self.cap.read()
                if not ret:
                    print("无法读取摄像头画面")
                    break

                # 使用高精度推理
                results = self.model(
                    frame,
                    conf=0.25,  # 低置信度阈值以提高召回率
                    iou=0.45,  # 低IOU阈值
                    imgsz=640,  # 推理尺寸，保持较大以提高精度
                    verbose=False
                )

                end_time = time.time()

                # 绘制检测结果
                annotated_frame = results[0].plot()

                # 计算性能指标
                avg_fps, avg_detection_time = self.calculate_metrics(start_time, end_time)

                # 绘制详细信息
                annotated_frame = self.draw_detailed_info(
                    annotated_frame, results, avg_fps, avg_detection_time
                )

                # 显示画面
                cv2.imshow('YOLOv8 High Accuracy Detection', annotated_frame)

            # 键盘操作
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                # 保存当前帧
                timestamp = int(time.time())
                filename = f'high_accuracy_detection_{timestamp}.jpg'
                cv2.imwrite(filename, annotated_frame)
                print(f"已保存高精度检测图片: {filename}")
            elif key == ord('p'):
                paused = not paused
                status = "暂停" if paused else "继续"
                print(f"检测{status}")

    def release(self):
        """释放资源"""
        self.cap.release()
        cv2.destroyAllWindows()
        print("释放资源完成")


# 使用示例
if __name__ == "__main__":
    # 注意: yolov8x.pt 模型文件较大，首次使用会自动下载
    # 如果下载缓慢，可以手动下载后放在指定路径

    detector = HighAccuracyYOLOv8Detector(
        model_path='yolov8x.pt',  # 使用最大的模型获得最高精度
        camera_id=0
    )

    try:
        detector.run_high_accuracy_detection()
    except KeyboardInterrupt:
        print("用户中断检测")
    finally:
        detector.release()
import torch
from ultralytics import YOLO


class GPUHighAccuracyYOLOv8Detector(HighAccuracyYOLOv8Detector):
    def __init__(self, model_path='yolov8x.pt', camera_id=0):
        super().__init__(model_path, camera_id)

        # 检查GPU可用性
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"使用设备: {self.device}")

        if self.device == 'cuda':
            print(f"GPU型号: {torch.cuda.get_device_name()}")
            print(f"GPU内存: {torch.cuda.get_device_properties(0).total_memory / 1024 ** 3:.1f} GB")

        # 将模型移动到相应设备
        self.model.to(self.device)

    def optimize_for_accuracy(self):
        """GPU专用的精度优化"""
        self.model.overrides['conf'] = 0.25
        self.model.overrides['iou'] = 0.45
        self.model.overrides['agnostic_nms'] = False
        self.model.overrides['max_det'] = 100
        self.model.overrides['device'] = self.device

        # GPU特有优化
        if self.device == 'cuda':
            # 使用半精度推理提高速度同时保持精度
            self.model.overrides['half'] = True
            print("启用半精度推理")


# GPU版本使用示例
if __name__ == "__main__":
    detector = GPUHighAccuracyYOLOv8Detector('yolov8x.pt', 0)

    try:
        detector.run_high_accuracy_detection()
    finally:
        detector.release()