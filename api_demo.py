import requests
import json
import time


class APIDemo:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"

    def test_basic_chat(self):
        """测试基础对话API"""
        print("💬 测试基础对话API")
        print("-" * 40)

        prompts = [
            "你好，请介绍一下你自己",
            "用Python写一个计算器程序",
            "什么是人工智能？"
        ]

        for i, prompt in enumerate(prompts, 1):
            print(f"\n{i}. 你的问题: {prompt}")

            data = {
                "model": "qwen2:0.5b",
                "prompt": prompt,
                "stream": False
            }

            try:
                start_time = time.time()
                response = requests.post(self.ollama_url, json=data, timeout=30)
                end_time = time.time()

                if response.status_code == 200:
                    result = response.json()
                    print(f"   AI回答: {result['response'][:100]}...")
                    print(f"   响应时间: {end_time - start_time:.2f}秒")
                else:
                    print(f"   ❌ 请求失败: {response.status_code}")

            except Exception as e:
                print(f"   ❌ 错误: {e}")

    def test_with_different_models(self):
        """测试不同模型"""
        print("\n🤖 测试不同模型")
        print("-" * 40)

        models = ["qwen2:0.5b"]  # 你可以添加更多模型，如 "llama2", "codellama:7b"

        for model in models:
            print(f"\n测试模型: {model}")

            data = {
                "model": model,
                "prompt": "请写一首关于春天的短诗",
                "stream": False
            }

            try:
                response = requests.post(self.ollama_url, json=data, timeout=30)
                if response.status_code == 200:
                    result = response.json()
                    print(f"   回答: {result['response'][:80]}...")
                else:
                    print(f"   ❌ {model} 请求失败")
            except Exception as e:
                print(f"   ❌ {model} 错误: {e}")

    def test_streaming(self):
        """测试流式输出（如果支持）"""
        print("\n🌀 测试流式输出")
        print("-" * 40)

        data = {
            "model": "qwen2:0.5b",
            "prompt": "请详细解释机器学习",
            "stream": True  # 流式输出
        }

        try:
            response = requests.post(self.ollama_url, json=data, stream=True, timeout=30)

            if response.status_code == 200:
                print("流式输出: ", end="", flush=True)
                for line in response.iter_lines():
                    if line:
                        try:
                            json_data = json.loads(line)
                            if 'response' in json_data:
                                print(json_data['response'], end="", flush=True)
                        except json.JSONDecodeError:
                            continue
                print()  # 换行
            else:
                print("❌ 流式请求失败")

        except Exception as e:
            print(f"❌ 流式输出错误: {e}")

    def check_ollama_status(self):
        """检查Ollama服务状态"""
        print("🔍 检查Ollama服务状态")
        print("-" * 40)

        try:
            # 检查服务是否运行
            response = requests.get("http://localhost:11434/", timeout=5)
            print("✅ Ollama服务正在运行")

            # 检查可用模型
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            models = response.json().get('models', [])

            if models:
                print("📚 可用模型:")
                for model in models:
                    print(f"   - {model.get('name')}")
            else:
                print("❌ 没有找到模型，请下载: ollama pull qwen2:0.5b")

        except requests.exceptions.ConnectionError:
            print("❌ Ollama服务未运行")
            print("💡 请在CMD中运行: ollama serve")
        except Exception as e:
            print(f"❌ 状态检查失败: {e}")

    def run_demo(self):
        """运行完整的API演示"""
        print("=" * 50)
        print("🔌 API调用演示")
        print("=" * 50)

        # 1. 检查服务状态
        self.check_ollama_status()

        input("\n按回车键继续测试API调用...")

        # 2. 测试各种API功能
        self.test_basic_chat()
        self.test_with_different_models()

        print("\n🎉 API演示完成！")


if __name__ == "__main__":
    demo = APIDemo()
    demo.run_demo()