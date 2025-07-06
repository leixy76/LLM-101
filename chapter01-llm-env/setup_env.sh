#!/bin/bash

# LLM-101 环境配置脚本
# 适用于 Ubuntu 22.04 + Python 3.10.18

set -e

echo "🚀 开始配置 LLM-101 开发环境..."

# 检查系统版本
echo "📋 检查系统环境..."
if [[ $(lsb_release -rs) != "22.04" ]]; then
    echo "⚠️  警告: 推荐使用 Ubuntu 22.04 LTS"
fi

# 更新系统包
echo "🔄 更新系统包..."
sudo apt update && sudo apt upgrade -y

# 安装基础依赖
echo "📦 安装基础依赖..."
sudo apt install -y \
    curl \
    wget \
    git \
    build-essential \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release

# 检查是否已安装 Conda
if ! command -v conda &> /dev/null; then
    echo "🐍 安装 Miniconda..."
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
    bash ~/miniconda.sh -b -p $HOME/miniconda
    echo 'export PATH="$HOME/miniconda/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
    rm ~/miniconda.sh
else
    echo "✅ Conda 已安装"
fi

# 初始化 Conda
echo "🔧 初始化 Conda..."
source $HOME/miniconda/etc/profile.d/conda.sh

# 创建虚拟环境
echo "🌟 创建 LLM-101 虚拟环境..."
conda create -n llm101 python=3.10.18 -y
conda activate llm101

# 检查 GPU 和 CUDA
echo "🖥️  检查 GPU 状态..."
if command -v nvidia-smi &> /dev/null; then
    echo "✅ NVIDIA GPU 检测成功"
    nvidia-smi
    
    # 安装 CUDA Toolkit
    echo "🔥 安装 CUDA Toolkit..."
    conda install -y nvidia/label/cuda-11.8.0::cuda-toolkit
    
    # 安装 PyTorch (GPU版本)
    echo "🔥 安装 PyTorch (GPU版本)..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
else
    echo "⚠️  未检测到 NVIDIA GPU，将安装 CPU 版本"
    # 安装 PyTorch (CPU版本)
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
fi

# 安装项目依赖
echo "📚 安装项目依赖..."
pip install -r requirements.txt

# 验证安装
echo "🔍 验证安装..."
python -c "import torch; print(f'PyTorch版本: {torch.__version__}')"
python -c "import torch; print(f'CUDA可用: {torch.cuda.is_available()}')"

# 安装开发工具
echo "🛠️  安装开发工具..."

# 配置 Git (如果尚未配置)
if [[ -z $(git config --global user.name) ]]; then
    echo "🔧 配置 Git..."
    read -p "请输入您的 Git 用户名: " git_name
    read -p "请输入您的 Git 邮箱: " git_email
    git config --global user.name "$git_name"
    git config --global user.email "$git_email"
fi

# 创建项目目录结构
echo "📁 创建项目目录结构..."
mkdir -p {data,models,logs,outputs,configs}

# 创建环境变量文件
echo "🔐 创建环境变量模板..."
if [ ! -f "env.template" ]; then
    echo "❌ 环境变量模板文件不存在，请确保 env.template 文件存在"
    exit 1
fi

echo "📝 请复制 env.template 为 .env 并填入您的 API Keys"

# 完成提示
echo ""
echo "🎉 LLM-101 环境配置完成！"
echo ""
echo "📋 下一步操作："
echo "1. 激活虚拟环境: conda activate llm101"
echo "2. 复制环境变量: cp env.template .env"
echo "3. 编辑 .env 文件，填入您的 API Keys"
echo "4. 运行第一个应用: python first_llm_app.py"
echo "5. 尝试提示词工程: python prompt_engineering_demo.py"
echo ""
echo "🔗 更多信息请查看 README.md"
echo "💡 如有问题，请访问项目 GitHub 仓库获取帮助"
echo ""
echo "⭐ 如果这个项目对您有帮助，请给个 Star 支持！" 