"""task_1.py"""


import sys
import os
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox


class JsonPlaceholderApp(QMainWindow):
    """JSON request app"""

    def __init__(self):
        """init method"""
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """init ui method"""
        self.setGeometry(100, 100, 300, 200)

        self.label = QLabel(
            'Нажмите кнопку, чтобы выполнить запрос и сохранить объекты', self)
        self.label.adjustSize()

        self.btn_request = QPushButton('Выполнить запрос', self)
        self.btn_request.clicked.connect(self.make_request)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_request)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def make_request(self):
        """request make method"""
        try:
            response = requests.get(
                'https://jsonplaceholder.typicode.com/posts', timeout=60)
            if response.status_code == 200:
                posts = response.json()
                self.save_to_folder(posts)
                QMessageBox.information(
                    self, 'Объекты сохранены в папку "json_data"', QMessageBox.StandardButton.Ok)
            else:
                QMessageBox.warning(
                    self, 'Не выполнен запрос', QMessageBox.StandardButton.Ok)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(
                self, f'Произошла ошибка запроса: {e}', QMessageBox.StandardButton.Ok)

    def save_to_folder(self, data):
        """save file to folder

        Args:
            data (json): JSON data
        """
        folder_name = 'json_data'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        with open(os.path.join(folder_name, 'posts.json'), 'w', encoding="utf-8") as f:
            f.write(str(data))


def main():
    """main method"""
    app = QApplication(sys.argv)
    window = JsonPlaceholderApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
