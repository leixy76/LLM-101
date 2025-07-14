# 飞书消息自动翻译系统使用指南

本文档提供完整的使用指南，帮助初学者快速上手。

## 📋 目录

1. [环境准备](#环境准备)
2. [部署n8n服务](#部署n8n服务)
3. [配置翻译API](#配置翻译api)
4. [设置飞书机器人](#设置飞书机器人)
5. [配置n8n工作流](#配置n8n工作流)
6. [测试和调试](#测试和调试)
7. [常见问题](#常见问题)

## 🛠️ 环境准备

### 1. 系统要求

- **操作系统**: Ubuntu 22.04.4 LTS
- **内存**: 至少4GB RAM
- **存储**: 至少10GB可用空间
- **网络**: 稳定的互联网连接

### 2. 安装Docker

```bash
# 更新系统包
sudo apt update && sudo apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com | sh

# 添加用户到docker组
sudo usermod -aG docker $USER

# 重启或重新登录以应用组更改
newgrp docker

# 验证安装
docker --version
docker-compose --version
```

### 3. 安装Python环境

```bash
# 安装Python和pip
sudo apt install python3 python3-pip -y

# 安装Jupyter Notebook (用于运行翻译API)
pip3 install jupyter notebook
```

## 🚀 部署n8n服务

### 1. 使用一键启动脚本

```bash
cd chapter07-llm-n8n
./start.sh
```

启动脚本会自动完成以下操作：
- ✅ 检查系统要求
- ✅ 创建必要目录
- ✅ 生成环境配置
- ✅ 启动Docker服务
- ✅ 显示访问信息

### 2. 手动启动（可选）

如果一键启动失败，可以手动启动：

```bash
# 1. 复制环境配置
cp env.example .env

# 2. 编辑配置文件
nano .env
# 修改密码和密钥

# 3. 启动服务
docker-compose up -d

# 4. 查看服务状态
docker-compose ps

# 5. 查看日志
docker-compose logs -f n8n
```

### 3. 访问n8n界面

启动成功后，访问：
- **本地地址**: http://localhost:5678
- **用户名**: admin
- **密码**: password123

## 🔧 配置翻译API

### 1. 获取ngrok Token

1. 访问 https://ngrok.com
2. 注册免费账号
3. 登录后在Dashboard获取Authtoken
4. 复制token备用

### 2. 运行翻译API

#### 方式一: Google Colab (推荐)

1. **上传Notebook**
   - 打开 Google Colab
   - 上传 `feishu_translator.ipynb`

2. **配置Token**
   ```python
   # 在第3个代码单元中修改
   NGROK_TOKEN = "your_actual_ngrok_token_here"
   ```

3. **运行所有单元**
   - 依次运行所有代码单元
   - 等待模型下载完成
   - 记录生成的ngrok URL

#### 方式二: 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 启动Jupyter
jupyter notebook

# 在浏览器中打开 feishu_translator.ipynb
# 配置ngrok token并运行所有单元
```

### 3. 获取API地址

运行成功后，会显示类似信息：
```
🌍 公网地址: https://abc123.ngrok.io
🔧 在n8n中使用以下URL:
   https://abc123.ngrok.io/feishu/translate
```

**重要**: 保存这个URL，稍后在n8n中需要使用。

## 🤖 设置飞书机器人

### 1. 创建飞书应用

1. **登录飞书开放平台**
   - 访问 https://open.feishu.cn/
   - 使用飞书账号登录

2. **创建应用**
   - 点击"创建应用"
   - 选择"机器人"类型
   - 填写应用信息

3. **获取凭证**
   - 记录 App ID
   - 记录 App Secret

### 2. 配置机器人权限

在飞书开放平台中：

1. **添加权限**
   - `im:message` - 接收和发送消息
   - `im:message:send_as_bot` - 以机器人身份发送消息

2. **发布版本**
   - 点击"创建版本"
   - 等待审核通过

### 3. 配置事件订阅

1. **设置请求URL**
   ```
   https://your-ngrok-url.ngrok.io/webhook/feishu-webhook
   ```

2. **订阅事件**
   - `接收消息` - im.message.receive_v1

3. **获取Bot Token**
   - 在"凭证与基础信息"中获取
   - 格式: `t-xxx`

## ⚡ 配置n8n工作流

### 1. 导入工作流

1. **打开n8n界面**
   - 访问 http://localhost:5678
   - 使用admin/password123登录

2. **导入配置**
   - 点击右上角"+"
   - 选择"Import from file"
   - 上传 `workflows/feishu_translator_workflow.json`

### 2. 配置节点

#### 2.1 配置翻译API节点

1. **找到"调用翻译API"节点**
2. **更新URL**
   ```
   https://your-ngrok-url.ngrok.io/feishu/translate
   ```
3. **保存配置**

#### 2.2 配置飞书API节点

1. **找到"发送回复到飞书"节点**
2. **设置Headers**
   ```
   Authorization: Bearer YOUR_FEISHU_BOT_TOKEN
   Content-Type: application/json
   ```
3. **保存配置**

### 3. 激活工作流

1. **保存工作流**
   - 按Ctrl+S或点击保存按钮

2. **激活工作流**
   - 点击右上角的开关，变为绿色

3. **获取Webhook URL**
   - 点击"飞书Webhook接收器"节点
   - 复制Production URL
   - 格式: `http://localhost:5678/webhook/feishu-webhook`

### 4. 更新飞书事件订阅

在飞书开放平台中：
1. 将Webhook URL更新为n8n提供的地址
2. 保存配置

## 🧪 测试和调试

### 1. 测试翻译API

在Google Colab或本地运行测试单元：

```python
# 测试中文翻译
response = requests.post(
    f"{base_url}/translate",
    json={"text": "你好世界"}
)
print(response.json())

# 测试英文翻译
response = requests.post(
    f"{base_url}/translate", 
    json={"text": "Hello world"}
)
print(response.json())
```

### 2. 测试n8n工作流

1. **手动触发测试**
   - 在n8n中点击"Test workflow"
   - 发送测试数据

2. **查看执行历史**
   - 在n8n中查看"Executions"
   - 检查每个节点的输入输出

### 3. 测试飞书机器人

1. **邀请机器人到群聊**
2. **发送测试消息**
   ```
   @机器人 你好世界
   Hello, how are you?
   ```
3. **检查回复**
   - 应该收到翻译结果
   - 格式: 原文 + 译文

## 🐛 常见问题

### 1. Docker相关问题

**问题**: Docker服务启动失败
```bash
# 解决方案
sudo systemctl start docker
sudo systemctl enable docker
```

**问题**: 权限不够
```bash
# 解决方案
sudo usermod -aG docker $USER
newgrp docker
```

### 2. n8n访问问题

**问题**: 无法访问n8n界面
- 检查端口5678是否被占用
- 检查防火墙设置
- 查看容器日志: `docker-compose logs n8n`

**问题**: 登录失败
- 确认用户名密码正确
- 检查.env文件配置

### 3. 翻译API问题

**问题**: ngrok连接失败
- 检查token是否正确
- 确认网络连接正常
- 尝试重新启动服务

**问题**: 模型加载失败
- 检查网络连接
- 尝试重新运行代码单元
- 检查磁盘空间

### 4. 飞书集成问题

**问题**: 机器人收不到消息
- 检查事件订阅配置
- 确认Webhook URL正确
- 检查机器人权限

**问题**: 无法发送回复
- 检查Bot Token是否正确
- 确认机器人有发送消息权限
- 查看n8n执行日志

### 5. 工作流调试

**问题**: 工作流执行失败
1. **查看执行历史**
   - 在n8n中点击"Executions"
   - 找到失败的执行

2. **检查错误信息**
   - 点击失败的节点
   - 查看错误详情

3. **常见错误**
   - API地址错误: 检查URL配置
   - 认证失败: 检查Token配置
   - 超时错误: 增加超时时间

## 📊 监控和维护

### 1. 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f n8n
docker-compose logs -f postgres
docker-compose logs -f redis
```

### 2. 性能监控

```bash
# 查看资源使用
docker stats

# 查看磁盘使用
docker system df

# 清理未使用的镜像
docker system prune
```

### 3. 数据备份

```bash
# 备份数据库
docker-compose exec postgres pg_dump -U n8n_user n8n > backup.sql

# 备份n8n配置
docker cp n8n_feishu_translator:/home/node/.n8n ./n8n_backup
```

### 4. 更新服务

```bash
# 更新镜像
docker-compose pull

# 重启服务
docker-compose down
docker-compose up -d
```

## 🎯 最佳实践

### 1. 安全配置

- 修改默认密码
- 使用强加密密钥
- 定期更新组件
- 监控异常访问

### 2. 性能优化

- 启用Redis缓存
- 合理设置资源限制
- 监控内存使用
- 定期清理日志

### 3. 故障恢复

- 定期备份数据
- 准备恢复流程
- 监控服务状态
- 设置告警机制

## 📞 获取帮助

如果遇到问题：

1. **查看日志**: 首先检查相关服务的日志
2. **参考文档**: 查看项目README和USAGE文档  
3. **测试隔离**: 分别测试各个组件
4. **社区支持**: 在GitHub Issues中提问

---

**祝你使用愉快！** 🎉 