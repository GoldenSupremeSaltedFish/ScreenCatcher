import tkinter as tk
from tkinter import scrolledtext
from PIL import ImageGrab
from pyzbar.pyzbar import decode
import cv2
import numpy as np
import webbrowser
import keyboard
import threading
import time
# 截取屏幕
def captureScreen():
    screen = ImageGrab.grab()
    screenNp = np.array(screen)
    return cv2.cvtColor(screenNp, cv2.COLOR_RGB2BGR)
# 防抖处理
def debounce(wait):
    def decorator(fn):
        last_call = [0]
        def debounced(*args, **kwargs):
            now = time.time()
            if now - last_call[0] >= wait:
                last_call[0] = now
                return fn(*args, **kwargs)
        return debounced
    return decorator

# 识别二维码并在文本框中显示
@debounce(0.5)  # 防抖时间为0.5秒
def recognizeQrCode():
    screenImage = captureScreen()
    qrCodes = decode(screenImage)
    resultTextbox.delete(1.0, tk.END)  # 清空文本框
    for qrCode in qrCodes:
        qrData = qrCode.data.decode('utf-8')
        resultTextbox.insert(tk.END, f"识别到的二维码信息: {qrData}\n")
        
        if qrData.startswith('http://weixin.qq.com'):
            resultTextbox.insert(tk.END, f"这是微信的链接，目前无法支持打开 {qrData}\n")
            continue
        # 如果二维码数据是一个URL，自动打开浏览器
        elif qrData.startswith('http'):
            resultTextbox.insert(tk.END, f"正在打开浏览器: {qrData}\n")
            webbrowser.open(qrData)
            resultTextbox.insert(tk.END, "浏览器已打开\n")
        else:
            resultTextbox.insert(tk.END, "二维码信息不是有效的URL\n")
    
    if not qrCodes:
        resultTextbox.insert(tk.END, "未识别到二维码\n")

# 创建简单的GUI（缺乏防抖）
def create_gui():
    global resultTextbox
    rootWindow = tk.Tk()
    rootWindow.title("二维码识别器")

    # 创建文本框用于显示结果
    resultTextbox = scrolledtext.ScrolledText(rootWindow, width=50, height=10)
    resultTextbox.pack(pady=10)

    # 创建一个按钮来触发二维码识别
    recognizeButton = tk.Button(rootWindow, text="截屏并识别二维码(alt+q)", command=recognizeQrCode)
    recognizeButton.pack(pady=10)

    # 创建一个按钮来退出
    exitButton = tk.Button(rootWindow, text="退出", command=rootWindow.quit)
    exitButton.pack(pady=10)

    # 启动GUI主循环
    rootWindow.mainloop()

# 在后台监听快捷键
def start_keyboard_listener():
    keyboard.add_hotkey('alt+q', recognizeQrCode)  # 监听 Win+Q 组合键
    keyboard.wait('esc')  # 按 Esc 键退出程序

def main():
    # 创建线程来运行快捷键监听
    keyboard_thread = threading.Thread(target=start_keyboard_listener, daemon=True)
    keyboard_thread.start()
    # 根本不需要gui，我们需要一个灰色底色的全屏让用户进行选择然后进行扫码
    # 可选取的文字识别（全屏）
    # 运行GUI程序
    create_gui()

if __name__ == "__main__":
    main()
