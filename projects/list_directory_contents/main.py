import os, webbrowser
from n4s import fs, term
from sys import executable as python_executable, argv as python_argv, exit as python_exit
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QStatusBar, QPlainTextEdit, QRadioButton, QMenuBar, QMenu, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QFileDialog, QVBoxLayout, QHBoxLayout, QCheckBox
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
- Radio Buttons
- Child Window
- Directory Browser

CREDITS:
Mike Afshari (need4swede)
https://mafshari.work
https://github.com/need4swede
'''

## NEW WINDOW
class DirectoryContents(QWidget):
    """
    This window displays the contents of your directory
    """
    def __init__(self, text):
        super().__init__()

        ## KEEP WINDOW ON TOP
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)

        ## WINDOW CONTENTS
        layout = QVBoxLayout()
        self.label = QPlainTextEdit()
        self.label.setFixedSize(800, 400)
        self.label.setPlainText(text)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.show()

## MAIN APPLICATION 
class MainWindow(QWidget):

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
        self.setWindowTitle('List Directory Contents')
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(15, 15, 15, 0)
        self.setFixedHeight(200)
        self.setFixedWidth(315)
        self.setLayout(self.layout)

        ############################################################################## LAYOUT SECTIONS
        ############################################################# MENU BAR
        self.menuBar = QMenuBar()
        self.fileMenu = QMenu('File')
        self.menuBar.addMenu(self.fileMenu)
        self.fileMenu.addAction(' &New Text File', lambda: fs.system('app-textedit'))

        self.helpMenu = QMenu('Help')
        self.menuBar.addMenu(self.helpMenu)
        self.helpMenu.addAction(' &Developer Info', lambda: webbrowser.open('https://www.mafshari.work'))

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
        self.textBoxPlaceholderText = 'Directory Path...'
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
        self.radio_select_files = QRadioButton('Files ONLY', self)
        self.radio_select_files.move(15, 105)
        self.radio_select_files.setCursor(QCursor(Qt.CursorShape.DragCopyCursor))
        self.radio_select_files.setToolTip(
            "Only return a list of files")
        self.radio_select_files.show()

        self.radio_select_dirs = QRadioButton('Folders ONLY', self)
        self.radio_select_dirs.move(120, 105)
        self.radio_select_dirs.setCursor(QCursor(Qt.CursorShape.DragCopyCursor))
        self.radio_select_dirs.setToolTip(
            "Only return a list of directories")
        self.radio_select_dirs.show()

        self.radio_select_all = QRadioButton('Both', self)
        self.radio_select_all.move(245, 105)
        self.radio_select_all.setCursor(QCursor(Qt.CursorShape.DragCopyCursor))
        self.radio_select_all.setToolTip(
            "Return a list of files and directories")
        self.radio_select_all.show()
        self.radio_select_all.setChecked(True)

        ##################################################################################### BROWSE BUTTON
        self.browse_button = QPushButton('📂 Browse')
        self.browse_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.browse_button.clicked.connect(self.browse_dir)
        self.browse_button.setEnabled(True)
        self.browse_button.show()

        ################################################################################### LABELS
        self.credit = QLabel('PyQt6 Project | by Need4Swede')
        self.credit.setStyleSheet('font-size: 11px; font-weight: bold;')

        ##################################################################################### TOP SECTION
        self.topSection.addWidget(self.textBox)
        self.topSection.addWidget(self.quitBtn)
        self.topSection.addWidget(self.button)

        ################################################################################ METADATA SECTION
        self.mainLabels.addWidget(self.credit)
        self.middleSection.addLayout(self.mainLabels)

        ################################################################################ DOWNLOAD SECTION
        self.bottomSection.addLayout(self.centerButton)
        
        ################################################################################# OPTIONS SECTION
        self.additionalSection.setSizeGripEnabled(False)
        self.additionalSection.addPermanentWidget(self.browse_button)

        ################################################################################### CREATE LAYOUT
        self.layout.addLayout(self.topSection)
        self.layout.addWidget(self.browse_button)
        self.layout.addSpacing(25)
        self.layout.addLayout(self.middleSection)

    ## RUN ACTION
    def run(self):

        ## INITIALIZE DIR SELECTION AND RESULT
        dir_selection = self.textBox.text()
        result = ''

        ## APPLY USER SELECTION
        if self.radio_select_all.isChecked():
            results = fs.read_dir(dir_selection)
        elif self.radio_select_files.isChecked():
            results = fs.read_dir(dir_selection, Output='files')
        elif self.radio_select_dirs.isChecked():
            results = fs.read_dir(dir_selection, Output='dirs')
        
        ## ITERATE THROUGH LIST
        for x in range(len(results)):
            result = result + results[x] + "\n"

        ## SHOW RESULTS
        self.new_window = DirectoryContents(str(result))

    ## RESET GUI
    def reset(self):
        self.textBox.clear()

    ## BROWSE DIRECTORY
    def browse_dir(self):
        self.reset()
        path = str(QFileDialog.getExistingDirectory(self, "Browse Directory"))
        self.textBox.setText(path)

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
    if fs.system('is-mac'):
        app.setStyleSheet('{}')
    else:
        import qdarktheme
        app.setStyleSheet(qdarktheme.load_stylesheet())
    
    ## APP
    app_version = 1.0
    MainWindow = MainWindow()
    MainWindow.show()
    term.clear()
    python_exit(app.exec())