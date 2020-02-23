#!/usr/bin/env python3

import sys
sys.path.append('/home/htran/bin/python')
sys.path.append('/home/htran/.local/lib/python3.6/site-packages')
#print("/home/htran/.local/lib/python3.6/site-packages/sphinx_intl/basic.py")
print("sys.path={}".format(sys.path))
import os
import re
import io

from babel.messages import pofile
from sphinx_intl.pycompat import relpath
from functionbase import FunctionBase
#from validatevipo import ValidateVIPO
#from copymsgstrfromdir import CopyMsgStrFromDir
#from sphinx_import.flatpotext import FlatPOText
from replacetranslation import ReplaceTranslation

from sphinx_intl import catalog as c

function_list=[
    #ApplyDictionary()
    #RemoveEntryByText()
    #CopyMsgStrFromFile()
    #ValidateVIPO()
    #CopyMsgStrFromDir()
    #FlatPOText()
    ReplaceTranslation()
    ]


class ProcessPOFiles():
    def __init__(self):
        self.doc_dir="/home/htran/blender_documentations/blender_docs"
        self.locale_dir = "{}/locale".format(self.doc_dir)
        self.languages = ["vi"]
        self.pot_dir = "{}/build/locale".format(self.doc_dir)


    def dump_po(self, filename, catalog):
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # Because babel automatically encode strings, file should be open as binary mode.
        #print("Saving file:{}".format(filename))
        with io.open(filename, 'wb') as f:
            pofile.write_po(f, catalog, width=0)

    def run(self):
        status = {
            'create': 0,
            'update': 0,
            'notchanged': 0,
        }

        for dirpath, dirnames, filenames in os.walk(self.pot_dir):
            for filename in filenames:
                pot_file = os.path.join(dirpath, filename)
                base, ext = os.path.splitext(pot_file)
                basename = relpath(base, self.pot_dir)

                for lang in self.languages:
                    po_dir = os.path.join(self.locale_dir, lang, 'LC_MESSAGES')
                    po_file = os.path.join(po_dir, basename + ".po")
                    if os.path.exists(po_file):
                        cat = c.load_po(po_file)
                        changed = False
                        #self.dump_po(po_file, cat)
                        for func in function_list:
                            if isinstance(func, FunctionBase):
                                #print("apply_function: po_file{}".format(po_file))
                                func.category = c
                                func.pofileCategory = cat
                                func.fileName = po_file
                                func.setLocalVars()
                                func.run()
                                if (func.changed):
                                    print('Update:{}'.format(po_file))
                                    status['update'] += 1
                                    self.dump_po(po_file, cat)
                                else:
                                    pass
                                    #status['notchanged'] += 1
        return status

x = ProcessPOFiles()
x.run()
