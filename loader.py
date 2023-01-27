#---------------------------------------------------------#
# Python Browser
#---------------------------------------------------------#
# Year: 2023
# Ver: rev 1
#---------------------------------------------------------#
import http.client as hcli
queue = []
loaded = {}
main_connection = None
mode = 1 # 1 - HTTPS 0 - HTTP

def startConnection( url ):
    global main_connection

    if isinstance(main_connection, hcli.HTTPConnection ) or isinstance(main_connection, hcli.HTTPSConnection ):
        main_connection.close()

    if mode == 1:
        main_connection = hcli.HTTPSConnection( url )
    else:
        main_connection = hcli.HTTPConnection( url )


def endConnection():
    global main_connection
    if isinstance(main_connection, hcli.HTTPConnection) or isinstance(main_connection, hcli.HTTPSConnection):
        main_connection.close()

def load( url: str="/" ):
    global main_connection
    global queue
    main_connection.request( "GET", url )
    queue.append( ( main_connection.getresponse(), url))

def doQueue():
    global queue
    global loaded
    pos = 0
    while pos < len(queue):
        request, file = queue[ pos ]
        if request.status == 0 or request.status == 1:
            pos += 1
        else:
            loaded[ file ] = ( request.read(), request.status, request.reason)
            del queue[ pos ]
startConnection("www.google.com")
load()


while True:
    doQueue()