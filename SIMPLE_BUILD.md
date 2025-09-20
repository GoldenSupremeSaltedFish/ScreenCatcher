# 简化构建说明

## 概述

工作流已简化为只生成 exe 文件，移除了不必要的打包步骤。

## 构建产物

- **ScreenCatcher.exe** - 独立可执行文件
  - 无需安装
  - 包含所有依赖
  - 直接运行

## GitHub Actions 工作流

### 触发条件
- 推送到 `main`/`master` 分支
- 创建标签 (如 `v1.0.0`)
- 发布 Release

### 构建步骤
1. 安装 Python 3.12
2. 安装依赖 (PyInstaller, Pillow, PyZBar)
3. 安装 Visual C++ Redistributable
4. 构建 exe 文件
5. 上传到 Artifacts
6. 发布到 GitHub Releases (仅标签触发)

## 本地构建

### 快速构建
```bash
python build_local.py
```

### 手动构建
```bash
# 安装依赖
pip install pyinstaller pillow pyzbar

# 构建
pyinstaller --clean ScreenCatcher.spec
# 或
pyinstaller --onefile --windowed --name ScreenCatcher src/screencatcher/ScreenCatcher.py
```

## 文件结构

```
dist/
└── ScreenCatcher.exe    # 最终的可执行文件
```

## 使用说明

1. 下载 `ScreenCatcher.exe`
2. 双击运行
3. 使用 `Alt+Q` 截图识别二维码
4. 按 `Esc` 退出

## 优势

- ✅ 简化构建流程
- ✅ 减少构建时间
- ✅ 单一文件分发
- ✅ 无需解压安装
- ✅ 更小的存储占用
