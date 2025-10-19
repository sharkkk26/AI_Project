import requests
import json


def simple_chat():
    """使用正确的模型名称与AI对话"""

    # 正确的API地址
    url = "http://localhost:11434/api/generate"

    user_message = input("你想问什么：")

    # 使用你已安装的模型名称
    data = {
        "model": "qwen2:0.5b",  # 改成你实际安装的模型
        "prompt": user_message,
        "stream": False
    }

    try:
        print("正在发送请求...")
        response = requests.post(url, json=data, timeout=60)

        print(f"响应状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("\n🤖 AI回答：")
            print(result['response'])
        else:
            print(f"请求失败：{response.status_code}")
            print(f"错误信息：{response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ 连接被拒绝，请确保Ollama正在运行")
        print("提示：在CMD中运行 'ollama serve'")
    except Exception as e:
        print(f"错误：{e}")


if __name__ == "__main__":
    simple_chat()