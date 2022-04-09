import os
import inspect as INP
from babel.messages import Catalog, Message
from pprint import pprint as pp
from sphinx_intl import catalog as c
from datetime import datetime, date
from collections import OrderedDict

from observer import LocationObserver
from translation_finder import TranslationFinder
from pattern_utils import PatternUtils as pu

from refs.ref_base import RefBase
from refs.ref_menu import RefMenu
from refs.ref_abbr import RefAbbr
from refs.ref_keyboard import RefKeyboard
from refs.ref_guilabel import RefGUILabel
from refs.ref_with_link import RefWithLink
from refs.ref_term import RefTerm
from refs.ref_with_external_link import RefWithExternalLink
from refs.ref_with_internal_link import RefWithInternalLink
from refs.ref_single_quote import RefSingleQuote
from refs.ref_ast import RefAST
from refs.ref_ga_only import RefGA
from refs.ref_ga_with_bracket import RefGAWithBrackets

class RefDriver:
    home = os.environ['HOME']
    home = os.path.join(home, 'Dev/tran')
    global_untran_list = []

    def __init__(self):
        self.obs: LocationObserver = None
        self.mid = None
        self.mstr = None
        self.new_txt = None
        self.ref_handler_list = None
        self.tf = TranslationFinder()

    def jointText(self, orig: str, tran: str, loc: tuple):
        s, e = loc
        left = orig[:s]
        right = orig[e:]
        has_tran = (tran is not None)
        string_list = ([left, tran, right] if has_tran else [left, right])
        new_string = ''.join(string_list)
        return new_string

    def translateRefs(self, m: Message):
        def insertRefHandler(ref_handler: RefBase):
            handler = ref_handler(self.new_txt, tf=self.tf)
            pat = handler.getPattern()
            dict_list = pu.patternMatchAll(pat, self.new_txt)
            has_patterns = len(dict_list) > 0
            if not has_patterns:
                return None

            loc_list = list(dict_list.keys())
            handler.obs = insertRefHandler.obs
            handler.obs.markLocListAsUsed(loc_list)

            dict_list = list(dict_list.items())
            dict_list.sort(reverse=True)
            handler.extend(dict_list)
            return handler

        def translate_handler(ref_handler: RefBase):
            ref_handler.translateAll()
            RefDriver.global_untran_list.extend(ref_handler.need_tran_list)
            return ref_handler

        self.mid = m.id
        has_id = len(self.mid) > 0
        if not has_id:
            return None

        self.mstr = m.string
        has_tran = len(self.mstr) > 0
        if has_tran:
            return None

        is_debug = ('["Agent"]' in self.mid)
        if is_debug:
            is_debug = True

        # always the global mid text has already been updated,
        # each ref handler would generate it's own locations,
        # after previous handler has updated the message
        new_txt = str(self.mid)
        self.new_txt = new_txt

        self.obs = LocationObserver(self.mid)
        insertRefHandler.obs: LocationObserver = self.obs

        handler_list_raw = list(map(insertRefHandler, self.ref_handler_list))
        handler_list = [handler for handler in handler_list_raw if (handler is not None)]
        has_handlers = len(handler_list) > 0
        if not has_handlers:
            return None

        translate_handler.global_untran_list = self.obs
        handler_list = list(map(translate_handler, handler_list))

        ref_list = [x for y in handler_list for x in y]

        for (loc, mm) in ref_list:
            is_translated = (mm.translation is not None)
            if not is_translated:
                continue

            sub_list = mm.getSubEntriesAsList()
            (oloc, otxt) = sub_list[0]
            tran_txt = mm.translation
            new_txt = self.jointText(new_txt, tran_txt, oloc)

        is_changed = (new_txt != self.mid)
        if not is_changed:
            return None

        report_msg = f'\nmid:{self.mid}\nnew_mstr:{new_txt}\n\n'
        print(report_msg)
        m.string = new_txt
        is_debug = True
        return m

    def writeUntranslatedDict(self, untran_dic_file):
        has_untran = len(RefDriver.global_untran_list) > 0
        if not has_untran:
            return

        global_untran_list = list(set(RefDriver.global_untran_list))
        global_untran_list.sort()

        # use dict to filter out same text different case entries
        lcase_dict = OrderedDict()
        for txt in global_untran_list:
            entry = {txt.lower(): txt}
            lcase_dict.update(entry)
        global_untran_list = list(lcase_dict.values())

        today_date = datetime.now()
        untran_catalog = Catalog(project='Translate Blender Man',
                                 version='1.0',
                                 creation_date=today_date,
                                 revision_date=today_date,
                                 language_team="UK <hoangduytran1960@gmail.com>",
                                 locale="vi",
                                 last_translator="Hoang Duy Tran <hoangduytran1960@gmail.com>")
        for txt in global_untran_list:
            txt = txt.strip()
            untran_catalog.add(txt)

        c.dump_po(untran_dic_file, untran_catalog, line_width=4096)

    def executeDriver(self):
        ref_handler_list = [RefMenu]
        self.ref_handler_list = [RefGAWithBrackets]

        dict_file = os.path.join(RefDriver.home, 'cor_0014.po')
        input_file = os.path.join(RefDriver.home, 'blender_manual_0003_0019.po')
        output_file = os.path.join(RefDriver.home, 'blender_manual_0003_0020.po')
        untran_dic_file = os.path.join(RefDriver.home, '20220408_untran.po')
        data = c.load_po(input_file)

        result_list = list(map(self.translateRefs, data))

        is_translated_list = [(mm is not None) for mm in result_list]
        is_changed = (True in is_translated_list)
        is_writing_changes = (is_changed and output_file is not None)
        if is_writing_changes:
            print(f'writing changes to {output_file}')
            # c.dump_po(output_file, data, line_width=4096)
        self.writeUntranslatedDict(untran_dic_file)