from PySide6.QtWidgets import QMenuBar

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.create_menu()

    def create_menu(self):
        self.addMenu("File")
        self.addMenu("Edit")
        self.addMenu("View")
        self.addMenu("Help")