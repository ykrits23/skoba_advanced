# main.py (фрагмент — вставте перед імпортом MainWindow)
import sys

# --- реєструємо лоадери з app.core ---
from app.core import register_default_loaders
register_default_loaders()

from PyQt5.QtWidgets import QApplication
from app.gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
