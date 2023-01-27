import pygame as pg

pg.font.init()

textFonts = {}

textTags = {}
textTags[ 'h1' ] = { 'font-size': 24 }
textTags[ 'h2' ] = { 'font-size': 20 }
textTags[ 'h3' ] = { 'font-size': 18 }
textTags[ 'h4' ] = { 'font-size': 16 }
textTags[ 'h5' ] = { 'font-size': 14 }
textTags[ 'h6' ] = { 'font-size': 12 }

textTags[ 'b' ] = { 'font-weight':'bold' }
textTags[ 'i' ] = { 'font-style':'italic'}
textTags[ 'div' ] = { 'font-size': 11 }
textTags[ 'p' ] = { 'font-size': 11 }




class HTMLTag:
    def __init__(self):
        self.type = ''
        self.parameters = {}
        self.content = []
        self.render = {}

    def add(self, content):
        self.content.append( content )
    def addMod(self, name, val):
        self.parameters[ name ] = val

    def hasMod(self, name):
        return name in self.parameters

    def setMod(self, name):
        self.parameters[ name ] = True

    def getMod(self, name):
        return self.parameters[ name ]

    def setType(self, type):
        global textTags
        self.type = type
        if type in textTags:
            for key, val in textTags[type].items():
                self.render[ key ] = val

    def isTypeOf(self, type):
        return self.type == type

    def getType(self):
        return self.type

    def textPrepRender(self, **render_parameters):

        myTextData = []
        myStyle = self.render.copy()
        if render_parameters:
            for key, val in enumerate(render_parameters):
                myStyle[key] = val

        if 'font-size' not in myStyle: myStyle['font-size'] = 9
        if 'font-style' not in myStyle: myStyle['font-style'] = 'normal'
        if 'font-weight' not in myStyle: myStyle['font-weight'] = 'normal'
        if 'font-family' not in myStyle: myStyle['font-family'] = 'arial'

        for element in self.content:
            if isinstance( element, str ): # This is just a string!
                myTextData.append( ( element, myStyle ) )
            else: # This is a tag
                myTextData = myTextData + element.textPrepRender( render_parameters=myStyle )

        return myTextData

    def textSplitRender( self, textData ):
        newTextData = []

        max_w = 240
        w = max_w
        for text, style in textData:
            charSize = int(style['font-size']*0.6)
            stringLen = charSize*len( text )
            if stringLen > w:
                charsPerLine = max_w // charSize
                lines = len(text)//charsPerLine
                lastLineSize = len(text)%charsPerLine*charSize
                if len(text)%charsPerLine !=  0: lines += 1
                for i in range( lines+1 ):
                    newStyle = style.copy()
                    newStyle['new_x'] = 0
                    if i == lines:
                        newStyle['new_x'] = lastLineSize
                    newTextData.append( (text[ i*charsPerLine : min( len( text ), i*charsPerLine+charsPerLine ) ], newStyle) )

                w = max_w - w % stringLen
            else:
                newStyle = style.copy()
                w = w - stringLen
                newStyle['new_x'] = max_w-w
                newTextData.append( (text, newStyle) )
        return newTextData

    def textRender(self, textData):
        global textFonts
        w = 240
        h = 0
        for text, style in textData:
            h += style['font-size']+2

        mySurface = pg.Surface( ( w, h ), flags=pg.SRCALPHA)
        mySurface.fill( (255,255,255, 0))

        x, y = 0, 0
        for text, style in textData:
            realFontName = style['font-family'] + str( style['font-size'] )
            if realFontName not in textFonts:
                textFonts[realFontName] = pg.font.SysFont( style['font-family'], style['font-size'] )

            if isinstance( style['font-weight'], str ) and style['font-weight'] == "bold" or isinstance( style['font-weight'], int ) and style['font-weight'] > 0:
                textFonts[realFontName].set_bold( True )
            else:
                textFonts[realFontName].set_bold( False )


            if style['font-style'] == "italic":
                textFonts[realFontName].set_italic( True )
            else:
                textFonts[realFontName].set_italic( False )

            appendSurf = textFonts[realFontName].render( text, True, (0,0,0) )

            mySurface.blit( appendSurf, (x, y))
            if style['new_x'] == 0:
                x = 0
                y = y + style['font-size']+2
            else:
                x = style['new_x']
        return mySurface


tag = HTMLTag()
tag.setType("p")

tag.add("Have a ")

innerTag = HTMLTag()
innerTag.setType("b")
innerTag.add("nice")
tag.add(innerTag)

tag.add(" day!")


disp = pg.display.set_mode( (240, 320))
disp.fill((255,255,255))
disp.blit( tag.textRender( tag.textSplitRender( tag.textPrepRender())), (0,0))
pg.display.flip()

while True:
    pg.display.flip()


