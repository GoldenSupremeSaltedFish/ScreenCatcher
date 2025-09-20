#!/usr/bin/env python3
"""
本地构建脚本 - 用于测试 PyInstaller 打包
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """运行命令并处理错误"""
    print(f"\n🔄 {description}...")
    print(f"执行命令: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 成功")
        if result.stdout:
            print(f"输出: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败")
        print(f"错误: {e.stderr}")
        return False

def main():
    """主函数"""
    print("🚀 开始本地构建 ScreenCatcher...")
    
    # 检查 Python 版本
    if sys.version_info < (3, 8):
        print("❌ 需要 Python 3.8 或更高版本")
        return False
    
    print(f"✅ Python 版本: {sys.version}")
    
    # 安装依赖
    if not run_command("pip install pyinstaller pillow pyzbar", "安装构建依赖"):
        return False
    
    # 清理之前的构建
    if os.path.exists("dist"):
        print("🧹 清理之前的构建文件...")
        shutil.rmtree("dist")
    
    if os.path.exists("build"):
        print("🧹 清理之前的构建文件...")
        shutil.rmtree("build")
    
    # 构建可执行文件 - 尝试不同的方法
    build_success = False
    
    # 方法1: 使用 .spec 文件
    if os.path.exists("ScreenCatcher.spec"):
        print("🔧 使用 ScreenCatcher.spec 文件构建...")
        build_success = run_command("pyinstaller --clean ScreenCatcher.spec", "构建可执行文件")
    elif os.path.exists("ScreenCatcher-simple.spec"):
        print("🔧 使用 ScreenCatcher-simple.spec 文件构建...")
        build_success = run_command("pyinstaller --clean ScreenCatcher-simple.spec", "构建可执行文件")
    
    # 方法2: 使用命令行参数
    if not build_success:
        print("🔧 使用命令行参数构建...")
        build_success = run_command(
            "pyinstaller --onefile --windowed --name ScreenCatcher --clean src/screencatcher/ScreenCatcher.py",
            "构建可执行文件"
        )
    
    if not build_success:
        return False
    
    # 检查构建结果
    exe_path = Path("dist/ScreenCatcher.exe")
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✅ 构建成功!")
        print(f"📁 可执行文件位置: {exe_path.absolute()}")
        print(f"📊 文件大小: {size_mb:.1f} MB")
        return True
    else:
        print("❌ 构建失败 - 未找到可执行文件")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 构建完成! 你可以运行 dist/ScreenCatcher.exe 来测试应用。")
    else:
        print("\n💥 构建失败! 请检查错误信息。")
        sys.exit(1)
