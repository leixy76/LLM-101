#!/usr/bin/env python3
"""
LLM-101 GPU 和 CUDA 环境检查脚本
用于验证 NVIDIA GPU 驱动和 CUDA 是否正确安装
"""

import os
import sys
import subprocess
import platform

def print_header(title):
    """打印标题"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def run_command(cmd, description=""):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_system_info():
    """检查系统信息"""
    print_header("系统信息")
    print(f"操作系统: {platform.system()} {platform.release()}")
    print(f"架构: {platform.machine()}")
    print(f"Python版本: {sys.version}")
    
    # 检查Ubuntu版本
    if platform.system() == "Linux":
        success, output, _ = run_command("lsb_release -a")
        if success:
            print(f"Linux发行版信息:")
            print(output)

def check_nvidia_gpu():
    """检查NVIDIA GPU硬件"""
    print_header("NVIDIA GPU 硬件检查")
    
    # 检查PCI设备
    success, output, _ = run_command("lspci | grep -i nvidia")
    if success and output.strip():
        print("✅ 检测到NVIDIA GPU硬件:")
        print(output)
        return True
    else:
        print("❌ 未检测到NVIDIA GPU硬件")
        return False

def check_nvidia_driver():
    """检查NVIDIA驱动"""
    print_header("NVIDIA 驱动检查")
    
    success, output, _ = run_command("nvidia-smi")
    if success:
        print("✅ NVIDIA驱动已安装并正常工作:")
        print(output)
        return True
    else:
        print("❌ NVIDIA驱动未安装或无法正常工作")
        print("请运行以下命令安装驱动:")
        print("sudo apt install -y ubuntu-drivers-common")
        print("sudo ubuntu-drivers autoinstall")
        print("sudo reboot")
        return False

def check_cuda():
    """检查CUDA"""
    print_header("CUDA 检查")
    
    # 检查nvcc命令
    success, output, _ = run_command("nvcc --version")
    if success:
        print("✅ CUDA已安装:")
        print(output)
        cuda_installed = True
    else:
        print("❌ CUDA未安装或nvcc命令不可用")
        cuda_installed = False
    
    # 检查CUDA路径
    cuda_paths = [
        "/usr/local/cuda",
        "/usr/local/cuda-12.1",
        "/usr/local/cuda-11.8"
    ]
    
    print("\n📁 CUDA安装路径检查:")
    for path in cuda_paths:
        if os.path.exists(path):
            print(f"✅ 发现CUDA路径: {path}")
        else:
            print(f"❌ 未找到CUDA路径: {path}")
    
    # 检查环境变量
    print("\n🔧 环境变量检查:")
    cuda_home = os.environ.get('CUDA_HOME')
    cuda_path = os.environ.get('PATH', '')
    cuda_lib = os.environ.get('LD_LIBRARY_PATH', '')
    
    print(f"CUDA_HOME: {cuda_home if cuda_home else '未设置'}")
    print(f"PATH包含CUDA: {'✅' if 'cuda' in cuda_path.lower() else '❌'}")
    print(f"LD_LIBRARY_PATH包含CUDA: {'✅' if 'cuda' in cuda_lib.lower() else '❌'}")
    
    return cuda_installed

def check_python_gpu_libraries():
    """检查Python GPU库"""
    print_header("Python GPU 库检查")
    
    libraries = [
        ("torch", "PyTorch"),
        ("tensorflow", "TensorFlow"),
        ("cupy", "CuPy"),
        ("numba", "Numba")
    ]
    
    for lib_name, display_name in libraries:
        try:
            __import__(lib_name)
            print(f"✅ {display_name} 已安装")
            
            # 特别检查PyTorch的CUDA支持
            if lib_name == "torch":
                import torch
                print(f"   PyTorch版本: {torch.__version__}")
                print(f"   CUDA可用: {'✅' if torch.cuda.is_available() else '❌'}")
                if torch.cuda.is_available():
                    print(f"   CUDA版本: {torch.version.cuda}")
                    print(f"   GPU数量: {torch.cuda.device_count()}")
                    for i in range(torch.cuda.device_count()):
                        print(f"   GPU {i}: {torch.cuda.get_device_name(i)}")
                        
        except ImportError:
            print(f"❌ {display_name} 未安装")

def check_conda_environment():
    """检查Conda环境"""
    print_header("Conda 环境检查")
    
    # 检查conda命令
    success, output, _ = run_command("conda --version")
    if success:
        print(f"✅ Conda已安装: {output.strip()}")
    else:
        print("❌ Conda未安装")
        return False
    
    # 检查当前环境
    current_env = os.environ.get('CONDA_DEFAULT_ENV', 'base')
    print(f"当前环境: {current_env}")
    
    # 列出所有环境
    success, output, _ = run_command("conda env list")
    if success:
        print("可用环境:")
        print(output)
    
    return True

def provide_recommendations():
    """提供建议"""
    print_header("环境配置建议")
    
    print("📋 完整的环境配置步骤:")
    print("1. 检查GPU硬件: lspci | grep -i nvidia")
    print("2. 安装NVIDIA驱动: sudo ubuntu-drivers autoinstall")
    print("3. 重启系统: sudo reboot")
    print("4. 安装CUDA 12.1:")
    print("   wget https://developer.download.nvidia.com/compute/cuda/12.1.0/local_installers/cuda_12.1.0_530.30.02_linux.run")
    print("   sudo sh cuda_12.1.0_530.30.02_linux.run --silent --toolkit --toolkitpath=/usr/local/cuda-12.1 --no-opengl-libs --override")
    print("5. 设置环境变量:")
    print("   echo 'export PATH=\"/usr/local/cuda-12.1/bin:$PATH\"' >> ~/.bashrc")
    print("   echo 'export LD_LIBRARY_PATH=\"/usr/local/cuda-12.1/lib64:$LD_LIBRARY_PATH\"' >> ~/.bashrc")
    print("   source ~/.bashrc")
    print("6. 创建Conda环境: conda create -n llm101 python=3.10.18")
    print("7. 激活环境: conda activate llm101")
    print("8. 安装PyTorch: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
    
    print("\n🔧 自动化脚本:")
    print("运行项目提供的自动化脚本: ./chapter01-llm-env/setup_llm101_dev.sh")

def main():
    """主函数"""
    print("🚀 LLM-101 GPU 和 CUDA 环境检查")
    print("=" * 60)
    
    # 系统信息
    check_system_info()
    
    # GPU硬件检查
    gpu_hardware = check_nvidia_gpu()
    
    # 驱动检查
    driver_ok = check_nvidia_driver() if gpu_hardware else False
    
    # CUDA检查
    cuda_ok = check_cuda()
    
    # Python库检查
    check_python_gpu_libraries()
    
    # Conda环境检查
    conda_ok = check_conda_environment()
    
    # 总结
    print_header("环境检查总结")
    print(f"GPU硬件: {'✅' if gpu_hardware else '❌'}")
    print(f"NVIDIA驱动: {'✅' if driver_ok else '❌'}")
    print(f"CUDA: {'✅' if cuda_ok else '❌'}")
    print(f"Conda: {'✅' if conda_ok else '❌'}")
    
    if not (gpu_hardware and driver_ok and cuda_ok):
        provide_recommendations()
    else:
        print("\n🎉 恭喜！您的GPU和CUDA环境配置正确！")
        print("可以开始使用LLM-101进行大模型开发了！")

if __name__ == "__main__":
    main() 