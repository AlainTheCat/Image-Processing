cimport cython
import numpy as np
cimport numpy as np

        # np.dtype([(('blue', 'b'), np.uint8), (('green', 'g'), np.uint8), (('red', 'r'), np.uint8), (('alpha', 'a'), np.uint8)])
        # dtype([(('blue', 'b'), 'u1'), (('green', 'g'), 'u1'), (('red', 'r'), 'u1'), (('alpha', 'a'), 'u1')])

# DTYPE = np.dtype([(('blue', 'b'), np.uint8), (('green', 'g'), np.uint8), (('red', 'r'), np.uint8), (('alpha', 'a'), np.uint8)])
# DTYPE = [(('blue', 'b'), 'u1'), (('green', 'g'), 'u1'), (('red', 'r'), 'u1'), (('alpha', 'a'), 'u1')]
# ctypedef np.dtype([(('blue', 'b'), np.uint8_t), (('green', 'g'), np.uint8_t), (('red', 'r'), np.uint8_t), (('alpha', 'a'), np.uint8_t)]) DTYPE_t

def negative(np.ndarray im, np.ndarray imT):
    imT["r"] = 255 - im["r"]
    imT["g"] = 255 - im["g"]
    imT["b"] = 255 - im["b"]
    imT["a"] = im["a"]

def lineX(np.ndarray im, np.ndarray imT, int X):
    cdef int j
    imT["r"] = im["r"]
    imT["g"] = im["g"]
    imT["b"] = im["b"]
    imT["a"] = im["a"]
    for j in range(0, imT.shape[1]):
        imT[j, X] = 255

@cython.boundscheck(False)
@cython.wraparound(False)
def translate(np.ndarray im, np.ndarray imT, int dX, int dY):
    cdef int i
    cdef int j
    cdef int height
    cdef int width
    height = im.shape[0]
    width = im.shape[1]
    for j in range(height):
        for i in range(width):
            if j + dY < 0 or j + dY > height - 1 or i + dX < 0 or i + dX > width - 1:
                imT[j, i] = 127
            else:
                imT[j, i] = im[j + dY, i + dX]

@cython.boundscheck(False)
@cython.wraparound(False)
def translateOK(np.ndarray im, np.ndarray imT, int dX, int dY):
    cdef int i
    cdef int j
    cdef int height2
    cdef int width2
    height2 = imT.shape[0]
    width2 = imT.shape[1]
    for j in range(height2):
        for i in range(width2):
            imT[j, i] = im[j + dY, i + dX]

"""
TODO
@cython.boundscheck(False)
@cython.wraparound(False)
# ci.crop(im0, imT, posX1, posX2, posY1, posY2)
def crop(np.ndarray im, np.ndarray imT, int posX1, int posX2, int posY1, int posY2)
    cdef int i
    cdef int j
    cdef int height
    cdef int width
    cdef int height2
    cdef int width2
    height2 = posY2 - posY1
    width2 = posX2 - posX1
    for j in range(height):
        for i in range(width):
            ....
"""

def rotate(np.ndarray im, np.ndarray imT, float theta):
    cdef int i
    cdef int j
    cdef int I
    cdef int J
    cdef int width
    cdef int height
    cdef float w2
    cdef float h2
    cdef float c2
    cdef float s2
    height = im.shape[0]
    width = im.shape[1]
    w2 = width / 2
    h2 = height / 2
    c2 = np.cos(theta)
    s2 = np.sin(theta)
    for j in range(height):
        for i in range(width):
            J = int((j - w2) * c2 + (i - h2) * s2 + w2)
            I = int(-(j - w2) * s2 + (i - h2) * c2 + h2)
            if 0 <= J < height - 1 and I >= 0 and I < width - 1:
                imT[j, i] = im[J, I]
            else:
                imT[j, i] = 127

@cython.boundscheck(False)
@cython.wraparound(False)
def hrGradient(np.ndarray im, np.ndarray imT):
    cdef int i
    cdef int j
    cdef int width
    cdef int height
    """
    Filtrage horizontal -> h(i, j)
                 1  2  1
                 0  0  0
                -1 -2 -1
    """
    cdef np.ndarray filter = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype = np.int8)
    cdef np.ndarray tabRed = np.zeros((9,), dtype=np.uint8)
    cdef np.ndarray tabGreen = np.zeros((9,), dtype=np.uint8)
    cdef np.ndarray tabBlue = np.zeros((9,), dtype=np.uint8)

    height = im.shape[0]
    width = im.shape[1]

    for j in range(height):
        for i in range(width):
            imT[j, i] = im[j, i]

    for j in range(1, height - 1, 1):
        for i in range(1, width - 1, 1):
            tabRed[0] = im[j - 1, i - 1]["r"]
            tabGreen[0] = im[j - 1, i - 1]["g"]
            tabBlue[0] = im[j - 1, i - 1]["b"]
            tabRed[1] = im[j - 1, i]["r"]
            tabGreen[1] = im[j - 1, i]["g"]
            tabBlue[1] = im[j - 1, i]["b"]
            tabRed[2] = im[j - 1, i + 1]["r"]
            tabGreen[2] = im[j - 1, i + 1]["g"]
            tabBlue[2] = im[j - 1, i + 1]["b"]
            tabRed[3] = im[j, i - 1]["r"]
            tabGreen[3] = im[j, i - 1]["g"]
            tabBlue[3] = im[j, i - 1]["b"]
            tabRed[4] = im[j, i]["r"]
            tabGreen[4] = im[j, i]["g"]
            tabBlue[4] = im[j, i]["b"]
            tabRed[5] = im[j, i + 1]["r"]
            tabGreen[5] = im[j, i + 1]["g"]
            tabBlue[5] = im[j, i + 1]["b"]
            tabRed[6] = im[j + 1, i - 1]["r"]
            tabGreen[6] = im[j + 1, i - 1]["g"]
            tabBlue[6] = im[j + 1, i - 1]["b"]
            tabRed[7] = im[j + 1, i]["r"]
            tabGreen[7] = im[j + 1, i]["g"]
            tabBlue[7] = im[j + 1, i]["b"]
            tabRed[8] = im[j + 1, i + 1]["r"]
            tabGreen[8] = im[j + 1, i + 1]["g"]
            tabBlue[8] = im[j + 1, i + 1]["b"]

            imT[j, i]["r"] = 255 - max(0, min(255, (
                        tabRed[0] * filter[0][0] + tabRed[1] * filter[1][0] + tabRed[2] * filter[2][0]
                        + tabRed[3] * filter[0][1] + tabRed[4] * filter[1][1] + tabRed[5] * filter[2][1]
                        + tabRed[6] * filter[0][2] + tabRed[7] * filter[1][2] + tabRed[8] * filter[2][2])))
            imT[j, i]["g"] = 255 - max(0, min(255, (
                        tabGreen[0] * filter[0][0] + tabGreen[1] * filter[1][0] + tabGreen[2] * filter[2][0]
                        + tabGreen[3] * filter[0][1] + tabGreen[4] * filter[1][1] + tabGreen[5] * filter[2][1]
                        + tabGreen[6] * filter[0][2] + tabGreen[7] * filter[1][2] + tabGreen[8] * filter[2][2])))
            imT[j, i]["b"] = 255 - max(0, min(255, (
                        tabBlue[0] * filter[0][0] + tabBlue[1] * filter[1][0] + tabBlue[2] * filter[2][0]
                        + tabBlue[3] * filter[0][1] + tabBlue[4] * filter[1][1] + tabBlue[5] * filter[2][1]
                        + tabBlue[6] * filter[0][2] + tabBlue[7] * filter[1][2] + tabBlue[8] * filter[2][2])))

@cython.boundscheck(False)
@cython.wraparound(False)
def vtGradient(np.ndarray im, np.ndarray imT):
    cdef int i
    cdef int j
    cdef int width
    cdef int height
    """
    Filtrage vertical -> v(i, j)
                1 0 -1
                2 0 -2
                1 0 -1
    """
    cdef np.ndarray filter = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]], dtype = np.int8)
    cdef np.ndarray tabRed = np.zeros((9,), dtype=np.uint8)
    cdef np.ndarray tabGreen = np.zeros((9,), dtype=np.uint8)
    cdef np.ndarray tabBlue = np.zeros((9,), dtype=np.uint8)

    height = im.shape[0]
    width = im.shape[1]

    for j in range(height):
        for i in range(width):
            imT[j, i] = im[j, i]

    for j in range(1, height - 1, 1):
        for i in range(1, width - 1, 1):
            tabRed[0] = im[j - 1, i - 1]["r"]
            tabGreen[0] = im[j - 1, i - 1]["g"]
            tabBlue[0] = im[j - 1, i - 1]["b"]
            tabRed[1] = im[j - 1, i]["r"]
            tabGreen[1] = im[j - 1, i]["g"]
            tabBlue[1] = im[j - 1, i]["b"]
            tabRed[2] = im[j - 1, i + 1]["r"]
            tabGreen[2] = im[j - 1, i + 1]["g"]
            tabBlue[2] = im[j - 1, i + 1]["b"]
            tabRed[3] = im[j, i - 1]["r"]
            tabGreen[3] = im[j, i - 1]["g"]
            tabBlue[3] = im[j, i - 1]["b"]
            tabRed[4] = im[j, i]["r"]
            tabGreen[4] = im[j, i]["g"]
            tabBlue[4] = im[j, i]["b"]
            tabRed[5] = im[j, i + 1]["r"]
            tabGreen[5] = im[j, i + 1]["g"]
            tabBlue[5] = im[j, i + 1]["b"]
            tabRed[6] = im[j + 1, i - 1]["r"]
            tabGreen[6] = im[j + 1, i - 1]["g"]
            tabBlue[6] = im[j + 1, i - 1]["b"]
            tabRed[7] = im[j + 1, i]["r"]
            tabGreen[7] = im[j + 1, i]["g"]
            tabBlue[7] = im[j + 1, i]["b"]
            tabRed[8] = im[j + 1, i + 1]["r"]
            tabGreen[8] = im[j + 1, i + 1]["g"]
            tabBlue[8] = im[j + 1, i + 1]["b"]

            imT[j, i]["r"] = 255 - max(0, min(255, (
                        tabRed[0] * filter[0][0] + tabRed[1] * filter[1][0] + tabRed[2] * filter[2][0]
                        + tabRed[3] * filter[0][1] + tabRed[4] * filter[1][1] + tabRed[5] * filter[2][1]
                        + tabRed[6] * filter[0][2] + tabRed[7] * filter[1][2] + tabRed[8] * filter[2][2])))
            imT[j, i]["g"] = 255 - max(0, min(255, (
                        tabGreen[0] * filter[0][0] + tabGreen[1] * filter[1][0] + tabGreen[2] * filter[2][0]
                        + tabGreen[3] * filter[0][1] + tabGreen[4] * filter[1][1] + tabGreen[5] * filter[2][1]
                        + tabGreen[6] * filter[0][2] + tabGreen[7] * filter[1][2] + tabGreen[8] * filter[2][2])))
            imT[j, i]["b"] = 255 - max(0, min(255, (
                        tabBlue[0] * filter[0][0] + tabBlue[1] * filter[1][0] + tabBlue[2] * filter[2][0]
                        + tabBlue[3] * filter[0][1] + tabBlue[4] * filter[1][1] + tabBlue[5] * filter[2][1]
                        + tabBlue[6] * filter[0][2] + tabBlue[7] * filter[1][2] + tabBlue[8] * filter[2][2])))

def border(np.ndarray im, np.ndarray imT):
    cdef int i
    cdef int j
    cdef int width
    cdef int height

    cdef np.ndarray filterH = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype = np.int8)
    cdef np.ndarray filterV = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]], dtype = np.int8)
    cdef np.ndarray tabRed = np.zeros((9,), dtype=np.uint8)
    cdef np.ndarray tabGreen = np.zeros((9,), dtype=np.uint8)
    cdef np.ndarray tabBlue = np.zeros((9,), dtype=np.uint8)

    height = im.shape[0]
    width = im.shape[1]

    for j in range(height):
        for i in range(width):
            imT[j, i] = im[j, i]

    for j in range(1, height - 1, 1):
        for i in range(1, width - 1, 1):
            tabRed[0] = im[j - 1, i - 1]["r"]
            tabGreen[0] = im[j - 1, i - 1]["g"]
            tabBlue[0] = im[j - 1, i - 1]["b"]
            tabRed[1] = im[j - 1, i]["r"]
            tabGreen[1] = im[j - 1, i]["g"]
            tabBlue[1] = im[j - 1, i]["b"]
            tabRed[2] = im[j - 1, i + 1]["r"]
            tabGreen[2] = im[j - 1, i + 1]["g"]
            tabBlue[2] = im[j - 1, i + 1]["b"]
            tabRed[3] = im[j, i - 1]["r"]
            tabGreen[3] = im[j, i - 1]["g"]
            tabBlue[3] = im[j, i - 1]["b"]
            tabRed[4] = im[j, i]["r"]
            tabGreen[4] = im[j, i]["g"]
            tabBlue[4] = im[j, i]["b"]
            tabRed[5] = im[j, i + 1]["r"]
            tabGreen[5] = im[j, i + 1]["g"]
            tabBlue[5] = im[j, i + 1]["b"]
            tabRed[6] = im[j + 1, i - 1]["r"]
            tabGreen[6] = im[j + 1, i - 1]["g"]
            tabBlue[6] = im[j + 1, i - 1]["b"]
            tabRed[7] = im[j + 1, i]["r"]
            tabGreen[7] = im[j + 1, i]["g"]
            tabBlue[7] = im[j + 1, i]["b"]
            tabRed[8] = im[j + 1, i + 1]["r"]
            tabGreen[8] = im[j + 1, i + 1]["g"]
            tabBlue[8] = im[j + 1, i + 1]["b"]

            imT[j, i]["r"] = 255 - min(255,
                        max(0, min(255, (
                        tabRed[0] * filterV[0][0] + tabRed[1] * filterV[1][0] + tabRed[2] * filterV[2][0]
                        + tabRed[3] * filterV[0][1] + tabRed[4] * filterV[1][1] + tabRed[5] * filterV[2][1]
                        + tabRed[6] * filterV[0][2] + tabRed[7] * filterV[1][2] + tabRed[8] * filterV[2][2])))
                        + max(0, min(255, (
                        tabRed[0] * filterH[0][0] + tabRed[1] * filterH[1][0] + tabRed[2] * filterH[2][0]
                        + tabRed[3] * filterH[0][1] + tabRed[4] * filterH[1][1] + tabRed[5] * filterH[2][1]
                        + tabRed[6] * filterH[0][2] + tabRed[7] * filterH[1][2] + tabRed[8] * filterH[2][2])))
                        )
            imT[j, i]["g"] = 255 - min(255,
                        max(0, min(255, (
                        tabGreen[0] * filterV[0][0] + tabGreen[1] * filterV[1][0] + tabGreen[2] * filterV[2][0]
                        + tabGreen[3] * filterV[0][1] + tabGreen[4] * filterV[1][1] + tabGreen[5] * filterV[2][1]
                        + tabGreen[6] * filterV[0][2] + tabGreen[7] * filterV[1][2] + tabGreen[8] * filterV[2][2])))
                        + max(0, min(255, (
                        tabGreen[0] * filterH[0][0] + tabGreen[1] * filterH[1][0] + tabGreen[2] * filterH[2][0]
                        + tabGreen[3] * filterH[0][1] + tabGreen[4] * filterH[1][1] + tabGreen[5] * filterH[2][1]
                        + tabGreen[6] * filterH[0][2] + tabGreen[7] * filterH[1][2] + tabGreen[8] * filterH[2][2])))
                        )
            imT[j, i]["b"] = 255 - min(255,
                        max(0, min(255, (
                        tabBlue[0] * filterV[0][0] + tabBlue[1] * filterV[1][0] + tabBlue[2] * filterV[2][0]
                        + tabBlue[3] * filterV[0][1] + tabBlue[4] * filterV[1][1] + tabBlue[5] * filterV[2][1]
                        + tabBlue[6] * filterV[0][2] + tabBlue[7] * filterV[1][2] + tabBlue[8] * filterV[2][2])))
                        + max(0, min(255, (
                        tabBlue[0] * filterH[0][0] + tabBlue[1] * filterH[1][0] + tabBlue[2] * filterH[2][0]
                        + tabBlue[3] * filterH[0][1] + tabBlue[4] * filterH[1][1] + tabBlue[5] * filterH[2][1]
                        + tabBlue[6] * filterH[0][2] + tabBlue[7] * filterH[1][2] + tabBlue[8] * filterH[2][2])))
                        )

@cython.boundscheck(False)
@cython.wraparound(False)
def point(np.ndarray imT, np.ndarray lum, int step):
    cdef int i
    cdef int j
    cdef int width
    cdef int height
    cdef int h
    cdef int l
    cdef int s

    height = imT.shape[0]
    width = imT.shape[1]

    s = 0

    if step == 2:
        height = height - height % 2
        width = width - width % 2

        for j in range(0, height, 2):
            for i in range(0, width, 2):
                for h in range(2):
                    for l in range(2):
                        s = s +  int(lum[j+h, i+l])
                s = int(s / 4)
                if s >= 171:
                    imT["r"][j, i] = 255
                    imT["g"][j, i] = 255
                    imT["b"][j, i] = 255
                    imT["r"][j, i + 1] = 255
                    imT["g"][j, i + 1] = 255
                    imT["b"][j, i + 1] = 255
                    imT["r"][j + 1, i] = 255
                    imT["g"][j + 1, i] = 255
                    imT["b"][j + 1, i] = 255
                    imT["r"][j + 1, i + 1] = 255
                    imT["g"][j + 1, i + 1] = 255
                    imT["b"][j + 1, i + 1] = 255
                elif s >= 85 and s < 171:
                    imT["r"][j, i + 1] = 255
                    imT["g"][j, i + 1] = 255
                    imT["b"][j, i + 1] = 255
                    imT["r"][j + 1, i] = 255
                    imT["g"][j + 1, i] = 255
                    imT["b"][j + 1, i] = 255

    elif step == 3:
        height = height - height % 3
        width = width - width % 3

        for j in range(0, height, 3):
            for i in range(0, width, 3):
                for h in range(3):
                    for l in range(3):
                        s = s +  int(lum[j+h, i+l])
                s = int(s / 9)
                if s >= 192:
                    for h in range(3):
                        for l in range(3):
                            imT["r"][j + h, i + l] = 255
                            imT["g"][j + h, i + l] = 255
                            imT["b"][j + h, i + l] = 255
                elif s >=  128 and s < 192:
                    imT["r"][j, i + 1] = 255
                    imT["g"][j, i + 1] = 255
                    imT["b"][j, i + 1] = 255
                    imT["r"][j + 1, i] = 255
                    imT["g"][j + 1, i] = 255
                    imT["b"][j + 1, i] = 255
                    imT["r"][j + 1, i + 1] = 255
                    imT["g"][j + 1, i + 1] = 255
                    imT["b"][j + 1, i + 1] = 255
                    imT["r"][j + 1, i + 2] = 255
                    imT["g"][j + 1, i + 2] = 255
                    imT["b"][j + 1, i + 2] = 255
                    imT["r"][j + 2, i + 1] = 255
                    imT["g"][j + 2, i + 1] = 255
                    imT["b"][j + 2, i + 1] = 255
                elif s >= 64 and s < 128:
                    imT["r"][j + 1, i + 1] = 255
                    imT["g"][j + 1, i + 1] = 255
                    imT["b"][j + 1, i + 1] = 255

    elif step == 4:
        height = height - height % 4
        width = width - width % 4

        for j in range(0, height, 4):
            for i in range(0, width, 4):
                for h in range(4):
                    for l in range(4):
                        s = s +  int(lum[j+h, i+l])
                s = int(s / 16)
                if s >= 205:
                    for h in range(4):
                        for l in range(4):
                            imT["r"][j + h, i + l] = 255
                            imT["g"][j + h, i + l] = 255
                            imT["b"][j + h, i + l] = 255
                elif s >=  154 and s < 205:
                    imT["r"][j, i + 1] = 255
                    imT["g"][j, i + 1] = 255
                    imT["b"][j, i + 1] = 255
                    imT["r"][j, i + 2] = 255
                    imT["g"][j, i + 2] = 255
                    imT["b"][j, i + 2] = 255
                    imT["r"][j + 1, i] = 255
                    imT["g"][j + 1, i] = 255
                    imT["b"][j + 1, i] = 255
                    imT["r"][j + 1, i + 1] = 255
                    imT["g"][j + 1, i + 1] = 255
                    imT["b"][j + 1, i + 1] = 255
                    imT["r"][j + 1, i + 2] = 255
                    imT["g"][j + 1, i + 2] = 255
                    imT["b"][j + 1, i + 2] = 255
                    imT["r"][j + 1, i + 3] = 255
                    imT["g"][j + 1, i + 3] = 255
                    imT["b"][j + 1, i + 3] = 255
                    imT["r"][j + 2, i] = 255
                    imT["g"][j + 2, i] = 255
                    imT["b"][j + 2, i] = 255
                    imT["r"][j + 2, i + 1] = 255
                    imT["g"][j + 2, i + 1] = 255
                    imT["b"][j + 2, i + 1] = 255
                    imT["r"][j + 2, i + 2] = 255
                    imT["g"][j + 2, i + 2] = 255
                    imT["b"][j + 2, i + 2] = 255
                    imT["r"][j + 2, i + 3] = 255
                    imT["g"][j + 2, i + 3] = 255
                    imT["b"][j + 2, i + 3] = 255
                    imT["r"][j + 3, i + 1] = 255
                    imT["g"][j + 3, i + 1] = 255
                    imT["b"][j + 3, i + 1] = 255
                    imT["r"][j + 3, i + 2] = 255
                    imT["g"][j + 3, i + 2] = 255
                    imT["b"][j + 3, i + 2] = 255
                elif s >= 102 and s < 154:
                    imT["r"][j + 1, i + 1] = 255
                    imT["g"][j + 1, i + 1] = 255
                    imT["b"][j + 1, i + 1] = 255
                    imT["r"][j + 1, i + 2] = 255
                    imT["g"][j + 1, i + 2] = 255
                    imT["b"][j + 1, i + 2] = 255
                    imT["r"][j + 2, i + 1] = 255
                    imT["g"][j + 2, i + 1] = 255
                    imT["b"][j + 2, i + 1] = 255
                    imT["r"][j + 2, i + 2] = 255
                    imT["g"][j + 2, i + 2] = 255
                    imT["b"][j + 2, i + 2] = 255
                elif s >= 51 and s < 102:
                    imT["r"][j + 1, i + 1] = 255
                    imT["g"][j + 1, i + 1] = 255
                    imT["b"][j + 1, i + 1] = 255
                    imT["r"][j + 2, i + 2] = 255
                    imT["g"][j + 2, i + 2] = 255
                    imT["b"][j + 2, i + 2] = 255
    elif step == 5:
        height = height - height % 5
        width = width - width % 5

        for j in range(0, height, 5):
            for i in range(0, width, 5):
                for h in range(5):
                    for l in range(5):
                        s = s +  int(lum[j+h, i+l])
                s = int(s / 25)
                if s >= 213:
                    for h in range(4):
                        for l in range(4):
                            imT["r"][j + h, i + l] = 255
                            imT["g"][j + h, i + l] = 255
                            imT["b"][j + h, i + l] = 255
                elif s >=  171 and s < 213:
                    imT["r"][j, i + 2] = 255
                    imT["g"][j, i + 2] = 255
                    imT["b"][j, i + 2] = 255
                    imT["r"][j + 1, i + 1] = 255
                    imT["g"][j + 1, i + 1] = 255
                    imT["b"][j + 1, i + 1] = 255
                    imT["r"][j + 1, i + 2] = 255
                    imT["g"][j + 1, i + 2] = 255
                    imT["b"][j + 1, i + 2] = 255
                    imT["r"][j + 1, i + 3] = 255
                    imT["g"][j + 1, i + 3] = 255
                    imT["b"][j + 1, i + 3] = 255
                    imT["r"][j + 2, i] = 255
                    imT["g"][j + 2, i] = 255
                    imT["b"][j + 2, i] = 255
                    imT["r"][j + 2, i + 1] = 255
                    imT["g"][j + 2, i + 1] = 255
                    imT["b"][j + 2, i + 1] = 255
                    imT["r"][j + 2, i + 2] = 255
                    imT["g"][j + 2, i + 2] = 255
                    imT["b"][j + 2, i + 2] = 255
                    imT["r"][j + 2, i + 3] = 255
                    imT["g"][j + 2, i + 3] = 255
                    imT["b"][j + 2, i + 3] = 255
                    imT["r"][j + 2, i + 4] = 255
                    imT["g"][j + 2, i + 4] = 255
                    imT["b"][j + 2, i + 4] = 255
                    imT["r"][j + 3, i + 1] = 255
                    imT["g"][j + 3, i + 1] = 255
                    imT["b"][j + 3, i + 1] = 255
                    imT["r"][j + 3, i + 2] = 255
                    imT["g"][j + 3, i + 2] = 255
                    imT["b"][j + 3, i + 2] = 255
                    imT["r"][j + 3, i + 3] = 255
                    imT["g"][j + 3, i + 3] = 255
                    imT["b"][j + 3, i + 3] = 255
                    imT["r"][j + 4, i + 2] = 255
                    imT["g"][j + 4, i + 2] = 255
                    imT["b"][j + 4, i + 2] = 255
                elif s >=  128 and s < 171:
                    imT["r"][j + 1, i + 1] = 255
                    imT["g"][j + 1, i + 1] = 255
                    imT["b"][j + 1, i + 1] = 255
                    imT["r"][j + 1, i + 2] = 255
                    imT["g"][j + 1, i + 2] = 255
                    imT["b"][j + 1, i + 2] = 255
                    imT["r"][j + 1, i + 3] = 255
                    imT["g"][j + 1, i + 3] = 255
                    imT["b"][j + 1, i + 3] = 255
                    imT["r"][j + 2, i + 1] = 255
                    imT["g"][j + 2, i + 1] = 255
                    imT["b"][j + 2, i + 1] = 255
                    imT["r"][j + 2, i + 2] = 255
                    imT["g"][j + 2, i + 2] = 255
                    imT["b"][j + 2, i + 2] = 255
                    imT["r"][j + 2, i + 3] = 255
                    imT["g"][j + 2, i + 3] = 255
                    imT["b"][j + 2, i + 3] = 255
                    imT["r"][j + 3, i + 1] = 255
                    imT["g"][j + 3, i + 1] = 255
                    imT["b"][j + 3, i + 1] = 255
                    imT["r"][j + 3, i + 2] = 255
                    imT["g"][j + 3, i + 2] = 255
                    imT["b"][j + 3, i + 2] = 255
                    imT["r"][j + 3, i + 3] = 255
                    imT["g"][j + 3, i + 3] = 255
                    imT["b"][j + 3, i + 3] = 255
                elif s >=  85 and s < 128:
                    imT["r"][j + 1, i + 2] = 255
                    imT["g"][j + 1, i + 2] = 255
                    imT["b"][j + 1, i + 2] = 255
                    imT["r"][j + 2, i + 1] = 255
                    imT["g"][j + 2, i + 1] = 255
                    imT["b"][j + 2, i + 1] = 255
                    imT["r"][j + 2, i + 2] = 255
                    imT["g"][j + 2, i + 2] = 255
                    imT["b"][j + 2, i + 2] = 255
                    imT["r"][j + 2, i + 3] = 255
                    imT["g"][j + 2, i + 3] = 255
                    imT["b"][j + 2, i + 3] = 255
                    imT["r"][j + 3, i + 2] = 255
                    imT["g"][j + 3, i + 2] = 255
                    imT["b"][j + 3, i + 2] = 255
                elif s >=  85 and s < 128:
                    imT["r"][j + 2, i + 2] = 255
                    imT["g"][j + 2, i + 2] = 255
                    imT["b"][j + 2, i + 2] = 255

@cython.boundscheck(False)
@cython.wraparound(False)
def stroke(np.ndarray imT, np.ndarray lum, int step):
    cdef int i
    cdef int j
    cdef int width
    cdef int height
    cdef int h
    cdef int l
    cdef int s

    height = imT.shape[0]
    width = imT.shape[1]

    s = 0

    if step == 2:
        height = height - height % 2
        width = width - width % 2

        for j in range(0, height, 2):
            for i in range(0, width, 2):
                for h in range(2):
                    for l in range(2):
                        s = s +  int(lum[j+h, i+l])
                s = int(s / 4)
                if s >= 171:
                    imT["r"][j, i] = 255
                    imT["g"][j, i] = 255
                    imT["b"][j, i] = 255
                    imT["r"][j, i + 1] = 255
                    imT["g"][j, i + 1] = 255
                    imT["b"][j, i + 1] = 255
                    imT["r"][j + 1, i] = 255
                    imT["g"][j + 1, i] = 255
                    imT["b"][j + 1, i] = 255
                    imT["r"][j + 1, i + 1] = 255
                    imT["g"][j + 1, i + 1] = 255
                    imT["b"][j + 1, i + 1] = 255
                elif s >= 85 and s < 171:
                    imT["r"][j, i + 1] = 255
                    imT["g"][j, i + 1] = 255
                    imT["b"][j, i + 1] = 255
                    imT["r"][j + 1, i + 1] = 255
                    imT["g"][j + 1, i + 1] = 255
                    imT["b"][j + 1, i + 1] = 255

    elif step == 3:
        height = height - height % 3
        width = width - width % 3

        for j in range(0, height, 3):
            for i in range(0, width, 3):
                for h in range(3):
                    for l in range(3):
                        s = s +  int(lum[j+h, i+l])
                s = int(s / 9)
                if s >= 192:
                    for h in range(3):
                        for l in range(3):
                            imT["r"][j + h, i + l] = 255
                            imT["g"][j + h, i + l] = 255
                            imT["b"][j + h, i + l] = 255
                elif s >=  128 and s < 192:
                    imT["r"][j, i + 1] = 255
                    imT["g"][j, i + 1] = 255
                    imT["b"][j, i + 1] = 255
                    imT["r"][j, i + 2] = 255
                    imT["g"][j, i + 2] = 255
                    imT["b"][j, i + 2] = 255
                    imT["r"][j + 1, i + 1] = 255
                    imT["g"][j + 1, i + 1] = 255
                    imT["b"][j + 1, i + 1] = 255
                    imT["r"][j + 1, i + 2] = 255
                    imT["g"][j + 1, i + 2] = 255
                    imT["b"][j + 1, i + 2] = 255
                    imT["r"][j + 2, i + 1] = 255
                    imT["g"][j + 2, i + 1] = 255
                    imT["b"][j + 2, i + 1] = 255
                    imT["r"][j + 2, i + 2] = 255
                    imT["g"][j + 2, i + 2] = 255
                    imT["b"][j + 2, i + 2] = 255
                elif s >= 64 and s < 128:
                    imT["r"][j, i + 1] = 255
                    imT["g"][j, i + 1] = 255
                    imT["b"][j, i + 1] = 255
                    imT["r"][j + 1, i + 1] = 255
                    imT["g"][j + 1, i + 1] = 255
                    imT["b"][j + 1, i + 1] = 255
                    imT["r"][j + 2, i + 1] = 255
                    imT["g"][j + 2, i + 1] = 255
                    imT["b"][j + 2, i + 1] = 255
    elif step == 4:
        height = height - height % 4
        width = width - width % 4

        for j in range(0, height, 4):
            for i in range(0, width, 4):
                for h in range(4):
                    for l in range(4):
                        s = s +  int(lum[j+h, i+l])
                s = int(s / 16)
                if s >= 205:
                    for h in range(4):
                        for l in range(4):
                            imT["r"][j + h, i + l] = 255
                            imT["g"][j + h, i + l] = 255
                            imT["b"][j + h, i + l] = 255
                elif s >=  154 and s < 205:
                    imT["r"][j, i + 1] = 255
                    imT["g"][j, i + 1] = 255
                    imT["b"][j, i + 1] = 255
                    imT["r"][j, i + 2] = 255
                    imT["g"][j, i + 2] = 255
                    imT["b"][j, i + 2] = 255
                    imT["r"][j, i + 3] = 255
                    imT["g"][j, i + 3] = 255
                    imT["b"][j, i + 3] = 255
                    imT["r"][j + 1, i + 1] = 255
                    imT["g"][j + 1, i + 1] = 255
                    imT["b"][j + 1, i + 1] = 255
                    imT["r"][j + 1, i + 2] = 255
                    imT["g"][j + 1, i + 2] = 255
                    imT["b"][j + 1, i + 2] = 255
                    imT["r"][j + 1, i + 3] = 255
                    imT["g"][j + 1, i + 3] = 255
                    imT["b"][j + 1, i + 3] = 255
                    imT["r"][j + 2, i + 1] = 255
                    imT["g"][j + 2, i + 1] = 255
                    imT["b"][j + 2, i + 1] = 255
                    imT["r"][j + 2, i + 2] = 255
                    imT["g"][j + 2, i + 2] = 255
                    imT["b"][j + 2, i + 2] = 255
                    imT["r"][j + 2, i + 3] = 255
                    imT["g"][j + 2, i + 3] = 255
                    imT["b"][j + 2, i + 3] = 255
                    imT["r"][j + 3, i + 1] = 255
                    imT["g"][j + 3, i + 1] = 255
                    imT["b"][j + 3, i + 1] = 255
                    imT["r"][j + 3, i + 2] = 255
                    imT["g"][j + 3, i + 2] = 255
                    imT["b"][j + 3, i + 2] = 255
                    imT["r"][j + 3, i + 3] = 255
                    imT["g"][j + 3, i + 3] = 255
                    imT["b"][j + 3, i + 3] = 255
                elif s >= 102 and s < 154:
                    imT["r"][j, i + 1] = 255
                    imT["g"][j, i + 1] = 255
                    imT["b"][j, i + 1] = 255
                    imT["r"][j, i + 2] = 255
                    imT["g"][j, i + 2] = 255
                    imT["b"][j, i + 2] = 255
                    imT["r"][j + 1, i + 1] = 255
                    imT["g"][j + 1, i + 1] = 255
                    imT["b"][j + 1, i + 1] = 255
                    imT["r"][j + 1, i + 2] = 255
                    imT["g"][j + 1, i + 2] = 255
                    imT["b"][j + 1, i + 2] = 255
                    imT["r"][j + 2, i + 1] = 255
                    imT["g"][j + 2, i + 1] = 255
                    imT["b"][j + 2, i + 1] = 255
                    imT["r"][j + 2, i + 2] = 255
                    imT["g"][j + 2, i + 2] = 255
                    imT["b"][j + 2, i + 2] = 255
                    imT["r"][j + 3, i + 1] = 255
                    imT["g"][j + 3, i + 1] = 255
                    imT["b"][j + 3, i + 1] = 255
                    imT["r"][j + 3, i + 2] = 255
                    imT["g"][j + 3, i + 2] = 255
                    imT["b"][j + 3, i + 2] = 255
                elif s >= 51 and s < 102:
                    imT["r"][j, i + 1] = 255
                    imT["g"][j, i + 1] = 255
                    imT["b"][j, i + 1] = 255
                    imT["r"][j + 1, i + 1] = 255
                    imT["g"][j + 1, i + 1] = 255
                    imT["b"][j + 1, i + 1] = 255
                    imT["r"][j + 2, i + 1] = 255
                    imT["g"][j + 2, i + 1] = 255
                    imT["b"][j + 2, i + 1] = 255
                    imT["r"][j + 3, i + 1] = 255
                    imT["g"][j + 3, i + 1] = 255
                    imT["b"][j + 3, i + 1] = 255
    elif step == 5:
        height = height - height % 5
        width = width - width % 5

        for j in range(0, height, 5):
            for i in range(0, width, 5):
                for h in range(5):
                    for l in range(5):
                        s = s +  int(lum[j+h, i+l])
                s = int(s / 25)
                if s >= 213:
                    for h in range(4):
                        for l in range(4):
                            imT["r"][j + h, i + l] = 255
                            imT["g"][j + h, i + l] = 255
                            imT["b"][j + h, i + l] = 255
                elif s >=  171 and s < 213:
                    imT["r"][j, i + 1] = 255
                    imT["g"][j, i + 1] = 255
                    imT["b"][j, i + 1] = 255
                    imT["r"][j, i + 2] = 255
                    imT["g"][j, i + 2] = 255
                    imT["b"][j, i + 2] = 255
                    imT["r"][j, i + 3] = 255
                    imT["g"][j, i + 3] = 255
                    imT["b"][j, i + 3] = 255
                    imT["r"][j, i + 4] = 255
                    imT["g"][j, i + 4] = 255
                    imT["b"][j, i + 4] = 255
                    imT["r"][j + 1, i + 1] = 255
                    imT["g"][j + 1, i + 1] = 255
                    imT["b"][j + 1, i + 1] = 255
                    imT["r"][j + 1, i + 2] = 255
                    imT["g"][j + 1, i + 2] = 255
                    imT["b"][j + 1, i + 2] = 255
                    imT["r"][j + 1, i + 3] = 255
                    imT["g"][j + 1, i + 3] = 255
                    imT["b"][j + 1, i + 3] = 255
                    imT["r"][j + 1, i + 4] = 255
                    imT["g"][j + 1, i + 4] = 255
                    imT["b"][j + 1, i + 4] = 255
                    imT["r"][j + 2, i + 1] = 255
                    imT["g"][j + 2, i + 1] = 255
                    imT["b"][j + 2, i + 1] = 255
                    imT["r"][j + 2, i + 2] = 255
                    imT["g"][j + 2, i + 2] = 255
                    imT["b"][j + 2, i + 2] = 255
                    imT["r"][j + 2, i + 3] = 255
                    imT["g"][j + 2, i + 3] = 255
                    imT["b"][j + 2, i + 3] = 255
                    imT["r"][j + 2, i + 4] = 255
                    imT["g"][j + 2, i + 4] = 255
                    imT["b"][j + 2, i + 4] = 255
                    imT["r"][j + 3, i + 1] = 255
                    imT["g"][j + 3, i + 1] = 255
                    imT["b"][j + 3, i + 1] = 255
                    imT["r"][j + 3, i + 2] = 255
                    imT["g"][j + 3, i + 2] = 255
                    imT["b"][j + 3, i + 2] = 255
                    imT["r"][j + 3, i + 3] = 255
                    imT["g"][j + 3, i + 3] = 255
                    imT["b"][j + 3, i + 3] = 255
                    imT["r"][j + 3, i + 4] = 255
                    imT["g"][j + 3, i + 4] = 255
                    imT["b"][j + 3, i + 4] = 255
                    imT["r"][j + 4, i + 1] = 255
                    imT["g"][j + 4, i + 1] = 255
                    imT["b"][j + 4, i + 1] = 255
                    imT["r"][j + 4, i + 2] = 255
                    imT["g"][j + 4, i + 2] = 255
                    imT["b"][j + 4, i + 2] = 255
                    imT["r"][j + 4, i + 3] = 255
                    imT["g"][j + 4, i + 3] = 255
                    imT["b"][j + 4, i + 3] = 255
                    imT["r"][j + 4, i + 4] = 255
                    imT["g"][j + 4, i + 4] = 255
                    imT["b"][j + 4, i + 4] = 255
                elif s >=  128 and s < 171:
                    imT["r"][j, i + 1] = 255
                    imT["g"][j, i + 1] = 255
                    imT["b"][j, i + 1] = 255
                    imT["r"][j, i + 2] = 255
                    imT["g"][j, i + 2] = 255
                    imT["b"][j, i + 2] = 255
                    imT["r"][j, i + 3] = 255
                    imT["g"][j, i + 3] = 255
                    imT["r"][j + 1, i + 1] = 255
                    imT["g"][j + 1, i + 1] = 255
                    imT["b"][j + 1, i + 1] = 255
                    imT["r"][j + 1, i + 2] = 255
                    imT["g"][j + 1, i + 2] = 255
                    imT["b"][j + 1, i + 2] = 255
                    imT["r"][j + 1, i + 3] = 255
                    imT["g"][j + 1, i + 3] = 255
                    imT["b"][j + 1, i + 3] = 255
                    imT["r"][j + 2, i + 1] = 255
                    imT["g"][j + 2, i + 1] = 255
                    imT["b"][j + 2, i + 1] = 255
                    imT["r"][j + 2, i + 2] = 255
                    imT["g"][j + 2, i + 2] = 255
                    imT["b"][j + 2, i + 2] = 255
                    imT["r"][j + 2, i + 3] = 255
                    imT["g"][j + 2, i + 3] = 255
                    imT["b"][j + 2, i + 3] = 255
                    imT["r"][j + 3, i + 1] = 255
                    imT["g"][j + 3, i + 1] = 255
                    imT["b"][j + 3, i + 1] = 255
                    imT["r"][j + 3, i + 2] = 255
                    imT["g"][j + 3, i + 2] = 255
                    imT["b"][j + 3, i + 2] = 255
                    imT["r"][j + 3, i + 3] = 255
                    imT["g"][j + 3, i + 3] = 255
                    imT["b"][j + 3, i + 3] = 255
                    imT["r"][j + 4, i + 1] = 255
                    imT["g"][j + 4, i + 1] = 255
                    imT["b"][j + 4, i + 1] = 255
                    imT["r"][j + 4, i + 2] = 255
                    imT["g"][j + 4, i + 2] = 255
                    imT["b"][j + 4, i + 2] = 255
                    imT["r"][j + 4, i + 3] = 255
                    imT["g"][j + 4, i + 3] = 255
                    imT["b"][j + 4, i + 3] = 255
                elif s >=  85 and s < 128:
                    imT["r"][j, i + 1] = 255
                    imT["g"][j, i + 1] = 255
                    imT["b"][j, i + 1] = 255
                    imT["r"][j, i + 2] = 255
                    imT["g"][j, i + 2] = 255
                    imT["b"][j, i + 2] = 255
                    imT["r"][j + 1, i + 1] = 255
                    imT["g"][j + 1, i + 1] = 255
                    imT["b"][j + 1, i + 1] = 255
                    imT["r"][j + 1, i + 2] = 255
                    imT["g"][j + 1, i + 2] = 255
                    imT["b"][j + 1, i + 2] = 255
                    imT["r"][j + 2, i + 1] = 255
                    imT["g"][j + 2, i + 1] = 255
                    imT["b"][j + 2, i + 1] = 255
                    imT["r"][j + 2, i + 2] = 255
                    imT["g"][j + 2, i + 2] = 255
                    imT["b"][j + 2, i + 2] = 255
                    imT["r"][j + 3, i + 1] = 255
                    imT["g"][j + 3, i + 1] = 255
                    imT["b"][j + 3, i + 1] = 255
                    imT["r"][j + 3, i + 2] = 255
                    imT["g"][j + 3, i + 2] = 255
                    imT["b"][j + 3, i + 2] = 255
                    imT["r"][j + 4, i + 1] = 255
                    imT["g"][j + 4, i + 1] = 255
                    imT["b"][j + 4, i + 1] = 255
                    imT["r"][j + 4, i + 2] = 255
                    imT["g"][j + 4, i + 2] = 255
                    imT["b"][j + 4, i + 2] = 255
                elif s >=  85 and s < 128:
                    imT["r"][j, i + 1] = 255
                    imT["g"][j, i + 1] = 255
                    imT["b"][j, i + 1] = 255
                    imT["r"][j + 1, i + 1] = 255
                    imT["g"][j + 1, i + 1] = 255
                    imT["b"][j + 1, i + 1] = 255
                    imT["r"][j + 2, i + 1] = 255
                    imT["g"][j + 2, i + 1] = 255
                    imT["b"][j + 2, i + 1] = 255
                    imT["r"][j + 3, i + 1] = 255
                    imT["g"][j + 3, i + 1] = 255
                    imT["b"][j + 3, i + 2] = 255
                    imT["r"][j + 4, i + 1] = 255
                    imT["g"][j + 4, i + 1] = 255
                    imT["b"][j + 4, i + 1] = 255
