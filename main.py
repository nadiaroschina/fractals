import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import math

X = 1500
Y = 700
N = 3


class Point():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __len__(self):
        return int(math.sqrt(self.x ** 2 + self.y ** 2))

    def rotate_60(self):
        cos = 0.5
        sin = math.sqrt(3) / 2
        x1 = self.x * cos + self.y * sin
        y1 = -self.x * sin + self.y * cos
        return Point(x1, y1)

    def rotate_90(self):
        x1 = self.y
        y1 = -self.x
        return Point(x1, y1)

    def rotate_120(self):
        cos = -0.5
        sin = math.sqrt(3) / 2
        x1 = self.x * cos + self.y * sin
        y1 = -self.x * sin + self.y * cos
        return Point(x1, y1)

    def __mul__(self, a):
        return Point(self.x * a, self.y * a)

    def __truediv__(self, a):
        return Point(self.x / a, self.y / a)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


class KochWidget(QWidget):
    global N

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.A = Point()
        self.P = Point()
        e = 30
        h = self.height()
        w = self.width()
        if w < h:
            self.A = Point(e, h / 2)
            self.P = Point(w / 2, h / 2)
        else:
            self.A = Point(w / 2 - h / 2 + e, h / 2)
            self.P = Point(w / 2, h / 2)
        self.n = N
        self.r = len(self.A - self.P)
        self.saved = Point()
        self.mouse = Point()
        self.prev_w = self.width()
        self.prev_h = self.height()

    def set_AP(self):

        v = Point(self.r, 0)
        self.A = self.P - v

    def set_N(self, value):

        self.n = value
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.set_AP()
        self.koch_snowflake(self.n, self.A, self.P, painter)
        painter.end()

    def koch_curve(self, n, A, B, painter):
        if n == 0:
            painter.drawLine(A.x, A.y, B.x, B.y)
        else:
            C = (A * 2) / 3 + B / 3
            E = (B * 2) / 3 + A / 3
            v = E - C
            D = C + v.rotate_60()
            self.koch_curve(n - 1, A, C, painter)
            self.koch_curve(n - 1, C, D, painter)
            self.koch_curve(n - 1, D, E, painter)
            self.koch_curve(n - 1, E, B, painter)

    def koch_snowflake(self, n, A, P, painter):
        v1 = A - P
        v2 = v1.rotate_120()
        v3 = v2.rotate_120()
        B = P + v2
        C = P + v3
        self.koch_curve(n, B, A, painter)
        self.koch_curve(n, C, B, painter)
        self.koch_curve(n, A, C, painter)

    def resizeEvent(self, event):
        w = self.width()
        h = self.height()
        self.P = Point(self.P.x * w / self.prev_w, self.P.y * h / self.prev_h)
        self.repaint()
        self.prev_w = w
        self.prev_h = h

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0 or self.r > 0:
            self.r += event.angleDelta().y() / 100
        self.repaint()

    def mousePressEvent(self, event):
        self.mouse = Point(event.x(), event.y())
        self.saved = self.P

    def mouseMoveEvent(self, event):
        v = Point(event.x(), event.y())
        self.P = self.saved - self.mouse + v
        self.repaint()


class IceTriangleWidget(QWidget):
    global N

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.A = Point()
        self.P = Point()
        e = 30
        h = self.height()
        w = self.width()
        if w < h:
            self.A = Point(e, h / 2)
            self.P = Point(w / 2, h / 2)
        else:
            self.A = Point(w / 2 - h / 2 + e, h / 2)
            self.P = Point(w / 2, h / 2)
        self.n = N
        self.r = len(self.A - self.P)
        self.saved = Point()
        self.mouse = Point()
        self.prev_w = self.width()
        self.prev_h = self.height()

    def set_AP(self):
        v = Point(self.r, 0)
        self.A = self.P - v

    def set_N(self, value):
        self.n = value
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.set_AP()
        self.ice_triangle(self.n, self.A, self.P, painter)
        painter.end()

    def ice_curve(self, n, A, B, painter):
        if n == 0:
            painter.drawLine(A.x, A.y, B.x, B.y)
        else:
            M = (A + B) / 2
            v = (B - M) * 4 / 10
            v1 = v.rotate_60()
            v2 = v.rotate_120()
            C = M + v1
            D = M + v2
            self.ice_curve(n - 1, A, M, painter)
            self.ice_curve(n - 1, M, B, painter)
            self.ice_curve(n - 1, M, C, painter)
            self.ice_curve(n - 1, M, D, painter)
            self.ice_curve(n - 1, C, M, painter)
            self.ice_curve(n - 1, D, M, painter)

    def ice_triangle(self, n, A, P, painter):
        v1 = A - P
        v2 = v1.rotate_120()
        v3 = v2.rotate_120()
        B = P + v2
        C = P + v3
        self.ice_curve(n, B, A, painter)
        self.ice_curve(n, A, B, painter)
        self.ice_curve(n, C, B, painter)
        self.ice_curve(n, B, C, painter)
        self.ice_curve(n, A, C, painter)
        self.ice_curve(n, C, A, painter)

    def resizeEvent(self, event):
        w = self.width()
        h = self.height()
        self.P = Point(self.P.x * w / self.prev_w, self.P.y * h / self.prev_h)
        self.repaint()
        self.prev_w = w
        self.prev_h = h

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0 or self.r > 0:
            self.r += event.angleDelta().y() / 100
        self.repaint()

    def mousePressEvent(self, event):
        self.mouse = Point(event.x(), event.y())
        self.saved = self.P

    def mouseMoveEvent(self, event):
        v = Point(event.x(), event.y())
        self.P = self.saved - self.mouse + v
        self.repaint()


class IceRectangleWidget(QWidget):
    global N

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.A = Point()
        self.P = Point()
        h = self.height()
        w = self.width()
        e = min(h, w) * 2 / 10 + 30
        if w < h:
            self.A = Point(e, h / 2 - w / 2 + e)
            self.P = Point(w / 2, h / 2)
        else:
            self.A = Point(w / 2 - h / 2 + e, e)
            self.P = Point(w / 2, h / 2)
        self.n = N
        self.r = len(self.P - self.A)
        self.saved = Point()
        self.mouse = Point()
        self.prev_w = self.width()
        self.prev_h = self.height()

    def set_AP(self):
        r_2 = self.r * math.sqrt(2) / 2
        v = Point(r_2, r_2)
        self.A = self.P - v

    def set_N(self, value):

        self.n = value
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.set_AP()
        self.ice_rectangle(self.n, self.A, self.P, painter)
        painter.end()

    def ice_curve(self, n, A, B, painter):
        if n == 0:
            painter.drawLine(A.x, A.y, B.x, B.y)
        else:
            M = (A + B) / 2
            v = (B - M) * 2 / 3
            v1 = v.rotate_90()
            C = M + v1
            self.ice_curve(n - 1, A, M, painter)
            self.ice_curve(n - 1, M, B, painter)
            self.ice_curve(n - 1, M, C, painter)
            self.ice_curve(n - 1, C, M, painter)

    def ice_rectangle(self, n, A, P, painter):
        v1 = A - P
        v2 = v1.rotate_90()
        v3 = v2.rotate_90()
        v4 = v3.rotate_90()
        B = P + v2
        C = P + v3
        D = P + v4
        self.ice_curve(n, B, A, painter)
        self.ice_curve(n, A, B, painter)
        self.ice_curve(n, C, B, painter)
        self.ice_curve(n, B, C, painter)
        self.ice_curve(n, D, C, painter)
        self.ice_curve(n, C, D, painter)
        self.ice_curve(n, D, A, painter)
        self.ice_curve(n, A, D, painter)

    def resizeEvent(self, event):
        w = self.width()
        h = self.height()
        self.P = Point(self.P.x * w / self.prev_w, self.P.y * h / self.prev_h)
        self.repaint()
        self.prev_w = w
        self.prev_h = h

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0 or self.r > 0:
            self.r += event.angleDelta().y() / 100
        self.repaint()

    def mousePressEvent(self, event):
        self.mouse = Point(event.x(), event.y())
        self.saved = self.P

    def mouseMoveEvent(self, event):
        v = Point(event.x(), event.y())
        self.P = self.saved - self.mouse + v
        self.repaint()


class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.resize(X, Y)
        self.setMinimumSize(400, 200)
        self.setWindowTitle("Happy new year!")
        self.KochWidget = KochWidget(self)
        self.KochWidget.close()
        self.IceTriangleWidget = IceTriangleWidget(self)
        self.IceTriangleWidget.close()
        self.IceRectangleWidget = IceRectangleWidget(self)
        self.IceRectangleWidget.close()
        self.fractal_type = 0
        self.show_widget()

    def set_fractal_type(self, fractal_type):
        self.fractal_type = fractal_type
        self.show_widget()

    def show_widget(self):

        if self.fractal_type == 0:
            self.KochWidget.show()
            self.IceTriangleWidget.close()
            self.IceRectangleWidget.close()
        if self.fractal_type == 1:
            self.IceTriangleWidget.show()
            self.KochWidget.close()
            self.IceRectangleWidget.close()
        if self.fractal_type == 2:
            self.IceRectangleWidget.show()
            self.KochWidget.close()
            self.IceTriangleWidget.close()

        self.KochWidget.setGeometry(0, 50, self.width(), self.height() - 50)
        self.IceTriangleWidget.setGeometry(0, 50, self.width(), self.height() - 50)
        self.IceRectangleWidget.setGeometry(0, 50, self.width(), self.height() - 50)

    def resizeEvent(self, event):
        self.KochWidget.setGeometry(0, 50, self.width(), self.height() - 50)
        self.IceTriangleWidget.setGeometry(0, 50, self.width(), self.height() - 50)
        self.IceRectangleWidget.setGeometry(0, 50, self.width(), self.height() - 50)


app = QApplication(sys.argv)
Window = MyWindow()

spinbox = QSpinBox(Window)
spinbox.setMaximum(8)
spinbox.setValue(N)
spinbox.setWindowTitle("Iterations")
spinbox.setGeometry(10, 10, 80, 40)

spinbox.valueChanged.connect(Window.KochWidget.set_N)
spinbox.valueChanged.connect(Window.IceTriangleWidget.set_N)
spinbox.valueChanged.connect(Window.IceRectangleWidget.set_N)

combobox = QComboBox(Window)
combobox.setGeometry(100, 10, 250, 40)
combobox.addItems(["Koch snowflake", "Ice triangle", "Ice rectangle"])

combobox.currentIndexChanged.connect(Window.set_fractal_type)

Window.show()
app.exec_()