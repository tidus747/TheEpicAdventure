#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Ivan Rodriguez (c) 2018
'''

import math
import numpy as np
import cv2
from matplotlib import pyplot as plt

# Definiciones
cos_30 = math.cos(math.radians(30))
sin_30 = math.sin(math.radians(30))
tan_30 = math.tan(math.radians(30))

perspectives = ["to_top","to_left","to_right","from_top","from_left","from_right"]

# Definimos las transformaciones posibles
transformations = {
        # From 2D to isometric top down view:
        #   * scale vertically by cos(30°)
        #   * shear horizontally by -30°
        #   * rotate clock-wise 30°
        'to_top':       [[cos_30,       -cos_30,    0],
                         [sin_30,       sin_30,     0]],

        # From 2D to isometric left-hand side view:
        #   * scale horizontally by cos(30°)
        #   * shear vertically by -30°
        'to_left':      [[cos_30,       0,          0],
                         [sin_30,       1,          0]],

        # From 2D to isometric right-hand side view:
        #   * scale horizontally by cos(30°)
        #   * shear vertically by 30°
        'to_right':     [[cos_30,       0,          0],
                         [-sin_30,      1,          0]],

        # From isometric top down view to 2D:
        #   * rotate counter-clock-wise 30°
        #   * shear horizontally by 30°
        #   * scale vertically by 1 / cos(30°)
        'from_top':     [[tan_30,       1,          0],
                         [-tan_30,      1,          0]],

        # From isometric left-hand side view to 2D:
        #   * shear vertically by 30°
        #   * scale horizontally by 1 / cos(30°)
        'from_left':    [[1 / cos_30,   0,          0],
                         [-tan_30,      1,          0]],

        # From isometric right-hand side view to 2D:
        #   * shear vertically by -30°
        #   * scale horizontally by 1 / cos(30°)
        'from_right':   [[1 / cos_30,   0,          0],
                         [tan_30,       1,          0]]
}

def increaseBorders(tile):
    """Funcion para aumentar la imagen manteniendo el tile en el centro.

    Keyword arguments:
    tile -- que se pretende copiar en una imagen de mayor tamaño.
    """
    y,x,ch = tile.shape
    new_tile = np.zeros([y*5,x*5,ch]).astype("uint8")

    new_tile[y*2:tile.shape[0]+y*2,x*2:tile.shape[1]+x*2,:] = tile[:,:,:]

    return new_tile

def isofrom2d(tile_2d,trans_string):
    """Funcion para generar un tile en isométrico a partir de un tile 2d.

    Keyword arguments:
    tile_2d -- que se pretende convertir a isométrico.
    """
    rows,cols,ch = tile_2d.shape

    return cv2.warpAffine(tile_2d,np.array(transformations[trans_string]),(cols,rows))

def drawTransformations(tile_2d):
    """Funcion para generar las posibles proyecciones de un tile 2d en isométrico.

    Keyword arguments:
    tile_2d -- que se pretende convertir a isométrico.
    """
    total = len(perspectives) # Número de subplots que queremos añadir
    columnas = 3 # Número de columnas de la figura

    filas = total // columnas
    filas += total % columnas

    position = range(1, total + 1) # Índice para el control de posición de los subplots

    fig = plt.figure(1)

    for x in range(total):
        tile_2d_grande = increaseBorders(tile_2d)
        imagen = isofrom2d(tile_2d_grande,perspectives[x])
        ax = fig.add_subplot(filas,columnas,position[x])
        ax.imshow(imagen[:,:,[2,1,0]])
        ax.set_title(perspectives[x])

    plt.show()

    return 0
