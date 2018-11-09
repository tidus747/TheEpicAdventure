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
from scipy.ndimage import rotate

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
RESOURCES_PATH = "../../Individual/"

LISTA_DE_RECURSOS = ['Columnas','Puertas','Bordes','Esquinas','Suelos','Banderas','Misc']

BACKGROUND_H = 608
BACKGROUND_W = 1024
TILE_SIZE = 16
WALL_MARGIN = 16

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


def load_resources(data, size_x = 16, size_y = 16):
    """Funcion para buscar los recursos por medio de una palabra clave.

    Keyword arguments:
    data_column -- datos leídos por Pandas, hay que introducir la columna que
    estamos buscando para poder guardarla.
    size_x -- ancho del tile.
    size_y -- alto del tile.
    """
    list_elements = check_column_elements(data)
    tiles = np.zeros((size_y,size_x,3,len(list_elements))).astype('uint8')

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

def fill_walls(bg,wall_tiles_up=None,wall_tiles_bot =None, wall_tiles_left =None, wall_tiles_right=None):
    """Funcion para rellenar automáticamente los muros de los bordes.

    Keyword arguments:
    wall_tiles -- imágenes a colocar en los muros.
    background -- imagen de fondo sobre la que se va a trabajar.
    """
    # Muros de la parte superior
    if (type(wall_tiles_up) == np.ndarray):
        for x in range(TILE_SIZE,BACKGROUND_W-TILE_SIZE,TILE_SIZE):
            bg[WALL_MARGIN:WALL_MARGIN+TILE_SIZE,x:x+TILE_SIZE,:] = wall_tiles_up

    if (type(wall_tiles_bot) == np.ndarray):
        for x in range(TILE_SIZE,BACKGROUND_W-TILE_SIZE,TILE_SIZE):
            bg[BACKGROUND_H-TILE_SIZE-WALL_MARGIN:BACKGROUND_H-WALL_MARGIN,x:x+TILE_SIZE,:] = wall_tiles_bot

    if (type(wall_tiles_left) == np.ndarray):
        for y in range(WALL_MARGIN,BACKGROUND_H,TILE_SIZE):
            bg[y:y+TILE_SIZE,0:0+TILE_SIZE,:] = wall_tiles_left

    if (type(wall_tiles_right) == np.ndarray):
        for y in range(WALL_MARGIN,BACKGROUND_H,TILE_SIZE):
            bg[y:y+TILE_SIZE,BACKGROUND_W-TILE_SIZE:BACKGROUND_W,:] = wall_tiles_right

    return background

def copy_image_alpha(image,dst):
    """Funcion para rellenar una imagen con otra con canal alpha.

    Keyword arguments:
    image -- imagen con canal alpha.
    background -- imagen de fondo sobre la que se va a trabajar.
    """

    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if (image[y,x,0] != 0 and image[y,x,1] != 0 and image[y,x,2] != 0):
                dst[y,x,:] = image[y,x,:]

    return dst

def put_misc(misc_tiles,background): # TODO Hay que añadir el wall margin
    """Funcion para rellenar automáticamente el escenario con miscelánea.

    Keyword arguments:
    misc_tiles -- imágenes a colocar en el escenario.
    background -- imagen de fondo sobre la que se va a trabajar.
    """
    repeticion = random.randint(1,10)
    for i in range(misc_tiles.shape[3]):
        for j in range(repeticion):
            pos_x = random.randint(TILE_SIZE,BACKGROUND_W-TILE_SIZE)
            pos_y = random.randint(TILE_SIZE,BACKGROUND_H-TILE_SIZE)

            copy_image_alpha(misc_tiles[:,:,:,i],background[pos_y:pos_y+TILE_SIZE,pos_x:pos_x+TILE_SIZE,:])
        repeticion = random.randint(1,10)

    return background

def fill_edges(edges_tiles, background):
    """Funcion para rellenar automáticamente los bordes de la pantalla.

    Keyword arguments:
    edges_tiles -- imágenes a colocar en los bordes de la pantalla.
    background -- imagen de fondo sobre la que se va a trabajar.
    """

    for x in range(0,BACKGROUND_W,TILE_SIZE):
        copy_image_alpha(edges_tiles[:,:,:,0],background[0:TILE_SIZE,x:x+TILE_SIZE,:])
        copy_image_alpha(rotate(edges_tiles[:,:,:,0],180,reshape=False),background[BACKGROUND_H-TILE_SIZE:BACKGROUND_H,x:x+TILE_SIZE,:])

    for y in range(0,BACKGROUND_H,TILE_SIZE):
        copy_image_alpha(rotate(edges_tiles[:,:,:,0],90,reshape=False),background[y:y+TILE_SIZE,0:TILE_SIZE,:])
        copy_image_alpha(rotate(edges_tiles[:,:,:,0],-90,reshape=False),background[y:y+TILE_SIZE,BACKGROUND_W-TILE_SIZE:BACKGROUND_W,:])

    return background

def put_door(door_tiles,pos_x,pos_y,background):
    """Funcion para colocar puertas en la escena.

    Keyword arguments:
    door_tiles -- imágenes de la puerta a colocar.
    background -- imagen de fondo sobre la que se va a trabajar.
    """
    copy_image_alpha(door_tiles[:,:,:,0],background[WALL_MARGIN-TILE_SIZE:(WALL_MARGIN-TILE_SIZE)+door_tiles[:,:,:,0].shape[0],BACKGROUND_W/2:BACKGROUND_W/2+door_tiles[:,:,:,0].shape[1],:])

    return background

#os.chdir(RESOURCES_PATH)
data = pd.read_csv("resources.csv")

# Cargamos todos los recursos disponibles
tiles_Columnas = load_resources(data[LISTA_DE_RECURSOS[0]])
tiles_Puerta = load_resources(data[LISTA_DE_RECURSOS[1]],size_x=32,size_y=32)
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
#background = fill_walls(background,wall_tiles_up=tiles_Esquinas[:,:,:,4],wall_tiles_right=tiles_Esquinas[:,:,:,6],wall_tiles_left=tiles_Esquinas[:,:,:,3])

# Colocamos la miscelánea
background = put_misc(tiles_Misc,background)

# Colocamos los bordes de la pantalla
#background = fill_edges(tiles_Bordes, background)

# Colocamos la puerta
#background = put_door(tiles_Puerta,background)

# Colocamos las columnas de los muros
