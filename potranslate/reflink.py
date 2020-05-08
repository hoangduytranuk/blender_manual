#!/usr/bin/env python3
import sys
sys.path.append('/Users/hoangduytran/blender_manual/potransßlate')

import re
from common import Common as cm
from common import _, pp
from ignore import Ignore as ig
from collections import defaultdict, OrderedDict
from translation_finder import TranslationFinder
# from pyparsing import nestedExpr
from enum import Enum

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
    ACCEPTABLE = 0
    FUZZY = 1
    IGNORED = 3
    REMOVE = 4


class TextStyle(Enum):
    NORMAL = 0
    ITALIC = 1
    BOLD = 2
    BOX = 3
    RAW = 4


class RefType(Enum):
    GA = "\`"
    ARCH_BRACKET = "()"
    AST_QUOTE = "*"
    DBL_QUOTE = "\""
    SNG_QUOTE = "'"
    MM = ":MM:"
    ABBR = ":abbr:"
    CLASS = ":class:"
    DOC = ":doc:"
    GUILABEL = ":guilabel:"
    KBD = ":kbd:"
    LINENOS = ":linenos:"
    MATH = ":math:"
    MENUSELECTION = ":menuselection:"
    MOD = ":mod:"
    REF = ":ref:"
    SUP = ":sup:"
    TERM = ":term:"
    TEXT = "generic_text"
    FILLER = "filler"


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
        self.translation_state: TranslationState = TranslationState.ACCEPTABLE
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

    def getTranslationState(self):
        return self.translation_state

    def setTranslationState(self, state: TranslationState):
        current_state = self.getTranslationState()
        is_fuzzy = (current_state == TranslationState.FUZZY)
        if not is_fuzzy:
            self.translation_state = state

    def getTranslation(self):
        return self.translation

    def setTranlation(self, tran, state=TranslationState.ACCEPTABLE):
        orig = self.getText()
        is_ignored = ig.isIgnored(orig)
        is_same = cm.isTextuallySame(orig, tran)
        is_ignored_all = (is_ignored or is_same)
        if is_ignored_all:
            tran = None
            state = TranslationState.IGNORED
        else:
            self.translation = tran
            self.setTranslationState(state)

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
        for orig, breakdown in cm.patternMatchAll(cm.KEYBOARD_SEP, self.getText()):
            s, e, txt = orig
            entry = {s: (s, e, txt)}
            item_list.update(entry)
        return item_list

    def getTextForMenu(self):
        item_list = {}
        word_list = cm.findInvert(cm.MENU_SEP, self.getText())
        for k, v in reversed(list(word_list.items())):
            s, e, txt = v
            entry = {s: (s, e, txt)}
            item_list.update(entry)
        return item_list

    def getTextForAbbrev(self):
        item_list = {}
        for orig, breakdown in cm.patternMatchAll(cm.ABBR_TEXT, self.getText()):
            os, oe, otxt = orig
            has_breakdown = (breakdown and len(breakdown) > 0)
            if not has_breakdown:
                continue

            for bs, be, btxt in breakdown:
                entry = {bs: (bs, be, btxt)}
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

    def getRefTextOnly(self):

        ref_type = self.getRefType()

        is_kbd = (ref_type == RefType.KBD)
        is_abbr = (ref_type == RefType.ABBR)
        is_menu = (ref_type == RefType.MENUSELECTION)
        if is_kbd:
            entry_list = self.getTextForKeyboard()
        elif is_abbr:
            entry_list = self.getTextForAbbrev()
        elif is_menu:
            entry_list = self.getTextForMenu()
        else:
            entry_list = self.getTextForGenericRef()

        return entry_list


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

    def setOriginType(self):
        orig_item = self.getOrigin()
        has_orig = (orig_item is not None) and (orig_item.getText() is not None)
        if not has_orig:
            return False

        # orig_txt = orig_item.getText()
        # is_debug = ("In some cases you may not want to use the default" in orig_txt)
        # if is_debug:
        #     _("DEBUG")
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

            # item: RefItem = None
            # for item in self.reflist:
            #     item.start = cm.alterValue(item.start, alter_value=start, op=op)
            #     item.end = item.start + len(item.text)
            #
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

    # def getRefTextOnly(self):
    #
    #     has_ref = (not self.isRefEmtpy())
    #     if not has_ref:
    #         return None
    #
    #     item:RefItem = None
    #     ref_type = self.getOrigin().getRefType()
    #     for s, e, txt in self.getRefList():


class RefList(defaultdict):
    def __init__(self, msg=None, pat=None, keep_orig=False, tf=None):
        self.msg = msg
        self.translation = None
        self.translation_state = TranslationState.FUZZY
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

    def getTranslation(self):
        return self.translation

    def setTranslation(self, tran, state=TranslationState.ACCEPTABLE):
        if ig.isIgnored(self.msg):
            self.setTranslation(self.msg)
            self.translation_state = TranslationState.IGNORED
        else:
            _('set translation:', self.msg, "=>", tran)
            self.translation = tran
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

        # is_debug = ("INSERT(ATTRIB+XDATA)" in self.msg)
        # if is_debug:
        #     _("DEBUG")

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

    def findOnePattern(self, msg, pattern, reftype, keep_original, start_loc=0):
        valid_msg = (msg is not None) and (len(msg) > 0)
        valid_pattern = (pattern is not None)
        valid = valid_msg and valid_pattern
        if not valid:
            return None

        result_list = RefList(msg=msg, pat=pattern)
        try:
            for origin, breakdown in cm.patternMatchAll(pattern, msg):
                is_end = (origin is None)
                if is_end:
                    break

                s, e, orig = origin
                o_ss = s + start_loc
                o_ee = o_ss + len(orig)
                orig_ref_item = RefItem(o_ss, o_ee, orig, ref_type=reftype, keep_orig=keep_original)

                v = RefRecord(origin=orig_ref_item, reflist=None, pat=pattern)
                entry = {o_ss: v}
                result_list.update(entry)

                has_breakdown = (breakdown is not None) and (len(breakdown) > 0)
                if not has_breakdown:
                    continue

                new_ref_list = []
                for ss, ee, g in breakdown:
                    if not g:
                        continue
                    i_s = orig.find(g)
                    # ss = i_s + s # using setence index
                    ss = i_s  # using sub pattern index
                    ee = ss + len(g)
                    xtype = self.getType(g)
                    is_text = (xtype == RefType.TEXT)
                    if not is_text:
                        orig_ref_item.setRefType(xtype)
                    else:
                        ref_item = RefItem(ss, ee, g,
                                           keep_orig=keep_original)  # should this take default reftype.TEXT????
                        new_ref_list.append(ref_item)
                v.reflist = new_ref_list

        except Exception as e:
            _("RefList.findPattern()")
            _("pattern:", pattern)
            _("text:", result_list.msg)
            _(e)
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

            # is_debug = (test_txt in i_txt) and (test_txt in r_txt)
            # if is_debug:
            #     _("DEBUG")

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
                    _("CAN REPLACE V's result BY ITEM'S RESULT")
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

    def findPattern(self, pattern_list, start_loc=0):
        for p, ref_type, keep_orig in pattern_list:
            one_list: RefList = self.findOnePattern(self.msg, p, ref_type, keep_orig, start_loc=start_loc)
            is_empty = (one_list is None) or (len(one_list) == 0)
            if is_empty:
                continue

            diff_list = self.diff(one_list)
            self.update(diff_list)
        sorted_list = sorted(list(self.items()))
        self.clear()
        self.update(sorted_list)

    def testRecord(self, record: RefRecord):
        valid = (record is not None)
        if not valid:
            _("testRecord: Unable to TEST, record is NONE")
            return

        orig = record.getOrigin()
        ref_list = record.getRefList()
        orig_txt = orig.text
        item: RefItem
        for item in ref_list:
            left = orig_txt[:item.start]
            right = orig_txt[:item.end:]
            txt = left + item.text + right
            _("original:", orig_txt)
            _("ref_text:", txt)

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
        for origin, bkdown in cm.patternMatchAll(cm.NEGATE_FIND_WORD, temp_msg):
            is_end = (origin is None)
            if is_end:
                break

            s, e, orig = origin
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

        # is_debug = ('Làm Dịu Đầu Ra' in msg)
        # if is_debug:
        #     _('DEBUG')

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
                _("found_matched_ref:", v_txt, " for:", msg)
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
            target_ref_record.getOrigin().setTranlation(tran_txt)
            _("transferRefRecordText:", target_ref_record)
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

        def replaceArchedQuote(txt):
            new_txt = str(txt)
            new_txt = re.sub('\)', ']', new_txt)
            new_txt = re.sub('\(', '[', new_txt)
            return new_txt

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

        pattern_list = [
            (cm.GA_REF, RefType.GA, True),  # this will have to further classified as progress
            (cm.AST_QUOTE, RefType.AST_QUOTE, True),
            (cm.DBL_QUOTE, RefType.DBL_QUOTE, True),
            (cm.SNG_QUOTE, RefType.SNG_QUOTE, True),
        ]
        orig_list = RefList(msg=orig_txt)
        orig_list.findPattern(pattern_list)

        self.findPattern(pattern_list)
        has_record = (len(self) > 0)
        if not has_record:
            return

        balanceNumberOfItems(self, orig_list)  # this will fill in 'filler' records, assingting search

        _('list of refs:')
        pp(self)
        _(f'quotedFindRefs, orig: [{orig_txt}]')
        _(f'quotedFindRefs, tran: [{self.msg}]')

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
                _(f'Ignoring [{ref_orig_txt}]')
                continue

            is_debug = ref_orig.textContain('handLeft') or ref_orig.textContain('bàn tay trái')
            if is_debug:
                _(f'DEBUG')

            # is_debug = ('%' in ref_orig_txt)
            # if is_debug:
            #     _('DEBUG')

            is_ast_quote = (ref_type == RefType.AST_QUOTE)
            is_dbl_quote = (ref_type == RefType.DBL_QUOTE)
            is_sng_quote = (ref_type == RefType.SNG_QUOTE)
            is_abbr = (ref_type == RefType.ABBR)  # # dealing with this later when switch to the test_dic.json

            is_acceptable = (is_ast_quote or is_dbl_quote or is_sng_quote or is_abbr)

            if is_acceptable:
                pp(f'ref_orig:[{ref_orig}]')
                pp(f'ref:[{ref_list}]')

                # is_debug = ('key' in ref_orig_txt.lower()) or ('khóa' in ref_orig_txt.lower())
                # if is_debug:
                #     print('DEBUG')

                is_reverse = ig.isReverseOrder(ref_orig_txt)

                ref_list_len = len(ref_list)
                has_ref = (ref_list_len > 0)
                has_more_than_one_ref_items = (ref_list_len > 1)
                if has_more_than_one_ref_items:
                    _(f'ref list has more than one item:[{ref_list_len}]')

                if is_abbr:
                    first_ref_item = ref_list[0]
                    fis, fie, fi_txt = first_ref_item.getValues()
                    fi_word_list = cm.ABBREV_CONTENT_PARSER.findall(fi_txt)
                    existing_tran, existing_orig = fi_word_list[0]
                    orig_entry = orig_list.findRefRecord(existing_orig, index, is_reversed_list=True)
                    is_found_orig = (orig_entry is not None)
                    if not is_found_orig:  # item introduced while translating, ignore, since there are no possibility to identify the origin
                        _(f'DEBUG: entry not in orig text:[{existing_orig} => [{existing_tran}]')
                        continue

                    orig_orig = orig_entry.getOrigin()
                    # orig_ref_list = orig_entry.getRefList()
                    # orig_orig_txt = orig_orig.getText()
                    #
                    # ref_tran_txt = ref_orig_txt
                    # ref_orig_txt = orig_orig_txt
                    # os, oe = ref_orig.getLocation()

                    _(f'DEBUG: found orig entry:[{orig_orig}], for the current:[{v}] and index: [{index}]')
                    continue
                elif has_ref:
                    is_debug = ('handLeft' in ref_orig_txt)
                    if is_debug:
                        _(f'DEBUG')
                    first_ref_item = ref_list[0]
                    r_txt = first_ref_item.getText()
                    # ref_txt_list = r_txt.split(cm.REF_SEP)
                    ref_txt_list = refSplit(ref_orig_txt)  # keeping the original ast, double, single quote
                    has_ref_sep = (len(ref_txt_list) > 1)
                    if has_ref_sep:
                        ref_tran_txt = ref_txt_list[0]
                        ref_orig_txt = ref_txt_list[1]
                    else:
                        is_debug = ('handLeft' in ref_orig_txt)
                        if is_debug:
                            _(f'DEBUG')

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
                            _(f"Unable to find original for [{ref_orig_txt}]")
                            r_txt = first_ref_item.getText()
                            os, oe = ref_orig.getLocation()
                            r_txt = replaceArchedQuote(r_txt)

            is_change = (ref_tran_txt is not None) and (ref_orig_txt is not None)
            if is_change:
                ref_tran_txt = replaceArchedQuote(ref_tran_txt)
                ref_orig_txt = replaceArchedQuote(ref_orig_txt)
                if is_reverse:
                    replacement = f':abbr:`{ref_orig_txt} ({ref_tran_txt})`'
                else:
                    replacement = f':abbr:`{ref_tran_txt} ({ref_orig_txt})`'

                os, oe = ref_orig.getLocation()
                left_side = new_txt[:os]
                right_side = new_txt[oe:]
                new_txt = left_side + replacement + right_side
                _(f'left_side:[{left_side}]')
                _(f'right_side:[{right_side}]')
                _(f'replacement:[{replacement}]')
                _(f'new_txt:[{new_txt}]')
            _()

        return new_txt

    def transferTranslatedRefs(self, current_msg, current_tran):
        self.msg = current_msg
        pattern_list = [
            (cm.GA_REF, RefType.GA, True),  # this will have to further classified as progress
            (cm.AST_QUOTE, RefType.AST_QUOTE, True),
            (cm.DBL_QUOTE, RefType.DBL_QUOTE, True),
            (cm.SNG_QUOTE, RefType.SNG_QUOTE, True),
        ]
        self.findPattern(pattern_list)
        has_record = (len(self) > 0)
        if not has_record:
            _("Message has refs, but translation DOESN'T")
            if self.keep_original:
                has_original = (current_msg in current_tran)
                if not has_original:
                    txt = f'{current_msg} -- {current_tran}'
                else:
                    txt = f'-- {current_msg}'
                self.setTranslation(txt)
            else:
                self.setTranslation(current_tran)
            return None

        sorted_list = sorted(list(self.items()))
        self.clear()
        self.update(sorted_list)
        self.translateRefList()

        current_tran_reflist = RefList(msg=current_tran)
        current_tran_reflist.setTranslation(current_tran)

        current_tran_reflist.findPattern(pattern_list)
        has_record = (len(current_tran_reflist) > 0)

        sorted_list = sorted(list(current_tran_reflist.items()))
        current_tran_reflist.clear()
        current_tran_reflist.update(sorted_list)

        un_transferred_list = self.transferRefRecordText(current_tran_reflist)
        tran = current_tran_reflist.transferTranslation(current_tran)
        current_tran_reflist.setTranslation(tran)

        # _("tran before:", current_tran)
        # _("tran now:", current_tran_reflist.getTranslation())

        has_untransferred = (un_transferred_list and len(un_transferred_list) > 0)
        if has_untransferred:
            _("Untransferred:")
            pp(un_transferred_list)
        return un_transferred_list

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

    def correctRefs(self, non_tran, tran):
        self.msg = tran

        pattern_list = [
            (cm.GA_REF, RefType.GA, True),  # this will have to further classified as progress
            (cm.AST_QUOTE, RefType.AST_QUOTE, True),
            (cm.DBL_QUOTE, RefType.DBL_QUOTE, True),
            (cm.SNG_QUOTE, RefType.SNG_QUOTE, True),
            (cm.DBL_QUOTE_SLASH, RefType.DBL_QUOTE, True),
        ]
        self.findPattern(pattern_list)
        has_record = (len(self) > 0)
        if not has_record:
            return False

        sorted_list = sorted(list(self.items()))
        self.clear()
        self.update(sorted_list)

        orig_reflist = RefList(msg=non_tran)
        orig_reflist.findPattern(pattern_list)

        v: RefRecord = None
        for k, v in self.items():
            tran_orig = v.getOrigin()
            s, e, tran_txt = tran_orig.getValues()
            orig_item = orig_reflist.findRefByText(tran_txt)
            is_found = (orig_item is not None)
            if not is_found:
                print("Translation entry NOT FOUND:", k, v)
                continue

            ov: RefRecord = None
            ok, ov = orig_item
            os, oe, otxt = ov.getOrigin().getValues()

            print("Original found:", otxt, "for:", tran_txt)
            print("Original type", ov.getOrigin().getRefType())
            print("Original Reflist", ov.getRefList())

    def parseMessage(self):
        # is_debug = ("Box Deselect:" in msg)
        # if is_debug:
        #     _("DEBUG")

        # entry include: (pattern, ref_type, include_original)
        pattern_list = [
            (cm.GA_REF, RefType.GA, True),  # this will have to further classified as progress
            (cm.AST_QUOTE, RefType.AST_QUOTE, True),
            (cm.DBL_QUOTE, RefType.DBL_QUOTE, True),
            (cm.SNG_QUOTE, RefType.SNG_QUOTE, True),
        ]
        self.findPattern(pattern_list)

        # **** should break up sentences here
        self.findTextOutsideRefs()

        has_record = (len(self) > 0)
        if has_record:
            sorted_list = sorted(list(self.items()))
            list_type = type(sorted_list)
            self.clear()
            self.update(sorted_list)
            _("Sorted")
        else:
            tran, is_fuzzy = self.tf.translate(self.msg)
            has_tran = (tran is not None)
            if has_tran and self.keep_original:
                tran = f"{tran} -- {self.msg}"
            elif not has_tran and self.keep_original:
                tran = f"-- {self.msg}"
            elif not has_tran and not self.keep_original:
                tran = ""
            self.setTranslation(tran)

        # arched_bracket_list = cm.parseMessageWithDelimiterPair('(', ')', self.msg)
        # has_record = (len(arched_bracket_list) > 0)
        # if has_record:
        #     for s, e, txt in arched_bracket_list:
        #         result_list: RefList = self.findOnePattern(txt, cm.ARCH_BRAKET_MULTI, start_loc=s)
        #         for k, v in result_list.items():
        #             orig = v.getOrigin()
        #             o_s, o_e, o_txt = orig.getValues()
        #             sub_ref_list = RefList(msg=o_txt)
        #             sub_ref_list.findPattern(pattern_list)
        #             has_sub_ref = (len(sub_ref_list) > 0)
        #             if has_sub_ref:
        #                 # sub_ref_list.finalizeList()
        #                 v.getRefList().clear()
        #                 for kk, vv in sub_ref_list.items():
        #                     v.getRefList().append(vv)
        #             ref_list_entry = {o_s:v}
        #             self.update(ref_list_entry)

        # sorted_list = sorted(self.items(), key=lambda t: t[0])
        # self.clear()
        # self.update(ref_list)

        # pp(self.items())
        # remove redundancies
        # self.removeRedundancies()

    def mergeTranslationToOrigin(self, ref_rec: RefRecord):
        orig_item: RefItem = ref_rec.getOrigin()
        ref_list = ref_rec.getRefList()
        has_ref_list = (ref_list is not None) and (len(ref_list) > 0)
        if not has_ref_list:
            return

        tran_txt = str(orig_item.getText())
        ref_item: RefItem = None
        for ref_item in reversed(ref_list):
            tran_state = ref_item.translation_state
            is_ignore = (tran_state == TranslationState.IGNORED) or (tran_state == TranslationState.REMOVE)
            if is_ignore:
                continue

            is_ignore_left_right = (ref_item.converted_to_abbr == True)
            s, e = ref_item.getLocation()
            o_txt = ref_item.getText()
            tran_state = ref_item.getTranslationState()
            tran = ref_item.getTranslation()
            has_translation = (tran is not None) and (len(tran) > 0)
            if not has_translation:
                continue

            if is_ignore_left_right:
                tran_txt = tran
            else:
                left_txt = tran_txt[:s]
                right_txt = tran_txt[e:]
                tran_txt = left_txt + tran + right_txt

        # is_same = (tran_txt == orig_item.getText())
        # if is_same:
        # tran_txt = ""
        orig_item.setTranlation(tran_txt)

    def transferTranslation(self, msg):
        tran = str(msg)
        v: RefRecord = None
        for k, v in reversed(list(self.items())):
            self.mergeTranslationToOrigin(v)
            os, oe = v.getOriginLocation()
            otran = v.getOrigin().getTranslation()
            has_tran = (otran is not None) and (len(otran) > 0)
            if not has_tran:
                continue

            tran = tran[:os] + otran + tran[oe:]
        return tran

    def translateRefItem(self, ref_item: RefItem, ref_type):
        valid = (ref_item is not None)
        if not valid:
            return

        ref_txt = ref_item.getText()
        # is_debug = ("alias" in ref_txt.lower())
        # if is_debug:
        #     _("DEBUG")

        is_ignore = ig.isIgnored(ref_txt)
        if is_ignore:
            ref_item.setTranlation(None, state=TranslationState.IGNORED)
            return

        is_kbd = (ref_type == RefType.KBD)
        is_abbr = (ref_type == RefType.ABBR)
        is_menu = (ref_type == RefType.MENUSELECTION)
        # ----------
        is_ast = (ref_type == RefType.AST_QUOTE)
        is_dbl_quote = (ref_type == RefType.DBL_QUOTE)
        is_sng_quote = (ref_type == RefType.SNG_QUOTE)
        is_quoted = (is_ast or is_dbl_quote or is_sng_quote)

        converted_to_abbr = False
        if is_kbd:
            tran = self.tf.translateKeyboard(ref_txt)
        elif is_abbr:
            tran = self.tf.translateAbbrev(ref_txt)
        elif is_menu:
            tran = self.tf.translateMenuSelection(ref_txt)
        elif is_quoted:
            tran = self.tf.translateQuoted(ref_txt)
            converted_to_abbr = True
        else:
            tran = self.tf.translateRefWithLink(ref_txt)
        has_tran = (tran is not None)
        if has_tran:
            ref_item.converted_to_abbr = converted_to_abbr
            ref_item.setTranlation(tran, state=TranslationState.ACCEPTABLE)
        else:
            ref_item.setTranlation("", state=TranslationState.ACCEPTABLE)

    def translateRefRecord(self, record: RefRecord):
        valid = (record is not None)
        if not valid:
            return

        orig: RefItem = record.getOrigin()
        orig_text = orig.getText()
        has_ref_list = (record.reflist is not None) and (len(record.reflist) > 0)
        if not has_ref_list:
            orig_trans, is_fuzzy = self.tf.translate(orig_text)  # find the whole piece first to see if it's there
            has_orig_tran = (orig_trans is not None) and (orig_trans != orig_text)
            if has_orig_tran:
                orig.translation = orig_trans
                orig.translation_state = TranslationState.ACCEPTABLE
            return

        # translate the ref_list
        ref_type = orig.getRefType()
        ref_list: list = record.getRefList()
        for item in reversed(ref_list):
            is_math = (ref_type == RefType.MATH)
            is_class = (ref_type == RefType.CLASS)
            is_sup = (ref_type == RefType.SUP)
            is_ignore = (is_math or is_class or is_sup)
            if is_ignore:
                continue

            self.translateRefItem(item, ref_type)

    def translateRefList(self):
        valid = (len(self) > 0)
        if not valid:
            return

        # is_debug = ("Image sequences can use placeholder files" in self.msg)
        # if is_debug:
        #     _("DEBUG")

        has_ref = (len(self) > 0)
        if not has_ref:
            trans, is_fuzzy = self.tf.translate(self.msg)
            valid = (trans is not None)
            if valid:
                if self.keep_original:
                    tran_text = f'{trans} -- {self.msg}'
                else:
                    tran_text = trans
            else:
                tran = None

            tran_state = (TranslationState.FUZZY if is_fuzzy else TranslationState.ACCEPTABLE)
            self.setTranslation(tran_text, state=tran_state)
            return

        for k, ref_item in reversed(list(self.items())):
            self.translateRefRecord(ref_item)

        tran = self.transferTranslation(self.msg)
        has_tran = (tran is not None) and (len(tran) > 0)
        if has_tran:
            self.setTranslation(tran)
