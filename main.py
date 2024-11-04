import sys
from PyQt5.QtWidgets import QApplication
from modules.intro import Intro

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Show the intro screen first
    intro = Intro()
    sys.exit(app.exec_())
