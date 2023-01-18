import http.client as hcli
Connection = None
Response = None

def openURL( url: str ) -> None:
    global Connection
    if isinstance(Connection, hcli.HTTPSConnection ):
        Connection.close()
    Connection = hcli.HTTPSConnection( url )

def startLoadURL( url: str="/index.html" ):
    global Connection
    global Response
    Connection.request( "GET", url )
    Response = Connection.getresponse()

def readURL():
    global Response
    print( Response.status, Response.reason )
    return Response.read()