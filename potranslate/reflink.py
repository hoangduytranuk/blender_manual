import sys
sys.path.append('/Users/hoangduytran/PycharmProjects/potranslate')

from common import Common as cm
from common import _, pp

#from pyparsing import nestedExpr
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
    ACCEPTABLE=0
    FUZZY=1
    IGNORED=3
    REMOVE=4

class TextStyle(Enum):
    NORMAL=0
    ITALIC=1
    BOLD=2
    BOX=3
    RAW=4

class RefType(Enum):
    ABBR=":abbr:"
    CLASS=":class:"
    DOC = ":doc:"
    GUILABEL=":guilabel:"
    KBD=":kbd:"
    LINENOS=":linenos:"
    MATH=":math:"
    MENUSELECTION=":menuselection:"
    MOD=":mod:"
    REF=":ref:"
    SUP=":sup:"
    TERM=":term:"
    TEXT="generic_text"

class RefItem:

    def __init__(self, start=-1, end=-1, txt=None):
        self.start:int = start
        self.end:int = end
        self.text:str = txt
        self.translation:str = None
        self.old_translation: str = None
        self.translation_state:TranslationState = TranslationState.ACCEPTABLE
        self.translation_include_original: bool = False
        self.reftype:RefType = RefType.TEXT
        self.text_style:TextStyle = TextStyle.NORMAL

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

    def setTranslationState(self, state:TranslationState):
        current_state = self.getTranslationState()
        is_fuzzy = (current_state == TranslationState.FUZZY)
        if not is_fuzzy:
            self.translation_state = state

    def getTranslation(self):
        return self.translation

    def setTranlation(self, tran, state=TranslationState.ACCEPTABLE):
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

class RefRecord:
    def __init__(self, origin:RefItem = None, reflist: list = [], pat=None):
        self.origin: RefItem = origin
        self.reflist: list = reflist
        self.pattern: str = pat
        self.setOriginType()

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
            ref_entry = RefItem(start=ss, end=ee, txt=i_txt)
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

    def appendRefItem(self, ref_list_item : RefItem = None):
        valid = (ref_list_item is not None)
        if not valid:
            return
        self.reflist.append(ref_list_item)

    def getOrigin(self):
        return self.origin

    def getRefList(self):
        return self.reflist

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


class RefList(dict):
    type_blk_list = [RefType.ABBR, RefType.CLASS, RefType.DOC, RefType.GUILABEL, RefType.KBD,
                     RefType.LINENOS, RefType.MATH, RefType.MENUSELECTION, RefType.MOD,
                     RefType.REF, RefType.SUP, RefType.TERM]

    def __init__(self, msg=None, pat=None, translation_finder=None, keep_orig=False):
        self.msg = msg
        self.translation = None
        self.translation_state = TranslationState.FUZZY
        self.pattern = pat
        self.keep_original = keep_orig
        self.tf = translation_finder

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
        self.translation = tran
        self.translation_state = state

    def getType(self, xtype):
        for x in RefList.type_blk_list:
            x_value = x.value
            has_type = (x_value == xtype)
            if has_type:
                return x
        else:
            return RefType.TEXT

    def getRefsAsList(self):
        ref_list=[]
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
            entry= RefItem(start=ss, end=ee, txt=v_orig_txt)
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
            entry={k:(s,e)}
            loc_list.update(entry)

        remove_list=[]
        for k, v in loc_list.items():
            vs, ve = v  # remove
            for kk, vv in loc_list.items():
                is_same = (kk == k) and (vv == v)
                if is_same:
                    continue
                vvs, vve = vv # keep
                is_remove = (vs > vvs) and (ve < vve) and (k not in remove_list)
                if is_remove:
                    remove_list.append(k)
        for k in remove_list:
            del self[k]

    def merge(self, other_list, alter_value=0, op=None):
        valid = (other_list is not None) and (len(other_list) > 0)
        if not valid:
            return

        remain_list=RefList(msg=other_list.msg, pat=other_list.pattern)
        other_loc_list = other_list.getOrigLocList(alter_value=alter_value, op=op)
        v: RefRecord = None
        for k, v in self.items():
            v_orig: RefItem = v.getOrigin()
            is_dupped = (v_orig in other_loc_list)
            if not is_dupped:
                remain_list.update({k:v})
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
            new_ref_list.update({key:v})

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

    def findOnePattern(self, msg, pattern, start_loc=0):
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
                ref_item = RefItem(o_ss, o_ee, orig)
                v = RefRecord(origin=ref_item, reflist=[], pat=pattern)
                entry={o_ss:v}
                result_list.update(entry)

                has_breakdown = (breakdown is not None) and (len(breakdown) > 0)
                if not has_breakdown:
                    continue

                for ss, ee, g in breakdown:
                    if not g:
                        continue
                    i_s = orig.find(g)
                    #ss = i_s + s # using setence index
                    ss = i_s # using sub pattern index
                    ee = ss + len(g)

                    ref_item = RefItem(ss, ee, g)
                    v.appendRefItem(ref_list_item = ref_item)

        except Exception as e:
            _("RefList.findPattern()")
            _("pattern:", pattern)
            _("text:", result_list.msg)
            _(e)
        return result_list

    def isEmpty(self):
        is_empty = (len(self) == 0)
        return is_empty
    
    def inRange(self, item : RefRecord):
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
        for p in pattern_list:
            one_list : RefList = self.findOnePattern(self.msg, p, start_loc=start_loc)
            is_empty = (len(one_list) == 0)
            if is_empty:
                continue

            diff_list = self.diff(one_list)
            self.update(diff_list)

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


    def finalizeList(self):
        if self.isEmpty():
            return {}

        # is_debug = ("This can be used with different" in self.msg)
        # if is_debug:
        #     _("DEBUG")

        k: int = -1
        v: RefRecord = None
        v_len = -1
        entry_list = RefList(msg=self.msg)
        try:
            for k, v in self.items():
                v_len = -1
                xtype = None
                xtype = text_entry = None

                new_record : RefRecord = RefRecord(origin=v.getOrigin(), reflist=[])
                entry_list.update({k: new_record})
                origin_entry = v.getOrigin()
                v_len = len(v.getRefList())

                if v_len == 0:
                    text_entry = origin_entry
                elif v_len == 1:
                    text_entry = v.getRefItemByIndex(0)
                elif v_len == 2:  # :kbd:,
                    type_entry : RefItem = v.getRefItemByIndex(0)
                    text_entry : RefItem = v.getRefItemByIndex(1)
                    xtype = type_entry.text

                    xs, xe, xtxt = type_entry.getValues()
                    enum_type = self.getType(xtxt)
                    origin_entry.setRefType(enum_type)
                else:
                    raise Exception("Impossible List, there are more items than expected!")

                # is_debug = ("Screen Space Ambient Occlusion" in self.msg)
                # if is_debug:
                #     print("DEBUG")

                txt = text_entry.text

                # has_xtype = (xtype is not None)
                has_xtype = origin_entry.getRefType() != RefType.TEXT
                has_menu = origin_entry.getRefType() == RefType.MENUSELECTION
                has_abbr = origin_entry.getRefType() == RefType.ABBR
                has_kbd = origin_entry.getRefType() == RefType.KBD
                has_doc = origin_entry.getRefType() == RefType.DOC
                has_ref = origin_entry.getRefType() == RefType.REF

                uri_ref : RefList = self.findOnePattern(txt, cm.LINK_WITH_URI)
                has_uri = (not uri_ref.isEmpty())

                if has_uri and not (has_abbr or has_menu or has_doc):
                    origin_entry.setRefType(RefType.REF)
                    uri_rec : RefRecord = uri_ref.getRecordByIndex(0)
                    uri_ref_rec : RefItem = uri_rec.getRefItemByIndex(0)
                    # orig_uri_entry : RefItem = v.getRefItemByIndex(0)
                    ttxt = uri_ref_rec.text
                    ss = text_entry.start + uri_ref_rec.start
                    ee = ss + len(ttxt)

                    # otxt = origin_entry.text
                    # tts = self.msg[:ss]
                    # tte = self.msg[ee:]
                    # ttx = tts + ttxt + tte

                    entry: RefItem = RefItem(start=ss, end=ee, txt=ttxt)
                    new_record.appendRefItem(ref_list_item=entry)
                    #new_record.appendRefItem(ref_list_item=entry)
                elif has_xtype:
                    if has_abbr:
                        abbr_rec: RefRecord = None
                        abbr_list = self.findOnePattern(txt, cm.LINK_WITH_URI)
                        abbr_rec = abbr_list.getRecordByIndex(0)
                        abbr_txt_entry : RefItem = abbr_rec.getRefItemByIndex(1)
                        orig_abbr_entry: RefItem = v.getRefItemByIndex(1)
                        o_s, o_e = orig_abbr_entry.getLocation()

                        ttxt = abbr_txt_entry.text
                        #ss = orig_abbr_entry.start + abbr_txt_entry.start
                        ss = o_s + abbr_txt_entry.start
                        ee = ss + len(ttxt)

                        # otxt = origin_entry.text
                        # tts = self.msg[:ss]
                        # tte = self.msg[ee:]
                        # ttx = tts + ttxt + tte

                        entry : RefItem = RefItem(start=ss, end=ee, txt=ttxt)
                        new_record.appendRefItem(ref_list_item=entry)
                    elif has_menu:

                        menu_list = self.findOnePattern(txt, cm.MENU_PART)
                        orig_mnu_entry: RefItem = v.getRefItemByIndex(1)
                        vv: RefRecord = None
                        for k, vv in menu_list.items():
                            menu_txt_entry = vv.getOrigin()
                            ttxt = menu_txt_entry.text
                            ss = orig_mnu_entry.start + menu_txt_entry.start
                            #ss = o_s + menu_txt_entry.start
                            ee = ss + len(ttxt)

                            # otxt = origin_entry.text
                            # tts = self.msg[:ss]
                            # tte = self.msg[ee:]
                            # ttx = tts + ttxt + tte

                            entry : RefItem = RefItem(start=ss, end=ee, txt=ttxt)
                            new_record.appendRefItem(ref_list_item=entry)
                    elif has_doc:

                        # is_debug = ("Be sure to check the" in self.msg)
                        # if is_debug:
                        #     _("DEBUG")

                        uri_rec: RefRecord = uri_ref.getRecordByIndex(0)
                        if not uri_rec:
                            # for: :doc:`/about/contribute/guides/writing_guide`
                            new_record.appendRefItem(ref_list_item=text_entry)
                            continue

                        uri_ref_rec: RefItem = uri_rec.getRefItemByIndex(0)
                        orig_uri_entry: RefItem = v.getRefItemByIndex(1)

                        ttxt = uri_ref_rec.text
                        ss = orig_uri_entry.start + uri_ref_rec.start
                        ee = ss + len(ttxt)

                        new_text_entry=RefItem(start=ss, end=ee, txt=ttxt)
                        new_record.appendRefItem(ref_list_item=new_text_entry)
                    else:
                        new_record.appendRefItem(ref_list_item=text_entry)
                else:
                    new_record.appendRefItem(ref_list_item=text_entry)

        except Exception as e:
            _(self)
            _("k, v, v_len")
            _(k, v, v_len)
            raise e

        self.clear()
        self.update(entry_list)


    def parseMessage(self):
        # is_debug = ("Box Deselect:" in msg)
        # if is_debug:
        #     _("DEBUG")

        self.findPattern([cm.GA_REF, cm.AST_QUOTE, cm.DBL_QUOTE, cm.SNG_QUOTE])
        has_ref = (len(self) > 0)
        if not has_ref:
            trans, is_fuzzy, is_ignore = self.tf.translate(self.msg)
            if is_ignore:
                self.translation = ""
                self.translation_state = TranslationState.IGNORED
                return

            valid = (trans is not None)
            if not valid:
                self.translation = ""
                self.translation_state = TranslationState.ACCEPTABLE
                return

            if self.keep_original:
                tran_text = "{} -- {}".format(trans, self.msg)
            else:
                tran_text = trans

            self.translation = tran_text
            self.translation_state = is_fuzzy
            return

        self.finalizeList()

        arched_bracket_list = cm.parseMessageWithDelimiterPair('(', ')', self.msg)
        has_record = (len(arched_bracket_list) > 0)
        if has_record:
            for s, e, txt in arched_bracket_list:
                result_list: RefList = self.findOnePattern(txt, cm.ARCH_BRAKET_MULTI, start_loc=s)
                for k, v in result_list.items():
                    orig = v.getOrigin()
                    o_s, o_e, o_txt = orig.getValues()
                    sub_ref_list = RefList(msg=o_txt)
                    sub_ref_list.findPattern([cm.GA_REF, cm.AST_QUOTE, cm.DBL_QUOTE, cm.SNG_QUOTE])
                    has_sub_ref = (len(sub_ref_list) > 0)
                    if has_sub_ref:
                        sub_ref_list.finalizeList()
                        v.getRefList().clear()
                        for kk, vv in sub_ref_list.items():
                            v.getRefList().append(vv)
                    ref_list_entry = {o_s:v}
                    self.update(ref_list_entry)

        # sorted_list = sorted(self.items(), key=lambda t: t[0])
        # self.clear()
        # self.update(ref_list)

        # pp(self.items())
        # remove redundancies
        self.removeRedundancies()

    def transferTranslation(self, from_item: RefItem, to_item: RefItem):
        ll = rr = from_tran = None
        try:
            from_tran = from_item.getTranslation()
            if not from_tran:
                return

            from_tran_state = from_item.getTranslationState()
            f_s, f_e, f_txt = from_item.getValues()

            to_translation = to_item.getTranslation()
            has_tran = to_translation and (len(to_translation) > 0)
            if not has_tran:
                to_tran = str(to_item.getText())
                to_item.setTranlation(to_tran)
                to_translation = to_tran

            ll = to_translation[:f_s]
            rr = to_translation[f_e:]
            tran = ll + from_tran + rr
            to_item.setTranlation(tran, state=from_tran_state)
        except Exception as e:
            _("from_item", from_item)
            _("to_item", to_item)
            _("ll", ll)
            _("rr", rr)
            _("from_tran", from_tran)
            _(e)
            raise e

    def translateRefItem(self, ref_item: RefItem, original_type=RefType.TEXT):
        valid = (ref_item is not None)
        if not valid:
            return
        orig_text = ref_item.getText()
        valid = (orig_text is not None) and (len(orig_text) > 0)
        if not valid:
            return

        # is_debug = ("Ctrl-MMB" in orig_text)
        # if is_debug:
        #     _("translateRefItem original_type:", original_type)

        is_keyboard = (original_type == RefType.KBD)
        if is_keyboard:
            # keyboard will return original if not there
            tran = self.tf.translateKeyboard(orig_text)
            ref_item.setTranlation(tran)
        else:
            tran, is_fuzzy, is_ignore = self.tf.translate(orig_text)

            if is_ignore:
                ref_item.setTranlation("", TranslationState.IGNORED)
                return

            is_ref_type = (original_type != RefType.TEXT)
            is_menu_type = (original_type == RefType.MENUSELECTION)

            if is_menu_type:
                if tran:
                    tran = "{} ({})".format(tran, orig_text)
                else:
                    tran = "({})".format(orig_text)
            elif is_ref_type:
                if tran:
                    tran = "{} -- {}".format(tran, orig_text)
                else:
                    tran = "-- {}".format(orig_text)

            if tran:
                tran_state = (TranslationState.FUZZY if is_fuzzy else TranslationState.ACCEPTABLE)
                ref_item.setTranlation(tran, state=tran_state)
                #_("translateRefItem ref_item:", ref_item)
                #_(orig_text, "=>" ,ref_item.getTranslation(), " tran_state:", ref_item.getTranslationState())

    def translateRefRecord(self, record: RefRecord):
        valid = (record is not None)
        if not valid:
            return

        orig: RefItem = record.getOrigin()
        orig_text = orig.getText()
        orig_trans, is_fuzzy, is_ignore = self.tf.translate(orig_text) # find the whole piece first to see if it's there
        if is_ignore:
            orig.setTranlation("")
            orig.setTranslationState(TranslationState.IGNORED)
            return

        has_orig_tran = (orig_trans is not None) and (not is_fuzzy)
        if has_orig_tran:
            orig.translation = orig_trans
            orig.translation_state = TranslationState.ACCEPTABLE
            # should clean out all ref list
            return

        original_ref_type = orig.getRefType()
        ref_list: list = record.getRefList()
        for item in reversed(ref_list):
            is_item = isinstance(item, RefItem)
            is_record = isinstance(item, RefRecord)
            if is_record:
                self.translateRefRecord(item)
                self.transferTranslation(item.getOrigin(), orig)
                # # attach translation to orig using original
                # print("attach translation from REFRECORD to original:", item.getOrigin(), "=>", orig)
            else:
                self.translateRefItem(item, original_type= original_ref_type)
                self.transferTranslation(item, orig)
                # # attach translation to orig using ref
                # print("attach translation from REFITEM to original:", item, "=>", orig)

    def translateRefList(self):
        valid = (len(self) > 0)
        if not valid:
            return

        # is_debug = ("Image sequences can use placeholder files" in self.msg)
        # if is_debug:
        #     _("DEBUG")

        self.translation = str(self.msg)
        to_item = RefItem(start=0, end=len(self.msg), txt=self.translation)

        key_list = self.keys()
        rev_key_list = reversed(sorted(key_list))
        for k in rev_key_list:
            v: RefRecord = self[k]
            self.translateRefRecord(v)
            self.transferTranslation(v.getOrigin(), to_item)
            #_("IN LOOP to_item:", to_item)

        #_("FINALLY to_item:", to_item)
        self.setTranslation(to_item.getTranslation(), state=to_item.getTranslationState())

        tr = self.getTranslation()
        has_translation = (tr is not None) and (tr != self.msg)
        if not has_translation:
            tr, must_mark, is_ignore = self.tf.translate(self.msg)
            has_translation = (tr is not None) and (not is_ignore)
            if is_ignore:
                self.setTranslation("", state=TranslationState.IGNORED)
                return

            if self.keep_original:
                if has_translation:
                    tr = "{} -- {}".format(tr, self.msg)
                else:
                    tr = "-- {}".format(self.msg)
            self.setTranslation(tr, state=TranslationState.ACCEPTABLE)
            ## fixing links in current translation here

        #_("FINALLY self.translation :", self.getTranslation())
        #_(self.getTranslation())


    def dumpRefItem(self, ref_item: RefItem, storage_dict:dict):
        valid = (ref_item is not None)
        if not valid:
            return

        orig_text = ref_item.getText()
        valid = (orig_text is not None) and (len(orig_text) > 0)
        if not valid:
            return

        state = ref_item.translation_state
        is_ignore = (state == TranslationState.IGNORED)
        if is_ignore:
            print("dumpRefItem Ignoring:", orig_text)
            return
        
        trans = ref_item.getTranslation()
        txt = (trans if trans is not None else "")
        entry={orig_text:txt}
        # is_the_same = (cm.isTextuallySimilar(orig_text, txt, is_absolute=True))        
        # if is_the_same:
        #     print("dumpRefItem Ignoring, similar:", entry)
        #     return

        storage_dict.update(entry)

    def dumpRefRecord(self, ref_item: RefRecord, storage_dict:dict):
        valid = (ref_item is not None)
        if not valid:
            return

        orig_item: RefItem = ref_item.getOrigin()
        ref_list: list = ref_item.getRefList()
        for item in ref_list:
            is_item = isinstance(item, RefItem)
            is_record = isinstance(item, RefRecord)
            if is_record:
                self.dumpRefRecord(item, storage_dict)
            else:
                self.dumpRefItem(item, storage_dict)
        else:
            self.dumpRefItem(orig_item, storage_dict)

    def dumpRefList(self, dump_dict: dict):
        for k, v in self.items():
            self.dumpRefRecord(v, dump_dict)
        list_item = RefItem(start=0, end=0, txt=self.msg)
        list_item.setTranlation(self.getTranslation())
        list_item.setTranslationState(self.translation_state)
        self.dumpRefItem(list_item, dump_dict)


