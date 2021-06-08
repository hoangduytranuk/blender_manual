#!/usr/bin/env python3
import re
from translation_finder import TranslationFinder
from definition import Definitions as df, RefType, TranslationState
from common import Common as cm, dd, pp, LocationObserver
from matcher import MatcherRecord
from ignore import Ignore as ig
from collections import defaultdict, OrderedDict

import operator as OP
import inspect as INP

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
        def setReftypeAndUsingSubTextLocation(dict_list: dict):
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
                    setReftypeAndUsingSubTextLocation(local_found_dict)
            except Exception as e:
                df.LOG(f'{e}; pat:[{pat}]; find_txt:[{find_txt}]; ref:[{ref}]; local_found_dict:[{local_found_dict}];', error=True)
                raise e
            return local_found_dict

        valid_msg = (msg is not None) and (len(msg) > 0)
        valid_pattern = (pattern is not None)
        valid = valid_msg and valid_pattern
        if not valid:
            return
        try:
            found_dict = getMatches(pattern, msg, reftype)
            if found_dict:
                self.update(found_dict)
            local_obs.markLocListAsUsed( found_dict.keys() )
        except Exception as e:
            df.LOG(f'{e} msg:[{msg}]; found_dict:[{found_dict}]', error=True)
            raise e


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
                df.LOG(f'{e} loc:[{loc}]; mm:[{mm}]', error=True)
                raise e

    def findPattern(self, pattern_list: list, txt: str):
        count_item = 0
        obs = LocationObserver(txt)
        pattern_list.reverse()
        obs = LocationObserver(txt)

        for index, item in enumerate(pattern_list):
            p, ref_type = item
            self.findOnePattern(obs, obs.blank, p, ref_type)
        # self.validateFoundEntries()

        # if len(self):
        #     dd('List of refs found:')
        #     dd('-' * 80)
        #     pp(self)
        #     dd('-' * 80)
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
        if len(self):
            dd('Finishing parseMessage:')
            dd('-' * 80)
            for loc, mm_rec in self.items():
                dd(f'{loc}')
                dd(f'{mm_rec.txt}')
                dd('-' * 80)


    def translateMatcherRecord(self, mm: MatcherRecord):
        sub_loc: tuple = None
        try:
            ref_txt = mm.txt
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
                ok = self.tf.translateRefWithLink(mm)

            # mm_tran = cm.jointText(ref_txt, tran, sub_loc)
            # mm.setTranlation(mm_tran, is_fuzzy, is_ignore)
        except Exception as e:
            df.LOG(f'{e} ref_item:{mm}, ref_type:{ref_type}', error=True)

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



