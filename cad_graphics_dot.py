from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class QDMGraphicsDot(QGraphicsItem):
    def __init__(self, dot, uuid, parent=None):
        super().__init__(parent)
        self.dot = dot
        print(dot._x, dot._y)

        self.uuid = uuid

        self.width = 10
        self.height = 10

        self._pen_default = QPen(QColor("#7F000000"))
        self._brush_default = QBrush(QColor("#FFF2F2F9"))

        self._pen_selected = QPen(QColor("#f5a623"))
        self._brush_selected = QBrush(QColor("#f5a623"))

        self._pen_highlighted = QPen(QColor("#00A8FF"))
        self._brush_highlighted = QBrush(QColor("#3300A8FF"))
        self._highlighted = False

        self.setPos(self.dot._x, self.dot._y)
        self.initUI()

    def boundingRect(self):
        # return QRectF(0, 0, self.width, self.height).normalized
        return QRectF(-self.width/2, -self.height/2, self.width, self.height).normalized()

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)

    # возможно стоит перенести эту логику в node_dot
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            self.dot._x = value.x()
            self.dot._y = value.y()
            self.dot.update_lines()
        return super().itemChange(change, value)

    @property 
    def x(self): return self.dot._x

    @x.setter
    def x(self, value):
        self.dot._x = value

    @property 
    def y(self): return self.dot._y

    @y.setter
    def y(self, value):
        self.dot._y = value

    def setHighlighted(self, highlighted):
        if self._highlighted == highlighted:
            return
        self._highlighted = highlighted
        self.update()

    def paint(self, painter, option, widget = ...):

        # paint dot

        path_outline = QPainterPath()
        # path_outline.addRoundedRect(0, 0, self.width, self.height, 1, 1) 
        path_outline.addEllipse(-self.width/2, -self.height/2, self.width, self.height)
        # path_outline.addEllipse(0, 0, self.width, self.height)
        if self.isSelected():
            painter.setPen(self._pen_selected)
            painter.setBrush(self._brush_selected)
        elif self._highlighted:
            painter.setPen(self._pen_highlighted)
            painter.setBrush(self._brush_highlighted)
        else:
            painter.setPen(self._pen_default)
            painter.setBrush(self._brush_default)
        painter.drawPath(path_outline.simplified())

        # return super().paint(painter, option, widget)