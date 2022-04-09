#!/usr/bin/env python3
import re
from definition import Definitions as df, RefType, TranslationState
from common import Common as cm, LocationObserver
from utils import dd, pp
from matcher import MatcherRecord
from ignore import Ignore as ig
from collections import defaultdict, OrderedDict
from sentence import StructRecogniser as SR
from nocasedict import NoCaseDict as NDIC
import concurrent.futures
from pattern_utils import PatternUtils as pu
from get_text_within import GetTextWithin as GTW
from string_utils import StringUtils as st
from bracket import RefAndBracketsParser as PSER
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

        self.parsed_dict = NDIC()
        self.sr_global_dict = NDIC()
        self.keep_abbr = True
        self.local_ref_map = None

    def reproduce(self):
        return self.__class__()

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
        translation_state_list=[mm.translation_state for loc, mm in self.items()]
        return translation_state_list

    def isAllTranslated(self):
        state_list = self.getTranslationStateList()
        is_all_translated = not (TranslationState.UNTRANSLATED in state_list)
        return is_all_translated

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

    def isEmpty(self):
        is_empty = (len(self) == 0)
        return is_empty

    def getListOfRefType(self, request_list_of_ref_type):
        ref_list = [mm for (loc, mm) in self.items() if mm.type in request_list_of_ref_type]
        return ref_list

    def getUnparsedDict(self, unparsed_dict: dict):
        mm: MatcherRecord = None
        unparsed = {}
        for uloc, mm in unparsed_dict.items():
            (ms, me) = mm.getMainLoc()
            mtxt = mm.getMainText()

            mm = MatcherRecord(s=ms, e=me, txt=mtxt)
            mm.addSubMatch(-1, -1, None)
            mm.addSubMatch(0, len(mtxt), mtxt)
            mm.type = RefType.TEXT
            entry = {uloc: mm}
            unparsed.update(entry)
        return unparsed

    def parseMessage(self, is_ref_only=False, include_brackets=False, pattern_list=None):
        dict_list = PSER.parseMsgAndBrackets(self.msg)
        self.clear()
        self.update(dict_list)
        print(self)

    def createSRAndTranslateSegment(self, segment):
        (loc, mm) = segment
        input_txt = mm.txt
        sr = SR(translation_engine=self.tf, processed_dict=self.parsed_dict, glob_sr=self.sr_global_dict, ref_list=self)
        trans = sr.parseAndTranslateText(loc, input_txt)
        is_fuzzy = sr.isFuzzy()
        is_ignore = sr.isIgnore()
        if trans:
            trans = cm.matchCase(input_txt, trans)
        return (loc, input_txt, trans, is_fuzzy, is_ignore)

    def translateOneLineOfText(self, input_txt):
        is_ignore = ig.isIgnored(input_txt)
        if is_ignore:
            return None, False, True

        trans = self.tf.isInDict(input_txt)
        if trans:
            return trans, False, False

        txt_list = pu.findInvert(df.PUNCTUATION_FINDER, input_txt)
        # dd('TRANSLATING LIST OF SEGMENTS:')
        # pp(txt_list)
        # dd('-' * 80)
        tran_list = []
        non_ignored_list = [(loc, mm) for (loc, mm) in txt_list.items() if not ig.isIgnored(mm.txt)]
        if not non_ignored_list:
            return None, False, True

        with concurrent.futures.ThreadPoolExecutor() as executor:
            found_results = executor.map(self.createSRAndTranslateSegment, non_ignored_list)

        found_result_list = list(found_results)

        tran_list = [(loc, trans, is_fuzzy, is_ignore) for (loc, input_txt, trans, is_fuzzy, is_ignore) in found_result_list if bool(trans)]
        translation = str(input_txt)
        is_ignore_list=[]
        is_fuzzy_list=[]
        if tran_list:
            tran_list.sort(reverse=True)
            for (loc, trans, is_fuzzy, is_ignore) in tran_list:
                is_ignore_list.append(is_ignore)
                is_fuzzy_list.append(is_fuzzy)
                translation = cm.jointText(translation, trans, loc)

        is_ignore = (False not in is_ignore_list)
        is_fuzzy = (True in is_fuzzy_list)
        return (translation, is_fuzzy, is_ignore)

    def translate(self):
        # RefType.ABBR:
        # RefType.ARCH_BRACKET:
        # RefType.CLASS:
        # RefType.DOC:
        # RefType.DOUBLE_GA:
        # RefType.FUNC:
        # RefType.FUNCTION:
        # RefType.GA_EMBEDDED_GA:
        # RefType.GENERIC_QUOTE:
        # RefType.GUILABEL:
        # RefType.KBD:
        # RefType.MATH:
        # RefType.MENUSELECTION:
        # RefType.METHOD:
        # RefType.MOD:
        # RefType.REF:
        # RefType.SINGLE_GA:
        # RefType.SUP:
        # RefType.TERM:
        # RefType.TEXT:

        def translateRefRecords(ref_list):
            non_txt_list = []
            for loc, mm_record in ref_list:
                is_ref = (mm_record.type != RefType.TEXT)
                if not is_ref:
                    continue
                entry = (loc, mm_record)
                non_txt_list.append(entry)

            for loc, mm_record in non_txt_list:
                self.translateMatcherRecord(mm_record)

        def collectTranslationsFromRefRecords(ref_list):
            tran_text = str(self.msg)
            mm_record: MatcherRecord = None
            for loc, mm_record in ref_list:
                trans = mm_record.translation
                has_tran = bool(trans)
                if has_tran:
                    tran_text = cm.jointText(tran_text, trans, loc)
            return tran_text

        def translateTextEntriesOnly():
            for loc, mm in self.items():
                is_txt = (mm.type == RefType.TEXT)
                if not is_txt:
                    continue

                txt = mm.getSubText()
                if not txt:
                    txt = mm.txt

                trans, is_fuzzy, is_ignore = self.translateOneLineOfText(txt)
                mm.setTranlation(trans, is_fuzzy, is_ignore)


        sent_translation = self.tf.isInDict(self.msg)
        if sent_translation:
            self.setTranslation(sent_translation, False, False)
            return

        mm_record: MatcherRecord = None
        is_translated = (self.translation_state != TranslationState.UNTRANSLATED)
        if is_translated:
            return

        ref_map = df.global_ref_map
        input_txt = self.msg
        has_ref = ref_map.hasMarkedLoc()
        if not has_ref:
            sent_translation, is_fuzzy, is_ignore = self.translateOneLineOfText(input_txt)
        else:
            tran_required_reversed_list = list(self.items())
            tran_required_reversed_list.sort(reverse=True)
            translateRefRecords(tran_required_reversed_list)

            is_all_translated = self.isAllTranslated()
            if not is_all_translated:
                translateTextEntriesOnly()

            sent_translation = collectTranslationsFromRefRecords(tran_required_reversed_list)
            # masking_string, masked_list = genMasks(input_txt)
            # trans, is_fuzzy, is_ignore = self.translateOneLineOfText(masking_string)
            # sent_translation = restoreMaskingString(trans, masked_list)

        is_fuzzy = self.isFuzzy()
        is_ignore = self.isIgnore()
        self.setTranslation(sent_translation, is_fuzzy, is_ignore)

    def translateMatcherRecord(self, mm: MatcherRecord, is_translating_arch_bracket=True):
        def find_function(entry):
            (ref_type, function) = entry
            mm_record: MatcherRecord = find_function.mm_record
            return (mm.type == ref_type) and (function is not None)

        tran_functions = [
            (RefType.ABBR, self.translateAbbrev),
            # (RefType.ARCH_BRACKET, self.translateArchBracket),
            # (RefType.CLASS, None),
            # (RefType.DOC, self.translateRefWithLink),
            # (RefType.DOUBLE_GA, self.translateRefWithLink),
            # (RefType.FUNC, None),
            # (RefType.FUNCTION, None),
            # (RefType.GA_EMBEDDED_GA, None),
            # (RefType.GENERIC_QUOTE, self.translateQuoted),
            # (RefType.GUILABEL, None),
            # (RefType.KBD, self.translateKeyboard),
            # (RefType.MATH, None),
            # (RefType.MENUSELECTION, self.translateMenuSelection),
            # (RefType.METHOD, None),
            # (RefType.MOD, None),
            # (RefType.REF, self.translateRefWithLink),
            # (RefType.SINGLE_GA, self.translateRefWithLink),
            # (RefType.SUP, None),
            # (RefType.TERM, self.translateRefWithLink),
            # (RefType.TEXT, self.translateArchBracket),
        ]
        try:
            find_function.mm_record = mm
            executable_list = list(filter(find_function, tran_functions))
            has_executable = bool(executable_list)
            if not has_executable:
                return False
            (ref_type, function) = executable_list[0]
            is_done = function(mm)
            return is_done
        except Exception as e:
            df.LOG(f'{e} ref_item:{mm}', error=True)

    def translateArchBracket(self, mm: MatcherRecord):
        input_txt = mm.txt
        trans, is_fuzzy, is_ignore = self.translateOneLineOfText(input_txt)
        mm.setTranlation(trans, is_fuzzy, is_ignore)
        return bool(trans)

    def translateKeyboard(self, mm: MatcherRecord):
        msg = mm.getSubText()
        orig = str(msg)
        trans = str(msg)
        kbd_dict = self.tf.kbd_dict

        result_dict = pu.patternMatchAll(df.KEYBOARD_SEP, msg)
        for sub_loc, sub_mm in result_dict.items():
            txt = sub_mm.txt
            has_dic = (txt in kbd_dict)
            if not has_dic:
                continue

            tr = kbd_dict[txt]
            if tr:
                trans = cm.jointText(trans, tr, sub_loc)

        is_fuzzy = False
        is_ignore = False
        is_the_same = (orig == trans)
        if is_the_same:
            trans = None
            is_fuzzy = True
        main_txt = mm.getMainText()
        trans = cm.jointText(main_txt, trans, mm.getSubLoc())
        mm.setTranlation(trans, is_fuzzy, is_ignore)
        return True

    def translateQuoted(self, mm: MatcherRecord):
        def formatTran(current_untran, current_tran):
            starter = ("" if is_blank_quote else mm.getStarter())
            ender = ("" if is_blank_quote else mm.getEnder())

            english_part = f'{current_untran}'
            translation_part = f'({current_tran})'
            body = f'{english_part} {translation_part}'
            tran = f'{starter}:abbr:`{body}`{ender}'
            return tran

        msg = mm.getSubText()
        is_blank_quote = (mm.type == RefType.BLANK_QUOTE)
        tran, is_fuzzy, is_ignore = self.translateOneLineOfText(msg)
        if is_ignore:
            return False

        if not tran:
            mm.setTranlation(None, is_fuzzy, is_ignore)
            return False

        tran = formatTran(msg, tran)
        mm.setTranlation(tran, is_fuzzy, is_ignore)
        return True

    def translateRefWithLink(self, mm: MatcherRecord, is_include_original_txt=True):
        # ref with link :ref:`contact <contribute-contact>` => :ref:`Liên Lạc (Contact) <contribute-contact>`
        # ref is link :ref:`ui-data-block`, :ref:`basic.raw_copy <rigify.rigs.basic.raw_copy>`, :ref:`bpy.ops.screen.redo_last`
        # :ref:`\"auto\" <curve-handle-type-auto>`
        #
        def formatTran(current_untran, current_tran):
            ref_type: RefType = mm.type
            has_ref = bool(ref_type)
            has_valid_ref_type = (has_ref and isinstance(ref_type, RefType))
            is_text_type = (has_valid_ref_type and ref_type == RefType.TEXT)
            is_bracket_or_quote = (has_valid_ref_type and (df.BRACKET_OR_QUOTE_REF.search(ref_type.name) is not None))
            is_ignore_type = (is_text_type or is_bracket_or_quote)
            is_formatting = (not is_ignore_type)
            if not is_formatting:
                return current_tran

            if is_include_original_txt:
                new_tran = f'{current_tran} ({current_untran})'
            else:
                new_tran = f'{current_tran}'
            return new_tran

        is_fuzzy = is_ignore = False
        tran = None

        is_using_main = False
        msg = mm.getSubText()
        if not msg:
            msg = mm.getMainText()
            is_using_main = True

        tran_collection = []
        tran_filled = False
        tran = None
        has_ref_link = (df.REF_LINK.search(msg) is not None)
        if not has_ref_link:
            tran, is_fuzzy, is_ignore = self.translateOneLineOfText(msg)
            valid = (bool(tran) and not is_ignore)
            if valid:
                tran = formatTran(msg, tran)
        else:
            found_dict = pu.findInvert(df.REF_LINK, msg)
            found_dict_list = list(found_dict.items())
            found_entry = found_dict_list[0]
            (sub_loc, sub_mm) = found_entry

            sub_txt = sub_mm.getMainText()
            tran, is_fuzzy, is_ignore = self.translateOneLineOfText(sub_txt)
            valid = (bool(tran) and not is_ignore)
            if valid:
                tran = formatTran(sub_txt, tran, has_ref_link=True)
                tran = cm.jointText(msg, tran, sub_loc)

        has_tran = bool(tran)
        if has_tran:
            translation = str(mm.getMainText())
            loc = (mm.getMainLoc() if is_using_main else mm.getSubLoc())
            tran = self.removeAbbrevInTran(tran)
            translation = cm.jointText(translation, tran, loc)
            mm.setTranlation(translation, is_fuzzy, is_ignore)
        return has_tran

    def translateMenuSelection(self, mm: MatcherRecord):
        def formatAbbrevTran(current_untran, current_tran):
            has_abbr = cm.hasAbbr(current_tran)
            if has_abbr:
                abbr_orig, abbr_marker, abbr_exp = cm.extractAbbr(current_tran)
                return_tran = cm.removeOriginal(current_untran, abbr_exp)
                return return_tran
            else:
                return current_tran

        def translateMenuItem(loc_word_list):
            for loc, mnu_item_mm in loc_word_list.items():
                sub_txt: str = mnu_item_mm.txt

                tran, is_fuzzy, is_ignore = self.translateOneLineOfText(sub_txt)

                if is_ignore:
                    continue

                tran = formatAbbrevTran(sub_txt, tran)

                is_tran_valid = (tran and (tran != sub_txt))
                if is_tran_valid:
                    is_sub_text_bracketed = sub_txt.startswith('(') and sub_txt.endswith(')')
                    if is_sub_text_bracketed:
                        tran_txt = f"{tran} {sub_txt}"
                    else:
                        tran_txt = f"{tran} ({sub_txt})"
                else:
                    tran_txt = f"({sub_txt})"

                mnu_item_mm.setTranlation(tran_txt, is_fuzzy, is_ignore)

        try:
            cm.debugging(mm.txt)
            msg = mm.getSubText()

            word_list = pu.findInvert(df.MENU_SEP, msg, is_reversed=True)
            translateMenuItem(word_list)

            trans = str(msg)
            tran_state_list=[]
            for loc, mnu_item_mm in word_list.items():
                trans = cm.jointText(trans, mnu_item_mm.translation, loc)
                tran_state_list.append(mnu_item_mm.translation_state)

            main_tran = mm.txt
            sub_loc = mm.getSubLoc()
            final_tran = cm.jointText(main_tran, trans, sub_loc)

            is_fuzzy = (TranslationState.FUZZY in tran_state_list)
            is_ignore = (TranslationState.IGNORED in tran_state_list)

            actual_ignore = ((not is_fuzzy) and is_ignore)
            mm.setTranlation(final_tran, is_fuzzy, actual_ignore)
            return True
        except Exception as e:
            df.LOG(f'{e} [{mm}]')
            raise e

    def removeAbbrevInTran(self, current_tran):
        if not current_tran:
            return None

        abbrev_mm = pu.patternMatch(df.ABBREV_PATTERN_PARSER, current_tran)
        if not abbrev_mm:
            return current_tran

        (abbr_loc, abbr_txt) = abbrev_mm.getSubEntryByIndex(0)
        abbrev_orig_rec, abbrev_part, exp_part = cm.extractAbbr(abbr_txt)
        abbrev_part_decoded = f'{abbrev_part} {exp_part}'
        abbs, abbe = abbr_loc
        left = current_tran[:abbs]
        right = current_tran[abbe:]
        new_tran = left + abbrev_part_decoded + right
        return new_tran

    def translateAbbrev(self, mm: MatcherRecord) -> list:
        '''
            translateAbbrev: Routine to parse abbreviation entry, such as:
            :abbr:`JONSWAP (JOint North Sea WAve Project)`.
            The routine will capture the part within brackets and translating
            that part, rejoins the translation with original text:
            'JONSWAP (JOint North Sea WAve Project -- <translation part>)'
        :param msg:
            text which contains the part within grave accents (GA), ie.
            JONSWAP (JOint North Sea WAve Project)
        :return:
            'JONSWAP (JOint North Sea WAve Project -- <translation part>)' if has translationm, else
            'JONSWAP (JOint North Sea WAve Project -- <translation part>)'
        '''

        sub_list = mm.getSubEntriesAsList()
        print(sub_list)
        return False

        msg = mm.getSubText()
        tran_txt = str(msg)
        first_match_mm: MatcherRecord = None
        all_matches = pu.patternMatchAll(df.ABBR_TEXT, msg)
        if not all_matches:
            return False

        all_matches_list = list(all_matches.items())
        first_match = all_matches_list[0]
        first_match_loc, first_match_mm = first_match

        abbrev_loc, abbrev_explain_txt = first_match_mm.getSubEntryByIndex(1)
        tran, is_fuzzy, is_ignore = self.translateOneLineOfText(abbrev_explain_txt)

        tran = self.removeAbbrevInTran(tran)
        valid = (tran and (tran != abbrev_explain_txt))
        if valid:
            translation = f"{abbrev_explain_txt}: {tran}"
        else:
            translation = f"{abbrev_explain_txt}: "

        tran_txt = cm.jointText(msg, translation, abbrev_loc)
        main_txt = mm.getMainText()
        sub_loc = mm.getSubLoc()
        final_tran = cm.jointText(main_txt, tran_txt, sub_loc)
        mm.setTranlation(final_tran, is_fuzzy, is_ignore)
        return True

    def translateAttrib(self, mm: MatcherRecord):
        def formatResult(orig_txt, tran_list):
            translation = str(orig_txt)
            tran_list.sort(reverse=True)
            for loc, sl_txt, tl_txt in tran_list:
                if tl_txt:
                    translation = cm.jointText(translation, tl_txt, loc)
            return translation

        orig_txt = str(mm.txt)
        translated_list=[]
        sub_list = mm.getSubEntriesAsList()
        interested_part = sub_list[1:]
        for loc, sl_txt in interested_part:
            (tl_txt, is_fuzzy, is_ignore) = self.translateOneLineOfText(sl_txt)
            entry = (loc, sl_txt, tl_txt)
            translated_list.append(entry)

        translation = formatResult(orig_txt, translated_list)
        mm.setTranlation(translation, True, False)
        return True
