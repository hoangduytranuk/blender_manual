import re
from collections import OrderedDict
from enum import Enum
from definition import Definitions as df, \
    TranslationState, \
    RefType, \
    SentStructMode as SMODE, \
    SentStructModeRecord as SMODEREC
import inspect as INP

class MatcherRecordType(Enum):
    MASTER = 0
    SUBRECORD = 1
    LEFT_SYMBOL = 2
    RIGHT_SYMBOL = 3
    INVALID = 4

REF_LINK = re.compile(r'[\s]?[\<]([^\<\>]+)[\>][\s]?')

class MatcherRecord(OrderedDict):
    def __init__(self, s=-1, e=-1, txt=None, matcher_record: re.Match =None):
        self.__s = -1
        self.__e = -1
        self.__txt = None
        self.__pattern = None
        self.__type = None
        self.__translation = None
        self.__translation_state = TranslationState.UNTRANSLATED
        self.__sentence_structure_mode: dict = None
        self.__order_list = None

        actual_s = (matcher_record.start() if matcher_record else s)
        actual_e = (matcher_record.end() if matcher_record else e)
        actual_txt = (matcher_record.group(0) if matcher_record else txt)

        is_init_txt = ((not matcher_record) and bool(actual_txt))
        is_location_added = not ((actual_s == -1) or (actual_e == -1))
        is_init_location = (is_init_txt and not is_location_added)
        if is_init_location:
            actual_s = 0
            actual_e = len(actual_txt)

        self.s = actual_s
        self.e = actual_e
        self.txt = actual_txt
        self.children = None

        if matcher_record:
            start = 0
            end = len(matcher_record.regs)
            s = e = 0
            loc_dict={}
            for index in range(start, end):
                txt = matcher_record.group(index)

                rs, re = matcher_record.regs[index]
                is_found = ((rs >= 0) and (re >= 0))
                if not is_found:
                    continue

                # is_over_lapped = (rs in loc_dict)
                # if is_over_lapped:
                #     continue

                # loc_dict_entry={rs: re}
                # loc_dict.update(loc_dict_entry)

                self.addSubMatch(rs, re, txt)
        else:
            self.addSubMatch(actual_s, actual_e, actual_txt)

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

    @property
    def list_of_forward_slashes(self):
        return self.__list_of_forward_slashes

    @list_of_forward_slashes.setter
    def list_of_forward_slashes(self, new_list_of_forward_slashes):
        self.__list_of_forward_slashes = new_list_of_forward_slashes

    def __repr__(self):
        string = ""
        try:
            string = "\n{!r}".format(self.__dict__)
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
        self.translation_state == TranslationState.ACCEPTABLE

    def appendSubRecords(self, sub_rec_list):
        current_list = self.getSubEntriesAsList()
        current_list.extend(sub_rec_list)
        self.clear()
        self.update(current_list)

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

    def hasMode(self, mode_looking_for: SMODE, is_include_location=False):
        list_modes = self.getListOfModes()
        sent_struct_mode_record: SMODEREC = None
        is_found = False
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
