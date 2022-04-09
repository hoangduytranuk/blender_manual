import os
import time

from sphinx_intl import catalog as c
from babel.messages import Catalog, Message
from potask_base import POTaskBase, POResultRecord, writeJSONDic, loadJSONDic
from translation_finder import TranslationFinder
from nocasedict import NoCaseDict
from ignore import Ignore as ig
from definition import Definitions as df
# from common import Common as cm
import pathlib as PL
from get_text_within import GetTextWithin as gt

class JSON2PO(POTaskBase):
    def __init__(self,
                 input_file=None,
                 output_to_file=None,
                 ):
        POTaskBase.__init__(
                self,
                input_file=input_file,
                output_to_file=output_to_file,
        )
        self.tf = None

    def performTask(self):

        in_dict = loadJSONDic(self.po_path)
        out_catalog = Catalog(
            locale='vi',
            last_translator='Hoang Duy Tran <hoangduytran1960@googlemail.com>',
            language_team='London, UK, Hoang Duy Tran <hoangduytran1960@googlemail.com>'
        )
        for index, (k, v) in enumerate(in_dict.items()):
            out_catalog.add(k, string=v)
            print(f'adding: [{k}]=>[{v}]')
        is_output = bool(self.opo_path)
        if is_output:
            print(f'Saving output to: [{self.opo_path}]')
            c.dump_po(self.opo_path, out_catalog)
