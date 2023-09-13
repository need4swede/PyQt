## IMPORTS
if 'Imports':

    if 'Standard':
        import os, sys, csv, warnings, re, subprocess, platform
        from datetime import datetime

    if 'Libraries':
        try:
            from n4s import fs # pip install n4s
        except ImportError:
            print("\n'n4s' library not installed! Please install it via 'pip install n4s'\n")
            sys.exit()
        from openpyxl import load_workbook
        warnings.filterwarnings("ignore")

    if 'PyQt6':
        from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout,
                                    QLineEdit, QPushButton, QTextEdit, QFileDialog, QMainWindow)
        from PyQt6.QtGui import QPalette, QColor, QDragEnterEvent, QDropEvent
        from PyQt6.QtCore import Qt, QDir, QTimer

## SETTINGS
if 'Settings':

    ## APP INFO
    APP_NAME = "Aeries2Google"

    ## APP VERSION
    APP_VERSION = 1.0

    ## APP DEVS
    APP_DEVS = "need4swede"

    ## APP YEAR
    APP_YEAR = datetime.today().strftime("%Y")

    ## DOMAIN
    DOMAIN = "need4swede.net"

    ## PASSWORD
    PASSWORD = "need4swede"

    ## ORG UNIT
    ORG_UNIT = "/Students"

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

## SET UI THEMES
class ThemeHandler:

    ## SET THEME METHOD
    def set_theme(self, theme):

        ## CREATE PALETTE
        palette = QPalette()

        ## SET DARK THEME
        if theme.lower() == 'dark':
            ## THEME SETTINGS
            palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.black)
            palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
            palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.ColorRole.Highlight, Qt.GlobalColor.transparent)
            palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)

        ## APPLY THEME
        QApplication.setPalette(palette)


class FileDropLineEdit(QLineEdit):
    def __init__(self, file_type, *args, **kwargs):
        super(FileDropLineEdit, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.file_type = file_type

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        url = event.mimeData().urls()[0].toLocalFile()
        if url.endswith(self.file_type):
            self.setText(url)

class Application(QWidget, ThemeHandler):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.html_text = FileDropLineEdit('.html')
        self.css_text = FileDropLineEdit('.css')
        self.js_text = FileDropLineEdit('.js')

        layout.addLayout(self.create_file_input('HTML File:', self.html_text, '.html'))
        layout.addLayout(self.create_file_input('CSS File:', self.css_text, '.css'))
        layout.addLayout(self.create_file_input('JS File:', self.js_text, '.js'))

        self.combine_btn = QPushButton('Combine')
        self.combine_btn.clicked.connect(self.combine_files)

        layout.addWidget(self.combine_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
        self.setWindowTitle('File Combiner')
        self.show()

    def create_file_input(self, label, textbox, file_ext):
        layout = QHBoxLayout()
        label_widget = QLabel(label)
        btn = QPushButton('Browse')
        btn.clicked.connect(lambda: self.open_file_dialog(textbox, file_ext))

        layout.addWidget(label_widget)
        layout.addWidget(textbox)
        layout.addWidget(btn)

        return layout

    def open_file_dialog(self, textbox, file_ext):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", f"All {file_ext.upper()} Files (*{file_ext});;All Files (*)")
        if file_name:
            textbox.setText(file_name)

    def combine_files(self):
        html_path = self.html_text.text()
        css_path = self.css_text.text()
        js_path = self.js_text.text()

        if not all([html_path, css_path, js_path]):
            print("All files must be selected before combining")
            return

        try:
            with open(html_path, 'r') as html_file:
                html_content = html_file.read()

            with open(css_path, 'r') as css_file:
                css_content = css_file.read()

            with open(js_path, 'r') as js_file:
                js_content = js_file.read()

            css_injected = f"<style>\n{css_content}\n</style>"
            js_injected = f"<script>\n{js_content}\n</script>"

            index_head_end = html_content.lower().index('</head>')
            index_body_end = html_content.lower().index('</body>')

            combined_content = html_content[:index_head_end] + css_injected + html_content[index_head_end:index_body_end] + js_injected + html_content[index_body_end:]

            output_path = '/'.join(html_path.split('/')[:-1]) + '/combined.html'
            with open(output_path, 'w') as output_file:
                output_file.write(combined_content)

            print(f"Files combined successfully. Output saved as {output_path}")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec())


