import sys
import os
from PyQt6 import uic
from PyQt6 import QtWidgets

MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
FORMS_DIR = os.path.join(MAIN_DIR, "forms")


class RunSpeedConverter(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.load_ui.loadUi(os.path.join(FORMS_DIR, 
                                        "run_speed_converter.ui"), self)

        self.minPerMileLE.textChanged.connect(self.select)
        self.mphLE.textChanged.connect(self.select)
        self.calculatePB.clicked.connect(self.calculate)
        self.resetPB.clicked.connect(self.reset)
        self.quitAction.triggered.connect(self.close)

    def select(self):
        if self.sender() is self.minPerMileLE:
            self.mphLE.clear()
        elif self.sender() is self.mphLE:
            self.minPerMileLE.clear()

    def calculate(self):
        min_per_mile = self.minPerMileLE.text()
        mph = self.mphLE.text()
        if min_per_mile != "":
            verify = self.verify_input_min_per_mile(min_per_mile)
            if verify:
                result = self.get_mph(min_per_mile)
                result = str(result)
                self.resultLE.setText(result)
                self.resultLB.setText("mph")
            else:
                return
        elif mph != "":
            verify = self.verify_input_mph(mph)
            if verify:
                min, sec = self.get_min_per_mile(mph)
                min = str(min)
                sec = str(sec)
                if len(sec) == 1:
                    sec = "0" + sec
                result = min + ":" + sec
                self.resultLE.setText(result)
                self.resultLB.setText("min per mile")
            else:
                return
        else:
            return

    def verify_input_min_per_mile(self, min_per_mile):
        try:
            time = min_per_mile.split(":")
            min = int(time[0])
            sec = int(time[1])
        except:
            QtWidgets.QMessageBox.warning(self, "Error", 
                                          "The input format is wrong")
            self.reset()
            return False
        if min < 0 or min > 60:
            QtWidgets.QMessageBox.warning(self, "Error", 
                                          "The input format is wrong")
            self.reset()
            return False
        elif sec < 0 or sec > 60:
            QtWidgets.QMessageBox.warning(self, "Error", 
                                          "The input format is wrong")
            self.reset()
            return False
        else:
            return True

    def verify_input_mph(self, mph):
        try:
            mph = float(mph)
        except:
            QtWidgets.QMessageBox.warning(self, "Error", 
                                          "The input format is wrong")
            self.reset()
            return False
        return True

    def get_mph(self, min_per_mile):
        time = min_per_mile.split(":")
        minutes = int(time[0])
        seconds = int(time[1])
        minutes = minutes + (seconds / 60)
        mph = 60 / minutes
        mph = round(mph, 2)
        return mph

    def get_min_per_mile(self, mph):
        min_per_mile = 60 / float(mph)
        minutes = int(min_per_mile)
        minutes_to_convert = min_per_mile - minutes
        seconds = minutes_to_convert * 60
        seconds = round(seconds)
        return minutes, seconds

    def reset(self):
        self.minPerMileLE.clear()
        self.mphLE.clear()
        self.resultLE.clear()
        self.resultLB.clear()
        self.minPerMileLE.setFocus()

    def closeEvent(self, event):
        event.accept()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = RunSpeedConverter()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
