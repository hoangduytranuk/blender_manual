#!/usr/bin/env python3
"""
Using sphinx catalog to read/write PO file
Transfer msgstr from new_vipo/vi.po to po/blender.pot to create new vi.po file
"""

import sys
sys.path.append("/home/htran/.local/lib/python3.6/site-packages")
sys.path.append("/home/htran/bin/python/PO")
sys.path.append("/home/htran/bin")

import re
import os
import io

from sphinx_intl import catalog as c
from common import Common as cm
from babel.messages.catalog import Message
from bisect import bisect_left
from babel.messages import pofile

class ValidatePO:
    def __init__(self, root_dir_x, root_dir_y):
        self.from_vipo_path="/home/htran/blender_documentations/new_po/vi.po"
        self.to_blender_pot_path="/home/htran/blender_documentations/po/blender.pot"

    def run(self):


#x.validate(doc_x)


