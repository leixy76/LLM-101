#!/usr/bin/env python3
"""
🚀 LLM-101 第一个大模型应用
这是一个简单的聊天机器人，展示如何调用大模型API
"""

import os
import sys
from typing import Optional
from dotenv import load_dotenv

# 尝试导入不同的客户端
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    print("⚠️  OpenAI库未安装，请运行: pip install openai")

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("⚠️  requests库未安装，请运行: pip install requests")

# 加载环境变量
load_dotenv()

class LLMChat:
    """大模型聊天类"""
    
    def __init__(self):
        self.client = None
        self.model = None
        self.setup_client()
    
    def setup_client(self):
        """设置API客户端"""
        # 尝试OpenAI API
        if HAS_OPENAI and os.getenv("OPENAI_API_KEY"):
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = "gpt-3.5-turbo"
            print("✅ 使用OpenAI API")
            return
        
        # 尝试DeepSeek API
        if HAS_OPENAI and os.getenv("DEEPSEEK_API_KEY"):
            self.client = OpenAI(
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url="https://api.deepseek.com"
            )
            self.model = "deepseek-chat"
            print("✅ 使用DeepSeek API")
            return
        
        # 尝试Anthropic API
        if os.getenv("ANTHROPIC_API_KEY"):
            try:
                import anthropic
                self.client = anthropic.Anthropic(
                    api_key=os.getenv("ANTHROPIC_API_KEY")
                )
                self.model = "claude-3-haiku-20240307"
                print("✅ 使用Anthropic API")
                return
            except ImportError:
                print("⚠️  Anthropic库未安装，请运行: pip install anthropic")
        
        print("❌ 未找到可用的API配置，请检查环境变量设置")
        sys.exit(1)
    
    def chat(self, message: str, system_prompt: Optional[str] = None) -> str:
        """与大模型对话"""
        if not system_prompt:
            system_prompt = "你是一个友好、专业的AI助手。请用简洁明了的语言回答用户的问题。"
        
        try:
            if "anthropic" in str(type(self.client)):
                # Anthropic API调用
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=1000,
                    temperature=0.7,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": message}
                    ]
                )
                return response.content[0].text
            else:
                # OpenAI兼容API调用
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
                return response.choices[0].message.content
        
        except Exception as e:
            return f"❌ 调用失败: {str(e)}"

def print_welcome():
    """打印欢迎信息"""
    print("=" * 60)
    print("🚀 欢迎使用 LLM-101 第一个大模型应用！")
    print("=" * 60)
    print("💡 这是一个简单的聊天机器人，展示如何调用大模型API")
    print("📝 您可以输入任何问题，AI会为您回答")
    print("🔧 输入 'quit' 或 'exit' 退出程序")
    print("🔧 输入 'help' 查看更多命令")
    print("=" * 60)

def print_help():
    """打印帮助信息"""
    print("\n📋 可用命令:")
    print("  help    - 显示此帮助信息")
    print("  clear   - 清屏")
    print("  info    - 显示系统信息")
    print("  quit    - 退出程序")
    print("  exit    - 退出程序")
    print("\n💡 提示词示例:")
    print("  - 请解释一下什么是大模型")
    print("  - 帮我写一个Python函数来计算斐波那契数列")
    print("  - 翻译这句话：Hello, how are you?")
    print("  - 总结一下机器学习的基本概念")

def print_info(chat_bot):
    """打印系统信息"""
    print(f"\n🔧 系统信息:")
    print(f"  模型: {chat_bot.model}")
    print(f"  客户端: {type(chat_bot.client).__name__}")
    print(f"  Python版本: {sys.version.split()[0]}")
    
    # 检查环境变量
    api_keys = {
        "OPENAI_API_KEY": "OpenAI",
        "DEEPSEEK_API_KEY": "DeepSeek", 
        "ANTHROPIC_API_KEY": "Anthropic"
    }
    
    print(f"  API配置:")
    for key, name in api_keys.items():
        status = "✅" if os.getenv(key) else "❌"
        print(f"    {name}: {status}")

def main():
    """主函数"""
    print_welcome()
    
    # 初始化聊天机器人
    try:
        chat_bot = LLMChat()
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return
    
    print("\n🤖 AI助手已准备就绪！您可以开始对话了。\n")
    
    while True:
        try:
            user_input = input("👤 您: ").strip()
            
            if not user_input:
                continue
            
            # 处理特殊命令
            if user_input.lower() in ['quit', 'exit']:
                print("👋 再见！感谢使用LLM-101！")
                break
            elif user_input.lower() == 'help':
                print_help()
                continue
            elif user_input.lower() == 'clear':
                os.system('clear' if os.name == 'posix' else 'cls')
                continue
            elif user_input.lower() == 'info':
                print_info(chat_bot)
                continue
            
            # 调用大模型
            print("🤖 AI正在思考中...")
            response = chat_bot.chat(user_input)
            print(f"🤖 AI: {response}\n")
            
        except KeyboardInterrupt:
            print("\n👋 程序被中断，再见！")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    main() 