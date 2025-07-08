#!/usr/bin/env python3
"""
🧠 思维链(Chain of Thought)提示词技术实现
包含基础CoT、零样本CoT、复杂推理等高级技巧
"""

import os
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

@dataclass
class CoTStep:
    """思维链步骤"""
    step_number: int
    description: str
    reasoning: str
    result: Any

class ChainOfThoughtEngine:
    """思维链推理引擎"""
    
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
    
    def call_llm(self, messages: List[Dict[str, str]], temperature: float = 0.3) -> str:
        """调用大模型"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ 调用失败: {str(e)}"
    
    def basic_cot(self, problem: str, domain: str = "数学") -> str:
        """基础思维链推理"""
        prompt = f"""
请解决以下{domain}问题，并逐步展示你的思考过程：

问题：{problem}

请按照以下格式回答：
步骤1：[分析问题]
步骤2：[确定解决方法]
步骤3：[执行计算/推理]
步骤4：[验证答案]
最终答案：[给出结论]

让我一步步思考：
"""
        
        messages = [
            {"role": "system", "content": f"你是一位{domain}专家，善于逐步分析问题。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.call_llm(messages)
    
    def zero_shot_cot(self, problem: str) -> str:
        """零样本思维链（添加"让我一步步思考"）"""
        prompt = f"""
{problem}

让我一步步思考：
"""
        
        messages = [
            {"role": "system", "content": "你是一个善于逐步分析问题的AI助手。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.call_llm(messages)
    
    def few_shot_cot(self, problem: str, examples: List[Dict[str, str]]) -> str:
        """少样本思维链"""
        prompt = "以下是一些解题示例：\n\n"
        
        for i, example in enumerate(examples, 1):
            prompt += f"示例{i}：\n"
            prompt += f"问题：{example['problem']}\n"
            prompt += f"解答：{example['solution']}\n\n"
        
        prompt += f"现在请解决以下问题：\n问题：{problem}\n解答："
        
        messages = [
            {"role": "system", "content": "你是一个善于学习示例并逐步解决问题的AI助手。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.call_llm(messages)
    
    def multi_step_reasoning(self, problem: str, steps: List[str]) -> str:
        """多步骤推理"""
        prompt = f"""
请解决以下复杂问题，按照指定步骤进行分析：

问题：{problem}

分析步骤：
"""
        for i, step in enumerate(steps, 1):
            prompt += f"{i}. {step}\n"
        
        prompt += "\n请按照上述步骤逐一分析，并在每个步骤后给出你的思考过程："
        
        messages = [
            {"role": "system", "content": "你是一个善于按步骤分析复杂问题的专家。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.call_llm(messages)
    
    def self_ask_cot(self, question: str) -> str:
        """自问自答式思维链"""
        prompt = f"""
请回答以下问题，使用自问自答的方式进行思考：

主问题：{question}

请按照以下格式思考：
1. 为了回答这个问题，我需要知道什么？
2. 让我先问自己：[子问题1]
   回答：[答案1]
3. 接下来我需要问：[子问题2]
   回答：[答案2]
4. [继续自问自答...]
5. 综合以上信息，我的最终答案是：[最终答案]

开始思考：
"""
        
        messages = [
            {"role": "system", "content": "你善于通过自问自答的方式深入思考问题。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.call_llm(messages)
    
    def analogical_reasoning(self, problem: str, analogy: str) -> str:
        """类比推理"""
        prompt = f"""
请使用类比的方法来解决以下问题：

问题：{problem}

类比：{analogy}

请按照以下步骤进行类比推理：
1. 分析类比情况的特点和解决方法
2. 找出类比与当前问题的相似之处
3. 将类比的解决方法应用到当前问题
4. 调整和优化解决方案
5. 得出最终答案

让我通过类比来思考：
"""
        
        messages = [
            {"role": "system", "content": "你善于使用类比方法来解决问题。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.call_llm(messages)

def demo_mathematical_reasoning():
    """数学推理演示"""
    print("🧮 数学推理思维链演示")
    print("=" * 60)
    
    engine = ChainOfThoughtEngine()
    
    # 基础数学问题
    math_problem = "一个矩形的长是宽的3倍，如果周长是32米，求这个矩形的面积。"
    
    print("📝 问题：", math_problem)
    print("\n🔍 基础思维链解答：")
    print("-" * 40)
    result = engine.basic_cot(math_problem, "数学")
    print(result)

def demo_logical_reasoning():
    """逻辑推理演示"""
    print("\n🧠 逻辑推理思维链演示")
    print("=" * 60)
    
    engine = ChainOfThoughtEngine()
    
    # 逻辑推理问题
    logic_problem = """
    有三个盒子，分别标记为A、B、C。
    - 每个盒子里都有一个球，球的颜色是红色、蓝色或绿色之一
    - 已知：A盒子里的球不是红色
    - 已知：B盒子里的球是蓝色或绿色
    - 已知：C盒子里的球不是绿色
    - 已知：三个盒子里的球颜色都不相同
    
    请问每个盒子里是什么颜色的球？
    """
    
    print("📝 问题：", logic_problem.strip())
    print("\n🔍 自问自答式推理：")
    print("-" * 40)
    result = engine.self_ask_cot(logic_problem)
    print(result)

def demo_complex_reasoning():
    """复杂推理演示"""
    print("\n🎯 复杂推理思维链演示")
    print("=" * 60)
    
    engine = ChainOfThoughtEngine()
    
    # 复杂商业问题
    business_problem = """
    一家初创公司正在考虑是否要开发一个新的移动应用。
    
    背景信息：
    - 开发成本：50万元
    - 市场规模：预计100万潜在用户
    - 竞争对手：已有3个类似应用
    - 团队经验：有2年移动开发经验
    - 资金情况：总资金200万元
    - 时间窗口：需要在6个月内上线
    
    请分析是否应该开发这个应用？
    """
    
    analysis_steps = [
        "分析市场机会和竞争环境",
        "评估技术可行性和团队能力",
        "计算财务风险和预期回报",
        "考虑时间成本和机会成本",
        "制定风险缓解策略",
        "给出最终建议和理由"
    ]
    
    print("📝 问题：", business_problem.strip())
    print("\n🔍 多步骤推理分析：")
    print("-" * 40)
    result = engine.multi_step_reasoning(business_problem, analysis_steps)
    print(result)

def demo_few_shot_learning():
    """少样本学习演示"""
    print("\n📚 少样本思维链演示")
    print("=" * 60)
    
    engine = ChainOfThoughtEngine()
    
    # 提供几个例子
    examples = [
        {
            "problem": "如果一个数的平方等于25，这个数是多少？",
            "solution": """
            步骤1：设这个数为x，则x² = 25
            步骤2：对等式两边开平方根，得到x = ±√25
            步骤3：计算√25 = 5
            步骤4：因此x = ±5
            答案：这个数是5或-5
            """
        },
        {
            "problem": "一个三角形的两边长分别是3和4，第三边长是5，这是什么三角形？",
            "solution": """
            步骤1：检查是否满足三角形存在条件：3+4>5, 3+5>4, 4+5>3，都成立
            步骤2：检查是否为直角三角形：3²+4² = 9+16 = 25 = 5²
            步骤3：满足勾股定理，所以是直角三角形
            答案：这是一个直角三角形
            """
        }
    ]
    
    new_problem = "一个正方形的对角线长度是10√2，求这个正方形的面积。"
    
    print("📝 新问题：", new_problem)
    print("\n🔍 基于示例的推理：")
    print("-" * 40)
    result = engine.few_shot_cot(new_problem, examples)
    print(result)

def main():
    """主函数"""
    print("🧠 思维链(Chain of Thought)技术演示")
    print("=" * 80)
    
    try:
        demo_mathematical_reasoning()
        demo_logical_reasoning()
        demo_complex_reasoning()
        demo_few_shot_learning()
        
        print("\n" + "=" * 80)
        print("🎉 演示完成！")
        print("💡 思维链技术通过分解推理步骤，显著提升了模型在复杂问题上的表现。")
        print("🚀 不同的CoT变体适用于不同类型的问题，选择合适的方法是关键。")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")

if __name__ == "__main__":
    main() 