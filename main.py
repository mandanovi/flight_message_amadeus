from gui import FlightReader
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication
import sys


load_dotenv()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FlightReader()
    ex.show()
    sys.exit(app.exec_())

