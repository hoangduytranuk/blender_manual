import re
from collections import OrderedDict
from enum import Enum

class MatcherRecordType(Enum):
    MASTER = 0
    SUBRECORD = 1
    LEFT_SYMBOL = 2
    RIGHT_SYMBOL = 3
    INVALID = 4

class MatcherRecord(OrderedDict):
    def __init__(self, s: int = -1, e: int = -1, txt: str = None, matcher_record : re.Match = None):
        self.s = (s if not matcher_record else matcher_record.start())
        self.e = (e if not matcher_record else matcher_record.end())
        self.txt = (txt if not matcher_record else matcher_record.group(0))
        self.pattern = None
        self.type = None

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

    def updateMaster(self, nss, nee, ntxt, using_record=None):
        if using_record:
            (nss, nee), ntxt = using_record

        self.s = nss
        self.e = nee
        self.txt = ntxt
        self.updateSubRecords(nss, nee)

    def addSubRecordFromAnother(self, other):
        clist = self.getSubEntriesAsList()
        (cs, ce), ctxt = clist[0]

        olist = other.getSubEntriesAsList()
        nsublist = []
        for (sub_s, sub_e), sub_txt in olist:
            is_a_valid_sub_record = bool(sub_txt)
            if not is_a_valid_sub_record:
                ns = sub_s
                ne = sub_e
            else:
                ns = cs + sub_s
                ne = ns + len(sub_txt)
            nloc = (ns, ne)
            nentry = (nloc, sub_txt)
            nsublist.append(nentry)

        clist.extend(nsublist)
        self.clear()
        self.update(clist)

    def updateSubRecordsUsingLoc(self, loc:tuple):
        self.updateSubRecords(loc[0], loc[1])

    def updateSubRecords(self, nss:int, nee:int):
        current_list = self.getSubEntriesAsList()
        new_list = []
        for (cs, ce), ctxt in current_list:
            has_text = bool(ctxt)
            if has_text:
                ccs = cs + nss
                cce = ccs + len(ctxt)
            else:
                ccs = cs
                cce = ce
            nentry = ((ccs, cce), ctxt)
            new_list.append(nentry)

        self.clear()
        self.update(new_list)

    def setMainToUseExistingIndex(self, idx: int):
        is_no_change = (idx <= 0)
        if is_no_change:
            return

        current_list = self.getSubEntriesAsList()
        try:
            (cs, ce), ctxt = current_list[idx]
            self.updateMaster(cs, ce, ctxt)
        except Exception as e:
            raise e

    def updateMasterLoc(self, nloc:tuple):
        ns, ne = nloc
        self.updateMaster(ns, ne, self.txt)

    def updateMasterUsingLoc(self, nloc:tuple, ntxt:str):
        ns, ne = nloc
        self.updateMaster(ns, ne, ntxt)

    def updateEntryByIndexUsingLoc(self, index, loc, n_txt):
        ss, ee = loc
        self.updateEntryByIndex(index, ss, n_txt)

    def updateEntryByIndex(self, index, start, new_txt):
        try:
            new_list = []
            current_list = self.getSubEntriesAsList()
            current_entry = current_list[index]
            (cs, ce), ctxt = current_entry
            cs += start
            ce = ((cs + len(new_txt)) if new_txt else (cs + len(ctxt)))
            if new_txt:
                ctxt = new_txt
            loc = (cs, ce)
            new_entry = (loc, ctxt)

            current_list.pop(index)
            current_list.insert(index, new_entry)

            self.clear()
            self.update(new_list)
            is_first_entry = (index == 0)
            if is_first_entry:
                self.updateMasterUsingLoc(loc, ctxt)
        except Exception as e:
            print(e)
            raise e

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