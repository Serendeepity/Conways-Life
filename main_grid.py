from PyQt5 import QtCore, QtGui, QtWidgets
from typing import Tuple, Set
import sys

LIVE = QtGui.QImage("images/bug.png")
DEAD = QtGui.QImage("images/white.png")


class Cell(QtWidgets.QWidget):
    clicked = QtCore.pyqtSignal(tuple)

    def __init__(self, x, y, live=False, *args, **kwargs):
        super(Cell, self).__init__(*args, **kwargs)

        self._flag = False

        self.setFixedSize(QtCore.QSize(16, 16))
        self.live = live
        self.pos = x, y

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, QtGui.QPixmap([DEAD, LIVE][self.live]))

    def reverse(self):
        self.live = not self.live
        self.update()

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        self.reverse()
        self.clicked.emit((self.pos, self.live))


class GridOfCells(QtWidgets.QWidget):
    touched = QtCore.pyqtSignal(int)

    def __init__(self, w, h, *args, **kwargs):
        super(GridOfCells, self).__init__(*args, **kwargs)
        self.lives = set()

        self.layout = QtWidgets.QGridLayout()
        self.layout.setSpacing(0)

        for x in range(w):
            for y in range(h):
                cell = Cell(y, x)
                cell.clicked.connect(self.cell_click)
                self.layout.addWidget(cell, y, x)

        self.setLayout(self.layout)

    @QtCore.pyqtSlot(tuple)
    def cell_click(self, e: Tuple[Tuple[int, int], bool]):
        if e[1]:
            self.lives.add(e[0])
        else:
            self.lives -= {e[0]}
        self.touched.emit(1)

    def renew(self, new_lives: Set[Tuple[int, int]]):
        cells_to_die = set()
        for old in self.lives:
            if old in new_lives:
                new_lives.remove(old)
            else:
                self.layout.itemAtPosition(*old).widget().reverse()
                cells_to_die.add(old)
        self.lives -= cells_to_die
        for new in new_lives:
            self.layout.itemAtPosition(*new).widget().reverse()
            self.lives.add(new)
        self.update()

    def reset(self):
        for live in self.lives:
            self.layout.itemAtPosition(*live).widget().reverse()
        self.lives = set()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    grid = GridOfCells(75, 50)
    grid.show()
    sys.exit(app.exec())
