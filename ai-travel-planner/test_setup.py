#!/usr/bin/env python3
"""
Simple test script to verify the project setup is working correctly.
This script tests the basic project structure and dependencies.
"""

import sys
import os
import subprocess
from pathlib import Path

def test_python_version():
    """Test that Python 3.10 is being used."""
    version = sys.version_info
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    assert version.major == 3 and version.minor == 10, f"Expected Python 3.10, got {version.major}.{version.minor}"

def test_project_structure():
    """Test that all required directories exist."""
    required_dirs = [
        "services/agent-service",
        "services/api-gateway", 
        "services/chat-service",
        "services/rag-service",
        "services/vllm-service",
        "services/workflow-service",
        "shared/config",
        "shared/models",
        "shared/utils",
        "docker",
        "requirements",
        "scripts",
        "tests"
    ]
    
    for dir_path in required_dirs:
        path = Path(dir_path)
        assert path.exists() and path.is_dir(), f"Directory {dir_path} does not exist"
        print(f"✓ Directory exists: {dir_path}")

def test_required_files():
    """Test that all required files exist."""
    required_files = [
        "pyproject.toml",
        ".env.example",
        ".gitignore",
        "Makefile",
        "README.md",
        "requirements/base.txt",
        "requirements/dev.txt",
        "requirements/vllm.txt",
        "scripts/setup-dev.sh",
        "docker/docker-compose.dev.yml"
    ]
    
    for file_path in required_files:
        path = Path(file_path)
        assert path.exists() and path.is_file(), f"File {file_path} does not exist"
        print(f"✓ File exists: {file_path}")

def test_init_files():
    """Test that all service directories have __init__.py files."""
    service_dirs = [
        "services/agent-service",
        "services/api-gateway",
        "services/chat-service", 
        "services/rag-service",
        "services/vllm-service",
        "services/workflow-service",
        "shared/config",
        "shared/models",
        "shared/utils"
    ]
    
    for dir_path in service_dirs:
        init_file = Path(dir_path) / "__init__.py"
        assert init_file.exists(), f"__init__.py missing in {dir_path}"
        print(f"✓ __init__.py exists in: {dir_path}")

def main():
    """Run all tests."""
    print("🧪 Testing AI Travel Planner project setup...")
    print()
    
    try:
        test_python_version()
        print()
        
        test_project_structure()
        print()
        
        test_required_files()
        print()
        
  