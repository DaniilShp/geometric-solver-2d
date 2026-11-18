from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class QDMGraphicsLine(QGraphicsPathItem):
    def __init__(self, line, uuid, parent=None):
        super().__init__(parent)

        self._line = line

        self.uuid = uuid

        self._color = QColor("#FFF2F2F9")
        self._color_selected = QColor("#FFFFA637")
        self._color_highlighted = QColor("#00A8FF")
        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)
        self._pen_highlighted = QPen(self._color_highlighted)

        self._pen.setWidthF(2.0)
        self._pen_selected.setWidthF(2.0)
        self._pen_highlighted.setWidthF(3.0)
        self._highlighted = False

        self.initUI()
        self.updatePath()

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)

    def setHighlighted(self, highlighted):
        if self._highlighted == highlighted:
            return
        self._highlighted = highlighted
        self.update()

    def boundingRect(self):
        margin = self._pen.widthF() / 2 + 1
        return self.path().boundingRect().adjusted(-margin, -margin, margin, margin)

    def paint(self, painter, option, widget = ...):
        if self.isSelected():
            painter.setPen(self._pen_selected)
        elif self._highlighted:
            painter.setPen(self._pen_highlighted)
        else:
            painter.setPen(self._pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path() )
       

    def updatePath(self):
        # raise NotImplemented("Implement")
        path = QPainterPath(QPointF(self._line.start_dot._x, self._line.start_dot._y))
        path.lineTo(self._line.end_dot._x, self._line.end_dot._y)
        self.setPath(path)