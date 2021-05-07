#!/usr/bin/env python3
import re
from translation_finder import TranslationFinder
from definition import Definitions as df
from common import Common as cm, dd, pp, LocationObserver
from matcher import MatcherRecord
from ignore import Ignore as ig
from collections import defaultdict, OrderedDict
from reftype import RefType
from reftype import TranslationState
import copy as CP
import operator as OP
'''
:abbr:`
:class:`
:doc:`
:guilabel:`
:kbd:`
:linenos:`
:math:`
:menuselection:`
:mod:`
:ref:`
:sup:`
:term:`
'''





# :MM:
# :abbr:
# :class:
# :doc:
# :guilabel:
# :kbd:
# :linenos:
# :math:
# :menuselection:
# :minute:
# :mod:
# :ref:
# :sup:
# :term:

class RefList(defaultdict):
    def __init__(self, msg=None, pat=None, keep_orig=False, tf=None):
        self.msg = msg
        self.translation = None
        self.translation_state = TranslationState.UNTRANSLATED
        self.match_record = None
        self.pattern = pat
        self.keep_original = keep_orig
        self.tf = tf

    def getTranslation(self):
        return self.translation

    def getTranslationState(self):
        stat_list = self.getTranslationStateList()
        
        is_fuzzy = (TranslationState.FUZZY in stat_list)
        is_ignore = (TranslationState.IGNORED in stat_list)
        is_accept = (TranslationState.ACCEPTABLE in stat_list)
        
        state = 0
        if is_fuzzy:
            state += 1
        if is_ignore:
            state += 2

        is_def_fuzzy = (state == 1 or state == 3)
        is_def_ignored = (state == 2)

        final_state = TranslationState.ACCEPTABLE
        if is_def_fuzzy:
            final_state = TranslationState.FUZZY
        if is_def_ignored:
            final_state = TranslationState.IGNORED
        return final_state

    def getTranslationStateList(self):
        translation_state_list=[]
        translation_state_list.append(self.translation_state)
        for loc, mm in self.items():
            translation_state_list.append(mm.translation_state)
        return translation_state_list

    def isFuzzy(self):
        state_list = self.getTranslationStateList()
        has_fuzzy = (TranslationState.FUZZY in state_list)
        has_ignored = (TranslationState.IGNORED in state_list)
        has_acceptable = (TranslationState.ACCEPTABLE in state_list)

        return has_fuzzy or (has_ignored and has_acceptable)

    def isIgnore(self):
        state_list = self.getTranslationStateList()
        has_fuzzy = (TranslationState.FUZZY in state_list)
        has_ignored = (TranslationState.IGNORED in state_list)
        has_acceptable = (TranslationState.ACCEPTABLE in state_list)
        return has_ignored and not (has_fuzzy or has_acceptable)

    def setTranslation(self, tran: str, is_fuzzy: bool, is_ignored: bool):
        if not tran:
            tran = ""
        self.translation = tran
        state = (TranslationState.ACCEPTABLE)
        if is_fuzzy:
            state = TranslationState.FUZZY
        if is_ignored:
            state = TranslationState.IGNORED
        self.translation_state = state

    def setText(self, msg):
        self.msg = msg

    def getRecordByIndex(self, index):
        for i, rec in enumerate(self.items()):
            if i == index:
                k, v = rec
                return v
        else:
            return None

    def setParentForChildren(self):
        for k, mm in self.items():
            mm.parent = self

    def findOnePattern(self, local_obs: LocationObserver, msg: str, pattern: re.Pattern, reftype: RefType):
        def setLocationSubMain(dict_list: dict):
            for main_loc, mm in dict_list.items():
                new_mm_list=[]
                mm_list_of_items = mm.getSubEntriesAsList()
                new_mm_list.append(mm_list_of_items[0])
                main_s, main_e = main_loc
                main_txt = mm.txt
                for index in range(1, len(mm_list_of_items)):
                    actual_ref_type = reftype
                    is_type_field = (index == 1)
                    (sub_s, sub_e), sub_txt = mm_list_of_items[index]
                    if is_type_field:
                        try:
                            sub_ref_type = RefType.getRef(sub_txt)
                            actual_ref_type = (sub_ref_type if bool(sub_ref_type) else reftype)
                        except Exception as e:
                            actual_ref_type = RefType.TEXT
                        mm.type = actual_ref_type

                    if sub_txt:
                        dist = (sub_e - sub_s)
                        ss = (sub_s - main_s)
                        ee = ss + dist
                        new_entry = ((ss, ee), sub_txt)
                    else:
                        new_entry = ((sub_s, sub_e), sub_txt)
                    new_mm_list.append(new_entry)
                mm.clear()
                mm.update(new_mm_list)

        def getMatches(pat: re.Pattern, find_txt: str, ref: RefType):
            local_found_dict = {}
            try:
                is_bracket = (ref == RefType.ARCH_BRACKET)
                if is_bracket:
                    local_found_dict = cm.getTextWithinBrackets('(', ')', find_txt, is_include_bracket=False)
                else:
                    local_found_dict = cm.patternMatchAll(pat, find_txt)
                    setLocationSubMain(local_found_dict)
            except Exception as e:
                print(pat)
                print(find_txt)
                print(ref)
                print(local_found_dict)
                print(e)
                raise e
            return local_found_dict

        ignored_dict={}
        entry_orig = entry_type_or_open_symbol = entry_sub = entry_close_symbol = None

        valid_msg = (msg is not None) and (len(msg) > 0)
        valid_pattern = (pattern is not None)
        valid = valid_msg and valid_pattern
        mm: MatcherRecord = None
        sub_mm: MatcherRecord = None
        loc = None
        if not valid:
            return ignored_dict
        try:
            found_dict = getMatches(pattern, msg, reftype)
            if not found_dict:
                return
        except Exception as exception:
            dd("RefList.findOnePattern()")
            dd("pattern:", pattern)
            dd("text:", msg)
            dd(f'mm: [{mm}]; loc: [{loc}]')
            dd(exception)
            raise exception


        found_list = list(found_dict.items())
        for loc, mm in found_list:
            is_parsed_location = local_obs.isLocUsed(loc)
            if is_parsed_location:
                print(f'findOnePattern() PARSED: {loc}, {mm} => IGNORED.')
                is_parsed_location = local_obs.isLocUsed(loc) # for debugging
                continue

            entry_type = mm.type
            actual_ref_type = (entry_type if entry_type else reftype)

            sub_txt = mm.getSubText()
            is_keyboard = (actual_ref_type == RefType.KBD)
            is_ignored = ((not is_keyboard) and ig.isIgnored(sub_txt))
            if is_ignored:
                local_obs.markLocAsUsed(loc)
                continue

            mm.pattern = pattern
            entry = {(mm.s, mm.e): mm}
            self.update(entry)
            local_obs.markLocAsUsed(loc)
        return

    def isEmpty(self):
        is_empty = (len(self) == 0)
        return is_empty

    def validateFoundEntries(self):
        mm: MatcherRecord = None
        for loc, mm in self.items():
            mm_list_of_records = mm.getSubEntriesAsList()
            try:
                (main_s, main_e), main_txt = mm_list_of_records[0]
                (sub_s, sub_e), sub_txt = mm_list_of_records[2]

                valid_sub_txt = main_txt[sub_s: sub_e]
                is_valid = (valid_sub_txt == sub_txt)
                if not valid_sub_txt:
                    raise ValueError(f'validateFoundEntries(): problem with sub_record: {mm}, sub-text extracted doesn\'t match the main-text')

                valid_main_txt = self.msg[main_s: main_e]
                is_valid = (valid_main_txt == main_txt)
                if not valid_sub_txt:
                    raise ValueError(f'validateFoundEntries(): problem with sub_record: {mm}, main-text extracted doesn\'t match the part in the msg')

            except Exception as e:
                print(loc, mm)
                print(e)
                raise e

    def findPattern(self, pattern_list: list, txt: str):
        count_item = 0
        pattern_list.reverse()
        obs = LocationObserver(txt)
        for index, item in enumerate(pattern_list):
            p, ref_type = item
            self.findOnePattern(obs, obs.blank, p, ref_type)
        # print('final:')
        # pp(self)
        # print('end_final')
        self.validateFoundEntries()
        return count_item, obs.getUnmarkedPartsAsDict()

    def addUnparsedDict(self, unparsed_dict: dict):
        mm: MatcherRecord = None
        for uloc, mm in unparsed_dict.items():
            (ms, me) = mm.getMainLoc()
            mtxt = mm.getMainText()

            is_ignored = ig.isIgnored(mtxt)
            if is_ignored:
                continue

            left, mid, right = cm.getTextWithin(mtxt)
            is_all_symbols = (not bool(mid))
            is_ignorable = ig.isIgnored(mid)

            is_ignored = (is_all_symbols or is_ignorable)
            if is_ignored:
                continue

            mm = MatcherRecord(s=ms, e=me, txt=mtxt)
            mm.addSubMatch(-1, -1, None)
            mm.addSubMatch(0, len(mtxt), mtxt)
            mm.type = RefType.TEXT
            entry = {uloc: mm}
            self.update(entry)

    def parseMessage(self):

        trans = self.tf.isInDict(self.msg)
        if trans:
            self.setTranslation(trans, False, False)
            return

        is_link_path = cm.isLinkPath(self.msg)
        if is_link_path:
            dd(f'parseMessage(): IGNORED [{self.msg}]; is_full_path')
            return

        local_msg = str(self.msg)
        count, unparsed_dict = self.findPattern(df.pattern_list, local_msg)
        self.addUnparsedDict(unparsed_dict)
        # # **** should break up sentences here
        # self.findTextOutsideRefs()
        dd('Finishing parseMessage:')


    def translateMatcherRecord(self, mm: MatcherRecord):
        sub_loc: tuple = None
        try:
            ref_txt = mm.getSubText()
            sub_loc = mm.getSubLoc()
            ref_type = mm.type

            is_blank_quote = (ref_type == RefType.BLANK_QUOTE)
            is_kbd = (ref_type == RefType.KBD)
            is_abbr = (ref_type == RefType.ABBR)
            is_menu = (ref_type == RefType.MENUSELECTION)
            is_ga = (ref_type == RefType.GA)
            is_ref = (ref_type == RefType.REF)
            is_doc = (ref_type == RefType.DOC)
            is_osl_attrib = (ref_type == RefType.OSL_ATTRIB)
            is_term = (ref_type == RefType.TERM)

            # ----------
            is_ast = (ref_type == RefType.AST_QUOTE)
            is_dbl_ast_quote = (ref_type == RefType.DBL_AST_QUOTE)
            is_dbl_quote = (ref_type == RefType.DBL_QUOTE)
            is_sng_quote = (ref_type == RefType.SNG_QUOTE)
            is_python_format = (ref_type == RefType.PYTHON_FORMAT)
            is_function = (ref_type == RefType.FUNCTION)

            is_quoted = (is_ast or is_dbl_quote or is_sng_quote or is_dbl_ast_quote or is_blank_quote)

            converted_to_abbr = False
            if is_kbd:
                dd(f'translateRefItem: is_kbd:{ref_txt}')
                ok = self.tf.translateKeyboard(mm)
            elif is_abbr:
                dd(f'translateRefItem: is_abbr:{ref_txt}')
                ok = self.tf.translateAbbrev(mm)
            elif is_menu:
                dd(f'translateRefItem: is_menu:{ref_txt}')
                ok = self.tf.translateMenuSelection(mm)
            elif is_quoted:
                dd(f'translateRefItem: is_quoted:{ref_txt}')
                ok = self.tf.translateQuoted(mm)
                converted_to_abbr = True
            elif is_osl_attrib or is_python_format or is_function:
                return
            else:
                # is_ignore = cm.isLinkPath(ref_txt)
                # if is_ignore:
                #     ref_item.setTranlation(None, False, True)
                #     return
                #
                # dd(f'translateRefItem: anything else: {ref_txt}')
                # is_ref_path = (is_ref and df.REF_PATH.search(ref_txt) is not None)
                # is_doc_path = (is_doc and df.DOC_PATH.search(ref_txt) is not None)
                # is_ignore_path = (is_ref_path or is_doc_path)
                # if is_ignore_path:
                #     return
                ok = self.tf.translateRefWithLink(mm)

            # mm_tran = cm.jointText(ref_txt, tran, sub_loc)
            # mm.setTranlation(mm_tran, is_fuzzy, is_ignore)
        except Exception as e:
            print(f'ERROR! translateRefItem(), ref_item:{mm}, ref_type:{ref_type}, ERROR: {e}')

    def translate(self):
        mm_record: MatcherRecord = None
        is_translated = (self.translation_state != TranslationState.UNTRANSLATED)
        if is_translated:
            return

        tran_text = str(self.msg)
        has_ref = (len(self) > 0)

        if not has_ref:
            trans, is_fuzzy, is_ignore = self.tf.translate(tran_text)
            if trans:
                if self.keep_original:
                    trans = cm.matchCase(self.msg, trans)
                    tran_text = f'{trans} -- {tran_text}'
                else:
                    tran_text = trans
            self.setTranslation(tran_text, is_fuzzy, is_ignore)
        else:
            tran_required_reversed_list = list(self.items())
            tran_required_reversed_list.sort(reverse=True)
            for k, mm_record in tran_required_reversed_list:
                self.translateMatcherRecord(mm_record)

            sent_translation = tran_text
            for mm_loc, mm_record in tran_required_reversed_list:
                tran = mm_record.translation
                has_translation = bool(tran)
                if not has_translation:
                    continue
                sent_translation = cm.jointText(sent_translation, tran, mm_loc)

            is_fuzzy = self.isFuzzy()
            is_ignore = self.isIgnore()
            self.setTranslation(sent_translation, is_fuzzy, is_ignore)


    def getListOfRefType(self, request_list_of_ref_type):
        ref_list=[]
        for mm_loc, mm in self.items():
            type = mm.type
            is_found = (type in request_list_of_ref_type)
            if is_found:
                ref_list.append(mm)
        return ref_list



