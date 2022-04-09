import re
from collections import OrderedDict
from enum import Enum

from definition import RefType, \
    Definitions as df, \
    TranslationState, \
    SentStructMode as SMODE, \
    SentStructModeRecord as SMODEREC

class MatcherRecordType(Enum):
    MASTER = 0
    SUBRECORD = 1
    LEFT_SYMBOL = 2
    RIGHT_SYMBOL = 3
    INVALID = 4

REF_LINK = re.compile(r'[\s]?[<]([^<>]+)[>][\s]?')

class MatcherRecord(OrderedDict):

    def __init__(self, s=-1, e=-1, txt=None, matcher_record: re.Match =None, ref_type: RefType = RefType.TEXT, pattern=None):
        self.__s: int = -1
        self.__e: int = -1
        self.__txt: str = None
        self.__pattern: re.Pattern = None
        self.__type: RefType = None
        self.__translation: str = None
        self.__translation_state: TranslationState = TranslationState.UNTRANSLATED
        self.__sentence_structure_mode: dict = None
        self.__order_list: list = None

        is_using_matcher_record = bool(matcher_record)
        if is_using_matcher_record:
            actual_s = (matcher_record.start() if matcher_record else s)
            actual_e = (matcher_record.end() if matcher_record else e)
            actual_txt = (matcher_record.group(0) if matcher_record else txt)
        else:
            actual_s = s
            actual_e = e
            actual_txt = txt

        self.type = ref_type
        self.pattern = pattern

        searched_ref_type = RefType.getRef(actual_txt)
        is_found = (searched_ref_type is not None)
        self.type = (searched_ref_type if is_found else ref_type)

        is_init_txt = ((not is_using_matcher_record) and bool(actual_txt))
        is_location_added = not ((actual_s == -1) or (actual_e == -1))
        is_init_location = (is_init_txt and not is_location_added)
        if is_init_location:
            actual_s = 0
            actual_e = len(actual_txt)

        self.s = actual_s
        self.e = actual_e
        self.txt = actual_txt
        self.children = None

        if is_using_matcher_record:
            self.addRecord(matcher_record)

    @classmethod
    def reproduce(cls, new_s=-1, new_e=-1, new_txt=None, new_matcher_record: re.Match =None):
        return cls( s=new_s, e=new_e, txt=new_txt, matcher_record = new_matcher_record)

    def clone(self):
        new_inst = MatcherRecord.reproduce(new_s=self.s, new_e=self.e, new_txt=self.txt, new_matcher_record=None)
        return new_inst

    def override(self, new_root_loc = None, new_txt_len = None):
        def calNewLoc(current_loc):
            (cs, ce) = current_loc
            (ns, ne) = new_root_loc
            new_s = (ns + cs)
            if new_txt_len:
                new_e = (new_s + new_txt_len)
            else:
                dist = (ce - cs)
                new_e = (new_s + dist)
            return (new_s, new_e)

        new_loc = calNewLoc(self.loc)
        self.loc = new_loc
        new_sub_list = OrderedDict()
        for index, (loc, txt) in enumerate(self.getSubEntriesAsList()):
            new_loc = calNewLoc(loc)
            entry = {new_loc: txt}
            new_sub_list.update(entry)
        self.clear()
        self.update(new_sub_list)

    @property
    def loc(self):
        return (self.s, self.e)

    @loc.setter
    def loc(self, new_loc):
        (ns, ne) = new_loc
        (self.s, self.e) = (ns, ne)

    def addRecord(self, matcher_record: re.Match):
        blank_msg = str(self.txt)
        if matcher_record:
            start = 0
            end = len(matcher_record.regs)
            s = e = 0
            loc_dict={}
            start_spaces = end_spaces = ""
            valid_locs = []
            for index, (rs, re) in enumerate(matcher_record.regs):
                valid = (rs < re)
                if not valid:
                    continue
                loc = (rs, re)
                valid = not (loc in valid_locs)
                if not valid:
                    continue
                valid_locs.append(loc)
                txt = matcher_record.group(index)
                self.addSubMatch(rs, re, txt)
        else:
            self.addSubMatch(self.s, self.e, self.txt)

    @property
    def order_list(self):
        return self.__order_list

    @order_list.setter
    def order_list(self, new_list):
        self.__order_list = new_list

    @property
    def smode(self):
        return self.__sentence_structure_mode

    @smode.setter
    def smode(self, new_mode):
        self.__sentence_structure_mode = new_mode

    @property
    def s(self):
        return self.__s

    @s.setter
    def s(self, new_s):
        self.__s = new_s

    @property
    def e(self):
        return self.__e

    @e.setter
    def e(self, new_e):
        self.__e = new_e

    @property
    def txt(self):
        return self.__txt

    @txt.setter
    def txt(self, new_txt):
        self.__txt = new_txt

    @property
    def pattern(self):
        return self.__pattern

    @pattern.setter
    def pattern(self, new_pattern):
        self.__pattern = new_pattern

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, new_type):
        self.__type = new_type

    @property
    def translation(self):
        return self.__translation

    @translation.setter
    def translation(self, new_translation):
        self.__translation = new_translation

    @property
    def translation_state(self):
        return self.__translation_state

    @translation_state.setter
    def translation_state(self, new_translation_state):
        self.__translation_state = new_translation_state

    def __repr__(self):
        string = ""
        try:
            # string = '\n----MatcherRecord start------\n'
            # string += "\nMAIN-RECORD:\n{!r}".format(self.__dict__)
            string += f'txt:[{self.txt}]\n'
            string += f'type:[{self.type}]\n'
            sub_list = self.getSubEntriesAsList()
            if sub_list:
                string += "SUB-LIST:{!r}\n".format(sub_list)
                # string += "\nSUB-LIST:\n{!r}\n".format(sub_list)
            # string += '\n----MatcherRecord end------\n'
        except Exception as e:
            pass
        return string

    # this is for use with SentStruct, do not change
    def initUsingList(self, list_of_loc_and_txt, original_text=None, pattern=None):
        try:
            if not original_text:
                temp_dict = OrderedDict(list_of_loc_and_txt)
                text_list = temp_dict.values()
                original_text = ' '.join(text_list)

            list_len = len(list_of_loc_and_txt)
            (fs, fe), first_txt = list_of_loc_and_txt[0]
            (ls, le), last_txt = list_of_loc_and_txt[list_len-1]
            self.txt = original_text
            self.s = fs
            self.e = le
            self.pattern = pattern
            self.clear()
            self.update(list_of_loc_and_txt)
        except Exception as e:
            df.LOG(f'{e}; initUsingList(), list_of_loc_and_txt:[{list_of_loc_and_txt}]; original_text:[{original_text}]', error=True)
            raise e

    def isIgnored(self):
        state = (self.translation_state == TranslationState.IGNORED)
        return state

    def isFuzzy(self):
        state = (self.translation_state == TranslationState.FUZZY)
        return state

    def isRemove(self):
        state = (self.translation_state == TranslationState.REMOVE)
        return state

    def isUntranslated(self):
        state = (self.translation_state == TranslationState.UNTRANSLATED)
        return state

    def isTranslated(self):
        is_translated = (self.translation_state == TranslationState.ACCEPTABLE)
        state = (self.isIgnored() or self.isRemove() or is_translated)
        return state

    def setTranslated(self):
        self.translation_state = TranslationState.ACCEPTABLE

    def appendSubRecords(self, sub_rec_list):
        current_list = self.getSubEntriesAsList()
        current_list.extend(sub_rec_list)
        self.clear()
        self.update(current_list)

    def updateMasterLocTuple(self, new_loc):
        (ns, ne) = new_loc
        self.updateMasterLoc(ns, ne)

    def updateMasterLoc(self, s, e):
        current_list = self.getSubEntriesAsList()
        new_list = []
        for (cloc, txt) in current_list:
            (cs, ce) = cloc
            ns = cs + s
            ne = ns + len(txt)
            new_loc = (ns, ne)
            new_entry = (new_loc, txt)
            new_list.append(new_entry)
        self.s = s
        txt_len = len(self.txt)
        self.e = self.s + txt_len
        self.clear()
        self.update(new_list)

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

    def hasMode(self, mode_looking_for: SMODE, is_include_location=False):
        list_modes = self.getListOfModes()
        sent_struct_mode_record: SMODEREC = None
        is_found = False
        smode_loc = None
        for smode_loc, sent_struct_mode_record_list in list_modes:
            for sent_struct_mode_record in sent_struct_mode_record_list:
                is_found = (sent_struct_mode_record.smode == mode_looking_for)
                if not is_found:
                    continue

                loc = (smode_loc if is_include_location else None)
                entry = (is_found, loc)
                return entry

        loc = (smode_loc if is_include_location else None)
        entry = (is_found, loc)
        return entry

    def getListOfModes(self):
        list_of_modes = []
        smode_dict: OrderedDict = None
        try:
            smode_dict = self.smode
            for smode_loc, value in smode_dict.items():
                (pat_txt, sent_struct_mode_record) = value
                if not sent_struct_mode_record:
                    continue

                entry = (smode_loc, sent_struct_mode_record)
                list_of_modes.append(entry)
        except Exception as e:
            pass
        return list_of_modes

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
            has_sub_index = not (sub_index is None)
            if has_sub_index:
                return ll[sub_index]
            else:
                return ll
        except Exception as e:
            return None

    def getMainEntry(self):
        try:
            l = self.getSubEntriesAsList()
            return l[0]
        except Exception as e:
            return None

    def getMainText(self):
        return self.getComponent(0, sub_index=1)

    def getMainLoc(self):
        return self.getComponent(0, sub_index=0)

    def getSubText(self):
        result = self.getComponent(2, sub_index=1)
        if not result:
            result = self.getComponent(1, sub_index=1)
        return result

    def getSubLoc(self):
        result = self.getComponent(2, sub_index=0)
        if not result:
            result = self.getComponent(1, sub_index=0)
        return result

    def getType(self):
        sub_comp = self.getComponent(1, sub_index=1)
        return sub_comp

    def getTypeLoc(self):
        sub_comp = self.getComponent(1, sub_index=0)
        return sub_comp

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
