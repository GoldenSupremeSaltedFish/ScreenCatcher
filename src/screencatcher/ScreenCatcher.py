import tkinter as tk
import webbrowser
from tkinter import scrolledtext

import cv2
import numpy as np
from PIL import ImageGrab
from pyzbar.pyzbar import decode  # type: ignore[import-untyped]


def main():
    """主函数"""

    def captureScreen():
        """截取屏幕"""
        screen = ImageGrab.grab()
        screenNp = np.array(screen)
        return cv2.cvtColor(screenNp, cv2.COLOR_RGB2BGR)

    def recognizeQrCode():
        """识别二维码并在文本框中展示解码内容"""
        screenImage = captureScreen()
        qrCodes = decode(screenImage)
        resultTextbox.delete(1.0, tk.END)  # 清空文本框
        for qrCode in qrCodes:
            qrData = qrCode.data.decode("utf-8")
            resultTextbox.insert(tk.END, f"识别到的二维码信息: {qrData}\n")
            if qrData.startswith('http://weixin.qq.com'):
                resultTextbox.insert(tk.END, f"这是微信的链接，目前无法支持打开 {qrData}\n")
            # 如果二维码数据是一个URL，自动打开浏览器
            elif qrData.startswith("http"):
                resultTextbox.insert(tk.END, f"正在打开浏览器: {qrData}\n")
                webbrowser.open(qrData)
            else:
                resultTextbox.insert(tk.END, "二维码信息不是有效的URL\n")

        if not qrCodes:
            resultTextbox.insert(tk.END, "未识别到二维码\n")

    # 创建简单的GUI
    rootWindow = tk.Tk()
    rootWindow.title("二维码识别器")

    # 创建文本框用于显示结果
    resultTextbox = scrolledtext.ScrolledText(rootWindow, width=50, height=10)
    resultTextbox.pack(pady=10)

    # 创建一个按钮来触发二维码识别
    recognizeButton = tk.Button(
        rootWindow, text="截屏并识别二维码", command=recognizeQrCode
    )
    recognizeButton.pack(pady=10)
    # 创建一个按钮来退出
    exitButton = tk.Button(rootWindow, text="退出", command=rootWindow.quit)
    exitButton.pack(pady=10)

    # 启动GUI主循环
    rootWindow.mainloop()


if __name__ == "__main__":
    main()
