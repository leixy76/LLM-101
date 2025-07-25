#!/bin/bash

# AI Travel Planner Development Environment Setup Script
# This script sets up the development environment for the AI Travel Planner project

set -e  # Exit on any error

echo "🚀 Setting up AI Travel Planner development environment..."

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3.10 --version 2>/dev/null || echo "Python 3.10 not found")
if [[ $python_version == *"Python 3.10"* ]]; then
    echo "✅ Python 3.10 found: $python_version"
else
    echo "❌ Python 3.10 is required but not found. Please install Python 3.10."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔧 Creating Python virtual environment..."
    python3.10 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "🔧 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "🔧 Installing Python dependencies..."
pip install -r requirements/dev.txt

# Check Docker
echo "📋 Checking Docker..."
if command -v docker &> /dev/null; then
    echo "✅ Docker found: $(docker --version)"
else
    echo "❌ Docker not found. Please install Docker."
    exit 1
fi

# Check Docker Compose
if command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose found: $(docker-compose --version)"
elif docker compose version &> /dev/null; then
    echo "✅ Docker Compose (plugin) found: $(docker compose version)"
else
    echo "❌ Docker Compose not found. Please install Docker Compose."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "🔧 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your configuration."
else
    echo "✅ .env file already exists"
fi

# Initialize Git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "🔧 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: Project structure and development environment"
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Set up pre-commit hooks
echo "🔧 Setting up pre-commit hooks..."
pre-commit install
echo "✅ Pre-commit hooks installed"

# Create necessary directories
echo "🔧 Creating necessary directories..."
mkdir -p logs data/chroma models checkpoints
echo "✅ Directories created"

# Start development services
echo "🔧 Starting development services..."
docker-compose -f docker/docker-compose.dev.yml up -d postgres redis chromadb n8n

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "📋 Checking service health..."
if docker-compose -f docker/docker-compose.dev.yml ps | grep -q "Up"; then
    echo "✅ Development services are running"
else
    echo "⚠️  Some services may not be running properly. Check with: docker-compose -f docker/docker-compose.dev.yml ps"
fi

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run tests: pytest"
echo "4. Start development server: uvicorn services.api_gateway.main:app --reload"
echo ""
echo "🔗 Service URLs:"
echo "- PostgreSQL: localhost:5432"
echo "- Redis: localhost:6379"
echo "- ChromaDB: http://localhost:8000"
echo "- n8n: http://localhost:5678 (admin/admin)"
echo ""
echo "🛠️  Useful commands:"
echo "- Start services: docker-compose -f docker/docker-compose.dev.yml up -d"
echo "- Stop services: docker-compose -f docker/docker-compose.dev.yml down"
echo "- View logs: docker-compose -f docker/docker-compose.dev.yml logs -f"
echo "- Run tests: pytest"
echo "- Format code: black . && isort ."
echo "- Type check: mypy ."