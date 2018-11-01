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

import numpy as np
from matplotlib import pyplot as plt
import os
import pandas as pd
import cv2
import random

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
RESOURCES_PATH = "../../Individual/"

LISTA_DE_RECURSOS = ['Columnas','Puertas','Bordes','Esquinas','Suelos','Banderas','Misc']

BACKGROUND_H = 608
BACKGROUND_W = 1024
TILE_SIZE = 16

def check_column_elements(data):
    """Funcion para comprobar los recursos disponibles en la columna.

    Keyword arguments:
    data -- datos leídos por Pandas, hay que introducir la columna que
    estamos buscando para poder guardarla.
    """
    lista = list(data.values)
    is_null = list(data.isnull())
    list_elements = []

    for i in range(len(lista)):
        if (is_null[i] == False):
            list_elements.append(lista[i])

    return list_elements


def load_resources(data):
    """Funcion para buscar los recursos por medio de una palabra clave.

    Keyword arguments:
    data_column -- datos leídos por Pandas, hay que introducir la columna que
    estamos buscando para poder guardarla.
    """
    list_elements = check_column_elements(data)
    tiles = np.zeros((16,16,3,len(list_elements))).astype('uint8')

    for i in range(len(list_elements)):
        tiles[:,:,:,i] = cv2.imread(RESOURCES_PATH+list_elements[i])

    return tiles

def fill_floor(floor_tiles,background):
    """Funcion para rellenar automáticamente el suelo.

    Keyword arguments:
    floor_tiles -- imágenes a colocar en el suelo.
    background -- imagen de fondo sobre la que se va a trabajar.
    """
    for x in range(0,BACKGROUND_W,TILE_SIZE):
        for y in range(0,BACKGROUND_H,TILE_SIZE):
            background[y:y+TILE_SIZE,x:x+TILE_SIZE,:] = floor_tiles[:,:,:,0]

            # Generamos un número aleatorio para poder añadir el suelo personalizado
            suelo = random.randint(1,100)
            if ( suelo < 8 ):
                background[y:y+TILE_SIZE,x:x+TILE_SIZE,:] = floor_tiles[:,:,:,suelo]

    return background

def fill_walls(wall_tiles,background):
    """Funcion para rellenar automáticamente los muros de los bordes.

    Keyword arguments:
    wall_tiles -- imágenes a colocar en los muros.
    background -- imagen de fondo sobre la que se va a trabajar.
    """
    for x in range(TILE_SIZE,BACKGROUND_W-TILE_SIZE,TILE_SIZE):
        background[0:0+TILE_SIZE,x:x+TILE_SIZE,:] = wall_tiles[:,:,:,4]

    for y in range(0,BACKGROUND_H,TILE_SIZE):
        background[y:y+TILE_SIZE,0:0+TILE_SIZE,:] = wall_tiles[:,:,:,6]

    return background

def fill_borders(borders_tiles,background):
    """Funcion para rellenar automáticamente los bordes de la pantalla.

    Keyword arguments:
    border_tiles -- imágenes a colocar en los bordes.
    background -- imagen de fondo sobre la que se va a trabajar.
    """


    return background


#os.chdir(RESOURCES_PATH)
data = pd.read_csv("resources.csv")

# Cargamos todos los recursos disponibles
tiles_Columnas = load_resources(data[LISTA_DE_RECURSOS[0]])
tiles_Bordes = load_resources(data[LISTA_DE_RECURSOS[2]])
tiles_Esquinas = load_resources(data[LISTA_DE_RECURSOS[3]])
tiles_Suelos = load_resources(data[LISTA_DE_RECURSOS[4]])
tiles_Banderas = load_resources(data[LISTA_DE_RECURSOS[5]])
tiles_Misc = load_resources(data[LISTA_DE_RECURSOS[6]])

# Generamos el mapa vacío
background = np.zeros((BACKGROUND_H,BACKGROUND_W,3)).astype('uint8')

# Generamos el suelo
background = fill_floor(tiles_Suelos,background)

# Generamos los muros
background = fill_walls(tiles_Esquinas,background)
