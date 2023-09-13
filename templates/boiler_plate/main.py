## IMPORTS
if 'Imports':

    if 'Standard':
        import os, sys
        from datetime import datetime

    if 'Libraries':
        from n4s import fs, term, web, strgs

    if 'PyQt6':
        from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout,
                                    QLineEdit, QPushButton, QComboBox, QMessageBox, QTextEdit, QFileDialog, QMainWindow)
        from PyQt6.QtGui import QFont, QPalette, QColor
        from PyQt6.QtCore import Qt, QDir, QTimer

## SETTINGS
if 'Settings':

    ## APP INFO
    APP_NAME = "app"

    ## APP VERSION
    APP_VERSION = 1.0

    ## APP DEVS
    APP_DEVS = "need4swede"

    ## APP YEAR
    APP_YEAR = datetime.today().strftime("%Y")

## GLOBAL VARIABLES
if 'Global Variables':

    ## OS VERSION
    OS_VERSION = float(fs.system('info')[1])

    ## USER DIR
    USER = f"{QDir.homePath()}"

    ## SCREEN WIDTH
    SCREEN_WIDTH = ''

    ## SCREEN HEIGHT
    SCREEN_HEIGHT = ''

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        * {
            background-color: #333;
        }
        QWidget {
            font-size: 15px;
            border-radius: 4px;
        }
        QLabel {
            font-family: 'Sans Serif';
        }
        QToolTip {
            padding: 4px;
            border: 1px solid #bababa;
        }
        QStatusBar {
            font-size: 13px;
        }
        QStatusBar QPushButton {
            background-color: none;
            padding: 0 40px;
            color: #fff;
        }
        QStatusBar QPushButton:hover {
            background-color: none;
            color: #0078d4;
        }
        QLineEdit {
            padding: 4px 10px;
            margin-right: 10px;
            border: 2px solid #bababa;
            font-size: 16px;
            selection-background-color: #0078d4;
        }
        QLineEdit:hover {
            border-color: #808080;
        }
        QLineEdit:focus {
            border-color: #0078d4;
        }
        QMenu {
            border: 1px solid #bababa;
            padding: 5px;
        }
        QMenu::item {
            padding: 3px 25px;
            border-radius: 4px;
        }
        QMenu::item:selected {
            color: #fff;
            background-color: #0078d4;
        }
        QPushButton {
            font-size: 12px;
            width: 0px;
            height: 10px;
            padding: 0;
            color: #fff;
            border: none;
            background-color: #656565;
        }
        QPushButton:hover, QComboBox:hover {
            background-color: #097ed9;
        }
        QPushButton:pressed, QComboBox:pressed {
            background-color: #00477c;
        }
        QPushButton:disabled, QComboBox:disabled {
            background-color: #77b7e9;
        }
        QComboBox {
            padding: 5.5px 30px 5.5px 45px;
            color: #fff;
            border: none;
            background-color: #0078d4;
        }
        QComboBox::drop-down {
            border-radius: 0;
        }
        QComboBox:on {
            border-bottom-left-radius: 0;
            border-bottom-right-radius: 0;
        }
        QComboBox QAbstractItemView {
            border-radius: 0;
            outline: 0;
        }
        QComboBox QAbstractItemView::item {
            height: 33px;
            padding-left: 42px;
            background-color: #fff;
        }
        QComboBox QAbstractItemView::item:selected {
            background-color: #0078d4;
        }
        QProgressBar {
            text-align: center;
        }
        QProgressBar::chunk {
            background: #0078d4;
            border-radius: 4px;
        }
        QMessageBox QLabel {
            font-size: 13px;
        }
        QMessageBox QPushButton {
            width: 60px;
            padding: 6px 8px;
        }
    ''')
    app.setFont(QFont('Helvetica Nue'))
    app.setStyleSheet("QLabel{font-family: 'Helvetica Nue';}")
    main_window = MainWindow()
    sys.exit(app.exec())