# OpenAI API辅助函数 - 替换Anthropic API
import openai
import os

# 全局变量存储
API_KEY = ""
MODEL_NAME = "gpt-4o"  # 默认模型

def set_api_key(key):
    """设置OpenAI API密钥"""
    global API_KEY
    API_KEY = key
    openai.api_key = key

def set_model_name(model):
    """设置模型名称"""
    global MODEL_NAME
    MODEL_NAME = model

def get_completion(prompt: str, system_prompt="", max_tokens=2000, temperature=0.0):
    """
    使用OpenAI API获取完成响应，替换原有的Anthropic Claude API
    
    参数:
        prompt (str): 用户提示
        system_prompt (str): 系统提示（可选）
        max_tokens (int): 最大token数，默认2000
        temperature (float): 温度参数，默认0.0表示更确定性
    
    返回:
        str: AI模型的响应文本
    """
    try:
        # 构建消息列表
        messages = []
        
        # 如果有系统提示，添加系统消息
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # 添加用户消息
        messages.append({"role": "user", "content": prompt})
        
        # 调用OpenAI API
        client = openai.OpenAI(api_key=API_KEY)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"API调用错误: {str(e)}"

def get_completion_messages(messages: list, max_tokens=2000, temperature=0.0):
    """
    使用OpenAI API处理多轮对话消息
    
    参数:
        messages (list): 消息列表，每个消息包含role和content
        max_tokens (int): 最大token数，默认2000
        temperature (float): 温度参数，默认0.0
    
    返回:
        str: AI模型的响应文本
    """
    try:
        client = openai.OpenAI(api_key=API_KEY)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"API调用错误: {str(e)}"

# 为了兼容性，创建一个模拟的client对象
class MockAnthropicClient:
    """模拟Anthropic客户端，用于兼容性"""
    
    class Messages:
        def create(self, model, max_tokens, temperature, system="", messages=None):
            # 将Anthropic格式转换为OpenAI格式
            openai_messages = []
            
            if system:
                openai_messages.append({"role": "system", "content": system})
            
            if messages:
                for msg in messages:
                    openai_messages.append(msg)
            
            try:
                client = openai.OpenAI(api_key=API_KEY)
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=openai_messages,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                
                # 模拟Anthropic响应格式
                class MockResponse:
                    def __init__(self, content):
                        self.content = [MockContent(content)]
                
                class MockContent:
                    def __init__(self, text):
                        self.text = text
                
                return MockResponse(response.choices[0].message.content)
                
            except Exception as e:
                # 返回错误信息的模拟响应
                class MockResponse:
                    def __init__(self, content):
                        self.content = [MockContent(content)]
                
                class MockContent:
                    def __init__(self, text):
                        self.text = text
                
                return MockResponse(f"API调用错误: {str(e)}")
    
    def __init__(self, api_key):
        self.messages = self.Messages()

# 创建模拟的anthropic模块
class MockAnthropic:
    @staticmethod
    def Anthropic(api_key):
        return MockAnthropicClient(api_key)

# 设置模型映射
MODEL_MAPPING = {
    "claude-3-haiku-20240307": "gpt-4o-mini",
    "claude-3-sonnet-20240229": "gpt-4o", 
    "claude-3-opus-20240229": "gpt-4o",
    "claude-3-5-sonnet-20241022": "gpt-4o",
    "claude-3-5-haiku-20241022": "gpt-4o-mini"
}

def map_model_name(claude_model):
    """将Claude模型名称映射到OpenAI模型名称"""
    return MODEL_MAPPING.get(claude_model, "gpt-4o") 