from PySide6.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QWidget, QFileDialog)
from PySide6.QtCore import Qt
from ui.menubar import MenuBar
from ui.toolbar import ToolBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Processing Studio')
        self.resize(1400,800)
        self.setup_ui()
        self.create_menu()
        self.create_toolbar()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        ## Creating image panels
        viewer_layout = QHBoxLayout()

        self.original_label = QLabel("Original Label")
        self.processed_label = QLabel("Processed Label")

        self.original_label.setAlignment(Qt.AlignCenter)
        self.processed_label.setAlignment(Qt.AlignCenter)
        self.original_label.setMinimumSize(600,600)
        self.processed_label.setMinimumSize(600,600)
        self.original_label.setStyleSheet("""border : 2px solid gray;""")
        self.processed_label.setStyleSheet("""border : 2px solid gray;""")

        viewer_layout.addWidget(self.original_label)
        viewer_layout.addWidget(self.processed_label)
        main_layout.addLayout(viewer_layout)

    def open_image(self):
        file, _ = QFileDialog.getOpenFileName(self,
                                              "Open Image",
                                              "",
                                              "Images (*.png, *.jpg, *.jpeg)")
        
        if (file):
            print(file)

    def open_video(self):
        file, _ = QFileDialog.getOpenFileName(self,
                                              "Open Image",
                                              "",
                                              "Images (*.mp4, *.avi, *.mov)")
        
        if (file):
            print(file)

    
    def create_menu(self):
        self.menu = MenuBar(self)
        self.setMenuBar(self.menu)

    def create_toolbar(self):
        self.toolbar = ToolBar()
        self.addToolBar(self.toolbar)
        self.toolbar.open_image.triggered.connect(self.open_image)
        self.toolbar.open_video.triggered.connect(self.open_video)