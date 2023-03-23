#----------------------------------------------------#
# *Python browser
# network.py
#----------------
# Loads resources, stores and caches them
#----------------------------------------------------#
import http.client as http
import io
import storage

main_connection:http.HTTPSConnection = None
url = ""

load_queue = []
resources = {}
#----------------------------------------------------#
# *startConnection
# Starts connection to internet resource
def startConnection( site ):
    global main_connection
    global url
    url = site
    if main_connection is not None:
        main_connection.close()
        main_connection = None
    main_connection = http.HTTPSConnection( site, timeout=2 )


#----------------------------------------------------#
# *downloadResource
# Starts resource download
def downloadResource( path ):
    global main_connection
    global load_queue
    global url

    main_connection.request( "GET", path )
    if path == "/": path = "/index.html"
    load_queue.append( ( main_connection.getresponse(), url+path ))

#-----------------------------------------------------#
# *fetchQueue
# Checks download queue for newly downloaded file
def fetchQueue():
    global load_queue
    global resources

    pos = 0
    while pos < len( load_queue ):
        request, file = load_queue[ pos ]
        if request.status == 0 or request.status == 1:
            pos += 1
        else:
            storage.pushResource( file, ( request.read(), request.status, request.reason ) )
            del load_queue[ pos ]

