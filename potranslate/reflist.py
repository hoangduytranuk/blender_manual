#!/usr/bin/env python3
import re
from translation_finder import TranslationFinder
from common import Common as cm, dd, pp, LocationObserver
from matcher import MatcherRecord
from ignore import Ignore as ig
from collections import defaultdict, OrderedDict
from reftype import RefType
from refrecord import RefRecord
from reftype import TranslationState
from refitem import RefItem

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
pattern_list = [
    (cm.ARCH_BRAKET_SINGLE_FULL, RefType.ARCH_BRACKET),
    (cm.PYTHON_FORMAT, RefType.PYTHON_FORMAT),
    (cm.FUNCTION, RefType.FUNCTION),
    (cm.AST_QUOTE, RefType.AST_QUOTE),
    (cm.DBL_QUOTE, RefType.DBL_QUOTE),
    (cm.SNG_QUOTE, RefType.SNG_QUOTE),
    (cm.GA_REF, RefType.GA),
]

def hasRef(txt) -> bool:
    simple_flag = False
    complicated_flag = False
    for pat, ref_type in pattern_list:
        has_ref = (pat.search(txt) is not None)
        is_function = (ref_type == RefType.FUNCTION)
        is_ga = (ref_type == RefType.GA)

        has_simple_ref = (has_ref and not (is_function or is_ga))
        has_complicated_ref = (has_ref and (is_function or is_ga))
        if has_simple_ref:
            simple_flag = True
        else:
            simple_flag = False

        if has_complicated_ref:
            complicated_flag = True

    return simple_flag, complicated_flag


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

    def findRecord(self, ref_record: RefRecord):
        for k, v in self.items():
            is_found = (v.isEquivalent(ref_record))
            if is_found:
                return v
        else:
            return None

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
        v : RefRecord = None
        translation_state_list.append(self.translation_state)
        for k, v in self.items():
            if v.isIgnore():
                translation_state_list.append(TranslationState.IGNORED)
            elif v.isFuzzy():
                translation_state_list.append(TranslationState.FUZZY)
            else:
                translation_state_list.append(TranslationState.ACCEPTABLE)
        return translation_state_list

    def isFuzzy(self):
        v:RefRecord = None
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

    def getType(self, xtype):
        for x in RefType:
            x_value = x.value
            has_type = (x_value == xtype)
            if has_type:
                return x
        else:
            return RefType.TEXT

    def getRefsAsList(self):
        ref_list = []
        v: RefRecord = None
        for k, v in self.items():
            v_ref_list = v.getRefListWithOriginalApplied()
            ref_list.extend(v_ref_list)
        return ref_list

    def getOrigLocList(self, alter_value=0, op=None):
        loc_list = []
        v: RefRecord = None
        for k, v in self.items():
            v_orig: RefItem = v.getOrigin()
            v_orig_txt = v_orig.text
            ss = cm.alterValue(v_orig.start, alter_value=alter_value, op=op)
            ee = ss + len(v_orig_txt)
            entry = RefItem(start=ss, end=ee, txt=v_orig_txt)
            loc_list.append(entry)
        return loc_list

    def removeRedundancies(self):
        loc_list = {}
        v: RefRecord = None
        for k, v in self.items():
            v_orig: RefItem = v.getOrigin()
            s, e = v_orig.getLocation()
            entry = {k: (s, e)}
            loc_list.update(entry)

        remove_list = []
        for k, v in loc_list.items():
            vs, ve = v  # remove
            for kk, vv in loc_list.items():
                is_same = (kk == k) and (vv == v)
                if is_same:
                    continue
                vvs, vve = vv  # keep
                is_remove = (vs > vvs) and (ve < vve) and (k not in remove_list)
                if is_remove:
                    remove_list.append(k)
        for k in remove_list:
            del self[k]

    def merge(self, other_list, alter_value=0, op=None):
        valid = (other_list is not None) and (len(other_list) > 0)
        if not valid:
            return

        remain_list = RefList(msg=other_list.msg, pat=other_list.pattern)
        other_loc_list = other_list.getOrigLocList(alter_value=alter_value, op=op)
        v: RefRecord = None
        for k, v in self.items():
            v_orig: RefItem = v.getOrigin()
            is_dupped = (v_orig in other_loc_list)
            if not is_dupped:
                remain_list.update({k: v})
        self.clear()
        self.update(remain_list)
        self.update(other_list)

    def alterOriginLocation(self, start: int, op: str):

        valid = op in "+-/*%="
        if not valid:
            return

        valid = (len(self) > 0)
        if not valid:
            return

        new_ref_list = RefList(msg=self.msg, pat=self.pattern)
        v: RefRecord
        new_v: RefRecord
        k = -1
        for k, v in self.items():
            v.alterOriginLocation(start, op=op)
            o_s, o_e = v.getOriginLocation()
            key = o_s
            new_ref_list.update({key: v})

        self.clear()
        self.update(new_ref_list)

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
        ref_record: RefRecord = None
        for k, ref_record in self.items():
            ref_record.parent = self

    def extractTextFromTextWithLink(self, k: str, loc:tuple, ref_type: RefType):
        dd(f'extractTextFromTextWithLink: k:{k}; loc:{loc} ref_type:{ref_type}')

        has_html = (cm.URL_LEADING_PATTERN.search(k) is not None)
        ref_link_find_pattern = (cm.REF_WITH_HTML_LINK if has_html else cm.REF_WITH_LINK)
        found_dict = cm.patternMatchAll(ref_link_find_pattern, k)
        if not found_dict:
            return None, None

        mmtxt: MatcherRecord = None
        mmlink: MatcherRecord = None
        txt = k
        actual_loc = loc
        try:
            mm_list = list(found_dict.items())
            item_count = len(mm_list)
            is_ignore = (item_count != 2)
            if is_ignore:
                return None, None

            txtloc, mmtxt = mm_list[0]
            (ts, te), txt = mmtxt.getOriginAsTuple()
            (os, oe) = loc
            ac_s = (os + ts)
            ac_e = (ac_s + len(txt))
            actual_loc = (ac_s, ac_e)

            linkloc, mmlink = mm_list[1]
            (ls, le), link = mmlink.getOriginAsTuple()
        except Exception as e:
            pass
        return txt, actual_loc

    def findOnePattern(self, msg: str, pattern: re.Pattern, reftype: RefType):
        ignored_dict={}
        result_list = RefList(msg=msg, pat=pattern)
        entry_orig = entry_type_or_open_symbol = entry_sub = entry_close_symbol = None

        valid_msg = (msg is not None) and (len(msg) > 0)
        valid_pattern = (pattern is not None)
        valid = valid_msg and valid_pattern
        if not valid:
            return result_list, ignored_dict
        try:
            is_bracket = (reftype == RefType.ARCH_BRACKET)
            if is_bracket:
                found_dict = cm.getTextWithinBrackets('(', ')', msg, is_include_bracket=False)
            else:
                found_dict = cm.patternMatchAll(pattern, msg)

            if not found_dict:
                return result_list, ignored_dict

            found_list = list(found_dict.items())
            mm: MatcherRecord = None
            for loc, mm in found_list:

                starter = ender = None
                is_regiter_starter = False
                mm_list = mm.getSubEntriesAsList()
                try:
                    entry_orig = mm_list[0]
                    entry_type_or_open_symbol = mm_list[1]
                    entry_sub = mm_list[2]
                    entry_close_symbol = mm_list[3]
                except Exception as e:
                    pass

                (sub_ss, sub_ee), sub_txt = entry_sub
                is_ignored = ig.isIgnored(sub_txt)
                if is_ignored:
                    entry={loc: mm}
                    ignored_dict.update(entry)
                    continue

                (type_ss, type_ee), type_or_start_part = entry_type_or_open_symbol
                actual_ref_type = reftype
                if bool(type_or_start_part):
                    rf = RefType.getRef(type_or_start_part)
                    actual_ref_type = (RefType.TEXT if (rf == None) else rf)
                    mm.type = actual_ref_type

                entry = {(mm.s, mm.e): mm}
                self.update(entry)
                #         is_regiter_starter = (cm.REF_TYPE_NAME_TO_REGISTER_STARTER_PAT.search(rf.name) is not None)
                #     starter = (type_or_start_part if is_regiter_starter else None)
                #
                # if entry_close_symbol:
                #     (ender_s, ender_e), ender = entry_close_symbol


                # (o_ss, o_ee), o_txt = entry_orig
                # orig_ref_item = RefItem(o_ss, o_ee, o_txt, ref_type=actual_ref_type, translation_finder=self.tf)
                #
                # actual_sub_ss = o_txt.find(sub_txt)
                # actual_sub_ee = actual_sub_ss + len(sub_txt)
                #
                # ref_item = RefItem(actual_sub_ss, actual_sub_ee, sub_txt, ref_type=actual_ref_type, translation_finder=self.tf, my_parent=orig_ref_item)
                # ref_item.ender_txt = ender
                # ref_item.starter_txt = starter
                #
                # if entry_close_symbol:
                #     (cl_ss, cl_ee), ender = entry_close_symbol
                # orig_ref_item.setStarterEnder(starter, ender)
                #
                # ref_record = RefRecord(origin=orig_ref_item, reflist=[ref_item], pat=pattern, my_parent=self)
                # print(f'ref_record: [{ref_record}]')
                # print('-' * 80)
                # orig_ref_item.parent = ref_record
                # entry = {(o_ss, o_ee): ref_record}
                # result_list.update(entry)

        except Exception as exception:
            dd("RefList.findPattern()")
            dd("pattern:", pattern)
            dd("text:", result_list.msg)
            dd(exception)
            raise exception
        return ignored_dict

    def isEmpty(self):
        is_empty = (len(self) == 0)
        return is_empty

    def inRange(self, item: RefRecord):
        valid = (item is not None)
        if not valid:
            return False

        i_s, i_e = item.getOriginLocation()
        i_txt = item.getOrigin().text
        # test_txt = "Mirror"
        v: RefRecord = None
        for k, v in self.items():
            r_s, r_e = v.getOriginLocation()
            r_txt = v.getOrigin().text

            is_in_range = (i_s >= r_s) and (i_e <= r_e)
            if is_in_range:
                item_origin: RefItem = item.getOrigin()
                v_first_record: RefItem = v.getRefItemByIndex(0)
                is_same = (item_origin == v_first_record)
                if is_same:
                    item_ref: RefItem = item.getRefItemByIndex(0)
                    item_ref.start += item_origin.start
                    v.clearRefList()
                    v.appendRefItem(item_ref)
                    dd("CAN REPLACE V's result BY ITEM'S RESULT")
                return True
        else:
            return False

    def diff(self, other_list: dict):
        loc_keep_list = RefList(msg=self.msg)
        v: RefRecord = None
        for k, v in other_list.items():
            in_forbidden_range: bool = self.inRange(v)
            if not in_forbidden_range:
                entry = {k: v}
                loc_keep_list.update(entry)

        return loc_keep_list

    def findPattern(self, pattern_list: list):
        count_item = 0
        p: re.Pattern = None
        ref_type: RefType = None
        m: re.Match = None
        pattern_list.reverse()
        obs = LocationObserver(str(self.msg))
        found_list_backup = []
        for index, item in enumerate(pattern_list):
            p, ref_type = item
            one_list, ignored_list = self.findOnePattern(obs.blank, p, ref_type)
            found_list_backup.extend(one_list)

            is_continue = not (one_list or ignored_list)
            if is_continue:
                continue

            loc_list=[]
            loc_list.extend(list(one_list.keys()))
            loc_list.extend(list(ignored_list.keys()))
            for loc in loc_list:
                obs.markedLocAsUsed(loc)

            if one_list:
                count_item += len(one_list)
                self.update(one_list)
        print('final:')
        pp(found_list_backup)
        print('end_final')
        sorted_list = sorted(list(self.items()))
        self.clear()
        self.update(sorted_list)
        return count_item, obs.getUnmarkedPartsAsDict()


    def testRecord(self, record: RefRecord):
        valid = (record is not None)
        if not valid:
            dd("testRecord: Unable to TEST, record is NONE")
            return

        orig = record.getOrigin()
        ref_list = record.getRefList()
        orig_txt = orig.text
        item: RefItem
        for item in ref_list:
            left = orig_txt[:item.start]
            right = orig_txt[item.end:]
            txt = left + item.text + right
            dd("original:", orig_txt)
            dd("ref_text:", txt)


    def findRefRecord(self, msg, entry_index, is_using_first_anyway=False, is_reversed_list=False):
        has_record = (len(self) > 0)
        if not has_record:
            return None

        is_ignore = ig.isIgnored(msg)
        if is_ignore:
            return None

        k_list = list(self.keys())
        k_len = len(k_list)
        if is_reversed_list:
            k_list = list(reversed(k_list))

        for k in k_list:
            v = self[k]
            v_txt = v.getOriginText()
            is_ignore = ig.isIgnored(v_txt)
            if is_ignore:
                return None

            is_in_left = cm.isTextuallySubsetOf(v_txt, msg)
            is_in_right = cm.isTextuallySubsetOf(msg, v_txt)
            is_matched = (is_in_left or is_in_right)
            if is_matched:
                dd("found_matched_ref:", v_txt, " for:", msg)
                return v

        if (entry_index < k_len):
            k = k_list[entry_index]
            v = self[k]
        elif (is_using_first_anyway and (k_len > 0)):
            k = k_list[0]
            v = self[k]
        else:
            v = None
        return v

    def transferRefRecordText(self, target_ref_list):
        un_transferred_list = {}
        v: RefRecord = None
        for k, v in self.items():
            v_txt = v.getOriginText()
            target_ref_record: RefRecord = target_ref_list.findRefRecord(v_txt)
            is_found = (target_ref_record is not None)
            if not is_found:
                entry = {k: v}
                un_transferred_list.update(entry)
                continue
            tran_txt = v.getOrigin().getTranslation()
            target_ref_record.getOrigin().setTranlation(tran_txt, v.isFuzzy(), v.isIgnore())
            dd("transferRefRecordText:", target_ref_record)
        return un_transferred_list

    def quotedToAbbrev(self, orig_txt):
        def balanceNumberOfItems(tran_list, orig_list):
            tran_len = len(tran_list)
            orig_len = len(orig_list)

            diff = abs(tran_len - orig_len)
            is_balanced = (diff == 0)
            if is_balanced:
                return False

            chosen_list = (tran_list if (tran_len < orig_len) else orig_list)
            chosen_list_keys = chosen_list.keys()
            has_key = len(chosen_list_keys) > 0
            if has_key:
                last_key = list(chosen_list_keys)[-1]
            else:
                last_key = 0

            for index in range(diff):
                ref_item = RefItem(start=-1, end=-1, txt=RefType.FILLER.value, ref_type=RefType.FILLER, translation_finder=self.tf)
                ref_rec = RefRecord(origin=ref_item)
                k = last_key + 1
                entry = {k: ref_rec}
                chosen_list.update(entry)

        def refSplit(ref_txt):
            ref_txt_list = ref_txt.split(cm.REF_SEP)
            has_len = (len(ref_txt_list) > 1)
            if not has_len:
                return ref_txt_list

            quote_char = ref_txt[0]
            has_second = (len(ref_txt) > 1) and (ref_txt[1] == quote_char)
            if has_second:
                quote_char = ref_txt[:2]

            left_side = ref_txt_list[0]
            right_side = ref_txt_list[1]

            is_filling = (left_side.startswith(quote_char) and not left_side.endswith(quote_char))
            if is_filling:
                left_side = left_side + quote_char
                ref_txt_list[0] = left_side

            is_filling = (right_side.endswith(quote_char) and not right_side.startswith(quote_char))
            if is_filling:
                right_side = quote_char + right_side
                ref_txt_list[1] = right_side
            return ref_txt_list

        orig_list = RefList(msg=orig_txt)
        orig_list.findPattern(pattern_list)

        self.findPattern(pattern_list)
        has_record = (len(self) > 0)
        if not has_record:
            return

        balanceNumberOfItems(self, orig_list)  # this will fill in 'filler' records, assingting search

        # dd('list of refs:')
        # pp(self)
        dd(f'quotedFindRefs, orig: [{orig_txt}]')
        dd(f'quotedFindRefs, tran: [{self.msg}]')

        new_txt = str(self.msg)
        v: RefRecord
        k_list = reversed(list(self.keys()))
        for index, k in enumerate(k_list):
            is_reverse = False
            ref_tran_txt = ref_orig_txt = None
            v = self[k]

            ref_orig = v.getOrigin()
            ref_list = v.getRefList()
            ref_type = ref_orig.getRefType()

            ref_orig_txt = ref_orig.getText()
            is_ignore = ig.isIgnored(ref_orig_txt)
            if is_ignore:
                dd(f'Ignoring [{ref_orig_txt}]')
                continue

            is_ast_quote = (ref_type == RefType.AST_QUOTE)
            is_dbl_quote = (ref_type == RefType.DBL_QUOTE)
            is_sng_quote = (ref_type == RefType.SNG_QUOTE)
            is_abbr = (ref_type == RefType.ABBR)  # # dealing with this later when switch to the test_dic.json
            is_arched_braket = (ref_type == RefType.ARCH_BRACKET)

            is_acceptable = (is_ast_quote or is_dbl_quote or is_sng_quote or is_abbr or is_arched_braket)

            if is_acceptable:
                pp(f'ref_orig:[{ref_orig}]')
                pp(f'ref:[{ref_list}]')

                is_reverse = ig.isReverseOrder(ref_orig_txt)

                ref_list_len = len(ref_list)
                has_ref = (ref_list_len > 0)
                has_more_than_one_ref_items = (ref_list_len > 1)
                if has_more_than_one_ref_items:
                    dd(f'ref list has more than one item:[{ref_list_len}]')

                if is_abbr:
                    first_ref_item = ref_list[0]
                    fis, fie, fi_txt = first_ref_item.getValues()
                    fi_word_list = cm.ABBREV_CONTENT_PARSER.findall(fi_txt)
                    existing_tran, existing_orig = fi_word_list[0]
                    orig_entry = orig_list.findRefRecord(existing_orig, index, is_reversed_list=True)
                    is_found_orig = (orig_entry is not None)
                    if not is_found_orig:  # item introduced while translating, ignore, since there are no possibility to identify the origin
                        dd(f'DEBUG: entry not in orig text:[{existing_orig} => [{existing_tran}]')
                        continue

                    orig_orig = orig_entry.getOrigin()
                    dd(f'DEBUG: found orig entry:[{orig_orig}], for the current:[{v}] and index: [{index}]')
                    continue
                elif has_ref:
                    first_ref_item = ref_list[0]
                    r_txt = first_ref_item.getText()
                    # ref_txt_list = r_txt.split(cm.REF_SEP)
                    ref_txt_list = refSplit(ref_orig_txt)  # keeping the original ast, double, single quote
                    has_ref_sep = (len(ref_txt_list) > 1)
                    if has_ref_sep:
                        ref_tran_txt = ref_txt_list[0]
                        ref_orig_txt = ref_txt_list[1]
                    else:
                        pp(f'first_ref_item:[{first_ref_item}]')
                        orig_entry = orig_list.findRefRecord(ref_orig_txt, index, is_reversed_list=True)
                        is_found_orig = (orig_entry is not None)
                        if is_found_orig:
                            orig_orig = orig_entry.getOrigin()
                            orig_ref_list = orig_entry.getRefList()
                            orig_orig_txt = orig_orig.getText()

                            ref_tran_txt = ref_orig_txt
                            ref_orig_txt = orig_orig_txt
                            os, oe = ref_orig.getLocation()
                        else:
                            dd(f"Unable to find original for [{ref_orig_txt}]")
                            r_txt = first_ref_item.getText()
                            os, oe = ref_orig.getLocation()
                            r_txt = cm.replaceArchedQuote(r_txt)

            is_change = (ref_tran_txt is not None) and (ref_orig_txt is not None)
            if is_change:
                ref_tran_txt = cm.replaceArchedQuote(ref_tran_txt)
                ref_orig_txt = cm.replaceArchedQuote(ref_orig_txt)

                is_trimming_first_char = (cm.LEADING_WITH_SYMBOL.search(ref_tran_txt) is not None)
                is_trimming_last_char = (cm.TRAILING_WITH_SYMBOL.search(ref_tran_txt) is not None)

                if is_trimming_first_char:
                    ref_tran_txt = cm.LEADING_WITH_SYMBOL.sub("", ref_tran_txt)
                    ref_orig_txt = cm.LEADING_WITH_SYMBOL.sub("", ref_orig_txt)

                if is_trimming_last_char:
                    ref_tran_txt = cm.TRAILING_WITH_SYMBOL.sub("", ref_tran_txt)
                    ref_orig_txt = cm.TRAILING_WITH_SYMBOL.sub("", ref_orig_txt)

                if is_reverse:
                    replacement = f':abbr:`{ref_orig_txt} ({ref_tran_txt})`'
                else:
                    replacement = f':abbr:`{ref_tran_txt} ({ref_orig_txt})`'

                # replacement = replaceQuoted(replacement)
                os, oe = ref_orig.getLocation()
                print(f'hello os:{os}, oe:{oe}')
                left_side = new_txt[:os]
                right_side = new_txt[oe:]
                new_txt = left_side + replacement + right_side
                dd(f'left_side:[{left_side}]')
                dd(f'right_side:[{right_side}]')
                dd(f'replacement:[{replacement}]')
                dd(f'new_txt:[{new_txt}]')
            dd()

        return new_txt

    # def transferTranslatedRefs(self, current_msg, current_tran):
    #     self.msg = current_msg
    #     pattern_list = [
    #         (cm.GA_REF, RefType.GA, True),  # this will have to further classified as progress
    #         (cm.AST_QUOTE, RefType.AST_QUOTE, True),
    #         (cm.DBL_QUOTE, RefType.DBL_QUOTE, True),
    #         (cm.SNG_QUOTE, RefType.SNG_QUOTE, True),
    #     ]
    #     self.findPattern(pattern_list)
    #     has_record = (len(self) > 0)
    #     if not has_record:
    #         dd("Message has refs, but translation DOESN'T")
    #         if self.keep_original:
    #             has_original = (current_msg in current_tran)
    #             if not has_original:
    #                 current_tran = cm.matchCase(current_msg, current_tran)
    #                 txt = f'{current_msg} -- {current_tran}'
    #                 self.setTranslation(txt, TranslationState.ACCEPTABLE)
    #             else:
    #                 txt = f'-- {current_msg}'
    #                 self.setTranslation(txt, TranslationState.FUZZY)
    #         else:
    #             self.setTranslation(current_tran, TranslationState.ACCEPTABLE)
    #         return None
    #
    #     sorted_list = sorted(list(self.items()))
    #     self.clear()
    #     self.update(sorted_list)
    #     self.translateRefList()
    #
    #     current_tran_reflist = RefList(msg=current_tran)
    #     current_tran_reflist.setTranslation(current_tran, current_tran_reflist.translation_state)
    #
    #     current_tran_reflist.findPattern(pattern_list)
    #
    #     sorted_list = sorted(list(current_tran_reflist.items()))
    #     current_tran_reflist.clear()
    #     current_tran_reflist.update(sorted_list)
    #
    #     un_transferred_list = self.transferRefRecordText(current_tran_reflist)
    #     tran = current_tran_reflist.transferTranslation(current_tran)
    #     current_tran_reflist.setTranslation(tran)
    #
    #     # dd("tran before:", current_tran)
    #     # dd("tran now:", current_tran_reflist.getTranslation())
    #
    #     has_untransferred = (un_transferred_list and len(un_transferred_list) > 0)
    #     if has_untransferred:
    #         dd("Untransferred:")
    #         pp(un_transferred_list)
    #     return un_transferred_list

    def findRefByText(self, txt):
        for index, item in enumerate(self.items()):
            k, v = item
            orig = v.getOrigin()
            s, e, otxt = orig.getValues()
            is_found = cm.isTextuallySimilar(otxt, txt)
            if is_found:
                return item
        else:
            return None

    def addUnparsedDict(self, unparsed_dict: dict):
        for uloc, utxt in unparsed_dict.items():
            us, ue = uloc
            orig = RefItem(start=us, end=ue, txt=utxt, ref_type=RefType.TEXT,
                               translation_finder=self.tf)
            sub = RefItem(start=0, end=len(utxt), txt=utxt, ref_type=RefType.TEXT,
                               translation_finder=self.tf, my_parent=orig)

            ref_rec = RefRecord(origin=orig, reflist=[sub], my_parent=self)
            orig.parent = ref_rec
            entry = {uloc: ref_rec}
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

        count, unparsed_dict = self.findPattern(pattern_list)
        self.addUnparsedDict(unparsed_dict)
        # # **** should break up sentences here
        # self.findTextOutsideRefs()
        dd('Finishing parseMessage:')

    def mergeTranslationToOrigin(self, ref_rec: RefRecord):
        orig_item: RefItem = ref_rec.getOrigin()
        ref_list = ref_rec.getRefList()
        if not ref_list:
            return

        tran_txt = str(orig_item.getText())
        ref_item: RefItem = None
        for ref_item in reversed(ref_list):
            tran_state = ref_item.translation_state
            is_ignore = (tran_state == TranslationState.IGNORED) or (tran_state == TranslationState.REMOVE)
            if is_ignore:
                continue

            tran = ref_item.getTranslation()
            if not tran:
                continue

            is_ignore_left_right = (ref_item.converted_to_abbr == True)
            s, e = ref_item.getLocation()

            if is_ignore_left_right:
                tran_txt = tran
            else:
                left_txt = tran_txt[:s]
                right_txt = tran_txt[e:]
                tran_txt = left_txt + tran + right_txt

        orig_item.setTranlation(tran_txt, False, False) # temporary acceptable. The isFuzzy or isIgnore will show up TRUE state

    def transferTranslation(self, msg):
        dd(f'transferTranslation:() msg:[{msg}]')
        tran = str(msg)
        v: RefRecord = None
        origin: RefItem = None
        temp_tran = str(msg)
        item_list = list(self.items())
        item_list.sort(reverse=True)
        translation_inserted = False
        for k, v in item_list:
            # self.mergeTranslationToOrigin(v)
            ref_list = v.getRefList()
            origin = v.getOrigin()
            ref_type = origin.getRefType()
            has_ref_list = bool(ref_list)

            otran: str = None
            if has_ref_list:
                is_dbl_quote = (ref_type == RefType.DBL_QUOTE)
                is_sng_quote = (ref_type == RefType.SNG_QUOTE)
                is_ast_quote = (ref_type == RefType.AST_QUOTE)

                is_quoted = (is_ast_quote or is_dbl_quote or is_sng_quote)

                first_item: RefItem = v.getRefItemByIndex(0)
                if is_quoted:
                    os, oe = origin.getLocation()
                else:
                    os, oe = first_item.getLocation()
                otran = first_item.getTranslation()
            else:
                os, oe = v.getOriginLocation()
                otran = v.getOrigin().getTranslation()

            has_tran = (otran is not None) and (len(otran) > 0)
            if not has_tran:
                continue

            temp_part = temp_tran[os:oe]
            translated_or_overlapped = (cm.FILLER_CHAR_PATTERN.search(temp_part) is not None)
            if translated_or_overlapped:
                temp_loc = (os, oe)
                dd(f'[{temp_part}] temp_loc:[{temp_loc}] is considered to be overlapped!')
                continue

            left = tran[:os]
            right = tran[oe:]
            tran = left + otran + right
            translation_inserted = True

            temp_blank = cm.FILLER_CHAR * (oe - os)
            temp_tran_left = temp_tran[:os]
            temp_tran_right = temp_tran[oe:]
            temp_blank = temp_tran_left + temp_blank + temp_tran_right
            dd(f'temp_tran_left:[{temp_tran_left}]')
            dd(f'temp_tran_right:[{temp_tran_right}]')

        if translation_inserted:
            return tran
        else:
            return None

    def translate(self):
        ref_record: RefRecord = None
        is_translated = (self.translation_state != TranslationState.UNTRANSLATED)
        if is_translated:
            return

        tran_text = str(self.msg)
        has_ref = (len(self) > 0)

        if not has_ref:
            trans, is_fuzzy, is_ignore = self.tf.translate(self.msg)
            if trans:
                if self.keep_original:
                    trans = cm.matchCase(self.msg, trans)
                    tran_text = f'{trans} -- {self.msg}'
                else:
                    tran_text = trans
            self.setTranslation(tran_text, is_fuzzy, is_ignore)
        else:
            tran_required_reversed_list = list(self.items())
            tran_required_reversed_list.sort(reverse=True)
            for k, ref_record in tran_required_reversed_list:
                ref_record.translate()

            # for k, ref_record in tran_required_reversed_list:
            #     orig = ref_record.getOrigin()
            #     is_ignored = (orig.translation_state == TranslationState.IGNORED)
            #     if is_ignored:
            #         continue
            #
            #     is_translated = (orig.translation_state != TranslationState.UNTRANSLATED)
            #     if is_translated:
            #         tran = orig.getTranslation()
            #         os, oe = orig.getLocation()
            #         left = tran_text[:os]
            #         right = tran_text[oe:]
            #         tran_text = left + tran + right

            has_translation = (tran_text != self.msg)
            if not has_translation:
                return

            tran_text = cm.matchCase(self.msg, tran_text)
            if self.keep_original:
                tran_text = f'{tran_text} -- {self.msg}'

            is_fuzzy = self.isFuzzy()
            is_ignored = self.isIgnore()
            self.setTranslation(tran_text, is_fuzzy, is_ignored)  # temporary acceptable, isFuzzy and isIgnore will show TRUE state

    def getListOfRefType(self, request_list_of_ref_type):
        ref_list=[]
        v : RefRecord = None
        for k, v in self.items():
            v_type = v.getOrigin().getRefType()
            is_found = (v_type in request_list_of_ref_type)
            if is_found:
                ref_list.append(v)
        return ref_list

    def getListOfKeyboard(self, is_translate=False):
        kbd_list = self.getListOfRefType([RefType.KBD])

        kbd_def = TranslationFinder.KEYBOARD_TRANS_DIC_PURE

        kbd_item : RefRecord = None
        new_list=[]
        for kbd_item in kbd_list:
            kbd_text_first_item : RefItem = kbd_item.getRefItemByIndex(0)
            kbd_text = kbd_text_first_item.getText()
            if is_translate:
                tran_kbd_text = self.tf.translateKeyboard(kbd_text)
                new_list.append(tran_kbd_text)
            else:
                new_list.append(kbd_text)
            # dd(f'orig_text:{kbd_text} => kbd_orig_text:{kbd_orig_text}')
        return new_list

    def getListOfRefs(self):
        ref_list = self.getListOfRefType([RefType.REF, RefType.DOC, RefType.GA])

        kbd_def = TranslationFinder.KEYBOARD_TRANS_DIC_PURE

        kbd_item : RefRecord = None
        new_list=[]
        for ref_item in ref_list:
            first_ref_item = ref_item.getRefItemByIndex(0)
            first_ref_item_text = first_ref_item.getText()
            has_separator = (cm.REF_SEP in first_ref_item_text)
            if has_separator:
                text_list = first_ref_item_text.split(cm.REF_SEP)
                first_ref_item_text = text_list[1]
            new_list.append(first_ref_item_text)

        return new_list

    def getListOfNonRefWords(self):
        text_only_list = self.getListOfRefType([RefType.TEXT])

        ref_item : RefRecord = None
        new_list=[]
        for ref_item in text_only_list:
            ref_text = ref_item.getOrigin().getText()
            word_list = cm.WORD_ONLY.findall(ref_text)
            for w in word_list:
                new_list.extend(word_list)
        return new_list

    def getListOfNonRefText(self):
        text_only_list = self.getListOfRefType([RefType.TEXT])
        new_list=[]
        for ref_item in text_only_list:
            ref_text = ref_item.getOrigin().getText()
            new_list.append(ref_text)
        return new_list
