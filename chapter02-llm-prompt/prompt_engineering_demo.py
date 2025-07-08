#!/usr/bin/env python3
"""
🎯 LLM-101 提示词工程示例
展示不同的提示词技巧：零样本、少样本、思维链、自我反思等
"""

import os
import json
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

class PromptEngineeringDemo:
    """提示词工程演示类"""
    
    def __init__(self):
        self.client = self.setup_client()
        self.model = "gpt-3.5-turbo"
    
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
    
    def call_llm(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """调用大模型"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ 调用失败: {str(e)}"
    
    def zero_shot_example(self, text: str) -> str:
        """零样本学习示例"""
        prompt = f"请分析以下文本的情感倾向（积极、消极、中性）：\n\n{text}"
        
        messages = [
            {"role": "system", "content": "你是一个专业的情感分析助手。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.call_llm(messages)
    
    def few_shot_example(self, text: str) -> str:
        """少样本学习示例"""
        prompt = f"""请分析以下文本的情感倾向。

                    示例：
                    文本：今天天气真好，心情很愉快！
                    情感：积极

                    文本：这部电影太无聊了，浪费时间。
                    情感：消极

                    文本：今天是周一，开始新的一周。
                    情感：中性

                    现在请分析：
                    文本：{text}
                    情感："""
        
        messages = [
            {"role": "system", "content": "你是一个专业的情感分析助手。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.call_llm(messages)
    
    def chain_of_thought_example(self, text: str) -> str:
        """思维链(CoT)示例"""
        prompt = f"""请分析以下文本的情感倾向。请按照以下步骤进行分析：

                        1. 首先，识别文本中的关键词和短语
                        2. 然后，分析这些词语的情感色彩
                        3. 接着，考虑整体语境和语调
                        4. 最后，综合判断情感倾向（积极、消极、中性）

                        文本：{text}

                        请逐步分析："""
        
        messages = [
            {"role": "system", "content": "你是一个专业的情感分析助手，善于逐步分析问题。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.call_llm(messages, temperature=0.3)
    
    def self_reflection_example(self, text: str) -> str:
        """自我反思示例"""
        print("🔄 自我反思过程展示：")
        print("=" * 50)
        
        # 第一步：初始分析
        print("📋 第一步：初始分析")
        print("-" * 30)
        initial_prompt = f"请分析以下文本的情感倾向：\n\n{text}"
        
        messages = [
            {"role": "system", "content": "你是一个专业的情感分析助手。"},
            {"role": "user", "content": initial_prompt}
        ]
        
        initial_response = self.call_llm(messages)
        print(f"初始分析结果：\n{initial_response}")
        print("-" * 30)
        
        # 第二步：自我反思和改进
        print("\n🤔 第二步：自我反思和改进")
        print("-" * 30)
        reflection_prompt = f"""你刚才的分析结果是：
                            {initial_response}

                            现在请重新审视这个分析：
                            1. 这个分析是否准确？
                            2. 有没有遗漏的重要信息？
                            3. 是否需要调整结论？

                            请给出你的最终分析结果。

                            原文本：{text}"""
        
        messages = [
            {"role": "system", "content": "你是一个善于自我反思和改进的情感分析助手。"},
            {"role": "user", "content": reflection_prompt}
        ]
        
        final_response = self.call_llm(messages, temperature=0.3)
        print(f"反思改进结果：\n{final_response}")
        print("-" * 30)
        
        # 对比总结
        print("\n📊 对比总结：")
        print("🔹 初始分析：更直接，基于第一印象")
        print("🔹 反思改进：更深入，考虑多个角度，结论更可靠")
        print("=" * 50)
        
        return final_response
    
    def role_playing_example(self, product_description: str) -> str:
        """角色扮演示例"""
        prompt = f"""你现在是一位资深的电商文案专家，拥有10年的营销经验。你的任务是为以下产品写一段吸引人的营销文案。

                    要求：
                    - 突出产品的核心卖点
                    - 使用情感化的语言
                    - 包含行动号召
                    - 文案长度控制在100字以内

                    产品描述：{product_description}

                    请写出营销文案："""
        
        messages = [
            {"role": "system", "content": "你是一位经验丰富的电商文案专家，擅长创作有说服力的营销文案。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.call_llm(messages)
    
    def structured_output_example(self, text: str) -> str:
        """结构化输出示例"""
        prompt = f"""请分析以下文本并以JSON格式返回结果：

                        文本：{text}

                        请返回以下格式的JSON：
                        {{
                            "sentiment": "积极/消极/中性",
                            "confidence": 0.0-1.0,
                            "keywords": ["关键词1", "关键词2", "关键词3"],
                            "summary": "简短总结",
                            "reasoning": "分析理由"
                        }}

                        请确保返回的是有效的JSON格式。"""
        
        messages = [
            {"role": "system", "content": "你是一个专业的情感分析助手，总是返回结构化的JSON结果。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.call_llm(messages, temperature=0.3)
    
    def run_comparison(self, text: str):
        """运行所有示例并比较结果"""
        print("🎯 提示词工程技巧对比分析")
        print("=" * 60)
        print(f"📝 分析文本: {text}")
        print("=" * 60)
        
        techniques = [
            ("零样本学习", self.zero_shot_example),
            ("少样本学习", self.few_shot_example),
            ("思维链(CoT)", self.chain_of_thought_example),
            ("自我反思", self.self_reflection_example),
            ("结构化输出", self.structured_output_example)
        ]
        
        for name, method in techniques:
            print(f"\n🔍 {name}:")
            print("-" * 40)
            result = method(text)
            print(result)
            print("-" * 40)
    
    def marketing_demo(self, product_description: str):
        """营销文案生成示例"""
        print("\n📢 营销文案生成示例")
        print("=" * 60)
        print(f"📝 产品描述: {product_description}")
        print("=" * 60)
        
        result = self.role_playing_example(product_description)
        print(f"\n✨ 生成的营销文案:")
        print(result)

def main():
    """主函数"""
    print("🎯 LLM-101 提示词工程技巧演示")
    print("=" * 60)
    
    try:
        demo = PromptEngineeringDemo()
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return
    
    # 示例文本
    sample_texts = [
        "今天收到了期待已久的包裹，打开一看质量超出预期，非常满意！",
        "这家餐厅的服务态度很差，食物也不新鲜，不会再来了。",
        "会议定于明天上午9点在会议室举行，请准时参加。"
    ]
    
    # 产品描述示例
    product_sample = "智能蓝牙耳机，支持主动降噪，续航时间长达30小时，采用人体工学设计，佩戴舒适。"
    
    print("请选择演示类型：")
    print("1. 情感分析技巧对比")
    print("2. 营销文案生成")
    print("3. 自定义文本分析")
    
    choice = input("\n请输入选择 (1-3): ").strip()
    
    if choice == "1":
        print("\n选择要分析的文本：")
        for i, text in enumerate(sample_texts, 1):
            print(f"{i}. {text}")
        
        text_choice = input("\n请输入选择 (1-3): ").strip()
        try:
            selected_text = sample_texts[int(text_choice) - 1]
            demo.run_comparison(selected_text)
        except (ValueError, IndexError):
            print("❌ 无效选择")
    
    elif choice == "2":
        demo.marketing_demo(product_sample)
    
    elif choice == "3":
        custom_text = input("\n请输入要分析的文本: ").strip()
        if custom_text:
            demo.run_comparison(custom_text)
        else:
            print("❌ 文本不能为空")
    
    else:
        print("❌ 无效选择")
    
    print("\n🎉 演示完成！")
    print("💡 提示：不同的提示词技巧适用于不同的场景，选择合适的技巧可以显著提升效果。")

if __name__ == "__main__":
    main() 