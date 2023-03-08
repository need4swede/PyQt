import sys
from time import sleep
from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from PyQt6.QtWidgets import (QApplication, QWidget,
                                QHBoxLayout, QGridLayout,
                                    QLabel, QPushButton, QProgressBar)


######## GLOBAL VARIABLES ####################
SCREEN_WIDTH = ''                             # SCREEN WIDTH
SCREEN_HEIGHT = ''                            # SCREEN HEIGHT
COUNT = 0                                     # GLOBAL COUNT
##############################################

## THREAD HANDLER
class ThreadClass(QtCore.QThread):

    ## INITIALIZE SIGNALS
    int_signal = QtCore.pyqtSignal(int)
    string_signal = QtCore.pyqtSignal(str)

    ## INITIALIZE CLASS
    def __init__(self, parent=None, index=0):
        super(ThreadClass, self).__init__(parent)

        ## GET INDEX NUMBER
        self.index = index

        ## GET INDEX NAME
        self.index_name = index
        if self.index == 1:
            self.index_name = 'Progress Bar'
        if self.index == 2:
            self.index_name = 'Timer'

        ## SET RUN FLAG
        self.is_running = True

    ## RUNNING THE THREAD
    def run(self):

        ## PRINT START OF THREAD
        print('\nStarting - Thread:', self.index_name + '\n')

        if self.index_name == 'Progress Bar':

            ## IMPORT GLOBAL VARIABLE
            global COUNT

            ## ASSIGN GLOBAL VALUE TO LOCAL VARIABLE
            count = COUNT

            ## WHILTE RUN FLAG IS TRUE
            while (True):

                ## IF GLOBAL COUNT
                if COUNT > 99:
                    COUNT = 0

                ## INCRAMENT COUNTER
                count += 1
                COUNT += 1

                ## ARBITRARY DELAY FOR PROGRESS BAR
                sleep(0.05)

                ## SEND VARIABLE VALUE TO THE FUNCTION THE THREAD IS ASSIGNED TO
                self.int_signal.emit(count)

                ## ONCE THE COUNT LIMIT IS REACHED
                if count > 99:

                    ## RESET VALUE SENT TO FUNCTION
                    self.int_signal.emit(count)

                    ## STOP FUNCTION FROM RUNNING
                    MainWindow.progress_bar_stop()

                    ## MARK TASK AS COMPLETE
                    MainWindow.counter.setText(f'Task Complete')

        if self.index_name == 'Timer':

            ## INITIALIZE COUNT
            count = 0

            ## WHILE RUN FLAG IS TRUE
            while (True):

                ## WAIT A SECOND
                sleep(1)

                ## INCRIMENT COUNT
                count += 1

                ## SEND VARIABLE VALUE TO THE FUNCTION THE THREAD ASSIGNED TO
                self.int_signal.emit(count)

    ## STOPPING THE THREAD
    def stop(self):

        ## UPDATE GLOBAL RUN FLAG
        self.is_running = False

        ## PRINT STOPPING OF THREAD
        print('\nStopping - Thread:', self.index_name + '\n')

        ## TERMINATE THREAD
        self.terminate()

## MAIN APPLICATION
class MainWindow(QWidget):

    ## INITIALIZE APPLICATION & GUI
    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)

        ## KEEP WINDOW ON TOP
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)

        ## GET SCREEN DIMENSIONS
        screen = QApplication.primaryScreen()
        rect = screen.availableGeometry()
        self.screen_width = rect.width()
        self.screen_height = rect.height()

        ## UPDATE GLOBAL SCREEN DIMENSIONS
        global SCREEN_WIDTH, SCREEN_HEIGHT
        SCREEN_WIDTH = self.screen_width
        SCREEN_HEIGHT = self.screen_height

        ## ON WINDOW CLOSE
        app.aboutToQuit.connect(self.quit)

        ## INITIALIZE THREADS
        self.thread = {}

        ## RUN FLAGS
        self.progress_bar_running = False
        self.timer_running = False

        ## INITIALIZE GUI
        self.build_layout()

    ## INITIALIZE LAYOUT
    def set_layout(self):

        ## INITIALIZE LAYOUT
        self.layout = QHBoxLayout()

        ## SET LAYOUT
        self.setLayout(self.layout)

        ## DISPLAY GUI
        self.show()

    ## CONSTRUCT LAYOUT WIDGETS
    def build_layout(self):

        ## CREATE LAYOUT
        self.set_layout()

        ## LEFT SECTION
        leftSection = QGridLayout()
        if 'Section Widgets':

            ## CONSTRUCT WIDGETS
            if 'Progress Bar Buttons':
                self.btn_start_pbar = QPushButton('Start')
                self.btn_stop_pbar = QPushButton('Stop'); self.btn_stop_pbar.setEnabled(False)
                self.btn_reset_pbar = QPushButton('Reset'); self.btn_reset_pbar.setEnabled(False)

            ## WIDGET ACTIONS
            if 'Progress Bar Buttons':
                self.btn_start_pbar.clicked.connect(self.progress_bar_start)
                self.btn_stop_pbar.clicked.connect(self.progress_bar_stop)
                self.btn_reset_pbar.clicked.connect(self.progress_bar_reset)

            ## ADD WIDGETS TO LAYOUT
            if 'Progress Bar Buttons':
                leftSection.addWidget(self.btn_start_pbar)
                leftSection.addWidget(self.btn_stop_pbar)
                leftSection.addWidget(self.btn_reset_pbar)

        ## RIGHT SECTION
        rightSection = QGridLayout()
        if 'Section Widgets':

            ## CONSTRUCT WIDGETS
            self.progress_bar_1 = QProgressBar()
            self.counter = QLabel('')

            ## RESIZE WIDGETS
            self.progress_bar_1.setFixedSize(250, 30)
            self.counter.setAlignment(Qt.AlignmentFlag.AlignBaseline | Qt.AlignmentFlag.AlignHCenter)

            ## ADD WIDGETS TO LAYOUT
            rightSection.addWidget(self.progress_bar_1); rightSection.addWidget(self.counter)

        ## BUILD LAYOUT
        self.layout.addLayout(leftSection)
        self.layout.addSpacing(10)
        self.layout.addLayout(rightSection)

    ## PROGRESS BAR (FUNCTION)
    def emit_number_signal(self, number):

        ## GET THREAD INDEX
        index = self.sender().index

        ## PROGRESS BAR
        if index == 1:

            ## ASSIGN NUMBER VARIABLE
            count = number

            ## PERFORM TASKS
            self.progress_bar_1.setValue(count)
            self.counter.setText(f'{str(count)}%')

        ## TIMER
        if index == 2:

            ## ASSIGN NUMBER VARIABLE
            count = number
            if count == 1:
                print(f'Time Elapsed: {count} Second')
            else:
                print(f'Time Elapsed: {count} Seconds')

    ## PROGRESS BAR (START)
    def progress_bar_start(self):

        ## ASSIGN PROGRESS BAR TO THREAD[1]
        self.thread[1] = ThreadClass(parent=None, index=1)

        ## START THREAD
        self.thread[1].start()

        ## CONNECT SIGNAL
        self.thread[1].int_signal.connect(self.emit_number_signal)

        ## UPDATE RUN FLAG
        self.progress_bar_running = True

        ## UPDATE BUTTONS
        self.btn_start_pbar.setEnabled(False)
        self.btn_stop_pbar.setEnabled(True)
        self.btn_reset_pbar.setEnabled(False)

    ## PROGRESS BAR (STOP)
    def progress_bar_stop(self):

        ## IMPORT GLOBAL VARIABLE
        global COUNT

        ## STOP THREAD AT INDEX 1
        self.thread[1].stop()

        ## UPDATE BUTTON WIDGETS
        self.btn_start_pbar.setEnabled(True)
        self.btn_stop_pbar.setEnabled(False)
        self.btn_reset_pbar.setEnabled(True)

        ## UPDATE RUN FLAG
        self.progress_bar_running = False

        ## UPDATE LABEL WIDGET
        if COUNT <= 99:
            self.counter.setText(f'Task Stopped')

    ## PROGRESS BAR (RESET)
    def progress_bar_reset(self):

        ## IMPORT GLOBAL VARIABLE
        global COUNT

        ## RESET GLOBAL VARIABLE VALUE
        COUNT = 0

        ## RESET PROGRESS BAR VALUE
        self.progress_bar_1.setValue(COUNT)

        ## RESET COUNTER VALUE
        self.counter.setText('')

        ## DISABLE RESET BUTTON
        self.btn_reset_pbar.setEnabled(False)

    ## QUIT APP
    def quit(self):

        ## CHECK IF PROGRESS BAR IS RUNNING
        if self.progress_bar_running:

            ## TERMINATE THREAD
            self.thread[1].stop()

        ## CHECK IF TIMER IS RUNNING
        if self.timer_running:

            ## TERMINATE THREAD
            self.thread[2].stop()

        ## CLOSE APP
        self.close()


## RUN
if __name__ == '__main__':

    ## INITIALIZE QAPP AND SET STYLESHEET
    app = QApplication(sys.argv)

    ## START MAIN WINDOW
    MainWindow = MainWindow()
    MainWindow.show()

    ## START TIMER
    MainWindow.thread[2] = ThreadClass(parent=None, index=2)
    MainWindow.thread[2].start()
    MainWindow.thread[2].int_signal.connect(MainWindow.emit_number_signal)
    MainWindow.timer_running = True

    ## EXEC
    sys.exit(app.exec())