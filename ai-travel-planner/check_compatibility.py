#!/usr/bin/env python3
"""
检查vLLM 0.9.1与其他依赖的兼容性
Check compatibility of vLLM 0.9.1 with other dependencies
"""

import sys
from packaging import version

def check_vllm_compatibility():
    """检查vLLM 0.9.1的依赖兼容性"""
    print("🔍 检查vLLM 0.9.1依赖兼容性...")
    
    # vLLM 0.9.1的推荐依赖版本
    vllm_requirements = {
        "torch": ">=2.4.0",
        "transformers": ">=4.45.0", 
        "tokenizers": ">=0.19.0",
        "accelerate": ">=0.26.0",
        "ray": ">=2.9.0",
        "pydantic": ">=2.0.0",
        "numpy": ">=1.24.0",
        "fastapi": ">=0.100.0",
    }
    
    # 当前项目中的版本
    current_versions = {
        "torch": "2.5.1",
        "transformers": "4.47.1",
        "tokenizers": "0.21.0", 
        "accelerate": "1.2.1",
        "ray": "2.40.0",
        "pydantic": "2.10.3",
        "numpy": "2.2.1",
        "fastapi": "0.115.6",
    }
    
    print("\n📋 兼容性检查结果:")
    all_compatible = True
    
    for package, min_version in vllm_requirements.items():
        current_ver = current_versions.get(package, "未知")
        min_ver = min_version.replace(">=", "")
        
        if current_ver != "未知":
            try:
                if version.parse(current_ver) >= version.parse(min_ver):
                    print(f"✅ {package}: {current_ver} (要求: {min_version})")
                else:
                    print(f"❌ {package}: {current_ver} (要求: {min_version})")
                    all_compatible = False
            except Exception as e:
                print(f"⚠️  {package}: 版本解析错误 - {e}")
        else:
            print(f"⚠️  {package}: 版本未知")
    
    print(f"\n{'✅ 所有依赖兼容!' if all_compatible else '❌ 存在兼容性问题!'}")
    
    # 额外的vLLM 0.9.1特性说明
    print("\n🆕 vLLM 0.9.1 新特性:")
    print("- 改进的内存管理和性能优化")
    print