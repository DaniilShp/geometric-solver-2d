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
        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)

        self._pen.setWidthF(2.0)
        self._pen_selected.setWidthF(2.0)

        self.initUI()
        self.updatePath()

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)

    def boundingRect(self):
        margin = self._pen.widthF() / 2 + 1
        return self.path().boundingRect().adjusted(-margin, -margin, margin, margin)

    def paint(self, painter, option, widget = ...):
        painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path() )
       

    def updatePath(self):
        # raise NotImplemented("Implement")
        path = QPainterPath(QPointF(self._line.start_dot._x, self._line.start_dot._y))
        path.lineTo(self._line.end_dot._x, self._line.end_dot._y)
        self.setPath(path)