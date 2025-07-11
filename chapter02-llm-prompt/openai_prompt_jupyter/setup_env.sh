#!/bin/bash

# OpenAI API 环境变量设置脚本
# 使用方法: ./setup_env.sh

echo "🔧 OpenAI API 环境变量配置助手"
echo "=================================="

# 检查是否已有配置
if [ ! -z "$OPENAI_API_KEY" ]; then
    echo "✅ 检测到已有 OPENAI_API_KEY: ${OPENAI_API_KEY:0:8}...${OPENAI_API_KEY: -4}"
else
    echo "❌ 未检测到 OPENAI_API_KEY 环境变量"
fi

echo ""
echo "请选择配置方式："
echo "1) 临时设置（仅当前会话有效）"
echo "2) 永久设置（写入 ~/.bashrc）"
echo "3) 创建 .env 文件"
echo "4) 显示当前配置"
echo "5) 验证配置"
echo "0) 退出"

read -p "请输入选项 [0-5]: " choice

case $choice in
    1)
        echo ""
        echo "🔧 临时环境变量设置"
        echo "==================="
        read -p "请输入您的 OpenAI API Key: " api_key
        read -p "请输入模型名称 [默认: gpt-4o]: " model_name
        model_name=${model_name:-gpt-4o}
        
        read -p "是否使用自定义API地址？(y/N): " custom_url
        if [[ $custom_url =~ ^[Yy]$ ]]; then
            read -p "请输入API地址 [如: https://vip.apiyi.com/v1]: " base_url
            export OPENAI_BASE_URL="$base_url"
            echo "export OPENAI_BASE_URL=\"$base_url\""
        fi
        
        export OPENAI_API_KEY="$api_key"
        export MODEL_NAME="$model_name"
        
        echo ""
        echo "✅ 临时环境变量设置成功！"
        echo "当前会话中可以使用以下变量："
        echo "export OPENAI_API_KEY=\"$api_key\""
        echo "export MODEL_NAME=\"$model_name\""
        ;;
        
    2)
        echo ""
        echo "🔧 永久环境变量设置"
        echo "==================="
        read -p "请输入您的 OpenAI API Key: " api_key
        read -p "请输入模型名称 [默认: gpt-4o]: " model_name
        model_name=${model_name:-gpt-4o}
        
        read -p "是否使用自定义API地址？(y/N): " custom_url
        
        # 备份 .bashrc
        cp ~/.bashrc ~/.bashrc.backup.$(date +%Y%m%d_%H%M%S)
        
        # 添加到 .bashrc
        echo "" >> ~/.bashrc
        echo "# OpenAI API Configuration (added by setup_env.sh)" >> ~/.bashrc
        echo "export OPENAI_API_KEY=\"$api_key\"" >> ~/.bashrc
        echo "export MODEL_NAME=\"$model_name\"" >> ~/.bashrc
        
        if [[ $custom_url =~ ^[Yy]$ ]]; then
            read -p "请输入API地址 [如: https://vip.apiyi.com/v1]: " base_url
            echo "export OPENAI_BASE_URL=\"$base_url\"" >> ~/.bashrc
        fi
        
        echo ""
        echo "✅ 永久环境变量设置成功！"
        echo "配置已添加到 ~/.bashrc"
        echo "请运行以下命令使配置生效："
        echo "source ~/.bashrc"
        echo ""
        echo "或者重新打开终端"
        ;;
        
    3)
        echo ""
        echo "🔧 创建 .env 文件"
        echo "================"
        read -p "请输入您的 OpenAI API Key: " api_key
        read -p "请输入模型名称 [默认: gpt-4o]: " model_name
        model_name=${model_name:-gpt-4o}
        
        cat > .env << EOF
# OpenAI API Configuration
OPENAI_API_KEY=$api_key
MODEL_NAME=$model_name
EOF

        read -p "是否使用自定义API地址？(y/N): " custom_url
        if [[ $custom_url =~ ^[Yy]$ ]]; then
            read -p "请输入API地址 [如: https://vip.apiyi.com/v1]: " base_url
            echo "OPENAI_BASE_URL=$base_url" >> .env
        fi
        
        echo ""
        echo "✅ .env 文件创建成功！"
        echo "文件内容："
        cat .env
        echo ""
        echo "注意：.env 文件需要配合 python-dotenv 库使用"
        ;;
        
    4)
        echo ""
        echo "🔍 当前配置信息"
        echo "==============="
        echo "OPENAI_API_KEY: ${OPENAI_API_KEY:+${OPENAI_API_KEY:0:8}...${OPENAI_API_KEY: -4}}"
        echo "MODEL_NAME: ${MODEL_NAME:-未设置}"
        echo "OPENAI_BASE_URL: ${OPENAI_BASE_URL:-未设置}"
        
        if [ -f .env ]; then
            echo ""
            echo ".env 文件存在，内容："
            cat .env
        fi
        ;;
        
    5)
        echo ""
        echo "🔍 验证配置"
        echo "==========="
        
        # 检查Python环境
        if command -v python3 &> /dev/null; then
            echo "✅ Python3 可用"
        else
            echo "❌ Python3 未找到"
        fi
        
        # 检查配置
        if [ ! -z "$OPENAI_API_KEY" ]; then
            echo "✅ OPENAI_API_KEY 已设置"
            
            # 测试API连接
            echo "🔍 测试API连接..."
            python3 -c "
import os
import sys
sys.path.append('.')

try:
    from config import validate_config, print_config_info
    print('✅ 配置模块可用')
    print_config_info()
    if validate_config():
        print('✅ 配置验证成功')
    else:
        print('❌ 配置验证失败')
except Exception as e:
    print(f'❌ 配置验证失败: {e}')
"
        else
            echo "❌ OPENAI_API_KEY 未设置"
        fi
        ;;
        
    0)
        echo "👋 再见！"
        exit 0
        ;;
        
    *)
        echo "❌ 无效选项"
        ;;
esac

echo ""
echo "🎯 下一步："
echo "1. 如果设置了环境变量，运行 'source ~/.bashrc' 或重新打开终端"
echo "2. 在 Jupyter notebook 中运行配置检查"
echo "3. 开始使用 OpenAI API！"
echo ""
echo "📚 获取API密钥："
echo "- OpenAI官方: https://platform.openai.com/api-keys"
echo "- DeepSeek: https://platform.deepseek.com/api-keys"
echo "- 国内代理: https://www.apiyi.com/register/?aff_code=we80" 