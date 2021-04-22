import re
from collections import OrderedDict
from enum import Enum
from reftype import TranslationState, RefType

class MatcherRecordType(Enum):
    MASTER = 0
    SUBRECORD = 1
    LEFT_SYMBOL = 2
    RIGHT_SYMBOL = 3
    INVALID = 4

class MatcherRecord(OrderedDict):
    def __init__(self, s=-1, e=-1, txt=None, matcher_record=None):
        self.s = (s if not matcher_record else matcher_record.start())
        self.e = (e if not matcher_record else matcher_record.end())
        self.txt = (txt if not matcher_record else matcher_record.group(0))
        self.pattern = None
        self.type = None
        self.translation = None
        self.translation_state = TranslationState.UNTRANSLATED

        if not matcher_record:
            self.addSubMatch(self.s, self.e, self.txt)
            return

        start = 0
        end = len(matcher_record.regs)
        s = e = 0
        for index in range(start, end):
            rs, re = matcher_record.regs[index]
            txt = matcher_record.group(index)
            self.addSubMatch(rs, re, txt)

    def __repr__(self):
        string = ""
        try:
            string = "\n{!r}".format(self.__dict__)
        except Exception as e:
            pass
        return string

    def updateMasterLoc(self, s, e):
        self.s = s
        self.e = e
        first_entry = ((s, e), self.txt)
        current_list = self.getSubEntriesAsList()
        current_list.pop(0)
        current_list.insert(0, first_entry)

        self.clear()
        self.update(current_list)

    def setTranlation(self, tran, is_fuzzy: bool, is_ignore: bool):
        if not tran:
            tran = ""

        self.translation = tran
        st = TranslationState.ACCEPTABLE
        if is_fuzzy:
            st = TranslationState.FUZZY
        elif is_ignore:
            st = TranslationState.IGNORED
        self.translation_state = st

    def addSubRecordFromAnother(self, other):
        clist = self.getSubEntriesAsList()
        del clist[1:]
        olist = other.getSubEntriesAsList()
        del olist[0]

        clist.extend(olist)
        self.clear()
        self.update(clist)

    def addSubMatch(self, s: int, e: int, txt: str):
        loc = (s, e)
        entry = {loc: txt}
        self.update(entry)

    def getOriginAsTuple(self):
        loc = (self.s, self.e)
        entry = (loc, self.txt)
        return entry

    def getOriginLoc(self):
        loc = (self.s, self.e)
        return loc

    def getSubEntryByIndex(self, index: int):
        try:
            l = self.getSubEntriesAsList()
            return l[index]
        except Exception as e:
            return None

    def getSubEntriesAsList(self):
        l = list(self.items())
        return l

    def setComponent(self, comp_index, sub_index=None, new_value=None):
        l = self.getSubEntriesAsList()
        comp = sub_comp = None
        try:
            loc, txt = l[comp_index]
            ll = [loc, txt]
            ll[sub_index] = new_value
            new_entry = (ll[0], ll[1])
            l.pop(comp_index)
            l.insert(comp_index, new_entry)
            self.clear()
            self.update(l)
        except Exception as e:
            return None

    def getComponent(self, comp_index, sub_index=None):
        l = self.getSubEntriesAsList()
        comp = sub_comp = None
        try:
            loc, txt = l[comp_index]
            ll = [loc, txt]
            return ll[sub_index]
        except Exception as e:
            return None

    def getMainText(self):
        return self.getComponent(0, sub_index=1)

    def getMainLoc(self):
        return self.getComponent(0, sub_index=0)

    def getSubText(self):
        return self.getComponent(2, sub_index=1)

    def getSubLoc(self):
        return self.getComponent(2, sub_index=0)

    def getType(self):
        sub_comp = self.getComponent(1, sub_index=1)
        is_valid = (bool(sub_comp) and isinstance(sub_comp, RefType))
        if is_valid:
            return sub_comp
        else:
            return None

    def getStarter(self):
        sub_comp = self.getComponent(1, sub_index=1)
        is_valid = (bool(sub_comp) and isinstance(sub_comp, str) and not (sub_comp.startswith(':') and sub_comp.endswith(':')))
        if is_valid:
            return sub_comp
        else:
            return None

    def getEnder(self):
        sub_comp = self.getComponent(3, sub_index=1)
        is_valid = (bool(sub_comp) and isinstance(sub_comp, str))
        if is_valid:
            return sub_comp
        else:
            return None
