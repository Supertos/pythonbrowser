#----------------------------------------------------#
# *Python browser
# html.py
#----------------
# Combines functionality of
# - html_tools.py
# - html_tokenizer.py
# - html_postprocessor.py
#----------------------------------------------------#
import html_tools
import html_tokenizer

#---------------------------------------------------------------#
# *HTMLTag
# This class handles html tags
class HTMLTag:
    def __init__(self):
        self.type = ""
        self.content = []
        self.modifiers = {}
        self.id = 0
        self.parent = 0

    def setType(self, type):
        self.type = type

    def addMod(self, name, val=True):
        self.modifiers[name] = val

    def push(self, val):
        self.content.append(val)

    #def setRenderMod(self, name, val):
        #self.render[ name ] = val

#---------------------------------------------------------------#
# *HTML
# This class handles html files
class HTML:
    #---------------------------------------#
    # *HTML.__init__()
    # Object constructor
    def __init__(self):
        self.tags = []

        self.head = 0
        self.body = 0
        self.doctype = 0
        self.html = 0

        self.classes = {}
        self.ids = {}
        self.types = {}

    # ---------------------------------------#
    # *HTML.debug( tag to push )
    # Prints debug information
    def debug(self):
        print( "HTML object")

        print("Tags: ")
        for i in range( len( self.tags ) ):
            val = self.tags[ i ]

            print( i, ":", val.type, val.content, val.modifiers )

        print( "<head> id: ",self.head )
        print( "<body> id: ",self.body )
        print( "<html> id: ",self.html )
        print( "<!DOCTYPE> id: ",self.doctype )

    #---------------------------------------#
    # *HTML.pushTag( tag to push )
    # Pushes tag to tag stack and returns it's id
    def pushTag( self, tag ):
        tag.id = len( self.tags )
        self.tags.append( tag )

        if "id" in tag.modifiers:
            self.ids[ tag.modifiers[ "id" ] ] = tag.id

        if "class" in tag.modifiers:
            myClass = tag.modifiers[ "class" ]

            if myClass not in self.classes:
                self.classes[ myClass ] = []
            self.classes[ myClass ].append( tag.id )

        if tag.type not in self.types:
            self.types[ tag.type ] = []
        self.types[ tag.type ].append( tag.id )

        if tag.type == "head": self.head = tag.id
        if tag.type == "body": self.body = tag.id
        if tag.type == "html": self.html = tag.id
        if tag.type == "!DOCTYPE": self.doctype = tag.id

        return tag.id

    # ---------------------------------------------#
    # *HTML.spiritToTag( spirit )
    # Converts spirit object with tokenizer information to html tag
    def spiritToTag(self, spirit):
        tag = HTMLTag()

        tag.modifiers = spirit.modifiers
        tag.type = spirit.type

        return tag

    # ---------------------------------------------#
    # *HTML.buildTag( tokens, start pos, parent id )
    # Builds tag from previously created token list
    def buildTag(self, tokens, start, parent):

        spirit = tokens[ start ]
        tag = self.spiritToTag( spirit )
        tag.parent = parent

        self.pushTag( tag )

        if spirit.isClosing: return tag.id, start
        pos = start + 1

        while pos < len(tokens):
            tkn = tokens[pos]

            if isinstance(tkn, str):
                tag.push( html_tools.replaceHTMLEnts( tkn ) )
            elif tkn.isClosing and tkn.type == tag.type:
                return tag.id, pos
            else:
                add, pos = self.buildTag(tokens, pos, tag.id )
                tag.push(add)
            pos += 1

        raise ValueError("Tag " + tag.type + " has start but has no end")

    #---------------------------------------------#
    # *HTML.build( tokens )
    # Builds tag from previously created token list
    def build( self, tokens ):
        pos = 0
        while pos < len(tokens):
            if isinstance(tokens[pos], html_tokenizer.HTMLSpirit):
                add, pos = self.buildTag(tokens, pos, -1)
            pos += 1



    def checkParent(self, filter, tag, pos):
        node = filter[pos]
        if "class" in node:
            if "class" not in tag.modifiers or tag.modifiers["class"] != node["class"]:
                return False

        if "type" in node:
            if tag.type != node["type"]:
                return False

        if "id" in node:
            if "id" not in tag.modifiers or tag.modifiers["id"] != node["id"]:
                return False

        if len( filter ) - 1 > pos:
            return self.checkParent( filter, self.tags[ tag.parent ], pos+1 )
        else:
            return True

    #----------------------------------------------#
    #
    def getSelectorList(self, selector):
        datas = selector.split(",")
        out = []
        for element in datas:

            element = element.replace( ">", " " )
            element = element.replace( "+", " " )
            combinators = element.split(" ")

            filter = []
            for comb in combinators:
                node = {}
                if comb[0] == "#":
                    node[ "class" ] = comb[1:]
                elif comb[0] == ".":
                    node[ "id" ] = comb[ 1: ]
                else:
                    node[ "type" ] = comb
                filter.append( node )

            for a in filter:
                for id in range( len(self.tags) ):
                    tag = self.tags[ id ]
                    if self.checkParent( filter, tag, 0 ):
                        out.append( id )
        return out

    def applyCSS( self, css ):
        for selector, data in css.items():
            print( selector, self.getSelectorList( selector ) )
            #for property, value in data.items():


#---------------------------------------------#
# *processHTML( html source )
# Returns HTML object representing provided html source
def processHTML( html ):
    html = html_tools.removeSpaces( html )
    html = html_tokenizer.tokenizeHTML( html )

    out = HTML()
    out.build( html )

    return out

