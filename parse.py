

def parseTag( data:str ):
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

    state = 0
    out = {'params':{}, 'isClosing': False}
    saved_str = ""
    saved_strb = ""
    pos = -1
    endpos = len(data)-1
    endchar = ""
    last_char = ""
    for char in data:
        pos += 1
        if state == 0:  #Parse tag name
            if char == "/":
                out[ 'isClosing' ] = True
            elif char == " " or pos == endpos:
                if pos == endpos and char != " " and char != ">":
                    saved_str = saved_str + char
                out['name'] = saved_str
                out[ 'isSingle' ] = saved_str in single_tags

                state = 1
                saved_str = ""
            elif char != "<":
                saved_str = saved_str + char
        elif state == 1:    #Parse parameter name
            if char == "=":
                state = 2
            elif char != " " and last_char == " " or char == "/" or pos == endpos:
                if saved_str != "":
                    if char != "": saved_str = saved_str + char
                    out['params'][saved_str] = True
                    saved_str = ""
                saved_str = saved_str + char
            elif char != " ":
                saved_str = saved_str + char
        elif state == 2:    #Parse parameter
            if char == "'" or char == "\"":
                endchar = char
                state = 3
            elif last_char == " " and char != " " or pos == endpos:
                if saved_strb != "" :
                    state = 1
                    out['params'][saved_str]=saved_strb
                    saved_str = ""
                    saved_strb = ""
                    saved_str = saved_str + char
                else:
                    saved_strb = saved_strb + char
            elif char != " ":
                saved_strb = saved_strb + char
        elif state == 3: #Parse string parameter
            if char == endchar:
                state = 1
                out['params'][saved_str] = saved_strb
                saved_str = ""
                saved_strb = ""
            else:
                saved_strb = saved_strb + char
        last_char = char
    return out

def parseString( data:str ):

    state = 0
    out = []
    saved_str = ""
    saved_str_b = ""
    last_tag = ""
    last_tag_is_closing = False
    for pos in range( len(data) ):
        char = data[pos]

        if state == 0: #Parse plain text
            if char == "<" or pos == len(data)-1:
                saved_str = saved_str.replace("   ", "").replace("\n", "")
                if saved_str != "":
                    out.append( (1, saved_str ) )
                    saved_str = ""
                state = 1
            else:
                saved_str = saved_str + char
        elif state == 1: #Parse SOMETHING between <>
            if char == ">":
                if saved_str[0:3] != "!--":
                    newtag = parseTag( saved_str )
                    if ( last_tag == "script" or last_tag == "style") and not last_tag_is_closing and ( newtag['name'] != last_tag or not newtag['isClosing'] ): #THIS IS SPARTA SCRIPT!
                        state = 2
                        saved_str_b = saved_str_b + saved_str + char
                        saved_str = ""
                    else:

                        out.append( ( 3, saved_str_b ) )
                        out.append( ( 2, newtag ) )
                        last_tag = newtag['name']

                        saved_str = ""
                        saved_str_b = ""
                        if (last_tag == "script" or last_tag == "style") and not newtag['isClosing']:
                            state = 2
                        else:
                            state = 0
                        last_tag_is_closing = newtag['isClosing']
                else:
                    saved_str = ""
                    state = 0
            elif char == "<": #This is certainly a script!
                saved_str_b = saved_str_b + saved_str + char
                saved_str = ""
            else:
                saved_str = saved_str + char

        elif state == 2: #We're proceeding code!
            if char == "<" or pos == len(data)-1:
                if saved_str != "":
                    saved_str_b = saved_str+char
                    saved_str = ""
                state = 1
            else:
                saved_str = saved_str + char

    return out
def buildTag( data, pos ):
    out = {}

    if data[pos][1]['isSingle']:
        out = data[pos][1]
        del out['isSingle']
        del out['isClosing']
        return out, pos+1
    else:
        out = data[pos][1]
        out['inner'] = []
        del out['isSingle']
        del out['isClosing']
        i = pos+1
        while i < len(data):
            tkn = data[ i ]
            if tkn[0] == 1 or tkn[0] == 3:
                out['inner'].append( tkn[1] )
                i+=1
            elif tkn[0] == 2:
                if tkn[1]['isClosing'] and tkn[1]['name'] == out['name']:
                    return out, i+1
                else:
                    tag, i = buildTag( data, i )
                    out['inner'].append( tag )
        return out, len(data)

def treeBuild( data ):
    out = []
    Pos = 1
    while Pos < len(data):
        tkn = data[Pos]
        if tkn[0] == 2:
            tag, Pos = buildTag( data, Pos )
            out.append(tag)
        else:
            Pos += 1
    return out






