<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
                 <title> Image Processing - English version</title>
</head>
    <body>
        <p>English version</p>
        <h1>Image processing in Python and Qt with PySide</h1>
        <br /><br />
        <strong>Author: </strong>Alain the cat<br />
        <strong>Creation: </strong>06/08/2013 in C++ and QT<br />
        <strong>Modification: </strong>13/12/2016 in Python and PyQt5 with addition of functions<br />
        <strong>Modification: </strong>14/08/2023 in Python and PySide6 with addition of functions<br />
        <h2>License:</h2>
        <p>This <em>Image processing in Python</em> application is made available under the
            terms of the Creative Commons license.
            You can copy or modify it (Improvements are welcome),
            under the conditions set by the license.</p>
        <h2>Description:</h2>
            <p>This application processes images in Python with PySide6.
                To speed up some processing, functions have been written in Cython and others in C++
                with PyBind11 (Linux version only).</p>
            <p>The main functions are as follows:</p>
                <ul>
                    <li>Geometric transformations</li>
                        <ul>
                            <li>Vertical symmetry</li>
                            <li>Horizontal symmetry</li>
                            <li>Rotation</li>
                            <li>Diagonalization</li>
                            <li>Medallion</li>
                            <li>Translation</li>
                            <li>Zoom +</li>
                            <li>Zoom -</li>
                            <li>Crop</li>
                        </ul>
                    <li>Local filters</li>
                        <ul>
                            <li>Brightness</li>
                            <li>Contrast</li>
                            <li>Luminance</li>
                            <li>Modifying RGB Colors</li>
                            <li>Red effect</li>
                            <li>Threshold</li>
                            <li>Binarization</li>
                            <li>Red, green and blue filters</li>
                            <li>Windowing</li>
                            <li>Greyscale</li>
                            <li>Shade of colors</li>
                            <li>False colors</li>
                            <li>Sepia</li>
                        </ul>
                    <li>Neighborhood filters</li>
                        <ul>
                            <li>Average</li>
                            <li>Median filter</li>
                            <li>Gaussian filter</li>
                            <li>Horizontal gradient</li>
                            <li>Vertical gradient</li>
                            <li>Edge detection</li>
                            <li>Erosion</li>
                            <li>Dilation</li>
                            <li>Gamma Filter</li>
                            <li>Dot transformation</li>
                            <li>Dash transformation</li>
                        </ul>
                    <li>Noise Simulator</li>
                        <ul>
                            <li>White noise</li>
                            <li>Salt and pepper noise</li>
                            <li>Gaussian noise</li>
                        </ul>
                    <li>Encryption</li>
                        <ul>
                            <li>Pixelation</li>
                            <li>Random Key Row Shift Encryption</li>
                            <li>Line shift encryption with fixed key</li>
                            <li>Decryption</li>
                            <li>Inserting a secret image</li>
                            <li>Inserting a secret text</li>
                            <li>Puzzle</li>
                        </ul>
                    <li>Image overlay</li>
                        <ul>
                            <li>Red, green, blue, white, black and tinted background</li>
                            <li>image overlay</li>
                            <li>Anaglyphs</li>
                            <li>Image overlay</li>
                        </ul>
                    <li>Format change</li>
                        <ul>
                            <li>Monochrome</li>
                            <li>Index8</li>
                            <li>ARGB32</li>
                            <li>Grayscale8</li>
                            <li>Image size reduction</li>
                        </ul>
                    <li>Development of new functions</li>
                        <ul>
                            <li>Color TV pattern</li>
                            <li>Black and white TV pattern</li>
                            <li>Hexadecimal code of the image</li>
                            <li>Histogram</li>
                            <li>Sandbox functions</li>
                        </ul>
                </ul>
        <h2>Limitation:</h2>
            <p>This application only supports images:</p>
            <ul>
                <li>in jpg or png format</li>
                <li>modest size</li>
                <li>4-byte RGBA format</li>
            </ul>
        <h2>Installation</h2>
            <h3>Operating Systems:</h3>
            <p>This program runs on:</p>
                <li>Linux (Ubuntu)</li>
                <li>Windows 10 and 11</li>
            <h3>Interpreter Python:</h3>
            <p>Python3.13</p>
            <h3>Python Packages :</h3>
            <ul>
                <li>Pyside6</li>
                <li>Numpy</li>
                <li>Matplotlib</li>
                <li>Cython</li>
                <li>PyBind11 (on Linux only)</li>
                <li>Qimage2ndarray</li>
                <li>Setuptools</li>
            </ul>
            <p>For more information, see requirements.txt</p>
    </body>
</html>
