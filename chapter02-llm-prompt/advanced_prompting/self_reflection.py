#!/usr/bin/env python3
"""
🔄 自我反思(Self-Reflection)提示词技术实现
通过让模型审视和改进自己的回答来提升质量
"""

import os
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

@dataclass
class ReflectionResult:
    """反思结果"""
    original_answer: str
    reflection_analysis: str
    improved_answer: str
    confidence_score: float
    iteration: int

class SelfReflectionEngine:
    """自我反思引擎"""
    
    def __init__(self):
        self.client = self.setup_client()
        self.model = "gpt-3.5-turbo"
        self.max_iterations = 3
    
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
    
    def initial_answer(self, question: str, domain: str = "通用") -> str:
        """生成初始答案"""
        prompt = f"请回答以下问题：\n\n{question}"
        
        messages = [
            {"role": "system", "content": f"你是一位{domain}专家，请仔细回答用户的问题。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.call_llm(messages)
    
    def reflect_on_answer(self, question: str, answer: str) -> str:
        """对答案进行反思分析"""
        reflection_prompt = f"""
请审视以下问答对，并进行深入分析：

原问题：{question}

我的回答：{answer}

请从以下几个维度进行反思：
1. 【准确性检查】回答是否准确完整？有没有事实性错误？
2. 【逻辑性分析】推理过程是否清晰合理？有没有逻辑漏洞？
3. 【完整性评估】是否遗漏了重要信息或关键点？
4. 【清晰度评价】表达是否清晰易懂？有没有歧义？
5. 【相关性判断】回答是否切题？有没有偏离主题？

请详细分析并指出需要改进的地方：
"""
        
        messages = [
            {"role": "system", "content": "你是一位善于批判性思考的评估专家，能够客观地分析和评价回答质量。"},
            {"role": "user", "content": reflection_prompt}
        ]
        
        return self.call_llm(messages)
    
    def improve_answer(self, question: str, original_answer: str, reflection: str) -> str:
        """基于反思改进答案"""
        improvement_prompt = f"""
基于以下反思分析，请改进原始回答：

原问题：{question}

原始回答：{original_answer}

反思分析：{reflection}

请提供一个改进后的回答，确保：
1. 修正所有指出的错误
2. 补充遗漏的重要信息
3. 优化表达的清晰度
4. 保持逻辑的一致性

改进后的回答：
"""
        
        messages = [
            {"role": "system", "content": "你是一位善于改进和完善回答的专家，能够根据反思意见显著提升回答质量。"},
            {"role": "user", "content": improvement_prompt}
        ]
        
        return self.call_llm(messages)
    
    def evaluate_confidence(self, question: str, answer: str) -> float:
        """评估答案的置信度"""
        confidence_prompt = f"""
请评估以下回答的置信度：

问题：{question}
回答：{answer}

请从以下维度评分（1-10分）：
1. 事实准确性（是否基于可靠信息）
2. 逻辑合理性（推理过程是否严密）
3. 完整性（是否全面回答了问题）
4. 清晰度（表达是否明确易懂）

请给出每个维度的分数，并计算总体置信度（0-1之间的小数）：
"""
        
        messages = [
            {"role": "system", "content": "你是一位专业的答案质量评估师，能够客观准确地评估回答质量。"},
            {"role": "user", "content": confidence_prompt}
        ]
        
        result = self.call_llm(messages)
        
        # 简单解析置信度（实际应用中可能需要更复杂的解析）
        try:
            import re
            confidence_match = re.search(r'置信度[：:]\s*([0-1]\.\d+)', result)
            if confidence_match:
                return float(confidence_match.group(1))
            else:
                return 0.7  # 默认置信度
        except:
            return 0.7
    
    def multi_round_reflection(self, question: str, domain: str = "通用") -> List[ReflectionResult]:
        """多轮反思优化"""
        results = []
        current_answer = self.initial_answer(question, domain)
        
        for iteration in range(self.max_iterations):
            print(f"\n🔄 第{iteration + 1}轮反思...")
            
            # 反思当前答案
            reflection = self.reflect_on_answer(question, current_answer)
            
            # 改进答案
            improved_answer = self.improve_answer(question, current_answer, reflection)
            
            # 评估置信度
            confidence = self.evaluate_confidence(question, improved_answer)
            
            # 保存结果
            result = ReflectionResult(
                original_answer=current_answer,
                reflection_analysis=reflection,
                improved_answer=improved_answer,
                confidence_score=confidence,
                iteration=iteration + 1
            )
            results.append(result)
            
            # 如果置信度足够高，提前结束
            if confidence > 0.9:
                print(f"✅ 置信度达到{confidence:.2f}，反思完成")
                break
            
            # 准备下一轮
            current_answer = improved_answer
        
        return results
    
    def comparative_reflection(self, question: str, answers: List[str]) -> str:
        """比较多个答案并反思"""
        comparison_prompt = f"""
请比较以下多个回答，并进行深入分析：

问题：{question}

回答选项：
"""
        for i, answer in enumerate(answers, 1):
            comparison_prompt += f"\n选项{i}：{answer}\n"
        
        comparison_prompt += """
请分析：
1. 每个回答的优缺点
2. 哪个回答最准确完整
3. 如何结合各个回答的优点
4. 提供一个最佳的综合答案

分析结果：
"""
        
        messages = [
            {"role": "system", "content": "你是一位善于比较分析的专家，能够综合多个观点提供最佳答案。"},
            {"role": "user", "content": comparison_prompt}
        ]
        
        return self.call_llm(messages)
    
    def error_detection_reflection(self, question: str, answer: str) -> str:
        """专注于错误检测的反思"""
        error_prompt = f"""
请仔细检查以下回答中可能存在的错误：

问题：{question}
回答：{answer}

请重点检查：
1. 【事实性错误】：数据、定义、概念是否正确
2. 【逻辑错误】：推理过程是否有矛盾或跳跃
3. 【计算错误】：如有计算，结果是否正确
4. 【理解错误】：是否误解了问题的意图
5. 【表达错误】：是否有歧义或不清楚的地方

如果发现错误，请指出具体位置并提供正确的版本：
"""
        
        messages = [
            {"role": "system", "content": "你是一位严格的错误检测专家，善于发现各种类型的错误。"},
            {"role": "user", "content": error_prompt}
        ]
        
        return self.call_llm(messages)

def demo_basic_reflection():
    """基础反思演示"""
    print("🔄 基础自我反思演示")
    print("=" * 60)
    
    engine = SelfReflectionEngine()
    
    question = "请解释什么是机器学习，它与人工智能和深度学习的关系是什么？"
    
    print(f"📝 问题：{question}")
    
    # 多轮反思
    results = engine.multi_round_reflection(question, "人工智能")
    
    for i, result in enumerate(results):
        print(f"\n🔄 第{result.iteration}轮反思：")
        print(f"置信度：{result.confidence_score:.2f}")
        print(f"改进后答案：\n{result.improved_answer}")

def demo_error_detection():
    """错误检测演示"""
    print("\n🔍 错误检测反思演示")
    print("=" * 60)
    
    engine = SelfReflectionEngine()
    
    # 包含错误的回答
    question = "地球到太阳的平均距离是多少？"
    wrong_answer = "地球到太阳的平均距离大约是93万公里，这个距离被称为一个天文单位（AU）。"
    
    print(f"📝 问题：{question}")
    print(f"🤔 待检查的回答：{wrong_answer}")
    
    error_analysis = engine.error_detection_reflection(question, wrong_answer)
    print(f"\n🔍 错误检测结果：\n{error_analysis}")

def demo_comparative_reflection():
    """比较反思演示"""
    print("\n⚖️ 比较反思演示")
    print("=" * 60)
    
    engine = SelfReflectionEngine()
    
    question = "如何有效地学习编程？"
    
    answers = [
        "学习编程最重要的是多练习，每天至少写代码2小时，从简单的程序开始。",
        "应该先学好理论基础，理解算法和数据结构，然后再开始实际编程。",
        "最好的方法是找个项目来做，在实践中学习，遇到问题就查资料解决。"
    ]
    
    print(f"📝 问题：{question}")
    print("📊 待比较的回答：")
    for i, answer in enumerate(answers, 1):
        print(f"{i}. {answer}")
    
    comparison_result = engine.comparative_reflection(question, answers)
    print(f"\n⚖️ 比较分析结果：\n{comparison_result}")

def demo_confidence_evolution():
    """置信度演化演示"""
    print("\n📈 置信度演化演示")
    print("=" * 60)
    
    engine = SelfReflectionEngine()
    
    question = "量子计算相比传统计算有什么优势？实际应用前景如何？"
    
    print(f"📝 问题：{question}")
    
    # 执行多轮反思并跟踪置信度变化
    results = engine.multi_round_reflection(question, "计算机科学")
    
    print("\n📈 置信度演化过程：")
    for result in results:
        print(f"第{result.iteration}轮：置信度 {result.confidence_score:.2f}")
    
    if results:
        print(f"\n✨ 最终优化答案：\n{results[-1].improved_answer}")

def main():
    """主函数"""
    print("🔄 自我反思(Self-Reflection)技术演示")
    print("=" * 80)
    
    try:
        demo_basic_reflection()
        demo_error_detection()
        demo_comparative_reflection()
        demo_confidence_evolution()
        
        print("\n" + "=" * 80)
        print("🎉 演示完成！")
        print("💡 自我反思技术通过让模型审视自己的回答，显著提升了输出质量。")
        print("🚀 结合错误检测、比较分析等技巧，可以构建更可靠的AI系统。")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")

if __name__ == "__main__":
    main() 