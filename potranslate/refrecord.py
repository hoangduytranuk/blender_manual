from common import Common as cm, dd, pp
from reftype import RefType
from copy import deepcopy
from reftype import TranslationState
from refitem import RefItem
from err import ErrorMessages as er

class RefRecord:
    def __init__(self, origin: RefItem = None, reflist: list = [], pat=None, my_parent=None):
        self.origin: RefItem = origin
        self.reflist: list = reflist
        self.pattern: str = pat
        self.parent=my_parent
        # self.setOriginType()
        self.setParentForChildren()

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

    def setParentForChildren(self):
        ref_item: RefItem = None
        for ref_item in self.reflist:
            ref_item.parent = self
        self.origin.parent = self

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

    def removeBlankFromText(self):
        if self.origin:
            self.origin.removeBlankFromText()
            if self.origin.hasExtraItems():
                print(f'origin:{self.origin}')
                pp(self.origin.extra_list)
                raise ValueError(er.UNEXPECTED_ADDITIONAL_REF_RECORD)

        if self.reflist:
            ref_item: RefItem = None
            for ref_item in self.reflist:
                ref_item.removeBlankFromText()
                if ref_item.hasExtraItems():
                    print(f'ref_item:{ref_item}')
                    pp(self.origin.extra_list)
                    raise ValueError(er.UNEXPECTED_ADDITIONAL_REF_RECORD)

    def translate(self):
        # translate the ref_list

        translation = str(self.getOriginText())
        ref_list = self.reflist
        has_ref_list = bool(ref_list)
        if not has_ref_list:
            self.getOrigin().translate()
            return

        item: RefItem = None
        for item in reversed(ref_list):
            ref_type = item.getRefType()

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

            item.translate()
            state = item.translation_state
            is_ignore = (state == TranslationState.IGNORED)
            if is_ignore:
                continue

            tran = item.getTranslation()
            if not tran:
                continue

            s, e = item.getLocation()
            left = translation[:s]
            right = translation[e:]
            translation = left + tran + right

        is_same = (translation == self.getOriginText())
        if not is_same:
            is_fuzzy = self.isFuzzy()
            is_ignore = self.isIgnore()
            self.origin.setTranlation(translation, is_fuzzy, is_ignore)