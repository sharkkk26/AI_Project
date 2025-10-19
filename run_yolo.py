from ultralytics import YOLO


def simple_yolo_test():
    print("🚀 启动YOLO图像识别...")

    # 加载模型（首次运行会自动下载）
    model = YOLO('yolov8n.pt')
    print("✅ 模型加载完成")

    # 方法1：使用网络测试图片
    print("方法1: 测试网络图片...")
    results = model('https://ultralytics.com/images/bus.jpg')

    # 显示结果
    print("🎯 识别结果:")
    for result in results:
        for box in result.boxes:
            class_name = result.names[box.cls.item()]
            confidence = box.conf.item()
            print(f"  - {class_name}: {confidence:.1%}")

    # 保存带标注的结果图片
    results[0].save('result_bus.jpg')
    print("📁 结果图片已保存: result_bus.jpg")


if __name__ == "__main__":
    simple_yolo_test()