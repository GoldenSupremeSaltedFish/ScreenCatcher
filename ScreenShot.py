import threading
import tkinter as tk
from PIL import ImageGrab
from queue import Queue
from win32 import win32gui, win32print
from win32.lib import win32con
from win32.win32api import GetSystemMetrics


def get_real_resolution():
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return w, h


def get_screen_size():
    """获取缩放后的分辨率"""
    w = GetSystemMetrics(0)
    h = GetSystemMetrics(1)
    return w, h


class Box:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

    def isNone(self):
        return self.start_x is None or self.end_x is None

    def setStart(self, x, y):
        self.start_x = x
        self.start_y = y

    def setEnd(self, x, y):
        self.end_x = x
        self.end_y = y

    def box(self):
        lt_x = min(self.start_x, self.end_x)
        lt_y = min(self.start_y, self.end_y)
        rb_x = max(self.start_x, self.end_x)
        rb_y = max(self.start_y, self.end_y)
        return lt_x, lt_y, rb_x, rb_y


class SelectionArea:
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.area_box = Box()

    def empty(self):
        return self.area_box.isNone()

    def setStartPoint(self, x, y):
        self.canvas.delete('area', 'lt_txt', 'rb_txt')
        self.area_box.setStart(x, y)
        self.canvas.create_text(
            x, y - 10, text=f'({x}, {y})', fill='red', tag='lt_txt')

    def updateEndPoint(self, x, y):
        self.area_box.setEnd(x, y)
        self.canvas.delete('area', 'rb_txt')
        box_area = self.area_box.box()
        self.canvas.create_rectangle(
            *box_area, fill='black', outline='red', width=2, tags="area")
        self.canvas.create_text(
            x, y + 10, text=f'({x}, {y})', fill='red', tag='rb_txt')


class ScreenCapture:
    def __init__(self):
        self.queue = Queue()
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        real_resolution = get_real_resolution()
        screen_size = get_screen_size()
        screen_scale_rate = round(real_resolution[0] / screen_size[0], 2)
        self.screenshot = ScreenShot(screen_scale_rate, self.queue)
        
    def get_result(self):
        try:
            result = self.queue.get(timeout=10)  # 设置超时时间为 10 秒
            return result
        except Queue.Empty:
            return None  # 超时返回 None

    def stop(self):
        if self.thread.is_alive():
            self.screenshot.win.quit()
            self.thread.join()


class ScreenShot:
    def __init__(self, screen_scale_rate, queue):
        self.win = tk.Tk()
        self.win.attributes('-alpha', 0.25)
        self.win.overrideredirect(True)

        self.width = self.win.winfo_screenwidth()
        self.height = self.win.winfo_screenheight()

        self.is_selecting = False
        self.screen_scale_rate = screen_scale_rate
        self.queue = queue

        # 设置绑定键盘和鼠标事件
        self.win.bind('<KeyPress-Escape>', self.exit)
        self.win.bind('<KeyPress-Return>', self.confirmScreenShot)
        self.win.bind('<Button-1>', self.selectStart)
        self.win.bind('<ButtonRelease-1>', self.selectDone)
        self.win.bind('<Motion>', self.changeSelectionArea)

        self.canvas = tk.Canvas(self.win, width=self.width, height=self.height)
        self.canvas.pack()

        self.area = SelectionArea(self.canvas)
        self.win.mainloop()

    def exit(self, event=None):
        self.win.quit()
        self.queue.put(None)  # 退出时放入 None 表示没有截图

    def clear(self):
        self.canvas.delete('area', 'lt_txt', 'rb_txt')

    def captureImage(self):
        if self.area.empty():
            return None
        else:
            box_area = [x * self.screen_scale_rate for x in self.area.area_box.box()]
            self.clear()
            img = ImageGrab.grab(box_area)
            return img

    def confirmScreenShot(self, event=None):
        img = self.captureImage()
        self.queue.put(img)  # 将截图结果放入队列
        self.win.quit()

    def selectStart(self, event):
        self.is_selecting = True
        self.area.setStartPoint(event.x, event.y)

    def changeSelectionArea(self, event):
        if self.is_selecting:
            self.area.updateEndPoint(event.x, event.y)

    def selectDone(self, event):
        self.is_selecting = False
