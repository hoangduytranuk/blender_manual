#!/usr/bin/python3 -d
"""
Using sphinx catalog to read/write PO file
Transfer msgstr from new_vipo/vi.po to po/blender.pot to create new vi.po file
"""

import os
import io
from pprint import pprint as PP
from distutils import log as logger
from sphinx_intl import catalog as c
from babel.messages import pofile
from babel.messages.catalog import Message, Catalog

class TranslateTitleFiles:
    def __init__(self):
        self.dic_path = "/home/htran/blender_documentations/new_po/vi.po"
        self.dic_cat = c.load_po(self.dic_path)
        self.dic_cat_lower = self.poCatDictLower(self.dic_cat)
        #po_dic = self.poCatToList(dic_cat)

        #po_dic_lower = self.poCatToListLower(dic_cat)
        #sorted_po_dic = sorted(po_dic)
        #PP(po_dic_lower)
        #sorted_lower_po_dic = sorted(po_dic_lower)


    def poCatToList(self, po_cat):
        l = []
        for index, m in enumerate(po_cat):
            k = m.id
            v = m
            l.append((k, v))
        return l

    def poCatToListLower(self, po_cat):
        l = []
        for index, m in enumerate(po_cat):
            k = m.id.lower()
            v = m
            l.append((k, v))
        return l

    def poCatDictLower(self, po_cat):
        l = {}
        for index, m in enumerate(po_cat):
            k = m.id.lower()
            v = m
            l.update({k: v})
        return l

    # PP(sorted_lower_po_dic)

    def dump_po(self, filename, catalog):
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # Because babel automatically encode strings, file should be open as binary mode.
        with io.open(filename, 'wb') as f:
            pofile.write_po(f, catalog, width=4096)

    def findTranslation(self, msg):
        has_translation = (msg in self.dic_cat)
        if has_translation:
            trans = self.dic_cat[msg]
        else:
            print("Look into the lower list")
            has_translation = (msg in self.dic_cat_lower)
            if has_translation:
                trans = self.dic_cat_lower[msg.lower()]
            else:
                trans = None

        if (has_translation):
            txt = trans.string
            return txt
        return None

    def run(self):
        trans = None
        msg = "author"
        trans = self.findTranslation(msg)
        if (trans):
            print("{} = {}".format(msg, trans))


x = TranslateTitleFiles()
x.run()
