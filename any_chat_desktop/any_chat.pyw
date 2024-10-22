import webview
import ctypes

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('dlm.mutigpt.desktop')
webview.create_window('迪乐姆多模态大模型桌面程序', 'http://8.133.177.11:9999/',width=1920,height=1080,fullscreen=False,resizable=True)
webview.start()