import os, webbrowser
from sys import executable as python_executable, argv as python_argv, exit as python_exit
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QStatusBar, QMenuBar, QMenu, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QFileDialog, QVBoxLayout, QHBoxLayout, QCheckBox
from PyQt6.QtGui import QCursor, QFont
from PyQt6.QtCore import Qt

'''
DESIGN:
- Vertically shaped window with stacked UI elements
- Capable of collapsing and expanding
- Always on top GUI

FUNCTIONALITY:
- Text Input
- Buttons
- Checkbox
- Child Window
- Directory Browser

CREDITS:
Mike Afshari (need4swede)
https://mafshari.work
https://github.com/need4swede
'''

## NEW WINDOW
class NewWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window.
    """
    def __init__(self, text):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel(text)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.label)
        self.setLayout(layout)

## MAIN APPLICATION 
class app_name(QWidget):

    ## INITIALIZE APPLICATION & GUI
    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)

        ################################################################################### GLOBAL FLAGS

        ## KEEP WINDOW ON TOP
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)

        ## GET SCREEN DIMENSIONS
        screen = QApplication.primaryScreen()
        rect = screen.availableGeometry()
        self.screen_width = rect.width()
        self.screen_height = rect.height()

        ## ON WINDOW CLOSE
        app.aboutToQuit.connect(self.quit)

        ################################################################################# PARENT LAYOUT
        self.setWindowTitle('app_name')
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(15, 15, 15, 10)
        self.setFixedHeight(400)
        self.setFixedWidth(315)
        self.setLayout(self.layout)

        ############################################################################## LAYOUT SECTIONS
        ############################################################# MENU BAR
        self.menuBar = QMenuBar()
        self.fileMenu = QMenu('File')
        self.menuBar.addMenu(self.fileMenu)
        self.fileMenu.addAction(' &Submenu1', lambda: print('File > Submenu1'))
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(' &Submenu2', lambda: print('File > Submenu2'))

        self.helpMenu = QMenu('Help')
        self.menuBar.addMenu(self.helpMenu)
        self.helpMenu.addAction(' &app_name Help', lambda: webbrowser.open('https://www.mafshari.work'))
        self.helpMenu.addAction(' &Full Changelog', lambda: webbrowser.open('https://www.mafshari.work'))
        self.helpMenu.addAction(' &Check for Updates', lambda: print('Checking for updates...'))

        ########################################################## TOP SECTION
        self.topSection = QHBoxLayout() # 
        
        ####################################################### MIDDLE SECTION
        self.middleSection = QHBoxLayout() # 
        self.mainLabels = QVBoxLayout() # 
        
        ################################################### ADDITIONAL SECTION
        self.additionalSection = QStatusBar() # 
        
        ####################################################### BOTTOM SECTION
        self.centerButton = QVBoxLayout() # 
        self.bottomSection = QHBoxLayout() # 
        
        ########################################################## MESSAGE BOX
        self.message = QMessageBox() # MESSAGE PROMPTS
        self.message.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.message.move(self.geometry().center())

        ###############################################################################################

        ###################################################################################### TEXT BOX
        self.textBox = QLineEdit()
        self.textBox.setFixedSize(140, 33)
        self.textBoxPlaceholderText = 'TextBox...'
        self.textBox.setPlaceholderText(self.textBoxPlaceholderText)

        ################################################################################# FETCH BUTTON
        self.button = QPushButton('Run')
        self.button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button.clicked.connect(self.run)

        ################################################################################## QUIT BUTTON
        self.quitBtn = QPushButton('Quit')
        self.quitBtn.setFixedSize(60,32)
        self.quitBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.quitBtn.clicked.connect(self.quit)

        ############################################################################### FLOATING TOOLS
        self.checkbox = QCheckBox('Checkbox', self)
        self.checkbox.move(225, 289)
        self.checkbox.setCursor(QCursor(Qt.CursorShape.DragCopyCursor))
        self.checkbox.setToolTip(
            "This is a tooltip!\n"
            "Here you can explain what this checkbox does to your users")
        self.checkbox.stateChanged.connect(lambda: self.checkbox_state(self.checkbox))
        self.checkbox.show()

        ##################################################################################### BROWSE BUTTON
        self.browse_button = QPushButton('📂 Browse')
        self.browse_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.browse_button.clicked.connect(self.browse_dir)
        self.browse_button.setEnabled(True)
        self.browse_button.show()

        #################################################################################### MINIMIZE APP
        self.minimize_button = QPushButton('Minimize')
        self.minimize_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.minimize_button.clicked.connect(self.minimize_window)
        self.minimize_button.show()

        ################################################################################### LABELS
        self.first_label = QLabel('Main Label')
        self.second_label = QLabel('Second Label')
        self.third_label = QLabel('Third Label')
        self.fourth_label = QLabel('Fourth Label')
        self.credit = QLabel('app_name | by Need4Swede')
        self.version = QLabel(f'Version {app_version}')
        self.credit.setStyleSheet('font-size: 11px; font-weight: bold;')
        self.version.setStyleSheet('''
            font-size: 10px; 
            background: none; 
            text-align: left; 
            padding: 0; 
            width: 2px;
            ''')

        ################################################################################# CENTER BUTTON
        self.center_button = QPushButton('Center Button')
        self.center_button.setFixedSize(120,32)
        self.center_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.center_button.setEnabled(False)
        self.center_button.clicked.connect(self.reset)
        self.center_button.show()

        ##################################################################################### TOP SECTION
        self.topSection.addWidget(self.textBox)
        self.topSection.addWidget(self.quitBtn)
        self.topSection.addWidget(self.button)

        ################################################################################ METADATA SECTION
        self.mainLabels.addWidget(self.first_label)
        self.mainLabels.addWidget(self.second_label)
        self.mainLabels.addWidget(self.third_label)
        self.mainLabels.addWidget(self.fourth_label)
        self.mainLabels.addWidget(self.credit)
        self.mainLabels.addWidget(self.version)
        self.middleSection.addLayout(self.mainLabels)

        ################################################################################ DOWNLOAD SECTION
        self.centerButton.addWidget(self.center_button)
        self.bottomSection.addLayout(self.centerButton)
        
        ################################################################################# OPTIONS SECTION
        self.additionalSection.setSizeGripEnabled(False)
        self.additionalSection.addPermanentWidget(self.browse_button)

        ################################################################################### CREATE LAYOUT
        self.layout.addLayout(self.topSection)
        self.layout.addLayout(self.middleSection)
        self.layout.addLayout(self.bottomSection)
        self.layout.addWidget(self.minimize_button)
        self.layout.addWidget(self.browse_button)
    
    ## RUN ACTION
    def run(self):

        ## IF TEXTBOX IS EMPTY, USE PLACEHOLDER TEXT
        if self.textBox.text() == '':
            self.new_window = NewWindow(self.textBoxPlaceholderText)
        else:
            self.new_window = NewWindow(self.textBox.text())

        ## SHOW NEW WINDOW
        self.new_window.show()

    ## RESET GUI
    def reset(self):
        self.textBox.clear()
        self.center_button.setEnabled(False)
        self.checkbox.setChecked(False)

    ## CHECKBOX STATE
    def checkbox_state(self, checkbox):
        if checkbox.isChecked():
            self.center_button.setEnabled(True)
        else:
            self.center_button.setEnabled(False)

    ## MINIMIZE APP WINDOW
    def minimize_window(self):

        ## MINIMIZE
        if self.minimize_button.text() == 'Minimize':
            self.textBox.hide()
            self.button.hide()
            self.first_label.hide()
            self.second_label.hide()
            self.third_label.hide()
            self.fourth_label.hide()
            self.credit.hide()
            self.version.hide()
            self.center_button.hide()
            self.browse_button.hide()
            self.setFixedHeight(70)
            self.layout.setContentsMargins(10,0,10,10)
            self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
            self.show()
            self.minimize_button.setText('Expand')
            return

        ## MAXIMIZE
        else:
            self.textBox.show()
            self.button.show()
            self.first_label.show()
            self.second_label.show()
            self.third_label.show()
            self.fourth_label.show()
            self.credit.show()
            self.version.show()
            self.center_button.show()
            self.browse_button.show()
            self.setFixedHeight(400)
            self.layout.setContentsMargins(15, 15, 15, 10)
            self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnBottomHint)
            self.show()
            self.minimize_button.setText('Minimize')
            return

    ## BROWSE DIRECTORY
    def browse_dir(self):
        ## NEW DL DIR
        path = str(QFileDialog.getExistingDirectory(self, "Browse Directory"))
        if path:
            ## GET APP DIR
            self.appDir = path
            self.browse_button.setToolTip(path)

    ## RESTART GUI
    def restart(self):
        python = python_executable
        os.execl(python, python, * python_argv)
    
    ## QUIT APP PROCESS
    def quit(self):
        app.exit()

## RUN APP
if __name__ == '__main__':

    ## INITIALIZE QAPP AND SET STYLESHEET
    app = QApplication(python_argv)
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
    
    ## APP
    app_version = 1.0
    app_name = app_name()
    app_name.show()
    python_exit(app.exec())