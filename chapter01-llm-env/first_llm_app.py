 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 第一个大模型应用 - 快速入门示例
================================

这是一个完整的大模型应用示例，展示如何：
1. 从环境变量读取API配置
2. 调用OpenAI兼容的大模型API
3. 处理基础对话和角色扮演
4. 实现错误处理机制
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

def main():
    """主程序入口"""
    print("🚀 LLM-101: 第一个大模型应用")
    print("=" * 50)
    
    # 1. 加载环境变量配置
    load_dotenv()
    
    # 2. 获取API配置
    api_key = os.getenv('OPENAI_API_KEY')
    base_url = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
    model = os.getenv('DEFAULT_MODEL', 'gpt-3.5-turbo')
    
    # 3. 检查API密钥
    if not api_key:
        print("❌ 错误：未找到API密钥！")
        print("请确保：")
        print("1. 已创建.env文件（可从env.template复制）")
        print("2. 在.env文件中设置了OPENAI_API_KEY")
        return
    
    # 4. 初始化OpenAI客户端
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    print(f"✅ 客户端初始化成功")
    print(f"📡 API地址: {base_url}")
    print(f"🤖 使用模型: {model}")
    
    # 5. 构建对话消息
    messages = [
        {
            "role": "system", 
            "content": "你是一个友好的AI助手，用中文回答问题。请简洁明了地回答用户的问题。"
        },
        {
            "role": "user", 
            "content": "你好！请用一句话介绍你自己，并告诉我你能帮助我做什么？"
        }
    ]
    
    try:
        # 6. 调用大模型API
        print("\n🚀 正在调用大模型...")
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=int(os.getenv('MAX_TOKENS', '1000')),
            temperature=float(os.getenv('TEMPERATURE', '0.7'))
        )
        
        # 7. 获取并显示回复
        reply = response.choices[0].message.content
        print(f"\n🤖 AI助手回复:")
        print(f"📝 {reply}")
        
        # 8. 显示使用统计
        usage = response.usage
        print(f"\n📊 使用统计:")
        print(f"🔤 输入tokens: {usage.prompt_tokens}")
        print(f"🔤 输出tokens: {usage.completion_tokens}")
        print(f"🔤 总计tokens: {usage.total_tokens}")
        
        print(f"\n🎉 恭喜！您的第一个大模型应用运行成功！")
        
    except Exception as e:
        print(f"❌ API调用失败: {str(e)}")
        print("\n🔧 故障排除建议：")
        print("1. 检查API密钥是否正确")
        print("2. 确认网络连接是否正常")
        print("3. 检查API服务是否可用")
        print("4. 确认账户余额是否充足")

if __name__ == "__main__":
    main() 