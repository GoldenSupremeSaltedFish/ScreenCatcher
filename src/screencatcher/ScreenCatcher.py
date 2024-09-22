import threading
import tkinter as tk
from tkinter import scrolledtext
from PIL import ImageGrab
import webbrowser
from pyzbar.pyzbar import decode
import time
from ScreenShot import ScreenCapture
import keyboard  # 快捷键监听模块


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


@debounce(0.5)  # 防抖，0.5秒间隔
def recognizeQrCode():
     # 保证截图窗口在主线程中运行
    capture_thread = ScreenCapture()

    # 获取截图结果，阻塞直到有结果或超时
    img = capture_thread.get_result()

    if img is None:
        resultTextbox.insert(tk.END, "没有截屏\n")
        return

    # img.show()
    threading.Thread(target=process_qr_code, args=(img,), daemon=True).start()

# 处理二维码识别
def process_qr_code(img):
    qrCodes = decode(img)
    resultTextbox.delete(1.0, tk.END)  # 清空文本框
    for qrCode in qrCodes:
        qrData = qrCode.data.decode('utf-8')
        resultTextbox.insert(tk.END, f"识别到的二维码信息: {qrData}\n")

        if qrData.startswith('http://weixin.qq.com'):
            resultTextbox.insert(tk.END, f"这是微信的链接，目前无法支持打开 {qrData}\n")
        elif qrData.startswith('http'):
            resultTextbox.insert(tk.END, f"正在打开浏览器: {qrData}\n")
            webbrowser.open(qrData)
            resultTextbox.insert(tk.END, "浏览器已打开\n")
        else:
            resultTextbox.insert(tk.END, "二维码信息不是有效的URL\n")

    if not qrCodes:
        resultTextbox.insert(tk.END, "未识别到二维码\n")

# 快捷键监听函数
def start_keyboard_listener():
    keyboard.add_hotkey('alt+q', recognizeQrCode)  # 监听 Alt+Q 组合键
    keyboard.wait('esc')  # 按 Esc 键退出程序

# 创建GUI
def create_gui():
    root = tk.Tk()
    root.title("二维码识别器")

    global resultTextbox
    resultTextbox = scrolledtext.ScrolledText(root, width=50, height=10)
    resultTextbox.pack(pady=10)

    recognize_button = tk.Button(root, text="截屏并识别二维码(alt+q)", command=recognizeQrCode)
    recognize_button.pack(pady=10)

    exit_button = tk.Button(root, text="退出", command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()

# 主函数
def main():
    # 创建线程来运行快捷键监听
    keyboard_thread = threading.Thread(target=start_keyboard_listener, daemon=True)
    keyboard_thread.start()
    
    create_gui()

if __name__ == "__main__":
    main()
