# python
#
# frame_colors - v.1.0
# To automatically colorize selected frames
#
# Created by Cristobal Vila - etereaestudios.com - November 2022
#


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

        act = self.addAction(loadSvgIcon("tr_black", DEFAULT_ICON_SIZE), "FCTr_black")
        act.setToolTip(self.tr("Make Frame Tr_black"))
        act.triggered.connect(self.__makeTr_black)

        act = self.addAction(loadSvgIcon("tr_white", DEFAULT_ICON_SIZE), "FCTr_white")
        act.setToolTip(self.tr("Make Frame Tr_white"))
        act.triggered.connect(self.__makeTr_white)

        act = self.addAction(loadSvgIcon("tr_yellow", DEFAULT_ICON_SIZE), "FCTr_yellow")
        act.setToolTip(self.tr("Make Frame Tr_yellow"))
        act.triggered.connect(self.__makeTr_yellow)

        act = self.addAction(loadSvgIcon("tr_orange", DEFAULT_ICON_SIZE), "FCTr_orange")
        act.setToolTip(self.tr("Make Frame Tr_orange"))
        act.triggered.connect(self.__makeTr_orange)

        act = self.addAction(loadSvgIcon("tr_red", DEFAULT_ICON_SIZE), "FCTr_red")
        act.setToolTip(self.tr("Make Frame Tr_red"))
        act.triggered.connect(self.__makeTr_red)

        act = self.addAction(loadSvgIcon("tr_magenta", DEFAULT_ICON_SIZE), "FCTr_magenta")
        act.setToolTip(self.tr("Make Frame Tr_magenta"))
        act.triggered.connect(self.__makeTr_magenta)

        act = self.addAction(loadSvgIcon("tr_purple", DEFAULT_ICON_SIZE), "FCTr_purple")
        act.setToolTip(self.tr("Make Frame Tr_purple"))
        act.triggered.connect(self.__makeTr_purple)

        act = self.addAction(loadSvgIcon("tr_blue", DEFAULT_ICON_SIZE), "FCTr_blue")
        act.setToolTip(self.tr("Make Frame Tr_blue"))
        act.triggered.connect(self.__makeTr_blue)

        act = self.addAction(loadSvgIcon("default", DEFAULT_ICON_SIZE), "FCDefault")
        act.setToolTip(self.tr("Make Frame Default"))
        act.triggered.connect(self.__makeDefault)

        act = self.addAction(loadSvgIcon("tr_cyan", DEFAULT_ICON_SIZE), "FCTr_cyan")
        act.setToolTip(self.tr("Make Frame Tr_cyan"))
        act.triggered.connect(self.__makeTr_cyan)

        act = self.addAction(loadSvgIcon("tr_green", DEFAULT_ICON_SIZE), "FCTr_green")
        act.setToolTip(self.tr("Make Frame Tr_green"))
        act.triggered.connect(self.__makeTr_green)

        act = self.addAction(loadSvgIcon("black", DEFAULT_ICON_SIZE), "FCBlack")
        act.setToolTip(self.tr("Make Frame Black"))
        act.triggered.connect(self.__makeBlack)

        act = self.addAction(loadSvgIcon("white", DEFAULT_ICON_SIZE), "FCWhite")
        act.setToolTip(self.tr("Make Frame White"))
        act.triggered.connect(self.__makeWhite)

        act = self.addAction(loadSvgIcon("yellow", DEFAULT_ICON_SIZE), "FCYellow")
        act.setToolTip(self.tr("Make Frame Yellow"))
        act.triggered.connect(self.__makeYellow)

        act = self.addAction(loadSvgIcon("orange", DEFAULT_ICON_SIZE), "FCOrange")
        act.setToolTip(self.tr("Make Frame Orange"))
        act.triggered.connect(self.__makeOrange)

        act = self.addAction(loadSvgIcon("red", DEFAULT_ICON_SIZE), "FCRed")
        act.setToolTip(self.tr("Make Frame Red"))
        act.triggered.connect(self.__makeRed)

        act = self.addAction(loadSvgIcon("magenta", DEFAULT_ICON_SIZE), "FCMagenta")
        act.setToolTip(self.tr("Make Frame Magenta"))
        act.triggered.connect(self.__makeMagenta)

        act = self.addAction(loadSvgIcon("purple", DEFAULT_ICON_SIZE), "FCPurple")
        act.setToolTip(self.tr("Make Frame Purple"))
        act.triggered.connect(self.__makePurple)

        act = self.addAction(loadSvgIcon("blue", DEFAULT_ICON_SIZE), "FCBlue")
        act.setToolTip(self.tr("Make Frame Blue"))
        act.triggered.connect(self.__makeBlue)

        act = self.addAction(loadSvgIcon("sky", DEFAULT_ICON_SIZE), "FCSky")
        act.setToolTip(self.tr("Make Frame Sky"))
        act.triggered.connect(self.__makeSky)

        act = self.addAction(loadSvgIcon("cyan", DEFAULT_ICON_SIZE), "FCCyan")
        act.setToolTip(self.tr("Make Frame Cyan"))
        act.triggered.connect(self.__makeCyan)

        act = self.addAction(loadSvgIcon("green", DEFAULT_ICON_SIZE), "FCGreen")
        act.setToolTip(self.tr("Make Frame Green"))
        act.triggered.connect(self.__makeGreen)

        self.__toolbarList[graphViewID] = weakref.ref(self)
        self.destroyed.connect(partial(frameColorsToolbar.__onToolbarDeleted, graphViewID=graphViewID))

    def tooltip(self):
        return self.tr("Change Frame Color")


    # ALL THESE FUNCTIONS-INSIDE-FUNCTIONS ARE ABSOLUTY STUPID WAY OF WORK.
    # I need to understand these class, self, triggered.connect stuff...
    def __makeYellow(self):
        defineColor('yellow')

    def __makeOrange(self):
        defineColor('orange')

    def __makeRed(self):
        defineColor('red')

    def __makeMagenta(self):
        defineColor('magenta')

    def __makePurple(self):
        defineColor('purple')

    def __makeBlue(self):
        defineColor('blue')

    def __makeSky(self):
        defineColor('sky')

    def __makeCyan(self):
        defineColor('cyan')

    def __makeGreen(self):
        defineColor('green')

    def __makeWhite(self):
        defineColor('white')

    def __makeBlack(self):
        defineColor('black')

    def __makeTr_yellow(self):
        defineColor('tr_yellow')

    def __makeTr_orange(self):
        defineColor('tr_orange')

    def __makeTr_red(self):
        defineColor('tr_red')

    def __makeTr_magenta(self):
        defineColor('tr_magenta')

    def __makeTr_purple(self):
        defineColor('tr_purple')

    def __makeTr_blue(self):
        defineColor('tr_blue')

    def __makeDefault(self):
        defineColor('default')

    def __makeTr_cyan(self):
        defineColor('tr_cyan')

    def __makeTr_green(self):
        defineColor('tr_green')

    def __makeTr_white(self):
        defineColor('tr_white')

    def __makeTr_black(self):
        defineColor('tr_black')

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
