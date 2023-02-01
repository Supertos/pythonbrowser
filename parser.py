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
        self.isClosing = False

    def add(self, content):
        self.content.append( content )
    def addMod(self, name, val):
        if name == "": return
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


single_tags = [
        "area",
        "base",
        "br",
        "col",
        "command",
        "embed",
        "hr",
        "img",
        "input",
        "keygen",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
        "!DOCTYPE"
    ]


def isSingleTag( name ):
    global single_tags
    return name in single_tags


def parseTag( data: str ) -> HTMLTag:
    out = HTMLTag()
    endpos = len( data )-1
    #-------------------------------------------------#
    # TAG Parsing states:
    # 0 - Processing tagname
    # 1 - Processing modifier name
    # 2 - Awaiting = to appear
    # 3 - Processing modifier value
    # 4 - Processing modifier string

    state = 0
    string_endsymbol = ""

    saved_parameter = ""
    saved_name = ""
    for pos in range( len( data ) ):
        char = data[ pos ]

        if state == 0:
            if char == "/":
                out.isClosing = True

            elif char == ">" or char == " ":
                out.setType( saved_name )
                if isSingleTag( saved_name ): out.isClosing = True
                saved_name, state = "", 1

            elif pos == endpos:
                out.setType(saved_name+char)
                if isSingleTag( saved_name+char ): out.isClosing = True
                saved_name, state = "", 1

            elif char != "<":
                saved_name += char

        elif state == 1:
            if char == ">" or char == "/":
                out.addMod( saved_name, True )
                saved_name, state = "", 1

            elif pos == endpos:
                out.addMod( saved_name, True )
                saved_name, state = "", 1

            elif char == "=":
                state = 3

            elif char == " ":
                if saved_name != "":
                    state = 2

            else:
                saved_name += char

        elif state == 2:
            if char == "=":
                state = 3

            elif char != " ":
                out.addMod( saved_name, True )
                saved_name, state = char, 1

        elif state == 3:
            if char == "'" or char == "\"":
                string_endsymbol = char
                state = 4

            elif char == " " or char == ">" or char == "/":
                if saved_parameter != "":
                    out.addMod( saved_name, saved_parameter)
                    saved_parameter, saved_name, state = "", "", 1

            elif pos == endpos:
                out.addMod( saved_name, saved_parameter+char)
                saved_parameter, saved_name, state = "", "", 1
            else:
                saved_parameter += char

        elif state == 4:
            if char == string_endsymbol:
                out.addMod( saved_name, saved_parameter )
                saved_parameter, saved_name, state = "", "", 1
            else:
                saved_parameter += char

    return out

def isScriptTag( tag: HTMLTag ) -> bool:
    return not tag.isClosing and ( tag.type == "script" or tag.type == "style" )

def parseString( data: str ) -> list:

    out = []
    endpos = len( data )-1
    #-------------------------------------------------#
    # TAG Parsing states:
    # 0 - Processing plain text
    # 1 - Processing tag
    # 2 - Processing something alien
    state = 0

    saved_string = ""
    saved_code = ""
    prev_isScriptTag = False
    prev_tagtype = ""
    prev_tagIsClosing = Truess
    for pos in range( len( data ) ):
        char = data[ pos ]

        if state == 0:
            if char == "<":
                if not prev_tagIsClosing and saved_string != "": out.append( saved_string ) # Disallow out-of-tag text
                saved_string, state = "<", 1

            elif pos == endpos:
                out.append( saved_string )
            else:
                saved_string += char
        elif state == 1:
            if char == ">":
                saved_string += char
                tag = parseTag(saved_string)
                if prev_isScriptTag and tag.type != prev_tagtype: # This is not a closing tag for script tag!
                    state = 2
                    saved_code = saved_code + saved_string + char
                    saved_string = ""
                else:
                    if saved_string[0:4] != "<!--":
                        if prev_isScriptTag: out.append( saved_code )
                        out.append( tag )
                        prev_isScriptTag = isScriptTag( tag )
                        prev_tagtype = tag.type
                        prev_tagIsClosing = tag.isClosing
                        saved_string, state = "", 0
                        if prev_isScriptTag: state = 2
                    else:
                        saved_string, state = "", 0

            elif char == "<":   # We can't start tag twice! Certainly a script!
                saved_code = saved_code + saved_string
                saved_string = "<"
            else:
                saved_string += char

        elif state == 2:
            if char == "<":
                saved_string, state = "<", 1
            elif pos == endpos:
                saved_code += char
                saved_string, state = "<", 1
            else:
                saved_code = saved_code + char

    return out

pr = """
        <!-- This is a long commentary
        That is required to test how commentaries in this shitty HTML implementation work
        By the way i hate python -->

        <!DOCTYPE html>
                <html>
                    <head>
                        <title>Main page</title>
                        <script lang='js'>
                            let a = 1;
                            for( var i = 1; i<=10; i++ );
                            {
                                a = a + i;
                            }
                        </script>
                    </head>
                    <body>
                        <img href='gui/logo.png'> 
                        <h1>Welcome to my little page!</h1>
                        <h2>Home</h2>
                        <p>Have a <b>nice</b> day! </p>
                    </body>"""

a = parseString( pr )
for entr in a:
    if isinstance( entr , str):
        print( "String: ", entr )
    else:
        print("Tag: ", entr.type, entr.isClosing)
