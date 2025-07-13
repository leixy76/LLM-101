# VLLM DeepSeek 谷歌 Colab 实验场

一个用于在 Google Colab 中使用 VLLM 运行 DeepSeek 模型的简化实现。这个实验场允许您在 Colab 环境中轻松部署和交互 DeepSeek-R1-Distill-Qwen-1.5B 和其他 DeepSeek 模型。

## 📚 目录

- [VLLM DeepSeek 谷歌 Colab 实验场](#vllm-deepseek-谷歌-colab-实验场)
  - [📚 目录](#-目录)
  - [🚀 特性](#-特性)
  - [🌟 Google Colab 简介](#-google-colab-简介)
    - [什么是 Google Colab？](#什么是-google-colab)
    - [🎯 为什么选择 Google Colab？](#-为什么选择-google-colab)
    - [🔧 支持的硬件规格](#-支持的硬件规格)
  - [📝 Google Colab 注册使用流程](#-google-colab-注册使用流程)
    - [第一步：注册 Google 账户](#第一步注册-google-账户)
    - [第二步：访问 Google Colab](#第二步访问-google-colab)
    - [第三步：创建和配置笔记本](#第三步创建和配置笔记本)
    - [第四步：启用 GPU 加速](#第四步启用-gpu-加速)
    - [第五步：Google Drive 集成（可选）](#第五步google-drive-集成可选)
    - [第六步：基本使用技巧](#第六步基本使用技巧)
    - [第七步：使用限制和注意事项](#第七步使用限制和注意事项)
    - [第八步：升级到付费版本（可选）](#第八步升级到付费版本可选)
  - [📋 前置条件](#-前置条件)
    - [🎯 必需条件](#-必需条件)
    - [🚀 推荐配置](#-推荐配置)
    - [💡 免费资源说明](#-免费资源说明)
  - [🛠️ 快速开始](#️-快速开始)
  - [⚙️ 配置选项](#️-配置选项)
    - [模型参数](#模型参数)
    - [服务器设置](#服务器设置)
  - [🔍 监控和调试](#-监控和调试)
  - [📊 性能提示](#-性能提示)
  - [🚧 故障排除](#-故障排除)
  - [📝 许可证](#-许可证)
  - [🙏 致谢](#-致谢)
  - [🤝 贡献](#-贡献)

## 🚀 特性

- 在 Google Colab 中轻松部署 DeepSeek 模型
- 实时服务器监控和状态检查
- 针对 Colab 的 GPU 环境进行优化
- 模型交互的交互式界面
- 使用 VLLM 进行内存高效的模型服务
- 支持各种 DeepSeek 模型变体

## 🌟 Google Colab 简介

### 什么是 Google Colab？

Google Colab（Colaboratory）是 Google 提供的一个免费的云端 Jupyter 笔记本环境，专门为机器学习和数据科学设计。它最大的优势是**完全免费提供 GPU 和 TPU 资源**，让您无需购买昂贵的硬件就能运行深度学习模型。

### 🎯 为什么选择 Google Colab？

**💰 免费 GPU 资源**
- **Tesla T4 GPU**：15GB 显存，完全免费使用
- **运行时限制**：免费版本每次可连续运行 12 小时
- **每日限制**：通常每天可使用 12-24 小时的 GPU 时间

**🚀 零配置环境**
- 无需安装任何软件，直接在浏览器中运行
- 预装了 TensorFlow、PyTorch、NumPy 等常用库
- 支持 pip 和 apt 包管理器

**☁️ 云端存储**
- 与 Google Drive 无缝集成
- 代码和数据自动保存到云端
- 支持多人协作编辑

**💡 付费升级选项**
- **Colab Pro**：$9.99/月，更长的运行时间和更好的 GPU
- **Colab Pro+**：$49.99/月，包含更强大的 GPU（V100、A100）

### 🔧 支持的硬件规格

| GPU 类型 | 显存 | 免费版本 | 付费版本 | 适用场景 |
|---------|------|----------|----------|----------|
| Tesla T4 | 15GB | ✅ | ✅ | 小型模型训练、推理 |
| Tesla V100 | 16GB | ❌ | ✅ | 中型模型训练 |
| Tesla A100 | 40GB | ❌ | ✅ | 大型模型训练 |
| Tesla L4 | 22.5GB | ❌ | ✅ | 新一代高效推理 |

## 📝 Google Colab 注册使用流程

### 第一步：注册 Google 账户

1. **访问 Google 官网**
   - 打开浏览器，访问 [accounts.google.com](https://accounts.google.com)
   - 点击"创建账户" → "个人用途"

2. **填写注册信息**
   ```
   姓名：输入您的真实姓名
   用户名：选择一个唯一的用户名
   密码：设置强密码（至少8位，包含字母、数字、符号）
   ```

3. **验证手机号码**
   - 输入手机号码接收验证码
   - 输入收到的验证码完成验证

4. **完成账户设置**
   - 添加恢复邮箱（可选但推荐）
   - 同意 Google 服务条款

### 第二步：访问 Google Colab

1. **打开 Colab 官网**
   - 访问 [colab.research.google.com](https://colab.research.google.com)
   - 使用您的 Google 账户登录

2. **初次使用设置**
   - 首次访问会显示欢迎页面
   - 可以选择查看教程或直接开始使用

3. **从 GitHub 打开笔记本**
   ```
   方法一：直接访问 GitHub 链接
   - 在 GitHub 上找到 .ipynb 文件
   - 将 GitHub URL 中的 "github.com" 替换为 "colab.research.google.com/github"
   
   方法二：使用 Colab 打开
   - 在 Colab 中点击"文件" → "打开笔记本"
   - 选择"GitHub"标签页
   - 输入仓库 URL 或搜索用户名/仓库名
   
   方法三：使用徽章链接
   - 点击 README 中的 "Open in Colab" 徽章
   - 自动跳转到 Colab 并加载笔记本
   ```

### 第三步：创建和配置笔记本

1. **创建新笔记本**
   ```
   方法一：点击"新建笔记本"
   方法二：文件 → 新建笔记本
   方法三：使用快捷键 Ctrl+M N
   ```

2. **重命名笔记本**
   - 点击左上角的"Untitled0.ipynb"
   - 输入新名称，如"DeepSeek-VLLM-Demo"

3. **连接到运行时**
   - 点击右上角的"连接"按钮
   - 等待分配计算资源（通常需要10-30秒）

### 第四步：启用 GPU 加速

1. **更改运行时类型**
   ```
   菜单栏 → 代码执行程序 → 更改运行时类型
   或者：Runtime → Change runtime type
   ```

2. **选择硬件加速器**
   ```
   硬件加速器：选择 "GPU"
   GPU 类型：选择 "T4"（免费版本）
   运行时规格：选择 "标准"
   ```

3. **确认设置**
   - 点击"保存"按钮
   - 系统会重新分配带有 GPU 的运行时

4. **验证 GPU 可用性**
   ```python
   # 在代码单元格中运行以下代码
   !nvidia-smi
   
   # 或者使用 Python 检查
   import torch
   print(f"CUDA 可用: {torch.cuda.is_available()}")
   print(f"GPU 数量: {torch.cuda.device_count()}")
   if torch.cuda.is_available():
       print(f"GPU 名称: {torch.cuda.get_device_name(0)}")
   ```

### 第五步：Google Drive 集成（可选）

1. **挂载 Google Drive**
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

2. **授权访问**
   - 点击生成的链接
   - 选择您的 Google 账户
   - 点击"允许"授权访问

3. **验证挂载**
   ```python
   import os
   print(os.listdir('/content/drive/MyDrive'))
   ```

### 第六步：基本使用技巧

1. **代码单元格操作**
   ```
   运行当前单元格：Ctrl + Enter
   运行并创建新单元格：Shift + Enter
   添加代码单元格：Ctrl + M B
   添加文本单元格：Ctrl + M M
   删除单元格：Ctrl + M D
   ```

2. **文件上传下载**
   ```python
   # 上传文件
   from google.colab import files
   uploaded = files.upload()
   
   # 下载文件
   files.download('filename.txt')
   ```

3. **安装 Python 包**
   ```python
   # 使用 pip 安装
   !pip install package_name
   
   # 使用 apt 安装系统包
   !apt-get install package_name
   ```

4. **查看系统信息**
   ```python
   # 查看 CPU 信息
   !cat /proc/cpuinfo | grep "model name" | head -1
   
   # 查看内存信息
   !free -h
   
   # 查看磁盘空间
   !df -h
   ```

### 第七步：使用限制和注意事项

1. **免费版本限制**
   ```
   - 连续运行时间：最长 12 小时
   - 空闲超时：90 分钟自动断开
   - 每日使用限制：通常 12-24 小时
   - 存储空间：临时磁盘约 100GB
   ```

2. **最佳实践**
   ```
   - 定期保存工作到 Google Drive
   - 避免长时间空闲（会被自动断开）
   - 大文件建议存储在 Google Drive 中
   - 使用 GPU 时及时释放资源
   ```

3. **常见问题解决**
   ```
   问题：无法连接到 GPU
   解决：重新选择运行时类型，或稍后重试
   
   问题：运行时意外断开
   解决：重新连接运行时，从 Google Drive 恢复数据
   
   问题：安装包失败
   解决：使用 !pip install --upgrade pip 更新 pip
   ```

### 第八步：升级到付费版本（可选）

1. **Colab Pro 订阅**
   - 访问 [colab.research.google.com/signup](https://colab.research.google.com/signup)
   - 选择 Colab Pro ($9.99/月)
   - 享受更长的运行时间和更好的 GPU

2. **Pro+ 高级功能**
   - 访问更强大的 GPU（V100、A100）
   - 更长的运行时间限制
   - 更大的内存容量
   - 后台执行支持

## 🌐 Ngrok 隧道服务详解

### 什么是 Ngrok？

Ngrok 是一个强大的内网穿透工具，可以将您在本地（或 Colab）运行的服务通过安全隧道暴露到公网上。在我们的项目中，Ngrok 用于将 Colab 中运行的 VLLM 服务暴露到公网，让您可以从任何地方访问您的大模型 API。

### 🎯 为什么需要 Ngrok？

**🔒 Colab 网络限制**
- Google Colab 默认不允许外部直接访问内部端口
- 本地服务（如 FastAPI）只能在 Colab 内部访问
- 需要隧道服务将内部端口暴露到公网

**🌍 远程访问需求**
- 让团队成员访问您的模型服务
- 在移动设备上测试 API
- 与外部应用程序集成
- 演示和分享您的项目

**⚡ 即时部署**
- 无需复杂的服务器配置
- 几秒钟内获得公网 URL
- 支持 HTTPS 加密传输

### 📝 Ngrok 注册使用完整流程

#### 第一步：注册 Ngrok 账户

1. **访问 Ngrok 官网**
   - 打开浏览器，访问 [ngrok.com](https://ngrok.com)
   - 点击右上角的 "Sign up" 按钮

2. **选择注册方式**
   ```
   方式一：邮箱注册
   - 输入邮箱地址
   - 设置密码（至少8位，包含字母和数字）
   - 点击 "Sign up"
   
   方式二：第三方登录
   - GitHub 账户登录
   - Google 账户登录
   - Microsoft 账户登录
   ```

3. **验证邮箱**
   - 检查您的邮箱收件箱
   - 点击验证链接完成邮箱验证
   - 返回 Ngrok 网站登录

#### 第二步：获取 Authtoken

1. **登录 Ngrok Dashboard**
   - 使用注册的账户登录 [dashboard.ngrok.com](https://dashboard.ngrok.com)
   - 进入控制台主页

2. **获取 Authtoken**
   ```
   位置：Dashboard → Getting Started → Your Authtoken
   或者：Dashboard → Auth → Your Authtoken
   
   示例 Token：
   2abc123def456ghi789jkl012mno345_6pqrstu7vwxyz8ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk
   ```

3. **复制并保存 Token**
   - 点击 "Copy" 按钮复制完整的 authtoken
   - 将 token 保存到安全的地方（如密码管理器）
   - ⚠️ **重要**：不要将 token 分享给他人或提交到公共代码仓库

#### 第三步：在 Colab 中配置 Ngrok

1. **安装 pyngrok**
   ```python
   # 安装 pyngrok 包
   !pip install pyngrok
   ```

2. **设置 Authtoken**
   ```python
   from pyngrok import ngrok
   
   # 方法一：直接设置（适合临时使用）
   ngrok.set_auth_token("your_authtoken_here")
   
   # 方法二：使用环境变量（推荐）
   import os
   os.environ['NGROK_AUTHTOKEN'] = 'your_authtoken_here'
   ngrok.set_auth_token(os.environ['NGROK_AUTHTOKEN'])
   ```

3. **创建隧道**
   ```python
   # 创建 HTTP 隧道到端口 8000
   public_url = ngrok.connect(8000)
   print(f"🌐 公网访问地址: {public_url}")
   
   # 获取隧道信息
   tunnels = ngrok.get_tunnels()
   for tunnel in tunnels:
       print(f"隧道名称: {tunnel.name}")
       print(f"本地地址: {tunnel.config['addr']}")
       print(f"公网地址: {tunnel.public_url}")
   ```

#### 第四步：验证隧道连接

1. **检查隧道状态**
   ```python
   import requests
   import time
   
   def check_tunnel_status(public_url):
       try:
           # 检查健康端点
           health_url = f"{public_url}/health"
           response = requests.get(health_url, timeout=10)
           
           if response.status_code == 200:
               print(f"✅ 隧道连接成功！")
               print(f"🌐 API 基础地址: {public_url}")
               print(f"🔍 健康检查: {health_url}")
               print(f"📝 API 文档: {public_url}/docs")
               return True
           else:
               print(f"❌ 隧道连接失败，状态码: {response.status_code}")
               return False
               
       except requests.exceptions.RequestException as e:
           print(f"❌ 连接错误: {e}")
           return False
   
   # 等待服务启动
   time.sleep(5)
   check_tunnel_status(public_url)
   ```

2. **测试 API 调用**
   ```python
   def test_api_call(public_url):
       try:
           api_url = f"{public_url}/v1/chat/completions"
           
           payload = {
               "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
               "messages": [
                   {"role": "user", "content": "你好，请介绍一下你自己"}
               ],
               "max_tokens": 100,
               "temperature": 0.7
           }
           
           headers = {
               "Content-Type": "application/json"
           }
           
           response = requests.post(api_url, json=payload, headers=headers, timeout=30)
           
           if response.status_code == 200:
               result = response.json()
               print("✅ API 调用成功！")
               print(f"🤖 模型回复: {result['choices'][0]['message']['content']}")
           else:
               print(f"❌ API 调用失败，状态码: {response.status_code}")
               print(f"错误信息: {response.text}")
               
       except Exception as e:
           print(f"❌ API 测试错误: {e}")
   
   # 执行 API 测试
   test_api_call(public_url)
   ```

#### 第五步：Ngrok 管理和监控

1. **查看隧道状态**
   ```python
   # 获取所有活跃隧道
   tunnels = ngrok.get_tunnels()
   print(f"活跃隧道数量: {len(tunnels)}")
   
   for i, tunnel in enumerate(tunnels):
       print(f"\n隧道 {i+1}:")
       print(f"  名称: {tunnel.name}")
       print(f"  协议: {tunnel.proto}")
       print(f"  本地地址: {tunnel.config['addr']}")
       print(f"  公网地址: {tunnel.public_url}")
   ```

2. **访问 Ngrok Web 界面**
   ```python
   # Ngrok 提供本地 Web 界面用于监控
   print("🖥️  Ngrok Web 界面: http://127.0.0.1:4040")
   print("📊 在此界面可以查看:")
   print("   - 实时请求日志")
   print("   - 隧道状态和配置")
   print("   - 请求/响应详情")
   print("   - 性能统计信息")
   ```

3. **关闭隧道**
   ```python
   # 关闭特定隧道
   ngrok.disconnect(public_url)
   
   # 关闭所有隧道
   ngrok.kill()
   
   print("🔒 所有 Ngrok 隧道已关闭")
   ```

### 🔧 Ngrok 高级配置

#### 自定义域名（付费功能）

```python
# 使用自定义子域名（需要付费账户）
public_url = ngrok.connect(8000, subdomain="my-llm-api")
print(f"🌐 自定义域名: {public_url}")
```

#### 基本认证保护

```python
# 添加基本认证保护 API
public_url = ngrok.connect(8000, auth="username:password")
print(f"🔐 受保护的 API: {public_url}")
```

#### 区域选择

```python
# 选择 Ngrok 服务器区域（减少延迟）
public_url = ngrok.connect(8000, region="ap")  # 亚太地区
# 可选区域: us, eu, ap, au, sa, jp, in
```

### 💡 Ngrok 使用技巧和注意事项

#### ✅ 最佳实践

1. **安全性考虑**
   ```python
   # 使用环境变量存储敏感信息
   import os
   from google.colab import userdata
   
   # 在 Colab 中使用 Secrets 功能
   try:
       ngrok_token = userdata.get('NGROK_TOKEN')
       ngrok.set_auth_token(ngrok_token)
   except:
       print("请在 Colab Secrets 中设置 NGROK_TOKEN")
   ```

2. **错误处理**
   ```python
   def create_secure_tunnel(port, retries=3):
       for attempt in range(retries):
           try:
               public_url = ngrok.connect(port)
               print(f"✅ 隧道创建成功 (尝试 {attempt + 1}): {public_url}")
               return public_url
           except Exception as e:
               print(f"❌ 隧道创建失败 (尝试 {attempt + 1}): {e}")
               if attempt < retries - 1:
                   time.sleep(2)
               else:
                   raise e
   ```

3. **资源清理**
   ```python
   import atexit
   
   def cleanup_ngrok():
       """程序退出时自动清理 Ngrok 隧道"""
       try:
           ngrok.kill()
           print("🧹 Ngrok 隧道已清理")
       except:
           pass
   
   # 注册退出处理函数
   atexit.register(cleanup_ngrok)
   ```

#### ⚠️ 限制和注意事项

1. **免费账户限制**
   ```
   - 同时最多 1 个隧道
   - 每分钟最多 20 个连接
   - 隧道会在 8 小时后自动关闭
   - 随机生成的子域名
   ```

2. **付费升级选项**
   ```
   Personal Plan ($8/月):
   - 同时最多 3 个隧道
   - 自定义子域名
   - 更高的连接限制
   
   Pro Plan ($20/月):
   - 同时最多 10 个隧道
   - 自定义域名
   - IP 白名单
   - 密码保护
   ```

3. **性能考虑**
   ```
   - Ngrok 会增加一定的网络延迟
   - 大文件传输可能较慢
   - 建议仅用于开发和演示
   - 生产环境建议使用专业的云服务
   ```

### 📱 完整的 Ngrok 使用示例

```python
# 完整的 Ngrok 集成示例
import os
import time
import requests
from pyngrok import ngrok

class NgrokManager:
    def __init__(self, authtoken):
        self.authtoken = authtoken
        self.public_url = None
        self.setup_ngrok()
    
    def setup_ngrok(self):
        """设置 Ngrok 认证"""
        try:
            ngrok.set_auth_token(self.authtoken)
            print("✅ Ngrok 认证设置成功")
        except Exception as e:
            print(f"❌ Ngrok 认证失败: {e}")
            raise
    
    def create_tunnel(self, port, subdomain=None):
        """创建安全隧道"""
        try:
            if subdomain:
                self.public_url = ngrok.connect(port, subdomain=subdomain)
            else:
                self.public_url = ngrok.connect(port)
            
            print(f"🌐 隧道创建成功: {self.public_url}")
            return self.public_url
        except Exception as e:
            print(f"❌ 隧道创建失败: {e}")
            raise
    
    def wait_for_service(self, max_wait=60):
        """等待服务启动"""
        print("⏳ 等待服务启动...")
        
        for i in range(max_wait):
            try:
                response = requests.get(f"{self.public_url}/health", timeout=5)
                if response.status_code == 200:
                    print(f"✅ 服务已启动！用时 {i+1} 秒")
                    return True
            except:
                time.sleep(1)
        
        print(f"❌ 服务启动超时（{max_wait} 秒）")
        return False
    
    def get_api_info(self):
        """获取 API 信息"""
        if not self.public_url:
            return None
        
        return {
            "base_url": self.public_url,
            "health_check": f"{self.public_url}/health",
            "api_docs": f"{self.public_url}/docs",
            "chat_endpoint": f"{self.public_url}/v1/chat/completions"
        }
    
    def cleanup(self):
        """清理隧道"""
        try:
            ngrok.kill()
            print("🧹 Ngrok 隧道已清理")
        except:
            pass

# 使用示例
if __name__ == "__main__":
    # 替换为您的实际 authtoken
    NGROK_TOKEN = "your_authtoken_here"
    
    # 创建 Ngrok 管理器
    ngrok_manager = NgrokManager(NGROK_TOKEN)
    
    # 创建隧道
    public_url = ngrok_manager.create_tunnel(8000)
    
    # 等待服务启动
    if ngrok_manager.wait_for_service():
        # 显示 API 信息
        api_info = ngrok_manager.get_api_info()
        print("\n🚀 API 服务信息:")
        for key, value in api_info.items():
            print(f"  {key}: {value}")
    
    # 程序结束时清理
    # ngrok_manager.cleanup()
```

## 📋 前置条件

在运行实验场之前，请确保您具备：

### 🎯 必需条件
- **Google 账户**：用于访问 Google Colab（完全免费）
- **网络连接**：稳定的互联网连接用于模型下载和推理

### 🚀 推荐配置
- **GPU 运行时**：在 Colab 中启用 GPU 加速（Tesla T4 免费提供）
- **Google Drive**：用于保存代码和模型文件（可选）

### 💡 免费资源说明
- **完全免费**：Google Colab 提供的 Tesla T4 GPU（15GB 显存）
- **无需付费**：所有基础功能都可以免费使用
- **即开即用**：无需安装任何软件或配置环境

## 🛠️ 快速开始

1. **在 Colab 中打开**
   
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/your-username/your-repo/blob/main/deepseek_vllm_demo.ipynb)
   
   > 💡 **提示**：点击上方徽章可直接在 Google Colab 中打开预配置的笔记本

2. **安装依赖**
   ```python
   !pip install fastapi nest-asyncio pyngrok uvicorn

   !pip install vllm
   ```

3. **启动服务器**
   ```python
   import subprocess
   model = 'deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B' # 在此处指定您的模型

   
   vllm_process = subprocess.Popen([
       'vllm',
       'serve',
       'deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B',
       '--trust-remote-code',
       '--dtype', 'half',
       '--max-model-len', '16384',
       '--enable-chunked-prefill', 'false',
       '--tensor-parallel-size', '1'
   ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
   ```

4. **监控服务器状态**
   ```python
   # [包含之前实现的监控代码]
   ```

## ⚙️ 配置选项

### 模型参数
- `--dtype`: 设置为 'half' 以获得最佳 Colab 性能
- `--max-model-len`: 最大序列长度（默认：16384）
- `--tensor-parallel-size`: GPU 并行设置
- `--enable-chunked-prefill`: 预填充优化设置

### 服务器设置
- 默认端口：8000
- 健康检查端点：`/health`
- 生成端点：`/generate`

## 🔍 监控和调试

实验场包含内置的监控功能：
- 实时服务器状态检查
- 输出日志记录（stdout/stderr）
- 错误处理和恢复
- 进程管理

## 📊 性能提示

1. **内存管理**
   - 使用 `dtype=half` 进行高效内存使用
   - 根据需要调整 `max-model-len`
   - 监控 Colab GPU 内存使用情况

2. **优化**
   - 尽可能批处理请求
   - 使用适当的温度设置
   - 监控令牌使用情况

## 🚧 故障排除

常见问题和解决方案：

1. **服务器无法启动**
   - 检查 Colab 中的 GPU 可用性
   - 验证 VLLM 安装
   - 检查内存使用情况

2. **响应时间慢**
   - 减少 `max_tokens`
   - 调整批处理大小
   - 检查网络连接

3. **内存不足**
   - 减少模型参数
   - 清除 Colab 运行时
   - 使用 GPU 重启运行时

## 🌐 Ngrok 详细使用指南

### 🔧 什么是 Ngrok？

Ngrok 是一个安全的内网穿透工具，可以将本地运行的服务通过安全隧道暴露到公网，让外部用户可以访问您在 Colab 中运行的模型服务。

**主要优势：**
- 🚀 快速将本地服务暴露到公网
- 🔒 提供 HTTPS 加密连接
- 📊 内置流量监控和分析
- 🌍 全球多个节点可选
- 💻 无需复杂的网络配置

### 📝 Ngrok 注册流程

#### 第一步：访问 Ngrok 官网

1. 打开浏览器，访问 [https://ngrok.com](https://ngrok.com)
2. 点击右上角的 **"Sign up"** 按钮

#### 第二步：创建账户

**方式一：使用邮箱注册**
```
1. 选择 "Sign up with email"
2. 填写以下信息：
   - Email: 您的邮箱地址
   - Password: 设置密码（至少8位）
   - Confirm Password: 确认密码
3. 勾选同意服务条款
4. 点击 "Sign up" 完成注册
```

**方式二：使用第三方账户**
```
支持以下方式快速注册：
- GitHub 账户
- Google 账户
- Microsoft 账户
```

#### 第三步：邮箱验证

1. 检查您的邮箱，查找来自 Ngrok 的验证邮件
2. 点击邮件中的验证链接
3. 完成邮箱验证后，自动跳转到控制台

### 🔑 获取 Authtoken

#### 在 Ngrok Dashboard 中获取

1. **登录后访问控制台**
   ```
   登录成功后，您会看到 Ngrok Dashboard
   ```

2. **找到 Authtoken 部分**
   ```
   在左侧菜单中点击 "Your Authtoken"
   或直接访问：https://dashboard.ngrok.com/get-started/your-authtoken
   ```

3. **复制 Token**
   ```
   您会看到类似这样的 token：
   2abc123def456ghi789jkl_1MnOpQrStUvWxYz2AbCdEfGhIjKlMn
   
   点击 "Copy" 按钮复制到剪贴板
   ```

#### Token 格式说明
```
Ngrok Authtoken 格式：
- 长度：约50-60个字符
- 格式：数字+字母+下划线的组合
- 示例：2abc123def456ghi789jkl_1MnOpQrStUvWxYz2AbCdEfGhIjKlMn
```

### 🚀 在 Google Colab 中配置 Ngrok

#### 方法一：基础配置

```python
# 1. 安装 pyngrok
!pip install pyngrok

# 2. 导入必要的库
from pyngrok import ngrok, conf
import time

# 3. 设置 authtoken（替换为您的实际 token）
ngrok.set_auth_token("您的_Ngrok_Authtoken")

# 4. 创建隧道
public_url = ngrok.connect(8000)
print(f"🌐 公网访问地址: {public_url}")
```

#### 方法二：高级配置

```python
from pyngrok import ngrok, conf
import requests
import time
import json

class NgrokManager:
    def __init__(self, authtoken):
        """初始化 Ngrok 管理器"""
        self.authtoken = authtoken
        self.tunnel = None
        self.public_url = None
        
    def setup(self):
        """设置 Ngrok 配置"""
        try:
            # 设置 authtoken
            ngrok.set_auth_token(self.authtoken)
            print("✅ Ngrok authtoken 设置成功")
            return True
        except Exception as e:
            print(f"❌ Ngrok 设置失败: {e}")
            return False
    
    def create_tunnel(self, port=8000, protocol="http", region="us"):
        """创建隧道"""
        try:
            # 创建隧道
            self.tunnel = ngrok.connect(
                port, 
                proto=protocol,
                region=region  # 可选：us, eu, ap, au, sa, jp, in
            )
            self.public_url = str(self.tunnel).replace("http://", "https://")
            
            print(f"🌐 隧道创建成功!")
            print(f"📡 本地地址: http://localhost:{port}")
            print(f"🌍 公网地址: {self.public_url}")
            
            return self.public_url
        except Exception as e:
            print(f"❌ 隧道创建失败: {e}")
            return None
    
    def check_tunnel_status(self):
        """检查隧道状态"""
        try:
            tunnels = ngrok.get_tunnels()
            if tunnels:
                for tunnel in tunnels:
                    print(f"🔗 隧道信息:")
                    print(f"   公网地址: {tunnel.public_url}")
                    print(f"   本地地址: {tunnel.config['addr']}")
                    print(f"   协议: {tunnel.proto}")
                    print(f"   名称: {tunnel.name}")
                return True
            else:
                print("❌ 没有活跃的隧道")
                return False
        except Exception as e:
            print(f"❌ 检查隧道状态失败: {e}")
            return False
    
    def test_connection(self):
        """测试连接"""
        if not self.public_url:
            print("❌ 没有可用的公网地址")
            return False
            
        try:
            # 测试健康检查端点
            response = requests.get(f"{self.public_url}/health", timeout=10)
            if response.status_code == 200:
                print(f"✅ 连接测试成功! 状态码: {response.status_code}")
                return True
            else:
                print(f"⚠️ 连接测试失败! 状态码: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 连接测试异常: {e}")
            return False
    
    def get_tunnel_info(self):
        """获取隧道详细信息"""
        try:
            # 获取 Ngrok API 信息
            api_url = "http://localhost:4040/api/tunnels"
            response = requests.get(api_url)
            
            if response.status_code == 200:
                data = response.json()
                print("📊 隧道详细信息:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                return data
            else:
                print(f"❌ 无法获取隧道信息: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ 获取隧道信息失败: {e}")
            return None
    
    def close_tunnel(self):
        """关闭隧道"""
        try:
            if self.tunnel:
                ngrok.disconnect(self.tunnel.public_url)
                print("✅ 隧道已关闭")
            
            # 关闭所有隧道
            ngrok.kill()
            print("✅ 所有 Ngrok 进程已终止")
        except Exception as e:
            print(f"❌ 关闭隧道失败: {e}")

# 使用示例
def setup_ngrok_tunnel(authtoken, port=8000):
    """设置 Ngrok 隧道的完整流程"""
    print("🚀 开始设置 Ngrok 隧道...")
    
    # 创建管理器
    ngrok_manager = NgrokManager(authtoken)
    
    # 设置认证
    if not ngrok_manager.setup():
        return None
    
    # 创建隧道
    public_url = ngrok_manager.create_tunnel(port)
    if not public_url:
        return None
    
    # 等待服务启动
    print("⏳ 等待服务启动...")
    time.sleep(5)
    
    # 检查隧道状态
    ngrok_manager.check_tunnel_status()
    
    # 测试连接（可选，需要服务已启动）
    # ngrok_manager.test_connection()
    
    return ngrok_manager

# 完整使用示例
"""
# 替换为您的实际 authtoken
NGROK_AUTHTOKEN = "您的_Ngrok_Authtoken"

# 设置隧道
ngrok_manager = setup_ngrok_tunnel(NGROK_AUTHTOKEN, 8000)

if ngrok_manager:
    print(f"🎉 Ngrok 设置完成! 公网地址: {ngrok_manager.public_url}")
    
    # 在实验结束时关闭隧道
    # ngrok_manager.close_tunnel()
"""
```

### 🔍 隧道验证和监控

#### 验证隧道连接

```python
def verify_ngrok_tunnel(public_url):
    """验证 Ngrok 隧道是否正常工作"""
    import requests
    
    tests = [
        {"name": "基础连接", "url": f"{public_url}"},
        {"name": "健康检查", "url": f"{public_url}/health"},
        {"name": "API文档", "url": f"{public_url}/docs"},
    ]
    
    print("🔍 开始验证隧道连接...")
    
    for test in tests:
        try:
            response = requests.get(test["url"], timeout=10)
            if response.status_code == 200:
                print(f"✅ {test['name']}: 正常 (状态码: {response.status_code})")
            else:
                print(f"⚠️ {test['name']}: 异常 (状态码: {response.status_code})")
        except Exception as e:
            print(f"❌ {test['name']}: 连接失败 - {e}")
    
    print("🔍 验证完成!")
```

#### 监控隧道流量

```python
def monitor_ngrok_traffic():
    """监控 Ngrok 隧道流量"""
    import requests
    import time
    
    api_url = "http://localhost:4040/api/requests/http"
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            requests_data = data.get('requests', [])
            
            print(f"📊 隧道流量统计:")
            print(f"   总请求数: {len(requests_data)}")
            
            if requests_data:
                recent_requests = requests_data[-5:]  # 最近5个请求
                print(f"   最近请求:")
                for req in recent_requests:
                    print(f"     {req.get('method', 'N/A')} {req.get('uri', 'N/A')} - {req.get('status', 'N/A')}")
        else:
            print(f"❌ 无法获取流量信息: {response.status_code}")
    except Exception as e:
        print(f"❌ 监控流量失败: {e}")
```

### ⚙️ 高级配置选项

#### 自定义域名（付费功能）

```python
# 使用自定义子域名（需要付费账户）
tunnel = ngrok.connect(8000, subdomain="my-model-api")
print(f"自定义域名: {tunnel.public_url}")
```

#### 认证保护

```python
# 添加基础认证保护
tunnel = ngrok.connect(8000, auth="username:password")
print(f"受保护的隧道: {tunnel.public_url}")
```

#### 区域选择

```python
# 选择最近的区域以获得更好的延迟
regions = {
    "us": "美国",
    "eu": "欧洲", 
    "ap": "亚太",
    "au": "澳大利亚",
    "sa": "南美",
    "jp": "日本",
    "in": "印度"
}

# 为中国用户推荐使用 ap（亚太）区域
tunnel = ngrok.connect(8000, region="ap")
```

### 🛡️ 安全最佳实践

#### 1. Token 安全

```python
# ❌ 不要在代码中硬编码 token
ngrok.set_auth_token("2abc123def456ghi789jkl_1MnOpQrStUvWxYz2AbCdEfGhIjKlMn")

# ✅ 使用环境变量或安全输入
import os
from getpass import getpass

# 方法1: 环境变量
token = os.getenv('NGROK_AUTHTOKEN')

# 方法2: 安全输入
token = getpass("请输入您的 Ngrok Authtoken: ")

ngrok.set_auth_token(token)
```

#### 2. 访问控制

```python
# 限制访问IP（企业功能）
tunnel = ngrok.connect(8000, allow_cidr="192.168.1.0/24")

# 添加认证
tunnel = ngrok.connect(8000, auth="admin:secure_password")
```

#### 3. 监控和日志

```python
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_tunnel_activity():
    """记录隧道活动"""
    try:
        tunnels = ngrok.get_tunnels()
        for tunnel in tunnels:
            logger.info(f"活跃隧道: {tunnel.public_url} -> {tunnel.config['addr']}")
    except Exception as e:
        logger.error(f"记录隧道活动失败: {e}")
```

### 📊 错误处理和调试

#### 常见错误及解决方案

```python
def handle_ngrok_errors():
    """处理常见的 Ngrok 错误"""
    
    error_solutions = {
        "authtoken": {
            "错误": "invalid authtoken",
            "原因": "Token 无效或过期",
            "解决方案": [
                "1. 检查 token 是否正确复制",
                "2. 确认账户状态正常",
                "3. 重新生成 authtoken"
            ]
        },
        "tunnel_limit": {
            "错误": "tunnel session failed: too many connections",
            "原因": "免费账户隧道数量限制",
            "解决方案": [
                "1. 关闭其他活跃隧道",
                "2. 升级到付费账户",
                "3. 使用 ngrok.kill() 清理"
            ]
        },
        "port_conflict": {
            "错误": "bind: address already in use",
            "原因": "端口被占用",
            "解决方案": [
                "1. 更换端口号",
                "2. 停止占用端口的进程",
                "3. 重启 Colab 运行时"
            ]
        }
    }
    
    print("🔧 Ngrok 常见错误解决方案:")
    for error_type, info in error_solutions.items():
        print(f"\n❌ {info['错误']}")
        print(f"📋 原因: {info['原因']}")
        print("💡 解决方案:")
        for solution in info['解决方案']:
            print(f"   {solution}")
```

#### 调试工具

```python
def debug_ngrok_setup():
    """调试 Ngrok 设置"""
    print("🔍 Ngrok 环境诊断...")
    
    # 检查安装
    try:
        import pyngrok
        print(f"✅ pyngrok 版本: {pyngrok.__version__}")
    except ImportError:
        print("❌ pyngrok 未安装")
        return
    
    # 检查 ngrok 进程
    try:
        tunnels = ngrok.get_tunnels()
        print(f"📊 当前隧道数量: {len(tunnels)}")
        for tunnel in tunnels:
            print(f"   🔗 {tunnel.public_url} -> {tunnel.config['addr']}")
    except Exception as e:
        print(f"❌ 获取隧道信息失败: {e}")
    
    # 检查网络连接
    try:
        import requests
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        print(f"✅ Ngrok API 响应: {response.status_code}")
    except Exception as e:
        print(f"❌ Ngrok API 连接失败: {e}")
```

### 💰 免费账户限制

#### 免费版限制

```
🆓 免费账户限制:
- 同时隧道数: 1个
- 连接数限制: 40连接/分钟
- 隧道超时: 8小时
- 自定义域名: 不支持
- 认证保护: 基础认证
- 流量统计: 基础统计
```

#### 付费版优势

```
💎 付费账户优势:
- 同时隧道数: 3-10个
- 无连接数限制
- 永久隧道
- 自定义域名
- 高级认证
- 详细分析
- 优先支持
```

### 🚀 完整使用示例

```python
# 完整的 Ngrok 集成示例
import asyncio
import uvicorn
from fastapi import FastAPI
from pyngrok import ngrok
import threading
import time

class ModelServer:
    def __init__(self, authtoken):
        self.authtoken = authtoken
        self.app = FastAPI(title="DeepSeek Model API")
        self.ngrok_manager = None
        
    def setup_ngrok(self):
        """设置 Ngrok 隧道"""
        ngrok.set_auth_token(self.authtoken)
        tunnel = ngrok.connect(8000, region="ap")
        self.public_url = str(tunnel).replace("http://", "https://")
        print(f"🌍 模型服务公网地址: {self.public_url}")
        return self.public_url
    
    def setup_routes(self):
        """设置 API 路由"""
        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy", "timestamp": time.time()}
        
        @self.app.post("/generate")
        async def generate_text(request: dict):
            # 这里集成您的模型推理逻辑
            return {"response": "Hello from DeepSeek!"}
    
    def start_server(self):
        """启动服务器"""
        self.setup_routes()
        
        # 在后台线程中启动 FastAPI 服务
        def run_server():
            uvicorn.run(self.app, host="0.0.0.0", port=8000, log_level="info")
        
        server_thread = threading.Thread(target=run_server)
        server_thread.daemon = True
        server_thread.start()
        
        # 等待服务启动
        time.sleep(3)
        
        # 设置 Ngrok 隧道
        public_url = self.setup_ngrok()
        
        return public_url

# 使用示例
"""
# 替换为您的 authtoken
NGROK_AUTHTOKEN = "您的_Ngrok_Authtoken"

# 创建并启动服务
server = ModelServer(NGROK_AUTHTOKEN)
public_url = server.start_server()

print(f"🎉 服务已启动!")
print(f"📡 本地访问: http://localhost:8000")
print(f"🌍 公网访问: {public_url}")
print(f"📖 API文档: {public_url}/docs")
"""
```

### 📚 更多资源

- 📖 [Ngrok 官方文档](https://ngrok.com/docs)
- 🐍 [pyngrok 文档](https://pyngrok.readthedocs.io/)
- 💬 [Ngrok 社区论坛](https://community.ngrok.com/)
- 🎥 [Ngrok 使用教程](https://www.youtube.com/results?search_query=ngrok+tutorial)

---

通过以上详细指南，您应该能够顺利注册 Ngrok 账户、获取 authtoken，并在 Google Colab 中成功配置和使用 Ngrok 隧道服务。

## 📝 许可证

本项目基于 MIT 许可证 - 详情请参阅 LICENSE 文件。

## 🙏 致谢

- [VLLM 项目](https://github.com/vllm-project/vllm)
- [DeepSeek AI](https://github.com/deepseek-ai)
- Google Colab 团队

## 🤝 贡献

欢迎贡献！请随时提交问题和拉取请求。