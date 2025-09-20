import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import webbrowser
from pyzbar.pyzbar import decode  # type: ignore[import-untyped]
import time
from datetime import datetime
from .ScreenShot import ScreenCapture
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
    capture_thread = ScreenCapture()

    # 获取截图结果，阻塞直到有结果或超时
    img = capture_thread.get_result()

    if img is None:
        update_textbox("没有截屏\n")
        return

    threading.Thread(target=process_qr_code, args=(img,), daemon=True).start()

def process_qr_code(img):
    qrCodes = decode(img)
    update_textbox("")  # 清空文本框
    for qrCode in qrCodes:
        qrData = qrCode.data.decode("utf-8")
        update_textbox(f"识别到的二维码信息: {qrData}\n")

        if qrData.startswith("http://weixin.qq.com"):
            update_textbox(f"这是微信的链接，目前无法支持打开 {qrData}\n")
        elif qrData.startswith("http"):
            update_textbox(f"正在打开浏览器: {qrData}\n")
            webbrowser.open(qrData)
            update_textbox("浏览器已打开\n")
        else:
            update_textbox("二维码信息不是有效的URL\n")

    if not qrCodes:
        update_textbox("未识别到二维码\n")

def update_textbox(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    resultTextbox.config(state=tk.NORMAL)
    resultTextbox.insert(tk.END, full_message)
    resultTextbox.config(state=tk.DISABLED)

def start_keyboard_listener():
    keyboard.add_hotkey("alt+q", recognizeQrCode)
    keyboard.wait("esc")

def create_gui():
    root = tk.Tk()
    root.title("二维码识别器")
    root.geometry("600x400")
    root.overrideredirect(True)  # 去除默认的窗口装饰

    # 创建画布和背景
    canvas = tk.Canvas(root, bg="#ffffff", bd=0, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # 画圆角矩形
    def create_rounded_rect(x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1, x1+radius, y1,
                  x2-radius, y1, x2-radius, y1,
                  x2, y1, x2, y1+radius,
                  x2, y1+radius, x2, y2-radius,
                  x2, y2-radius, x2, y2,
                  x2-radius, y2, x2-radius, y2,
                  x1+radius, y2, x1+radius, y2,
                  x1, y2, x1, y2-radius,
                  x1, y2-radius, x1, y1+radius,
                  x1, y1+radius, x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    create_rounded_rect(0, 0, 600, 400, radius=25, fill="#dfe6e9")

    frame = ttk.Frame(canvas, padding="10 10 10 10")
    frame.place(relwidth=1, relheight=1)

    label = ttk.Label(frame, text="历史记录:", font=("Helvetica", 12))
    label.pack(anchor=tk.W, padx=10, pady=(0, 5))

    global resultTextbox
    resultTextbox = scrolledtext.ScrolledText(frame, width=70, height=15, font=("Helvetica", 12), state=tk.DISABLED)
    resultTextbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    button_frame = ttk.Frame(frame)
    button_frame.pack(pady=10)

    recognize_button = ttk.Button(button_frame, text="截屏并识别二维码 (alt+q)", command=recognizeQrCode)
    recognize_button.grid(row=0, column=0, padx=10)

    exit_button = ttk.Button(button_frame, text="退出", command=root.quit)
    exit_button.grid(row=0, column=1, padx=10)

    # 绑定鼠标事件以便移动窗口
    def on_mouse_press(event):
        root.startX = event.x
        root.startY = event.y

    def on_mouse_drag(event):
        x = root.winfo_pointerx() - root.startX
        y = root.winfo_pointery() - root.startY
        root.geometry(f"+{x}+{y}")

    canvas.bind("<ButtonPress-1>", on_mouse_press)
    canvas.bind("<B1-Motion>", on_mouse_drag)

    root.mainloop()

def main():
    keyboard_thread = threading.Thread(target=start_keyboard_listener, daemon=True)
    keyboard_thread.start()
    create_gui()

if __name__ == "__main__":
    main()
