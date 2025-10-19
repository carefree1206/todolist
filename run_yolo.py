from ultralytics import YOLO
import torch
device = torch.device('cpu')  # 暂时使用 CPU

#1. 加载一个预训练模型
# 你可以选择不同的模型尺寸：n, s, m, l, x （从小到大，精度和速度的权衡）
model = YOLO('yolov8n.pt')

#2. 对图片进行检测
results = model('114514.jpg')

#3. 显示结果
#会生成一张带检测框的新图片，保存在 'runs/detect/predict' 目录下
results[0].show()

#4. 保存结果图片
results[0].save('result.jpg')  # 保存为 result.jpg

print("检测完成！结果已保存。")