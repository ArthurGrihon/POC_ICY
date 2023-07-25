import sys
from PyQt5.QtWidgets import QApplication
from mainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()       
    sys.exit(app.exec_())
        
#### CONTINUE UPDATE ICY CODE CHANGES FOR SAPCER WIDGET REMOVAL ####