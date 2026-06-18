from PySide6.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QWidget, QFileDialog)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
from ui.menubar import MenuBar
from ui.toolbar import ToolBar
from ui.sidebar import SideBar
from core.filters import ImageFilters
from core.morphology import Morphology
from core.segmentation import Segmentation
import cv2
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.original_image = None
        self.processed_image = None
        self.setWindowTitle('Image Processing Studio')
        self.resize(1400,800)
        self.setup_ui()
        self.create_menu()
        self.create_toolbar()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout()
        central.setLayout(main_layout)

        ## Creating image panels
        image_layout = QHBoxLayout()

        self.original_label = QLabel("Original Label")
        self.processed_label = QLabel("Processed Label")

        self.original_label.setAlignment(Qt.AlignCenter)
        self.processed_label.setAlignment(Qt.AlignCenter)
        self.original_label.setMinimumSize(600,600)
        self.processed_label.setMinimumSize(600,600)
        self.original_label.setStyleSheet("""border : 2px solid gray;""")
        self.processed_label.setStyleSheet("""border : 2px solid gray;""")

        image_layout.addWidget(self.original_label)
        image_layout.addWidget(self.processed_label)

        ## Sidebar
        self.sidebar = SideBar()

        ##Filters
        self.sidebar.gaussian.clicked.connect(lambda : self.apply_filters(self.sidebar.gaussian))
        self.sidebar.laplacian.clicked.connect(lambda : self.apply_filters(self.sidebar.laplacian))
        self.sidebar.canny.clicked.connect(lambda : self.apply_filters(self.sidebar.canny))
        self.sidebar.median.clicked.connect(lambda : self.apply_filters(self.sidebar.median))
        self.sidebar.sobel.clicked.connect(lambda : self.apply_filters(self.sidebar.sobel))
        self.sidebar.blur.clicked.connect(lambda : self.apply_filters(self.sidebar.blur))
        self.sidebar.bilateral.clicked.connect(lambda : self.apply_filters(self.sidebar.bilateral))
        self.sidebar.grayscale.clicked.connect(lambda : self.apply_filters(self.sidebar.grayscale))

        ##Morphology
        self.sidebar.dilate.clicked.connect(lambda : self.apply_morphlogy(self.sidebar.dilate))
        self.sidebar.erode.clicked.connect(lambda : self.apply_morphlogy(self.sidebar.erode))
        self.sidebar.gradient.clicked.connect(lambda : self.apply_morphlogy(self.sidebar.gradient))
        self.sidebar.tophat.clicked.connect(lambda : self.apply_morphlogy(self.sidebar.tophat))

        ##Segmentation
        self.sidebar.threshold.clicked.connect(lambda : self.apply_segment(self.sidebar.threshold))
        self.sidebar.adaptive.clicked.connect(lambda : self.apply_segment(self.sidebar.adaptive))
        self.sidebar.kmeans.clicked.connect(lambda : self.apply_segment(self.sidebar.kmeans))

        main_layout.addWidget(self.sidebar)
        main_layout.addLayout(image_layout)

    def open_image(self):
        file, _ = QFileDialog.getOpenFileName(self,
                                              "Open Image",
                                              "",
                                              "Images (*.png, *.jpg, *.jpeg)")
        
        if (file):
            img = cv2.imread(file)
            if img is None:
                return
            self.original_image = img
            self.show_image(self.original_image, self.original_label)

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

    def show_image(self, image, label):
        if (len(image.shape) == 2):
            height, width = image.shape
            bytes_per_line = width
            qImage = QImage(image.data,
                            width,
                            height,
                            bytes_per_line,
                            QImage.Format_Grayscale8
                            )
            
        else:
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, channel = rgb.shape
            bytes_per_line = channel * width
            qImage = QImage(rgb.data,
                            width,
                            height,
                            bytes_per_line,
                            QImage.Format_RGB888)
            
        pixmap = QPixmap.fromImage(qImage)
        pixmap = pixmap.scaled(label.size(),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        
        label.setPixmap(pixmap)

    def apply_filters(self, item):
        if self.original_image is None:
            return
        
        name = item.text()

        if name == "Gaussian":
            self.processed_image = ImageFilters.gaussian(self.original_image)

        elif name == "Laplacian":
            self.processed_image = ImageFilters.laplacian(self.original_image)

        elif name == "Canny":
            self.processed_image = ImageFilters.canny(self.original_image)

        elif name == "Median":
            self.processed_image = ImageFilters.median(self.original_image)

        elif name == "Sobel":
            self.processed_image = ImageFilters.sobel(self.original_image)

        elif name == "Blur":
            self.processed_image = ImageFilters.blur(self.original_image)

        elif name == "Bilateral":
            self.processed_image = ImageFilters.bilateral(self.original_image)
        
        elif name == "GrayScale":
            self.processed_image = ImageFilters.grayscale(self.original_image)

        self.show_image(self.processed_image, self.processed_label)

    def apply_morphlogy(self, operation):
        if self.original_image is None:
            return
        
        operation = operation.text()
        if operation == 'Dilate':
            self.processed_image = Morphology.dilate(self.original_image)
        
        elif operation == 'Erode':
            self.processed_image = Morphology.erode(self.original_image)

        elif operation == 'Gradient':
            self.processed_image = Morphology.gradient(self.original_image)

        elif operation == 'Tophat':
            self.processed_image = Morphology.tophat(self.original_image)

        self.show_image(self.processed_image, self.processed_label)

    def apply_segment(self, operation):
        if self.original_image is None:
            return
        
        operation = operation.text()
        if operation == "Threshold":
            self.processed_image = Segmentation.threshold(self.original_image)

        elif operation == "Adaptive":
            self.processed_image = Segmentation.adaptive(self.original_image)

        elif operation == "K-Means":
            self.processed_image = Segmentation.kmeans(self.original_image)

        self.show_image(self.processed_image, self.processed_label)