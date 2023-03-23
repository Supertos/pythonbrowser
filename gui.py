#----------------------------------------------------#
# *Python browser
# network.py
#----------------
# Loads resources, stores and caches them
#----------------------------------------------------#
import pygame as pg
import render

canvas = None
#----------------------------------------------------#
# *redrawMenu
# redraws GUI elements
def redrawMenu():

    global canvas

    css_box = render.box( {} )
    css_box.autoForText( "Privet-medved", 9 )
    css_box.border = ( 10, 0, 10, 0 )

    bottom_bar = pg.Surface((640, 32))
    bottom_bar.fill((255, 150, 150))

    pixarr = pg.PixelArray(bottom_bar)
    for y in range(32):
        for x in range(640):
            pixarr[x, y] = (255, 150 - y * 2, 150 - y * 2)
    pixarr.close()

    canvas.blit(css_box.render(), (128, 128))
    canvas.blit(bottom_bar, (0, 480-32))

    pg.display.flip()

#----------------------------------------------------#
# *runWindow
# starts window
def runWindow():
    global canvas
    canvas = pg.display.set_mode( ( 640, 480 ) )
    pg.display.set_caption( "Supertos Browser" )
    pg.display.set_icon( pg.image.load("icon.png") )
    canvas.fill( (255,255,255) )

#----------------------------------------------------#
# *fetchEvents
# fetches events
def fetchEvents():
    while True:
        ev = pg.event.poll()
        if ev.type == pg.NOEVENT:
            break
        elif ev.type == pg.QUIT:
            quit()