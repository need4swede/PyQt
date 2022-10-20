
######## IMPORTS ##############################
from n4s import fs, web, term, strgs
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QPlainTextEdit,
                                QVBoxLayout, QWidget, QProgressBar)
from PyQt6.QtCore import QProcess, QThread, pyqtSignal
import sys, time, multiprocessing, os
###############################################

## 1. SET THE NAME OF YOUR APPLICATION (CHANGE '_app_exe' IF NAME IS DIFFERENT THAN '_app_name')

######## GLOBAL VARIABLES #####################
# NAME OF APPLICATION
_app_name = "MyApp"
# NAME OF EXE
if fs.system('is-mac'):
    _app_exe = f"{_app_name}.app" 
else:
    _app_exe = f"{_app_name}.exe"
# UNINSTALLATION FLAG
_uninstall = False
###############################################

## 2. SET THE DIRECTORIES OF YOUR APPLICATION

######## APP DIRECTORIES ######################
if fs.system('is-mac'):
    _app_network_dir = "/Volumes/MyApplications"
    _app_local_dir = fs.root('apps')
    _app_icon = f"{_app_network_dir}/icon.icns"
else:
    _app_network_dir = r"\\192.168.XX.XX\MyApplications"
    _app_local_dir = f"{fs.root('userlib')}\Roaming\{strgs.clean_text(_app_name, Remove_Spaces=True)}\\app"
    _app_icon = f"{_app_network_dir}\icon.ico"
###############################################

## SENDS PROGRESS BAR SIGNAL TO MAIN WINDOW
class ProgressBarThread(QThread):
    _signal = pyqtSignal(int)
    def __init__(self):
        super(ProgressBarThread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        for i in range(100):
            if _uninstall:
                time.sleep(0.03)
            else:
                time.sleep(0.06)
            self._signal.emit(i)

## MAIN APPLICATION
class MainWindow(QMainWindow):

    ## INITIALIZE WINDOW
    def __init__(self):
        super().__init__()

        ## WINDOW TITLE
        self.setWindowTitle("Application Installer")

        ## SET HEIGHT
        self.setFixedHeight(120)

        ## HANDLE EXIT
        app.aboutToQuit.connect(lambda: app.quit())

        ## IMPORT GLOBAL VARIABLES
        global _uninstall

        ## TASK SET TO NONE
        self.task = None
        self.app_installed = False

        ## INSTALL BUTTON
        self.install_btn = QPushButton()

        ## UNINSTALL BUTTON
        self.uninstall_btn = QPushButton(f"Uninstall {_app_name}")

        ## INSTALLATION BUTTON - INSTALL (WINDOWS)
        if not fs.system('is-mac') and not fs.path_exists(f"{_app_local_dir}\\{_app_exe}"):
            self.install_btn.setText(f"Install {_app_name}")
            self.uninstall_btn.hide()
        
        ## INSTALLATION BUTTON - INSTALL (MAC)
        elif fs.system('is-mac') and not fs.path_exists(f"{_app_local_dir}/{_app_exe}"):
            self.install_btn.setText(f"Install {_app_name}")
            self.uninstall_btn.hide()

        ## INSTALLATION BUTTON - UPDATE
        else:
            self.install_btn.setText(f"Update {_app_name}")
            self.uninstall_btn.show()
            self.app_installed = True
        
        ## INSTALLATION BUTTON - SET ACTIONS
        self.install_btn.pressed.connect(self.start_installation)
        self.uninstall_btn.pressed.connect(self.start_uninstallation)

        ## WINDOW TEXT PROMPTS
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)

        ## PROGRESS BAR
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)

        ## CREATE LAYOUT
        self.layout = QVBoxLayout()

        ## ADD INSTALL BUTTON
        self.layout.addWidget(self.install_btn)

        ## ADD UNINSTALL BUTTON
        if self.app_installed:
            self.layout.addWidget(self.uninstall_btn)
            self.setFixedHeight(160)
        
        ## ADD PROGRESS BAR
        self.layout.addWidget(self.progress)

        ## ADD WINDOW TEXT PROMPTS
        self.layout.addWidget(self.text)

        ## SET LAYOUT
        w = QWidget()
        w.setLayout(self.layout)
        self.setCentralWidget(w)

    ## HANDLE TEXT PROMPTS
    def message(self, s):
        self.text.appendPlainText(s)

    ## HANDLE PROGRESS BAR
    def update_progressbar(self, msg):

        ## IMPORT GLOBAL VARIABLES
        global _uninstall

        ## CONSTRUCT PROGRESS BAR VALUES
        self.progress.setValue(int(msg))

        ## INSTALL PROMPT
        if self.progress.value() == 23:
            if not _uninstall:
                if not fs.path_exists(f"{_app_local_dir}\\{_app_exe}"):
                    self.message("Installing...")
                else:
                    self.message("Installing updates (if any)...")
            else:
                self.message("Removing app...")
        
        ## VERIFYING PROMPT
        if self.progress.value() == 98:
            self.message("Verifying...")
        
        ## RUN INSTALLER / UNINSTALLER
        if self.progress.value() == 99:
            if not _uninstall:
                self.run_installer()
                self.message("Installation Complete!")
            else:
                self.run_uninstaller()
                self.message("App has been removed!")

            ## SET TASK BACK TO 'NONE'
            self.task = None

            ## UPDATE INSTALL BUTTON
            self.install_btn.setText('Exit Installer')
            self.install_btn.pressed.connect(app.quit)
            self.install_btn.setEnabled(True)

            ## RESET PROGRESS BAR
            self.progress.setValue(0)

    ## START INSTALLATION TASK
    def start_installation(self):
        if self.task is None:  # No process running.
            self.thread = ProgressBarThread()
            self.thread._signal.connect(self.update_progressbar)
            self.install_btn.setEnabled(False)
            self.uninstall_btn.setEnabled(False)
            self.thread.start()
            self.message("Gathering Files...")
            self.task = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.

    ## SET INSTALL TO UNINSTALL
    def start_uninstallation(self):

        ## IMPORT GLOBAL VARIABLES
        global _uninstall

        ## UPDATE GLOBAL VARIABLE
        _uninstall = True

        ## BEGIN INSTALL PROCESS
        self.start_installation()

    ## CREATE DESKTOP SHORTCUT
    def createShortcut(self, target='', name='App', icon=''):
        '''
        path: Output
        target: exe to make shortcut of
        name: name of shortcut
        icon: app icon
        '''

        ## WINDOWS ONLY
        if not fs.system('is-mac'):

            ## IMPORTS
            import win32com.client

            ## SET DESKTOP
            desktop = fs.root('desktop')

            ## SET OUTPUT PATH
            path = os.path.join(desktop, f'{name}.lnk')

            ## CREATE SHORTCUT
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.IconLocation = icon
            shortcut.WindowStyle = 7 # 7 - Minimized, 3 - Maximized, 1 - Normal
            shortcut.save()

    ## INSTALL TASK
    def run_installer(self):

        ## VERIFY NETWORK CONNECTIVITY (FILE IS HOSTED ON SERVER)
        if web.network_test():

            ## MAC
            if fs.system("is-mac") and fs.path_exists(_app_network_dir):

                ## COPY TO 'DOCUMENTS' DIR
                fs.copy_file(f"{_app_network_dir}/{_app_exe}", fs.root('apps'), overwrite=True)

            ## WINDOWS
            elif fs.path_exists(_app_network_dir):

                ## CREATE APP DIR IN 'APPDATA\ROAMING'
                fs.path_exists(f"{fs.root('userlib')}\Roaming\{strgs.clean_text(_app_name, Remove_Spaces=True)}", Make=True)

                ## CREATE DIR FOR EXE INSIDE APP DIR
                fs.path_exists(_app_local_dir, Make=True)

                ## COPY APP TO NEW EXE DIR
                fs.copy_file(f"{_app_network_dir}\{_app_exe}", _app_local_dir, overwrite=True)

                ## REMOVE OLD DESKTOP SHORTCUT
                if fs.path_exists(f"{fs.root('desktop')}\{_app_name}.lnk"):
                    fs.remove_file(f"{fs.root('desktop')}\{_app_name}.lnk")
                    term.wait(2)
                
                ## CREATE DESKTOP SHORTCUT
                self.createShortcut(f"{_app_local_dir}\{_app_exe}", _app_name, _app_icon)

    ## UNINSTALL TASK
    def run_uninstaller(self):
        if fs.system('is-mac'):
            fs.remove_file(f"{fs.root('apps')}/{_app_exe}")
        else:
            fs.remove_dir(f"{fs.root('userlib')}\Roaming\{strgs.clean_text(_app_name, Remove_Spaces=True)}")
            fs.remove_file(f"{fs.root('desktop')}\{_app_name}.lnk")

## RUN
if __name__ == '__main__':
    
    ## REQUIRED FOR MULTI-THREADED WORKFLOW
    multiprocessing.freeze_support()
    
    ## MAIN APPLICATION
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()