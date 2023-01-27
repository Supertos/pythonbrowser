import url
import time
import parse
import gui
import pygame as pg
url.openURL("www.google.com")
url.startLoadURL("/")

def stringHTMLConvert( str ):
    last_pos = 0
    while str.find( "&#", last_pos ) != -1:
        start = str.find("&#", last_pos)+2
        id = 0
        unicode_id = ""
        for pos in range( start, len(str) ):
            char = str[ pos ]
            if char == ";" or pos == len(str)-1:
                if unicode_id != "" and char == ";":
                    str = str[:start-2] + chr( int(unicode_id ) ) + str[pos+1:len(str)]
                last_pos = start-1
                break
            else:
                try:
                    val = int( char )
                    unicode_id = unicode_id + char
                except ValueError:
                    last_pos = start-1
                    break
    return str

print( stringHTMLConvert( "&#1055;&#1056;" ))
endtime = time.time() + 1
data = url.readURL().decode('utf-8')
data = stringHTMLConvert( data )
res = parse.parseString( data )



data = parse.treeBuild( res )




def getTagText( tag ):
    if 'inner' not in tag or tag['name'] == 'script' or tag['name'] == 'style' : return ""
    text = ""
    for el in tag['inner']:
        if isinstance( el, str ):
            text = text + el
        else:
            text = text + getTagText( el )+"\n"
    return text
def renderTags( tags ):
    surf = pg.Surface( (240, 320-24) )
    surf.fill( (255,255,255) )
    font = pg.font.init()
    font = pg.font.SysFont('arial', 11)
    fonth1 = pg.font.SysFont('arial', 32)
    fonth2 = pg.font.SysFont('arial', 24)
    y = 0
    for tag in tags:
        txt = getTagText( tag )
        data = txt.split("\n")
        size = 11
        if tag['name']=="h1":
            size = 32
        elif tag['name'] == "h2":
            size = 24
        for el in data:
            img = None
            if size == 11:
                img = font.render(el, True, (0, 0, 0))
            elif size == 24:
                img = fonth2.render( el, True, (0,0,0) )
            elif size == 32:
                img = fonth1.render( el, True, (0,0,0) )

            if el.replace(" ", "")!="":
                surf.blit( img, (0, y) )
                y += 1+size
    return surf

TagSurf = None
if __name__ == "__main__":
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
                        <h2>Home<h2>
                        <p>Have a <b>nice</b> day! </p>
                    <body>
                </html> """
    #res = parse.parseString(pr)
    #data = parse.treeBuild(res)



pg.init()

TagToSize = {}
TagToSize['p'] = 9
TagToSize['div'] = 9
TagToSize['h1'] = 18
TagToSize['h2'] = 16
TagToSize['h3'] = 14
TagToSize['h4'] = 12
TagToSize['h5'] = 11

def renderTag( Tag, ParentData ):
    global TagToSize
    import io
    if 'inner' not in Tag :
        if Tag['name'] == 'img':
            print("Tried to load img!", Tag['params']['src'] )
            url.startLoadURL( "/"+Tag['params']['src'] )
            endtime = time.time() + 1
            while time.time() < endtime:
                pass
            f = io.BytesIO(url.readURL())
            img = pg.image.load( f )
            w, h = img.get_size()
            w = w*0.4
            h = h*0.4

            img = pg.transform.scale( img, (w,h))
            surf = pg.Surface((w,h), flags=pg.SRCALPHA)
            surf.blit( img, (0,0))
            return surf
        else:
            return pg.Surface((0, 0), flags=pg.SRCALPHA)
    elif Tag['name'] == 'head': return pg.Surface( (0,0), flags=pg.SRCALPHA )
    elif Tag['name'] == 'script': return pg.Surface( (0,0), flags=pg.SRCALPHA )
    elif Tag['name'] == 'style': return pg.Surface( (0,0), flags=pg.SRCALPHA )
    pg.font.init()
    Surfaces = []

    MyParentData = ParentData
    if Tag['name'] in TagToSize:
        MyParentData['TextSize'] = TagToSize[Tag['name']]

    MyFont = None
    if 'TextSize' in MyParentData:
        MyFont = pg.font.SysFont('arial', MyParentData['TextSize'])
    else:
        MyFont = pg.font.SysFont('arial', 11)
    w, h = 240, 0
    cur_w = 0
    for el in Tag['inner']:
        if isinstance( el, str ):
            datas = el.split("\n")
            for line in datas:
                if line != "":
                    Surfaces.append( MyFont.render(line, True, (0,0,0)) )
                    print( "\"", line, "\"" )
        else:
            surf = renderTag(el, MyParentData)

            if len(Surfaces) > 0 and el['name'] == "b":
                merge_surf = pg.Surface( ( surf.get_width()+Surfaces[-1].get_width(), surf.get_height()+Surfaces[-1].get_height() ), flags=pg.SRCALPHA )
                merge_surf.fill((0,0,0,0))
                merge_surf.blit( Surfaces[-1], (0,0) )
                merge_surf.blit( surf, (Surfaces[-1].get_width(),0) )
                Surfaces[-1] = merge_surf
            else:
                Surfaces.append( surf )


    x, y = 0, 0
    for el in Surfaces:
        h += el.get_height()+2
    MySurf = pg.Surface( ( w, h ), flags=pg.SRCALPHA )
    MySurf.fill( (255,255,255, 255) )
    for el in Surfaces:

        MySurf.blit( el, (x, y) )
        y = y + el.get_height() + 2
        #x = x + el.get_width()

    return MySurf


Renders = []
w, h = 0, 0
for el in data:
    a = renderTag(el, {})
    Renders.append( a )
    w = max( w, a.get_width() )
    h = h + 2 + a.get_height()
TagSurf = pg.Surface( (w, h ), flags=pg.SRCALPHA)
y = 0
for el in Renders:
    TagSurf.blit( el, ( 0, y ) )
    y += el.get_height() + 2
TagSurf.fill( (0,0,0,0))
TagSurf.blit( Renders[0], ( 0, 0 ) )


Scr = pg.display.set_mode( (240,320) )
pg.display.set_caption("Bowser mini")

cursor = pg.image.load("src/cursor.png")
rect = cursor.get_rect( size=(8,8) )
BottomBar = pg.Surface( (240, 24) )
BottomBar.fill( (255,150,150) )

pixarr = pg.PixelArray( BottomBar )
for y in range( 24 ):
    for x in range( 240 ):
        pixarr[ x, y ] = (255, 150-y*2, 150-y*2)
pixarr.close()

Scr.blit( BottomBar, (0, 320-24 ) )
Scr.fill( (255,255,255) )
c_pos = (0,0)



virtual_y = 0

while True:
    while True:
        ev = pg.event.poll()
        if ev.type == pg.NOEVENT:
            break
        elif ev.type == pg.QUIT:
            quit()

    x, y = c_pos
    if pg.key.get_pressed()[pg.K_UP]:
        y = max( 0, y - 0.05 )
        if y == 0:
            virtual_y = virtual_y + 0.05

    elif pg.key.get_pressed()[pg.K_DOWN]:
        y = min( 320, y + 0.05 )
        if y >= 320:
            virtual_y = virtual_y - 0.05

    if pg.key.get_pressed()[pg.K_RIGHT]:
        x = min( 240, x + 0.05 )
    elif pg.key.get_pressed()[pg.K_LEFT]:
        x = max( 0, x - 0.05 )

    c_pos = (x, y)
    Scr.fill( (255,255,255, 0) )
    #if TagSurf:
    Scr.blit( Renders[0], (0,virtual_y) )
    Scr.blit( cursor, c_pos, (12,0,12, 14) )
    Scr.blit( BottomBar, (0, 320-24 ) )


    pg.display.flip()