from PySide6.QtWidgets import QToolBar
from PySide6.QtCore import QSize
from PySide6.QtGui import QAction

class ToolBar(QToolBar):
    def __init__(self):
        super().__init__()
        self.create_toolbar()

    def create_toolbar(self):
        self.open_image = QAction("Open Image", self)
        self.open_video = QAction("Open Video", self)
        self.camera = QAction("Camera", self)
        self.save = QAction("Save", self)
        self.yolo = QAction("Yolo", self)
        self.exit = QAction("Exit", self)
        self.addAction(self.open_image)
        self.addAction(self.open_video)
        self.addAction(self.camera)
        self.addAction(self.save)
        self.addAction(self.yolo)
        self.addAction(self.exit)