from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from main_grid import GridOfCells
from engine import infinite_generation, next_step
from typing import Tuple, Set


class Worker(QtCore.QThread):
    step_done = QtCore.pyqtSignal(set)

    def __init__(self, data: Set[Tuple[int, int]], speed=1):
        super(Worker, self).__init__()
        self.data = data
        self.speed = speed

    def run(self):
        for step in infinite_generation(self.data):
            ans = set()
            ans |= step
            self.step_done.emit(ans)
            self.msleep(1000 // self.speed)


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, w, h):
        super(MyWindow, self).__init__()
        self.setWindowTitle("Conway's Life")
        self.container = QtWidgets.QWidget(self)

        h_box = QtWidgets.QHBoxLayout()
        h_box.setSpacing(30)
        v_box = QtWidgets.QVBoxLayout()

        self.widget1 = QtWidgets.QWidget(self.container)
        self.widget1.setObjectName("lives")
        self.formLayout_1 = QtWidgets.QFormLayout(self.widget1)
        self.formLayout_1.setContentsMargins(1, 1, 1, 1)
        self.formLayout_1.setObjectName("formLayout_1")
        self.label_1 = QtWidgets.QLabel(self.widget1)
        self.label_1.setObjectName("label_1")
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(50)
        self.label_1.setFont(font)
        self.label_1.setText("LIVES")
        self.formLayout_1.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_1)
        self.lcdNumber_1 = QtWidgets.QLCDNumber(3, self.widget1)
        self.lcdNumber_1.setObjectName("lcdLives")
        self.lcdNumber_1.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.formLayout_1.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lcdNumber_1)

        self.widget2 = QtWidgets.QWidget(self.container)
        self.widget2.setObjectName("Age")
        self.formLayout_2 = QtWidgets.QFormLayout(self.widget2)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget2)
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(font)
        self.label_2.setText("AGE")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.widget2)
        self.lcdNumber_2.setObjectName("lcdAge")
        self.lcdNumber_2.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lcdNumber_2)

        self.button_0 = QtWidgets.QPushButton()
        self.button_0.setObjectName('Start')
        self.button_0.setText('Start')
        self.button_0.clicked.connect(self.start)

        self.button_1 = QtWidgets.QPushButton()
        self.button_1.setObjectName('Step')
        self.button_1.setText('Step')
        self.button_1.clicked.connect(self.one_step)

        self.button_3 = QtWidgets.QPushButton()
        self.button_3.setObjectName('Reset')
        self.button_3.setText('Reset')
        self.button_3.clicked.connect(self.reset)

        self.speed_ruler = QtWidgets.QDial()
        self.speed_ruler.setMinimum(1)
        self.speed_ruler.setMaximum(10)
        self.speed_ruler.setSingleStep(1)
        self.speed_ruler.setValue(5)
        self.speedometer = QtWidgets.QLabel('SPEED')
        self.speedometer.setFont(font)
        self.speed_value = QtWidgets.QLCDNumber(2)
        self.speed_value.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.widget3 = QtWidgets.QWidget(self.container)
        self.formLayout_3 = QtWidgets.QFormLayout(self.widget3)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.speedometer)
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.speed_value)
        self.speed_value.display(5)
        self.speed_ruler.valueChanged.connect(self.set_speed)
        self.speed = 5

        h_box.addWidget(self.widget1)
        h_box.addWidget(self.widget2)
        h_box.addWidget(self.widget3)
        h_box.addWidget(self.speed_ruler)
        h_box.addWidget(self.button_0)
        h_box.addWidget(self.button_1)
        h_box.addWidget(self.button_3)

        self.grid = GridOfCells(w, h)
        self.grid.touched.connect(self.start_count)

        v_box.addLayout(h_box)
        v_box.addWidget(self.grid)
        self.container.setLayout(v_box)

        self.setCentralWidget(self.container)

        self.thread = None

    def start_count(self):
        self.lcdNumber_1.display(len(self.grid.lives))

    def set_speed(self, e):
        self.speed_value.display(e)
        self.speed = e

    def update_interface(self, new_data):
        self.grid.renew(new_data)
        self.lcdNumber_2.display(self.lcdNumber_2.value() + 1)
        self.lcdNumber_1.display(len(self.grid.lives))
        self.grid.update()

    def one_step(self):
        new = next_step(self.grid.lives)
        self.update_interface(new)

    def start(self):
        if self.thread:
            self.thread.terminate()
            self.thread = None
            self.button_0.setText("Start")
        else:
            self.thread = Worker(self.grid.lives, self.speed)
            self.thread.step_done.connect(self.update_interface)
            self.thread.start()
            self.button_0.setText("Stop")

    def reset(self):
        self.grid.reset()
        self.lcdNumber_1.display(0)
        self.lcdNumber_2.display(0)


app = QtWidgets.QApplication([])
application = MyWindow(75, 50)
application.show()

sys.exit(app.exec())
