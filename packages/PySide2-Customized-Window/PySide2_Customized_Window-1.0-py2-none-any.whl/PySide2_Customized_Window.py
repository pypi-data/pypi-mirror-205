try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    ISPYSIDE1 = False
except:
    raise ImportError('Cannot load PySide2.')
try:
    import nt
except:
    raise Exception('Windows, ReactOS or Wine is required.')
import sys
import ctypes
try:
    import winreg
except:
    import _winreg as winreg
from ctypes.wintypes import MSG, POINT, RECT


class LOGFONT(ctypes.Structure):
    _fields_ = [
    ('lfHeight', ctypes.c_long),
    ('lfWidth', ctypes.c_long),
    ('lfEscapement', ctypes.c_long),
    ('lfOrientation', ctypes.c_long),
    ('lfWeight', ctypes.c_long),
    ('lfItalic', ctypes.c_byte),
    ('lfUnderline', ctypes.c_byte),
    ('lfStrikeOut', ctypes.c_byte),
    ('lfCharSet', ctypes.c_byte),
    ('lfOutPrecision', ctypes.c_byte),
    ('lfClipPrecision', ctypes.c_byte),
    ('lfQuality', ctypes.c_byte),
    ('lfPitchAndFamily', ctypes.c_byte),
    ('lfFaceName', ctypes.c_wchar * 32)]


class NONCLIENTMETRICS(ctypes.Structure):
    _fields_ = [
    ('cbSize', ctypes.c_ulong),
    ('iBorderWidth', ctypes.c_int),
    ('iScrollWidth', ctypes.c_int),
    ('iScrollHeight', ctypes.c_int),
    ('iCaptionWidth', ctypes.c_int),
    ('iCaptionHeight', ctypes.c_int),
    ('lfCaptionFont', LOGFONT),
    ('iSmCaptionWidth', ctypes.c_int),
    ('iSmCaptionHeight', ctypes.c_int),
    ('lfSmCaptionFont', LOGFONT),
    ('iMenuWidth', ctypes.c_int),
    ('iMenuHeight', ctypes.c_int),
    ('lfMenuFont', LOGFONT),
    ('lfStatusFont', LOGFONT),
    ('lfMessageFont', LOGFONT),
    ('iPaddedBorderWidth', ctypes.c_int),]


class NCCALCSIZE_PARAMS(ctypes.Structure):
    _fields_ = [('rgrc', RECT * 3),
                ('lppos', ctypes.POINTER(ctypes.c_void_p))]


class WindowCompositionAttribute(ctypes.Structure):
    _fields_ = [("Attribute", ctypes.c_int), ("Data", ctypes.POINTER(ctypes.c_int)), ("SizeOfData", ctypes.c_size_t)]


class ACCENT_POLICY(ctypes.Structure):
    _fields_ = [("AccentState", ctypes.c_uint), ("AccentFlags", ctypes.c_uint), ("GradientColor", ctypes.c_uint),
        ("AnimationId", ctypes.c_uint)]


class DWM_BLURBEHIND(ctypes.Structure):
    _fields_ = [('dwFlags', ctypes.c_ulong), ('fEnable', ctypes.c_long),
        ('hRgnBlur', ctypes.c_void_p), ('fTransitionOnMaximized', ctypes.c_long)]


class MARGINS(ctypes.Structure):
    _fields_ = [("cxLeftWidth", ctypes.c_int), ("cxRightWidth", ctypes.c_int), ("cyTopHeight", ctypes.c_int),
                ("cyBottomHeight", ctypes.c_int)]


class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
    _fields_ = [("Attribute", ctypes.c_ulong), ("Data", ctypes.POINTER(ACCENT_POLICY)),
        ("SizeOfData", ctypes.c_ulong)]


class Win10BlurEffect:
    def __init__(self):
        self.WCA_ACCENT_POLICY = 19
        self.ACCENT_ENABLE_BLURBEHIND = 3
        self.ACCENT_ENABLE_ACRYLICBLURBEHIND = 4
        self.SetWindowCompositionAttribute = ctypes.windll.user32.SetWindowCompositionAttribute

        self.accentPolicy = ACCENT_POLICY()
        self.winCompAttrData = WINDOWCOMPOSITIONATTRIBDATA()
        self.winCompAttrData.Attribute = self.WCA_ACCENT_POLICY
        self.winCompAttrData.SizeOfData = ctypes.sizeof(self.accentPolicy)
        self.winCompAttrData.Data = ctypes.pointer(self.accentPolicy)

    def setAeroEffect(self, hWnd, gradientColor='01000000', isEnableShadow=True, animationId=0):
        gradientColor = ctypes.c_ulong(int(gradientColor, base=16))
        animationId = ctypes.c_ulong(animationId)
        accentFlags = ctypes.c_ulong(0x20 | 0x40 | 0x80 | 0x100 | 0x200) if isEnableShadow else ctypes.c_ulong(0)

        self.accentPolicy.AccentState = self.ACCENT_ENABLE_BLURBEHIND
        self.accentPolicy.GradientColor = gradientColor
        self.accentPolicy.AccentFlags = accentFlags
        self.accentPolicy.AnimationId = animationId
        code = self.SetWindowCompositionAttribute(hWnd, ctypes.pointer(self.winCompAttrData))
        return code

    def setAcrylicEffect(self, hWnd, gradientColor='01000000', isEnableShadow=True, animationId=0):
        gradientColor = ctypes.c_ulong(int(gradientColor, base=16))
        animationId = ctypes.c_ulong(animationId)
        accentFlags = ctypes.c_ulong(0x20 | 0x40 | 0x80 | 0x100) if isEnableShadow else ctypes.c_ulong(0)

        self.accentPolicy.AccentState = self.ACCENT_ENABLE_ACRYLICBLURBEHIND
        self.accentPolicy.GradientColor = gradientColor
        self.accentPolicy.AccentFlags = accentFlags
        self.accentPolicy.AnimationId = animationId
        code = self.SetWindowCompositionAttribute(hWnd, ctypes.pointer(self.winCompAttrData))
        return code


def isAeroEnabled():
    try:
        pfEnabled = ctypes.c_uint()
        ctypes.windll.dwmapi.DwmIsCompositionEnabled(ctypes.byref(pfEnabled))
        return pfEnabled.value
    except:
        return 0


def isdarktheme():
    try:
        value = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                                   "Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize"),
                                    "AppsUseLightTheme")[0]
    except:
        return False
    if value:
        return False
    else:
        return True


def pyside1_hwnd(winId):
    try:
        ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.c_void_p
        ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object, ctypes.c_char_p]
        hwnd = ctypes.pythonapi.PyCapsule_GetPointer(winId, None)
    except ValueError:
        ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
        ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
        hwnd = ctypes.pythonapi.PyCObject_AsVoidPtr(winId)
    return hwnd


def gethwnd(window):
    hwnd = window.winId()
    if type(hwnd) != int:
        try:
            hwnd = int(hwnd)
        except:
            hwnd = pyside1_hwnd(hwnd)
    return hwnd


def getdpiforwindow_winapi(hwnd):
    try:
        dpi_x = ctypes.c_uint()
        dpi_y = ctypes.c_uint()
        monitor_handle = ctypes.windll.user32.MonitorFromWindow(hwnd, 2)
        ctypes.windll.shcore.GetDpiForMonitor(monitor_handle, 0, ctypes.byref(dpi_x), ctypes.byref(dpi_y))
        dpi = dpi_x.value
    except:
        try:
            if ctypes.windll.user32.IsProcessDPIAware():
                hDC = ctypes.windll.user32.GetDC(None)
                dpi = ctypes.windll.gdi32.GetDeviceCaps(hDC, 88)
                ctypes.windll.user32.ReleaseDC(None, hDC)
            else:
                dpi = 96
        except:
            dpi = 96
    return dpi


def getdefaultfont():
    result = NONCLIENTMETRICS()
    result.cbSize = ctypes.sizeof(NONCLIENTMETRICS)
    ctypes.windll.user32.SystemParametersInfoW(0x29, ctypes.sizeof(NONCLIENTMETRICS), ctypes.pointer(result), 0)
    defaultfont = result.lfMessageFont.lfFaceName
    return defaultfont


class CustomizedWindow(QWidget):
    '''A customized window based on PySideX.'''
    def __init__(self):
        super(CustomizedWindow, self).__init__()
        self.hwnd = gethwnd(self)
        self.animation1 = QPropertyAnimation(self, b'windowOpacity')
        self.animation1.setDuration(250)
        self.animation1.setStartValue(0.0)
        self.animation1.setEndValue(1.0)
        self.animation2 = QPropertyAnimation(self, b'windowOpacity')
        self.animation2.setDuration(250)
        self.animation2.setStartValue(1.0)
        self.animation2.setEndValue(0.0)
        self.nonclientareasizeinited = False
        self.isblurwindow = isinstance(self, BlurWindow)
        WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_int)
        MessageHandlerAddress = ctypes.cast(WNDPROC(self.MessageHandler), ctypes.c_void_p).value
        self.originalMessageHandler = ctypes.windll.user32.SetWindowLongW(self.hwnd, -4, MessageHandlerAddress)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.hwnd = gethwnd(self)
        if ISPYSIDE1:
            ctypes.windll.user32.SetWindowLongW(self.hwnd, -16, 0x40000 | 0x20000 | 0x10000)
        else:
            ctypes.windll.user32.SetWindowLongW(self.hwnd, -16, 0xc00000 | 0x40000 | 0x20000 | 0x10000)
        ctypes.windll.user32.SetWindowLongW(self.hwnd, -20, 0x200)
        self.isaeroenabled = isAeroEnabled()
        if self.isaeroenabled:
            if self.isblurwindow:
                self.setBlurEffect()
            else:
                self.setDWMShadowEffect()
        self.dpi = getdpiforwindow_winapi(self.hwnd)
        dpi = self.dpi
        self.maximizedwindowborderwidth_list = self.getMaximizedWindowBorderWidth()
        self.themecolour = 0
        self.isdarktheme = isdarktheme()
        self.setMinimumSize(int(220.0 * dpi / 96.0), int(48.0 * dpi / 96.0))
        self.border_width = int(5.0 * dpi / 96.0)
        self.title_height = int(30.0 * dpi / 96.0)
        self.menubutton_width = int(46.0 * dpi / 96.0)
        self.title_font_size = int(13.0 * dpi / 96.0)
        self.titleiconlayout_margin = int(7.0 * dpi / 96.0)
        self.inminsizebutton = False
        self.inmaxsizebutton = False
        self.inclosebutton = False
        self.intitlebar = False
        self.intopborder = False
        self.inleftborder = False
        self.inbottomborder = False
        self.inrightborder = False
        try:
            self.defaultfont = getdefaultfont()
        except:
            self.defaultfont = ''
        self.windowmargin_left = 0
        self.windowmargin_right = 0
        self.windowmargin_top = 0
        self.windowmargin_bottom = 0
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)
        self.titleBarLayout = QHBoxLayout()
        self.titleBarLayout.setContentsMargins(0, 0, 0, 0)
        self.titleBarLayout.setSpacing(0)
        self.titleBar = QLabel('', self)
        self.titleBar.setLayout(self.titleBarLayout)
        self.mainLayout.addWidget(self.titleBar)
        self.clientArea = QLabel('', self)
        self.mainLayout.addWidget(self.clientArea)
        self.titleIconLayout = QHBoxLayout()
        self.titleIconLayout.setContentsMargins(self.titleiconlayout_margin, self.titleiconlayout_margin, self.titleiconlayout_margin, self.titleiconlayout_margin)
        self.titleIconLayout.setSpacing(0)
        self.titleIconContainerLabel = QLabel('', self.titleBar)
        self.titleIconContainerLabel.setStyleSheet('background:transparent')
        self.titleIconContainerLabel.setLayout(self.titleIconLayout)
        self.titleIconLabel = QLabel('', self.titleIconContainerLabel)
        self.titleIconLabel.setStyleSheet('background:transparent')
        self.titleIconLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.titleIconLayout.addWidget(self.titleIconLabel)
        self.titleBarLayout.addWidget(self.titleIconContainerLabel)
        self.titleTextLabel = QLabel(self.windowTitle(), self.titleBar)
        self.titleTextLabel.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        self.titleBarLayout.addWidget(self.titleTextLabel)
        self.minMaxSizeButtonHoverBackgroundStyleSheet_Light = 'background:rgba(0, 0, 0, 25); border-radius:0px'
        self.minMaxSizeButtonPressedBackgroundStyleSheet_Light = 'background:rgba(0, 0, 0, 50); border-radius:0px'
        self.minMaxSizeButtonHoverBackgroundStyleSheet_Dark = 'background:rgba(255, 255, 255, 25); border-radius:0px'
        self.minMaxSizeButtonPressedBackgroundStyleSheet_Dark = 'background:rgba(255, 255, 255, 50); border-radius:0px'
        self.closeButtonHoverBackgroundStyleSheet = 'background:rgba(255, 0, 0, 255); border-radius:0px'
        self.closeButtonPressedBackgroundStyleSheet = 'background:rgba(255, 0, 0, 127); border-radius:0px'
        self.minSizeButton = QPushButton('', self.titleBar)
        self.minSizeButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.minSizeButton.setFocusPolicy(Qt.NoFocus)
        self.titleBarLayout.addWidget(self.minSizeButton)
        self.maxSizeButton = QPushButton('', self.titleBar)
        self.maxSizeButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.maxSizeButton.setFocusPolicy(Qt.NoFocus)
        self.titleBarLayout.addWidget(self.maxSizeButton)
        self.closeButton = QPushButton('', self.titleBar)
        self.closeButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.closeButton.setFocusPolicy(Qt.NoFocus)
        self.titleBarLayout.addWidget(self.closeButton)
        self.paintTitleBarAndClientArea(self.isActiveWindow())
        self.originalSetWindowTitle = self.setWindowTitle
        self.setWindowTitle = self.setWindowTitle2
        self.originalSetWindowIcon = self.setWindowIcon
        self.setWindowIcon = self.setWindowIcon2
        if not ISPYSIDE1:
            self.windowHandle().screenChanged.connect(self.screenChangedHandler)
    def setDarkTheme(self, themecolour=0):
        '''themecolour=0: Auto; themecolour=1: Light; themecolour=2: Dark'''
        self.themecolour = themecolour
        if themecolour == 0:
            self.isdarktheme = isdarktheme()
        elif themecolour == 1:
            self.isdarktheme = False
        elif themecolour == 2:
            self.isdarktheme = True
        else:
            raise Exception
    def setWindowTitle2(self, arg__1):
        self.originalSetWindowTitle(arg__1)
        self.paintTitleBarAndClientArea(self.isActiveWindow())
    def setWindowIcon2(self, icon):
        self.originalSetWindowIcon(icon)
        self.paintTitleBarAndClientArea(self.isActiveWindow())
    def paintTitleBarAndClientArea(self, isactivewindow=0, ismaximized=-1):
        SWP_NOSIZE = 0x1
        SWP_NOMOVE = 0x2
        SWP_NOZORDER = 0x4
        hwnd = self.hwnd
        dpi = self.dpi
        title_height = self.title_height
        menubutton_width = self.menubutton_width
        title_font_size = self.title_font_size
        titleiconlayout_margin = self.titleiconlayout_margin
        defaultfont = self.defaultfont
        isblurwindow = self.isblurwindow
        isaeroenabled = self.isaeroenabled
        isdarktheme = self.isdarktheme
        if ismaximized == -1:
            ismaximized = self.isMaximized()
        self.titleBar.setLayout(self.titleBarLayout)
        self.titleBar.setFixedHeight(self.title_height)
        self.titleIconContainerLabel.setFixedSize(title_height, title_height)
        titleiconsize = int(title_height - int(2.0 * titleiconlayout_margin))
        windowicon = self.windowIcon()
        windowiconpixmap = windowicon.pixmap(titleiconsize, titleiconsize)
        self.titleIconLabel.setPixmap(windowiconpixmap)
        self.titleIconLayout.setContentsMargins(self.titleiconlayout_margin, self.titleiconlayout_margin, self.titleiconlayout_margin, self.titleiconlayout_margin)
        self.titleTextLabel.setText(self.windowTitle())
        self.titleTextLabel.setAlignment(Qt.AlignVCenter)
        self.titleTextLabel.setFixedHeight(title_height)
        self.minSizeButton.setFixedSize(menubutton_width, title_height)
        self.maxSizeButton.setFixedSize(menubutton_width, title_height)
        self.closeButton.setFixedSize(menubutton_width, title_height)
        self.minSizeButton.setStyleSheet('background:transparent; border-radius:0px')
        self.maxSizeButton.setStyleSheet('background:transparent; border-radius:0px')
        self.closeButton.setStyleSheet('background:transparent; border-radius:0px')
        titletextpalette = QPalette()
        self.titleTextLabel.setStyleSheet('''QLabel{
background:transparent;
font-family:'%s';
font-size:%dpx;
}''' % (defaultfont, title_font_size))
        if isdarktheme:
            try:
                ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 19, ctypes.byref(ctypes.c_int(1)), ctypes.sizeof(ctypes.c_int(1)))
                ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(ctypes.c_int(1)), ctypes.sizeof(ctypes.c_int(1)))
            except: pass
            ctypes.windll.user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOMOVE | SWP_NOZORDER)
            if isblurwindow:
                if isaeroenabled:
                    self.titleBar.setStyleSheet('''QLabel{
background:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 rgba(0, 0, 0, 107) , stop: 1.0 rgba(0, 0, 0, 197));
}''')
                    self.clientArea.setStyleSheet('''QLabel{
background:rgba(0, 0, 0, 127);
}''')
                else:
                    self.titleBar.setStyleSheet('''QLabel{
background:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 rgba(38, 38, 38, 255) , stop: 1.0 rgba(0, 0, 0, 255));
}''')
                    self.clientArea.setStyleSheet('''QLabel{
background:rgba(20, 20, 20, 255);
}''')
            else:
                self.titleBar.setStyleSheet('''QLabel{
background:#000000;
}''')
                self.clientArea.setStyleSheet('''QLabel{
background:#000000;
}''')
            if isactivewindow:
                menuButtonPen = QPen(Qt.white)
                titletextpalette.setColor(QPalette.WindowText, Qt.white)
            else:
                menuButtonPen = QPen(QColor(155, 155, 155))
                titletextpalette.setColor(QPalette.WindowText, QColor(155, 155, 155))
        else:
            try:
                ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 19, ctypes.byref(ctypes.c_int(0)), ctypes.sizeof(ctypes.c_int(0)))
                ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(ctypes.c_int(0)), ctypes.sizeof(ctypes.c_int(0)))
            except: pass
            ctypes.windll.user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOMOVE | SWP_NOZORDER)
            if isblurwindow:
                if isaeroenabled:
                    self.titleBar.setStyleSheet('''QLabel{
background:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 rgba(255, 255, 255, 107) , stop: 1.0 rgba(255, 255, 255, 197));
}''')
                    self.clientArea.setStyleSheet('''QLabel{
background:rgba(255, 255, 255, 127);
}''')
                else:
                    self.titleBar.setStyleSheet('''QLabel{
background:qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 rgba(217, 217, 217, 255) , stop: 1.0 rgba(255, 255, 255, 255));
}''')
                    self.clientArea.setStyleSheet('''QLabel{
background:rgba(235, 235, 235, 255);
}''')
            else:
                self.titleBar.setStyleSheet('''QLabel{
background:#FFFFFF;
}''')
                self.clientArea.setStyleSheet('''QLabel{
background:#FFFFFF;
}''')
            if isactivewindow:
                menuButtonPen = QPen(Qt.black)
                titletextpalette.setColor(QPalette.WindowText, Qt.black)
            else:
                menuButtonPen = QPen(QColor(99, 99, 99))
                titletextpalette.setColor(QPalette.WindowText, QColor(99, 99, 99))
        self.titleTextLabel.setPalette(titletextpalette)
        menuButtonPen.setWidth(int(5.0 * dpi / 96.0))
        minPath = QPainterPath()
        minPath.moveTo(int(100.0 * dpi / 96.0), int(80.0 * dpi / 96.0))
        minPath.lineTo(int(156.0 * dpi / 96.0), int(80.0 * dpi / 96.0))
        minIcon = QIcon()
        minPixmap = QPixmap(int(256.0 * dpi / 96.0), int(160.0 * dpi / 96.0))
        minPixmap.fill(Qt.transparent)
        minPainter = QPainter(minPixmap)
        minPainter.setRenderHint(QPainter.Antialiasing)
        minPainter.setPen(menuButtonPen)
        minPainter.drawPath(minPath)
        minPainter.end()
        minIcon.addPixmap(minPixmap)
        self.minSizeButton.setIcon(minIcon)
        self.minSizeButton.setIconSize(QSize(menubutton_width, title_height))
        maxPath = QPainterPath()
        if ismaximized:
            maxPath.moveTo(int(103 * dpi / 96.0), int(65 * dpi / 96.0))
            maxPath.lineTo(int(143 * dpi / 96.0), int(65 * dpi / 96.0))
            maxPath.lineTo(int(143 * dpi / 96.0), int(105 * dpi / 96.0))
            maxPath.lineTo(int(103 * dpi / 96.0), int(105 * dpi / 96.0))
            maxPath.lineTo(int(103 * dpi / 96.0), int(65 * dpi / 96.0))
            maxPath.moveTo(int(113 * dpi / 96.0), int(55 * dpi / 96.0))
            maxPath.lineTo(int(153 * dpi / 96.0), int(55 * dpi / 96.0))
            maxPath.lineTo(int(153 * dpi / 96.0), int(95 * dpi / 96.0))
        else:
            maxPath.moveTo(int(103 * dpi / 96.0), int(55 * dpi / 96.0))
            maxPath.lineTo(int(153 * dpi / 96.0), int(55 * dpi / 96.0))
            maxPath.lineTo(int(153 * dpi / 96.0), int(105 * dpi / 96.0))
            maxPath.lineTo(int(103 * dpi / 96.0), int(105 * dpi / 96.0))
            maxPath.lineTo(int(103 * dpi / 96.0), int(55 * dpi / 96.0))
        maxIcon = QIcon()
        maxPixmap = QPixmap(int(256.0 * dpi / 96.0), int(160.0 * dpi / 96.0))
        maxPixmap.fill(Qt.transparent)
        maxPainter = QPainter(maxPixmap)
        maxPainter.setRenderHint(QPainter.Antialiasing)
        maxPainter.setPen(menuButtonPen)
        maxPainter.drawPath(maxPath)
        maxPainter.end()
        maxIcon.addPixmap(maxPixmap)
        self.maxSizeButton.setIcon(maxIcon)
        self.maxSizeButton.setIconSize(QSize(menubutton_width, title_height))
        closePath = QPainterPath()
        closePath.moveTo(int(103 * dpi / 96.0), int(55 * dpi / 96.0))
        closePath.lineTo(int(153 * dpi / 96.0), int(105 * dpi / 96.0))
        closePath.moveTo(int(153 * dpi / 96.0), int(55 * dpi / 96.0))
        closePath.lineTo(int(103 * dpi / 96.0), int(105 * dpi / 96.0))
        closeIcon = QIcon()
        closePixmap = QPixmap(int(256.0 * dpi / 96.0), int(160.0 * dpi / 96.0))
        closePixmap.fill(Qt.transparent)
        closePainter = QPainter(closePixmap)
        closePainter.setRenderHint(QPainter.Antialiasing)
        closePainter.setPen(menuButtonPen)
        closePainter.drawPath(closePath)
        closePainter.end()
        closeIcon.addPixmap(closePixmap)
        self.closeButton.setIcon(closeIcon)
        self.closeButton.setIconSize(QSize(menubutton_width, title_height))
    def setMenuButtonStyle(self, button, state=1):
        stylesheet1 = 'background:transparent'
        stylesheet2 = 'background:transparent'
        stylesheet3 = 'background:transparent'
        if button == 1:
            if state == 1:
                stylesheet1 = self.minMaxSizeButtonHoverBackgroundStyleSheet_Dark if self.isdarktheme else self.minMaxSizeButtonHoverBackgroundStyleSheet_Light
            elif state == 2:
                stylesheet1 = self.minMaxSizeButtonPressedBackgroundStyleSheet_Dark if self.isdarktheme else self.minMaxSizeButtonPressedBackgroundStyleSheet_Light
        elif button == 2:
            if state == 1:
                stylesheet2 = self.minMaxSizeButtonHoverBackgroundStyleSheet_Dark if self.isdarktheme else self.minMaxSizeButtonHoverBackgroundStyleSheet_Light
            elif state == 2:
                stylesheet2 = self.minMaxSizeButtonPressedBackgroundStyleSheet_Dark if self.isdarktheme else self.minMaxSizeButtonPressedBackgroundStyleSheet_Light
        elif button == 3:
            if state == 1:
                stylesheet3 = self.closeButtonHoverBackgroundStyleSheet
            elif state == 2:
                stylesheet3 = self.closeButtonPressedBackgroundStyleSheet
        elif button != 0:
            raise Exception
        self.minSizeButton.setStyleSheet(stylesheet1)
        self.maxSizeButton.setStyleSheet(stylesheet2)
        self.closeButton.setStyleSheet(stylesheet3)
    def MessageHandler(self, hwnd, message, wParam, lParam):
        '''For PySide1/2/6, you should call super method after defining MessageHandler.
Here's an example:
class MyOwnWindow(self):
|->|...
|->|def MessageHandler(self, hwnd, message, wParam, lParam):
|->||->|super(MyOwnWindow, self).MessageHandler(self, hwnd, message, wParam, lParam)
|->||->|...
'''
        WM_ACTIVATE = 0x6
        WM_SHOWWINDOW = 0x18
        WM_SETTINGCHANGE = 0x1a
        WM_GETMINMAXINFO = 0x24
        WM_NCCALCSIZE = 0x83
        WM_NCHITTEST = 0x84
        WM_NCLBUTTONDOWN = 0xa1
        WM_NCLBUTTONUP = 0xa2
        WM_LBUTTONUP = 0x2a2
        WM_DPICHANGED = 0x2e0
        WM_SYSCOMMAND = 0x112
        WM_THEMECHANGED = 0x31a
        WM_DWMCOMPOSITIONCHANGED = 0x31e
        SW_PARENTOPENING = 0x3
        SC_SIZE = 0xf000
        SC_MOVE = 0xf010
        SC_MINIMIZE = 0xf020
        SC_MAXIMIZE = 0xf030
        SC_CLOSE = 0xf060
        SC_RESTORE = 0xf120
        HTCLIENT = 0x1
        HTCAPTION = 0x2
        HTMINBUTTON = 0x8
        HTMAXBUTTON = 0x9
        HTCLOSE = 0x14
        HTLEFT = 0xa
        HTRIGHT = 0xb
        HTTOP = 0xc
        HTTOPLEFT = 0xd
        HTTOPRIGHT = 0xe
        HTBOTTOM = 0xf
        HTBOTTOMLEFT = 0x10
        HTBOTTOMRIGHT = 0x11
        WVR_REDRAW = 0x300
        try:
            dpi = self.dpi
            border_width = self.border_width
            title_height = self.title_height
            menubutton_width = self.menubutton_width
            windowmargin_left = self.windowmargin_left
            windowmargin_right = self.windowmargin_right
            windowmargin_top = self.windowmargin_top
            windowmargin_bottom = self.windowmargin_bottom
        except:
            dpi = 96
            border_width = 0
            title_height = 0
            menubutton_width = 0
            windowmargin_left = 0
            windowmargin_right = 0
            windowmargin_top = 0
            windowmargin_bottom = 0
        windowrect = self.GetWindowRect()
        windowx = windowrect.left
        windowy = windowrect.top
        try:
            globalpos = POINT()
            ctypes.windll.user32.GetPhysicalCursorPos(ctypes.byref(globalpos))
            ctypes.windll.user32.PhysicalToLogicalPoint(self.hwnd, ctypes.byref(globalpos))
            x = globalpos.x - windowx
            y = globalpos.y - windowy
        except:
            globalpos = POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(globalpos))
            x = globalpos.x - windowx
            y = globalpos.y - windowy
        width = windowrect.right - windowx
        height = windowrect.bottom - windowy
        intitlebar = windowmargin_top <= y < title_height + windowmargin_top
        inminsizebutton = int(width - windowmargin_left - 3 * menubutton_width) <= x < int(width - windowmargin_left - 2 * menubutton_width) and intitlebar
        inmaxsizebutton = int(width - windowmargin_left - 2 * menubutton_width) <= x < int(width - windowmargin_left - menubutton_width) and intitlebar
        inclosebutton = int(width - windowmargin_left - menubutton_width) <= x < int(width - windowmargin_left) and intitlebar
        intopborder = y <= border_width
        inleftborder = x <= border_width
        inbottomborder = int(height - y) <= border_width
        inrightborder = int(width - x) <= border_width
        self.inminsizebutton = inminsizebutton
        self.inmaxsizebutton = inmaxsizebutton
        self.inclosebutton = inclosebutton
        self.intitlebar = intitlebar
        self.intopborder = intopborder
        self.inleftborder = inleftborder
        self.inbottomborder = inbottomborder
        self.inrightborder = inrightborder
        if message == WM_NCCALCSIZE:
            if ISPYSIDE1:
                return self.Handle_WM_NCCALCSIZE_Message(hwnd, message, wParam, lParam)
        if message == WM_NCHITTEST:
            VK_LBUTTON = 0x1
            isleftbuttonpressed = ctypes.windll.user32.GetKeyState(VK_LBUTTON) not in [0, 1]
            if not self.isMaximized():
                if intopborder and inleftborder:
                    WM_NCHITTEST_result = HTTOPLEFT
                elif intopborder and inrightborder:
                    WM_NCHITTEST_result = HTTOPRIGHT
                elif inbottomborder and inleftborder:
                    WM_NCHITTEST_result = HTBOTTOMLEFT
                elif inbottomborder and inrightborder:
                    WM_NCHITTEST_result = HTBOTTOMRIGHT
                elif inleftborder:
                    WM_NCHITTEST_result = HTLEFT
                elif intopborder:
                    WM_NCHITTEST_result = HTTOP
                elif inrightborder:
                    WM_NCHITTEST_result = HTRIGHT
                elif inbottomborder:
                    WM_NCHITTEST_result = HTBOTTOM
            if not 'WM_NCHITTEST_result' in dir():
                if inminsizebutton:
                    if not isleftbuttonpressed:
                        self.setMenuButtonStyle(1, 1)
                    WM_NCHITTEST_result = HTMINBUTTON
                elif inmaxsizebutton:
                    if not isleftbuttonpressed:
                        self.setMenuButtonStyle(2, 1)
                    WM_NCHITTEST_result = HTMAXBUTTON
                elif inclosebutton:
                    if not isleftbuttonpressed:
                        self.setMenuButtonStyle(3, 1)
                    WM_NCHITTEST_result = HTCLOSE
                elif intitlebar:
                    WM_NCHITTEST_result = HTCAPTION
                else:
                    WM_NCHITTEST_result = HTCLIENT
            if WM_NCHITTEST_result not in [HTMINBUTTON, HTMAXBUTTON, HTCLOSE]:
                if not isleftbuttonpressed:
                    self.setMenuButtonStyle(0)
            return WM_NCHITTEST_result
        if message == WM_NCLBUTTONDOWN:
            if wParam in [HTMINBUTTON, HTMAXBUTTON, HTCLOSE]:
                if wParam == HTMINBUTTON:
                    self.setMenuButtonStyle(1, 2)
                if wParam == HTMAXBUTTON:
                    self.setMenuButtonStyle(2, 2)
                if wParam == HTCLOSE:
                    self.setMenuButtonStyle(3, 2)
                return 0
            return ctypes.windll.user32.DefWindowProcW(hwnd, message, wParam, lParam)
        if message == WM_NCLBUTTONUP:
            self.setMenuButtonStyle(0)
            if wParam == HTMINBUTTON:
                self.minSizeButtonClicked()
            elif wParam == HTMAXBUTTON:
                self.maxSizeButtonClicked()
            elif wParam == HTCLOSE:
                self.closeButtonClicked()
            return ctypes.windll.user32.DefWindowProcW(hwnd, message, wParam, lParam)
        if message == WM_LBUTTONUP:
            self.setMenuButtonStyle(0)
        if message == WM_DPICHANGED:
            window_rect = RECT.from_address(lParam)
            olddpi = self.dpi
            dpi = wParam >> 16
            self.dpi = dpi
            self.maximizedwindowborderwidth_list = self.getMaximizedWindowBorderWidth()
            self.setMinimumSize(int(220.0 * dpi / 96.0), int(48.0 * dpi / 96.0))
            x = window_rect.left
            y = window_rect.top
            width = int(window_rect.right - window_rect.left)
            height = int(window_rect.bottom - window_rect.top)
            self.setGeometry(x, y, width, height)
            self.border_width = int(5.0 * dpi / 96.0)
            self.title_height = int(30.0 * dpi / 96.0)
            self.menubutton_width = int(46.0 * dpi / 96.0)
            self.title_font_size = int(13.0 * dpi / 96.0)
            self.titleiconlayout_margin = int(7.0 * dpi / 96.0)
            self.paintTitleBarAndClientArea(self.isActiveWindow())
            ctypes.windll.user32.CallWindowProcW(self.originalMessageHandler, hwnd, message, wParam, lParam)
            return 0
        if message == WM_SETTINGCHANGE:
            if self.themecolour == 0 and str(ctypes.cast(lParam, ctypes.c_wchar_p).value) == 'ImmersiveColorSet':
                self.isdarktheme = isdarktheme()
                self.paintTitleBarAndClientArea(self.isActiveWindow())
        if message == WM_DWMCOMPOSITIONCHANGED:
            self.isaeroenabled = isAeroEnabled()
            if self.isaeroenabled:
                if self.isblurwindow:
                    self.setBlurEffect()
                else:
                    self.setDWMShadowEffect()
            self.paintTitleBarAndClientArea(self.isActiveWindow())
        if message == WM_ACTIVATE:
            isactivewindow = 0 if wParam == 0 else 1
            if not isactivewindow:
                self.setMenuButtonStyle(0)
            self.paintTitleBarAndClientArea(isactivewindow)
        if message == WM_SHOWWINDOW:
            self.paintTitleBarAndClientArea(self.isActiveWindow())
        return ctypes.windll.user32.CallWindowProcW(self.originalMessageHandler, hwnd, message, wParam, lParam)
    def Handle_WM_NCCALCSIZE_Message(self, hwnd, message, wParam, lParam):
        try:
            nonclientareasizeinited = self.nonclientareasizeinited
        except:
            nonclientareasizeinited = False
        if not nonclientareasizeinited:
            if ISPYSIDE1:
                ctypes.windll.user32.SetWindowLongW(self.hwnd, -16, ctypes.windll.user32.GetWindowLongW(self.hwnd, -16) | 0xc00000)
            self.nonclientareasizeinited = True
        if wParam:
            rect = ctypes.cast(lParam, ctypes.POINTER(NCCALCSIZE_PARAMS)).contents.rgrc[0]
        else:
            rect = ctypes.cast(lParam, ctypes.POINTER(RECT)).contents
        ISMAXIMIZED = ctypes.windll.user32.IsZoomed(hwnd)
        try:
            maximizedwindowborderwidth_list = self.maximizedwindowborderwidth_list
        except:
            maximizedwindowborderwidth_list = [0, 0]
        if ISMAXIMIZED:
            self.windowmargin_left = maximizedwindowborderwidth_list[0]
            self.windowmargin_right = maximizedwindowborderwidth_list[0]
            self.windowmargin_top = maximizedwindowborderwidth_list[1]
            self.windowmargin_bottom = maximizedwindowborderwidth_list[1]
        else:
            self.windowmargin_left = 0
            self.windowmargin_right = 0
            self.windowmargin_top = 0
            self.windowmargin_bottom = 0
        windowmargin_left = self.windowmargin_left
        windowmargin_right = self.windowmargin_right
        windowmargin_top = self.windowmargin_top
        windowmargin_bottom = self.windowmargin_bottom
        rect.left += windowmargin_left
        rect.right -= windowmargin_right
        rect.top += windowmargin_top
        rect.bottom -= windowmargin_bottom
        if nonclientareasizeinited:
            self.paintTitleBarAndClientArea(self.isActiveWindow(), ISMAXIMIZED)
        return 0
    def minSizeButtonClicked(self):
        WM_SYSCOMMAND = 0x112
        SC_MINIMIZE = 0xf020
        ctypes.windll.user32.SendMessageW(self.hwnd, WM_SYSCOMMAND, SC_MINIMIZE, 0)
    def maxSizeButtonClicked(self):
        WM_SYSCOMMAND = 0x112
        SC_MAXIMIZE = 0xf030
        SC_RESTORE = 0xf120
        if self.isMaximized():
            ctypes.windll.user32.SendMessageW(self.hwnd, WM_SYSCOMMAND, SC_RESTORE, 0)
        elif self.isFullScreen():
            pass
        else:
            ctypes.windll.user32.SendMessageW(self.hwnd, WM_SYSCOMMAND, SC_MAXIMIZE, 0)
    def closeButtonClicked(self):
        WM_SYSCOMMAND = 0x112
        SC_CLOSE = 0xf060
        ctypes.windll.user32.SendMessageW(self.hwnd, WM_SYSCOMMAND, SC_CLOSE, 0)
    def getMaximizedWindowBorderWidth(self):
        SM_CXSIZEFRAME = 32
        SM_CYSIZEFRAME = 33
        SM_CXPADDEDBORDER = 92
        dpi = self.dpi
        try:
            borderwidth_x = ctypes.windll.user32.GetSystemMetricsForDpi(SM_CXSIZEFRAME, dpi) + ctypes.windll.user32.GetSystemMetricsForDpi(SM_CXPADDEDBORDER, dpi)
            borderwidth_y = ctypes.windll.user32.GetSystemMetricsForDpi(SM_CYSIZEFRAME, dpi) + ctypes.windll.user32.GetSystemMetricsForDpi(SM_CXPADDEDBORDER, dpi)
        except:
            borderwidth_x = ctypes.windll.user32.GetSystemMetrics(SM_CXSIZEFRAME) + ctypes.windll.user32.GetSystemMetrics(SM_CXPADDEDBORDER)
            borderwidth_y = ctypes.windll.user32.GetSystemMetrics(SM_CYSIZEFRAME) + ctypes.windll.user32.GetSystemMetrics(SM_CXPADDEDBORDER)
        return [borderwidth_x, borderwidth_y]
    def nativeEvent(self, eventType, msg):
        '''For PySide2/6, you should call super method after defining nativeEvent.
Here's an example:
class MyOwnWindow(self):
|->|...
|->|def nativeEvent(self, eventType, msg):
|->||->|super(MyOwnWindow, self).nativeEvent(self, eventType, msg)
|->||->|...
'''
        WM_NCCALCSIZE = 0x83
        msg = MSG.from_address(msg.__int__())
        hwnd = msg.hWnd
        message = msg.message
        wParam = msg.wParam
        lParam = msg.lParam
        if message == WM_NCCALCSIZE:
            if not ISPYSIDE1:
                return True, self.Handle_WM_NCCALCSIZE_Message(hwnd, message, wParam, lParam)
        return super().nativeEvent(eventType, msg)
    def setBlurEffect(self):
        hwnd = self.hwnd
        try:
            bb = DWM_BLURBEHIND()
            bb.dwFlags = 1
            bb.fEnable = 1
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 2, ctypes.byref(ctypes.c_int(2)), ctypes.sizeof(ctypes.c_int(2)))
            win11_21h2_blur_code, win11_22h2_blur_code = self.setwin11blur(hwnd)
            if win11_22h2_blur_code:
                ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(MARGINS(1, 1, 0, 0)))
                ctypes.windll.dwmapi.DwmEnableBlurBehindWindow(ctypes.c_int(hwnd), ctypes.byref(bb))
            else:
                ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(MARGINS(-1, -1, -1, -1)))
                return 3
            try:
                AeroEffect = Win10BlurEffect()
                win10_blur_code = AeroEffect.setAeroEffect(hwnd, isEnableShadow=True)
                if win10_blur_code != 0:
                    return 2
            except: pass
            return 1
        except:
            return 0
    def setDWMShadowEffect(self):
        hwnd = self.hwnd
        try:
            ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(MARGINS(1, 1, 0, 0)))
            return 1
        except:
            return 0
    def setwin11blur(self, hWnd):
        Win11_21H2_ENTRY = 1029
        Win11_21H2_VALUE = 1
        Win11_22H2_ENTRY = 38
        Win11_22H2_VALUE = 3
        Win11_21H2_COMMAND = ctypes.windll.dwmapi.DwmSetWindowAttribute(hWnd, Win11_21H2_ENTRY,
                                                                        ctypes.byref(ctypes.c_int(Win11_21H2_VALUE)),
                                                                        ctypes.sizeof(ctypes.c_int))
        Win11_22H2_COMMAND = ctypes.windll.dwmapi.DwmSetWindowAttribute(hWnd, Win11_22H2_ENTRY,
                                                                        ctypes.byref(ctypes.c_int(Win11_22H2_VALUE)),
                                                                        ctypes.sizeof(ctypes.c_int))
        return (Win11_21H2_COMMAND, Win11_22H2_COMMAND)
    def GetWindowRect(self):
        lpRect = RECT()
        ctypes.windll.user32.GetWindowRect(self.hwnd, ctypes.byref(lpRect))
        return lpRect
    def screenChangedHandler(self):
        hwnd = gethwnd(self.windowHandle())
        SWP_NOSIZE = 0x1
        SWP_NOMOVE = 0x2
        SWP_NOZORDER = 0x4
        SWP_FRAMECHANGED = 0x20
        ctypes.windll.user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOMOVE | SWP_NOZORDER | SWP_FRAMECHANGED)


class BlurWindow(CustomizedWindow):
    '''A blur window based on PySideX.
Blur effect is avaliable on Windows Vista and newer.'''
    def __init__(self):
        super(BlurWindow, self).__init__()
