#import sys
#sys.path.append("/home/htran/.local/lib/python3.6/site-packages")
#import os

#from sphinx_intl import catalog as c
from functionbase import FunctionBase
#from babel.messages.catalog import Message

#print("dir(c):{}".format(dir(c)))
#exit(0)

class FlatPOText(FunctionBase):

    def run(self):
        self.changed = True
