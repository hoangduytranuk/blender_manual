import os
import inspect as INP
import re

from babel.messages import Catalog, Message
from pprint import pprint as pp
from sphinx_intl import catalog as c
from datetime import datetime, date
from collections import OrderedDict

import refs.ref_all
from observer import LocationObserver
from translation_finder import TranslationFinder
from pattern_utils import PatternUtils as pu
from string_utils import StringUtils as st

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
from refs.ref_all import RefAll
from refs.ref_brackets import RefBrackets
from refs.ref_ga_leading_symbs import RefGALeadingSymbols
from refs.ref_double_quoted_text import RefDoubleQuotedText
from refs.ref_dbl_ast import RefDoubleAST
from refs.ref_function import RefFunction

from definition import RefType
from get_text_within import GetTextWithin as gwt
class RefDriver(list):
    home = os.environ['HOME']
    home = os.path.join(home, 'Dev/tran')
    global_untran_list = []
    global_translated_list = []

    ref_handler_list = [
        (RefType.GUILABEL, RefGUILabel),
        (RefType.MENUSELECTION, RefMenu),
        (RefType.ABBR, RefAbbr),
        (RefType.GA_LEADING_SYMBOLS, RefGALeadingSymbols),
        (RefType.GA_EXTERNAL_LINK, RefWithExternalLink),
        (RefType.GA_INTERNAL_LINK, RefWithInternalLink),
        (RefType.REF_WITH_LINK, RefWithLink),
        (RefType.GA, RefGA), # done
        (RefType.KBD, RefKeyboard),
        (RefType.TERM, RefTerm),
        (RefType.AST_QUOTE, RefAST),
        (RefType.FUNCTION, RefFunction),
        (RefType.SNG_QUOTE, RefSingleQuote),
        (RefType.DBL_QUOTE, RefDoubleQuotedText),
        # (RefType.GLOBAL, RefAll), # problem
        (RefType.ARCH_BRACKET, RefBrackets),
    ]

    ref_handler_dict = OrderedDict(ref_handler_list)

    def __init__(self, tf=None):
        self.obs: LocationObserver = None
        self.mid = None
        self.mstr = None
        self.new_txt = None
        self.ref_handler_list = None
        self.tf = (TranslationFinder() if tf is None else tf)
        self.last_used_handler = None

    def jointText(self, orig: str, tran: str, loc: tuple):
        s, e = loc
        left = orig[:s]
        right = orig[e:]
        has_tran = (tran is not None)
        string_list = ([left, tran, right] if has_tran else [left, right])
        new_string = ''.join(string_list)
        return new_string

    def translateRefs(self, m: Message):
        from definition import RefType, Definitions as df
        def insertRefHandler(entry):
            ref_type = entry[0]
            ref_handler: RefBase = entry[1]

            # is_debug = ('curve if they have no bulges' in self.mid)
            # if is_debug:
            #     is_debug = True

            is_bracket = (ref_type == RefType.ARCH_BRACKET)
            txt = self.obs.blank
            if is_bracket:
                handler = RefBrackets(self.obs.blank, tf=self.tf)
                left_brks = '|'.join(df.left_set_brackets)
                right_brks = '|'.join(df.right_set_brackets)
                dict_list = st.getTextWithinBrackets(left_brks, right_brks, txt, is_include_bracket=True)
            else:
                handler = ref_handler(self.obs.blank, tf=self.tf, ref_type=ref_type)
                pat = handler.getPattern()
                dict_list = pu.patternMatchAll(pat, self.obs.blank, ref_type=ref_type, is_including_surrounding_symbols=True)

            self.last_used_handler = handler
            has_patterns = len(dict_list) > 0
            if not has_patterns:
                return None

            loc_list = list(dict_list.keys())
            self.obs.markLocListAsUsed(loc_list)

            dict_list = list(dict_list.items())
            dict_list.sort(reverse=True)
            handler.extend(dict_list)
            return handler

        def translate_handler(ref_handler: RefBase):
            ref_handler.translateAll()
            RefDriver.global_untran_list.extend(ref_handler.untranslated)
            RefDriver.global_translated_list.extend(ref_handler.translated)
            return ref_handler

        self.mid = m.id
        # self.mid = "``(LW)POLYLINE``, ``(LW)POLYGON`` as ``POLYLINE`` curve if they have no bulges else as ``BEZIER`` curve."
        has_id = len(self.mid) > 0
        if not has_id:
            return None

        self.mstr = m.string
        has_tran = len(self.mstr) > 0
        if has_tran:
            return None

        # always the global mid text has already been updated,
        # each ref handler would generate it's own locations,
        # after previous handler has updated the message
        self.new_txt = str(self.mid)
        self.obs = LocationObserver(self.new_txt)
        handler_list_raw = list(map(insertRefHandler, RefDriver.ref_handler_list))
        handler_list = [handler for handler in handler_list_raw if (handler is not None)]
        has_handlers = len(handler_list) > 0
        if not has_handlers:
            return None

        translate_handler.global_untran_list = self.obs
        handler_list = list(map(translate_handler, handler_list))
        ref_list = [x for y in handler_list for x in y]
        ref_list.sort(reverse=True)
        for (loc, mm) in ref_list:
            is_translated = (mm.translation is not None)
            if not is_translated:
                continue

            sub_list = mm.getSubEntriesAsList()
            tran_txt = mm.translation
            self.new_txt = self.jointText(self.new_txt, tran_txt, loc)

        is_changed = (self.new_txt != self.mid)
        if not is_changed:
            return None

        report_msg = f'\nmid:\n{self.mid}\n\nnew_mstr:\n{self.new_txt}\n\n\n'
        print(report_msg)
        m.string = self.new_txt
        return m

    def writeCatelog(self, dic_file, data_list):
        has_data = (data_list is not None) and (len(data_list) > 0)
        if not has_data:
            return

        data_list = list(set(data_list))
        data_list.sort()

        today_date = datetime.now()
        catalog = Catalog(project='Translate Blender Man',
                                 version='1.0',
                                 creation_date=today_date,
                                 revision_date=today_date,
                                 language_team="UK <hoangduytran1960@gmail.com>",
                                 locale="vi",
                                 last_translator="Hoang Duy Tran <hoangduytran1960@gmail.com>")
        for (txt, tran) in data_list:
            catalog.add(txt, string=tran)

        c.dump_po(dic_file, catalog, line_width=4096)

    def executeDriver(self):
        dict_file = os.path.join(RefDriver.home, 'cor_0015.po')
        input_file = os.path.join(RefDriver.home, 'blender_manual_0003_0022.po')
        output_file = os.path.join(RefDriver.home, 'blender_manual_0003_0023.po')
        untran_dic_file = os.path.join(RefDriver.home, '20220409_untran.po')
        tran_dic_file = os.path.join(RefDriver.home, '20220409_translated.po')
        data = c.load_po(input_file)

        result_list = list(map(self.translateRefs, data))

        is_translated_list = [(mm is not None) for mm in result_list]
        is_changed = (True in is_translated_list)
        is_writing_changes = (is_changed and output_file is not None)
        if is_writing_changes:
            print(f'writing changes to {output_file}')
            # c.dump_po(output_file, data, line_width=4096)
        self.writeCatelog(untran_dic_file, RefDriver.global_untran_list)
        self.writeCatelog(tran_dic_file, RefDriver.global_translated_list)
