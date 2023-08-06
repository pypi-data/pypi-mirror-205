import sys
from PySide2.QtWidgets import QApplication,QMainWindow
from PySide2.QtCore import Qt

class EditorWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        s = super().__init__(*args, **kwargs)
        self.setWindowTitle("Editor")

# Singleton
class EditorApp(QApplication):
    window=None
    ## object.__call__ is object()(), not object() unlike type()
    def __new__(cls, *args, **kwargs):
        if cls.instance()==None:
            _instance = super().__new__(cls,sys.argv)
        else:
            _instance = cls.instance()
        _instance.setAttribute(Qt.AA_CompressHighFrequencyEvents, False)
        _instance.setAttribute(Qt.AA_CompressTabletEvents, False)
        _instance.setAttribute(Qt.AA_SynthesizeTouchForUnhandledMouseEvents, False)
        _instance.setAttribute(Qt.AA_SynthesizeMouseForUnhandledTouchEvents, False)
        _instance.setAttribute(Qt.AA_SynthesizeMouseForUnhandledTabletEvents, False)
        return _instance
    def __init__(self, *args, **kwargs):
        if self.window==None:
            super().__init__(sys.argv)
            self.window = EditorWindow()
