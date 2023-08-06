from mistletoe.base_renderer import BaseRenderer


import hashlib
import rich
import logging
from rich.logging import RichHandler
from .YamlBlock import YamlFence, CodeFence
FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")


class Md2MacroRenderer(BaseRenderer):
    def __init__(self, *extras):
        super().__init__(YamlFence, CodeFence, *extras)
        
        self.blockid = 0
        self.embed = False
        self.asset_prefix = ""
        self.asset_dir = ""
        self.artifacts = []
        
    
    def set( self, **kwargs ) :
        if "embed" in kwargs :
            self.embed = kwargs.get( "embed" )
        if "asset_dir" in kwargs :
            self.asset_dir = kwargs.get( "asset_dir" )
        if "asset_prefix" in kwargs:
            self.asset_prefix = kwargs.get( "asset_prefix" )


    # SHOULD CENTRALIZE WITH OTHER RENDERERS
    def optionAsBool( self, options, n, default = False ):
        
        # option is false by default
        if n not in options :
            log.info( "A" )
            return default
        if type( options[n] ) == bool:
            log.info( "B" )
            return options[n]
        log.info( "C" )
        return not (options.get( n, "" ).lower() == 'false' or options.get( n, "" ) == '0')

    """
    Code Fence is a custom Code Block token that accepts optional arguments after the language id
    example:
    ```cpp in:0
    ...
    ```

    the above turns off echoing the input to rendered document
    """
    def render_code_fence( self, token ):
        log.info( "render_code_fence" )
        # rich.inspect( token )
        return self.render_block_code( token )

    def render_block_code(self, token):

        log.info( "options:" )
        log.info( token.options )
        if token.language != "cpp" and token.options.get( "exec", "" ) != "cpp":
            return self.render_raw_text( token )

        log.info( "exec : %s" % ( self.optionAsBool( token.options, "exec", True ) ) )
        if self.optionAsBool( token.options, "exec", True ) == False:
            return ""
            # return self.render_raw_text( token )
        # code =token.children[0].content
        
        hash = hashlib.md5( token.children[0].content.encode() )
        output = "// %%>{id} ----------ROOTMD_START_BLOCK{hash}----------\n".format( id = self.blockid, hash = hash.hexdigest() )
        output += 'printf( "START_BLOCK%%>{id}<%%{hash} {{\\n" );\n'.format( id = self.blockid, hash = hash.hexdigest() )
        for l in token.children[0].content.splitlines():
            output += "    " + l + "\n"
        output += 'printf( "END_BLOCK%%<{id}>%%{hash} }}\\n" );\n'.format( id = self.blockid, hash = hash.hexdigest() )
        output += "// %%<{id} ----------ROOTMD_END_BLOCK{hash}----------\n".format( id = self.blockid, hash = hash.hexdigest() )


        self.blockid += 1
        return output

    def render_inline_code(self, token):
        return "`" + self.render_raw_text(token) + "`"

        
    
    def render_thematic_break(self, token):
        # inspect( token )
        return "---"

    @staticmethod
    def render_line_break(token):
        log.debug( 'line break' )
        return '\n' if token.soft else '\n'

    def render_inner( self, token ):
        return ''.join(map(self.render_raw_text, token.children))
    def render_raw_text(self, token):
        """
        Default render method for RawText. Simply return token.content.
        """
        if hasattr(token, 'content'):
            output = ""
            for l in token.content.splitlines():
                output += "//" + l + "\n"
            return output
        return self.render_inner( token )
    def render_to_plain(self, token):
        log.info( "render_to_plain" )
        # if hasattr(token, 'children'):
        #     inner = [self.render_to_plain(child) for child in token.children]
        #     return ( '//' + ''.join(inner))
        # return ("//" + token.content)
        return ""

    def render_heading(self, token):
        inner = self.render_inner(token)
        out = "#" * int(token.level) + " " + inner
        return out

    def render_document(self, token):
        # inner = '\n'.join([self.render(child) for child in token.children])
        inner = ""
        parts = []
        for child in token.children :
            log.info( child.__class__.__name__ )
            if "CodeFence" == child.__class__.__name__ or "InlineCode" == child.__class__.__name__:
                parts.append( self.render( child ) )
            else:
                parts.append( self.render_raw_text( child ) )
            # rich.inspect( child )
        inner = '\n'.join( parts )
        return inner
