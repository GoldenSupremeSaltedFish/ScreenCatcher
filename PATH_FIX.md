# 路径和可移植性修复说明

## 问题分析

### 原始问题
1. **GitHub Actions 路径问题**: `.spec` 文件找不到
2. **代码可移植性差**: 硬编码的 win32 导入
3. **构建失败**: 路径配置不正确

### 根本原因
- 相对路径在不同环境中表现不一致
- 缺少错误处理和回退机制
- 依赖特定平台的模块

## 修复方案

### 1. 路径问题修复

#### 创建了多个 .spec 文件选项:
- `ScreenCatcher.spec` - 增强版，带路径检测
- `ScreenCatcher-simple.spec` - 简化版，避免复杂路径

#### 工作流智能选择:
```powershell
if (Test-Path "ScreenCatcher.spec") {
  pyinstaller --clean ScreenCatcher.spec
} elseif (Test-Path "ScreenCatcher-simple.spec") {
  pyinstaller --clean ScreenCatcher-simple.spec
} else {
  pyinstaller --onefile --windowed --name ScreenCatcher --clean src/screencatcher/ScreenCatcher.py
}
```

### 2. 可移植性改进

#### Win32 模块导入优化:
```python
try:
    import win32gui
    import win32print
    import win32con
    from win32api import GetSystemMetrics
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    print("Warning: win32 modules not available. Some features may not work.")
```

#### 回退机制:
- 如果 win32 不可用，使用 tkinter 作为回退
- 确保在不同环境中都能运行

### 3. 构建脚本改进

#### 本地构建脚本 (`build_local.py`):
- 自动检测可用的 .spec 文件
- 多种构建方法回退
- 更好的错误处理

## 修复的文件

1. **`.github/workflows/build-exe.yml`**
   - 添加路径检测和调试信息
   - 多种构建方法回退

2. **`ScreenCatcher.spec`**
   - 增强的路径处理
   - 更健壮的文件检测

3. **`ScreenCatcher-simple.spec`**
   - 简化的配置
   - 避免复杂路径问题

4. **`src/screencatcher/ScreenShot.py`**
   - 可选的 win32 导入
   - tkinter 回退机制

5. **`build_local.py`**
   - 多种构建方法
   - 更好的错误处理

## 测试建议

### 本地测试:
```bash
python build_local.py
```

### GitHub Actions 测试:
1. 提交所有修复
2. 推送代码触发工作流
3. 检查构建日志

### 验证步骤:
1. 检查 `.spec` 文件是否被找到
2. 验证构建是否成功
3. 测试生成的 exe 文件

## 预期结果

- ✅ GitHub Actions 构建成功
- ✅ 路径问题解决
- ✅ 代码更具可移植性
- ✅ 多种构建方法回退
- ✅ 更好的错误处理

## 后续优化建议

1. **添加图标支持**
2. **版本信息嵌入**
3. **数字签名** (可选)
4. **自动更新机制** (可选)
