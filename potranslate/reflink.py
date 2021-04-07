#!/usr/bin/env python3
import sys
# sys.path.append('/usr/local/lib/python3.7/site-packages')
# sys.path.append('/Users/hoangduytran/blender_manual/potranslate')

import re
from common import Common as cm, MatcherRecord, OverLappingState, dd, pp
from ignore import Ignore as ig
from collections import defaultdict, OrderedDict
from translation_finder import TranslationFinder, LocationObserver
# from pyparsing import nestedExpr
from enum import Enum
from reftype import RefType
from copy import copy, deepcopy

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


class TranslationState(Enum):
    UNTRANSLATED = 0
    ACCEPTABLE = 1
    FUZZY = 2
    IGNORED = 3
    REMOVE = 4


class TextStyle(Enum):
    NORMAL = 0
    ITALIC = 1
    BOLD = 2
    BOX = 3
    RAW = 4

pattern_list = [
    (cm.ARCH_BRAKET_SINGLE_FULL, RefType.ARCH_BRACKET),
    (cm.PYTHON_FORMAT, RefType.PYTHON_FORMAT),
    (cm.FUNCTION, RefType.FUNCTION),
    (cm.GA_REF, RefType.GA),
    (cm.AST_QUOTE, RefType.AST_QUOTE),
    (cm.DBL_QUOTE, RefType.DBL_QUOTE),
    (cm.SNG_QUOTE, RefType.SNG_QUOTE),
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

class RefItem:

    def __init__(self, start=-1, end=-1, txt=None, ref_type=RefType.TEXT, keep_orig=False):
        self.start: int = start
        self.end: int = end
        self.text: str = txt
        self.translation: str = None
        self.old_translation: str = None
        self.translation_state: TranslationState = TranslationState.UNTRANSLATED
        self.translation_include_original: bool = keep_orig
        self.reftype: RefType = ref_type
        self.text_style: TextStyle = TextStyle.NORMAL
        self.converted_to_abbr = False

    def __repr__(self):
        result = "(" + str(self.start) + ", " + \
                 str(self.end) + ", " + \
                 self.text + ", [TYPE]" + \
                 self.reftype.name + ", [STYLE]" + \
                 self.text_style.name + ", [INC]" + \
                 str(self.translation_include_original) + \
                 ")"
        if self.translation:
            result += "\n[TRANS]:(" + self.translation + ")[" + str(self.getTranslationState()) + "]"
        return result

    def __eq__(self, other):
        valid = (other is not None) and (isinstance(other, RefItem))
        if not valid:
            return False

        is_equal = (self.start == other.start) and \
                   (self.end == other.end) and \
                   (self.text == other.text) and \
                   (self.reftype == other.reftype)
        return is_equal

    def isIquivalent(self, other):
        if not other:
            return False

        is_same_type = (self.reftype == other.reftype)
        this_has_text = (self.text and len(self.text) > 0)
        other_has_text = (other.text and len(other.text) > 0)

        text_in_other = this_has_text and \
                        other_has_text and \
                        (self.text in other.text)
        other_text_in_this =  this_has_text and \
                        other_has_text and \
                        (other.text in self.text)
        is_equipvalent = is_same_type and (text_in_other or other_text_in_this)
        return is_equipvalent

    def textContain(self, search_txt):
        if self.text is None:
            return False
        return (search_txt in self.text)

    def getLocation(self):
        return self.start, self.end

    def setLocation(self, s, e):
        self.start = s
        self.end = e

    def setStart(self, s):
        self.start = s
        has_text = (self.txt is not None) and (len(self.text) > 0)
        if has_text:
            text_len = len(self.text)
            self.end = self.start + text_len

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text

    def getTranslationState(self):
        return self.translation_state

    def setTranslationState(self, state: TranslationState):
        self.translation_state = state

    def getTranslation(self):
        return self.translation

    def setTranlation(self, tran, is_fuzzy: bool, is_ignore: bool):
        if not tran:
            tran = ""

        self.translation = tran

        st = TranslationState.ACCEPTABLE
        if is_fuzzy:
            st = TranslationState.FUZZY
        elif is_ignore:
            st = TranslationState.IGNORED
        self.setTranslationState(st)

    def getValues(self):
        return self.start, self.end, self.text

    def setValues(self, start, end, txt):
        self.start = start
        self.end = end
        self.text = txt

    def getRefType(self):
        return self.reftype

    def setRefType(self, ref_type: RefType):
        self.reftype = ref_type

    def setIncludeOriginal(self, flag=True):
        self.translation_include_original = flag

    def isIncludeOriginal(self):
        return self.translation_include_original

    def getTextForKeyboard(self):
        item_list = {}
        found_dict = cm.patternMatchAll(cm.KEYBOARD_SEP, self.getText())
        for loc, mm in found_dict.items():
            (s, e), txt = mm.getOriginAsTuple()
            entry = {s: (s, e, txt)}
            item_list.update(entry)
        return item_list

    def getTextForGenericRef(self):
        item_list = {}

        msg = self.getText()
        is_pure_path = (cm.PURE_PATH.search(msg) is not None)
        is_pure_ref = (cm.PURE_REF.search(msg) is not None)
        is_api_ref = (cm.API_REF.search(msg) is not None)
        is_keep = (ig.isKeep(msg))
        is_keep_contain = (ig.isKeepContains(msg))
        is_ignore = (is_pure_path or is_pure_ref or is_api_ref) and (not (is_keep or is_keep_contain))
        if is_ignore:
            return item_list

        has_ref_link = (cm.REF_LINK.search(msg) is not None)
        if has_ref_link:
            found_list = cm.findInvert(cm.REF_LINK, msg)
            for k, v in reversed(list(found_list.items())):
                s, e, orig_txt = v
                entry = {s: (s, e, orig_txt)}
                item_list.update(entry)
        else:
            entry = {0: (0, len(msg), msg)}
            item_list.update(entry)
        return item_list

    def isOverlapped(self, other):
        this_s = self.start
        this_e = self.end

        other_s = other.start
        other_e = other.end

        is_start_ovrlap = (other_s <= this_s <= other_e)
        is_end_overlap = (other_s <= this_e <= other_e)
        is_overlap = (is_start_ovrlap or is_end_overlap)

        # max_end = max(this_e, other_e)
        # mask = (' ' * max_end)
        #
        # other_part = (cm.FILLER_CHAR * other_e - other_s)
        # mask_left = mask[:other_s] + other_part + mask[other_e:]
        # this_part = mask[this_s: this_e]
        # is_overlap = (cm.FILLER_CHAR_PATTERN.search(this_part) is not None)
        return is_overlap

    def coverDistance(self):
        this_s = self.start
        this_e = self.end
        this_covering_distance = (this_e - this_s)
        return this_covering_distance

    def compareCoveringDistance(self, other, is_less=False, is_equal=False):
        this_covering_distance = self.coverDistance()
        other_covering_distance = other.coverDistance()
        if is_less and not is_equal:
            return_result = (this_covering_distance < other_covering_distance)
        elif is_less and is_equal:
            return_result = (this_covering_distance <= other_covering_distance)
        elif not is_less and not is_equal:
            return_result = (this_covering_distance > other_covering_distance)
        elif not is_less and is_equal:
            return_result = (this_covering_distance >= other_covering_distance)
        return return_result

    def __lt__(self, other):
        return self.compareCoveringDistance(other, is_less=True)

    def __le__(self, other):
        return self.compareCoveringDistance(other, is_less=True, is_equal=True)

    def __gt__(self, other):
        return self.compareCoveringDistance(other, is_less=False)

    def __ge__(self, other):
        return self.compareCoveringDistance(other, is_less=False, is_equal=True)

    def __sub__(self, other):
        '''
            subtract this from the other by reducing text length and change locations
            :param other    other instance of RefItem
        '''

        this_s = self.start
        this_e = self.end

        other_s = other.start
        other_e = other.end

        min_start = min(this_s, other_s)
        max_end = max(this_e, other_e)
        mask_orig = (' ' * max_end)

        start_part = (cm.FILLER_CHAR * min_start)
        other_part = (cm.FILLER_CHAR * other_e - other_s)
        mask = start_part + mask_orig[min_start:]
        mask = mask[:other_s] + other_part + mask[other_e:]

        this_part = mask[this_s: this_e]
        # spaces to keep, FILLER_CHAR to remove
        this_txt = self.text
        list_of_remain = cm.patternMatchAll(cm.SPACES, this_part)
        this_keeping_txt_list = []
        for loc, mm in list_of_remain:
            (s, e), spaces = mm.getOriginAsTuple()
            txt_part = this_txt[s:e]
            is_not_worth_keeping = (cm.SYMBOLS_ONLY.search(txt_part) is not None)
            if is_not_worth_keeping:
                continue

            start_count, end_count, new_txt_part = cm.stripSpaces(txt_part)
            new_loc = (s + start_count, e - end_count)
            entry = (new_loc, new_txt_part)
            this_keeping_txt_list.append(entry)

        result_list = []
        for loc, remain_txt in this_keeping_txt_list:
            copy_of_this: RefItem = deepcopy(self)
            s, e = loc
            copy_of_this.setValues(start=s, end=e, txt=remain_txt)
            result_list.append(copy_of_this)

        # this list could be empty, in which case remove left part, keep the right part (A - B = empty => keep B only)
        return result_list


class RefRecord:
    def __init__(self, origin: RefItem = None, reflist: list = [], pat=None):
        self.origin: RefItem = origin
        self.reflist: list = reflist
        self.pattern: str = pat
        # self.setOriginType()

    def __repr__(self):
        result = ""
        if self.origin:
            result += ":" + str(self.origin) + ":"
            if self.reflist and (len(self.reflist) > 0):
                result += "{"
                for i in self.reflist:
                    result += str(i)
                result += "}"
        return result

    def setValues(self, origin: RefItem = None, reflist: list = [], pat=None):
        self.origin: RefItem = origin
        self.reflist: list = reflist
        self.pattern: str = pat

    def getTranslateStateList(self):
        state_list = []
        if self.origin:
            state_list.append(self.origin.translation_state)

        is_check_fuzzy_on_ref_list = bool(self.reflist)
        if is_check_fuzzy_on_ref_list:
            for ref_item in self.reflist:
                state_list.append(ref_item.translation_state)
        return state_list

    def isFuzzy(self):
        state_list = self.getTranslateStateList()
        has_ignored = (TranslationState.IGNORED in state_list)
        has_fuzzy = (TranslationState.FUZZY in state_list)

        is_fuzzy = (has_ignored or has_fuzzy)
        return is_fuzzy

    def isIgnore(self):
        state_list = self.getTranslateStateList()
        has_ignored = (TranslationState.IGNORED in state_list)
        has_fuzzy = (TranslationState.FUZZY in state_list)
        has_acceptable = (TranslationState.ACCEPTABLE in state_list)

        is_ignore = has_ignored and not (has_fuzzy or has_acceptable)
        return is_ignore

    def isOverLapped(self, other):
        this_orig = self.getOrigin()
        other_orig = other.getOrigin()
        is_ovrlap = this_orig.isOverlapped(other_orig)
        return is_ovrlap

    def __sub__(self, other):
        result_list = []

        this_orig = self.getOrigin()
        other_orig = other.getOrigin()
        result_orig_list = this_orig - other_orig

        for orig_item in result_orig_list:
            new_entry: RefRecord = deepcopy(self)
            new_entry.setValues(origin=orig_item, reflist=[])
            result_list.append(new_entry)

        return result_list
        # this_ref_list = self.getRefList()
        # other_ref_list = other.getRefList()

    def isIquivalent(self, other):
        if other is None:
            return False

        has_origin = (self.origin and other.origin)
        if not has_origin:
            return False

        is_equivalent = (self.origin.isEquivalent(other.origin))
        return is_equivalent

    def setOriginType(self):
        orig_item = self.getOrigin()
        has_orig = (orig_item is not None) and (orig_item.getText() is not None)
        if not has_orig:
            return False

        is_special = cm.isSpecialTerm(orig_item.getText())
        is_ended_with_dot = orig_item.getText().endswith('.)')
        if is_special and not is_ended_with_dot:
            orig_item.setRefType(RefType.REF)

    def getRefListWithOriginalApplied(self):
        ref_list = []
        orig = self.getOrigin()
        o_s, o_e, o_txt = orig.getValues()
        for item in self.reflist:
            i_txt = item.text
            ss = item.start + o_s
            ee = ss + len(i_txt)
            ref_entry = RefItem(start=ss, end=ee, txt=i_txt, )
            ref_list.append(ref_entry)
        return ref_list

    def getRefLocationList(self, alter_value=0, op=None):
        loc_list = []
        altering = (op is not None)
        for item in self.reflist:
            txt = item.text
            ss = cm.alterValue(item.start, alter_value=alter_value, op=op)
            ee = ss + len(txt)
            loc_item = (ss, ee)
            loc_list.append(loc_item)
        return loc_list

    def alterOriginLocation(self, start, op=None):
        try:
            self.origin.start = cm.alterValue(self.origin.start, alter_value=start, op=op)
            self.origin.end = self.origin.start + len(self.origin.text)
        except Exception as e:
            pass

    def clearRefList(self):
        self.reflist.clear()

    def getRefItemByIndex(self, index):
        ref_len = len(self.reflist)
        valid = (index >= 0) and (index < ref_len)
        item = (self.reflist[index] if valid else None)
        return item

    def appendRefItem(self, ref_list_item: RefItem = None):
        valid = (ref_list_item is not None)
        if not valid:
            return
        self.reflist.append(ref_list_item)

    def getOrigin(self):
        return self.origin

    def getRefList(self):
        return self.reflist

    def isRefEmtpy(self):
        return (self.getRefList() is None) or (len(self.getRefList()) == 0)

    def getOriginLocation(self):
        org = self.getOrigin()
        valid = (org is not None)
        if not valid:
            return -1, -1
        else:
            return org.start, org.end

    def getOriginText(self):
        org = self.getOrigin()
        valid = (org is not None)
        if not valid:
            return None
        else:
            return org.text

    def getOriginValues(self):
        org = self.getOrigin()
        valid = (org is not None)
        if not valid:
            return -1, -1, None
        else:
            return org.start, org.end, org.text

    def isEmptyOrigin(self):
        is_empty = (self.origin is None)
        if is_empty:
            return True
        s, e, t = self.getOriginValues()
        is_empty = (s == -1) or (e == -1)
        return is_empty

    def subtract(self, other):
        this_origin: RefItem = self.origin
        this_ref_list = self.getRefList()
        other_origin: RefItem = other.origin
        other_ref_list = other.getRefList()

class RefList(defaultdict):
    def __init__(self, msg=None, pat=None, keep_orig=False, tf=None):
        self.msg = msg
        self.translation = None
        self.translation_state = TranslationState.UNTRANSLATED
        self.pattern = pat
        self.keep_original = keep_orig
        self.tf = tf

    def __repr__(self):
        result = ""
        if self.msg:
            result += "[" + self.msg + "]\n"
            if self.translation:
                result += "[" + self.translation + "], state:" + self.translation_state.name + ",\n"

        for k, v in self.items():
            result += "" + str(k) + ", "
            result += str(v)
            result += "\n"
        return result

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
        valid_msg = (msg is not None) and (len(msg) > 0)
        valid_pattern = (pattern is not None)
        valid = valid_msg and valid_pattern
        if not valid:
            return None

        result_list = RefList(msg=msg, pat=pattern)
        try:
            is_bracket = (reftype == RefType.ARCH_BRACKET)
            is_function = (pattern == cm.FUNCTION)
            is_python = (pattern == cm.PYTHON_FORMAT)
            actual_ref_type = reftype

            if is_bracket:
                found_dict = cm.getTextWithinBrackets('(', ')', msg, is_include_bracket=False)
            else:
                found_dict = cm.patternMatchAll(pattern, msg)

            if not found_dict:
                return None

            found_list = list(found_dict.items())
            mm: MatcherRecord = None
            for loc, mm in found_list:
                orig = mm.getOriginAsTuple()
                (o_ss, o_ee), o_txt = orig
                is_ignored = ig.isIgnored(o_txt)
                if is_ignored:
                    continue

                # cm.debugging(o_txt)
                is_checking_for_path = (actual_ref_type == RefType.REF) or \
                                        (actual_ref_type == RefType.GA) or \
                                        (actual_ref_type == RefType.DOC) or \
                                        (actual_ref_type == RefType.CLASS) or \
                                        is_bracket

                is_path = is_checking_for_path and cm.isLinkPath(o_txt)
                if is_path:
                    dd(f'findOnePattern() IGNORE: [{o_txt}]; is_path = TRUE')
                    continue

                sub_content = mm.getSubEntryByIndex(0)
                if not sub_content:
                    sub_content = orig
                else:
                    mm_len = len(mm)
                    has_ref_type = (mm_len > 1)
                    if has_ref_type:
                        loc, reftext = sub_content
                        actual_ref_type = RefType.getRef(reftext)
                        sub_content = mm.getSubEntryByIndex(1)


                (sub_ss, sub_ee), sub_txt = sub_content

                is_doc = (actual_ref_type == RefType.DOC)
                is_ref = (actual_ref_type == RefType.REF)
                is_ga = (actual_ref_type == RefType.GA)
                sub_text_might_have_link = sub_txt and (is_bracket or is_doc or is_ref or is_ga)
                if sub_text_might_have_link:
                    actual_sub_txt, actual_loc = self.extractTextFromTextWithLink(sub_txt, (sub_ss, sub_ee), actual_ref_type)
                    sub_txt = actual_sub_txt
                    sub_ss, sub_ee = actual_loc


                orig_ref_item = RefItem(o_ss, o_ee, o_txt, ref_type=actual_ref_type)
                ref_item = RefItem(sub_ss, sub_ee, sub_txt, ref_type=actual_ref_type)

                ref_record = RefRecord(origin=orig_ref_item, reflist=[ref_item], pat=pattern)
                entry = {o_ss: ref_record}
                result_list.update(entry)

        except Exception as e:
            dd("RefList.findPattern()")
            dd("pattern:", pattern)
            dd("text:", result_list.msg)
            dd(e)
        return result_list

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

    def removeBlanksFromEntry(self, ref_record: RefRecord):
        def remove_blank_from_refitem(ref_item: RefItem):
            new_ref_rec_list=[]

            os, oe, otxt = ref_item.getValues()
            has_blank = (cm.FILLER_CHAR in otxt)
            if not has_blank:
                return new_ref_rec_list

            new_ref_item: RefItem = None
            part_list = cm.findInvert(cm.FILLER_CHAR_PATTERN, otxt)
            for loc, ntxt in part_list.items():
                new_ref_item = copy(ref_item)
                strip_s, strip_e, strip_txt = cm.stripSpaces(ntxt)
                s, e = loc
                ns = os + s + strip_s
                ne = ns + len(strip_txt)
                new_ref_item.setValues(ns, ne, strip_txt)

        new_ref_rec_list=[]


        new_ref_item = RefItem(start=ns, end=ne, txt=strip_txt)
        new_ref_rec.origin = new_ref_item
        new_ref_rec.reflist = []
        new_ref_rec_list.append(new_ref_rec)

        return new_ref_rec_list


    def findPattern(self, pattern_list: list):
        def cleanupIfNeeded():
            del_list = []
            new_list = []
            new_rec: RefRecord = None
            for s, ref_record in self.items():
                update_list = self.removeBlanksFromEntry(ref_record)
                if not update_list:
                    continue

                del_list.append(s)
                for new_rec in update_list:
                    orig = new_rec.getOrigin()
                    ss = orig.start
                    new_entry = {ss: new_rec}
                    new_list.append(new_entry)

            for k in del_list:
                del self[k]

            for entry in new_list:
                self.update(entry)

        count_item = 0
        preparsed_location = {}

        p: re.Pattern = None
        ref_type: RefType = None
        m: re.Match = None
        msg = self.msg
        pattern_list.reverse()
        remain_to_be_parsed = str(self.msg)
        for index, item in enumerate(pattern_list):
            p, ref_type = item
            one_list: RefList = self.findOnePattern(remain_to_be_parsed, p, ref_type)
            is_empty = (one_list is None) or (len(one_list) == 0)
            if is_empty:
                continue
            count_item += len(one_list)
            ref_record:RefRecord = None
            for k, v in one_list.items():
                origin: RefItem = v.getOrigin()
                s, e = origin.getLocation()
                blank_str = (cm.FILLER_CHAR * (e-s))
                left = remain_to_be_parsed[:s]
                right = remain_to_be_parsed[e:]
                remain_to_be_parsed = left + blank_str + right

            self.update(one_list)

        cleanupIfNeeded()
        sorted_list = sorted(list(self.items()))
        self.clear()
        self.update(sorted_list)
        return count_item


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

    def findTextOutsideRefs(self):
        has_ref = (len(self) > 0)
        if not has_ref:
            return

        temp_msg = str(self.msg)
        v: RefRecord = None
        # 1. Find where found pattern occured, fill it with a blank
        for k, v in reversed(list(self.items())):
            orig = v.getOrigin()
            os, oe, otxt = orig.getValues()
            blind = str(cm.FILLER_CHAR * len(otxt))
            temp_msg = temp_msg[:os] + blind + temp_msg[oe:]

        # 2. Remove text outside blank areas
        temp_dict = cm.patternMatchAll(cm.NEGATE_FIND_WORD, temp_msg)
        for loc, mm in temp_dict.items():
            (s, e), orig = mm.getOriginAsTuple()
            left, orig_txt, right = cm.getTextWithin(orig)
            if not orig_txt:
                continue

            # sen_dict = cm.getSentenceList(orig)
            # for loc, orig_txt in sen_dict.items():
            o_ss = s
            o_ee = o_ss + len(orig)
            orig_ref_item = RefItem(o_ss, o_ee, orig)
            v = RefRecord(origin=orig_ref_item, reflist=None)
            entry = {o_ss: v}
            self.update(entry)

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
                ref_item = RefItem(start=-1, end=-1, txt=RefType.FILLER.value, ref_type=RefType.FILLER)
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

    def parseMessage(self):

        trans = self.tf.isInDict(self.msg)
        if trans:
            self.setTranslation(trans, False, False)
            return

        is_link_path = cm.isLinkPath(self.msg)
        if is_link_path:
            dd(f'parseMessage(): IGNORED [{self.msg}]; is_full_path')
            return

        self.findPattern(pattern_list)

        # **** should break up sentences here
        self.findTextOutsideRefs()


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

    def translateRefItem(self, ref_item: RefItem):
        try:
            valid = (ref_item is not None)
            if not valid:
                return

            ref_txt = ref_item.getText()
            is_ignore = ig.isIgnored(ref_txt)
            if is_ignore:
                ref_item.setTranlation(None, False, True)
                return

            dd(f'translateRefItem: to be translated [{ref_txt}]')
            ref_type = ref_item.reftype
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
            is_dbl_quote = (ref_type == RefType.DBL_QUOTE)
            is_sng_quote = (ref_type == RefType.SNG_QUOTE)
            is_python_format = (ref_type == RefType.PYTHON_FORMAT)
            is_function = (ref_type == RefType.FUNCTION)

            is_quoted = (is_ast or is_dbl_quote or is_sng_quote)

            converted_to_abbr = False
            if is_kbd:
                dd(f'translateRefItem: is_kbd:{ref_txt}')
                tran, is_fuzzy, is_ignore = self.tf.translateKeyboard(ref_txt)
            elif is_abbr:
                dd(f'translateRefItem: is_abbr:{ref_txt}')
                tran, is_fuzzy, is_ignore = self.tf.translateAbbrev(ref_txt)
            elif is_menu:
                dd(f'translateRefItem: is_menu:{ref_txt}')
                tran, is_fuzzy, is_ignore = self.tf.translateMenuSelection(ref_txt)
            elif is_quoted:
                dd(f'translateRefItem: is_quoted:{ref_txt}')
                tran, is_fuzzy, is_ignore = self.tf.translateQuoted(ref_txt, ref_type=ref_type)
                converted_to_abbr = True
            elif is_osl_attrib or is_python_format or is_function:
                return
            else:
                # is_ignore = cm.isLinkPath(ref_txt)
                # if is_ignore:
                #     ref_item.setTranlation(None, False, True)
                #     return
                #
                dd(f'translateRefItem: anything else: {ref_txt}')
                is_ref_path = (is_ref and cm.REF_PATH.search(ref_txt.strip()) is not None)
                is_doc_path = (is_doc and cm.DOC_PATH.search(ref_txt.strip()) is not None)
                is_ignore_path = (is_ref_path or is_doc_path)
                if is_ignore_path:
                    return

                tran, is_fuzzy, is_ignore = self.tf.translateRefWithLink(ref_txt, ref_type)

            ref_item.setTranlation(tran, is_fuzzy, is_ignore)

            has_tran = (tran is not None)
            if has_tran:
                ref_item.converted_to_abbr = converted_to_abbr

        except Exception as e:
            print(f'ERROR! translateRefItem(), ref_item:{ref_item}, ref_type:{ref_type}, ERROR: {e}')

    def translateRefRecord(self, record: RefRecord):
        valid = (record is not None)
        if not valid:
            return

        orig: RefItem = record.getOrigin()
        orig_text = orig.getText()
        has_ref_list = (record.reflist is not None) and (len(record.reflist) > 0)
        if not has_ref_list:
            orig_trans, is_fuzzy, is_ignore = self.tf.translate(orig_text) # find the whole piece first to see if it's there
            orig.setTranlation(orig_trans, is_fuzzy, is_ignore)
            return

        # translate the ref_list
        ref_type = orig.getRefType()
        ref_list: list = record.getRefList()
        item: RefItem = None
        for item in reversed(ref_list):
            is_math = (ref_type == RefType.MATH)
            is_class = (ref_type == RefType.CLASS)
            is_sup = (ref_type == RefType.SUP)
            is_function = (ref_type == RefType.FUNCTION)
            is_mod = (ref_type == RefType.MOD)
            is_func = (ref_type == RefType.FUNC)
            is_lineno = (ref_type == RefType.LINENOS)

            is_ignore = (is_math or
                         is_class or
                         is_sup or
                         is_function or
                         is_mod or
                         is_func or
                         is_lineno)
            if is_ignore:
                continue

            self.translateRefItem(item)

    def translateRefList(self):

        is_translated = (self.translation_state != TranslationState.UNTRANSLATED)
        if is_translated:
            return

        tran_text = None
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
            for k, ref_item in tran_required_reversed_list:
                self.translateRefRecord(ref_item)

            tran = self.transferTranslation(self.msg)
            self.setTranslation(tran, False, False) # temporary acceptable, isFuzzy and isIgnore will show TRUE state

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
