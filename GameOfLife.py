import os.path

import pygame
import numpy
import time
import sys
from screeninfo import get_monitors

#Tamaño Ventana
altoMonitor = get_monitors()[0].height
tamano = int(altoMonitor * 0.90)

width = tamano
height = tamano
pygame.display.set_mode((width, height))


# Ruta para los archivos de recursos al ejecutar
try:
    ruta_base = sys._MEIPASS
except Exception:
    ruta_base = os.path.abspath(".")
ruta = os.path.join(ruta_base, "logo.png")

pygame.display.set_icon(pygame.image.load(ruta))

pygame.display.set_caption("Game of Life - John Conway")
#Control de la ejecución
pausa = True

#Color
colorBg = 25, 25, 25
colorCelulas = 255, 255, 255
colorRejilla = 50, 50, 50

colorBgP = 5, 5, 5
colorCelulasP = 235, 235, 235
colorRejillaP = 30, 30, 30

coloresStart = [colorBg, colorCelulas, colorRejilla]
coloresPausa = [colorBgP, colorCelulasP, colorRejillaP]

colorJuego = [coloresStart, coloresPausa]
colorActual = colorJuego[pausa]

#Velocidad
delay = 0.1


#Celdas
numCX = int(tamano/15)
numCY = int(tamano/15)


dimCW = width/numCX
dimCH = height/numCY

#Estado de las celdas. Viva = 1, Muerta = 0
#Rellena de ceros la matriz estadoJuego
estadoJuego = numpy.zeros((numCX, numCY))


pygame.init()
screen = pygame.display.set_mode((height, width))
screen.fill(colorActual[0])


#Bucle de ejecución
while True:

    recalculoEstadoJuego = numpy.copy(estadoJuego)

    #Limpia la pantalla para que no se superpongan las iteraciones
    screen.fill(colorActual[0])
    time.sleep(delay)

    #Eventos teclado y ratón
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                pausa = not pausa
                colorActual = colorJuego[pausa]


        clickRaton = pygame.mouse.get_pressed()
        if sum(clickRaton) > 0:
            posX, posY = pygame.mouse.get_pos()
            #Cálculo de celda clickada
            celX, celY = int(numpy.floor(posX/ dimCW)), int(numpy.floor(posY/ dimCH))
            recalculoEstadoJuego[celX, celY] = clickRaton[0]

    for y in range(0, numCY):
        for x in range(0, numCX):

            if not pausa:
                #Cálculo de vecinos
                numVecinos = estadoJuego[(x+1) % numCX, (y+1) % numCY] + \
                             estadoJuego[(x+1) % numCX, (y)   % numCY] + \
                             estadoJuego[(x+1) % numCX, (y-1) % numCY] + \
                             estadoJuego[(x)   % numCX, (y-1) % numCY] + \
                             estadoJuego[(x-1) % numCX, (y-1) % numCY] + \
                             estadoJuego[(x-1) % numCX, (y)   % numCY] + \
                             estadoJuego[(x-1) % numCX, (y+1) % numCY] + \
                             estadoJuego[(x)   % numCX, (y+1) % numCY]

                #Regla 1: Una célula con 3 vecinas vivas REVIVE
                if estadoJuego[x, y] == 0 and numVecinos == 3:
                    recalculoEstadoJuego[x, y] = 1

                #Regla 2: Una célula con menos de 2 o mas de 3 vecinas vivas MUERE
                elif estadoJuego[x, y] == 1 and (numVecinos < 2 or numVecinos > 3):
                    recalculoEstadoJuego[x, y] = 0




            #Poligono a dibujar
            coorPoly = [ (x     * dimCW,   y    * dimCH),
                        ((x+1)  * dimCW,   y    * dimCH),
                        ((x+1)  * dimCW,  (y+1) * dimCH),
                        ( x     * dimCW,  (y+1) * dimCH)]

            #Dibuja la rejilla
            if recalculoEstadoJuego[x, y] == 0:
                pygame.draw.polygon(screen, colorActual[2], coorPoly, pausa)
            elif recalculoEstadoJuego[x, y] == 1:
                pygame.draw.polygon(screen, colorActual[1], coorPoly, 0)

    #Actualizamos el estado del juego
    estadoJuego = numpy.copy(recalculoEstadoJuego)

    #Actualiza pantalla
    pygame.display.flip()