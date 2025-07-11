#!/usr/bin/env python3
"""
测试集成提示法修复
"""

from config import setup_notebook_environment

def test_ensemble_fix():
    """测试修复后的集成提示法"""
    
    # 设置环境
    try:
        client, get_completion = setup_notebook_environment()
        print("✅ 环境设置成功！")
    except Exception as e:
        print(f"❌ 环境设置失败: {e}")
        return
    
    # 定义修复后的集成提示法函数
    def ensemble_completion(prompt: str, system_prompt="", prefill="", n_runs=3):
        """
        修复版本的集成提示法：通过多次运行并选择最优结果来提高稳定性
        """
        results = []
        
        for i in range(n_runs):
            try:
                # 修复：只传入get_completion支持的3个参数
                result = get_completion(prompt, system_prompt, prefill)
                results.append(result)
                print(f"第 {i+1} 次运行完成，长度: {len(result)} 字符")
            except Exception as e:
                print(f"第 {i+1} 次运行失败: {e}")
        
        if not results:
            return "所有运行都失败了"
        
        # 选择最长的响应（通常更详细）
        best_result = max(results, key=len)
        
        print(f"\n=== 集成提示法结果 ===")
        print(f"运行了 {len(results)} 次，选择了最佳结果")
        print(f"最佳结果长度: {len(best_result)} 字符")
        
        return best_result
    
    # 测试用的简化提示
    test_prompt = """你是「小智」，一位专业的职业规划导师。

【问题】
社会工作师和人力资源专员，哪个职业需要更高的学历要求？

请给出专业分析。"""

    prefill = "小智："
    
    print("\n" + "="*60)
    print("🎯 【集成提示法测试】")
    print("="*60)
    
    # 运行集成提示法测试
    try:
        result = ensemble_completion(test_prompt, prefill=prefill, n_runs=2)
        print(f"\n【最终选择的回答】\n{result}")
        print(f"\n✅ 集成提示法测试成功！")
    except Exception as e:
        print(f"❌ 集成提示法测试失败: {e}")

if __name__ == "__main__":
    test_ensemble_fix() 