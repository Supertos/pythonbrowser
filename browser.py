#----------------------------------------------------#
# *Python browser
# network.py
#----------------
# Loads resources, stores and caches them
#----------------------------------------------------#
import gui
import network
import storage
gui.runWindow()

storage.openURL( "www.google.com" )
#storage.openURL( "www.python.org" )

while True:
    gui.fetchEvents()
    network.fetchQueue()
    gui.redrawMenu()


