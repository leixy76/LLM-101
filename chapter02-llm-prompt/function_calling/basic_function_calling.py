#!/usr/bin/env python3
"""
🔧 基础函数调用(Function Calling)实现
展示OpenAI Function Calling的核心功能和使用方法
"""

import os
import json
import math
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

@dataclass
class FunctionDefinition:
    """函数定义"""
    name: str
    description: str
    parameters: Dict[str, Any]

class FunctionCallingEngine:
    """函数调用引擎"""
    
    def __init__(self):
        self.client = self.setup_client()
        self.model = "gpt-3.5-turbo"
        self.available_functions = {}
        self.register_built_in_functions()
    
    def setup_client(self):
        """设置API客户端"""
        if os.getenv("OPENAI_API_KEY"):
            return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif os.getenv("DEEPSEEK_API_KEY"):
            return OpenAI(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com"
            )
        else:
            raise ValueError("请设置OPENAI_API_KEY或DEEPSEEK_API_KEY环境变量")
    
    def register_built_in_functions(self):
        """注册内置函数"""
        # 数学计算函数
        self.register_function(
            "calculate",
            "执行基本数学计算",
            {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "要计算的数学表达式，如 '2 + 3 * 4'"
                    }
                },
                "required": ["expression"]
            },
            self.calculate
        )
        
        # 获取当前时间
        self.register_function(
            "get_current_time",
            "获取当前日期和时间",
            {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "时区，如 'Asia/Shanghai'",
                        "default": "UTC"
                    }
                },
                "required": []
            },
            self.get_current_time
        )
        
        # 文本分析
        self.register_function(
            "analyze_text",
            "分析文本的基本信息",
            {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "要分析的文本"
                    },
                    "analysis_type": {
                        "type": "string",
                        "enum": ["length", "words", "sentiment", "summary"],
                        "description": "分析类型：length(长度)、words(词数)、sentiment(情感)、summary(摘要)"
                    }
                },
                "required": ["text", "analysis_type"]
            },
            self.analyze_text
        )
    
    def register_function(self, name: str, description: str, parameters: Dict[str, Any], 
                         function_impl: callable):
        """注册函数"""
        self.available_functions[name] = {
            "definition": FunctionDefinition(name, description, parameters),
            "implementation": function_impl
        }
    
    def get_function_definitions(self) -> List[Dict[str, Any]]:
        """获取所有函数定义"""
        definitions = []
        for func_info in self.available_functions.values():
            func_def = func_info["definition"]
            definitions.append({
                "type": "function",
                "function": {
                    "name": func_def.name,
                    "description": func_def.description,
                    "parameters": func_def.parameters
                }
            })
        return definitions
    
    def execute_function(self, function_name: str, arguments: Dict[str, Any]) -> str:
        """执行函数"""
        if function_name not in self.available_functions:
            return f"❌ 未知函数: {function_name}"
        
        try:
            function_impl = self.available_functions[function_name]["implementation"]
            result = function_impl(**arguments)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            return f"❌ 函数执行失败: {str(e)}"
    
    def chat_with_functions(self, user_message: str, max_iterations: int = 5) -> str:
        """支持函数调用的对话"""
        messages = [
            {"role": "system", "content": "你是一个智能助手，可以调用函数来帮助用户解决问题。"},
            {"role": "user", "content": user_message}
        ]
        
        for iteration in range(max_iterations):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=self.get_function_definitions(),
                    tool_choice="auto",
                    temperature=0.3
                )
                
                response_message = response.choices[0].message
                messages.append({
                    "role": "assistant",
                    "content": response_message.content,
                    "tool_calls": response_message.tool_calls
                })
                
                # 检查是否有函数调用
                if response_message.tool_calls:
                    for tool_call in response_message.tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        
                        print(f"🔧 调用函数: {function_name}")
                        print(f"📥 参数: {function_args}")
                        
                        # 执行函数
                        function_result = self.execute_function(function_name, function_args)
                        
                        print(f"📤 结果: {function_result}")
                        
                        # 将函数结果添加到消息列表
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": function_result
                        })
                else:
                    # 没有函数调用，返回最终回答
                    return response_message.content
                
            except Exception as e:
                return f"❌ 对话失败: {str(e)}"
        
        return "❌ 达到最大迭代次数，对话终止"
    
    # 内置函数实现
    def calculate(self, expression: str) -> Dict[str, Any]:
        """计算数学表达式"""
        try:
            # 安全的数学表达式评估
            allowed_names = {
                k: v for k, v in math.__dict__.items() if not k.startswith("__")
            }
            allowed_names.update({"abs": abs, "round": round})
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            
            return {
                "expression": expression,
                "result": result,
                "type": type(result).__name__,
                "success": True
            }
        except Exception as e:
            return {
                "expression": expression,
                "error": str(e),
                "success": False
            }
    
    def get_current_time(self, timezone: str = "UTC") -> Dict[str, Any]:
        """获取当前时间"""
        try:
            from datetime import datetime
            import pytz
            
            if timezone == "UTC":
                current_time = datetime.utcnow()
                tz_name = "UTC"
            else:
                tz = pytz.timezone(timezone)
                current_time = datetime.now(tz)
                tz_name = timezone
            
            return {
                "datetime": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "timestamp": current_time.timestamp(),
                "timezone": tz_name,
                "weekday": current_time.strftime("%A"),
                "success": True
            }
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }
    
    def analyze_text(self, text: str, analysis_type: str) -> Dict[str, Any]:
        """分析文本"""
        try:
            result = {"text_preview": text[:50] + "..." if len(text) > 50 else text}
            
            if analysis_type == "length":
                result.update({
                    "character_count": len(text),
                    "character_count_no_spaces": len(text.replace(" ", "")),
                    "byte_size": len(text.encode('utf-8'))
                })
            
            elif analysis_type == "words":
                words = text.split()
                result.update({
                    "word_count": len(words),
                    "unique_words": len(set(words)),
                    "average_word_length": sum(len(word) for word in words) / len(words) if words else 0
                })
            
            elif analysis_type == "sentiment":
                # 简单的情感分析（实际应用中可以使用更复杂的模型）
                positive_words = ["好", "很好", "优秀", "棒", "喜欢", "满意", "开心", "高兴"]
                negative_words = ["差", "不好", "糟糕", "讨厌", "不满", "生气", "愤怒", "难过"]
                
                text_lower = text.lower()
                positive_count = sum(1 for word in positive_words if word in text_lower)
                negative_count = sum(1 for word in negative_words if word in text_lower)
                
                if positive_count > negative_count:
                    sentiment = "positive"
                elif negative_count > positive_count:
                    sentiment = "negative"
                else:
                    sentiment = "neutral"
                
                result.update({
                    "sentiment": sentiment,
                    "positive_indicators": positive_count,
                    "negative_indicators": negative_count
                })
            
            elif analysis_type == "summary":
                sentences = text.split('。')
                result.update({
                    "sentence_count": len([s for s in sentences if s.strip()]),
                    "longest_sentence": max(sentences, key=len).strip() if sentences else "",
                    "text_structure": "formal" if "。" in text else "informal"
                })
            
            result["success"] = True
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }

def demo_basic_calculation():
    """基础计算演示"""
    print("🧮 基础计算功能演示")
    print("=" * 60)
    
    engine = FunctionCallingEngine()
    
    questions = [
        "请计算 15 * 24 + 30 / 6 的结果",
        "sin(π/4) 的值是多少？",
        "如果一个圆的半径是5，它的面积和周长分别是多少？"
    ]
    
    for question in questions:
        print(f"\n📝 问题: {question}")
        print("🤖 回答:")
        result = engine.chat_with_functions(question)
        print(result)
        print("-" * 40)

def demo_time_functions():
    """时间功能演示"""
    print("\n🕐 时间功能演示")
    print("=" * 60)
    
    engine = FunctionCallingEngine()
    
    questions = [
        "现在几点了？",
        "北京时间现在是几点？",
        "今天是星期几？"
    ]
    
    for question in questions:
        print(f"\n📝 问题: {question}")
        print("🤖 回答:")
        result = engine.chat_with_functions(question)
        print(result)
        print("-" * 40)

def demo_text_analysis():
    """文本分析演示"""
    print("\n📊 文本分析功能演示")
    print("=" * 60)
    
    engine = FunctionCallingEngine()
    
    questions = [
        "请分析这段话的字数：'人工智能是一门极富挑战性的科学，从事这项工作的人必须懂得计算机知识，心理学和哲学。'",
        "帮我分析一下这句话的情感：'今天天气真好，心情也很愉快！'",
        "这段文本有多少个句子：'今天是个好日子。天气晴朗。我很开心。'"
    ]
    
    for question in questions:
        print(f"\n📝 问题: {question}")
        print("🤖 回答:")
        result = engine.chat_with_functions(question)
        print(result)
        print("-" * 40)

def demo_complex_workflow():
    """复杂工作流演示"""
    print("\n🔄 复杂工作流演示")
    print("=" * 60)
    
    engine = FunctionCallingEngine()
    
    complex_question = """
    我有一段文本：'机器学习是人工智能的一个重要分支，它让计算机能够自动学习和改进。深度学习是机器学习的一个子领域。'
    
    请帮我：
    1. 分析这段文本有多少个字
    2. 分析情感倾向
    3. 如果每个字需要0.5秒来阅读，那么读完这段话需要多长时间？
    """
    
    print(f"📝 复杂问题: {complex_question}")
    print("\n🤖 AI助手分析过程:")
    result = engine.chat_with_functions(complex_question)
    print(f"\n✨ 最终回答:\n{result}")

def demo_interactive_session():
    """交互式对话演示"""
    print("\n💬 交互式对话演示")
    print("=" * 60)
    print("🤖 你好！我是支持函数调用的AI助手。")
    print("📝 我可以帮你进行数学计算、文本分析、查看时间等。")
    print("💡 输入 'quit' 或 'exit' 退出对话")
    print("-" * 60)
    
    engine = FunctionCallingEngine()
    
    while True:
        user_input = input("\n👤 你: ").strip()
        
        if user_input.lower() in ['quit', 'exit', '退出', '再见']:
            print("🤖 再见！感谢使用函数调用演示！")
            break
        
        if not user_input:
            continue
        
        print("🤖 AI助手:")
        try:
            response = engine.chat_with_functions(user_input)
            print(response)
        except KeyboardInterrupt:
            print("\n🤖 对话被中断")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")

def main():
    """主函数"""
    print("🔧 函数调用(Function Calling)技术演示")
    print("=" * 80)
    print("🎯 本演示展示如何使用OpenAI的函数调用功能")
    print("💡 AI助手可以调用外部函数来完成复杂任务")
    print("=" * 80)
    
    try:
        demo_basic_calculation()
        demo_time_functions()
        demo_text_analysis()
        demo_complex_workflow()
        
        print("\n" + "=" * 80)
        print("🎉 基础演示完成！")
        print("🚀 接下来是交互式对话环节...")
        
        demo_interactive_session()
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")

if __name__ == "__main__":
    main() 