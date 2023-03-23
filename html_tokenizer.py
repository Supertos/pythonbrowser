# ----------------------------------------------------#
# *Python browser
# html_tokenizer.py
# ----------------
# Parses loaded html files
# ----------------------------------------------------#


class HTMLSpirit:
    def __init__(self):
        self.type = ""
        self.is_single = False
        self.content = []
        self.modifiers = {}
        self.isClosing = False

    def setType(self, type):
        self.type = type

    def addMod(self, name, val=True):
        self.modifiers[name] = val

    def setRenderMod(self, name, val):
        self.render[ name ] = val

single_tags = [
    "area", "base", "br", "col", "command", "embed", "hr", "img", "input", "keygen", "link",
    "meta", "param", "source", "track", "wbr", "!doctype", "![endif]--"
]


def isSingleTag(name):
    global single_tags
    return name in single_tags

def isScriptTag( tag: HTMLSpirit ) -> bool:
    return not tag.isClosing and ( tag.type == "script" or tag.type == "style" )

def parseTag(data: str) -> HTMLSpirit:
    # -------------------------------------------------#
    # TAG Parsing states:
    # 0 - Processing tag name
    # 1 - Processing modifier name
    # 3 - Processing modifier value
    # 4 - Processing modifier string

    out = HTMLSpirit()

    state = 0
    string_endsymbol = ""

    saved_parameter = ""
    saved_name = ""
    for pos in range(len(data)):

        char = data[pos]

        if state == 0:
            if char == ">" or char == " ":
                out.setType(saved_name.lower())
                if isSingleTag(saved_name.lower()): out.isClosing = True
                saved_name, state = "", 1
            elif char != "<":
                if char == "/":
                    out.isClosing = True
                else:
                    saved_name += char
        elif state == 1:
            if saved_name != "" and ( char == ">" or char == "/" or char == " " ) :
                out.addMod(saved_name)
                saved_name = ""
            elif char == "=":
                state = 2
            elif char != " ":
                saved_name += char
        elif state == 2:
            if char == "'" or char == "\"":
                string_endsymbol = char
                state = 3
            elif char == " " or char == ">" or char == "/":
                if saved_parameter != "":
                    out.addMod(saved_name, saved_parameter)
                    saved_parameter, saved_name, state = "", "", 1
            else:
                saved_parameter += char
        elif state == 3:
            if char == string_endsymbol:
                out.addMod(saved_name, saved_parameter)
                saved_parameter, saved_name, state = "", "", 1
            else:
                saved_parameter += char

    return out


def tokenizeHTML( data: str ) -> list:

    out = []
    endpos = len( data )-1
    #-------------------------------------------------#
    # String Parsing states:
    # 0 - Processing plain text
    # 1 - Processing tag
    # 2 - Processing something alien
    state = 0

    saved_string = ""
    saved_code = ""
    prev_isScriptTag = False
    prev_tagtype = ""
    prev_tagIsClosing = True

    for char in data:

        if state == 0:

            if char == "<":
                if not prev_tagIsClosing and saved_string != "": out.append( saved_string ) # Disallow out-of-tag text
                saved_string, state = "<", 1
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
                    if saved_string[0:4] == "<!--":
                        if saved_string[-1] + saved_string[-2] == "--":
                            saved_string, state = "", 0
                        else:
                            saved_string += char
                    else:
                        if prev_isScriptTag: out.append(saved_code)
                        out.append(tag)
                        prev_isScriptTag = isScriptTag(tag)
                        prev_tagtype = tag.type
                        prev_tagIsClosing = tag.isClosing
                        saved_string, saved_code, state = "", "", 0
                        if prev_isScriptTag: state = 2


            elif char == "<":   # We can't start tag twice! Certainly a script!
                saved_code = saved_code + saved_string
                saved_string = "<"
            else:
                saved_string += char

        elif state == 2:
            if char == "<":
                saved_string, state = "<", 1
            else:
                saved_code = saved_code + char

    return out

