from PySide6.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QWidget, QFileDialog)
from PySide6.QtGui import QPixmap, QImage, QShortcut, QKeySequence
from PySide6.QtCore import Qt, QTimer
from ui.menubar import MenuBar
from ui.toolbar import ToolBar
from ui.sidebar import SideBar
from core.filters import ImageFilters
from core.morphology import Morphology
from core.segmentation import Segmentation
from core.transforms import ImageTransform
import cv2
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.original_image = None
        self.processed_image = None
        self.current_operation = None
        self.angle = 0
        self.scale = 1.0
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_video_frame)

        self.left_shortcut = QShortcut(QKeySequence(Qt.Key_Left), self)
        self.right_shortcut = QShortcut(QKeySequence(Qt.Key_Right), self)
        self.up_shortcut = QShortcut(QKeySequence(Qt.Key_Up), self)
        self.down_shortcut = QShortcut(QKeySequence(Qt.Key_Down), self)
        self.left_shortcut.activated.connect(self.rotate_left)
        self.right_shortcut.activated.connect(self.rotate_right)
        self.up_shortcut.activated.connect(self.zoom_in)
        self.down_shortcut.activated.connect(self.zoom_out)

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
        self.sidebar.gaussian.clicked.connect(lambda : self.set_operation("Gaussian"))
        self.sidebar.laplacian.clicked.connect(lambda : self.set_operation("Laplacian"))
        self.sidebar.canny.clicked.connect(lambda : self.set_operation("Canny"))
        self.sidebar.median.clicked.connect(lambda : self.set_operation("Median"))
        self.sidebar.sobel.clicked.connect(lambda : self.set_operation("Sobel"))
        self.sidebar.blur.clicked.connect(lambda : self.set_operation("Blur"))
        self.sidebar.bilateral.clicked.connect(lambda : self.set_operation("Bilateral"))
        self.sidebar.grayscale.clicked.connect(lambda : self.set_operation("GrayScale"))

        ##Morphology
        self.sidebar.dilate.clicked.connect(lambda : self.set_operation("Dilate"))
        self.sidebar.erode.clicked.connect(lambda : self.set_operation("Erode"))
        self.sidebar.gradient.clicked.connect(lambda : self.set_operation("Gradient"))
        self.sidebar.tophat.clicked.connect(lambda : self.set_operation("Tophat"))

        ##Segmentation
        self.sidebar.threshold.clicked.connect(lambda : self.set_operation("Threshold"))
        self.sidebar.adaptive.clicked.connect(lambda : self.set_operation("Adaptive"))
        self.sidebar.kmeans.clicked.connect(lambda : self.set_operation("K-Means"))

        ##Transform
        self.sidebar.rotate.clicked.connect(lambda : self.set_operation("Rotate"))
        self.sidebar.resiz.clicked.connect(lambda : self.set_operation("Resize"))
        self.sidebar.perspective.clicked.connect(lambda : self.set_operation("Perspective"))

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
                                              "Images (*.mp4 *.avi *.mov)")
        
        if (file):
            self.cap = cv2.VideoCapture(file)
            self.timer.start(30)

    def update_video_frame(self):
        if self.cap is None:
            return
        
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()

            if not ret:
                return
        
        self.original_image = frame
        self.show_image(self.original_image, self.original_label)
        processed = self.process_frame(frame)
        self.show_image(processed, self.processed_label)

    
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
        if label == self.original_label:
            pixmap = pixmap.scaled(label.size(),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        else:
            pixmap = pixmap.scaled(
            int(pixmap.width() * self.scale),
            int(pixmap.height() * self.scale),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
            )
        
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

    def apply_transform(self, operation):
        if self.original_image is None:
            return
        
        operation = operation.text()

        if operation == "Rotate":
            self.processed_image = ImageTransform.rotate(self.original_image)

        elif operation == "Resize":
            self.processed_image = ImageTransform.resize(self.original_image)

        elif operation == "Perspective":
            self.processed_image = ImageTransform.perspective(self.original_image)

        self.show_image(self.processed_image, self.processed_label)

    def rotate_left(self):
        if self.original_image is None:
            return
        
        self.angle -= 10
        self.processed_image = ImageTransform.rotate(self.original_image, self.angle)
        self.show_image(self.processed_image, self.processed_label)

    def rotate_right(self):
        if self.original_image is None:
            return
        self.angle += 10
        self.processed_image = ImageTransform.rotate(self.original_image, self.angle)
        self.show_image(self.processed_image, self.processed_label)

    def zoom_in(self):
        if self.original_image is None:
            return
        self.scale += 0.1
        self.processed_image = ImageTransform.resize(self.original_image, self.scale)
        self.show_image(self.processed_image, self.processed_label)

    def zoom_out(self):
        if self.original_image is None:
            return
        self.scale -= 0.1
        if self.scale < 0.1:
            self.scale = 0.1

        self.processed_image = ImageTransform.resize(self.original_image, self.scale)
        self.show_image(self.processed_image, self.processed_label)
    
    def set_operation(self, operation):
        self.current_operation = operation

        if self.original_image is None:
            result = self.process_frame(self.original_image)
            self.processed_image = result

            self.show_image(self.processed_image, self.processed_label)
    
    def process_frame(self, frame):
        if self.current_operation is None:
            return frame
        
        ## Filters
        if self.current_operation == "Gaussian":
            return ImageFilters.gaussian(frame)
        
        elif self.current_operation == "Laplacian":
            return ImageFilters.laplacian(frame)
        
        elif self.current_operation == "Canny":
            return ImageFilters.canny(frame)
        
        elif self.current_operation == "Median":
            return ImageFilters.median(frame)
        
        elif self.current_operation == "Sobel":
            return ImageFilters.sobel(frame)
        
        elif self.current_operation == "Blur":
            return ImageFilters.blur(frame)
        
        elif self.current_operation == "Bilateral":
            return ImageFilters.bilateral(frame)
        
        elif self.current_operation == "GrayScale":
            return ImageFilters.grayscale(frame)
        
        ## Morphology
        elif self.current_operation == "Dilate":
            return Morphology.dilate(frame)
        
        elif self.current_operation == "Erode":
            return Morphology.erode(frame)
        
        elif self.current_operation == "Gradient":
            return Morphology.gradient(frame)
        
        elif self.current_operation == "Tophat":
            return Morphology.tophat(frame)
        
        ## Segmentation
        elif self.current_operation == "Threshold":
            return Segmentation.threshold(frame)
        
        elif self.current_operation == "Adaptive":
            return Segmentation.adaptive(frame)
        
        elif self.current_operation == "K-Means":
            return Segmentation.kmeans(frame)
        
        ## Transform
        elif self.current_operation == "Rotate":
            return ImageTransform.rotate(frame)
        
        elif self.current_operation == "Resize":
            return ImageTransform.resize(frame)
        
        elif self.current_operation == "Perspective":
            return ImageTransform.perspective(frame)
        
        return frame