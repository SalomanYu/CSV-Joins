from PyQt5 import QtCore
from PyQt5.QtCore import QFile, QSize, QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QCursor
import sys, os
from concatenation import startConcatenation


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Concat')
        self.setFixedSize(500,200)

        wid = QWidget(self)
        self.setCentralWidget(wid)
        self.layout = QVBoxLayout()
        wid.setLayout(self.layout)

        self.setupUI()

    def setupUI(self):
        self.aboutLabel = QLabel('This application will join csv files into one csv file.')
        self.aboutLabel.setWordWrap(True)
        self.aboutLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.filedialogButton = QPushButton('Select folder')
        self.filedialogButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.filedialogButton.clicked.connect(self.selectFolder)
        
        self.layout.addWidget(self.aboutLabel)
        self.layout.addStretch(1)
        # self.layout.addStretch(0)
        self.layout.addWidget(self.filedialogButton)


    
    def selectFolder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder = QFileDialog.getExistingDirectory(self, 'Select folder with tables',)
        if folder:
            self.convert(folder)

    def convert(self, name):
        self.HBox = QHBoxLayout()
        self.label = QLabel(f'<u>You choice</u> {name}', self)
        self.label.setWordWrap(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.entry = QLineEdit(self)
        self.entry.setAlignment(QtCore.Qt.AlignCenter)
        self.entry.setPlaceholderText('Write filename')

        self.concatenationButton = QPushButton('Start')
        self.concatenationButton.setCursor(QtCore.Qt.PointingHandCursor)
        self.concatenationButton.clicked.connect(lambda x: self.start(name))
        self.concatenationButton.setShortcut('Enter')

        self.layout.addWidget(self.label)
        # self.layout.addStretch(1)
        self.layout.addStretch(0)
        self.layout.addWidget(self.entry)

        
        self.HBox.addWidget(self.filedialogButton)
        self.HBox.addWidget(self.concatenationButton)
        self.layout.addLayout(self.HBox)
        # self.layout.addWidget(self.concatenationButton)
        self.layout.addStretch(0)

    
    def start(self, path):
        tabooSymbols = ('/', ';', ':', '*', '?', '|')
        filename = self.entry.text()
        if any((symbol in tabooSymbols) for symbol in filename):
            QMessageBox.about(self, 'Error', "You are using forbidden characters in the file name.\nThe file name should not contain the following characters ('/', ';', ':', '*', '?', '|')")
            self.entry.clear()
        elif len(filename) < 1:
            QMessageBox.about(self, 'Error', 'Uncorrect file name')

        else:
            os.chdir(path)
            result = startConcatenation(filename)

            if result == 'success':
                QMessageBox.about(self, 'Success', 'The files joined successfully!')
                sys.exit()
            else:
                QMessageBox.about(self, 'Failed', 'An error has occurred. Check the folder for csv files')
                self.entry.clear()


app = QApplication(sys.argv)
runner = App()
with open('style.css') as file:
    style = file.read()

runner.setStyleSheet(style)
runner.show()
sys.exit(app.exec_())