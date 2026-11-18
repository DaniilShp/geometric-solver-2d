import logging

from cad_graphics_scene import QDMGraphicsScene
from cad_graphics_dot import *
from cad_graphics_line import *

logger = logging.getLogger("scene")

class Scene():

    def __init__(self):
        self.dots = []
        self.lines = []

        self.scene_width = 64000
        self.scene_height = 64000

        self.initUI()

    def initUI(self):
        self.grScene = QDMGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def find_dot_by_uuid(self, uuid):
        for dot in self.dots:
            if dot.uuid == uuid:
                return dot
        return None
    
    def find_line_by_uuid(self, uuid):
        for line in self.lines:
            if line.uuid == uuid:
                return line
        return None
    
    # experimental
    # def add_dot(self, dot):
    #     from 

    def addDot(self, dot):
        self.dots.append(dot)
        logger.debug("Point added to scene uuid=%s", dot.uuid)
        return dot

    def addLine(self, line):
        self.lines.append(line)
        logger.debug("Segment added to scene uuid=%s", line.uuid)
        return line

    def removeDot(self, uuid):
        dot = self.find_dot_by_uuid(uuid)
        if self.dotHasLine(dot):
            for line in self.lines:
                if line.start_dot == dot or line.end_dot == dot:
                    logger.warning(
                        "Cannot remove point uuid=%s: it belongs to segment uuid=%s",
                        uuid,
                        line.uuid,
                    )
                    break
            return
        
        self.dots.remove(dot)
        self.grScene.removeItem(dot.grNode)
        logger.debug("Point removed from scene uuid=%s", uuid)

    def dotHasLine(self, dot):
        for line in self.lines:
            if line.start_dot == dot or line.end_dot == dot:
                return True
        return False

    def removeLine(self, uuid):
        line = self.find_line_by_uuid(uuid)
        if line is None:
            logger.warning("Segment uuid=%s not found", uuid)
            return

        self.lines.remove(line)
        self.grScene.removeItem(line.grLine)
        logger.debug("Segment removed from scene uuid=%s", uuid)


    def removeItems(self, items):
        for item in items:
            if isinstance(item, QDMGraphicsDot):
                self.removeDot(item.uuid)
            if isinstance(item, QDMGraphicsLine):
                self.removeLine(item.uuid)