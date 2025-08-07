#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
华巡网络设备巡检系统 - 重构版本验证脚本
验证新的代码结构是否正确
"""

import os
import sys
import importlib.util

def check_file_exists(filepath, description=""):
    """检查文件是否存在"""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description}: {filepath} (不存在)")
        return False

def check_python_syntax(filepath):
    """检查Python文件语法"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            compile(f.read(), filepath, 'exec')
        return True
    except SyntaxError as e:
        print(f"✗ 语法错误 {filepath}: {e}")
        return False
    except Exception as e:
        print(f"✗ 检查错误 {filepath}: {e}")
        return False

def main():
    print("=" * 60)
    print("华巡网络设备巡检系统 - 重构版本结构验证")
    print("=" * 60)
    
    # 检查主要目录结构
    print("\n📁 检查目录结构:")
    directories = [
        "backend",
        "backend/config",
        "backend/models",
        "backend/routes",
        "backend/services",
        "backend/utils",
        "frontend_new",
        "frontend_new/assets",
        "frontend_new/assets/css",
        "frontend_new/assets/js",
        "frontend_new/services",
        "frontend_new/utils"
    ]
    
    dir_check_passed = True
    for directory in directories:
        if check_file_exists(directory, f"目录"):
            pass
        else:
            dir_check_passed = False
    
    # 检查关键文件
    print("\n📄 检查关键文件:")
    files = [
        ("app_new.py", "新主应用文件"),
        ("start_new.bat", "新启动脚本"),
        ("README_REFACTORED.md", "重构版README"),
        ("backend/config/settings.py", "配置文件"),
        ("backend/models/base.py", "基础模型"),
        ("backend/models/device.py", "设备模型"),
        ("backend/models/inspection_record.py", "巡检记录模型"),
        ("backend/models/inspection_log.py", "巡检日志模型"),
        ("backend/routes/device_routes.py", "设备路由"),
        ("backend/routes/inspection_routes.py", "巡检路由"),
        ("backend/routes/record_routes.py", "记录路由"),
        ("backend/services/device_service.py", "设备服务"),
        ("backend/services/inspection_service.py", "巡检服务"),
        ("backend/utils/device_utils.py", "设备工具"),
        ("backend/utils/export_utils.py", "导出工具"),
        ("backend/utils/validation.py", "验证工具"),
        ("frontend_new/index.html", "前端主页面"),
        ("frontend_new/assets/css/main.css", "主样式文件"),
        ("frontend_new/assets/js/app.js", "主应用JS"),
        ("frontend_new/services/api.js", "API服务"),
        ("frontend_new/services/device-service.js", "设备服务JS"),
        ("frontend_new/utils/datetime.js", "时间工具"),
        ("frontend_new/utils/validation.js", "验证工具JS")
    ]
    
    file_check_passed = True
    for filepath, description in files:
        if not check_file_exists(filepath, description):
            file_check_passed = False
    
    # 检查Python文件语法
    print("\n🐍 检查Python文件语法:")
    python_files = [
        "app_new.py",
        "backend/config/settings.py",
        "backend/models/base.py",
        "backend/models/device.py",
        "backend/models/inspection_record.py",
        "backend/models/inspection_log.py",
        "backend/routes/device_routes.py",
        "backend/routes/inspection_routes.py",
        "backend/routes/record_routes.py",
        "backend/services/device_service.py",
        "backend/services/inspection_service.py",
        "backend/services/import_service.py",
        "backend/utils/device_utils.py",
        "backend/utils/export_utils.py",
        "backend/utils/validation.py"
    ]
    
    syntax_check_passed = True
    for filepath in python_files:
        if os.path.exists(filepath):
            if check_python_syntax(filepath):
                print(f"✓ 语法检查通过: {filepath}")
            else:
                syntax_check_passed = False
        else:
            print(f"✗ 文件不存在: {filepath}")
            syntax_check_passed = False
    
    # 统计文件大小对比
    print("\n📊 文件大小统计:")
    original_files = {
        "app.py": "原始主文件",
        "frontend/index.html": "原始前端文件"
    }
    
    for filepath, description in original_files.items():
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"  {description}: {size:,} 字节")
    
    # 计算新结构的总文件数
    new_files_count = 0
    total_new_size = 0
    for filepath, _ in files:
        if os.path.exists(filepath):
            new_files_count += 1
            total_new_size += os.path.getsize(filepath)
    
    print(f"  重构版文件数量: {new_files_count} 个")
    print(f"  重构版总大小: {total_new_size:,} 字节")
    
    # 输出结果
    print("\n" + "=" * 60)
    print("验证结果:")
    print("=" * 60)
    
    if dir_check_passed and file_check_passed and syntax_check_passed:
        print("🎉 恭喜！重构版本结构验证通过！")
        print("✓ 目录结构正确")
        print("✓ 关键文件存在")
        print("✓ Python语法正确")
        print("\n可以尝试运行以下命令启动系统:")
        print("  python3 app_new.py")
        print("  或者运行 start_new.bat (Windows)")
        return True
    else:
        print("❌ 验证失败，存在以下问题:")
        if not dir_check_passed:
            print("✗ 目录结构不完整")
        if not file_check_passed:
            print("✗ 关键文件缺失")
        if not syntax_check_passed:
            print("✗ Python语法错误")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)