#!/bin/bash

# 飞书消息自动翻译系统启动脚本
# 适用于Ubuntu 22.04.4
# 作者: AI Assistant
# 描述: 一键启动n8n和相关服务

set -e  # 如果任何命令失败，脚本将退出

echo "🚀 飞书消息自动翻译系统启动脚本"
echo "======================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查系统要求
check_requirements() {
    log_info "检查系统要求..."
    
    # 检查操作系统
    if [[ ! -f /etc/os-release ]]; then
        log_error "无法检测操作系统版本"
        exit 1
    fi
    
    source /etc/os-release
    if [[ "$ID" != "ubuntu" ]] || [[ ! "$VERSION_ID" =~ ^22\.04 ]]; then
        log_warning "建议使用Ubuntu 22.04，当前系统: $PRETTY_NAME"
    fi
    
    # 检查Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker未安装，请先安装Docker"
        log_info "安装命令: curl -fsSL https://get.docker.com | sh"
        exit 1
    fi
    
    # 检查Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose未安装，请先安装Docker Compose"
        log_info "安装命令: sudo apt install docker-compose-plugin"
        exit 1
    fi
    
    # 检查Docker服务状态
    if ! systemctl is-active --quiet docker; then
        log_warning "Docker服务未运行，正在启动..."
        sudo systemctl start docker
        sudo systemctl enable docker
    fi
    
    log_success "系统要求检查通过"
}

# 创建必要的目录
create_directories() {
    log_info "创建必要的目录..."
    
    # 创建工作流目录
    mkdir -p workflows
    mkdir -p custom-nodes
    mkdir -p logs
    
    # 设置权限
    chmod 755 workflows custom-nodes logs
    
    log_success "目录创建完成"
}

# 检查配置文件
check_config() {
    log_info "检查配置文件..."
    
    # 检查docker-compose.yml
    if [[ ! -f "docker-compose.yml" ]]; then
        log_error "docker-compose.yml文件不存在"
        exit 1
    fi
    
    # 检查工作流文件
    if [[ ! -f "workflows/feishu_translator_workflow.json" ]]; then
        log_warning "工作流配置文件不存在，将在n8n中手动创建"
    fi
    
    log_success "配置文件检查完成"
}

# 配置环境变量
setup_environment() {
    log_info "设置环境变量..."
    
    # 创建.env文件（如果不存在）
    if [[ ! -f ".env" ]]; then
        cat > .env << EOF
# n8n基础配置
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=password123

# 加密密钥（请修改为随机字符串）
N8N_ENCRYPTION_KEY=$(openssl rand -hex 32)

# 数据库配置
POSTGRES_DB=n8n
POSTGRES_USER=n8n_user
POSTGRES_PASSWORD=$(openssl rand -base64 32)

# Redis配置
REDIS_PASSWORD=$(openssl rand -base64 32)

# 网络配置
WEBHOOK_URL=http://localhost:5678

# 日志配置
N8N_LOG_LEVEL=info
EOF
        log_success "环境配置文件已创建: .env"
        log_warning "请根据需要修改.env文件中的配置"
    else
        log_info "使用现有的环境配置文件"
    fi
}

# 启动服务
start_services() {
    log_info "启动Docker服务..."
    
    # 拉取最新镜像
    log_info "拉取最新的Docker镜像..."
    docker-compose pull
    
    # 启动服务
    log_info "启动所有服务..."
    docker-compose up -d
    
    # 等待服务启动
    log_info "等待服务启动..."
    sleep 10
    
    # 检查服务状态
    check_services_health
}

# 检查服务健康状态
check_services_health() {
    log_info "检查服务健康状态..."
    
    # 检查n8n服务
    if docker-compose ps n8n | grep -q "Up"; then
        log_success "n8n服务运行正常"
    else
        log_error "n8n服务启动失败"
        docker-compose logs n8n
        exit 1
    fi
    
    # 检查PostgreSQL服务
    if docker-compose ps postgres | grep -q "Up"; then
        log_success "PostgreSQL服务运行正常"
    else
        log_warning "PostgreSQL服务可能未启动"
    fi
    
    # 检查Redis服务
    if docker-compose ps redis | grep -q "Up"; then
        log_success "Redis服务运行正常"
    else
        log_warning "Redis服务可能未启动"
    fi
}

# 显示访问信息
show_access_info() {
    log_info "服务访问信息"
    echo "======================================"
    
    # 获取本机IP
    LOCAL_IP=$(hostname -I | awk '{print $1}')
    
    echo -e "${GREEN}🎉 服务启动成功！${NC}"
    echo ""
    echo "📋 访问地址:"
    echo "  🌐 n8n Web界面: http://localhost:5678"
    echo "  🌐 n8n Web界面(外网): http://${LOCAL_IP}:5678"
    echo ""
    echo "🔐 登录信息:"
    echo "  👤 用户名: admin"
    echo "  🔑 密码: password123"
    echo ""
    echo "🔗 数据库连接:"
    echo "  📊 PostgreSQL: localhost:5432"
    echo "  🗄️  Redis: localhost:6379"
    echo ""
    echo "📁 重要目录:"
    echo "  📂 工作流: ./workflows/"
    echo "  📂 日志: ./logs/"
    echo "  📂 数据: Docker volumes"
    echo ""
    echo "🛠️  管理命令:"
    echo "  🔍 查看日志: docker-compose logs -f"
    echo "  ⏸️  停止服务: docker-compose down"
    echo "  🔄 重启服务: docker-compose restart"
    echo "  🗑️  清理数据: docker-compose down -v"
    echo ""
    
    log_warning "请确保防火墙允许5678端口访问"
    log_info "初次访问n8n时，请使用上述登录信息"
}

# 显示下一步操作
show_next_steps() {
    echo ""
    log_info "下一步操作指南"
    echo "======================================"
    echo "1. 🌐 打开浏览器访问 http://localhost:5678"
    echo "2. 🔐 使用 admin/password123 登录n8n"
    echo "3. 📥 导入工作流配置文件 workflows/feishu_translator_workflow.json"
    echo "4. 🔧 配置翻译API地址（ngrok URL）"
    echo "5. 🤖 设置飞书机器人webhook地址"
    echo "6. ✅ 测试翻译功能"
    echo ""
    echo "📖 详细说明请查看README.md文件"
    echo ""
}

# 主函数
main() {
    echo ""
    log_info "开始启动飞书消息自动翻译系统..."
    echo ""
    
    # 执行启动流程
    check_requirements
    create_directories
    check_config
    setup_environment
    start_services
    show_access_info
    show_next_steps
    
    log_success "系统启动完成！"
}

# 错误处理函数
cleanup() {
    log_error "脚本执行过程中发生错误"
    log_info "正在清理..."
    
    # 如果服务已启动，尝试停止
    if docker-compose ps | grep -q "Up"; then
        log_info "停止已启动的服务..."
        docker-compose down
    fi
    
    exit 1
}

# 设置错误捕获
trap cleanup ERR

# 检查是否以root身份运行
if [[ $EUID -eq 0 ]]; then
    log_warning "不建议以root身份运行此脚本"
    read -p "确定要继续吗？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "脚本已取消"
        exit 1
    fi
fi

# 运行主函数
main

echo ""
log_success "�� 欢迎使用飞书消息自动翻译系统！" 