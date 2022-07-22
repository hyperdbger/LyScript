import win32api
import win32gui, win32con
import win32clipboard
import re
import time

class cWindow:
    def __init__(self):
        self._hwnd = None

    def SetAsForegroundWindow(self):
        win32gui.SetForegroundWindow(self._hwnd)

    def Maximize(self):
        # 最大化
        win32gui.ShowWindow(self._hwnd, win32con.SW_MAXIMIZE)

    def _window_enum_callback(self, hwnd, regex):
        if self._hwnd is None and re.match(regex, str(win32gui.GetWindowText(hwnd))) is not None:
            self._hwnd = hwnd

    def find_window_regex(self, regex):
        self._hwnd = None
        win32gui.EnumWindows(self._window_enum_callback, regex)

    def hide_always_on_top_windows(self):
        win32gui.EnumWindows(self._window_enum_callback_hide, None)

    def _window_enum_callback_hide(self, hwnd, unused):
        if hwnd != self._hwnd:
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) & win32con.WS_EX_TOPMOST:
                className = win32gui.GetClassName(hwnd)
                if not (className == 'Button' or className == 'Shell_TrayWnd'):
                    win32gui.ShowWindow(hwnd, win32con.SW_FORCEMINIMIZE)

    def OpenFile(self,path):
        # 按下F3
        win32api.keybd_event(0x72, 0, 0, 0)
        win32api.keybd_event(0x72, 0, win32con.KEYEVENTF_KEYUP, 0)

        # 打开剪贴板
        win32clipboard.OpenClipboard()
        # 清空剪贴板
        win32clipboard.EmptyClipboard()
        # 设置剪贴板内容
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, path)
        # 获取剪贴板内容
        date = win32clipboard.GetClipboardData()
        print("[*] OpenFile = {}".format(date))
        # 关闭剪贴板
        win32clipboard.CloseClipboard()
        time.sleep(0.2)

        # 按下ctrl+v
        win32api.keybd_event(0x11, 0, 0, 0)
        win32api.keybd_event(0x56, 0, 0, 0)
        win32api.keybd_event(0x56, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)

        # 按下回车
        win32api.keybd_event(0x0D, 0, 0, 0)
        win32api.keybd_event(0x0D, 0, win32con.KEYEVENTF_KEYUP, 0)

    def deatch(self):
        # 按下Ctrl+Alt+F2
        win32api.keybd_event(0x11, 0, 0, 0)
        win32api.keybd_event(0x12, 0, 0, 0)
        win32api.keybd_event(0x71, 0, 0, 0)
        win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x12, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x71, 0, win32con.KEYEVENTF_KEYUP, 0)

# 打开调试程序
def OpenFile(path):
    regex = ".*x32dbg.*"
    cWindows = cWindow()
    cWindows.find_window_regex(regex)
    cWindows.SetAsForegroundWindow()
    cWindows.SetAsForegroundWindow()
    cWindows.OpenFile(path)

# 关闭调试程序
def DeatchFile():
    regex = ".*x32dbg.*"
    cWindows = cWindow()
    cWindows.find_window_regex(regex)
    cWindows.SetAsForegroundWindow()
    cWindows.SetAsForegroundWindow()
    cWindows.deatch()

if __name__ == "__main__":

    # 批量打开一个列表
    for item in ["C:\Program Files (x86)\Kingsoft\kwifi\dbghelp.dll","C:\Program Files (x86)\Kingsoft\kwifi\keasyipcn.dll"]:
        OpenFile(item)
        time.sleep(3)
        DeatchFile()
