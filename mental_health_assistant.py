import requests
import json
import os
from datetime import datetime


# 1. 长期记忆系统
class LongTermMemory:
    def __init__(self, user_id="default_user"):
        self.user_id = user_id
        self.memory_file = f"memory_{user_id}.json"
        self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                self.memory = json.load(f)
        else:
            self.memory = {
                "basic_info": {"name": "", "age": "", "interests": []},
                "conversation_history": [],
                "emotional_patterns": {},
                "preferences": {}
            }

    def save_memory(self):
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)

    def update_basic_info(self, name, age=None, interests=None):
        self.memory["basic_info"] = {
            "name": name,
            "age": age,
            "interests": interests or [],
            "last_updated": datetime.now().isoformat()
        }
        self.save_memory()

    def add_conversation(self, user_input, ai_response, emotion=None):
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "ai_response": ai_response,
            "emotion": emotion
        }
        self.memory["conversation_history"].append(conversation)
        if len(self.memory["conversation_history"]) > 50:
            self.memory["conversation_history"] = self.memory["conversation_history"][-50:]
        self.save_memory()

    def get_user_context(self):
        basic = self.memory["basic_info"]
        recent_chats = self.memory["conversation_history"][-3:]

        context = f"用户姓名: {basic.get('name', '未知')}\n"
        if basic.get('age'):
            context += f"年龄: {basic['age']}\n"
        if basic.get('interests'):
            context += f"兴趣: {', '.join(basic['interests'])}\n"

        context += "\n最近对话:\n"
        for chat in recent_chats:
            context += f"用户: {chat['user_input']}\n"
            context += f"助理: {chat['ai_response']}\n"

        return context


# 2. 情绪识别
class EmotionAnalyzer:
    def __init__(self, ollama_url):
        self.ollama_url = ollama_url

    def analyze_emotion(self, text):
        prompt = f"""
        分析这句话的情绪："{text}"
        从[快乐, 悲伤, 愤怒, 焦虑, 压力, 平静, 兴奋, 孤独, 困惑, 中性]中选择。
        只回复情绪单词。
        """

        data = {
            "model": "qwen2:0.5b",
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(self.ollama_url, json=data, timeout=30)
            if response.status_code == 200:
                emotion = response.json()['response'].strip()
                return emotion if emotion in ["快乐", "悲伤", "愤怒", "焦虑", "压力", "平静", "兴奋", "孤独", "困惑",
                                              "中性"] else "中性"
            return "中性"
        except:
            return "中性"


# 3. 心理辅导智能体
class MentalHealthAssistant:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.memory = LongTermMemory()
        self.emotion_analyzer = EmotionAnalyzer(self.ollama_url)

    def start_session(self):
        """开始会话"""
        if not self.memory.memory["basic_info"].get("name"):
            return """👋 你好！我是你的心理辅导助手小暖。

为了更好地帮助你，请问你希望我怎么称呼你？"""

        user_name = self.memory.memory["basic_info"].get("name", "朋友")
        return f"你好{user_name}！很高兴再次见到你。今天感觉怎么样？"

    def process_user_input(self, user_input):
        """处理用户输入"""
        # 如果是第一次对话，收集名字
        if not self.memory.memory["basic_info"].get("name"):
            if "我叫" in user_input or "名字是" in user_input:
                name = self.extract_name(user_input)
                self.memory.update_basic_info(name=name)
                return f"很高兴认识你，{name}！我会记住你的名字。今天有什么想聊的吗？", "快乐"
            else:
                return "请问你希望我怎么称呼你呢？", "中性"

        # 分析情绪
        emotion = self.emotion_analyzer.analyze_emotion(user_input)

        # 生成回应
        context = self.memory.get_user_context()
        prompt = f"""
        {context}

        用户当前情绪: {emotion}
        用户说: "{user_input}"

        你是一个温暖的心理辅导老师小暖。请：
        1. 表达理解和共情
        2. 根据情绪提供适当支持
        3. 保持专业和温暖
        4. 用{self.memory.memory["basic_info"].get("name", "朋友")}称呼用户

        请用自然的中文回复。
        """

        response = self.generate_response(prompt)

        # 保存对话
        self.memory.add_conversation(user_input, response, emotion)

        return response, emotion

    def extract_name(self, text):
        """从文本中提取名字"""
        if "我叫" in text:
            return text.split("我叫")[1].split(" ")[0].strip()
        elif "名字是" in text:
            return text.split("名字是")[1].split(" ")[0].strip()
        else:
            return tex