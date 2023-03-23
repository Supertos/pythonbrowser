# ----------------------------------------------------#
# *Python browser
# storage.py
# ----------------
# Does storaging
# ----------------------------------------------------#

import css
import html
import network
import io

canvases = []
resources = {}

#-----------------------------------------------------#
# *getResource
# Loads resource
def getResource( name ):
    global resources
    if name not in resources: return None

    ext = name.split(".")[-1] # Get extension
    if ext == "html" or ext == "htm" or ext == "js" or ext == "php" or ext == "css": # For thee we'll return StringIO
        return io.StringIO( resources[name][0].decode('utf-8') )
    else:
        return io.BytesIO( resources[name][0] ) # For thee bytes will be enough!

#-----------------------------------------------------#
# *getResource
# Loads resource
def pushResource( path, data ):
    global resources
    global canvases
    resources[ path ] = data

    for canvas in canvases:
        if path in canvas.dependencies:
            canvas.onResourceLoad( path )

#---------------------------------------------------------------#
# *Canvas
# This class handles web resource content
class Canvas:
    def __init__( self ):

        self.html = None
        self.css = []
        self.js = []
        self.dependencies = []

    def loadURL( self, url ):
        network.startConnection( url )
        self.dependencies.append( url+"/index.html" )
        network.downloadResource( "/" )

    def onResourceLoad(self, name):
        ext = name.split(".")[-1] # Get extension
        if ext == "html" or ext == "htm":
            self.html = html.processHTML( getResource(name).read() )
            if "style" in self.html.types:
                for tagid in self.html.types["style"]:
                    tag = self.html.tags[ tagid ]
                    data = css.parseCSS(tag.content[0])
                    tag.content[0] = len( self.css )

                    self.css.append(data)

            if "script" in self.html.types:
                for tagid in self.html.types[ "script" ]:
                    tag = self.html.tags[ tagid ]
                    data = tag.content[0]
                    tag.content[0] = len( self.js )
                    #self.js.append( data )

            self.html.debug()
            for css_file in self.css:
                self.html.applyCSS( css_file )

#-----------------------------------------------------#
# *openURL
# Opens URL
def openURL( url ):
    global canvases
    canvas = Canvas()
    canvases.append( canvas )
    canvas.loadURL( url )
    return canvas
