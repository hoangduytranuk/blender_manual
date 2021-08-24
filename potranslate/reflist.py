#!/usr/bin/env python3
import re
from definition import Definitions as df, RefType, TranslationState
from common import Common as cm, dd, pp, LocationObserver
from matcher import MatcherRecord
from ignore import Ignore as ig
from collections import defaultdict, OrderedDict
from sentence import StructRecogniser as SR
from nocasedict import NoCaseDict as NDIC
import concurrent.futures

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

    def setParentForChildren(self):
        for k, mm in self.items():
            mm.parent = self

    def findOnePattern(self, msg: str, pattern: re.Pattern, reftype: RefType):
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
        found_dict = OrderedDict()
        try:
            found_dict = getMatches(pattern, msg, reftype)
            if found_dict:
                self.update(found_dict)
        except Exception as e:
            df.LOG(f'{e} msg:[{msg}]; found_dict:[{found_dict}]', error=True)
            raise e


    def isEmpty(self):
        is_empty = (len(self) == 0)
        return is_empty

    def cleanupBrackets(self):
        mm: MatcherRecord = None
        remove_list = []
        obs = LocationObserver(self.msg)
        for loc, mm in self.items():
            ref_type = mm.type
            is_bracket = (ref_type == RefType.ARCH_BRACKET)
            if is_bracket:
                continue

            obs.markLocAsUsed(loc)

        for loc, mm in self.items():
            ref_type = mm.type
            is_bracket = (ref_type == RefType.ARCH_BRACKET)
            if not is_bracket:
                continue

            txt = mm.txt
            is_fully_used = obs.isLocFullyUsed(loc)
            if is_fully_used:
                dd(f'REMOVING: [{mm}]')
                remove_list.append(loc)

        for loc in remove_list:
            del self[loc]

    def findPattern(self, pattern_list: list, txt: str):
        pattern_list.reverse()
        for index, item in enumerate(pattern_list):
            p, ref_type = item
            self.findOnePattern(txt, p, ref_type)

        self.cleanupBrackets()
        return len(self)

    def getListOfRefType(self, request_list_of_ref_type):
        ref_list=[]
        for mm_loc, mm in self.items():
            type = mm.type
            is_found = (type in request_list_of_ref_type)
            if is_found:
                ref_list.append(mm)
        return ref_list

    def addUnparsedDict(self, unparsed_dict: dict):
        mm: MatcherRecord = None
        for uloc, mm in unparsed_dict.items():
            (ms, me) = mm.getMainLoc()
            mtxt = mm.getMainText()

            left, mid, right = cm.getTextWithin(mtxt)
            is_all_symbols = (not bool(mid))

            is_ignored = (is_all_symbols)
            if is_ignored:
                continue

            mm = MatcherRecord(s=ms, e=me, txt=mtxt)
            mm.addSubMatch(-1, -1, None)
            mm.addSubMatch(0, len(mtxt), mtxt)
            mm.type = RefType.TEXT
            entry = {uloc: mm}
            self.update(entry)

    def parseMessage(self):
        # trans = self.tf.isInDict(self.msg)
        # if trans:
        #     self.setTranslation(trans, False, False)
        #     return

        local_msg = str(self.msg)
        cm.debugging(local_msg)
        count = self.findPattern(df.pattern_list, local_msg)

        df.global_ref_map = LocationObserver(self.msg)
        for loc, mm in self.items():
            df.global_ref_map.markLocAsUsed(loc)
        unparsed_dict = df.global_ref_map.getUnmarkedPartsAsDict()
        self.addUnparsedDict(unparsed_dict)

        if len(self):
            dd('Finishing parseMessage:')
            dd('-' * 80)
            for loc, mm_rec in self.items():
                dd(f'{loc}')
                dd(f'{mm_rec.txt}')
                dd('-' * 80)

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
        trans = self.tf.isInDict(input_txt)
        if trans:
            return trans, False, False

        txt_list = cm.findInvert(df.SPLIT_SENT_PAT, input_txt)
        dd('TRANSLATING LIST OF SEGMENTS:')
        pp(txt_list)
        dd('-' * 80)
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
        def restoreMaskingString(trans, mask_list):
            if bool(trans):
                new_tran = str(trans)
                mask_list_with_loc = []
                mm: MatcherRecord = None
                for loc, new_mask, mm_txt, mm in mask_list:
                    ss = trans.find(new_mask)
                    ee = ss + len(new_mask)
                    mm_tran = mm.translation
                    valid_tran = (mm_tran and mm_tran != mm_txt)
                    if not valid_tran:
                        mm_tran = mm_txt
                    mask_loc = (ss, ee)
                    mask_list_with_loc_entry = (mask_loc, mm_txt, mm_tran)
                    mask_list_with_loc.append(mask_list_with_loc_entry)

                mask_list_with_loc.sort(reverse=True)

                for (mask_loc, mm_txt, mm_tran) in mask_list_with_loc:
                    new_tran = cm.jointText(new_tran, mm_tran, mask_loc)
            else:
                new_tran = str(self.msg)
                ref_list = list(self.items())
                ref_list.sort(reverse=True)
                for loc, mm in ref_list:
                    trans_txt = mm.translation
                    if trans_txt:
                        new_tran = cm.jointText(new_tran, trans_txt, loc)
            return new_tran

        def genMasks(txt):
            temp_txt = str(txt)
            mask_table = []
            # letters = string.digits
            item_list = list(self.items())
            item_list.sort(reverse=True)

            for index, (loc, mm) in enumerate(item_list):
                mm_type = mm.type
                is_txt = (mm_type == RefType.TEXT)
                if is_txt:
                    continue

                mm_txt = mm.txt
                txt_len = len(mm_txt)
                # new_mask = (''.join(random.choice(letters) for i in range(txt_len)))
                new_mask = f'{index}{df.REF_MASK_STR}'
                mask_table_entry = (loc, new_mask, mm_txt, mm)
                mask_table.append(mask_table_entry)

                temp_txt = cm.jointText(temp_txt, new_mask, loc)

            return temp_txt, mask_table

        def getTextDirectTranslations(ref_list):
            for loc, mm_record in ref_list:
                is_txt = (mm_record.type == RefType.TEXT)
                if not is_txt:
                    continue
                mm_txt = mm_record.txt
                tran = self.tf.isInDict(mm_txt)
                is_translated = bool(tran)
                if is_translated:
                    mm_record.setTranlation(tran, False, False)

        def translateRefRecords(ref_list):
            for loc, mm_record in ref_list:
                is_ref = (mm_record.type != RefType.TEXT)
                if not is_ref:
                    continue
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
            # getTextDirectTranslations(tran_required_reversed_list)

            is_all_translated = self.isAllTranslated()
            if is_all_translated:
                sent_translation = collectTranslationsFromRefRecords(tran_required_reversed_list)
            else:
                masking_string, masked_list = genMasks(input_txt)
                trans, is_fuzzy, is_ignore = self.translateOneLineOfText(masking_string)
                sent_translation = restoreMaskingString(trans, masked_list)

        is_fuzzy = self.isFuzzy()
        is_ignore = self.isIgnore()
        self.setTranslation(sent_translation, is_fuzzy, is_ignore)

    def translateMatcherRecord(self, mm: MatcherRecord, is_translating_arch_bracket=True):
        sub_loc: tuple = None
        try:
            ref_txt = mm.txt
            ref_type = mm.type

            is_guilabel = (ref_type == RefType.GUILABEL)
            is_arch_bracket = (ref_type == RefType.ARCH_BRACKET)
            is_blank_quote = (ref_type == RefType.BLANK_QUOTE)
            is_kbd = (ref_type == RefType.KBD)
            is_abbr = (ref_type == RefType.ABBR)
            is_menu = (ref_type == RefType.MENUSELECTION)
            is_ga = (ref_type == RefType.GA)
            is_ref = (ref_type == RefType.REF)
            is_doc = (ref_type == RefType.DOC)
            is_osl_attrib = (ref_type == RefType.OSL_ATTRIB)
            is_term = (ref_type == RefType.TERM)
            is_math = (ref_type == RefType.MATH)

            # ----------
            is_ast = (ref_type == RefType.AST_QUOTE)
            is_dbl_ast_quote = (ref_type == RefType.DBL_AST_QUOTE)
            is_dbl_quote = (ref_type == RefType.DBL_QUOTE)
            is_sng_quote = (ref_type == RefType.SNG_QUOTE)
            is_python_format = (ref_type == RefType.PYTHON_FORMAT)
            is_function = (ref_type == RefType.FUNCTION)
            is_attrib = (ref_type == RefType.ATTRIB)

            is_quoted = (is_ast or is_dbl_quote or is_sng_quote or is_dbl_ast_quote or is_blank_quote)

            is_ignore = (is_osl_attrib or is_python_format or is_function or is_math)
            if is_ignore:
                return

            converted_to_abbr = False
            if is_kbd:
                dd(f'translateRefItem: is_kbd:{ref_txt}')
                ok = self.translateKeyboard(mm)
            elif is_abbr:
                dd(f'translateRefItem: is_abbr:{ref_txt}')
                ok = self.translateAbbrev(mm)
            elif is_menu:
                dd(f'translateRefItem: is_menu:{ref_txt}')
                ok = self.translateMenuSelection(mm)
            elif is_quoted:
                dd(f'translateRefItem: is_quoted:{ref_txt}')
                ok = self.translateQuoted(mm)
            elif is_attrib:
                dd(f'translateRefItem: is_attrib:{ref_txt}')
                ok = self.translateAttrib(mm)
            elif is_arch_bracket:
                ok = self.translateArchBracket(mm)
            else:
                is_include_original = not( is_guilabel )
                ok = self.translateRefWithLink(mm, is_include_original_txt=is_include_original)

        except Exception as e:
            df.LOG(f'{e} ref_item:{mm}, ref_type:{ref_type}', error=True)


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

        result_dict = cm.patternMatchAll(df.KEYBOARD_SEP, msg)
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

            explanation_part = f'({starter}{current_untran}{ender})'
            abbrev_part = f'{starter}{current_tran}{ender}'
            body = f'{abbrev_part} {explanation_part}'
            tran = f':abbr:`{body}`'
            return tran

        msg = mm.getSubText()
        is_blank_quote = (mm.type == RefType.BLANK_QUOTE)
        # is_fuzzy = False
        # is_ignore = self.checkIgnore(msg)
        # if is_ignore:
        #     return False

        tran, is_fuzzy, is_ignore = self.translateOneLineOfText(msg)
        if is_ignore:
            return False

        if not tran:
            mm.setTranlation(None, is_fuzzy, is_ignore)
            return False

        is_abbrev = cm.patternMatch(df.ABBREV_PATTERN_PARSER, tran)
        if not is_abbrev:
            tran = cm.removeOriginal(msg, tran)
            tran = formatTran(msg, tran)

        mm.setTranlation(tran, is_fuzzy, is_ignore)
        return True

    def translateRefWithLink(self, mm: MatcherRecord, is_include_original_txt=True):
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
            found_dict = cm.findInvert(df.REF_LINK, msg, is_reversed=True)
            found_dict_list = list(found_dict.items())
            found_entry = found_dict_list[0]
            (sub_loc, sub_mm) = found_entry

            sub_txt = sub_mm.getMainText()
            tran, is_fuzzy, is_ignore = self.translateOneLineOfText(sub_txt)
            valid = (bool(tran) and not is_ignore)
            if valid:
                tran = formatTran(sub_txt, tran)
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

            word_list = cm.findInvert(df.MENU_SEP, msg, is_reversed=True)
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

        abbrev_mm = cm.patternMatch(df.ABBREV_PATTERN_PARSER, current_tran)
        if not abbrev_mm:
            return current_tran

        new_tran = str(current_tran)
        (abbr_loc, abbr_txt) = abbrev_mm.getSubEntryByIndex(0)
        abbrev_orig_rec, abbrev_part, exp_part = cm.extractAbbr(abbr_txt)
        new_tran = f'{abbrev_part} {exp_part}'
        # new_tran = cm.jointText(new_tran, exp_part, abbr_loc)
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

        msg = mm.getSubText()
        tran_txt = str(msg)
        first_match_mm: MatcherRecord = None
        all_matches = cm.patternMatchAll(df.ABBR_TEXT, msg)
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

    # def translateOSLAttrrib(self, msg: str):
    #     if not msg:
    #         return None, False, False
    #
    #     tran_txt = str(msg)
    #     is_fuzzy_list=[]
    #     is_ignore_list=[]
    #     word_list_dict = cm.findInvert(df.COLON_CHAR, tran_txt, is_reversed=True)
    #     word_list_count = len(word_list_dict)
    #     for loc, orig_txt in word_list_dict.items():
    #         s, e = loc
    #         tran, is_fuzzy, is_ignore = self.translateOneText(orig_txt)
    #         is_fuzzy_list.append(is_fuzzy)
    #         is_ignore_list.append(is_ignore)
    #         has_tran = (tran and tran != orig_txt)
    #         if has_tran:
    #             left = tran_txt[:s]
    #             right = tran_txt[e:]
    #             tran_txt = left + tran + right
    #
    #     has_tran = (tran_txt != msg)
    #     if not has_tran:
    #         tran_txt = f'{msg} -- '
    #         return None, False, False
    #     else:
    #         is_fuzzy = (True in is_fuzzy_list)
    #         is_ignore = (not is_fuzzy) and (True in is_ignore_list) and (False not in is_ignore_list)
    #         tran_txt = f'{msg} ({tran_txt})'
    #         return tran_txt, is_fuzzy, is_ignore

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
