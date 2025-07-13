# Ubuntu 22.04.4 配置和运维 Makefile
# 作者: FlyAIBox
# 用途: 简化Ubuntu系统配置操作

.PHONY: help setup check clean install-deps update-system

# 默认目标
help:
	@echo "Ubuntu 22.04.4 配置和运维工具"
	@echo "=================================="
	@echo ""
	@echo "可用命令:"
	@echo "  make setup          - 交互式系统配置"
	@echo "  make setup-full     - 一键完整系统配置"
	@echo "  make check          - 系统健康检查"
	@echo "  make install-deps   - 安装基础依赖"
	@echo "  make update-system  - 更新系统"
	@echo "  make clean          - 清理临时文件"
	@echo "  make help           - 显示此帮助信息"
	@echo ""
	@echo "文档:"
	@echo "  docs/Ubuntu22.04.4-运维配置手册.md - 详细配置手册"
	@echo ""

# 交互式系统配置
setup:
	@echo "🚀 开始交互式系统配置..."
	@chmod +x scripts/ubuntu-quick-setup.sh
	@./scripts/ubuntu-quick-setup.sh

# 一键完整系统配置
setup-full:
	@echo "🚀 开始一键完整系统配置..."
	@chmod +x scripts/ubuntu-quick-setup.sh
	@./scripts/ubuntu-quick-setup.sh --full

# 系统健康检查
check:
	@echo "🔍 开始系统健康检查..."
	@chmod +x scripts/system-check.sh
	@./scripts/system-check.sh

# 安装基础依赖
install-deps:
	@echo "📦 安装基础依赖..."
	@sudo apt update
	@sudo apt install -y curl wget git vim htop tree unzip make

# 更新系统
update-system:
	@echo "🔄 更新系统..."
	@sudo apt update && sudo apt upgrade -y
	@sudo apt autoremove -y
	@sudo apt autoclean

# 清理临时文件
clean:
	@echo "🧹 清理临时文件..."
	@rm -f /tmp/test_io
	@sudo apt autoremove -y
	@sudo apt autoclean
	@echo "清理完成"

# 显示系统信息
info:
	@echo "💻 系统信息:"
	@echo "操作系统: $(shell lsb_release -d | cut -f2)"
	@echo "内核版本: $(shell uname -r)"
	@echo "系统架构: $(shell uname -m)"
	@echo "CPU核心数: $(shell nproc)"
	@echo "内存容量: $(shell free -h | grep Mem | awk '{print $$2}')"
	@echo "磁盘使用: $(shell df -h / | tail -1 | awk '{print $$5}')"

# 快速诊断
diagnose:
	@echo "🔧 快速诊断..."
	@echo "网络连接测试:"
	@ping -c 1 8.8.8.8 > /dev/null 2>&1 && echo "✅ 网络连接正常" || echo "❌ 网络连接异常"
	@echo "DNS解析测试:"
	@nslookup google.com > /dev/null 2>&1 && echo "✅ DNS解析正常" || echo "❌ DNS解析异常"
	@echo "磁盘空间检查:"
	@df -h / | tail -1 | awk '{if($$5+0 < 80) print "✅ 磁盘空间充足 ("$$5")"; else print "⚠️ 磁盘空间紧张 ("$$5")"}' 