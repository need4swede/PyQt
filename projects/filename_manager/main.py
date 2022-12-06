import os, webbrowser
from n4s import fs, term, strgs
from sys import executable as python_executable, argv as python_argv, exit as python_exit
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication, QStatusBar, QRadioButton, QCheckBox, QMenuBar, QMenu, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QFileDialog, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QCursor, QShortcut, QKeySequence
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

## RUN CHANGES
class ChangeFileName():

    ## INITIALIZE WINDOW
    def __init__(self):
        super().__init__()

    ## ADD TEXT TO EACH FILE
    def add_text(file_dir, file_rename):

        ## ITERATE THROUGH NESTED DIRECTORIES
        if MainWindow.checkbox_nested_dirs.isChecked():

            ## ITERATE THROUGH DIRECTORIES WITHIN INPUT DIR
            for i in range(MainWindow.dirs_count):

                ## LIST OF FILES WITHIN DIRECTORY
                file_list = sorted(fs.read_dir(MainWindow.dirs_list[i], 'files'))

                ## COUNT OF FILES WITHIN DIRECTORY
                file_count = fs.read_dir(MainWindow.dirs_list[i], 'file_count')

                ## RENAME FILES
                for file in range(file_count):
                    fs.rename(f"{MainWindow.dirs_list[i]}/{file_list[file]}", f"{fs.read_format(file_list[file], True, Read_Filename=True)}{file_rename}", False)
        
        ## SINGLE DIRECTORY, ITERATE THROUGH FILES ONLY
        else:

            ## LIST OF FILES WITHIN DIRECTORY
            file_list = sorted(fs.read_dir(file_dir, 'files'))

            ## COUNT OF FILES WITHIN DIRECTORY
            file_count = fs.read_dir(file_dir, 'file_count')

            ## RENAME FILES
            for file in range(file_count):
                fs.rename(f"{file_dir}/{file_list[file]}", f"{fs.read_format(file_list[file], True, Read_Filename=True)}{file_rename}", False)

    ## REMOVE TEXT FROM EACH FILE
    def remove_text(file_dir, file_rename):

        ## ITERATE THROUGH NESTED DIRECTORIES
        if MainWindow.checkbox_nested_dirs.isChecked():

            ## ITERATE THROUGH DIRECTORIES WITHIN INPUT DIR
            for i in range(MainWindow.dirs_count):

                ## LIST OF FILES WITHIN DIRECTORY
                file_list = sorted(fs.read_dir(MainWindow.dirs_list[i], 'files'))

                ## COUNT OF FILES WITHIN DIRECTORY
                file_count = fs.read_dir(MainWindow.dirs_list[i], 'file_count')

                ## RENAME FILES
                for file in range(file_count):
                    fs.rename(f"{MainWindow.dirs_list[i]}/{file_list[file]}", strgs.filter_text(file_list[file], [file_rename]))
        
        ## SINGLE DIRECTORY, ITERATE THROUGH FILES ONLY
        else:

            ## LIST OF FILES WITHIN DIRECTORY
            file_list = sorted(fs.read_dir(file_dir, 'files'))

            ## COUNT OF FILES WITHIN DIRECTORY
            file_count = fs.read_dir(file_dir, 'file_count')

            ## RENAME FILES
            for file in range(file_count):
                fs.rename(f"{file_dir}/{file_list[file]}", strgs.filter_text(file_list[file], [file_rename]))

## TEXT INPUT WINDOW
class TextInput(QWidget):

    ## INITIALIZE WINDOW
    def __init__(self, input_dir):
        super().__init__()

        ## WINDOW WIDTH
        self.setFixedWidth(300)

        ## WINDOW TITLE
        self.setWindowTitle('Filename Manager')

        ## INPUT DIR
        self.input_dir = input_dir

        ## CREATE SECTION
        self.layout = QVBoxLayout()

        ## CREATE TEXT WINDOW
        self.textBox = QLineEdit()
        self.textBox.setPlaceholderText("Type Something...")

        ## CREATE BUTTON
        self.button = QPushButton('Apply')
        self.button.clicked.connect(self.apply)

        ## KEEP WINDOW ON TOP
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.move(self.geometry().center())

        ## CREATE LAYOUT
        self.layout.addWidget(self.textBox)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        ## KEYBOARD SHORTCUTS
        self.shortcut_close = QShortcut(QKeySequence('Ctrl+m'), self)
        self.shortcut_close.activated.connect(lambda: self.close())
        self.apply = QShortcut(QKeySequence('Return'), self)
        self.apply.activated.connect(self.button.click)

        ## SHOW WINDOW
        self.show()

    ## APPLY TEXT CHANGES
    def apply(self):

        ## USER TEXT INPUT
        text_input = self.textBox.text()

        ## CHECK IF ADDING OR REMOVING TEXT
        if MainWindow.radio_add_text.isChecked():
            ChangeFileName.add_text(self.input_dir , self.textBox.text())
        if MainWindow.radio_remove_text.isChecked():
            ChangeFileName.remove_text(self.input_dir , self.textBox.text())

        ## CHECK IF CHOSEN DIRECTORY CAN BE ITERATED WITH AN INTEGER
        iterate_int = MainWindow.textBox.text().split(' ')[-1]
        try:
            iterate_int = int(iterate_int)
            iterate_int += 1
            iterate_int = str(iterate_int)
            MainWindow.textBox.setText(strgs.replace_text(Text=MainWindow.textBox.text(), Replace=MainWindow.textBox.text().split(' ')[-1], Replacement=iterate_int))
            MainWindow.button.click()
            # new_dir = strgs.replace_text(Text=MainWindow.textBox.text(), Replace=MainWindow.textBox.text().split(' ')[-1], Replacement=iterate_int)
            # self.repeat(new_dir, text_input)
        except Exception as error:
            pass
        clipboard.setText(text_input)
        self.close()

    ## ITERATE THROUGH DIRECTORIES
    def repeat(self, dir_input, text_input):
        self.new_window = TextInput(dir_input)
        self.new_window.textBox.setText(text_input)
        self.close()

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
        self.setWindowTitle('Filename Manager')
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
        self.radio_add_text = QRadioButton('Add Text', self)
        self.radio_add_text.move(45, 105)
        self.radio_add_text.setCursor(QCursor(Qt.CursorShape.DragCopyCursor))
        self.radio_add_text.setToolTip(
            "Only return a list of files")
        self.radio_add_text.show()

        self.radio_remove_text = QRadioButton('Remove Text', self)
        self.radio_remove_text.move(170, 105)
        self.radio_remove_text.setFixedWidth(125)
        self.radio_remove_text.setCursor(QCursor(Qt.CursorShape.DragCopyCursor))
        self.radio_remove_text.setToolTip(
            "Only return a list of directories")
        self.radio_remove_text.show()
        self.radio_remove_text.setChecked(True)

        self.checkbox_nested_dirs = QCheckBox('Nested Directories', self)
        self.checkbox_nested_dirs.move(15, 135)
        self.checkbox_nested_dirs.setFixedWidth(135)
        self.checkbox_nested_dirs.show()

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
        self.layout.addSpacing(55)
        self.layout.addLayout(self.middleSection)

        self.apply = QShortcut(QKeySequence('Return'), self)
        self.apply.activated.connect(self.button.click)

    ## RUN ACTION
    def run(self):

        ## INITIALIZE DIR SELECTION AND RESULT
        input_dir = self.textBox.text()

        ## SORT NAMES OF SUB DIRECTORIES WITHIN THE INPUT DIR
        self.dirs = sorted(fs.read_dir(Source=input_dir, Output='dirs'))

        ## COUNT SUB DIRECTORIES WITHIN THE INPUT DIR
        self.dirs_count = fs.read_dir(Source=input_dir, Output='dir_count')

        ## INITIALIZE SUB DIRECTORIES PATH LIST
        self.dirs_list = []

        ## ITERATE THROUGH SUB DIRECTORIES AND MAKE LIST OF FULL PATHS
        for x in range(self.dirs_count):
            self.dirs_list.append(f"{input_dir}/{self.dirs[x]}")

        ## LOAD INPUT WINDOW FOR INPUTING TEXT
        load_text_input = TextInput(input_dir)

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
    clipboard = app.clipboard()
    MainWindow = MainWindow()
    MainWindow.show()
    term.clear()
    python_exit(app.exec())