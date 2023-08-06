from PySide6.QtCore import QRect

import numpy as np
import mss as m


class Screeny:

    def __init__(self):
        """
        Initializing variables of the class.
        """
        self.mss = m.mss()
        self.monitor = self.mss.monitors[1]

    def take_screenshot(self, rect: QRect = None):
        """
        Makes a screenshot of the complete monitor or a given area.

        :param rect:    Rectangular area where the screenshot will be taken.
        :return:        Image as a numpy-array.
        """
        if rect == None:
            img = np.array(self.mss.grab(self.monitor))
        else:
            img = np.array(self.mss.grab((rect.x(), rect.y(), rect.width(), rect.height())))
        return img