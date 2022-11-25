# python
#
# frame_colors - v.1.0
# To automatically colorize selected frames
#
# Created by Cristobal Vila - etereaestudios.com - November 2022
# Thanks again to Luca Giarrizzo, from Substance Designer team, for the great help!!!


# Import the required classes, tools and other sd stuff.
import os
import sd
import re
import weakref

from functools import partial
from collections import OrderedDict

from sd.tools import io
from sd.tools import graphlayout
from sd.api import sdmodule
from sd.api import sdproperty
from sd.api import sdtypeenum

from sd.ui.graphgrid import *
from sd.api.sbs.sdsbscompgraph import *
from sd.api.sdgraphobjectpin import *
from sd.api.sdgraphobjectframe import *
from sd.api.sdgraphobjectcomment import *
from sd.api.sdproperty import SDPropertyCategory
from sd.api.sdvalueserializer import SDValueSerializer
from sd.api.sdapplication import SDApplicationPath

from PySide2 import QtCore, QtGui, QtWidgets, QtSvg


DEFAULT_ICON_SIZE = 24


# Literally copied from factory plugin 'node_align_tools'
def loadSvgIcon(iconName, size):
    currentDir = os.path.dirname(__file__)
    iconFile = os.path.abspath(os.path.join(currentDir, iconName + '.svg'))

    svgRenderer = QtSvg.QSvgRenderer(iconFile)
    if svgRenderer.isValid():
        pixmap = QtGui.QPixmap(QtCore.QSize(size, size))

        if not pixmap.isNull():
            pixmap.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(pixmap)
            svgRenderer.render(painter)
            painter.end()

        return QtGui.QIcon(pixmap)

    return None


# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#
#
#
# ------------ START MAIN CUSTOM FUNCTIONS ------------------------------------------------------------------------------
#
#
#

# To change colors in our frames, including a dictionary
def defineColor(color):

    app = sd.getContext().getSDApplication()
    uiMgr = app.getQtForPythonUIMgr()
    selectedStuff = uiMgr.getCurrentGraphSelectedObjects()

    colorsDict = {
        'yellow':       [1.0, 1.0, 0.0, 1.0],
        'orange':       [1.0, 0.5, 0.0, 1.0],
        'red':          [1.0, 0.0, 0.0, 1.0],
        'magenta':      [1.0, 0.0, 1.0, 1.0],
        'purple':       [0.5, 0.0, 1.0, 1.0],
        'blue':         [0.0, 0.0, 1.0, 1.0],
        'sky':          [0.0, 0.5, 1.0, 1.0],
        'cyan':         [0.0, 1.0, 1.0, 1.0],
        'green':        [0.0, 1.0, 0.0, 1.0],
        'white':        [1.0, 1.0, 1.0, 1.0],
        'black':        [0.0, 0.0, 0.0, 1.0],
        'tr_yellow':       [1.0, 1.0, 0.0, 0.15],
        'tr_orange':       [1.0, 0.5, 0.0, 0.15],
        'tr_red':          [1.0, 0.0, 0.0, 0.15],
        'tr_magenta':      [1.0, 0.0, 1.0, 0.15],
        'tr_purple':       [0.5, 0.0, 1.0, 0.15],
        'tr_blue':         [0.0, 0.0, 1.0, 0.15],
        'default':         [0.10196079, 0.5529412, 1.0, 0.2509804], # Factory default color
        'tr_cyan':         [0.0, 1.0, 1.0, 0.15],
        'tr_green':        [0.0, 1.0, 0.0, 0.15],
        'tr_white':        [1.0, 1.0, 1.0, 0.15],
        'tr_black':        [0.0, 0.0, 0.0, 0.15]
    }

    myColor = colorsDict[color]

    R = myColor[0]
    G = myColor[1]
    B = myColor[2]
    A = myColor[3]

    for item in selectedStuff:
        className = item.getClassName()
        if className == 'SDGraphObjectFrame':
            item.setColor(ColorRGBA(R, G, B, A))


# Adapted from factory plugin 'node_align_tools'
class frameColorsToolbar(QtWidgets.QToolBar):
    __toolbarList = {}

    def __init__(self, graphViewID, uiMgr):
        super(frameColorsToolbar, self).__init__(parent=uiMgr.getMainWindow())

        self.setObjectName("etereaestudios.com.frame_colors_toolbar")

        self.__graphViewID = graphViewID
        self.__uiMgr = uiMgr

        act = self.addAction(loadSvgIcon("tr_black", DEFAULT_ICON_SIZE), "FC_TR_black")
        act.setToolTip(self.tr("Make Frame Transparent Black"))
        act.triggered.connect(partial(defineColor, color="tr_black"))

        act = self.addAction(loadSvgIcon("tr_white", DEFAULT_ICON_SIZE), "FC_TR_white")
        act.setToolTip(self.tr("Make Frame Transparent White"))
        act.triggered.connect(partial(defineColor, color="tr_white"))

        act = self.addAction(loadSvgIcon("tr_yellow", DEFAULT_ICON_SIZE), "FC_TR_yellow")
        act.setToolTip(self.tr("Make Frame Transparent Yellow"))
        act.triggered.connect(partial(defineColor, color="tr_yellow"))

        act = self.addAction(loadSvgIcon("tr_orange", DEFAULT_ICON_SIZE), "FC_TR_orange")
        act.setToolTip(self.tr("Make Frame Transparent Orange"))
        act.triggered.connect(partial(defineColor, color="tr_orange"))

        act = self.addAction(loadSvgIcon("tr_red", DEFAULT_ICON_SIZE), "FC_TR_red")
        act.setToolTip(self.tr("Make Frame Transparent Red"))
        act.triggered.connect(partial(defineColor, color="tr_red"))

        act = self.addAction(loadSvgIcon("tr_magenta", DEFAULT_ICON_SIZE), "FC_TR_magenta")
        act.setToolTip(self.tr("Make Frame Transparent Magenta"))
        act.triggered.connect(partial(defineColor, color="tr_magenta"))

        act = self.addAction(loadSvgIcon("tr_purple", DEFAULT_ICON_SIZE), "FC_TR_purple")
        act.setToolTip(self.tr("Make Frame Transparent Purple"))
        act.triggered.connect(partial(defineColor, color="tr_purple"))

        act = self.addAction(loadSvgIcon("tr_blue", DEFAULT_ICON_SIZE), "FC_TR_blue")
        act.setToolTip(self.tr("Make Frame Transparent Blue"))
        act.triggered.connect(partial(defineColor, color="tr_blue"))

        act = self.addAction(loadSvgIcon("default", DEFAULT_ICON_SIZE), "FC_Default")
        act.setToolTip(self.tr("Make Frame Default Color"))
        act.triggered.connect(partial(defineColor, color="default"))

        act = self.addAction(loadSvgIcon("tr_cyan", DEFAULT_ICON_SIZE), "FC_TR_cyan")
        act.setToolTip(self.tr("Make Frame Transparent Cyan"))
        act.triggered.connect(partial(defineColor, color="tr_cyan"))

        act = self.addAction(loadSvgIcon("tr_green", DEFAULT_ICON_SIZE), "FC_TR_green")
        act.setToolTip(self.tr("Make Frame Transparent Green"))
        act.triggered.connect(partial(defineColor, color="tr_green"))

        act = self.addAction(loadSvgIcon("black", DEFAULT_ICON_SIZE), "FC_Black")
        act.setToolTip(self.tr("Make Frame Pure Black"))
        act.triggered.connect(partial(defineColor, color="black"))

        act = self.addAction(loadSvgIcon("white", DEFAULT_ICON_SIZE), "FC_White")
        act.setToolTip(self.tr("Make Frame Pure White"))
        act.triggered.connect(partial(defineColor, color="white"))

        act = self.addAction(loadSvgIcon("yellow", DEFAULT_ICON_SIZE), "FC_Yellow")
        act.setToolTip(self.tr("Make Frame Pure Yellow"))
        act.triggered.connect(partial(defineColor, color="yellow"))

        act = self.addAction(loadSvgIcon("orange", DEFAULT_ICON_SIZE), "FC_Orange")
        act.setToolTip(self.tr("Make Frame Pure Orange"))
        act.triggered.connect(partial(defineColor, color="orange"))

        act = self.addAction(loadSvgIcon("red", DEFAULT_ICON_SIZE), "FC_Red")
        act.setToolTip(self.tr("Make Frame Pure Red"))
        act.triggered.connect(partial(defineColor, color="red"))

        act = self.addAction(loadSvgIcon("magenta", DEFAULT_ICON_SIZE), "FC_Magenta")
        act.setToolTip(self.tr("Make Frame Pure Magenta"))
        act.triggered.connect(partial(defineColor, color="magenta"))

        act = self.addAction(loadSvgIcon("purple", DEFAULT_ICON_SIZE), "FC_Purple")
        act.setToolTip(self.tr("Make Frame Pure Purple"))
        act.triggered.connect(partial(defineColor, color="purple"))

        act = self.addAction(loadSvgIcon("blue", DEFAULT_ICON_SIZE), "FC_Blue")
        act.setToolTip(self.tr("Make Frame Pure Blue"))
        act.triggered.connect(partial(defineColor, color="blue"))

        act = self.addAction(loadSvgIcon("sky", DEFAULT_ICON_SIZE), "FC_Sky")
        act.setToolTip(self.tr("Make Frame Pure Sky"))
        act.triggered.connect(partial(defineColor, color="sky"))

        act = self.addAction(loadSvgIcon("cyan", DEFAULT_ICON_SIZE), "FC_Cyan")
        act.setToolTip(self.tr("Make Frame Pure Cyan"))
        act.triggered.connect(partial(defineColor, color="cyan"))

        act = self.addAction(loadSvgIcon("green", DEFAULT_ICON_SIZE), "FC_Green")
        act.setToolTip(self.tr("Make Frame Pure Green"))
        act.triggered.connect(partial(defineColor, color="green"))


        self.__toolbarList[graphViewID] = weakref.ref(self)
        self.destroyed.connect(partial(frameColorsToolbar.__onToolbarDeleted, graphViewID=graphViewID))

    def tooltip(self):
        return self.tr("Change Frame Color")

    #
    # ------------ END MAIN CUSTOM FUNCTIONS -----------------------------------------------------------------------------
    #
    #
    #
    # ////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////////////////////////////////////////////////////////////////////////


    # Literally copied from factory plugin 'node_align_tools'
    @classmethod
    def __onToolbarDeleted(cls, graphViewID):
        del cls.__toolbarList[graphViewID]

    # Literally copied from factory plugin 'node_align_tools'
    @classmethod 
    def removeAllToolbars(cls):
        for toolbar in cls.__toolbarList.values():
            if toolbar():
                toolbar().deleteLater()

# Adapted from factory plugin 'node_align_tools'
def onNewGraphViewCreated(graphViewID, uiMgr):
    # Ignore graph types not supported by the Python API.
    if not uiMgr.getCurrentGraph():
        return

    toolbar = frameColorsToolbar(graphViewID, uiMgr)
    uiMgr.addToolbarToGraphView(
        graphViewID,
        toolbar,
        icon = loadSvgIcon("frame_colors", DEFAULT_ICON_SIZE),
        tooltip = toolbar.tooltip())


graphViewCreatedCallbackID = 0

# Literally copied from factory plugin 'node_align_tools'
def initializeSDPlugin():

    # Get the application and UI manager object.
    ctx = sd.getContext()
    app = ctx.getSDApplication()
    uiMgr = app.getQtForPythonUIMgr()

    if uiMgr:
        global graphViewCreatedCallbackID
        graphViewCreatedCallbackID = uiMgr.registerGraphViewCreatedCallback(
            partial(onNewGraphViewCreated, uiMgr=uiMgr))


# Adapted from factory plugin 'node_align_tools'
def uninitializeSDPlugin():
    ctx = sd.getContext()
    app = ctx.getSDApplication()
    uiMgr = app.getQtForPythonUIMgr()

    if uiMgr:
        global graphViewCreatedCallbackID
        uiMgr.unregisterCallback(graphViewCreatedCallbackID)
        frameColorsToolbar.removeAllToolbars()
