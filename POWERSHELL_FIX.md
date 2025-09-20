# PowerShell 兼容性修复

## 问题描述

GitHub Actions 在 Windows 环境中使用 PowerShell，但工作流中使用了 Linux/Unix 风格的命令，导致构建失败。

## 错误信息
```
Get-ChildItem: A parameter cannot be found that matches parameter name 'la'.
```

## 修复内容

### 命令替换
- `pwd` → `Get-Location`
- `ls -la` → `Get-ChildItem`
- `echo` → `Write-Host`

### 修复前后对比

#### 修复前 (Linux/Unix 风格):
```bash
pwd
ls -la
echo "Using ScreenCatcher.spec"
```

#### 修复后 (PowerShell 风格):
```powershell
Get-Location
Get-ChildItem
Write-Host "Using ScreenCatcher.spec"
```

## 修复的文件

- `.github/workflows/build-exe.yml`

## 验证

修复后的命令在 Windows PowerShell 中应该能正常工作：
- ✅ `Get-Location` - 显示当前目录
- ✅ `Get-ChildItem` - 列出目录内容
- ✅ `Write-Host` - 输出信息
- ✅ `Test-Path` - 检查文件是否存在

## 测试建议

1. 提交修复后的工作流
2. 推送代码触发构建
3. 检查构建日志确认命令执行成功

## 相关链接

- [PowerShell 命令参考](https://docs.microsoft.com/en-us/powershell/)
- [GitHub Actions Windows 环境](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners#supported-runners-and-hardware-resources)
