



def parseCSSValue( val ):
    if val == "": return ""

    if val[0] == ".":
        val = "0"+val
    return val


#def parseSelector( str ):


def parseCSS( css ):
    css = css.replace(" ", "")
    css = css.replace("\n", "")
    css = css.replace("   ", "")
    out = {}
    state = 0
    cur_selector = ""
    cur_input = ""

    cur_property = ""
    cur_val = ""

    end_char = ""

    new_statement = {}
    for char in css:
        #---------------------------------#
        # CSS process states
        #---------------------------------#
        # 0 - Wait for selector
        # 1 - Wait for property
        # 2 - Wait for value
        #--------------------------------#

        if state == 0:
            if char == "{":
                state = 1
            elif char != " ":
                cur_selector += char

        elif state == 1:

            if char == ":":
                state = 2
            elif char == "}":
                state = 0
                out[ cur_selector ] = new_statement
                new_statement = {}
                cur_selector = ""

            elif char != " ":
                cur_property += char

        elif state == 2:
            if char == "\"" or char == "\"":
                if end_char == "":
                    end_char = char
                elif end_char == char:
                    end_char = ""
            elif char == ";":
                new_statement[ cur_property ] = parseCSSValue( cur_val )
                cur_val = ""
                cur_property = ""
                state = 1
            elif char == "}":
                new_statement[ cur_property ] = parseCSSValue( cur_val )
                cur_val = ""
                cur_property = ""
                out[ cur_selector ] = new_statement
                new_statement = {}
                cur_selector = ""
                state = 0
            elif end_char != "" or char != " ":
                cur_val += char

    return out
