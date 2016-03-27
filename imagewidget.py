#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QImage, QPainter, QPalette, QPixmap
from PyQt5 import QtWidgets, uic

class ImageWidget(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pixmap = None
        
    def setOriginalPixmap(self, pixmap):
        """"""
        self._pixmap = pixmap
        self.setScaledPixmap()

    def resizeEvent(self, event):
        """"""
        self.setScaledPixmap()

    def setScaledPixmap(self):
        """"""
        if self._pixmap is not None:
            scaled_pixmap = self._pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setPixmap(scaled_pixmap)
        
