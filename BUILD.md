# ScreenCatcher 构建说明

## 自动构建 (GitHub Actions)

项目已配置 GitHub Actions 工作流，会在以下情况下自动构建：

- 推送到 `main` 或 `master` 分支
- 创建标签 (如 `v1.0.0`)
- 发布 Release

### 构建产物

每次构建会生成：
- `ScreenCatcher.exe` - 独立可执行文件
- `ScreenCatcher-Portable.zip` - 便携版压缩包

## 本地构建

### 环境要求

- Python 3.8+
- Windows 10/11
- 足够的磁盘空间 (至少 1GB)

### 快速构建

```bash
# 运行自动构建脚本
python build_local.py
```

### 手动构建

```bash
# 1. 安装依赖
pip install pyinstaller pillow pyzbar

# 2. 构建可执行文件
pyinstaller --clean ScreenCatcher.spec

# 3. 检查结果
ls dist/ScreenCatcher.exe
```

## 构建配置

### PyInstaller 配置 (.spec 文件)

主要配置项：
- `--onefile`: 打包为单个可执行文件
- `--windowed`: GUI 应用，不显示控制台
- `--upx`: 启用 UPX 压缩
- `excludes`: 排除不需要的模块

### 体积优化

已排除的大型依赖：
- `opencv-python` (~100-200MB)
- `numpy` (~20-30MB)
- `matplotlib`, `pandas`, `seaborn` 等

### 包含的依赖

- `pillow` - 图像处理
- `pyzbar` - 二维码识别
- `keyboard` - 快捷键监听
- `pywin32` - Windows API

## 故障排除

### 常见问题

1. **pyzbar 相关错误**
   ```
   解决方案: 确保安装了 Visual C++ Redistributable
   ```

2. **模块导入错误**
   ```
   解决方案: 检查 hiddenimports 配置
   ```

3. **文件过大**
   ```
   解决方案: 检查 excludes 列表，移除不必要的模块
   ```

### 调试模式

```bash
# 启用控制台输出进行调试
pyinstaller --console ScreenCatcher.spec
```

## 发布流程

1. 更新版本号
2. 提交代码
3. 创建标签: `git tag v1.0.0`
4. 推送标签: `git push origin v1.0.0`
5. GitHub Actions 自动构建并发布 Release

## 文件结构

```
ScreenCatcher/
├── .github/workflows/
│   └── build-exe.yml          # GitHub Actions 工作流
├── src/screencatcher/
│   ├── ScreenCatcher.py       # 主程序
│   └── ScreenShot.py          # 截图模块
├── assets/                    # 资源文件
├── ScreenCatcher.spec         # PyInstaller 配置
├── build_local.py             # 本地构建脚本
└── BUILD.md                   # 构建说明
```
