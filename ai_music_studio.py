import requests
import json
import os


class AIMusicStudio:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"

    def analyze_emotion_for_music(self, text):
        """分析文本情绪用于音乐创作"""
        prompt = f"""
        分析以下文本的情绪，为音乐创作提供指导：
        "{text}"

        请输出JSON格式：
        {{
            "primary_emotion": "主要情绪",
            "intensity": "强度(1-10)",
            "recommended_tempo": "推荐速度",
            "suggested_instruments": ["建议乐器1", "建议乐器2"],
            "musical_style": "音乐风格"
        }}
        """

        data = {
            "model": "qwen2:0.5b",
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(self.ollama_url, json=data, timeout=60)
            if response.status_code == 200:
                return response.json()['response']
            else:
                return "情绪分析失败"
        except:
            return "AI服务不可用"

    def generate_lyrics(self, theme, style="流行"):
        """生成歌词"""
        prompt = f"""
        以"{theme}"为主题，创作一段{style}风格的歌词。

        要求：
        1. 包含主歌和副歌
        2. 押韵自然
        3. 情感真挚
        4. 适合演唱

        请直接输出歌词内容。
        """

        data = {
            "model": "qwen2:0.5b",
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(self.ollama_url, json=data, timeout=60)
            if response.status_code == 200:
                return response.json()['response']
            else:
                return "歌词生成失败"
        except:
            return "AI服务不可用"

    def create_music_project(self):
        """创建完整音乐项目"""
        print("🎵 AI音乐工作室")
        print("=" * 50)

        project_name = input("请输入项目名称: ").strip()
        theme = input("请输入音乐主题: ").strip()

        print(f"\n正在为'{theme}'创建音乐项目...")

        # 1. 情绪分析
        print("\n1. 🎭 情绪分析...")
        emotion_analysis = self.analyze_emotion_for_music(theme)
        print(emotion_analysis)

        # 2. 生成歌词
        print("\n2. 📝 生成歌词...")
        lyrics = self.generate_lyrics(theme)
        print(lyrics)

        # 3. 音乐创作指导
        print("\n3. 🎼 音乐创作指导...")
        guidance_prompt = f"""
        为主题"{theme}"提供详细的音乐创作指导。

        包括：
        - 和声进行建议
        - 节奏模式
        - 乐器编排
        - 动态变化
        - 制作提示

        用专业但易懂的中文描述。
        """

        data = {
            "model": "qwen2:0.5b",
            "prompt": guidance_prompt,
            "stream": False
        }

        try:
            response = requests.post(self.ollama_url, json=data, timeout=60)
            if response.status_code == 200:
                guidance = response.json()['response']
                print(guidance)
            else:
                print("创作指导生成失败")
        except:
            print("AI服务不可用")

        # 保存项目
        self.save_project(project_name, theme, emotion_analysis, lyrics)

    def save_project(self, project_name, theme, emotion_analysis, lyrics):
        """保存音乐项目"""
        filename = f"{project_name}_music_project.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"音乐项目: {project_name}\n")
            f.write(f"主题: {theme}\n")
            f.write("\n情绪分析:\n")
            f.write(emotion_analysis)
            f.write("\n\n歌词:\n")
            f.write(lyrics)
            f.write("\n\n=== AI音乐工作室生成 ===\n")

        print(f"\n💾 项目已保存: {filename}")

    def run_studio(self):
        """运行音乐工作室"""
        while True:
            print("\n🎵 AI音乐工作室")
            print("1. 创建新音乐项目")
            print("2. 情绪音乐分析")
            print("3. 歌词创作")
            print("4. 退出")

            choice = input("请选择 (1-4): ").strip()

            if choice == "1":
                self.create_music_project()
            elif choice == "2":
                text = input("请输入要分析的文本: ").strip()
                analysis = self.analyze_emotion_for_music(text)
                print(f"\n🎭 情绪分析结果:\n{analysis}")
            elif choice == "3":
                theme = input("请输入歌词主题: ").strip()
                style = input("请输入风格 (流行/摇滚/民谣): ").strip() or "流行"
                lyrics = self.generate_lyrics(theme, style)
                print(f"\n📝 生成的歌词:\n{lyrics}")
            elif choice == "4":
                print("再见！")
                break
            else:
                print("❌ 无效选择")


if __name__ == "__main__":
    studio = AIMusicStudio()
    studio.run_studio()