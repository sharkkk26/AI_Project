# AI_Project
# 🧠 AI心理辅导助手

> 项目 - 基于本地大模型的智能心理辅导系统

## 📋 项目简介
本项目探索本地化AI解决方案，构建了一个集对话、图像识别、情绪分析于一体的心理辅导助手。

## 🎯 已完成功能
- ✅ **智能对话**: 基于Ollama的本地大模型对话
- ✅ **图像分析**: 集成YOLOv8的物体识别与场景描述  
- ✅ **情绪识别**: 基于文本的情绪状态分析
- ✅ **长期记忆**: 用户信息记忆与个性化回应
- ✅ **API集成**: 可扩展的外部服务调用框架

## 🛠️ 技术栈
- **大模型**: Ollama + Qwen2
- **视觉识别**: YOLOv8 + Ultralytics  
- **开发语言**: Python
- **工具链**: Miniconda, OpenWebUI, Requests

## 🚀 快速开始
```bash
# 1. 安装依赖
pip install requests ultralytics pillow

# 2. 启动Ollama服务
ollama serve

# 3. 运行对话程序
python src/chat_with_ai.py
