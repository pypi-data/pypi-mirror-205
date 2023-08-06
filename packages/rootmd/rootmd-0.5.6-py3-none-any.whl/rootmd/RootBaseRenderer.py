from mistletoe.base_renderer import BaseRenderer
from shutil import move
import re
import logging
from .Executor import RootExecutor
from .Executor import GnuPlotExecutor
from .Executor import RnuPlotExecutor

from .YamlBlock import YamlFence, CodeFence
import yaml

from rich.logging import RichHandler
FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")

"""
Base renderer for mistletoe with ROOT code execution and asset injection.
"""

class RootBaseRenderer(BaseRenderer):
    def __init__(self, *extras):
        super().__init__(YamlFence, CodeFence, *extras)

        # externlal code executors
        self.gnuplot = GnuPlotExecutor()
        self.rnuplot = RnuPlotExecutor()
        self.root    = RootExecutor() 

        self.executors = {
            'cpp'     : self.root,
            'gnuplot' : self.gnuplot,
            'rnuplot' : self.rnuplot,
        } 

        self.handlers = {
            'cpp'         : self.handle_root,
            'gnuplot'     : self.handle_gnuplot,
            'rnuplot'     : self.handle_rnuplot
        }
    
    def render_yaml_fence(self, token):
        log.info("YAML Fence")
        try:
            y = yaml.safe_load( token.children[0].content )
            self.process_yaml( y )
            # Do something here
        except yaml.YAMLError as e:
            log.error( e )

        token.language = "yaml"
        if self.yaml.get( "hide", False ) == True or self.yaml.get( "hide", False ) == "1" or self.yaml.get( "hide", False ) == 1 :
            return ""
        return super().render_block_code(token)
    
    def render_inline_code( self, token):
        # rich.inspect( token )
        code = token.children[0].content

        # evaluate code inside BASH style blocks
        m = re.search( "\${(.*?)}", code )
        if m:
            # log.info( "--->CODE: %s" % ( m.groups()[0] ) )
            evalcode = m.groups()[0]
            evalcode += ';printf("\\n");'

            log.info( 'eval: "%s"' % evalcode )
            output, err, imgs = self.run_cmd( evalcode )
            log.info( "stdout: %s" % ( output ) )
            log.info( "stderr: %s" % ( err ) )
            return output

        return super().render_inline_code( token )

    def render_code_fence( self, token ):
        log.info( "render_code_fence" )
        # rich.inspect( token )
        return self.render_block_code( token )
    
    def render_block_code( self, token ) :
        pass


    def process_yaml( self, yaml ):
        pass

    def addExecutor( self, name, exec, handler ):
        self.executors[ name ] = exec
        self.handler[ name ] = handler

    def handle_root( self ) :
        pass
    
    def handle_gnuplot( self ) :
        pass
    
    def handle_rnuplot( self ) :
        pass