#!/usr/bin/env python3
"""
Artifactory 上传脚本
用于手动上传 exe 文件到 Artifactory
"""

import os
import sys
import requests
import base64
from pathlib import Path

def upload_to_artifactory(file_path, artifactory_url, username, password, repository="generic-local", version="latest"):
    """
    上传文件到 Artifactory
    
    Args:
        file_path: 要上传的文件路径
        artifactory_url: Artifactory URL
        username: 用户名
        password: 密码或 API Key
        repository: 仓库名称
        version: 版本号
    """
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 构建上传 URL
    filename = os.path.basename(file_path)
    upload_url = f"{artifactory_url}/{repository}/ScreenCatcher/{version}/{filename}"
    
    # 设置认证头
    auth_string = f"{username}:{password}"
    auth_bytes = auth_string.encode('ascii')
    auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
    headers = {
        'Authorization': f'Basic {auth_b64}',
        'Content-Type': 'application/octet-stream'
    }
    
    try:
        print(f"📤 上传文件到 Artifactory...")
        print(f"   文件: {file_path}")
        print(f"   URL: {upload_url}")
        
        with open(file_path, 'rb') as f:
            response = requests.put(upload_url, data=f, headers=headers)
        
        if response.status_code in [200, 201]:
            print(f"✅ 上传成功!")
            print(f"   状态码: {response.status_code}")
            print(f"   文件大小: {os.path.getsize(file_path) / (1024*1024):.1f} MB")
            return True
        else:
            print(f"❌ 上传失败!")
            print(f"   状态码: {response.status_code}")
            print(f"   响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 上传异常: {e}")
        return False

def main():
    """主函数"""
    print("🚀 Artifactory 上传工具")
    
    # 检查环境变量
    artifactory_url = os.getenv('ARTIFACTORY_URL')
    username = os.getenv('ARTIFACTORY_USER')
    password = os.getenv('ARTIFACTORY_PASSWORD')
    repository = os.getenv('ARTIFACTORY_REPOSITORY', 'generic-local')
    version = os.getenv('VERSION', 'latest')
    
    if not all([artifactory_url, username, password]):
        print("❌ 缺少必需的环境变量:")
        print("   ARTIFACTORY_URL")
        print("   ARTIFACTORY_USER") 
        print("   ARTIFACTORY_PASSWORD")
        print("\n💡 设置环境变量后重试:")
        print("   set ARTIFACTORY_URL=https://your-artifactory.com/artifactory")
        print("   set ARTIFACTORY_USER=your-username")
        print("   set ARTIFACTORY_PASSWORD=your-password")
        return False
    
    # 查找 exe 文件
    exe_path = Path("dist/ScreenCatcher.exe")
    if not exe_path.exists():
        print(f"❌ 找不到可执行文件: {exe_path}")
        print("💡 请先运行构建脚本生成 exe 文件")
        return False
    
    # 上传文件
    success = upload_to_artifactory(
        str(exe_path),
        artifactory_url,
        username,
        password,
        repository,
        version
    )
    
    if success:
        print(f"\n🎉 上传完成!")
        print(f"   仓库: {repository}")
        print(f"   版本: {version}")
    else:
        print(f"\n💥 上传失败!")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
