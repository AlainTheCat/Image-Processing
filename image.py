#!/usr/bin/env python3

"""
Image processing with Python3 and PySide6.

Author: Alain the Cat
Local Website: mao2.fr
"""

import json
import sys
import random
# import os

from math import sqrt, log, cos, pow
from statistics import median, mean

from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QTranslator, QSize
from PySide6.QtGui import QIcon, QPainter, Qt, QPixmap, QImage, QColor
from PySide6.QtPrintSupport import QPrintDialog, QPrinter
from PySide6.QtWidgets import QMainWindow, QMessageBox, QFileDialog

from imageUI import Ui_MainWindow

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import qimage2ndarray as q2a

import cythonImage as ci


class Language:
    """
    Language
    
    Attributes:
        id: int, language ident
        name: string, name of this language
        enable: bool, if true this language is active
        file: string, name of translation file (qm file)
    """

    def __init__(self, id, name, enable, file):
        """Initializes Language class"""
        self.id = id
        self.name = name
        self.enable = enable
        self.file = file


languages = []

# List all languages
with open('languageSettings.json') as f:
    data1 = json.load(f)

# Appending instances to list
for lang in range(len(data1)):
    languages.append(Language(data1['language' + str(lang)]['id'], data1['language' + str(lang)]['name'],
                              data1['language' + str(lang)]['enable'], data1['language' + str(lang)]['file']))

# Current file for translation
currentLanguage = "English"
currentLangIndex = 0
for lang in range(len(languages)):
    if languages[lang].enable:
        currentLangFile = languages[lang].file
        currentLanguage = languages[lang].name
        currentLangIndex = lang
print("Language: ", currentLanguage)
print("currentLangIndex: ", currentLangIndex)  # 0: English 1: French


class Menu:
    """
    Menu
    
    Attributes:
        method: int
        title: string
        param1 to 8: int
    """

    def __init__(self, method, title, param1, param2, param3, param4, param5, param6, param7, param8):
        """ initializes Menu """
        self.method = method
        self.title = title
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        self.param4 = param4
        self.param5 = param5
        self.param6 = param6
        self.param7 = param7
        self.param8 = param8


# Creating list of menus
menus = []


def byteToString(data):
    """
    Change an integer to string like 0x...

    :param data: integer
    :return: string
    """
    dataStr = ""
    for number in data:
        dataStr = dataStr + " " + hex(number)
    dataStr = dataStr.replace('0x', '')
    return dataStr


def initMenu():
    """Menus initialization."""
    for menu in range(110):
        menus.append(Menu("", "", "", "", "", "", "", "", "", ""))

    # 0 - Initialization
    menus[0].title = QtGui.QGuiApplication.translate("Image", "Initialization", None)

    # *** Local Filters ***
    # 1 Brightness
    menus[1].title = QtGui.QGuiApplication.translate("Image", "Brightness", None)
    menus[1].param5 = QtGui.QGuiApplication.translate("Image", "Brightness", None)
    # 2 Contrast
    menus[2].title = QtGui.QGuiApplication.translate("Image", "Contrast", None)
    menus[2].param6 = QtGui.QGuiApplication.translate("Image", "Contrast", None)
    # 3 Luminance
    menus[3].title = QtGui.QGuiApplication.translate("Image", "Luminance", None)
    # 4 Weighted Luminance
    menus[4].title = QtGui.QGuiApplication.translate("Image", "Weighted Luminance", None)
    # 5 RGB
    menus[5].title = QtGui.QGuiApplication.translate("Image", "RGB", None)
    menus[5].param4 = QtGui.QGuiApplication.translate("Image", "Red", None)
    menus[5].param5 = QtGui.QGuiApplication.translate("Image", "Green", None)
    menus[5].param6 = QtGui.QGuiApplication.translate("Image", "Blue", None)
    # 6 Red effect
    menus[6].title = QtGui.QGuiApplication.translate("Image", "Red Effect", None)
    menus[6].param4 = QtGui.QGuiApplication.translate("Image", "Red", None)
    menus[6].param5 = QtGui.QGuiApplication.translate("Image", "Other", None)
    # 7 Thresholding
    menus[7].title = QtGui.QGuiApplication.translate("Image", "Thresholding", None)
    menus[7].param4 = QtGui.QGuiApplication.translate("Image", "Red Threshold", None)
    menus[7].param5 = QtGui.QGuiApplication.translate("Image", "Green Threshold", None)
    menus[7].param6 = QtGui.QGuiApplication.translate("Image", "Blue Threshold", None)
    # 8 Binarization
    menus[8].title = QtGui.QGuiApplication.translate("Image", "Binarization", None)
    menus[8].param1 = QtGui.QGuiApplication.translate("Image", "Threshold", None)
    # 9 Negative
    menus[9].method = 9
    menus[9].title = QtGui.QGuiApplication.translate("Image", "Negative", None)
    # 10 Transparency
    menus[10].title = QtGui.QGuiApplication.translate("Image", "Transparency", None)
    menus[10].param1 = QtGui.QGuiApplication.translate("Image", "Alpha", None)
    # 11 Red Filter
    menus[11].title = QtGui.QGuiApplication.translate("Image", "Red Filter", None)
    # 12 Green Filter
    menus[12].title = QtGui.QGuiApplication.translate("Image", "Green Filter", None)
    # 13 Blue Filter
    menus[13].title = QtGui.QGuiApplication.translate("Image", "Blue Filter", None)
    # 14 Windowing
    menus[14].title = QtGui.QGuiApplication.translate("Image", "Windowing", None)
    menus[14].param1 = QtGui.QGuiApplication.translate("Image", "Win A", None)
    menus[14].param2 = QtGui.QGuiApplication.translate("Image", "Win B", None)
    # 15 Grey Level
    menus[15].title = QtGui.QGuiApplication.translate("Image", "Grey Level", None)
    menus[15].param7 = QtGui.QGuiApplication.translate("Image", "Number of levels", None)
    # 16 Color Level
    menus[16].title = QtGui.QGuiApplication.translate("Image", "Colors Level", None)
    menus[16].param7 = QtGui.QGuiApplication.translate("Image", "Number of levels", None)
    # 17 False Colors
    menus[17].title = QtGui.QGuiApplication.translate("Image", "False Colors", None)
    # 18 Sepia
    menus[18].title = QtGui.QGuiApplication.translate("Image", "Sepia", None)

    # *** Neighborhood Filters ***
    # 20 Integrating Filter
    menus[20].title = QtGui.QGuiApplication.translate("Image", "Integrating Filter", None)
    # 21 Median Filter
    menus[21].title = QtGui.QGuiApplication.translate("Image", "Median Filter", None)
    # 22 Gaussian Filter
    menus[22].title = QtGui.QGuiApplication.translate("Image", "Gaussian Filter", None)
    # 23 Horizontal Gradient
    menus[23].title = QtGui.QGuiApplication.translate("Image", "Horizontal Gradient Filter", None)
    # 24 Vertical Gradient
    menus[24].title = QtGui.QGuiApplication.translate("Image", "Vertical Gradient Filter", None)
    # 25 Borders detect
    menus[25].title = QtGui.QGuiApplication.translate("Image", "Borders Detect", None)
    # 26 Erosion
    menus[26].title = QtGui.QGuiApplication.translate("Image", "Erosion", None)
    # 27 Dilation
    menus[27].title = QtGui.QGuiApplication.translate("Image", "Dilation", None)
    # 28 Gamma
    menus[28].title = QtGui.QGuiApplication.translate("Image", "Gamma Filter", None)
    menus[28].param3 = QtGui.QGuiApplication.translate("Image", "Gamma", None)

    # 29 Points 36
    menus[29].title = QtGui.QGuiApplication.translate("Image", "Black Points", None)
    menus[29].param7 = QtGui.QGuiApplication.translate("Image", "Number of points", None)
    # 30 Vertical Strokes
    menus[30].title = QtGui.QGuiApplication.translate("Image", "Black Vertical Strokes", None)
    menus[30].param7 = QtGui.QGuiApplication.translate("Image", "Number of lines", None)
    # 31 Horizontal Strokes
    menus[31].title = QtGui.QGuiApplication.translate("Image", "Black Horizontal Strokes", None)
    menus[31].param7 = QtGui.QGuiApplication.translate("Image", "Number of lines", None)

    # 32 - Convolution
    menus[32].title = QtGui.QGuiApplication.translate("Image", "Convolution", None)

    # ***Superposition***
    # 40 Red Background
    menus[40].title = QtGui.QGuiApplication.translate("Image", "Red Background", None)
    # 41 Green Background
    menus[41].title = QtGui.QGuiApplication.translate("Image", "Green Background", None)
    # 42 Green Background
    menus[42].title = QtGui.QGuiApplication.translate("Image", "Green Background", None)
    # 43 White Background
    menus[43].title = QtGui.QGuiApplication.translate("Image", "White Background", None)
    # 44 Black Background
    menus[44].title = QtGui.QGuiApplication.translate("Image", "Black Background", None)
    # 45 Tint Background
    menus[45].title = QtGui.QGuiApplication.translate("Image", "Tint Background", None)
    menus[45].param4 = QtGui.QGuiApplication.translate("Image", "Red", None)
    menus[45].param5 = QtGui.QGuiApplication.translate("Image", "Green", None)
    menus[45].param6 = QtGui.QGuiApplication.translate("Image", "Blue", None)
    # 46 Image overlay on a green background
    menus[46].title = QtGui.QGuiApplication.translate("Image", "Overlay on green background", None)
    # 47 Anaglyphs
    menus[47].title = QtGui.QGuiApplication.translate("Image", "Anaglyph", None)
    # 48 Overlay image 1 on image 2
    menus[48].title = QtGui.QGuiApplication.translate("Image", "Overlay 1 on 2", None)
    menus[48].param6 = QtGui.QGuiApplication.translate("Image", "Ratio", None)

    # *** Noises ***
    # 50 White noise
    menus[50].title = QtGui.QGuiApplication.translate("Image", "White noise", None)
    menus[50].param1 = QtGui.QGuiApplication.translate("Image", "Points x 10", None)
    # 51 Pepper and salt noise
    menus[51].title = QtGui.QGuiApplication.translate("Image", "Pepper and salt noise", None)
    menus[51].param1 = QtGui.QGuiApplication.translate("Image", "Points x 10", None)
    # 52 Gaussian Noise
    menus[52].title = QtGui.QGuiApplication.translate("Image", "Gaussian noise", None)
    menus[52].param1 = QtGui.QGuiApplication.translate("Image", "Sigma/10, min: 0.1, max: 25.5", None)

    # *** Encryption ***
    # 60 Pixelation
    menus[60].title = QtGui.QGuiApplication.translate("Image", "Pixelation", None)
    menus[60].param4 = QtGui.QGuiApplication.translate("Image", "Pixels", None)
    # 61 Encryption
    menus[61].title = QtGui.QGuiApplication.translate("Image", "Encryption", None)
    menus[61].param3 = QtGui.QGuiApplication.translate("Image", "Gap", None)
    # 62 Encryption with fixed key
    menus[62].title = QtGui.QGuiApplication.translate("Image", "Encryption with fixed key", None)
    menus[62].param8 = QtGui.QGuiApplication.translate("Image", "Seed", None)
    # 63 Decryption
    menus[63].title = QtGui.QGuiApplication.translate("Image", "Decryption", None)
    menus[63].param8 = QtGui.QGuiApplication.translate("Image", "Seed", None)
    # 64 Secret message to hide
    menus[64].title = QtGui.QGuiApplication.translate("Image", "Secret message to hide", None)
    # 65 Show the secret message
    menus[65].title = QtGui.QGuiApplication.translate("Image", "Show the secret message", None)
    # 66 Text to hide (Stenganography)
    menus[66].title = QtGui.QGuiApplication.translate("Image", "Text to hide (Steganography)", None)
    # 67 Show the secret text
    menus[67].title = QtGui.QGuiApplication.translate("Image", "Show the secret text", None)
    # 68 Transform to ASCII file
    menus[68].title = QtGui.QGuiApplication.translate("Image", "ASCII Art", None)
    menus[68].param7 = QtGui.QGuiApplication.translate("Image", "Ratio", None)
    # 69 Puzzle
    menus[69].title = QtGui.QGuiApplication.translate("Image", "Puzzle", None)

    # *** Geometric Transformations ***
    # 70  Vertical symmetry
    menus[70].title = QtGui.QGuiApplication.translate("Image", "Vertical symmetry", None)
    # 71  Horizontal symmetry
    menus[71].title = QtGui.QGuiApplication.translate("Image", "Horizontal symmetry", None)
    # 72  Rotation 90° right
    menus[72].title = QtGui.QGuiApplication.translate("Image", "Rotation 90° right", None)
    # 73 Rotation
    menus[73].title = QtGui.QGuiApplication.translate("Image", "Rotation", None)
    menus[73].param1 = QtGui.QGuiApplication.translate("Image", "Angle of rotation", None)
    # 74  Image diagonalization
    menus[74].title = QtGui.QGuiApplication.translate("Image", "Image diagonalization", None)
    # 75 Medallion
    menus[75].title = QtGui.QGuiApplication.translate("Image", "Medallion", None)
    menus[75].param1 = QtGui.QGuiApplication.translate("Image", "RatioX", None)
    menus[75].param2 = QtGui.QGuiApplication.translate("Image", "RatioY", None)
    menus[75].param7 = QtGui.QGuiApplication.translate("Image", "Couleur du fond", None)
    # 76 Translation
    menus[76].title = QtGui.QGuiApplication.translate("Image", "Translation", None)
    menus[76].param1 = QtGui.QGuiApplication.translate("Image", "Horizontal Axis", None)
    menus[76].param2 = QtGui.QGuiApplication.translate("Image", "Vertical Axis", None)
    # 77 Zoom plus
    menus[77].title = QtGui.QGuiApplication.translate("Image", "Zoom plus", None)
    # 78 Zoom plus bilinear
    menus[78].title = QtGui.QGuiApplication.translate("Image", "Zoom Plus bilinear", None)
    # 79 Zoom less
    menus[79].title = QtGui.QGuiApplication.translate("Image", "Zoom less", None)
    # 80 Crop
    menus[80].title = QtGui.QGuiApplication.translate("Image", "Crop", None)
    menus[80].param1 = QtGui.QGuiApplication.translate("Image", "X1", None)
    menus[80].param2 = QtGui.QGuiApplication.translate("Image", "Y1", None)
    menus[80].param4 = QtGui.QGuiApplication.translate("Image", "X2", None)
    menus[80].param5 = QtGui.QGuiApplication.translate("Image", "Y2", None)

    # *** Focus and patterns***
    # 90 Depth 4 to 1
    menus[90].title = QtGui.QGuiApplication.translate("Image", "Depth 4 to 1", None)
    # 91 Depth 1 to 4
    menus[91].title = QtGui.QGuiApplication.translate("Image", "Depth 1 to 4", None)
    # 92 Color Pattern
    menus[92].title = QtGui.QGuiApplication.translate("Image", "Color Pattern", None)
    # 93 Black and White Pattern
    menus[93].title = QtGui.QGuiApplication.translate("Image", "Black and White Pattern", None)
    # 94 Image Code
    menus[94].title = QtGui.QGuiApplication.translate("Image", "Image Code", None)
    # 95 Histogram
    menus[95].title = QtGui.QGuiApplication.translate("Image", "Histogram", None)

    # *** Cancel the last action ***
    # 99 Cancel
    menus[99].title = QtGui.QGuiApplication.translate("Image", "Cancel the last action", None)

    # *** Image Format transformation ***
    # 100 Format Mono
    menus[100].title = QtGui.QGuiApplication.translate("Image", "Format Mono", None)
    # 101 Format Indexed8
    menus[101].title = QtGui.QGuiApplication.translate("Image", "Format Indexed8", None)
    # 102 Format ARGB32
    menus[102].title = QtGui.QGuiApplication.translate("Image", "Format ARGB32", None)
    # 103 Format Grayscale8
    menus[103].title = QtGui.QGuiApplication.translate("Image", "Format Grayscale8", None)
    # 104 Format Grayscale8
    menus[104].title = QtGui.QGuiApplication.translate("Image", "Format 800x600", None)

    # *** Functions in development ***
    # 105 Function test 1
    menus[105].title = QtGui.QGuiApplication.translate("Image", "Function test 1", None)
    # 106 Function test 2
    menus[106].title = QtGui.QGuiApplication.translate("Image", "Function test 2", None)
    # 107 Function test 3
    menus[107].title = QtGui.QGuiApplication.translate("Image", "Function test 3", None)
    # 108 Function test 4
    menus[108].title = QtGui.QGuiApplication.translate("Image", "Function test 4", None)


def saveLanguagesSettings():
    """Save the settings of the different languages in a json file."""
    settings = {}
    for language in languages:
        idLang = language.id
        name = language.name
        enable = language.enable
        file = language.file
        langIndex = "language" + str(idLang)
        langDict = {"id": idLang, "name": name, "enable": enable, "file": file}
        settings[langIndex] = langDict
        # Serializing json
    json_object = json.dumps(settings, indent=4)
    # Writing to sample.json
    with open("languageSettings.json", "w") as outfile:
        outfile.write(json_object)


def showDialog(msgTitle, msg1, msg2):
    """Opens a dialog window.

    Args:
        msgTitle: String, title of the message box
        msg1: String, message #1
        msg2: String, message #2

    Returns:
        answer: QMessageBox constant, 3 possibilities: Yes, No or Cancel
    """
    msgBox = QMessageBox()
    # msgBox.setIcon(QMessageBox.StandardButton.Information)
    msgBox.setWindowTitle(msgTitle)
    msgBox.setText(msg1)
    msgBox.setInformativeText(msg2)
    msgBox.setStandardButtons(
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
    answer = msgBox.exec()
    return answer


def languageSelected(index):
    """Allows to change the language after validation."""
    print("Index: ", index)
    language = str(languages[index].name)
    print("Language: ", language)
    answer = showDialog(QtGui.QGuiApplication.translate("Image", "Language", None),
                        QtGui.QGuiApplication.translate("Image",
                                                        "Do you want change for this language? "
                                                        "If yes you must restart the program.",
                                                        None), language)
    if answer == QMessageBox.StandardButton.Yes:
        print('Yes clicked')
        global currentLangIndex
        languages[currentLangIndex].enable = False
        currentLangIndex = index
        languages[currentLangIndex].enable = True
        saveLanguagesSettings()
    if answer == QMessageBox.StandardButton.No:
        print('No clicked')
    if answer == QMessageBox.StandardButton.Cancel:
        print('Cancel clicked')


def gaussian():
    """ Gaussian function,
    This function calculate a random number centered on 0 according to the normal distribution
    y = sqrt(-2*log(R1))cos(2*Pi*R2).

    """
    noise = 0
    rand1 = random.random()     # number from 0 to 1
    rand2 = random.random()
    if rand1 != 0:
        noise = sqrt(-2 * log(rand1)) * cos(2 * np.pi * rand2)
    return noise


def copyImage(fromImage, toImage):
    height = fromImage.height()
    width = fromImage.width()
    for j in range(height):
        for i in range(width):
            color = fromImage.pixelColor(i, j)
            green = color.green()
            blue = color.blue()
            red = color.red()
            alpha = color.alpha()
            color = QColor(red, green, blue, alpha)
            toImage.setPixelColor(i, j, color)


class Image(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

        self.meth = 0  # Using method
        self.aa = 50  # slider A value
        self.bb = 50  # slider B value
        self.cc = 10  # slider C value
        self.dd = 50  # slider D value
        self.ee = 50  # slider E value
        self.ff = 50  # slider F value
        self.pp = 1  # spinBox Point value
        self.seed = 100  # spinBox Seed value
        self.tt = 3  # spinBox Filter value (possible values : 3, 5, 7 and 9)
        self.isPattern = False
        self.isPatternNB = False

        self.image = QImage()  # image
        self.image1 = QImage()  # image loaded and displayed
        self.image2 = QImage()  # Second image
        self.image0 = QImage()  # image loaded
        self.imageBuffer = QImage()  # buffer image
        self.imageBuffer2 = QImage()  # buffer image 2
        self.imageBufferX = QImage()  # buffer image X
        self.imageBufferY = QImage()  # buffer image Y
        self.imageList = []  # image processing historic
        self.fileName = ""  # image 1 file name
        self.fileName2 = ""  # image 2 file name
        self.fileNameText = ""
        self.depth = 4

        self.filter = np.zeros((3, 3), dtype=np.int8)

        self.setWindowTitle(QtGui.QGuiApplication.translate("Image", "Image Processing with Python", None))
        self.setWindowIcon(QIcon("icons/Mao48x48.ico"))
        self.setupUi(self)
        self.printer = QPrinter()

        # Histogram
        # a figure instance to plot on
        self.figure = plt.figure()
        # this is the Canvas Widget that
        # displays the 'figure' it takes the
        # 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        initMenu()
        self.operatingMode(0)
        self.createConnections()
        self.openDefaultImage()

    def printImage(self):
        """Print the image (Pixmap into Label)."""

        if self.tabWidget.currentIndex() != 0:
            self.tabWidget.setCurrentIndex(0)
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), Qt.AspectRatioMode.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def loadImage1(self):
        """Load the first image."""

        size = QSize(700, 525)
        imageShow1 = self.image1.scaled(size, Qt.AspectRatioMode.KeepAspectRatio)  # Displays the largest possible image
        self.imageLabel.setPixmap(QPixmap.fromImage(imageShow1))  # Puts the image into imageLabel
        width1 = self.image1.size().width()
        height1 = self.image1.size().height()
        self.lcdWidthImage1.display(width1)  # Displays image width
        self.lcdHeightImage1.display(height1)  # Displays image height
        depth1 = self.image1.depth() / 8
        self.lcdDepthImage1.display(depth1)  # Displays the number of bytes per pixel (4 usually)
        self.lcdHisto.display(len(self.imageList))  # Displays the number of saved images into historic
        if depth1 != 4 or width1 > 1000 or height1 > 1000:
            self.enableButton(False)
            print("KO")
        else:
            self.enableButton(True)
            print("OK")

    def loadImage2(self):
        """Load the second image."""

        size = QSize(700, 525)
        imageShow2 = self.image2.scaled(size, Qt.AspectRatioMode.KeepAspectRatio)
        self.image2Label.setPixmap(QPixmap.fromImage(imageShow2))

        self.lcdWidthImage2.display(self.image2.width())
        self.lcdHeightImage2.display(self.image2.height())
        self.lcdDepthImage2.display(self.image2.depth() / 8)

    def message1(self):
        """Message to invite to load an image."""

        QMessageBox.information(self, QtGui.QGuiApplication.translate("Image", "Main Window ", None),
                                QtGui.QGuiApplication.translate("Image",
                                                                "Please open an image!!!\n"
                                                                "For open an image:\n"
                                                                "- Go to menu File/open,\n"
                                                                "- Select an image", None))

    def message2(self):
        """Invalid image size."""

        QMessageBox.information(self, QtGui.QGuiApplication.translate("Image", "Main Window ", None),
                                QtGui.QGuiApplication.translate("Image", "Format not accepted:\n"
                                                                         "- Width max 24 pixels\n"
                                                                         "- Height max 24 pixels\n"
                                                                         "- with 4 bytes.", None))

    def openDefaultImage(self):
        """Opens default image."""

        if self.tabWidget.currentIndex() != 0:
            self.tabWidget.setCurrentIndex(0)
        sizeMax = 1000
        self.hideParameter()

        self.fileName = "Images/Lenna.png"
        self.image1 = QImage(self.fileName)

        if self.image1.isNull():
            QMessageBox.information(self, QtGui.QGuiApplication.translate("Image", "Image Viewer", None),
             QtGui.QGuiApplication.translate("Image", "Cannot load %s." % self.fileName, None))
            return
        depth = self.image1.depth() / 8
        height = self.image1.height()
        width = self.image1.width()
        print("Depth: %i, Height: %i, Width: %i" % (depth, height, width))

        if depth != 4:
            QMessageBox.information(self, QtGui.QGuiApplication.translate("Image", "Main Window",
                                                                          None),
                                    QtGui.QGuiApplication.translate("Image",
                                                                    "This depth %s do not accept "
                                                                    "all functions."
                                                                    % self.fileName, None))
        if height > sizeMax or width > sizeMax:
            answer = showDialog(QtGui.QGuiApplication.translate("Image", "Main Window", None),
                                QtGui.QGuiApplication.translate("Image",
                                                                "Size too big, do you want reduce the size?",
                                                                None), "")
            if answer == QMessageBox.StandardButton.Yes:
                print('Yes clicked')
                width = 700
                height = 525
                self.imageBuffer = self.image1.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio,
                                                      Qt.TransformationMode.SmoothTransformation)
                self.image1 = self.imageBuffer
            if answer == QMessageBox.StandardButton.No:
                print('No clicked')
            if answer == QMessageBox.StandardButton.Cancel:
                print('Cancel clicked')
        self.isPattern = False
        self.isPatternNB = False
        self.initialize()
        self.message.setText(QtGui.QGuiApplication.translate("Image", "Loaded Image: %s." % self.fileName, None))
        self.labelMessage.setText(
            QtGui.QGuiApplication.translate("Image", "Message: Loaded Image %s" % self.fileName, None))

    def openImage(self):
        """Opens the first image."""

        if self.tabWidget.currentIndex() != 0:
            self.tabWidget.setCurrentIndex(0)
        sizeMax = 1000
        # self.hideParameter()

        options = QFileDialog.Option.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                       'Images (*.png *.jpeg *.jpg)', options=options)
        self.image1 = QImage(self.fileName)

        if self.image1.isNull():
            QMessageBox.information(self, QtGui.QGuiApplication.translate("Image", "Image Viewer", None),
             QtGui.QGuiApplication.translate("Image", "Cannot load %s." % self.fileName, None))
            return
        depth1 = self.image1.depth() / 8
        height1 = self.image1.height()
        width1 = self.image1.width()
        print("Depth: %i, Height: %i, Width: %i" % (depth1, height1, width1))

        if depth1 != 4:
            QMessageBox.information(self, QtGui.QGuiApplication.translate("Image", "Main Window ", None),
                                    QtGui.QGuiApplication.translate("Image",
                                                                    "This depth  %s do not accept"
                                                                    "all functions."
                                                                    % self.fileName, None))
        if height1 > sizeMax or width1 > sizeMax:
            answer = showDialog(QtGui.QGuiApplication.translate("Image", "Main Window", None),
                                QtGui.QGuiApplication.translate("Image",
                                                                "Size too big, do you want reduce the size?",
                                                                None), "")
            if answer == QMessageBox.StandardButton.Yes:
                print('Yes clicked')
                width = 700
                height = 525
                self.imageBuffer = self.image1.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio,
                                                      Qt.TransformationMode.SmoothTransformation)
                self.image1 = self.imageBuffer
            if answer == QMessageBox.StandardButton.No:
                print('No clicked')
                pass
            if answer == QMessageBox.StandardButton.Cancel:
                print('Cancel clicked')
                pass

        self.isPattern = False
        self.isPatternNB = False
        self.initialize()
        self.message.setText(QtGui.QGuiApplication.translate("Image", "Loaded Image: %s." % self.fileName, None))
        self.labelMessage.setText(
            QtGui.QGuiApplication.translate("Image", "Message: Loaded Image %s" % self.fileName, None))

    def saveImage(self):
        """Saves the image 1."""

        suffix = ""
        if self.tabWidget.currentIndex() != 0:
            self.tabWidget.setCurrentIndex(0)
        options = QFileDialog.Option.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(self, QtGui.QGuiApplication.translate("Image",
                                                                                        "Save this image", None),
                                                  "", QtGui.QGuiApplication.translate("Image",
                                                                                      "Image (*.jpg, *.jpeg, *.png)",
                                                                                      None),
                                                  options=options)
        if filename:
            if filename.endswith('jpg'):
                suffix = "JPG"
            if filename.endswith('jpeg'):
                suffix = "JPEG"
            if filename.endswith('png'):
                suffix = "PNG"
            self.image1.save(filename, suffix, -1)
        else:
            QMessageBox.information(self, QtGui.QGuiApplication.translate("Image", "Main Window ", None),
                                    QtGui.QGuiApplication.translate("Image",
                                                                    "Can't save this image", None))

    def openImage2(self):
        """Opens a second image to superimpose on the first."""

        if self.tabWidget.currentIndex() != 0:
            self.tabWidget.setCurrentIndex(0)
        sizeMax = 1000
        self.hideParameter()

        options = QFileDialog.Option.DontUseNativeDialog
        self.fileName2, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                        'Images (*.png *.jpeg *.jpg)', options=options)
        self.image2 = QImage(self.fileName2)

        if self.image2.isNull():
            QMessageBox.information(self, "Image Viewer", "Cannot load %s." % self.fileName2)
            return
        depth = self.image2.depth() / 8
        height = self.image2.height()
        width = self.image2.width()
        print("Depth: %i, Height: %i, Width: %i" % (depth, height, width))

        if depth != 4:
            QMessageBox.information(self, QtGui.QGuiApplication.translate("Image", "Main Window ", None),
                                    QtGui.QGuiApplication.translate("Image",
                                                                    "This depth %s do not accept all functions"
                                                                    % self.fileName2, None))
        if height > sizeMax:
            QMessageBox.information(self, QtGui.QGuiApplication.translate("Image", "Main Window ", None),
                                    QtGui.QGuiApplication.translate("Image",
                                                                    "This height %s is not accepted"
                                                                    % self.fileName2, None))
            return
        if width > sizeMax:
            QMessageBox.information(self, QtGui.QGuiApplication.translate("Image", "Main Window ", None),
                                    QtGui.QGuiApplication.translate("Image",
                                                                    "This width %s is not accepted"
                                                                    % self.fileName2, None))
            return
        self.isPattern = False
        self.isPatternNB = False
        self.loadImage2()
        self.message.setText(QtGui.QGuiApplication.translate("Image", "Loaded Image: %s." % self.fileName2, None))
        self.labelMessage.setText(
            QtGui.QGuiApplication.translate("Image", "Message: Loaded Image %s" % self.fileName2, None))

    def initialize(self):
        """0 - Initialization."""

        if self.image1.isNull():
            QMessageBox.information(self,
                                    QtGui.QGuiApplication.translate("Image", "Main Window ", None),
                                    QtGui.QGuiApplication.translate("Image",
                                                                    "Please load an image!!!\n"
                                                                    "For open an image:\n"
                                                                    " - Go to the menu File/Open,\n"
                                                                    " - Select an image", None))
            return
        self.meth = 0
        # self.displayCurrentFunction(self.meth)
        print("Method: %i" % self.meth)
        self.depth = self.image1.depth() / 8
        self.image1 = QImage(self.fileName)
        if len(self.imageList) != 0:
            self.imageList.clear()
        self.imageList.append(self.image1)
        self.loadImage1()

    def copy1to2(self):
        """Copy image 1 to image 2."""

        if self.tabWidget.currentIndex() != 0:
            self.tabWidget.setCurrentIndex(0)
        if self.image1.isNull():
            self.message1()
            return
        self.hideParameter()
        self.fileName2 = self.fileName
        self.image2 = QImage(self.fileName2)
        self.loadImage2()
        self.message.setText(QtGui.QGuiApplication.translate("Image",
                                                             "Image 1: {0} and  Image 2: {1}.".format(self.fileName,
                                                                                                      self.fileName2),
                                                             None))
        self.labelMessage.setText(QtGui.QGuiApplication.translate("Image",
                                                                  "Message: Image 1: {0} and Image 2: {1}.".format(
                                                                      self.fileName, self.fileName2), None))

    def copy2to1(self):  #
        """Copy image 2 to image 1."""

        if self.tabWidget.currentIndex() != 0:
            self.tabWidget.setCurrentIndex(0)
        if self.image2.isNull():
            self.message1()
            return
        self.hideParameter()
        self.fileName = self.fileName2
        self.image1 = QImage(self.fileName)
        self.loadImage1()
        self.message.setText(QtGui.QGuiApplication.translate("Image",
                                                             "Image 1: {0} and Image 2: {1}.".format(self.fileName,
                                                                                                     self.fileName2),
                                                             None))
        self.labelMessage.setText(QtGui.QGuiApplication.translate("Image",
                                                                  "Message: Image 1: {0} and Image 2: {1}.".format(
                                                                      self.fileName, self.fileName2), None))

    def swap1and2(self):  #
        """Swap image 1 and image 2"."""

        if self.tabWidget.currentIndex() != 0:
            self.tabWidget.setCurrentIndex(0)
        if self.image1.isNull():
            self.message1()
            return
        if self.image2.isNull():
            self.message2()
            return
        self.hideParameter()
        fileNameBuffer = self.fileName
        self.imageBuffer = QImage(fileNameBuffer)
        self.fileName = self.fileName2
        self.image1 = QImage(self.fileName)
        self.loadImage1()
        self.fileName2 = fileNameBuffer
        self.image2 = QImage(self.fileName2)
        self.loadImage2()
        self.message.setText(QtGui.QGuiApplication.translate("Image",
                                                             "Image 1: {0} and Image 2: {1}.".format(self.fileName,
                                                                                                     self.fileName2),
                                                             None))
        self.labelMessage.setText(QtGui.QGuiApplication.translate("Image",
                                                                  "Message: Image 1: {0} and Image 2: {1}.".format(
                                                                      self.fileName, self.fileName2), None))

    def adjustment(self):
        """Displays messages for debugging methods."""

        if self.tabWidget.currentIndex() != 2:
            self.tabWidget.setCurrentIndex(2)
        myText = QtGui.QGuiApplication.translate("Image", "FOCUS:\n", None)
        self.message.setText(myText)

    def about(self):
        """About."""

        if currentLanguage == "English":
            QMessageBox.about(self, "About the application",
                              "<p> This <b> application</b> aims to learn how to process images in Python, "
                              "with PySide6, by implementing some filtering and edge detection algorithms, "
                              "in the spatial and frequency domain.</p>")
        elif currentLanguage == "Français":
            QMessageBox.about(self, "A propos de l'application",
                              "<p>Cette <b> application</b> a pour objectif de s'initier "
                              "au traitement d'images en Python,"
                              "avec PySide6, en implémentant quelques algorithmes de filtrage "
                              "et de détection de contours,  "
                              "dans le domaine spatial et fréquentiel.</p>")

    def operatingMode(self, folder):
        """Procedure."""

        myText = ""
        if self.tabWidget.currentIndex() != folder:
            self.tabWidget.setCurrentIndex(folder)
        if currentLanguage == "English":
            self.fileNameText = "Html/readme-en.html"
        elif currentLanguage == "Français":
            self.fileNameText = "Html/readme-fr.html"
        else:
            return
        self.labelMessage.setText(QtGui.QGuiApplication.translate("Image",
                                                                  "Message: Procedure {0} loaded".format(
                                                                      self.fileNameText), None))
        if self.fileNameText:
            with open(self.fileNameText, "r") as file:
                for line in file:
                    myText += line.strip()
        self.modOpTextBrowser.setHtml(myText)

    def displayCurrentFunction(self, method):
        """
        Shows the current function.

        :param method: id of this function
        """
        print("Method:", method)
        title = menus[method].title
        print("Title: ", title)
        param1 = menus[method].param1
        param2 = menus[method].param2
        param3 = menus[method].param3
        param4 = menus[method].param4
        param5 = menus[method].param5
        param6 = menus[method].param6
        param7 = menus[method].param7
        param8 = menus[method].param8
        numberTitle = str(method) + " - " + title
        self.message.append(numberTitle)

        if self.tabWidget.currentIndex() != 0:
            self.tabWidget.setCurrentIndex(0)

        self.hideParameter()
        if param1 != "":
            self.viewParameterA(param1)
        if param2 != "":
            self.viewParameterB(param2)
        if param3 != "":
            self.viewParameterC(param3)
        if param4 != "":
            self.viewParameterD(param4)
        if param5 != "":
            self.viewParameterE(param5)
        if param6 != "":
            self.viewParameterF(param6)
        if param7 != "":
            self.viewParameterPoint(param7)
        if param8 != "":
            self.viewParameterSeed(param8)
        self.orderLabel.setText(
            QtGui.QGuiApplication.translate("Image", "<strong>Command running: %s </strong>" % numberTitle, None))

    # The different functions
    def copyToBuffer(self):
        depth = int(self.image1.depth() / 8)
        print("Depth: ", depth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        for j in range(height):
            for i in range(width):
                color = self.image1.pixelColor(i, j)
                green = color.green()
                blue = color.blue()
                red = color.red()
                color = QColor(red, green, blue, 255)
                self.imageBuffer.setPixelColor(i, j, color)

    def copyFromBuffer(self):
        depth = int(self.imageBuffer.depth() / 8)
        print("Depth: ", depth)
        height = self.imageBuffer.height()
        width = self.imageBuffer.width()
        self.image1 = QImage(width, height, QImage.Format.Format_ARGB32)
        for j in range(height):
            for i in range(width):
                color = self.imageBuffer.pixelColor(i, j)
                green = color.green()
                blue = color.blue()
                red = color.red()
                color = QColor(red, green, blue, 255)
                self.image1.setPixelColor(i, j, color)

    def brightness(self):
        """1 - Brightness,
            Add or subtract the same value (from + 127 to - 127) for all pixels.
        """
        self.meth = 1
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        deltaBrightness = int(2.54 * self.ee - 127)
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        if deltaBrightness >= 0:
            imT["r"] = np.where(im1["r"] < 255 - deltaBrightness, im1["r"] + deltaBrightness, 255)
            imT["g"] = np.where(im1["g"] < 255 - deltaBrightness, im1["g"] + deltaBrightness, 255)
            imT["b"] = np.where(im1["b"] < 255 - deltaBrightness, im1["b"] + deltaBrightness, 255)
        else:
            imT["r"] = np.where(im1["r"] > -deltaBrightness, im1["r"] + deltaBrightness, 0)
            imT["g"] = np.where(im1["g"] > -deltaBrightness, im1["g"] + deltaBrightness, 0)
            imT["b"] = np.where(im1["b"] > -deltaBrightness, im1["b"] + deltaBrightness, 0)
        imT["a"] = im1["a"]
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - Value: " + str(deltaBrightness))
        self.orderLabel.setText(self.orderLabel.text() + " - Value: " + str(deltaBrightness))

    def contrast(self):
        """2 - Contrast
            Méthod :
            im = 255*(im-min)/(max - min)
            where min = cv and from -64 to +64
            and max = 255 -cv and from 255 to 191
            im = 255*(im-cv)/(255-2cv).
        """
        self.meth = 2
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        cv = 255 * (self.ff - 50) / 200  # cv = 0: average value and varies from -64 to +64
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        imT["r"].astype(np.uint16)
        imT["g"].astype(np.uint16)
        imT["b"].astype(np.uint16)
        imT["r"] = np.minimum(255, np.maximum(255 * (im1["r"] - cv) / (255 - 2 * cv), 0))
        imT["g"] = np.minimum(255, np.maximum(255 * (im1["g"] - cv) / (255 - 2 * cv), 0))
        imT["b"] = np.minimum(255, np.maximum(255 * (im1["b"] - cv) / (255 - 2 * cv), 0))
        imT["r"].astype(np.uint8)
        imT["g"].astype(np.uint8)
        imT["b"].astype(np.uint8)
        imT["a"] = im1["a"]
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - Value: " + str(cv))
        self.orderLabel.setText(self.orderLabel.text() + " - Value: " + str(cv))

    def luminanceMean(self):
        """3 - Luminance mean,
            lum = 1/3 R + 1/3 G + 1/3B.
        """
        self.meth = 3
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        lum = 0.333 * im1["r"] + 0.333 * im1["g"] + 0.333 * im1["b"]  # luminance
        lum = lum.astype(np.uint8)
        imT["r"] = lum
        imT["g"] = lum
        imT["b"] = lum
        imT["a"] = im1["a"]
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def luminance(self):
        """4 - Luminance
            lum = w r ⋅ R + w g ⋅ G + w b ⋅ B
            Where wr, wg and wb are 3 weighting factors R, G and B.
            For analog TV: wr=0,299 wg=0,587 and wb=0,114.
            For encoding colors: wr=0,2125 wg=0,7154 and wb=0,072.
        """
        self.meth = 4
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        lum = 0.299 * im1["r"] + 0.587 * im1["g"] + 0.114 * im1["b"]  # luminance
        lum = lum.astype(np.uint8)
        imT["r"] = lum
        imT["g"] = lum
        imT["b"] = lum
        imT["a"] = im1["a"]
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def rgb(self):
        """5 - Action on color components."""
        
        self.meth = 5
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        lumr = int(2.54 * self.dd - 127)
        lumg = int(2.54 * self.ee - 127)
        lumb = int(2.54 * self.ff - 127)
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        imT["r"] = np.minimum(255, np.maximum(im1["r"] + lumr, 0))
        imT["g"] = np.minimum(255, np.maximum(im1["g"] + lumg, 0))
        imT["b"] = np.minimum(255, np.maximum(im1["b"] + lumb, 0))
        imT["a"] = im1["a"]
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def redEffect(self):
        """6 - Red effect"""
        self.meth = 6
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        lum = 0.299 * im1["r"] + 0.587 * im1["g"] + 0.114 * im1["b"]  # luminance
        lum = lum.astype(np.uint8)
        threshold1 = np.uint8(2.54 * self.dd)
        threshold2 = np.uint8(2.54 * self.ee)
        imT["r"] = np.where(im1["r"] > threshold1, im1["r"], lum)
        imT["g"] = np.where(im1["g"] < threshold2, im1["g"], lum)
        imT["b"] = np.where(im1["r"] < threshold2, im1["b"], lum)
        imT["a"] = im1["a"]
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def thresholdFilter(self):
        """7 - Threshold"""
        self.meth = 7
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        threshold1 = self.dd * 255 / 100
        threshold1 = np.uint8(threshold1)
        threshold2 = self.ee * 255 / 100
        threshold2 = np.uint8(threshold2)
        threshold3 = self.ff * 255 / 100
        threshold3 = np.uint8(threshold3)
        im1 = q2a.recarray_view(self.image1)
        lum = 0.299 * im1["r"] + 0.587 * im1["g"] + 0.114 * im1["b"]  # luminance
        lum = lum.astype(np.uint8)
        imT = q2a.recarray_view(self.imageBuffer)
        imT["r"] = np.where(lum > threshold1, 255, 0)
        imT["g"] = np.where(lum > threshold2, 255, 0)
        imT["b"] = np.where(lum > threshold3, 255, 0)
        imT["a"] = im1["a"]
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - " + str(self.dd) + "% " + str(self.ff) + "% " + str(self.ee) + "%")
        self.orderLabel.setText(self.orderLabel.text() + " - " + str(self.dd) + "% " + str(self.ff) + "% " +
                                str(self.ee) + "%")

    def binarizationFilter(self):
        """8 - Binarization"""
        self.meth = 8
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        threshold = self.aa * 255 / 100
        threshold = np.uint8(threshold)
        im1 = q2a.recarray_view(self.image1)
        lum = 0.299 * im1["r"] + 0.587 * im1["g"] + 0.114 * im1["b"]  # luminance
        lum = lum.astype(np.uint8)
        imT = q2a.recarray_view(self.imageBuffer)
        imT["r"] = np.where(lum > threshold, 255, 0)
        imT["g"] = np.where(lum > threshold, 255, 0)
        imT["b"] = np.where(lum > threshold, 255, 0)
        imT["a"] = im1["a"]
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - " + str(self.aa) + "%")
        self.orderLabel.setText(self.orderLabel.text() + " - " + str(self.aa) + "%")

    def negativeFilter(self):
        """9 - Negative"""
        self.meth = 9
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        # For development:
        ci.negative(im1, imT)
        """
        imT["r"] = 255 - im1["r"]
        imT["g"] = 255 - im1["g"]
        imT["b"] = 255 - im1["b"]
        imT["a"] = im1["a"]
        """
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def transparency(self):
        """10 - Transparency"""
        self.meth = 10
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        alpha = self.aa * 255 / 100
        alpha = np.uint8(alpha)
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        imT["r"] = im1["r"]
        imT["g"] = im1["g"]
        imT["b"] = im1["b"]
        imT["a"] = alpha
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - " + str(self.aa) + "%")
        self.orderLabel.setText(self.orderLabel.text() + " - " + str(self.aa) + "%")

    def red(self):
        """11 - Red filter"""
        self.meth = 11
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        imT["r"] = 255 - im1["r"]
        imT["g"] = 0
        imT["b"] = 0
        imT["a"] = im1["a"]
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def green(self):
        """12 - Green filter"""
        self.meth = 12
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        imT["r"] = 0
        imT["g"] = 255 - im1["g"]
        imT["b"] = 0
        imT["a"] = im1["a"]
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def blue(self):
        """13 - Blue filter"""
        self.meth = 13
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        imT["r"] = 0
        imT["g"] = 0
        imT["b"] = 255 - im1["b"]
        imT["a"] = im1["a"]
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def windowingFilter(self):
        """14 - Windowing"""
        self.meth = 14
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        thresholdA = self.aa * 255 / 100
        A = np.uint8(thresholdA)
        thresholdB = self.bb * 255 / 100
        B = np.uint8(thresholdB)
        if A > B:
            A = B - 1
        C = 255 // (B - A)
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        lumR = np.int16(C * (im1["r"] - A))
        lumG = np.int16(C * (im1["g"] - A))
        lumB = np.int16(C * (im1["b"] - A))
        imT["r"] = np.where(im1["r"] > A, lumR, 0) + np.where(im1["r"] < B, 0, 255 - lumR)
        imT["g"] = np.where(im1["g"] > A, lumG, 0) + np.where(im1["g"] < B, 0, 255 - lumG)
        imT["b"] = np.where(im1["b"] > A, lumB, 0) + np.where(im1["b"] < B, 0, 255 - lumB)
        imT["a"] = im1["a"]
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - " + str(self.aa) + "% " + str(self.bb) + "%")
        self.orderLabel.setText(self.orderLabel.text() + " - " + str(self.aa) + "% " + str(self.bb) + "%")

    def grayTint(self):
        """15 - Shade of grey"""
        self.meth = 15
        self.displayCurrentFunction(self.meth)
        pas = self.pp
        # print("Pas: ", pas)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        for j in range(height):
            for i in range(width):
                color = self.image1.pixelColor(i, j)
                lum = int((299 * color.red() + 587 * color.green() + 114 * color.blue()) / 1000)
                alpha = color.alpha()
                if pas == 1:
                    if lum < 128:
                        color = QColor(0, 0, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    else:
                        color = QColor(255, 255, 255, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                if pas == 2:
                    if lum < 85:
                        color = QColor(0, 0, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 171:
                        color = QColor(128, 128, 128, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    else:
                        color = QColor(255, 255, 255, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                if pas == 3:
                    if lum < 64:
                        color = QColor(0, 0, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 128:
                        color = QColor(85, 85, 85, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 192:
                        color = QColor(171, 171, 171, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    else:
                        color = QColor(255, 255, 255, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                if pas == 4:
                    if lum < 51:
                        color = QColor(0, 0, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 102:
                        color = QColor(64, 64, 64, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 154:
                        color = QColor(128, 128, 128, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 205:
                        color = QColor(192, 192, 192, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    else:
                        color = QColor(255, 255, 255, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                if pas == 5:
                    if lum < 43:
                        color = QColor(0, 0, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 85:
                        color = QColor(51, 51, 51, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 128:
                        color = QColor(102, 102, 102, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 171:
                        color = QColor(154, 154, 154, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 213:
                        color = QColor(205, 205, 205, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    else:
                        color = QColor(255, 255, 255, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                if pas == 6:
                    if lum < 37:
                        color = QColor(0, 0, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 73:
                        color = QColor(43, 43, 43, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 110:
                        color = QColor(86, 86, 86, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 146:
                        color = QColor(128, 128, 128, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 183:
                        color = QColor(171, 171, 171, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 219:
                        color = QColor(213, 213, 213, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    else:
                        color = QColor(255, 255, 255, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                if pas == 7:
                    if lum < 32:
                        color = QColor(0, 0, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 64:
                        color = QColor(37, 37, 37, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 196:
                        color = QColor(73, 73, 73, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 128:
                        color = QColor(110, 110, 110, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 160:
                        color = QColor(146, 146, 146, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 192:
                        color = QColor(183, 183, 183, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 224:
                        color = QColor(219, 219, 219, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    else:
                        color = QColor(255, 255, 255, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)

        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - Step: " + str(pas))
        self.orderLabel.setText(self.orderLabel.text() + " - Step: " + str(pas))

    def colorize(self):
        """16 - Color levels"""
        self.meth = 16
        self.displayCurrentFunction(self.meth)
        pas = self.pp
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        for j in range(height):
            for i in range(width):
                color = self.image1.pixelColor(i, j)
                lum = int((299 * color.red() + 587 * color.green() + 114 * color.blue()) / 1000)
                alpha = color.alpha()
                if pas == 1:
                    if lum < 128:
                        color = QColor(0, 0, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    else:
                        color = QColor(0, 255, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                if pas == 2:
                    if lum < 85:
                        color = QColor(0, 0, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 171:
                        color = QColor(0, 0, 255, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    else:
                        color = QColor(0, 255, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                if pas == 3:
                    if lum < 64:
                        color = QColor(0, 0, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 128:
                        color = QColor(0, 0, 255, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 192:
                        color = QColor(255, 0, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    else:
                        color = QColor(0, 255, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                if pas == 4:
                    if lum < 51:
                        color = QColor(0, 0, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 102:
                        color = QColor(0, 0, 255, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 154:
                        color = QColor(255, 0, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 205:
                        color = QColor(0, 255, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    else:
                        color = QColor(0, 255, 255, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                if pas == 5:
                    if lum < 43:
                        color = QColor(0, 0, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 85:
                        color = QColor(0, 0, 255, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 128:
                        color = QColor(255, 0, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 171:
                        color = QColor(255, 0, 255, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 213:
                        color = QColor(0, 255, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    else:
                        color = QColor(0, 255, 255, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                if pas == 6:
                    if lum < 37:
                        color = QColor(0, 0, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 73:
                        color = QColor(0, 0, 255, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 110:
                        color = QColor(255, 0, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 146:
                        color = QColor(255, 0, 255, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 183:
                        color = QColor(0, 255, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 219:
                        color = QColor(0, 255, 255, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    else:
                        color = QColor(255, 255, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                if pas == 7:
                    if lum < 32:
                        color = QColor(0, 0, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 64:
                        color = QColor(0, 0, 255, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 196:
                        color = QColor(255, 0, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 128:
                        color = QColor(255, 0, 255, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 160:
                        color = QColor(0, 255, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 192:
                        color = QColor(0, 255, 255, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    elif lum < 224:
                        color = QColor(255, 255, 0, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
                    else:
                        color = QColor(255, 255, 255, alpha)
                        self.imageBuffer.setPixelColor(i, j, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - Step: " + str(pas))
        self.orderLabel.setText(self.orderLabel.text() + " - Step: " + str(pas))

    def swapColor(self):
        """17 - Change colors
        """
        self.meth = 17
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        imT["r"] = im1["g"]
        imT["g"] = im1["b"]
        imT["b"] = im1["r"]
        imT["a"] = im1["a"]
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def sepiaFilter(self):
        """18 - Sepia
        Sepia(94, 38, 18)
        """
        self.meth = 18
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        imT["r"] = np.where(im1["r"] < 171, im1["r"] + 84, 255)
        imT["g"] = np.where(im1["g"] < 217, im1["g"] + 38, 255)
        imT["b"] = np.where(im1["b"] < 237, im1["b"] + 18, 255)
        imT["a"] = im1["a"]
        # print("New pixel 10x10: ", imT[10, 10])
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def averagingFilter(self):
        """ 20 - Integrating
        n: dimension aof filter example 3x3 or 5x5
        Edges are not filtered
        """
        self.meth = 20
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        for j in range(height):
            for i in range(width):
                color = self.image1.pixelColor(i, j)
                red = color.red()
                green = color.green()
                blue = color.blue()
                alpha = color.alpha()
                color = QColor(red, green, blue, alpha)
                self.imageBuffer.setPixelColor(i, j, color)
        n = self.tt
        # print("n: ", n)
        nb = int((n - 1) / 2)
        n2 = n * n
        red1 = np.zeros((n2,), dtype=np.uint8)
        green1 = np.zeros((n2,), dtype=np.uint8)
        blue1 = np.zeros((n2,), dtype=np.uint8)
        alpha1 = np.zeros((n2,), dtype=np.uint8)
        for j in range(nb, height - nb, 1):
            for i in range(nb, width - nb, 1):
                for jj in range(n):
                    for ii in range(n):
                        color = self.image1.pixelColor(i + ii - nb, j + jj - nb)
                        red1[ii + jj * n] = color.red()
                        green1[ii + jj * n] = color.green()
                        blue1[ii + jj * n] = color.blue()
                        alpha1[ii + jj * n] = color.alpha()
                red = mean(red1)
                green = mean(green1)
                blue = mean(blue1)
                alpha = mean(alpha1)
                color = QColor(red, green, blue, alpha)
                self.imageBuffer.setPixelColor(i, j, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - Filter size: " + str(n))
        self.orderLabel.setText(self.orderLabel.text() + " - Filter size: " + str(n))

    def medianFilter(self):
        """ 21 - Median filter
        n: dimension aof filter example 3x3 or 5x5
        Edges are not filtered
        """
        self.meth = 21
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        for j in range(height):
            for i in range(width):
                color = self.image1.pixelColor(i, j)
                red = color.red()
                green = color.green()
                blue = color.blue()
                alpha = color.alpha()
                color = QColor(red, green, blue, alpha)
                self.imageBuffer.setPixelColor(i, j, color)
        n = self.tt
        # print("n: ", n)
        nb = int((n - 1) / 2)
        n2 = n * n
        red1 = np.zeros((n2,), dtype=np.uint8)
        green1 = np.zeros((n2,), dtype=np.uint8)
        blue1 = np.zeros((n2,), dtype=np.uint8)
        alpha1 = np.zeros((n2,), dtype=np.uint8)
        for j in range(nb, height - nb, 1):
            for i in range(nb, width - nb, 1):
                for jj in range(n):
                    for ii in range(n):
                        color = self.image1.pixelColor(i + ii - nb, j + jj - nb)
                        red1[ii + jj * n] = color.red()
                        green1[ii + jj * n] = color.green()
                        blue1[ii + jj * n] = color.blue()
                        alpha1[ii + jj * n] = color.alpha()
                red = median(red1)
                green = median(green1)
                blue = median(blue1)
                alpha = median(alpha1)
                color = QColor(red, green, blue, alpha)
                self.imageBuffer.setPixelColor(i, j, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - Filter size: " + str(n))
        self.orderLabel.setText(self.orderLabel.text() + " - Filter size: " + str(n))

    def gaussianFilter(self):
        """22 - Gaussian Filter
            Gaussian Filter 5x5

            Filter mask is:
                2  4  5  4  2
                4  9 12  9  4
                5 12 15 12  5
                4  9 12  9  4
                2  4  5  4  2

            Edges are not filtered (2 pixels)
        """
        self.meth = 22
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        red1 = np.zeros((25,), dtype=np.uint8)
        green1 = np.zeros((25,), dtype=np.uint8)
        blue1 = np.zeros((25,), dtype=np.uint8)
        alpha1 = np.zeros((25,), dtype=np.uint8)
        for j in range(2, height - 2, 1):
            for i in range(2, width - 2, 1):
                for jj in range(5):
                    for ii in range(5):
                        color = self.image1.pixelColor(i + ii - 2, j + jj - 2)
                        red1[ii + jj * 5] = color.red()
                        green1[ii + jj * 5] = color.green()
                        blue1[ii + jj * 5] = color.blue()
                        alpha1[ii + jj * 5] = color.alpha()
                red = (2 * red1[0] + 4 * red1[1] + 5 * red1[2] + 4 * red1[3] + 2 * red1[4]
                       + 4 * red1[5] + 9 * red1[6] + 12 * red1[7] + 9 * red1[8] + 4 * red1[9]
                       + 5 * red1[10] + 12 * red1[11] + 15 * red1[12] + 12 * red1[13] + 5 * red1[14]
                       + 4 * red1[15] + 9 * red1[16] + 12 * red1[17] + 9 * red1[18] + 4 * red1[19]
                       + 2 * red1[20] + 4 * red1[21] + 5 * red1[22] + 4 * red1[23] + 2 * red1[24]) / 157
                green = (2 * green1[0] + 4 * green1[1] + 5 * green1[2] + 4 * green1[3] + 2 * green1[4]
                         + 4 * green1[5] + 9 * green1[6] + 12 * green1[7] + 9 * green1[8] + 4 * green1[9]
                         + 5 * green1[10] + 12 * green1[11] + 15 * green1[12] + 12 * green1[13] + 5 * green1[14]
                         + 4 * green1[15] + 9 * green1[16] + 12 * green1[17] + 9 * green1[18] + 4 * green1[19]
                         + 2 * green1[20] + 4 * green1[21] + 5 * green1[22] + 4 * green1[23] + 2 * green1[24]) / 157
                blue = (2 * blue1[0] + 4 * blue1[1] + 5 * blue1[2] + 4 * blue1[3] + 2 * blue1[4]
                        + 4 * blue1[5] + 9 * blue1[6] + 12 * blue1[7] + 9 * blue1[8] + 4 * blue1[9]
                        + 5 * blue1[10] + 12 * blue1[11] + 15 * blue1[12] + 12 * blue1[13] + 5 * blue1[14]
                        + 4 * blue1[15] + 9 * blue1[16] + 12 * blue1[17] + 9 * blue1[18] + 4 * blue1[19]
                        + 2 * blue1[20] + 4 * blue1[21] + 5 * blue1[22] + 4 * blue1[23] + 2 * blue1[24]) / 157
                alpha = alpha1[12]
                red = min(255, int(red))
                green = min(255, int(green))
                blue = min(255, int(blue))
                alpha = int(alpha)
                color = QColor(red, green, blue, alpha)
                self.imageBuffer.setPixelColor(i, j, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def hrgradient(self):
        """23 - Horizontal gradient
            Horizontal Filter:
                 1  2  1
                 0  0  0
                -1 -2 -1
            And
                Pixel(i, j) = 255-min(255, h(i,j))
            Edges are not filtered
        """
        self.meth = 23
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        """
        *** With Pybind11 ***
        s = bytes(np.array(self.image1.constBits()).reshape(height * width * 4))
        im1 = np.frombuffer(s, dtype=np.uint8).reshape((height, width, 4))
        # im1 = de.normex_arrays(im1).copy()
        s = im1.tobytes()
        ba = QByteArray(s)
        self.bytesToImage(ba, width, height, 4)

        *** With Cython ***
        """
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        ci.hrGradient(im1, imT)

        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def vtgradient(self):
        """24 - Vertical gradient
            Vertical Filter
                1 0 -1
                2 0 -2
                1 0 -1
            And
                Pixel(i, j) = 255-min(255, v(i, j))
            Edges are not filtered
        """
        self.meth = 24
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)

        """
        *** With Pybind11 ***
        s = bytes(np.array(self.image1.constBits()).reshape(height * width * 4))
        im1 = np.frombuffer(s, dtype=np.uint8).reshape((height, width, 4))
        # im1 = de.normey_arrays(im1).copy()
        ba = QByteArray(im1.tobytes())
        self.bytesToImage(ba, width, height, 4)

        *** With Cython ***
        """
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        ci.vtGradient(im1, imT)

        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def bytesToImage(self, ba, width, height, depth):
        size = ba.size()
        pixel = np.zeros(size)
        for p in range(size):
            pixel[p] = int.from_bytes(ba[p], "little")
        pixel = pixel.reshape((height, width, depth))
        for h in range(height):
            for w in range(width):
                red = pixel[h, w, 2]
                green = pixel[h, w, 1]
                blue = pixel[h, w, 0]
                alpha = pixel[h, w, 3]
                color = QColor(int(red), int(green), int(blue), int(alpha))
                self.imageBuffer.setPixelColor(w, h, color)

    def borderDetect(self):
        """25 - Border detect
        Sobel Filter :
            First -> Horizontal Filter -> h(i, j)
                1  2  1
                0  0  0
                -1 -2 -1
            Second -<>Vertical Filter -> v(i, j)
                1 0 -1
                2 0 -2
                1 0 -1
            And
                Pixel(i, j) = 255-min(255, v(i, j) + h(i,j))
            Edges are not filtered
        """
        self.meth = 25
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)

        """
        *** With Pybind11 ***
        s = bytes(np.array(self.image1.constBits()).reshape(height * width * 4))
        im1 = np.frombuffer(s, dtype=np.uint8).reshape((height, width, 4))
        # im1 = de.normex_arrays(im1).copy()
        # im1 = de.normey_arrays(im1).copy()
        ba = QByteArray(im1.tobytes())
        self.bytesToImage(ba, width, height, 4)

        *** With Cython ***
        """
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        ci.border(im1, imT)

        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.imageLabel.setPixmap(QPixmap.fromImage(self.image1))  # Puts the image into imageLabel

    def erosion(self):
        """26 - Erosion
        Image erosion -> remove roughness
         3x3 erosion filtering
             The filter mask is:
                 0 1 0
                 1 1 1
                 0 1 0

             Method: take the MINIMUM of the elements contained in the cross for each pixel
             The edges of the image are not filtered (for 1 pixel)
        """
        self.meth = 26
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        tabRed = np.zeros((5,), dtype=np.uint8)
        tabGreen = np.zeros((5,), dtype=np.uint8)
        tabBlue = np.zeros((5,), dtype=np.uint8)
        for j in range(1, height - 1, 1):
            for i in range(1, width - 1, 1):
                color = self.image1.pixelColor(i, j - 1)
                tabRed[0] = color.red()
                tabGreen[0] = color.green()
                tabBlue[0] = color.blue()
                color = self.image1.pixelColor(i - 1, j)
                tabRed[1] = color.red()
                tabGreen[1] = color.green()
                tabBlue[1] = color.blue()
                color = self.image1.pixelColor(i, j)
                tabRed[2] = color.red()
                tabGreen[2] = color.green()
                tabBlue[2] = color.blue()
                alpha = color.alpha()
                color = self.image1.pixelColor(i + 1, j)
                tabRed[3] = color.red()
                tabGreen[3] = color.green()
                tabBlue[3] = color.blue()
                color = self.image1.pixelColor(i, j + 1)
                tabRed[4] = color.red()
                tabGreen[4] = color.green()
                tabBlue[4] = color.blue()
                tabRed.sort()
                tabGreen.sort()
                tabBlue.sort()
                red = min(255, int(tabRed[0]))
                green = min(255, int(tabGreen[0]))
                blue = min(255, int(tabBlue[0]))
                color = QColor(red, green, blue, alpha)
                self.imageBuffer.setPixelColor(i, j, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def dilatation(self):
        """27 - Dilatation
        Image Dilation -> Fill Gaps
         3x3 dilation filtering
             The filter mask is:
                 0 1 0
                 1 1 1
                 0 1 0

             Method: take the MAXIMUM of the elements contained in the cross for each pixel
             The edges of the image are not filtered (for 1 pixel)
        """
        self.meth = 27
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        tabRed = np.zeros((5,), dtype=np.uint8)
        tabGreen = np.zeros((5,), dtype=np.uint8)
        tabBlue = np.zeros((5,), dtype=np.uint8)
        for j in range(1, height - 1, 1):
            for i in range(1, width - 1, 1):
                color = self.image1.pixelColor(i, j - 1)
                tabRed[0] = color.red()
                tabGreen[0] = color.green()
                tabBlue[0] = color.blue()
                color = self.image1.pixelColor(i - 1, j)
                tabRed[1] = color.red()
                tabGreen[1] = color.green()
                tabBlue[1] = color.blue()
                color = self.image1.pixelColor(i, j)
                tabRed[2] = color.red()
                tabGreen[2] = color.green()
                tabBlue[2] = color.blue()
                alpha = color.alpha()
                color = self.image1.pixelColor(i + 1, j)
                tabRed[3] = color.red()
                tabGreen[3] = color.green()
                tabBlue[3] = color.blue()
                color = self.image1.pixelColor(i, j + 1)
                tabRed[4] = color.red()
                tabGreen[4] = color.green()
                tabBlue[4] = color.blue()
                tabRed.sort()
                tabGreen.sort()
                tabBlue.sort()
                red = min(255, int(tabRed[4]))
                green = min(255, int(tabGreen[4]))
                blue = min(255, int(tabBlue[4]))
                color = QColor(red, green, blue, alpha)
                self.imageBuffer.setPixelColor(i, j, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def gammaFilter(self):
        """28 - Gamma filter
        the gamma method:
             the Function used is g(x,y) = (gmax/pow(gmax,gamma))(pow(f(x,y),gamma)
             gmax = 255
             gamma can vary from 0.1 to 2.0
        """
        self.meth = 28
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        gamma = int(self.cc / 10)
        # print("gamma: ", gamma)
        gmax = 255
        coef = gmax / pow(gmax, gamma)
        # print("coef: ", coef)
        for j in range(height):
            for i in range(width):
                color = self.image1.pixelColor(i, j)
                red = min(255, int(coef * pow(color.red(), gamma)))
                green = min(255, int(coef * pow(color.green(), gamma)))
                blue = min(255, int(coef * pow(color.blue(), gamma)))
                alpha = color.alpha()
                color = QColor(red, green, blue, alpha)
                self.imageBuffer.setPixelColor(i, j, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - gamma = " + str(gamma))
        self.orderLabel.setText(self.orderLabel.text() + " - gamma = " + str(gamma))

    def pointer(self):
        """29 - Draws black points"""
        self.meth = 29
        self.displayCurrentFunction(self.meth)
        step = self.pp  # step 1 to 5
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        im1 = q2a.recarray_view(self.image1)
        # print("Pixel 10x10: ", im1[10, 10])
        imT = q2a.recarray_view(self.imageBuffer)
        lum = 0.299 * im1["r"] + 0.587 * im1["g"] + 0.114 * im1["b"]  # luminance
        lum = lum.astype(np.uint8)

        imT["r"] = 0  # imT black
        imT["g"] = 0
        imT["b"] = 0
        imT["a"] = im1["a"]

        if step == 1:
            imT["r"] = np.where(lum > 128, 255, 0)
            imT["g"] = np.where(lum > 128, 255, 0)
            imT["b"] = np.where(lum > 128, 255, 0)
        else:
            ci.point(imT, lum, step)
        # print("New pixel 10x10: ", imT[10, 10])
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def verticalStroke(self):
        """30 - Draws vertical black lines"""
        self.meth = 30
        self.displayCurrentFunction(self.meth)
        step = self.pp  # step 1 to 5
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        im1 = q2a.recarray_view(self.image1)
        # print("Pixel 10x10: ", im1[10, 10])
        imT = q2a.recarray_view(self.imageBuffer)
        lum = 0.299 * im1["r"] + 0.587 * im1["g"] + 0.114 * im1["b"]  # luminance
        lum = lum.astype(np.uint8)

        imT["r"] = 0  # imT black
        imT["g"] = 0
        imT["b"] = 0
        imT["a"] = im1["a"]

        if step == 1:
            imT["r"] = np.where(lum > 128, 255, 0)
            imT["g"] = np.where(lum > 128, 255, 0)
            imT["b"] = np.where(lum > 128, 255, 0)
        else:
            ci.stroke(imT, lum, step)
        # print("New pixel 10x10: ", imT[10, 10])
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def horizontalStroke(self):
        """31 - Draws horizontal black lines
            with rotation 90°, Vertical Stroke, inverse rotation 90°

        self.meth = 72
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(height, width, QImage.Format_ARGB32)
        for j in range(height):
            for i in range(width):
                color = self.image1.pixelColor(i, j)
                self.imageBuffer.setPixelColor(height - 1 - j, i, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()


        """

        self.meth = 31
        self.displayCurrentFunction(self.meth)
        step = self.pp  # step 1 to 5
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        self.imageBuffer2 = QImage(height, width, QImage.Format.Format_ARGB32)

        # First rotation
        for j in range(height):
            for i in range(width):
                color = self.image1.pixelColor(i, j)
                self.imageBuffer2.setPixelColor(height - 1 - j, i, color)
        self.image2 = self.imageBuffer2

        # Vertical Stroke
        im1 = q2a.recarray_view(self.image2)
        imT2 = q2a.recarray_view(self.imageBuffer2)
        lum = 0.299 * im1["r"] + 0.587 * im1["g"] + 0.114 * im1["b"]  # luminance
        lum = lum.astype(np.uint8)

        imT2["r"] = 0  # imT black
        imT2["g"] = 0
        imT2["b"] = 0
        imT2["a"] = im1["a"]

        if step == 1:
            imT2["r"] = np.where(lum > 128, 255, 0)
            imT2["g"] = np.where(lum > 128, 255, 0)
            imT2["b"] = np.where(lum > 128, 255, 0)
        else:
            ci.stroke(imT2, lum, step)

        # Inverse rotation
        for k in range(width):
            for h in range(height):
                color = self.imageBuffer2.pixelColor(h, k)
                self.imageBuffer.setPixelColor(k, height - h - 1, color)

        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def convolutionFilter(self):
        """32 - Convolution
        3x3 convolution filter
             The filter mask is for example
                 -1 -1 -1
                 -1 8 -1
                 -1 -1 -1

             Sum must be 0
             The edges of the image are not filtered (for 1 pixel)
        """
        self.meth = 32
        self.displayCurrentFunction(self.meth)
        # Creating a new image with the same dimensions
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        tabRed = np.zeros((9,), dtype=np.uint8)
        tabGreen = np.zeros((9,), dtype=np.uint8)
        tabBlue = np.zeros((9,), dtype=np.uint8)
        for j in range(1, height - 1, 1):
            for i in range(1, width - 1, 1):
                color = self.image1.pixelColor(i - 1, j - 1)
                tabRed[0] = color.red()
                tabGreen[0] = color.green()
                tabBlue[0] = color.blue()
                color = self.image1.pixelColor(i - 1, j)
                tabRed[1] = color.red()
                tabGreen[1] = color.green()
                tabBlue[1] = color.blue()
                color = self.image1.pixelColor(i - 1, j + 1)
                tabRed[2] = color.red()
                tabGreen[2] = color.green()
                tabBlue[2] = color.blue()
                color = self.image1.pixelColor(i - 1, j)
                tabRed[3] = color.red()
                tabGreen[3] = color.green()
                tabBlue[3] = color.blue()
                color = self.image1.pixelColor(i, j)
                tabRed[4] = color.red()
                tabGreen[4] = color.green()
                tabBlue[4] = color.blue()
                alpha = color.alpha()
                color = self.image1.pixelColor(i, j + 1)
                tabRed[5] = color.red()
                tabGreen[5] = color.green()
                tabBlue[5] = color.blue()
                color = self.image1.pixelColor(i + 1, j - 1)
                tabRed[6] = color.red()
                tabGreen[6] = color.green()
                tabBlue[6] = color.blue()
                color = self.image1.pixelColor(i + 1, j)
                tabRed[7] = color.red()
                tabGreen[7] = color.green()
                tabBlue[7] = color.blue()
                color = self.image1.pixelColor(i + 1, j + 1)
                tabRed[8] = color.red()
                tabGreen[8] = color.green()
                tabBlue[8] = color.blue()
                red = max(0, min(255, int(
                        tabRed[0] * self.filter[0][0] + tabRed[1] * self.filter[1][0] + tabRed[2] * self.filter[2][0]
                        + tabRed[3] * self.filter[0][1] + tabRed[4] * self.filter[1][1] + tabRed[5] *
                        self.filter[2][1]
                        + tabRed[6] * self.filter[0][2] + tabRed[7] * self.filter[1][2] + tabRed[8] *
                        self.filter[2][2])))
                green = max(0, min(255, int(
                        tabGreen[0] * self.filter[0][0] + tabGreen[1] * self.filter[1][0] + tabGreen[2] *
                        self.filter[2][0]
                        + tabGreen[3] * self.filter[0][1] + tabGreen[4] * self.filter[1][1] + tabGreen[5] *
                        self.filter[2][1]
                        + tabGreen[6] * self.filter[0][2] + tabGreen[7] * self.filter[1][2] + tabGreen[8] *
                        self.filter[2][2])))
                blue = max(0, min(255, int(tabBlue[0] * self.filter[0][0] + tabBlue[1] * self.filter[1][0] + tabBlue[2] *
                                        self.filter[2][0]
                                        + tabBlue[3] * self.filter[0][1] + tabBlue[4] * self.filter[1][1] + tabBlue[5] *
                                        self.filter[2][1]
                                        + tabBlue[6] * self.filter[0][2] + tabBlue[7] * self.filter[1][2] + tabBlue[8] *
                                        self.filter[2][2])))
                color = QColor(red, green, blue, alpha)
                self.imageBuffer.setPixelColor(i, j, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def redBackground(self):
        """40 - Red background"""
        self.meth = 40
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        for j in range(height):
            for i in range(width):
                color = self.image1.pixelColor(i, j)
                alpha = color.alpha()
                color = QColor(255, 0, 0, alpha)
                self.imageBuffer.setPixelColor(i, j, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def greenBackground(self):
        """41 - Green background"""
        self.meth = 41
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        for j in range(height):
            for i in range(width):
                color = self.image1.pixelColor(i, j)
                alpha = color.alpha()
                color = QColor(0, 255, 0, alpha)
                self.imageBuffer.setPixelColor(i, j, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def blueBackground(self):
        """42 - blue background"""
        self.meth = 42
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        for j in range(height):
            for i in range(width):
                color = self.image1.pixelColor(i, j)
                alpha = color.alpha()
                color = QColor(0, 0, 255, alpha)
                self.imageBuffer.setPixelColor(i, j, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def whiteBackground(self):
        """43 - White background"""
        self.meth = 43
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        for j in range(height):
            for i in range(width):
                color = self.image1.pixelColor(i, j)
                alpha = color.alpha()
                color = QColor(255, 255, 255, alpha)
                self.imageBuffer.setPixelColor(i, j, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def blackBackground(self):
        """44 - Black background"""
        self.meth = 44
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        imT["r"] = 0
        imT["g"] = 0
        imT["b"] = 0
        imT["a"] = im1["a"]
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def backgroundHue(self):
        """45 - Black background"""
        self.meth = 45
        self.displayCurrentFunction(self.meth)
        red = np.uint8(self.dd * 255 / 100)
        green = np.uint8(self.ee * 255 / 100)
        blue = np.uint8(self.ff * 255 / 100)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        imT["r"] = red
        imT["g"] = green
        imT["b"] = blue
        imT["a"] = im1["a"]
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def greenScreen(self):
        """46 - Green Screen Overlay"""
        self.meth = 46
        self.displayCurrentFunction(self.meth)
        if self.image2.isNull():
            self.message2()
            return
        height1 = self.image1.height()
        width1 = self.image1.width()
        height2 = self.image2.height()
        width2 = self.image2.width()
        height = min(height1, height2)
        width = min(width1, width2)
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        im1 = q2a.recarray_view(self.image1)
        im2 = q2a.recarray_view(self.image2)
        imT = q2a.recarray_view(self.imageBuffer)
        imT["a"] = np.where(im2["g"][0:height, 0:width] > 224, 0, 255)
        imT["a"] = np.where(im2["r"][0:height, 0:width] > 32, im2["r"][0:height, 0:width], 0)
        imT["a"] = np.where(im2["b"][0:height, 0:width] > 32, im2["r"][0:height, 0:width], 0)
        imT["r"] = np.where(imT["a"] == 0, im1["r"][0:height, 0:width], im2["r"][0:height, 0:width])
        imT["g"] = np.where(imT["a"] == 0, im1["g"][0:height, 0:width], im2["g"][0:height, 0:width])
        imT["b"] = np.where(imT["a"] == 0, im1["b"][0:height, 0:width], im2["b"][0:height, 0:width])
        imT["a"] = 255
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def anaglyph(self):
        """47 - Anaglyph
        Make an anaglyph by superimposing image 2 (right) filtered in blue and green
         on image 1 (left) filtered in red
        """
        self.meth = 47
        self.displayCurrentFunction(self.meth)
        if self.image2.isNull():
            self.message2()
            return
        height1 = self.image1.height()
        width1 = self.image1.width()
        height2 = self.image2.height()
        width2 = self.image2.width()
        height = min(height1, height2)
        width = min(width1, width2)
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        im1 = q2a.recarray_view(self.image1)
        im2 = q2a.recarray_view(self.image2)
        imT = q2a.recarray_view(self.imageBuffer)
        imT["r"] = im1["r"][0:height, 0:width]  # On image 1 (Left) conservation of red
        imT["g"] = im2["g"][0:height, 0:width]  # On image 2 (Right) conservation of green
        imT["b"] = im2["b"][0:height, 0:width]  # On image 2 (Right) conservation of blue
        imT["a"] = 255
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def superimpose1on2(self):
        """48 - Superimpose image 1 on image 2"""
        self.meth = 48
        self.displayCurrentFunction(self.meth)
        r1 = self.ff / 100
        r2 = 1 - r1
        if self.image2.isNull():
            self.message2()
            return
        height1 = self.image1.height()
        width1 = self.image1.width()
        height2 = self.image2.height()
        width2 = self.image2.width()
        height = min(height1, height2)
        width = min(width1, width2)
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        im1 = q2a.recarray_view(self.image1)
        im2 = q2a.recarray_view(self.image2)
        imT = q2a.recarray_view(self.imageBuffer)
        imT["r"] = r1 * im1["r"][0:height, 0:width] + r2 * im2["r"][0:height, 0:width]
        imT["g"] = r1 * im1["g"][0:height, 0:width] + r2 * im2["g"][0:height, 0:width]
        imT["b"] = r1 * im1["b"][0:height, 0:width] + r2 * im2["b"][0:height, 0:width]
        imT["a"] = 255
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - Ratio: " + str(r1))
        self.orderLabel.setText(self.orderLabel.text() + " - Ratio: " + str(r1))

    def noiseWhiteMaker(self):
        """ 50 - White noise """
        self.meth = 50
        self.displayCurrentFunction(self.meth)
        number = self.aa
        if number == 0:
            number = 1
        height = self.image1.height()
        width = self.image1.width()
        im1 = q2a.recarray_view(self.image1)
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        imT = q2a.recarray_view(self.imageBuffer)
        noise = np.random.randint(number, size=(height, width))
        imT["r"].astype(np.uint16)
        imT["g"].astype(np.uint16)
        imT["b"].astype(np.uint16)
        imT["r"] = np.minimum(255, np.maximum(im1["r"] + noise, 0))
        imT["g"] = np.minimum(255, np.maximum(im1["g"] + noise, 0))
        imT["b"] = np.minimum(255, np.maximum(im1["b"] + noise, 0))
        imT["r"].astype(np.uint8)
        imT["g"].astype(np.uint8)
        imT["b"].astype(np.uint8)
        imT["a"] = im1["a"]
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - Max: " + str(number))
        self.orderLabel.setText(self.orderLabel.text() + " - Max: " + str(number))

    def noisePepperMaker(self):
        """ 51 - Pepper and salt noise """
        self.meth = 51
        self.displayCurrentFunction(self.meth)
        number = 100 - self.aa  # 0 to 100
        # print("Number: ", number)
        if number == 0:
            number = 1
        density = 1 / number
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        imT = q2a.recarray_view(self.imageBuffer)
        im1 = q2a.recarray_view(self.image1)
        imT["r"] = im1["r"]
        imT["g"] = im1["g"]
        imT["b"] = im1["b"]
        imT["a"] = im1["a"]
        noise = np.random.randint(number + 1, size=(height, width))
        # Pepper
        pepper = np.where(noise == 0)
        lines = pepper[0]
        rows = pepper[1]
        for i in range(len(lines)):
            imT[lines[i], rows[i]]["r"] = 0
            imT[lines[i], rows[i]]["g"] = 0
            imT[lines[i], rows[i]]["b"] = 0
        # Salt
        salt = np.where(noise == number)
        lines = salt[0]
        rows = salt[1]
        for i in range(len(lines)):
            imT[lines[i], rows[i]]["r"] = 255
            imT[lines[i], rows[i]]["g"] = 255
            imT[lines[i], rows[i]]["b"] = 255
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - Density: " + str(density))
        self.orderLabel.setText(self.orderLabel.text() + " - Density: " + str(density))

    def noiseGaussianMaker(self):
        """ 52 - Gaussian noise """
        self.meth = 52
        self.displayCurrentFunction(self.meth)
        sigma = self.aa / 10
        # print("Sigma: ", sigma)
        height = self.image1.height()
        width = self.image1.width()
        im1 = q2a.recarray_view(self.image1)
        # print("Pixel 10x10: ", im1[10, 10])
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        imT = q2a.recarray_view(self.imageBuffer)
        size = height * width
        noise = np.random.normal(0, sigma, size)
        noise = noise.reshape(height, width)
        imT["r"].astype(np.uint16)
        imT["g"].astype(np.uint16)
        imT["b"].astype(np.uint16)
        imT["r"] = np.minimum(255, np.maximum(im1["r"] + noise, 0))
        imT["g"] = np.minimum(255, np.maximum(im1["g"] + noise, 0))
        imT["b"] = np.minimum(255, np.maximum(im1["b"] + noise, 0))
        imT["r"].astype(np.uint8)
        imT["g"].astype(np.uint8)
        imT["b"].astype(np.uint8)
        imT["a"] = im1["a"]
        # print("New pixel 10x10: ", imT[10, 10])
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - Sigma: " + str(sigma))
        self.orderLabel.setText(self.orderLabel.text() + "Sigma: " + str(sigma))

    def pixelate(self):
        """60 - Pixelation"""
        self.meth = 60
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        if self.dd > 99 or self.dd < 1:
            self.dd = 50
        pas = self.dd
        # print("Pas: ", pas)
        if width - 1 < height - 1:
            p = int((width - 1) * pas / 1000)
        else:
            p = int((height - 1) * pas / 1000)
        if p < 1:
            p = 1
        # print("p: ", p)
        for j in range(height):
            mj = j % p
            for i in range(width):
                mi = i % p
                color = self.image1.pixelColor(i - mi, j - mj)
                self.imageBuffer.setPixelColor(i, j, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - " + str(pas) + "pixels")
        self.orderLabel.setText(self.orderLabel.text() + " - " + str(pas) + "pixels")

    def encryption(self):
        """61 - Encryption"""
        self.meth = 61
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        offset = int(0.005 * self.cc * width)  # 0 to 1/10 width max
        # print("Offset: ", offset)
        im1 = q2a.recarray_view(self.image1)
        # print("Pixel 10x10: ", im1[10, 10])
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        imT = q2a.recarray_view(self.imageBuffer)
        r = np.random.random_integers(0, 2, height)  # Array 1d of x integers 10 from 0 to 3
        r = r * offset
        for j in range(height):
            for i in range(width - 1, r[j], -1):
                imT[j, i]["r"] = im1[j, i - r[j]]["r"]
                imT[j, i]["g"] = im1[j, i - r[j]]["g"]
                imT[j, i]["b"] = im1[j, i - r[j]]["b"]
        imT["a"] = im1["a"]
        # print("New pixel 10x10: ", imT[10, 10])
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def fixedEncryption(self):
        """62 - Fixed encryption"""
        self.meth = 62
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        offset = int(0.05 * width)  # 1/20 width
        # print("Offset: ", offset)
        # print("Seed: ", self.seed)
        im1 = q2a.recarray_view(self.image1)
        # print("Pixel 10x10: ", im1[10, 10])
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        imT = q2a.recarray_view(self.imageBuffer)
        np.random.seed(self.seed)
        r = np.random.random_integers(0, 2, height)  # Array 1d of x integers 10 from 0 to 3
        r = r * offset
        for j in range(height):
            for i in range(width - 1, r[j], -1):
                imT[j, i]["r"] = im1[j, i - r[j]]["r"]
                imT[j, i]["g"] = im1[j, i - r[j]]["g"]
                imT[j, i]["b"] = im1[j, i - r[j]]["b"]
        imT["a"] = im1["a"]
        # print("New pixel 10x10: ", imT[10, 10])
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def decryption(self):
        """63 - Decryption"""
        self.meth = 63
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        offset = int(0.05 * width)  # 1/20 width
        # print("Offset: ", offset)
        # print("Seed: ", self.seed)
        im1 = q2a.recarray_view(self.image1)
        # print("Pixel 10x10: ", im1[10, 10])
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        imT = q2a.recarray_view(self.imageBuffer)
        # r = np.randInt([0,1,2], height)
        np.random.seed(self.seed)
        r = np.random.random_integers(0, 2, height)  # Array 1d of x integers 10 from 0 to 3
        r = r * offset
        for j in range(height):
            for i in range(r[j], width - r[j], ):
                imT[j, i]["r"] = im1[j, i + r[j]]["r"]
                imT[j, i]["g"] = im1[j, i + r[j]]["g"]
                imT[j, i]["b"] = im1[j, i + r[j]]["b"]
        imT["a"] = im1["a"]
        # print("New pixel 10x10: ", imT[10, 10])
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def hideSecret(self):
        """64 hide a secret image into an image
        This involves inserting a secret message (image 2 in monochrome) into an image (image 1)
         For this, the first least significant bit of the green component of image 1 is set to 0
         then replaced by the least significant bit of the second image
        """
        self.meth = 64
        self.displayCurrentFunction(self.meth)
        height1 = self.image1.height()
        width1 = self.image1.width()
        if self.image2.isNull():
            self.message2()
            return
        height2 = self.image2.height()
        width2 = self.image2.width()
        height = min(height1, height2)
        width = min(width1, width2)
        im1 = q2a.recarray_view(self.image1)
        # print("Pixel1 10x10: ", im1[10, 10])
        im2 = q2a.recarray_view(self.image2)
        im2[10, 10]["r"] = 255
        # print("Pixel2 10x10: ", im2[10, 10])
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        imT = q2a.recarray_view(self.imageBuffer)
        for j in range(height):
            for i in range(width):
                #  delete the least significant bit of image 1
                im1[j, i]["r"] = im1[j, i]["r"] & 0b11111110
                im1[j, i]["g"] = im1[j, i]["g"] & 0b11111110
                im1[j, i]["b"] = im1[j, i]["b"] & 0b11111110
                # delete the most significant bits of image 2
                im2[j, i]["r"] = im2[j, i]["r"] & 0b00000001
                im2[j, i]["g"] = im2[j, i]["g"] & 0b00000001
                im2[j, i]["b"] = im2[j, i]["b"] & 0b00000001
                # superimpose images 1 and 2
                imT[j, i]["r"] = im1[j, i]["r"] + im2[j, i]["r"]
                imT[j, i]["g"] = im1[j, i]["g"] + im2[j, i]["g"]
                imT[j, i]["b"] = im1[j, i]["b"] + im2[j, i]["b"]
                imT[j, i]["a"] = im1[j, i]["a"]
        # print("PixelT 10x10: ", imT[10, 10])
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def showSecret(self):  #
        """65 show a secret image into an image
        """
        self.meth = 65
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        im1 = q2a.recarray_view(self.image1)
        # print("Pixel1 10x10: ", im1[10, 10])
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        imT = q2a.recarray_view(self.imageBuffer)
        for j in range(height):
            for i in range(width):
                if im1[j, i]["r"] & 0b00000001:
                    imT[j, i]["r"] = 255
                else:
                    imT[j, i]["r"] = 0
                if im1[j, i]["g"] & 0b00000001:
                    imT[j, i]["g"] = 255
                else:
                    imT[j, i]["g"] = 0
                if im1[j, i]["b"] & 0b00000001:
                    imT[j, i]["b"] = 255
                else:
                    imT[j, i]["b"] = 0
                imT[j, i]["a"] = im1[j, i]["a"]
        # print("PixelT 10x10: ", imT[10, 10])
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def hideText(self):
        """66 hide a secret message into an image
        /* This is to insert a secret message in an image (image 1).
          * Method :
          * Each character (ASCII) is converted to binary
          * This binary is included in the image pixels:
          * binary = 0 then if unchanged even pixel, if odd pixel then pixel +1 (or -1 if the pixel is 255)
          * binary = 1 then if odd pixel unchanged if even pixel then pixel +1.
          * example :
          * character A (65) becomes 0 1 0 0 0 0 0 1
          * pixels Image(r,g,b,a) 255 255 255 153 219 5 102 0 become
          * Image (r,g,b,a) 254 255 254 154 220 6 102 1
        """
        self.meth = 66
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        im1 = q2a.recarray_view(self.image1)
        # print("Pixel1 0x0: ", im1[0, 0])
        # print("Pixel1 0x1: ", im1[0, 1])
        msg = self.textEditHideMessage.toPlainText()
        sizeMsg = len(msg)
        # print("Size: ", sizeMsg)
        binary = [0 for _ in range(8 * sizeMsg)]
        # letter = [ord(c) for c in msg]
        for j in range(sizeMsg):
            letter = ord(msg[j])
            if letter & 0b10000000 > 0:
                binary[8 * j] = 1
            else:
                binary[8 * j] = 0
            if letter & 0b01000000 > 0:
                binary[8 * j + 1] = 1
            else:
                binary[8 * j + 1] = 0
            if letter & 0b00100000 > 0:
                binary[8 * j + 2] = 1
            else:
                binary[8 * j + 2] = 0
            if letter & 0b00010000 > 0:
                binary[8 * j + 3] = 1
            else:
                binary[8 * j + 3] = 0
            if letter & 0b00001000 > 0:
                binary[8 * j + 4] = 1
            else:
                binary[8 * j + 4] = 0
            if letter & 0b00000100 > 0:
                binary[8 * j + 5] = 1
            else:
                binary[8 * j + 5] = 0
            if letter & 0b00000010 > 0:
                binary[8 * j + 6] = 1
            else:
                binary[8 * j + 6] = 0
            if letter & 0b00000001 > 0:
                binary[8 * j + 7] = 1
            else:
                binary[8 * j + 7] = 0
        # print("Binary: ", binary)
        for j in range(height):
            for i in range(width):
                if j * width + i * 4 < sizeMsg * 8:
                    if binary[j * width + i * 4] == 0 and im1[j, i]["r"] % 2 == 1:
                        if im1[j, i]["r"] == 255:
                            im1[j, i]["r"] = im1[j, i]["r"] - 1
                        else:
                            im1[j, i]["r"] = im1[j, i]["r"] + 1
                    if binary[j * width + i * 4] == 1 and im1[j, i]["r"] % 2 == 0:
                        im1[j, i]["r"] = im1[j, i]["r"] + 1
                    if binary[j * width + i * 4 + 1] == 0 and im1[j, i]["g"] % 2 == 1:
                        if im1[j, i]["g"] == 255:
                            im1[j, i]["g"] = im1[j, i]["g"] - 1
                        else:
                            im1[j, i]["g"] = im1[j, i]["g"] + 1
                    if binary[j * width + i * 4 + 1] == 1 and im1[j, i]["g"] % 2 == 0:
                        im1[j, i]["g"] = im1[j, i]["g"] + 1
                    if binary[j * width + i * 4 + 2] == 0 and im1[j, i]["b"] % 2 == 1:
                        if im1[j, i]["b"] == 255:
                            im1[j, i]["b"] = im1[j, i]["b"] - 1
                        else:
                            im1[j, i]["b"] = im1[j, i]["b"] + 1
                    if binary[j * width + i * 4 + 2] == 1 and im1[j, i]["b"] % 2 == 0:
                        im1[j, i]["b"] = im1[j, i]["b"] + 1
                    if binary[j * width + i * 4 + 3] == 0 and im1[j, i]["a"] % 2 == 1:
                        if im1[j, i]["a"] == 255:
                            im1[j, i]["a"] = im1[j, i]["a"] - 1
                        else:
                            im1[j, i]["a"] = im1[j, i]["a"] + 1
                    if binary[j * width + i * 4 + 3] == 1 and im1[j, i]["a"] % 2 == 0:
                        im1[j, i]["a"] = im1[j, i]["a"] + 1

        # print("Pixel1 0x0: ", im1[0, 0])
        # print("Pixel1 0x1: ", im1[0, 1])
        self.imageList.append(self.image1)
        self.loadImage1()

    def showText(self):
        """67 show a secret message into an image
        """
        self.meth = 67
        self.displayCurrentFunction(self.meth)
        secretMsg = "Secret Message: \n"
        height = self.image1.height()
        width = self.image1.width()
        maxSize = height * width * 4
        binary = [0 for _ in range(maxSize)]  # space = 32
        im1 = q2a.recarray_view(self.image1)
        for j in range(height):
            for i in range(width):
                binary[j * width + i * 4] = im1[j, i]["r"] % 2
                binary[j * width + i * 4 + 1] = im1[j, i]["g"] % 2
                binary[j * width + i * 4 + 2] = im1[j, i]["b"] % 2
                binary[j * width + i * 4 + 3] = im1[j, i]["a"] % 2
        for i in range(0, maxSize, 8):
            code = 128 * binary[i] + 64 * binary[i + 1] + 32 * binary[i + 2] + 16 * binary[i + 3] + 8 * binary[
                i + 4] + 4 * binary[i + 5] + 2 * binary[i + 6] + binary[i + 7]
            if code == 92:  # Backslash code
                break
            char = chr(code)
            secretMsg = secretMsg + str(char)
        self.loadImage1()
        if self.tabWidget.currentIndex() != 2:
            self.tabWidget.setCurrentIndex(2)
        self.message.append(secretMsg)

    def asciiFile(self):
        """68 ASCII Art
        """
        ASCII_CHARS = ["@", "8", "0", "#", "S", "?", "%", "*", "+", "=", ";", ":", "-", ",", ".", " "]
        self.meth = 68
        self.displayCurrentFunction(self.meth)

        # Step 1: gray scale

        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        lum = 0.299 * im1["r"] + 0.587 * im1["g"] + 0.114 * im1["b"]  # luminance
        lum = lum.astype(np.uint8)
        imT["r"] = lum
        imT["g"] = lum
        imT["b"] = lum
        imT["a"] = im1["a"]

        # step 2: pixelation
        ratio = self.pp  # step 1 to 5
        print("Ratio: ", ratio)
        widthStep = ratio
        heightStep = 2 * ratio  # Characters are taller than wide
        listChar = []
        print("widthStep ", widthStep, "heightStep: ", heightStep)
        nbColumn = int(width / widthStep)
        nbLine = int(height / heightStep)
        print("Column Number: ", nbColumn, "Line Number: ", nbLine)
        for h in range(nbLine):
            for w in range(nbColumn):
                color = self.image1.pixelColor(w * widthStep, h * heightStep)
                index = int((color.red() * 16) / 256)
                # print(ASCII_CHARS[index])
                listChar.append(ASCII_CHARS[index])

        # Step 3: text ASCII building
        textImage = []  # List of lines
        for h in range(nbLine):
            line = ""
            for w in range(nbColumn):
                line = line + listChar[h * nbColumn + w]
            self.message.append(line)
            textImage.append(line)

        # Save text ASCII file
        for l in range(nbLine):
            print(textImage[l])
        self.saveAsciiArtImage(textImage)

        # End
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - " + str(heightStep * widthStep) + " pixel square")
        self.orderLabel.setText(self.orderLabel.text() + " - " + str(heightStep * widthStep) + " pixel square")

    def saveAsciiArtImage(self, textImage):
        """Saves the ASCII Art image"""
        name = QFileDialog.getSaveFileName(self, 'Save ASCII Art Image File', "", "Text files (*.txt *.doc")
        file = open(name[0], 'w')
        file.write("\n".join(textImage))
        file.close()

    def puzzle(self):
        """69 Puzzle
        """
        self.meth = 69
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        # self.imageBuffer = QImage(width, height, QImage.Format_ARGB32)
        step = 10
        # print("Step ", step)
        widthColumn = int(width / step)
        heightLine = int(height / step)
        self.imageBuffer = QImage(widthColumn * step, heightLine * step, QImage.Format.Format_ARGB32)
        # print(""Width Column: ", widthColumn)
        # print("Height Line: ", heightLine)

        listPieceImage = []

        for h in range(step):
            for w in range(step):
                pieceImage = QImage(widthColumn, heightLine, QImage.Format.Format_ARGB32)
                for j in range(heightLine):
                    for i in range(widthColumn):
                        color = self.image1.pixelColor(w * widthColumn + i, h * heightLine + j)
                        pieceImage.setPixelColor(i, j, color)
                listPieceImage.append(pieceImage)
        # print("Puzzle Piece Number: ", len(listPieceImage))
        # self.image1 = listPieceImage[0]

        # Random list
        newListPieceImage = random.sample(listPieceImage, len(listPieceImage))
        # newListPieceImage = random.choice(listPieceImage)
        # New image building
        for h in range(step):
            for w in range(step):
                # print("Index: ", h * step + w)
                for j in range(heightLine):
                    for i in range(widthColumn):
                        color = newListPieceImage[h * step + w].pixelColor(i, j)
                        self.imageBuffer.setPixelColor(w * widthColumn + i, h * heightLine + j, color)
        # self.image1 = listPieceImage[50]
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - " + str(step * step) + " pieces of puzzle")
        self.orderLabel.setText(self.orderLabel.text() + " - " + str(step * step) + " pieces of puzzle")

    def verticalSymmetry(self):
        """70 - Vertical symmetry"""
        self.meth = 70
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        for j in range(height):
            for i in range(width):
                color = self.image1.pixelColor(i, j)
                self.imageBuffer.setPixelColor(width - 1 - i, j, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def horizontalSymmetry(self):
        """71 - Horizontal symmetry"""
        self.meth = 71
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        for j in range(height):
            for i in range(width):
                color = self.image1.pixelColor(i, j)
                self.imageBuffer.setPixelColor(i, height - 1 - j, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def rotation90(self):
        """72 - Rotation 90° right
        """
        self.meth = 72
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(height, width, QImage.Format.Format_ARGB32)
        for j in range(height):
            for i in range(width):
                color = self.image1.pixelColor(i, j)
                self.imageBuffer.setPixelColor(height - 1 - j, i, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def rotation(self):
        """73 - Rotation
         Rotates image with theta angle
         Method ;
            1 - Translation to center the image
            2 - Rotation of A angle in radian
            3 - Translation to return the image to its initial position
         J = (j-Width/2)*cosA +(i-Height/2)*sinA + Width/2
         I = -(j-Width/2)*sinA + (i-Height/2)*cosA + Height/2
         Condition: J >= 0 and J < Height - 1 and I >= 0 and I < Width - 1
         """
        self.meth = 73
        self.displayCurrentFunction(self.meth)
        theta = self.aa * 0.9
        # print("theta: ", theta)
        thetaR = theta * np.pi / 180
        # print(""theta radian : ", thetaR)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        """
        *** With Pybind11 ***
        s = bytes(np.array(self.image1.constBits()).reshape(height * width * 4))
        im1 = np.frombuffer(s, dtype=np.uint8).reshape((height, width, 4))
        im1 = de.rotation_arrays(im1, thetaR).copy()
        ba = QByteArray(im1.tobytes())
        self.bytesToImage(ba, width, height, 4)

        *** With cython ***
        """
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        ci.rotate(im1, imT, thetaR)

        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - Theta: " + str(theta))
        self.orderLabel.setText(self.orderLabel.text() + " - Theta: " + str(theta))

    def diagonalise(self):
        """74 - Diagonalization"""
        # Diagonal Equation: y = (-(h-1)/(w-1))*x + (h-1)
        # Diagonal top right to bottom left
        self.meth = 74
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        for j in range(height):
            for i in range(width):
                color = self.image1.pixelColor(i, j)
                self.imageBuffer.setPixelColor(i, j, color)
        for j in range(height):
            for i in range(width):
                color = self.image1.pixelColor(i, j)
                if j < int(-((height - 1) / (width - 1)) * i + 0.5) + (height - 1):
                    self.imageBuffer.setPixelColor(width - i - 1, height - j - 1, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def medallion(self):
        """75 - Medallion
        """
        self.meth = 75
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        ratioX = self.aa / 100.0
        ratioY = self.bb / 100.0
        p = self.pp
        centerX = int(width / 2)
        centerY = int(height / 2)
        a = int(ratioX * centerX)
        b = int(ratioY * centerY)
        # 1 - Background
        if p == 1:  # White Background
            for j in range(height):
                for i in range(width):
                    color = QColor(255, 255, 255, 255)
                    self.imageBuffer.setPixelColor(i, j, color)
        if p == 2:  # Black Background
            for j in range(height):
                for i in range(width):
                    color = QColor(0, 0, 0, 255)
                    self.imageBuffer.setPixelColor(i, j, color)
        if p == 3:  # Red Background
            for j in range(height):
                for i in range(width):
                    color = QColor(255, 0, 0, 255)
                    self.imageBuffer.setPixelColor(i, j, color)
        if p == 4:  # Green Background
            for j in range(height):
                for i in range(width):
                    color = QColor(0, 255, 0, 255)
                    self.imageBuffer.setPixelColor(i, j, color)
        if p == 5:  # Blue Background
            for j in range(height):
                for i in range(width):
                    color = QColor(0, 0, 255, 255)
                    self.imageBuffer.setPixelColor(i, j, color)
        if p == 6:  # Transparency Background
            for j in range(height):
                for i in range(width):
                    color = self.image1.pixelColor(i, j)
                    red = color.red()
                    green = color.green()
                    blue = color.blue()
                    color = QColor(red, green, blue, 0)
                    self.imageBuffer.setPixelColor(i, j, color)
        if p == 7:  # Clouded Background
            for j in range(height):
                for i in range(width):
                    color = self.image1.pixelColor(i, j)
                    red = color.red()
                    green = color.green()
                    blue = color.blue()
                    color = QColor(red, green, blue, 128)
                    self.imageBuffer.setPixelColor(i, j, color)
        # 2 - Medallion center
        for j in range(-b, b, 1):
            for i in range(-a, a, 1):
                dx = i / a
                dy = j / b
                if dx * dx + dy * dy <= 1:
                    color = self.image1.pixelColor(i + centerX, j + centerY)
                    self.imageBuffer.setPixelColor(i + centerX, j + centerY, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def translation(self):
        """76 Translation"""
        self.meth = 76
        self.displayCurrentFunction(self.meth)
        self.image0 = self.image1
        maxX = 100
        maxY = 100
        height = self.image1.height()
        width = self.image1.width()
        dX = int(2 * width * self.aa / maxX - width)
        dY = int(2 * height * self.bb / maxY - height)
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        """
        *** With Bind11 ***
        s = bytes(np.array(self.image1.constBits()).reshape(height * width * 4))
        im1 = np.frombuffer(s, dtype=np.uint8).reshape((height, width, 4))
        im1 = de.translation_arrays(im1, dX, dY).copy()
        ba = QByteArray(im1.tobytes())
        self.bytesToImage(ba, width, height, 4)

        *** With Cython"""
        im1 = q2a.recarray_view(self.image1)
        imT = q2a.recarray_view(self.imageBuffer)
        ci.translate(im1, imT, dX, dY)

        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - dX: " + str(dX) + " - dY: " + str(dY))
        self.orderLabel.setText(self.orderLabel.text() + " - dX: " + str(dX) + " - dY: " + str(dY))

    def translationValidation(self):
        """Translation validation"""
        self.displayCurrentFunction(self.meth)
        maxX = 100
        maxY = 100
        height = self.image0.height()
        width = self.image0.width()
        dX = int(2 * width * self.aa / maxX - width)
        dY = int(2 * height * self.bb / maxY - height)
        # print("dX: ", dX)
        # print("dY: ", dY)
        im0 = q2a.recarray_view(self.image0)
        # print(""Pixel 10x10: ", im0[10, 10])
        # print("Height: ", im0.shape[0])
        # print("Width: ", im0.shape[1])
        if dY >= 0:
            height2 = height - dY
        else:
            height2 = height + dY
            dY = 0
        if dX >= 0:
            width2 = width - dX
        else:
            width2 = width + dX
            dX = 0
        # print("Height2: ", height2)
        # print("Width2: ", width2)
        self.imageBuffer = QImage(width2, height2, QImage.Format.Format_ARGB32)
        imT = q2a.recarray_view(self.imageBuffer)
        ci.translateOK(im0, imT, dX, dY)
        for j in range(height2):
            for i in range(width2):
                imT[j, i] = im0[j + dY, i + dX]
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - dX: " + str(dX) + " - dY: " + str(dY))
        self.orderLabel.setText(self.orderLabel.text() + " - dX: " + str(dX) + " - dY: " + str(dY))

    def zoomPlus(self):
        """ 77 - Zoom +"""
        self.meth = 77
        self.displayCurrentFunction(self.meth)
        self.image0 = self.image1
        z = 2  # facteur de zoom
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        height = int(height / z) * z
        width = int(width / z) * z
        for j in range(0, height, z):
            for i in range(0, width, z):
                for zj in range(z):
                    for zi in range(z):
                        color = self.image1.pixelColor(int(i / z), int(j / z))
                        self.imageBuffer.setPixelColor(i + zi, j + zj, color)
        self.image1 = self.imageBuffer
        # self.imageList.append(self.image1)
        self.loadImage1()

    def zoomPlusValidation(self):
        """Zoom + validation"""
        self.displayCurrentFunction(self.meth)
        z = 2  # facteur de zoom
        height = self.image0.height()
        width = self.image0.width()
        height = int(height / z) * z
        width = int(width / z) * z
        height2 = 2 * height
        width2 = 2 * width
        self.imageBuffer = QImage(width2, height2, QImage.Format.Format_ARGB32)
        for j in range(0, height2, z):
            for i in range(0, width2, z):
                for zj in range(z):
                    for zi in range(z):
                        color = self.image0.pixelColor(int(i / z), int(j / z))
                        self.imageBuffer.setPixelColor(i + zi, j + zj, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def zoomBilinearPlus(self):
        """78 - Bilinear zoom + """
        self.meth = 78
        self.displayCurrentFunction(self.meth)
        self.image0 = self.image1
        z = 2  # facteur de zoom
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        height = int(height / z) * z
        width = int(width / z) * z
        for j in range(0, height, z):
            for i in range(0, width, z):
                color1 = self.image1.pixelColor(int(i / z), int(j / z))
                red1 = color1.red()
                green1 = color1.green()
                blue1 = color1.blue()
                alpha = color1.alpha()
                color2 = self.image1.pixelColor(int(i / z), int(j / z + 1))
                red2 = color2.red()
                green2 = color2.green()
                blue2 = color2.blue()
                color3 = self.image1.pixelColor(int(i / z + 1), int(j / z))
                red3 = color3.red()
                green3 = color3.green()
                blue3 = color3.blue()
                color4 = self.image1.pixelColor(int(i / z + 1), int(j / z + 1))
                red4 = color4.red()
                green4 = color4.green()
                blue4 = color4.blue()

                color5 = QColor(int((red1 + red2) / 2), int((green1 + green2) / 2), int((blue1 + blue2) / 2), alpha)
                color6 = QColor(int((red1 + red3) / 2), int((green1 + green3) / 2), int((blue1 + blue3) / 2), alpha)
                color7 = QColor(int((red1 + red2 + red3 + red4) / 4), int((green1 + green2 + green3 + green4) / 4),
                                int((blue1 + blue2 + blue3 + blue4) / 4), alpha)

                self.imageBuffer.setPixelColor(i, j, color1)
                self.imageBuffer.setPixelColor(i, j + 1, color5)
                self.imageBuffer.setPixelColor(i + 1, j, color6)
                self.imageBuffer.setPixelColor(i + 1, j + 1, color7)
        self.image1 = self.imageBuffer
        # self.imageList.append(self.image1)
        self.loadImage1()

    def zoomBilinearPlusValidation(self):
        """Bilinear zoom + Validation"""
        self.displayCurrentFunction(self.meth)
        z = 2  # facteur de zoom
        height = self.image0.height()
        width = self.image0.width()
        height = int(height / z) * z
        width = int(width / z) * z
        height2 = 2 * height
        width2 = 2 * width
        self.imageBuffer = QImage(width2, height2, QImage.Format.Format_ARGB32)
        for j in range(0, height2, z):
            for i in range(0, width2, z):
                color1 = self.image0.pixelColor(int(i / z), int(j / z))
                red1 = color1.red()
                green1 = color1.green()
                blue1 = color1.blue()
                alpha = color1.alpha()
                color2 = self.image0.pixelColor(int(i / z), int(j / z + 1))
                red2 = color2.red()
                green2 = color2.green()
                blue2 = color2.blue()
                color3 = self.image0.pixelColor(int(i / z + 1), int(j / z))
                red3 = color3.red()
                green3 = color3.green()
                blue3 = color3.blue()
                color4 = self.image0.pixelColor(int(i / z + 1), int(j / z + 1))
                red4 = color4.red()
                green4 = color4.green()
                blue4 = color4.blue()

                color5 = QColor(int((red1 + red2) / 2), int((green1 + green2) / 2), int((blue1 + blue2) / 2), alpha)
                color6 = QColor(int((red1 + red3) / 2), int((green1 + green3) / 2), int((blue1 + blue3) / 2), alpha)
                color7 = QColor(int((red1 + red2 + red3 + red4) / 4), int((green1 + green2 + green3 + green4) / 4),
                                int((blue1 + blue2 + blue3 + blue4) / 4), alpha)

                self.imageBuffer.setPixelColor(i, j, color1)
                self.imageBuffer.setPixelColor(i, j + 1, color5)
                self.imageBuffer.setPixelColor(i + 1, j, color6)
                self.imageBuffer.setPixelColor(i + 1, j + 1, color7)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def zoomLess(self):
        """ 79 - Zoom -"""
        self.meth = 79
        self.displayCurrentFunction(self.meth)
        self.image0 = self.image1
        z = 2  # facteur de zoom
        height = self.image0.height()
        width = self.image0.width()
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        height = int(height / z) * z
        width = int(width / z) * z
        for j in range(height):
            for i in range(width):
                if i * z < width and j * z < height:
                    color = self.image1.pixelColor(i * z, j * z)
                    self.imageBuffer.setPixelColor(i, j, color)
                else:
                    color = QColor(255, 255, 255, 255)
                    self.imageBuffer.setPixelColor(i, j, color)
        self.image1 = self.imageBuffer
        # self.imageList.append(self.image1)
        self.loadImage1()

    def zoomLessValidation(self):
        """Zoom less validation"""
        self.displayCurrentFunction(self.meth)
        z = 2  # facteur de zoom
        height = self.image1.height()
        width = self.image1.width()
        height = int(height / z) * z
        width = int(width / z) * z
        height2 = int(height / 2)
        width2 = int(width / 2)
        self.imageBuffer = QImage(width2, height2, QImage.Format.Format_ARGB32)
        for j in range(height2):
            for i in range(width2):
                color = self.image0.pixelColor(i * z, j * z)
                self.imageBuffer.setPixelColor(i, j, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def crop(self):
        """80 Crops this image"""
        self.meth = 80
        self.displayCurrentFunction(self.meth)
        self.image0 = self.image1
        height = self.image0.height()
        width = self.image0.width()
        posY1 = int(self.aa * height / 100)
        posY2 = int(height - self.dd * height / 100)
        posX1 = int(self.bb * width / 100)
        posX2 = int(width - self.ee * width / 100)
        # print("posX1: ", posX1)
        # print("posX2: ", posX2)
        # print("posY1: ", posY1)
        # print("posY2: ", posY2)
        im1 = q2a.recarray_view(self.image1)
        # print(""Pixel 10x10: ", im1[10, 10])
        # print("Height: ", im1.shape[0])
        # print("Width: ", im1.shape[1])
        self.imageBuffer = QImage(width, height, QImage.Format.Format_ARGB32)
        imT = q2a.recarray_view(self.imageBuffer)
        # ci.crop(im1, imT, posX1, posX2, posY1, posY2)

        imT["r"] = 0.5 * im1["r"]
        imT["g"] = 0.5 * im1["g"]
        imT["b"] = 0.5 * im1["b"]
        imT["a"] = im1["a"]
        imT["r"][posY1:posY2, posX1:posX2] = im1["r"][posY1:posY2, posX1:posX2]
        imT["g"][posY1:posY2, posX1:posX2] = im1["g"][posY1:posY2, posX1:posX2]
        imT["b"][posY1:posY2, posX1:posX2] = im1["b"][posY1:posY2, posX1:posX2]
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - posX1: " + str(posX1) + " - posX2: " + str(posX2) +
                            " - posY1: " + str(posY1) + " - posY2: " + str(posY2))
        self.orderLabel.setText(self.orderLabel.text() + " - posX1: " + str(posX1) + " - posX2: " + str(posX2) +
                                " - posY1: " + str(posY1) + " - posY2: " + str(posY2))

    def cropValidation(self):
        """Crop validation"""
        self.displayCurrentFunction(self.meth)
        height = self.image0.height()
        width = self.image0.width()
        posY1 = int(self.aa * height / 100)
        posY2 = int(height - self.dd * height / 100)
        posX1 = int(self.bb * width / 100)
        posX2 = int(width - self.ee * width / 100)
        # print("posX1: ", posX1)
        # print("posX2: ", posX2)
        # print("posY1: ", posY1)
        # print("posY2: ", posY2)
        im0 = q2a.recarray_view(self.image0)
        # print(""Pixel 10x10: ", im0[10, 10])
        # print("Height: ", im0.shape[0])
        # print("Width: ", im0.shape[1])
        height2 = posY2 - posY1
        width2 = posX2 - posX1
        self.imageBuffer = QImage(width2, height2, QImage.Format.Format_ARGB32)
        imT = q2a.recarray_view(self.imageBuffer)
        # ci.crop(im0, imT, posX1, posX2, posY1, posY2)

        imT["r"][0:height2, 0:width2] = im0["r"][posY1:posY2, posX1:posX2]
        imT["g"][0:height2, 0:width2] = im0["g"][posY1:posY2, posX1:posX2]
        imT["b"][0:height2, 0:width2] = im0["b"][posY1:posY2, posX1:posX2]
        imT["a"][0:height2, 0:width2] = im0["a"][posY1:posY2, posX1:posX2]
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()
        self.message.append(" - Height: " + str(height2) + " - Width: " + str(width2))
        self.orderLabel.setText(self.orderLabel.text() + " - Height: " + str(height2) + " - Width: " + str(width2))

    def depth4to1(self):
        """
        Transform 4 bytes image to one byte image
        """
        self.meth = 90
        self.displayCurrentFunction(self.meth)
        depth = self.image1.depth() / 8
        # print("Depth: ", depth)
        if depth == 4:
            flags = Qt.ImageConversionFlag.AutoColor
            self.imageBuffer = self.image1.convertToFormat(QImage.Format.Format_Grayscale8, flags)
            self.image1 = self.imageBuffer
            self.imageList.append(self.image1)
            self.loadImage1()

    def depth1to4(self):
        """
        Transform one byte image to 4 bytes image
        """
        self.meth = 91
        self.displayCurrentFunction(self.meth)
        depth = self.image1.depth() / 8
        # print("Depth: ", depth)
        if depth == 1:
            flags = Qt.ImageConversionFlag.AutoColor
            self.imageBuffer = self.image1.convertToFormat(QImage.Format.Format_ARGB32, flags)
            self.image1 = self.imageBuffer
            self.imageList.append(self.image1)
            self.loadImage1()

    def pattern(self):
        """Creates a test pattern for the development of methods
         - Color test pattern 16x12 on 4 bytes"""
        self.isPattern = True
        self.meth = 92
        self.displayCurrentFunction(self.meth)
        # New image creating
        # depth = 4
        # print("Depth: ", depth)
        height = 16
        width = 24
        self.image1 = QImage(width, height, QImage.Format.Format_ARGB32)
        self.labelMessage.setText(
            QtGui.QGuiApplication.translate("Image", "Message: Loaded Color Pattern Image", None))
        # Matrix image creating
        value2 = QtGui.qRgba(255, 0, 0, 255)
        value3 = QtGui.qRgba(0, 255, 0, 255)
        value4 = QtGui.qRgba(255, 255, 0, 255)
        value5 = QtGui.qRgba(0, 0, 255, 255)
        value6 = QtGui.qRgba(255, 0, 255, 255)
        value7 = QtGui.qRgba(0, 255, 255, 255)
        for j in range(16):
            self.image1.setPixel(0, j, value2)
            self.image1.setPixel(1, j, value2)
            self.image1.setPixel(2, j, value2)
            self.image1.setPixel(3, j, value2)
        for j in range(16):
            self.image1.setPixel(4, j, value3)
            self.image1.setPixel(5, j, value3)
            self.image1.setPixel(6, j, value3)
            self.image1.setPixel(7, j, value3)
        for j in range(16):
            self.image1.setPixel(8, j, value4)
            self.image1.setPixel(9, j, value4)
            self.image1.setPixel(10, j, value4)
            self.image1.setPixel(11, j, value4)
        for j in range(16):
            self.image1.setPixel(12, j, value5)
            self.image1.setPixel(13, j, value5)
            self.image1.setPixel(14, j, value5)
            self.image1.setPixel(15, j, value5)
        for j in range(16):
            self.image1.setPixel(16, j, value6)
            self.image1.setPixel(17, j, value6)
            self.image1.setPixel(18, j, value6)
            self.image1.setPixel(19, j, value6)
        for j in range(16):
            self.image1.setPixel(20, j, value7)
            self.image1.setPixel(21, j, value7)
            self.image1.setPixel(22, j, value7)
            self.image1.setPixel(23, j, value7)
        if len(self.imageList) != 0:
            self.imageList.clear()
        self.imageList.append(self.image1)
        self.loadImage1()
        # self.displayNewScreen2(self.meth, "")

    def patternNB(self):
        """93 - Creates a test pattern for the development of methods
         - Black and White test pattern 16x12 on 1 byte (4/3 format)"""
        self.isPatternNB = True
        self.meth = 93
        self.displayCurrentFunction(self.meth)
        # New image creating
        height = 16
        width = 12
        self.image1 = QImage(width, height, QImage.Format.Format_Indexed8)
        self.labelMessage.setText(QtGui.QGuiApplication.translate("Image",
                                                                  "Message: Loaded Black and White Pattern Image",
                                                                  None))
        val = [0, 36, 73, 109, 146, 182, 255, 255]
        for k in range(8):
            value = QtGui.qRgb(val[k], val[k], val[k])
            self.image1.setColor(k, value)
        for j in range(height):
            self.image1.setPixel(0, j, 0)
            self.image1.setPixel(1, j, 0)
            self.image1.setPixel(2, j, 1)
            self.image1.setPixel(3, j, 1)
            self.image1.setPixel(4, j, 2)
            self.image1.setPixel(5, j, 2)
            self.image1.setPixel(6, j, 3)
            self.image1.setPixel(7, j, 3)
            self.image1.setPixel(8, j, 4)
            self.image1.setPixel(9, j, 4)
            self.image1.setPixel(10, j, 5)
            self.image1.setPixel(11, j, 5)
        if len(self.imageList) != 0:
            self.imageList.clear()
        self.imageList.append(self.image1)
        self.loadImage1()
        # self.displayNewScreen2(self.meth, "")

    def displayImageCode(self):
        """ 94 - Shows the code from image 1"""
        self.meth = 94
        self.displayCurrentFunction(self.meth)
        if self.tabWidget.currentIndex() != 2:
            self.tabWidget.setCurrentIndex(2)
        height = self.image1.height()
        width = self.image1.width()
        depth = int(self.image1.depth() / 8)
        # print("height: ", height)
        # print("width: ", width)
        # print("depth: ", depth)
        if height > 24 or width > 24:
            self.message2()
            return
        myText = QtGui.QGuiApplication.translate("Image", "DISPLAY:\n", None)
        self.message.append(myText)
        myList = []
        myText = QtGui.QGuiApplication.translate("Image", "Image Tab:  <br />", None)
        myList.append(myText)
        if depth == 4:
            for col in range(height):
                data = ""
                for row in range(width):
                    color = self.image1.pixelColor(row, col)
                    green = color.green()
                    blue = color.blue()
                    red = color.red()
                    alpha = color.alpha()
                    data += hex(red) + " " + hex(green) + " " + hex(blue) + " " + hex(alpha) + " -"
                data = data.replace('0x', '')
                myList.append(data)
                myList.append("<br />")
            myText = "<p style=\"font-size:5pt;\">" + " ".join(myList) + "</p>"
        elif depth == 1:
            for col in range(height):
                data = ""
                for row in range(width):
                    color = self.image1.pixelColor(row, col)
                    gray = color.green()
                    data += hex(gray) + " -"
                data = data.replace('0x', '')
                myList.append(data)
                myList.append("<br />")
            myText = "<p style=\"font-size:7pt;\">" + " ".join(myList) + "</p>"
        else:
            self.message2()
            return
        self.message.append(myText)

    def displayHistogram(self):
        """95 - display Histogram
        Shows the histogram of image 1"""
        self.meth = 95
        self.displayCurrentFunction(self.meth)
        if self.tabWidget.currentIndex() != 3:
            self.tabWidget.setCurrentIndex(3)
            # Array creating
        im = q2a.recarray_view(self.image1)
        # Array of colors
        red = im["r"]
        green = im["g"]
        blue = im["b"]
        histo = np.zeros(256, int)  # 256 zeros vector
        if self.radioButtonRed.isChecked():
            color = "Red"
            # print("Color: ", color)
            for i in range(0, im.shape[0]):  # lines
                for j in range(0, im.shape[1]):  # rows
                    histo[red[i, j]] = histo[red[i, j]] + 1
        elif self.radioButtonGreen.isChecked():
            color = "Green"
            # print("Color: ", color)
            for i in range(0, im.shape[0]):
                for j in range(0, im.shape[1]):
                    histo[green[i, j]] = histo[green[i, j]] + 1
        elif self.radioButtonBlue.isChecked():
            color = "Blue"
            # print("Color: ", color)
            for i in range(0, im.shape[0]):
                for j in range(0, im.shape[1]):
                    histo[blue[i, j]] = histo[blue[i, j]] + 1
        else:
            color = "Luminance"
            # print("Color: ", color)
            # luminance
            lum = 0.299 * red + 0.587 * green + 0.114 * blue
            # Converts floats to bytes
            lum = lum.astype(np.uint8)
            # histogram creating
            for i in range(0, im.shape[0]):
                for j in range(0, im.shape[1]):
                    histo[lum[i, j]] = histo[lum[i, j]] + 1
        # Display values
        self.message.append(QtGui.QGuiApplication.translate("Image", "Histogram:\n", None))
        self.message.append(color)
        self.message.append(str(histo))

        # clearing old figure
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # plot data
        ax.plot(histo)
        ax.set_ylabel('number')
        ax.set_xlabel('pixel value')
        ax.set_title(color + ' histogram')

        # refresh canvas
        self.canvas.draw()
        self.histogramLayout.addWidget(self.canvas)

    def testFunction1(self):
        """105 - Pattern
        Creates a test pattern for the development of methods
         - Color test pattern 16x12 on 4 bytes"""
        self.isPattern = True
        self.meth = 105
        self.displayCurrentFunction(self.meth)

    def testFunction2(self):
        """106- Test QImage format to numpy ndarray and numpy ndarray to QImage format
        """
        self.meth = 106
        self.displayCurrentFunction(self.meth)

    def testFunction3(self):
        """107- Test
        Rotation  90° Left
        """
        self.meth = 107
        self.displayCurrentFunction(self.meth)
        height = self.image1.height()
        width = self.image1.width()
        self.imageBuffer = QImage(height, width, QImage.Format.Format_ARGB32)
        for k in range(height):
            for h in range(width):
                color = self.image1.pixelColor(h, k)
                self.imageBuffer.setPixelColor(k, width - 1 - h, color)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def testFunction4(self):
        """108- Test
        To Do
        """
        self.meth = 108
        self.displayCurrentFunction(self.meth)
        self.rotation90()
        self.verticalStroke()
        self.testFunction3()
        # self.rotation90()
        # self.rotation90()
        # self.rotation90()

    def cancel(self):
        """ 99 - Cancel
         The last action is cancelled
        """
        self.meth = 99
        self.displayCurrentFunction(self.meth)
        nbImage = len(self.imageList)
        if nbImage > 1:
            self.image1 = self.imageList[nbImage - 2]
            self.imageList.pop()
        self.loadImage1()

    def mono(self):
        """
        Transform RGBA image to Mono
        """
        self.meth = 100
        self.displayCurrentFunction(self.meth)
        depth = self.image1.depth() / 8
        # print("Depth: ", depth)
        if depth == 4:
            flags = Qt.ImageConversionFlag.AutoColor
            self.imageBuffer = self.image1.convertToFormat(QImage.Format.Format_Mono, flags)
            self.image1 = self.imageBuffer
            self.imageList.append(self.image1)
            self.loadImage1()

    def indexed8(self):
        """
        Transform RGBA image to indexed8
        """
        self.meth = 101
        self.displayCurrentFunction(self.meth)
        depth = self.image1.depth() / 8
        # print("Depth: ", depth)
        if depth == 4:
            flags = Qt.ImageConversionFlag.AutoColor
            self.imageBuffer = self.image1.convertToFormat(QImage.Format.Format_Indexed8, flags)
            self.image1 = self.imageBuffer
            self.imageList.append(self.image1)
            self.loadImage1()

    def aRGB32(self):
        """
        Transform to ARGB32

        """
        self.meth = 102
        self.displayCurrentFunction(self.meth)
        depth = self.image1.depth() / 8
        # print("Depth: ", depth)
        if depth == 1 or depth == 0.125:
            flags = Qt.ImageConversionFlag.AutoColor
            self.imageBuffer = self.image1.convertToFormat(QImage.Format.Format_ARGB32, flags)
            self.image1 = self.imageBuffer
            self.imageList.append(self.image1)
            self.loadImage1()

    def grayscale8(self):
        """
        Transform RGBA image to grayscale8

        """
        self.meth = 103
        self.displayCurrentFunction(self.meth)
        depth = self.image1.depth() / 8
        # print("Depth: ", depth)
        if depth == 4:
            flags = Qt.ImageConversionFlag.AutoColor
            self.imageBuffer = self.image1.convertToFormat(QImage.Format.Format_Grayscale8, flags)
            self.image1 = self.imageBuffer
            self.imageList.append(self.image1)
            self.loadImage1()

    def reduceSizeImage(self):
        """Reduce the size of image"""
        self.meth = 104
        self.displayCurrentFunction(self.meth)
        width = 700
        height = 525
        size = QSize(width, height)
        self.imageBuffer = self.image1.scaled(size, Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
        self.image1 = self.imageBuffer
        self.imageList.append(self.image1)
        self.loadImage1()

    def createFilter(self):
        """Creates a filter 3x3"""
        self.filter[0][0] = self.spinBoxF00.value()
        self.filter[0][1] = self.spinBoxF01.value()
        self.filter[0][2] = self.spinBoxF02.value()
        self.filter[1][0] = self.spinBoxF10.value()
        self.filter[1][1] = self.spinBoxF11.value()
        self.filter[1][2] = self.spinBoxF12.value()
        self.filter[2][0] = self.spinBoxF20.value()
        self.filter[2][1] = self.spinBoxF21.value()
        self.filter[2][2] = self.spinBoxF22.value()

    def createConnections(self):

        # 000 Menu
        self.openAct.triggered.connect(self.openImage)
        self.saveAct.triggered.connect(self.saveImage)
        self.printAct.triggered.connect(self.printImage)
        self.openImg2Act.triggered.connect(self.openImage2)
        self.copy1Act.triggered.connect(self.copy1to2)
        self.copy2Act.triggered.connect(self.copy2to1)
        self.swapAct.triggered.connect(self.swap1and2)
        # self.displayAct.clicked.connect(self.displayImageCode)
        self.closeAct.triggered.connect(self.close)
        self.adjustmentAct.triggered.connect(self.adjustment)
        self.aboutAct.triggered.connect(self.about)
        self.operatingModeAct.triggered.connect(lambda: self.operatingMode(4))
        self.frenchAct.triggered.connect(lambda: languageSelected(1))
        self.englishAct.triggered.connect(lambda: languageSelected(0))

        # 100 Mains controls
        self.pushButtonReset.clicked.connect(self.initialize)
        self.pushButtonUndo.clicked.connect(self.cancel)

        # 200 Geometric transformations
        self.pushButtonVerticalSymmetry.clicked.connect(self.verticalSymmetry)
        self.pushButtonHorizontalSymmetry.clicked.connect(self.horizontalSymmetry)
        self.pushButtonRotation90.clicked.connect(self.rotation90)
        self.pushButtonRotation.clicked.connect(self.rotation)
        self.pushButtonDiagonalization.clicked.connect(self.diagonalise)
        self.pushButtonMedallion.clicked.connect(self.medallion)

        # 200 Geometric transformations with validation
        self.pushButtonTranslation.clicked.connect(self.translation)
        self.pushButtonZoomPlus.clicked.connect(self.zoomPlus)
        self.pushButtonZoomPlusBilinear.clicked.connect(self.zoomBilinearPlus)
        self.pushButtonZoomLess.clicked.connect(self.zoomLess)
        self.pushButtonCrop.clicked.connect(self.crop)
        self.pushButtonValidation.clicked.connect(self.validation)

        # 300 Improvement of images and filters functions
        self.pushButtonBrightness.clicked.connect(self.brightness)
        self.pushButtonContrast.clicked.connect(self.contrast)
        self.pushButtonRGB.clicked.connect(self.rgb)
        self.pushButtonLuminance.clicked.connect(self.luminance)
        self.pushButtonRedEffect.clicked.connect(self.redEffect)
        self.pushButtonGaussianFilter.clicked.connect(self.gaussianFilter)
        self.pushButtonWindowing.clicked.connect(self.windowingFilter)
        self.pushButtonThresholding.clicked.connect(self.thresholdFilter)
        self.pushButtonBinarization.clicked.connect(self.binarizationFilter)
        self.pushButtonIntegratingFilter.clicked.connect(self.averagingFilter)
        self.pushButtonMedianFilter.clicked.connect(self.medianFilter)
        self.pushButtonNegative.clicked.connect(self.negativeFilter)
        self.pushButtonHorizontalGradient.clicked.connect(self.hrgradient)
        self.pushButtonVerticalGradient.clicked.connect(self.vtgradient)
        self.pushButtonBorderDetect.clicked.connect(self.borderDetect)
        self.pushButtonErosion.clicked.connect(self.erosion)
        self.pushButtonDilation.clicked.connect(self.dilatation)
        self.pushButtonGamma.clicked.connect(self.gammaFilter)
        self.pushButtonPoint.clicked.connect(self.pointer)
        self.pushButtonVerticalStroke.clicked.connect(self.verticalStroke)
        self.pushButtonHorizontalStroke.clicked.connect(self.horizontalStroke)
        self.pushButtonRedFilter.clicked.connect(self.red)
        self.pushButtonGreenFilter.clicked.connect(self.green)
        self.pushButtonBlueFilter.clicked.connect(self.blue)
        self.pushButtonTransparency.clicked.connect(self.transparency)
        self.pushButtonSepia.clicked.connect(self.sepiaFilter)
        self.pushButtonGreyLevel.clicked.connect(self.grayTint)
        self.pushButtonColorLevel.clicked.connect(self.colorize)
        self.pushButtonFalseColors.clicked.connect(self.swapColor)

        # 400 Image overlay functions
        self.pushButtonRedBackground.clicked.connect(self.redBackground)
        self.pushButtonGreenBackground.clicked.connect(self.greenBackground)
        self.pushButtonBlueBackground.clicked.connect(self.blueBackground)
        self.pushButtonWhiteBackground.clicked.connect(self.whiteBackground)
        self.pushButtonBlackBackground.clicked.connect(self.blackBackground)
        self.pushButtonTintBackground.clicked.connect(self.backgroundHue)
        self.pushButtonGreenScreen.clicked.connect(self.greenScreen)
        self.pushButtonAnaglyph.clicked.connect(self.anaglyph)
        self.pushButtonOverlay1on2.clicked.connect(self.superimpose1on2)

        # 500 Noise simulation functions
        self.pushButtonPepperAndSaltNoise.clicked.connect(self.noisePepperMaker)
        self.pushButtonGaussianNoise.clicked.connect(self.noiseGaussianMaker)
        self.pushButtonWhiteNoise.clicked.connect(self.noiseWhiteMaker)

        # 600 Encryption functions
        self.pushButtonPixellation.clicked.connect(self.pixelate)
        self.pushButtonEncryption.clicked.connect(self.encryption)
        self.pushButtonFixedEncryption.clicked.connect(self.fixedEncryption)
        self.pushButtonDecryption.clicked.connect(self.decryption)
        self.pushButtonHideSecret.clicked.connect(self.hideSecret)
        self.pushButtonShowSecret.clicked.connect(self.showSecret)
        self.pushButtonSteganography.clicked.connect(self.hideText)
        self.pushButtonShowText.clicked.connect(self.showText)
        self.pushButtonAsciiFile.clicked.connect(self.asciiFile)
        self.pushButtonPuzzle.clicked.connect(self.puzzle)

        # 700 Development and testing functions
        self.pushButtonDepth4to1.clicked.connect(self.depth4to1)
        self.pushButtonDepth1to4.clicked.connect(self.depth1to4)
        self.pushButtonTVPattern.clicked.connect(self.pattern)
        self.pushButtonBWTVPattern.clicked.connect(self.patternNB)
        self.pushButtonHistogram.clicked.connect(self.displayHistogram)
        self.pushButtonTest1.clicked.connect(self.testFunction1)
        self.pushButtonTest2.clicked.connect(self.testFunction2)
        self.pushButtonTest3.clicked.connect(self.testFunction3)
        self.pushButtonTest4.clicked.connect(self.testFunction4)

        # 800 Filter functions (convolution)
        self.pushButtonCreateFilter.clicked.connect(self.createFilter)
        self.pushButtonConvolution.clicked.connect(self.convolutionFilter)

        # 900 Development and testing functions
        self.pushButtonMono.clicked.connect(self.mono)
        self.pushButtonIndexed8.clicked.connect(self.indexed8)
        self.pushButtonARGB32.clicked.connect(self.aRGB32)
        self.pushButtonGrayscale8.clicked.connect(self.grayscale8)
        self.pushButtonReduceSize.clicked.connect(self.reduceSizeImage)

        # Display Sliders
        self.sliderA.valueChanged.connect(self.updateA)
        self.sliderB.valueChanged.connect(self.updateB)
        self.sliderC.valueChanged.connect(self.updateC)
        self.sliderD.valueChanged.connect(self.updateD)
        self.sliderE.valueChanged.connect(self.updateE)
        self.sliderF.valueChanged.connect(self.updateF)

        # Display SpinBoxs
        self.spinBoxPoint.valueChanged.connect(lambda: self.updatePoint(int(self.spinBoxPoint.value())))
        self.spinBoxSeed.valueChanged.connect(self.updateSeed)
        self.spinBoxFilter.valueChanged.connect(self.updateFilter)

        # Display RadioButtons
        self.radioButtonLuminance.pressed.connect(self.displayHistogram)
        self.radioButtonRed.pressed.connect(self.displayHistogram)
        self.radioButtonGreen.pressed.connect(self.displayHistogram)
        self.radioButtonBlue.pressed.connect(self.displayHistogram)

    def validation(self):
        """Validation """
        match self.meth:
            case 76:
                self.translationValidation()
                print("Translation validated")
            case 77:
                self.zoomPlusValidation()
                print("zoom + validated")
            case 78:
                self.zoomBilinearPlusValidation()
                print("Bilinear Zoom + validated")
            case 79:
                self.zoomLessValidation()
                print("Zoom - validated")
            case 80:
                self.cropValidation()
                print("Crop validated")
            case _:
                print("No validation function")

    def viewParameterA(self, textLabelA):
        """Show A parameter"""
        self.sliderA.setVisible(True)
        self.labelA.setVisible(True)
        self.labelA.setText(textLabelA)
        self.LcdA.setVisible(True)

    def viewParameterB(self, textLabelB):
        """Show B parameter"""
        self.sliderB.setVisible(True)
        self.labelB.setVisible(True)
        self.labelB.setText(textLabelB)
        self.LcdB.setVisible(True)

    def viewParameterC(self, textLabelC):
        """Show C parameter"""
        self.sliderC.setVisible(True)
        self.labelC.setVisible(True)
        self.labelC.setText(textLabelC)
        self.LcdC.setVisible(True)

    def viewParameterD(self, textLabelD):
        """Show D parameter"""
        self.sliderD.setVisible(True)
        self.labelD.setVisible(True)
        self.labelD.setText(textLabelD)
        self.LcdD.setVisible(True)

    def viewParameterE(self, textLabelE):
        """Show E parameter"""
        self.sliderE.setVisible(True)
        self.labelE.setVisible(True)
        self.labelE.setText(textLabelE)
        self.lcdE.setVisible(True)

    def viewParameterF(self, textLabelF):
        """Show F parameter"""
        self.sliderF.setVisible(True)
        self.labelF.setVisible(True)
        self.labelF.setText(textLabelF)
        self.lcdF.setVisible(True)

    def viewParameterPoint(self, textLabelP):
        """Show P parameter"""
        self.labelPointsNumber.setVisible(True)
        self.labelPointsNumber.setText(textLabelP)
        self.spinBoxPoint.setVisible(True)

    def viewParameterSeed(self, textLabelP):
        """Show seed parameter"""
        self.labelSeed.setVisible(True)
        self.labelSeed.setText(textLabelP)
        self.spinBoxSeed.setVisible(True)

    def hideParameter(self):
        """Hide all parameters"""
        self.sliderA.setVisible(False)
        self.labelA.setVisible(False)
        self.LcdA.setVisible(False)
        self.sliderB.setVisible(False)
        self.labelB.setVisible(False)
        self.LcdB.setVisible(False)
        self.sliderC.setVisible(False)
        self.labelC.setVisible(False)
        self.LcdC.setVisible(False)
        self.sliderD.setVisible(False)
        self.labelD.setVisible(False)
        self.LcdD.setVisible(False)
        self.sliderE.setVisible(False)
        self.labelE.setVisible(False)
        self.lcdE.setVisible(False)
        self.sliderF.setVisible(False)
        self.labelF.setVisible(False)
        self.lcdF.setVisible(False)

    #        self.labelPoint.setVisible(False)
    #        self.spinBoxPoint.setVisible(False)
    #        self.labelSeed.setVisible(False)
    #        self.spinBoxSeed.setVisible(False)

    # Update parameters
    def updateA(self, A):
        """Update A parameter"""
        self.aa = A
        if self.meth == 14:
            self.cancel()
            if self.sliderA.value() > self.sliderB.value():
                QMessageBox.information(self, QtGui.QGuiApplication.translate("Image", "Main Window ", None),
                                        QtGui.QGuiApplication.translate(
                                            "Image", "A value must be inferior B value", None))
                return
            self.windowingFilter()
        if self.meth == 8:
            self.cancel()
            self.binarizationFilter()
        if self.meth == 10:
            self.cancel()
            self.cancel()
            self.transparency()
        if self.meth == 50:
            self.cancel()
            self.noiseWhiteMaker()
        if self.meth == 51:
            self.cancel()
            self.noisePepperMaker()
        if self.meth == 52:
            self.cancel()
            self.noiseGaussianMaker()
        if self.meth == 76:
            self.cancel()
            self.translation()
        if self.meth == 73:
            self.cancel()
            self.rotation()
        if self.meth == 75:
            self.cancel()
            self.medallion()
        if self.meth == 80:
            self.cancel()
            self.crop()

    def updateB(self, B):
        """Update B parameter"""
        self.bb = B
        if self.meth == 14:
            self.cancel()
            self.windowingFilter()
        if self.meth == 75:
            self.cancel()
            self.medallion()
        if self.meth == 76:
            self.cancel()
            self.translation()
        if self.meth == 80:
            self.cancel()
            self.crop()

    def updateC(self, C):
        """Update C parameter"""
        self.cc = C
        if self.meth == 61:
            self.cancel()
            self.encryption()
        if self.meth == 28:
            self.cancel()
            self.gammaFilter()

    def updateD(self, D):
        """Update D parameter"""
        self.dd = D
        if self.meth == 60:
            self.cancel()
            self.pixelate()
        if self.meth == 5:
            self.cancel()
            self.rgb()
        if self.meth == 6:
            self.cancel()
            self.redEffect()
        if self.meth == 7:
            self.cancel()
            self.thresholdFilter()
        if self.meth == 45:
            self.cancel()
            self.backgroundHue()
        if self.meth == 80:
            self.cancel()
            self.crop()

    def updateE(self, E):
        """Update E parameter"""
        self.ee = E
        if self.meth == 1:
            self.cancel()
            self.brightness()
        if self.meth == 5:
            self.cancel()
            self.rgb()
        if self.meth == 6:
            self.cancel()
            self.redEffect()
        if self.meth == 7:
            self.cancel()
            self.thresholdFilter()
        if self.meth == 45:
            self.cancel()
            self.backgroundHue()
        if self.meth == 80:
            self.cancel()
            self.crop()
        if self.meth == 107:
            self.cancel()
            self.testFunction3()

    def updateF(self, F):
        """Update F parameter"""
        self.ff = F
        if self.meth == 5:
            self.cancel()
            self.rgb()
        if self.meth == 2:
            self.cancel()
            self.contrast()
        if self.meth == 7:
            self.cancel()
            self.thresholdFilter()
        if self.meth == 45:
            self.cancel()
            self.backgroundHue()
        if self.meth == 48:
            self.cancel()
            self.superimpose1on2()

    def updatePoint(self, p):
        """Update point parameter"""
        self.pp = p
        # print("p: ", self.pp)
        if self.meth == 29:
            if self.pp < 6:
                self.pointer()
        if self.meth == 30:
            if self.pp < 6:
                self.verticalStroke()
        if self.meth == 31:
            if self.pp < 6:
                self.horizontalStroke()

    #        if self.meth == 15:
    #           self.grayTint()
    #        if self.meth == 16:
    #           self.colorize()
    #        if self.meth == 75:
    #           self.medallion()
    def updateSeed(self, s):
        """Update seed parameter"""
        self.seed = s
        if self.meth == 62:
            self.fixedEncryption()
        if self.meth == 63:
            self.decryption()

    def updateFilter(self, t):
        """Update t parameter (filter size)"""
        self.tt = t
        if self.meth == 20 or self.meth == 21:
            if self.tt != 3 or self.tt != 5 or self.tt != 7 or self.tt != 9:
                self.tt = 3

    def enableButton(self, value):
        """ Buttons enabled or disabled
        argument:   value = True -> button enabled
                    value = False -> button disabled
        """
        self.pushButtonVerticalSymmetry.setEnabled(value)
        self.pushButtonHorizontalSymmetry.setEnabled(value)
        self.pushButtonRotation90.setEnabled(value)
        self.pushButtonRotation.setEnabled(value)
        self.pushButtonDiagonalization.setEnabled(value)
        self.pushButtonMedallion.setEnabled(value)
        self.pushButtonTranslation.setEnabled(value)
        self.pushButtonZoomPlus.setEnabled(value)
        self.pushButtonZoomPlusBilinear.setEnabled(value)
        self.pushButtonZoomLess.setEnabled(value)
        self.pushButtonCrop.setEnabled(value)
        self.pushButtonValidation.setEnabled(value)
        self.pushButtonBrightness.setEnabled(value)
        self.pushButtonContrast.setEnabled(value)
        self.pushButtonRGB.setEnabled(value)
        self.pushButtonLuminance.setEnabled(value)
        self.pushButtonRedEffect.setEnabled(value)
        self.pushButtonGaussianFilter.setEnabled(value)
        self.pushButtonWindowing.setEnabled(value)
        self.pushButtonThresholding.setEnabled(value)
        self.pushButtonBinarization.setEnabled(value)
        self.pushButtonIntegratingFilter.setEnabled(value)
        self.pushButtonMedianFilter.setEnabled(value)
        self.pushButtonNegative.setEnabled(value)
        self.pushButtonHorizontalGradient.setEnabled(value)
        self.pushButtonVerticalGradient.setEnabled(value)
        self.pushButtonBorderDetect.setEnabled(value)
        self.pushButtonErosion.setEnabled(value)
        self.pushButtonDilation.setEnabled(value)
        self.pushButtonGamma.setEnabled(value)
        self.pushButtonPoint.setEnabled(value)
        self.pushButtonVerticalStroke.setEnabled(value)
        self.pushButtonHorizontalStroke.setEnabled(value)
        self.pushButtonRedFilter.setEnabled(value)
        self.pushButtonGreenFilter.setEnabled(value)
        self.pushButtonBlueFilter.setEnabled(value)
        self.pushButtonTransparency.setEnabled(value)
        self.pushButtonSepia.setEnabled(value)
        self.pushButtonGreyLevel.setEnabled(value)
        self.pushButtonColorLevel.setEnabled(value)
        self.pushButtonFalseColors.setEnabled(value)
        self.pushButtonRedBackground.setEnabled(value)
        self.pushButtonGreenBackground.setEnabled(value)
        self.pushButtonBlueBackground.setEnabled(value)
        self.pushButtonWhiteBackground.setEnabled(value)
        self.pushButtonBlackBackground.setEnabled(value)
        self.pushButtonTintBackground.setEnabled(value)
        self.pushButtonGreenScreen.setEnabled(value)
        self.pushButtonAnaglyph.setEnabled(value)
        self.pushButtonOverlay1on2.setEnabled(value)
        self.pushButtonPepperAndSaltNoise.setEnabled(value)
        self.pushButtonGaussianNoise.setEnabled(value)
        self.pushButtonWhiteNoise.setEnabled(value)
        self.pushButtonPixellation.setEnabled(value)
        self.pushButtonEncryption.setEnabled(value)
        self.pushButtonFixedEncryption.setEnabled(value)
        self.pushButtonDecryption.setEnabled(value)
        self.pushButtonHideSecret.setEnabled(value)
        self.pushButtonShowSecret.setEnabled(value)
        self.pushButtonSteganography.setEnabled(value)
        self.pushButtonShowText.setEnabled(value)
        self.pushButtonAsciiFile.setEnabled(value)
        self.pushButtonPuzzle.setEnabled(value)
        self.pushButtonHistogram.setEnabled(value)
        self.pushButtonConvolution.setEnabled(value)


def main():
    app = QtWidgets.QApplication(sys.argv)

    #  Initialization of translator
    qt_translator = QTranslator(app)
    global currentLangFile
    if currentLangFile:
        qt_translator.load(currentLangFile)
        app.installTranslator(qt_translator)
    window = Image()
    window.adjustSize()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
