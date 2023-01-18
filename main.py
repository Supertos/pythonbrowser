import url
import time
import parse
import gui

url.openURL("www.youtube.com")
url.startLoadURL("/")

endtime = time.time() + 1

data = str(url.readURL())
data = data[2:len(data)-1]

res = parse.parseString( data )


from pprint import pprint

data = parse.treeBuild( res )

#import pprint

#pprint.pprint( data )


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
    res = parse.parseString(pr)
    data = parse.treeBuild(res)
    root = gui.Root()
    root.geometry('320x240')
    # root.attributes("-fullscreen", True)
    # root.attributes("-zoomed", True)
    root.renderTag(data[1])
    root.mainloop()