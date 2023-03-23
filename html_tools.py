#----------------------------------------------------#
# *Python browser
# html_tools.py
#----------------
# Removes unwanted html quirks
#----------------------------------------------------#

ent_to_char = {
    "nbsp": " ",
    "lt": "<",
    "gt": ">",
    "amp": "&",
    "quot": "\"",
    "apos": "'",
    "cent": "¢",
    "pound": "£",
    "yen": "¥",
    "euro": "€",
    "copy": "©",
    "reg": "®"
}

#---------------------------------------------#
# *removeSpaces( html source )
# Removes trash from html source
def removeSpaces( html ):
    global ent_to_char
    # Remove spaces
    html = html.replace( "\n", "" )
    while html.find( "  " ) != -1:
        html = html.replace( "  ", " " )
    return html

#---------------------------------------------#
# *replaceHTMLEnts( html source )
# Replaces HTML entities to ready-to-process-code
def replaceHTMLEnts( html ):
    pos = 0
    while pos < len( html ):
        pos = html.find( "&", pos )
        if pos == -1: return html
        semicolon_pos = html.find( ";", pos )
        data = html[ pos:(semicolon_pos) ]

        if semicolon_pos == -1:
            pos += 1
        else:
            new_data = ""
            #Handle data
            if data[0] == "#":
                new_data = chr( data[1:] )
            elif data in ent_to_char:
                new_data = ent_to_char[ data ]
            else:
                new_data = data
            html = html[ 0:pos ] + new_data + html[ semicolon_pos+1:len( html )]
    return html