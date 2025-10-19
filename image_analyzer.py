import requests
import json
import os
import sys
from PIL import Image

try:
    from ultralytics import YOLO

    print("✅ Ultralytics 导入成功")
except ImportError as e:
    print(f"❌ Ultralytics 导入失败: {e}")
    print("请运行: pip install ultralytics")
    input("按回车键退出...")
    sys.exit(1)


class DebugImageAnalyzer:
    def __init__(self):
        print("初始化 DebugImageAnalyzer...")
        self.ollama_url = "http://localhost:11434/api/generate"

        try:
            print("正在加载YOLO模型...")
            self.yolo_model = YOLO('yolov8n.pt')
            print("✅ YOLO模型加载成功")
        except Exception as e:
            print(f"❌ YOLO模型加载失败: {e}")
            self.yolo_model = None

    def check_services(self):
        """检查所有必要的服务"""
        print("\n🔍 检查服务状态...")

        # 检查Ollama
        try:
            response = requests.get("http://localhost:11434/", timeout=5)
            print("✅ Ollama服务正在运行")

            # 检查模型
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            models = response.json().get('models', [])
            if models:
                print("✅ 可用模型:")
                for model in models:
                    print(f"   - {model.get('name')}")
            else:
                print("❌ 没有找到模型")
                return False

        except Exception as e:
            print(f"❌ Ollama服务检查失败: {e}")
            print("💡 请运行: ollama serve")
            return False

        # 检查YOLO
        if self.yolo_model is None:
            print("❌ YOLO模型未加载")
            return False

        print("✅ 所有服务检查通过")
        return True

    def simple_test(self):
        """运行简单测试"""
        print("\n🎯 运行简单测试...")

        # 测试1: 检查桌面图片
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        print(f"桌面路径: {desktop_path}")

        if not os.path.exists(desktop_path):
            print("❌ 桌面路径不存在")
            return False

        # 查找图片文件
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        image_files = []

        for file in os.listdir(desktop_path):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(os.path.join(desktop_path, file))

        print(f"找到 {len(image_files)} 张图片:")
        for img in image_files[:3]:  # 只显示前3个
            print(f"  - {os.path.basename(img)}")

        if not image_files:
            print("❌ 桌面上没有找到图片文件")
            print("💡 请在桌面放置一些.jpg或.png格式的图片")
            return False

        # 测试2: 尝试分析第一张图片
        test_image = image_files[0]
        print(f"\n尝试分析图片: {os.path.basename(test_image)}")

        try:
            # 测试图片打开
            img = Image.open(test_image)
            print("✅ 图片可以正常打开")

            # 测试YOLO识别
            if self.yolo_model:
                results = self.yolo_model(test_image)
                print("✅ YOLO识别成功")

                # 显示识别结果
                detected_objects = []
                for result in results:
                    for box in result.boxes:
                        class_name = result.names[box.cls.item()]
                        confidence = box.conf.item()
                        detected_objects.append(f"{class_name}({confidence:.1%})")

                if detected_objects:
                    print("识别到的物体:")
                    for obj in detected_objects:
                        print(f"  - {obj}")
                else:
                    print("⚠️  未识别到物体")

            # 测试API调用
            print("\n测试API调用...")
            data = {
                "model": "qwen2:0.5b",
                "prompt": "请回复'API测试成功'",
                "stream": False
            }

            response = requests.post(self.ollama_url, json=data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ API调用成功: {result['response']}")
            else:
                print(f"❌ API调用失败: {response.status_code}")

            return True

        except Exception as e:
            print(f"❌ 测试失败: {e}")
            return False

    def run_interactive_simple(self):
        """简化的交互界面"""
        print("\n" + "=" * 50)
        print("🖼️ 图片分析调试版")
        print("=" * 50)

        # 检查服务
        if not self.check_services():
            print("❌ 服务检查失败，无法继续")
            return

        # 运行简单测试
        if not self.simple_test():
            print("❌ 简单测试失败")
            return

        print("\n🎉 所有测试通过！现在可以开始正式分析")

        # 提供简单选项
        while True:
            print("\n选择操作:")
            print("1. 分析单张图片")
            print("2. 退出")

            choice = input("请选择 (1-2): ").strip()

            if choice == "1":
                image_path = input("请输入图片完整路径: ").strip()

                if not os.path.exists(image_path):
                    print("❌ 文件不存在")
                    continue

                try:
                    # 分析图片
                    img = Image.open(image_path)
                    results = self.yolo_model(image_path)

                    # 显示结果
                    detected_objects = []
                    for result in results:
                        for box in result.boxes:
                            class_name = result.names[box.cls.item()]
                            confidence = box.conf.item()
                            detected_objects.append(f"{class_name}({confidence:.1%})")

                    print("\n🎯 识别结果:")
                    if detected_objects:
                        for obj in detected_objects:
                            print(f"  - {obj}")
                    else:
                        print("  - 未识别到物体")

                    # 生成AI描述
                    if detected_objects:
                        object_list = ", ".join([obj.split('(')[0] for obj in detected_objects])
                        prompt = f"请描述包含这些物体的场景: {object_list}"

                        data = {
                            "model": "qwen2:0.5b",
                            "prompt": prompt,
                            "stream": False
                        }

                        response = requests.post(self.ollama_url, json=data, timeout=30)
                        if response.status_code == 200:
                            description = response.json()['response']
                            print(f"\n🤖 AI描述:\n{description}")

                    # 保存结果图片
                    output_path = f"result_{os.path.basename(image_path)}"
                    results[0].save(output_path)
                    print(f"\n💾 结果保存: {output_path}")

                except Exception as e:
                    print(f"❌ 分析失败: {e}")

            elif choice == "2":
                print("👋 再见！")
                break

            else:
                print("❌ 无效选择")


def main():
    """主函数"""
    print("🚀 启动图片分析调试器...")

    try:
        analyzer = DebugImageAnalyzer()
        analyzer.run_interactive_simple()
    except Exception as e:
        print(f"💥 程序崩溃: {e}")
        import traceback
        traceback.print_exc()

    input("\n按回车键退出...")


if __name__ == "__main__":
    main()