import cv2
from ultralytics import YOLO
import time


def main():
    print("🚀 启动YOLO摄像头检测...")
    print("摄像头索引: 0 (默认摄像头)")
    print("按 'Q' 键退出程序")
    print("按 'S' 键保存截图")
    print("-" * 50)

    # 加载YOLO模型
    try:
        model = YOLO('yolov8n.pt')
        print("✅ YOLO模型加载成功")
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        return

    # 打开摄像头（使用索引0）
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ 无法打开摄像头0")
        return

    # 设置摄像头参数以获得更好的性能
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    print("✅ 摄像头0已成功打开")
    print("🔄 开始实时检测...")

    frame_count = 0
    start_time = time.time()
    detection_count = 0

    while True:
        # 读取帧
        ret, frame = cap.read()

        if not ret:
            print("❌ 无法读取视频帧")
            break

        # 使用YOLO进行目标检测
        results = model(frame)

        # 获取检测结果
        current_detections = 0
        if results[0].boxes is not None:
            current_detections = len(results[0].boxes)
            detection_count += current_detections

        # 在帧上绘制检测结果
        annotated_frame = results[0].plot()

        # 计算并显示FPS
        frame_count += 1
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time if elapsed_time > 0 else 0

        # 在画面上添加信息文字
        info_text = [
            f"FPS: {fps:.1f}",
            f"检测数: {current_detections}",
            f"总检测: {detection_count}",
            "按 Q 退出 | 按 S 截图"
        ]

        for i, text in enumerate(info_text):
            y_position = 30 + i * 25
            cv2.putText(annotated_frame, text, (10, y_position),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # 显示结果
        cv2.imshow('YOLO实时摄像头检测 - 摄像头0', annotated_frame)

        # 按键处理
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q'):
            break
        elif key == ord('s') or key == ord('S'):
            # 保存截图
            timestamp = int(time.time())
            filename = f"yolo_capture_{timestamp}.jpg"
            cv2.imwrite(filename, annotated_frame)
            print(f"📸 截图已保存: {filename}")

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()

    # 显示统计信息
    total_time = time.time() - start_time
    print(f"\n📊 检测统计:")
    print(f"   运行时间: {total_time:.1f}秒")
    print(f"   处理帧数: {frame_count}")
    print(f"   平均FPS: {frame_count / total_time:.1f}")
    print(f"   总检测数: {detection_count}")
    print("🎉 检测完成!")


if __name__ == "__main__":
    main()