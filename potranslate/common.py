import os
import operator as OP
from re import Pattern, Match, compile
from collections import OrderedDict
from pprint import pp
import hashlib
import time
from reftype import RefType
from collections import deque
from fuzzywuzzy import fuzz
from bisect import bisect_left
from matcher import MatcherRecord
from err import ErrorMessages as ER
import operator
import re
import copy as CP
from definition import Definitions as df

DEBUG=True
# DEBUG=False
DIC_LOWER_CASE=True

def dd(*args, **kwargs):
    if DEBUG:
        print(args, kwargs)
        if len(args) == 0:
            print('-' * 80)

class LocationObserver(OrderedDict):
    def __init__(self, msg):
        self.blank = str(msg)
        self.marked_loc={}

    def getTextAt(self, s: int, e: int):
        try:
            txt = self.blank[s:e]
            return txt
        except Exception as e:
            return None

    def getTextAtLoc(self, loc: tuple):
        (s, e) = loc
        return self.getTextAt(s, e)

    def markListAsUsed(self, loc_list:list):
        for loc in loc_list:
            self.markLocAsUsed(loc)

    def markAsUsed(self, s: int, e: int):
        loc = (s, e)
        is_already_marked = (loc in self.marked_loc)
        if is_already_marked:
            return

        marked_loc_entry = {loc: self.blank[s:e]}
        blk = (df.FILLER_CHAR * (e - s))
        left = self.blank[:s]
        right = self.blank[e:]
        self.blank = left + blk + right
        self.marked_loc.update(marked_loc_entry)

    def markLocAsUsed(self, loc: tuple):
        ss, ee = loc
        self.markAsUsed(ss, ee)

    def isPartlyUsed(self, s: int, e: int):
        part = self.blank[s:e]
        is_dirty = (df.FILLER_PARTS.search(part) is not None)
        is_fully_used = (df.FILLER_CHAR_ALL_PATTERN.search(part) is not None)
        return (is_dirty and not is_fully_used)

    def isLocPartlyUsed(self, loc: tuple):
        s, e = loc
        return self.isPartlyUsed(s, e)

    def isLocFullyUsed(self, loc: tuple):
        s, e = loc
        return self.isFullyUsed(s, e)

    def isFullyUsed(self, s:int, e:int):
        part = self.blank[s:e]
        is_all_used = (df.FILLER_CHAR_ALL_PATTERN.search(part) is not None)
        return is_all_used

    def isUsed(self, s: int, e: int):
        part = self.blank[s:e]
        is_dirty = (df.FILLER_PARTS.search(part) is not None)
        return is_dirty

    def isLocUsed(self, loc: tuple):
        s, e = loc
        return self.isUsed(s, e)

    def isCompletelyUsed(self):
        is_fully_done = (df.FILLER_CHAR_ALL_PATTERN.search(self.blank) is not None)
        return is_fully_done

    def getUnmarkedPartsAsDict(self):
        untran_dict = Common.findInvert(df.FILLER_PARTS, self.blank, is_reversed=True)
        return untran_dict

class Common:
    def isPath(txt: str) -> bool:
        def insertTextOutsideEntry():
            is_valid = (ee > ss)
            if not is_valid:
                return False

            text_outside_url = txt[ss:ee]
            ex_loc = (ss, ee)
            entry = {ex_loc: text_outside_url}
            text_outside_url_list.update(entry)
            return True

        if not txt:
            return False

        is_path = (df.PATH_CHECKER.search(txt) is not None)
        if is_path:
            return True

        urls = df.urlx_engine.find_urls(txt, get_indices=True)
        if not urls:
            return False

        # 1. Find the list of urls and put into dictionary so locations can be extracted, uing keys
        url_loc_list = {}
        for url, loc in urls:
            url_length = len(url)
            entry = {loc: url}
            url_loc_list.update(entry)


        # 2. find all the text outside the links and see if they are just spaces and symbols only, which can be classified as
        # IGNORABLE
        text_outside_url_list = {}
        ss = 0
        for loc in url_loc_list.keys():
            s, e = loc
            ee = s
            insertTextOutsideEntry()
            ss = e
        url = url_loc_list[loc]
        ee = len(url)
        insertTextOutsideEntry()

        # 3. Find out if text outside are but all symbols (non-alpha), which means they are discardable (non-translatable)
        is_ignorable = True
        for loc, text_outside in text_outside_url_list.items():
            is_all_symbols = df.SYMBOLS_ONLY.search(text_outside)
            if not is_all_symbols:
                is_ignorable = False

        return is_ignorable

    def isLinkPath(txt: str) -> bool:
        # is_file_extension = df.FILE_EXTENSION.search(txt)
        # is_file_name = df.FILE_NAME_WITH_EXTENSION.search(txt)
        is_path = Common.isPath(txt)
        if is_path:
            return True

        left, mid, right = Common.getTextWithin(txt)
        is_path = Common.isPath(mid)
        return is_path
        # is_path_link = (is_file_extension or is_file_name or is_path)
        # return is_path_link

    def shouldHaveDuplicatedEnding(cutoff_part, txt):
        is_verb_cutoff = (cutoff_part in ['ed', 'ing', 'es'])
        if not is_verb_cutoff:
            return False

        is_dup = (df.EN_DUP_ENDING.search(txt) is not None)
        return is_dup

    def replaceArchedQuote(txt):
        new_txt = str(txt)
        new_txt = re.sub('\)', ']', new_txt)
        new_txt = re.sub('\(', '[', new_txt)
        # new_txt = new_txt.replace('"', '\\\"')
        return new_txt

    def hasOriginal(msg, tran):
        orig_list = df.ALPHA_NUMERICAL.findall(msg)
        orig_set = "".join(orig_list)

        tran_list = df.ALPHA_NUMERICAL.findall(tran)
        tran_set = "".join(tran_list)

        has_orig = (orig_set in tran_set)
        #print("orig_set:", orig_set)
        #print("tran_set:", tran_set)
        #print("has_orig:", has_orig)
        return has_orig

    def isSpecialTerm(msg: str):
        is_special = (df.SPECIAL_TERM.search(msg) is not None)
        return is_special

    def matchCase(from_str : str , to_str : str):
        WORD_SHOULD_BE_LOWER = [
            'trong',
            'các',
            'những',
            'và',
            'thì'
            'là',
            'hoặc',
            'mà',
            'có',
            'của',
            'với',
            'đến',
            'tới',
        ]
        def lowercase(loc_text_dict, new_str):
            mm: MatcherRecord = None
            for loc, mm in ga_ref_dic.items():
                (s, e), text = mm.getOriginAsTuple()
                lcase_text = text.lower()
                left_part = new_str[:s]
                right_part = new_str[e:]
                new_str = left_part + lcase_text + right_part
            return new_str

        valid = (from_str and to_str)
        if not valid:
            return to_str

        new_str = str(to_str)

        first_char = from_str[0]
        remain_part = from_str[1:]

        from_str_has_multi_words = (df.SYMBOLS.search(from_str) is not None)
        to_str_has_multi_words = (df.SYMBOLS.search(to_str) is not None)

        from_string_is_to_first_upper = (first_char.isupper() and remain_part.islower())
        to_string_is_to_first_upper = not (from_str_has_multi_words or to_str_has_multi_words)

        is_first_upper = (first_char.isupper() and remain_part.islower())
        if is_first_upper:
            first_char = new_str[0].upper()
            remain_part = new_str[1:].lower()
            new_str = first_char + remain_part
        else:
            is_lower = (from_str.islower())
            if is_lower:
                new_str = new_str.lower()
                return new_str
            else:
                is_title = (from_str.istitle())
                if is_title:
                    new_str = new_str.title()
                else:
                    is_upper = (from_str.isupper())
                    if is_upper:
                        new_str = new_str.upper()

        # ensure ref keywords ':doc:' is always lowercase
        ga_ref_dic = Common.patternMatchAll(df.GA_REF_PART, new_str)
        new_str = lowercase(ga_ref_dic, new_str)
        for lcase_word in WORD_SHOULD_BE_LOWER:
            p = re.compile(r'\b%s\b' % lcase_word)
            p_list = Common.patternMatchAll(p, new_str)
            new_str = lowercase(p_list, new_str)

        return new_str

    def beginAndEndPunctuation(msg, is_single=False):
        if is_single:
            begin_with_punctuations = (df.BEGIN_PUNCTUAL_SINGLE.search(msg) is not None)
            ending_with_punctuations = (df.ENDS_PUNCTUAL_SINGLE.search(msg) is not None)
            if begin_with_punctuations:
                msg = df.BEGIN_PUNCTUAL_SINGLE.sub("", msg)
            if ending_with_punctuations:
                msg = df.ENDS_PUNCTUAL_SINGLE.sub("", msg)
        else:
            begin_with_punctuations = (df.BEGIN_PUNCTUAL_MULTI.search(msg) is not None)
            ending_with_punctuations = (df.ENDS_PUNCTUAL_MULTI.search(msg) is not None)
            if begin_with_punctuations:
                msg = df.BEGIN_PUNCTUAL_MULTI.sub("", msg)
            if ending_with_punctuations:
                msg = df.ENDS_PUNCTUAL_MULTI.sub("", msg)

        return msg, begin_with_punctuations, ending_with_punctuations

    def removeOriginal(msg, trans):
        if not trans:
            return trans

        has_abbr = Common.hasAbbr(trans)
        if has_abbr:
            return trans

        msg = re.escape(msg)
        p = r'\b{}\b'.format(msg)
        has_original = (re.search(p, trans, flags=re.I) is not None)
        endings_list = ["", "s", "es", "ies", "ed", "ing", "lly",]
        endings = sorted(endings_list, key=lambda x: len(x), reverse=True)

        if has_original:
            for end in endings:
                p = r'{}{}:\ '.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

                p = r'-- {}{}'.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

                p = r' ({}{})'.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

            for end in endings:
                p = r'{}{} --'.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

                p = r'({}{}) '.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

            for end in endings:
                p = r'\\b{}{}\\b'.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

                p = r'\\b({}{})\\b'.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

            trans = trans.strip()
            is_empty = (len(trans) == 0)
            if is_empty:
                trans = None
        return trans

    def cleanSlashesQuote(msg):
        if not msg:
            return msg

        msg = msg.replace("\\\\", "\\")
        msg = msg.replace("\\\"", "\"")
        return msg

    def patternMatch(pat: re.Pattern, text) -> MatcherRecord:
        m = pat.search(text)
        is_found = (m is not None)
        if not is_found:
            return None

        match_record = MatcherRecord(matcher_record=m)
        return match_record

    def patternMatchAll(pat, text):
        return_dict = {}
        try:
            for m in pat.finditer(text):
                match_record = MatcherRecord(matcher_record=m)
                match_record.pattern = pat
                loc = match_record.getMainLoc()
                dict_entry = {loc: match_record}
                return_dict.update(dict_entry)
        except Exception as e:
            print(f'patternMatchAll() pattern:[{pat}]; text:[{text}]')
            raise e
        return return_dict


    def findInvert(pattern, text:str, is_reversed=False):
        '''
        findInvert:
            Find list of words that are NOT matching the pattern.
            can use to find words amongst puntuations for instance.
            The routine uses internally declared FILLER_CHAR to mark the
            boundaries of unmatched words and then SPLIT at these boundaries
        :param pattern:
            the re.compile(d) pattern to use to find/replace
        :param text:
            the string of text that words are to be found
        :return:
            list of words that are NOT matching the pattern input
        '''

        is_string = isinstance(pattern, str)
        invert_required = False
        pat = pattern
        if is_string:
            # form the invert character pattern
            pat_string = r'(%s)(\w[^%s]+\w)(%s)' % (pattern, pattern, pattern)
            pat = compile(pat_string)
        else:
            invert_required = True

        found_list = []
        mm : MatcherRecord = None
        matched_dict = Common.patternMatchAll(pat, text)
        if not invert_required:
            for mmloc, mm in matched_dict.items():
                mm.type = RefType.TEXT
                mm.pattern = pat
                loc, found_txt = mm.getOriginAsTuple()
                entry = (loc, mm)
                found_list.append(entry)
        else:
            # 2: extract location list
            loc_list = matched_dict.keys()

            # 3: extract invert locations, using the location list above
            invert_loc_list = []
            ws = we = 0
            for s, e in loc_list:
                we = s
                if (ws < we):
                    invert_loc_list.append((ws, we))
                ws = e
            we = len(text)
            if (ws < we):
                invert_loc_list.append((ws, we))

            # 4: using the invert location list, extract words, exclude empties.
            for ws, we in invert_loc_list:
                found_txt = text[ws:we]
                left, mid, right = Common.getTextWithin(found_txt)
                is_empty = (not bool(mid))
                if is_empty:
                    continue

                loc = (ws, we)
                mm = MatcherRecord(s=ws, e=we, txt=found_txt)
                mm.type = RefType.TEXT
                mm.pattern = pat
                entry = (loc, mm)
                found_list.append(entry)

        if is_reversed:
            found_list.sort(key=OP.itemgetter(0), reverse=True)

        return_dict = OrderedDict(found_list)
        # dd('findInvert() found_list:')
        # dd('-' * 30)
        # pp(return_dict)
        # dd('-' * 30)
        return return_dict

    def getListOfLocation(find_list):
        loc_list = {}
        for k, v in find_list.items():
            s = v[0][0]
            e = v[0][1]
            t = v[0][2]
            entry = {k: [s, e, t]}
            loc_list.update(entry)
        return loc_list

    def inRange(item, ref_list):
        i_s, i_e, i_t = item
        for k, v in ref_list.items():
            r_s, r_e, r_t = v
            is_in_range = (i_s >= r_s) and (i_e <= r_e)
            if is_in_range:
                return True
        else:
            return False

    def diffLocation(ref_list, keep_list):
        loc_keep_list = {}
        for k, v in keep_list.items():
            in_forbiden_range = Common.inRange(v, ref_list)
            if not in_forbiden_range:
                s, e, txt = v
                ee = (s, e, txt)
                entry = {s: [ee]}
                loc_keep_list.update(entry)

        return loc_keep_list

    def mergeTwoLists(primary, secondary):

        loc_primary_list = Common.getListOfLocation(primary)
        loc_secondary_list = Common.getListOfLocation(secondary)
        keep_list = Common.diffLocation(loc_primary_list, loc_secondary_list)

        #pp(keep_list)
        for k, v in keep_list.items():
            keep_v = secondary[k]
            entry={k:keep_v}
            primary.update(entry)

        return primary

    def filteredTextList(ref_list, norm_list):
        loc_ref_list = Common.getListOfLocation(ref_list)
        loc_norm_list = Common.getListOfLocation(norm_list)
        keep_norm_list = Common.diffLocation(loc_ref_list, loc_norm_list)
        return keep_norm_list

    def getTextListForMenu(text_entry):
        entry_list = []

        matched_list = Common.findInvert(df.MENU_SEP, text_entry, is_reversed=True)
        for loc, mtxt in matched_list.items():
            ss, ee = loc
            entry=(ss, ee, mtxt)
            entry_list.append(entry)
        return entry_list

    def isListEmpty(list_elem):
        is_empty = (list_elem is None) or (len(list_elem) == 0)
        return is_empty

    def removeLowerCaseDic(dic_list : dict ):
        l_case = {}
        u_case = {}
        k = None
        v = None
        try:
            for i, e in enumerate(dic_list.items()):
                k, v = e
                if not k:
                    continue

                is_lower_k = (k.islower())
                if is_lower_k:
                    l_case.update({k: v})
                else:
                    u_case.update({k: v})

            u_l_case = dict((k.lower(), v) for k, v in u_case.items())

            l_case_remain = {}
            for k, v in l_case.items():
                if k in u_l_case:
                    continue
                else:
                    l_case_remain.update({k: v})
            u_case.update(l_case_remain)
        except Exception as e:
            dd("k:", k)
            dd("v:", k)
            dd(e)
            raise e
        return u_case

    def isTextuallySimilar(from_txt, to_txt):
        from_list = df.WORD_ONLY_FIND.findall(from_txt.lower())
        to_list = df.WORD_ONLY_FIND.findall(to_txt.lower())

        # convert list to set of words, non-repeating
        to_set = "".join(to_list)
        from_set = "".join(from_list)

        is_similar = (to_set in from_set) or (from_set in to_set)
        if not is_similar:
            from_set = set(from_set)
            to_set = set(to_set)
            intersect_set = from_set.intersection(to_set)
            is_similar = (intersect_set == from_set) or (intersect_set == to_set)
        return is_similar

    # def isTextuallyVerySimilar(from_txt, to_txt):
    #     similar_ratio = LE.ratio(from_txt, to_txt)
    #     acceptable = (similar_ratio >= 0.75)
    #     return acceptable

    def isTextuallySame(from_txt:str, to_txt:str):

        is_valid = (from_txt is not None) and (to_txt is not None)
        is_both_none = (from_txt is None) and (to_txt is None)
        if is_both_none:
            return True
        if not is_valid:
            return False

        from_list = df.WORD_ONLY_FIND.findall(from_txt.lower())
        to_list = df.WORD_ONLY_FIND.findall(to_txt.lower())

        # convert list to set of words, non-repeating
        to_set = "".join(to_list)
        from_set = "".join(from_list)

        # perform set intersection to find common set
        is_same = (to_set == from_set)
        return is_same

    def isTextuallySubsetOf(msg, tran):
        msg_list = df.WORD_ONLY_FIND.findall(msg.lower())
        tran_list = df.WORD_ONLY_FIND.findall(tran.lower())
        msg_str = "".join(msg_list)
        tran_str = "".join(tran_list)

        # perform set intersection to find common set
        is_subset = (msg_str in tran_str)
        return is_subset

    def alterValue(orig_value, alter_value=0, op=None):
        altering = (op is not None)
        if altering:
            if op == "+":
                orig_value += alter_value
            elif op == "=":
                orig_value -= alter_value
            elif op == "*":
                orig_value *= alter_value
            elif op == "/":
                orig_value /= alter_value
            elif op == "%":
                orig_value %= alter_value
            elif op == "=":
                orig_value = alter_value
        return orig_value

    def parseMessageWithDelimiterPair(open_char, close_char, msg):
        valid = (open_char is not None) and (close_char is not None) and (msg is not None) and (len(msg) > 0)
        if not valid:
            return None

        is_pair_same_char = (open_char == close_char)
        if is_pair_same_char:
            raise Exception("Open and close symbols must not be the same!")

        loc_list:list = []
        b_list=[]
        l = len(msg)
        s = e = 0
        k = -1
        for i in range(0, l):
            c = msg[i]
            is_open = (c == open_char)
            is_close = (c == close_char)
            if is_open:
                b_list.append(i)
            elif is_close:
                try:
                    last_s = b_list[-1]
                    b_list.pop()
                    txt = msg[last_s:i+1]
                    loc_list_entry=(last_s, i+1, txt)
                    loc_list.append(loc_list_entry)

                    ll = msg[:last_s]
                    rr = msg[i+1:]
                    ltxt = ll + txt + rr
                    is_same = (ltxt == msg)
                    if not is_same:
                        raise Exception("ERROR in location calculation for: [", txt, "] at start:", last_s, " end:", i+1, " in:[", msg, "]")
                except Exception as e:
                    continue
                    # msg = "Unbalanced pair [{},{}] at location:{}, message:[{}]".format(open_char, close_char, i, msg)
                    # print(e)
                    # raise Exception(msg)

        # has_unprocessed_pair = (len(b_list) > 0)
        # if has_unprocessed_pair:
        #     # msg = "Unbalanced pair [{},{}] at location:{}, message:[{}]".format(open_char, close_char, b_list, msg)
        #     # raise Exception(msg)

        has_loc_list = (len(loc_list) > 0)
        if not has_loc_list:
            return []
        else:
            sorted_loc_list = []
            sorted_loc_list = sorted(loc_list, key=lambda x: x[0])
            return sorted_loc_list

    # https://stackoverflow.com/questions/22058048/hashing-a-file-in-python , answered Jul 2 '17 at 17:23 - maxschlepzig (Georg Sauthoff)
    #
    # maxschlepzig
    # 23.3k99 gold badges9393 silver badges126
    def sha256sum(filename):
        h = hashlib.sha256()
        b = bytearray(df.PAGE_SIZE) # PAGE_SIZE = 20 * 4096, original 128*1024
        mv = memoryview(b)
        with open(filename, 'rb', buffering=0) as f:
            for n in iter(lambda : f.readinto(mv), 0):
                h.update(mv[:n])
        return h.hexdigest()

    def getFileModifiedTime(filename):
        return time.ctime( os.path.getmtime(filename))

    def getFileCreatedTime(filename):
        return time.ctime( os.path.getctime(filename))

    def removeLeadingTrailingSymbs(txt):
        def cleanForward(txt, pair_dict, leading_set):
            if not leading_set:
                return txt, leading_set

            temp_txt = str(txt)
            count = 0
            for sym_on in leading_set:
                is_sym_on_in_dict = (sym_on in pair_dict)
                if not is_sym_on_in_dict:
                    continue

                sym_off = pair_dict[sym_on]
                temp = temp_txt[1:]
                is_balance = Common.isBalancedSymbol(sym_on, sym_off, temp)
                if is_balance:
                    temp_txt = temp
                    count += 1
            if count > 0:
                leading_set = leading_set[count:]
            return temp_txt, leading_set

        def cleanBackward(txt, pair_dict, trailing_set):
            if not trailing_set:
                return txt, trailing_set

            temp_txt = str(txt)
            count = 0
            for sym_off in reversed(trailing_set):
                is_controlled = (sym_off in pair_dict)
                if not is_controlled:
                    temp_txt = temp_txt[:-1]
                    count += 1
                    continue

                sym_on = pair_dict[sym_off]
                temp = temp_txt[:-1]
                is_balance = Common.isBalancedSymbol(sym_on, sym_off, temp)
                if is_balance:
                    temp_txt = temp
                    count += 1
            if count > 0:
                trailing_set = trailing_set[:-count]
            return temp_txt, trailing_set

        def cleanBothEnds(txt, pair_dict, leading_set, trailing_set):
            count = 0
            temp_txt = str(txt)

            if leading_set and trailing_set:
                symbol_set = leading_set + trailing_set
            elif leading_set:
                symbol_set = leading_set
            elif trailing_set:
                symbol_set = trailing_set
            else:
                return temp_txt, leading_set, trailing_set

            for sym_on in symbol_set:
                is_sym_off_there = (sym_on in pair_dict)
                if not is_sym_off_there:
                    break

                sym_off = pair_dict[sym_on]
                is_both_ends = (temp_txt.startswith(sym_on) and temp_txt.endswith(sym_off))
                if not is_both_ends:
                    continue

                temp = temp_txt[1:-1]
                is_balance = Common.isBalancedSymbol(sym_on, sym_off, temp)
                if is_balance:
                    temp_txt = temp
                    count += 1
            if count > 0:
                leading_set = leading_set[count:]
                trailing_set = trailing_set[:-count]
            return temp_txt, leading_set, trailing_set

        # txt = '   ({this}....,!'
        # # txt = '(also :kbd:`Shift-W` :menuselection:`--> (Locked, ...)`) This will prevent all editing of the bone in *Edit Mode*; see :ref:`bone locking <animation_armatures_bones_locking>`'
        # # txt = '(Top/Side/Front/Camera...)'
        txt = txt.strip()

        pair_list = [('{', '}'), ('[', ']'), ('(', ')'), ('<', '>'), ('$', '$'),(':', ':'), ('*', '*'), ('\'', '\''), ('"', '"'), ('`', '`'),]
        pair_dict = {}
        for p in pair_list:
            s, e = p
            entry_1 = {s:e}
            entry_2 = {e:s}
            pair_dict.update(entry_1)
            pair_dict.update(entry_2)

        leading_set = df.REMOVABLE_SYMB_FULLSET_FRONT.findall(txt)
        if leading_set:
            leading_set = leading_set[0]

        trailing_set = df.REMOVABLE_SYMB_FULLSET_BACK.findall(txt)
        if trailing_set:
            trailing_set = trailing_set[0]

        temp_txt = str(txt)
        temp_txt, leading_set, trailing_set = cleanBothEnds(temp_txt, pair_dict, leading_set, trailing_set)

        temp_txt, leading_set = cleanForward(temp_txt, pair_dict, leading_set)
        temp_txt, trailing_set = cleanBackward(temp_txt, pair_dict, trailing_set)

        temp_txt, _, _ = cleanBothEnds(temp_txt, pair_dict, leading_set, trailing_set)
        return temp_txt

    def isBalancedSymbol(symb_on, symb_off, txt):
        p_str = f'\{symb_on}([^\{symb_on}\{symb_off}]+)\{symb_off}'
        p_exp = r'%s' % (p_str.replace("\\\\", "\\"))
        pattern = re.compile(p_exp)
        p_list = Common.patternMatchAll(pattern, txt)
        has_p_list = (len(p_list) > 0)
        if has_p_list:
            temp_txt = str(txt)
            for loc, mm in p_list.items():
                s, e = loc
                left = temp_txt[:s]
                right = temp_txt[e:]
                temp_txt = left + right
            return not ((symb_on in temp_txt) or (symb_off in temp_txt))
        else:
            return True

    def hasAbbr(txt):
        abbr_str = RefType.ABBR.value
        has_abbr = (abbr_str in txt)
        return has_abbr

    def extractAbbr(abbr_txt):
        if not abbr_txt:
            return None, None, None

        abbr_dict = Common.patternMatchAll(df.ABBREV_PATTERN_PARSER, abbr_txt)
        if not abbr_dict:
            return None, None, None

        abbrev_orig_rec = abbrev_part = exp_part = None
        mm: MatcherRecord = None

        for s, mm in abbr_dict.items():
            abbrev_orig_rec = mm.getOriginAsTuple()
            l = mm.getSubEntriesAsList()
            for loc, txt in l:
                found_texts = df.ABBR_TEXT_ALL.findall(txt)
                first_entry = found_texts[0]
                abbrev_part, exp_part = first_entry

        return abbrev_orig_rec, abbrev_part, exp_part

    def testDict(dic_to_use):
        key_list = list(dic_to_use.keys())
        debug_text = 'trick'
        is_there = (debug_text.lower() in key_list)
        if not is_there:
            print(f'debug_text:{debug_text} IS NOT THERE')
        else:
            print(f'debug_text:[{debug_text}] exists:{is_there}')

    def findInSortedList(item, sorted_list):
        if not sorted_list:
            return None
        if not item:
            return None
        
        lower_item = item.lower()
        lo = 0
        hi = len(sorted_list)
        found_index = bisect_left(sorted_list, lower_item, lo, hi)        
        is_found = (found_index >= 0 and found_index < hi)
        if not is_found:            
            return None
        else:
            try:
                found_item = sorted_list[found_index]
                is_found = (found_item == lower_item)
                if is_found:
                    return found_item
                else:
                    return None
            except Exception as e:
                print(f'Finding message: [{item}], found index:[{found_index}]')
                raise e

    def getTextWithinBrackets(
            start_bracket: str,
            end_bracket: str,
            text:str,
            is_include_bracket:bool =False,
            replace_internal_start_bracket:str = None,
            replace_internal_end_bracket:str = None
    ) -> list:

        def pop_q(pop_s, pop_e) -> bool:
            last_s = q.pop()
            orig_txt = obs.blank[last_s:pop_e]
            orig_s = last_s
            orig_e = pop_e

            ss = (last_s if is_include_bracket else last_s + len(start_bracket))
            ee = (pop_e if is_include_bracket else pop_s)

            txt_line = text[ss:ee]
            if not txt_line:
                return False

            is_replace_internal_bracket = (replace_internal_start_bracket and (start_bracket in txt_line))
            if is_replace_internal_bracket:
                txt_line = txt_line.replace(start_bracket, replace_internal_start_bracket)

            loc = (orig_s, orig_e)
            entry = (loc, orig_txt)
            sentence_list.append(entry)
            obs.markLocAsUsed(loc)
            return True

        def getBracketList():
            # 1. find positions of start bracket
            if is_same_brakets:
                p_txt = r'\%s' % start_bracket
            else:
                p_txt = r'\%s|\%s' % (start_bracket, end_bracket)

            p = re.compile(p_txt)

            # split at the boundary of start and end brackets
            brk_list=[]
            m_list = p.finditer(text)
            for m in m_list:
                ss = m.start()
                ee = m.end()
                brk = m.group(0)
                entry=(ss, ee, brk)
                brk_list.append(entry)
            return brk_list

        def getSentenceList():
            bracket_list = getBracketList()
            if not bracket_list:
                return sentence_list

            # detecting where start/end and take the locations
            mm: MatcherRecord = None
            if is_same_brakets:
                for s, e, bracket in bracket_list:
                    is_bracket = (bracket == start_bracket)
                    if is_bracket:
                        if not q:
                            q.append(s)
                        else:
                            is_finished = pop_q(s, e)
                            if not is_finished:
                                continue
            else:
                for s, e, bracket in bracket_list:
                    is_open = (bracket == start_bracket)
                    is_close = (bracket == end_bracket)
                    if is_open:
                        q.append(s)
                    if is_close:
                        if not q:
                            continue
                        else:
                            is_finished = pop_q(s, e)
                            if not is_finished:
                                continue
            return sentence_list

        def removeBrackets(mm: MatcherRecord):
            bracket_pattern_txt = r'(\%s)?([^\%s\%s]+)(\%s)?' % (start_bracket, start_bracket, end_bracket, end_bracket)
            bracket_pattern = re.compile(bracket_pattern_txt)
            # print(f'main mm: {mm}')
            main_txt = mm.getMainText()
            sub_mm: MatcherRecord = None
            # Common.debugging(main_txt)
            try:
                found_dict = Common.patternMatchAll(bracket_pattern, main_txt)
                found_list = list(found_dict.items())
                if not found_list:
                    return False

                count = len(found_list)
                is_valid = (count < 2)
                if not is_valid:
                    raise ValueError(ER.TOO_MANY_SUB_ITEM)
                sub_loc, sub_mm = found_list[0]
                mm.addSubRecordFromAnother(sub_mm)
                # print(f'sub_mm list: {found_list}')
                return True
            except Exception as e:
                dd('removeBrackets():')
                dd(mm)
                dd(e)
                raise e

        def updateRecordsUsingSubLoc(dict_list, rootloc):
            for mmloc, mm in dict_list.items():
                is_same = (mmloc == rootloc)
                if is_same:
                    continue
                mm.type = RefType.TEXT
                # print(rootloc, mmloc, mm)
                rs, re  = rootloc
                ms, me = mmloc
                dist = me-ms
                new_ms = ms + rs
                new_me = new_ms + dist
                mm.updateMasterLoc(new_ms, new_me)


        sentence_list = []
        q = deque()
        s: int = -1
        e: int = -1
        last_s: int = -1
        is_same_brakets = (start_bracket == end_bracket)
        if is_same_brakets:
            print(f'getTextWithinBracket() - WARNING: start_bracket and end_braket is THE SAME {start_bracket}. '
                  f'ERRORS might occurs!')

        obs = LocationObserver(text)
        sentence_list = getSentenceList()
        result_dict = OrderedDict()

        for index, (sub_loc, sub_txt) in enumerate(sentence_list):
            part_dict = Common.findInvert(df.FILLER_PARTS,
                                          sub_txt, is_reversed=True)
            updateRecordsUsingSubLoc(part_dict, sub_loc)
            for loc, mm in part_dict.items():
                new_loc = (mm.s, mm.e)
                test_text = text[mm.s: mm.e]
                new_entry = {new_loc: mm}
                result_dict.update(new_entry)

        remove_list=[]
        for loc, mm in result_dict.items():
            is_ok = removeBrackets(mm)
            if not is_ok:
                remove_list.append(loc)

        for loc in remove_list:
            del result_dict[loc]

        return result_dict

    def removeSurroundingSpaces(self, txt_loc, txt):
        start_spc_mm: MatcherRecord = Common.patternMatch(df.START_SPACES, txt)
        end_spc_mm: MatcherRecord = Common.patternMatch(df.END_SPACES, txt)

        (ts, te) = txt_loc
        ns = ts
        ne = te
        ntxt = txt
        if start_spc_mm:
            (ss, se) = start_spc_mm.getMainLoc()
            diff = (se - ss)
            ns += diff
            ntxt = ntxt[diff:]
        if end_spc_mm:
            (es, ee) = end_spc_mm.getMainLoc()
            diff = (ee - es)
            ne -= diff
            ntxt = ntxt[:-diff]
        n_loc = (ns, ne)
        return (n_loc, ntxt)

    def removingNonAlpha(original_word: str):
        default_loc = (0, 0)
        is_empty_word = (original_word is None) or (len(original_word) == 0)
        if original_word is None:
            return (default_loc, original_word)

        max_len = len(original_word)
        s = max_len // 2
        e = s

        left_part = original_word[0:s]
        right_part = original_word[e:max_len]
        matcher = df.WORD_END_REMAIN.search(left_part)
        if matcher:
            grp = matcher.group(0)
            s -= len(grp)

        matcher = df.WORD_START_REMAIN.search(right_part)
        if matcher:
            grp = matcher.group(0)
            e += len(grp)

        loc = (s, e)
        new_word = original_word[s:e]
        return (loc, new_word)

    def insertTranslation(orig_word: str, new_word: str, current_trans: str) -> str:
        is_valid = (orig_word and new_word and current_trans)
        if not is_valid:
            return current_trans

        loc, actual_new_word = Common.locRemain(orig_word, new_word)
        ss, ee = loc
        left = orig_word[:ss]
        right = orig_word[ee:]
        new_tran = left + current_trans + right
        return new_tran

    def locRemain(original_word: str, new_word: str) -> list:
        '''
        locRemain:
            Find where the remainder starts, ends, excluding alphanumeric characters, so can decide
            if remainder can be removed or not and how far
        :param original_word: word where new_word is extracted from
        :param new_word: word from which dictionary has found from original word
        :return:
            list of locations (start, end) within the original where original word including
            but not containing any alpha-numerical characters, which can be removed (ie. remainder
            parts of the word in the original_word)
        '''
        # REWRITE THIS, MAKE IT SHORTER
        try:
            max_len = len(original_word)
            ss = original_word.find(new_word)
            ee = ss + len(new_word)

            found_test = original_word[ss:ee]
            ok = (found_test == new_word)
            if not ok:
                raise Exception(f'FAILED TO LOCATE [{new_word}] in [{original_word}]')

            left_part = original_word[0:ss]
            right_part = original_word[ee:max_len]

            matcher = df.WORD_END_REMAIN.search(left_part)
            if matcher:
                grp = matcher.group(0)
                ss -= len(grp)

            matcher = df.WORD_START_REMAIN.search(right_part)
            if matcher:
                grp = matcher.group(0)
                ee += len(grp)

            loc = (ss, ee)
            return loc, original_word[ss:ee]
        except Exception as e:
            raise e

        return (-1, -1), new_word

    def replaceStr(from_str: str, to_str: str, txt: str) -> str:
        '''
        Replace a sub-string (from_str) with another sub-string (to_str) in the
        string input (txt), with return count
        :param from_str:
            the sub-string to be replaced
        :param to_str:
            the sub-string acting as the replacement, to be replaced by.
        :param txt:
            the string to perform the replacement upon.
        :return:
            result_str, count

            the string with replacements performed upon,
            the count for number of replaced instances, how many times the replacement succeeded
        '''
        prev_txt = str(txt)
        rep_count: int = 0
        result_txt = str(txt)
        is_finished = False
        while not is_finished:
            result_txt = result_txt.replace(from_str, to_str, 1)
            has_changed = not (result_txt == prev_txt)
            if has_changed:
                rep_count += 1
                prev_txt = str(result_txt)
            else:
                is_finished = True
        return result_txt, rep_count

    def bracketParser(text):
        def error_msg(item, text_string):
            return f'Imbalanced parenthesis! Near the "{item}" text_string:[{text_string}]'

        _tokenizer = df.ARCH_BRACKET_SPLIT.split
        def tokenize(text_line: str):
            return list(filter(None, _tokenizer(text_line)))

        def _helper(tokens):
            outside_brackets = []
            bracketed = []
            q = []
            max = len(tokens)
            chosen_items = []
            start_loc = end_loc = 0
            for i in range(0, max):
                item = tokens[i]
                if item == '(':
                    q.append(i)
                elif item == ')':
                    if not q:
                        raise ValueError(error_msg(item, text))
                    q.pop()
                    bracketed.extend(chosen_items)
                    chosen_items = []
                else:
                    start_loc = text.find(item, end_loc)
                    end_loc = start_loc + len(item)
                    loc = (start_loc, end_loc)
                    entry = (loc, item)
                    if q:
                        chosen_items.append(entry)
                    else:
                        outside_brackets.append(entry)
            if q:
                raise ValueError(error_msg(item, text))
            return bracketed, outside_brackets
        tokens = tokenize(text)
        bracketed_list, outside_bracket_list = _helper(tokens)
        return bracketed_list, outside_bracket_list

    def wordInclusiveLevel(orig_txt:str, fuzzy_txt:str) -> int:
        '''
        Expected to see 0 to indicate every fuzzy word is included in
        original text
        :param orig_txt: original text
        :param fuzzy_txt: fuzzily found text
        :return:
            0 if all words in fuzzy text is included in the original text, fuzzily
            > 0 number of words NOT included in the original text
        '''
        def isFuzzilyInList(word_to_find, word_list):
            for word in word_list:
                ratio = fuzz.ratio(word, word_to_find)
                acceptable = (ratio >= df.FUZZY_ACCEPTABLE_RATIO)
                if acceptable:
                    return True
            return False

        fuzzy_list = fuzzy_txt.split()
        orig_list = orig_txt.split()
        list_len = len(fuzzy_list)
        fuzzy_word_count = 0
        for fuzzy_word in fuzzy_list:
            is_in_original = (fuzzy_word in orig_list) or isFuzzilyInList(fuzzy_word, orig_list)
            fuzzy_word_count += (1 if is_in_original else 0)

        inc_percentage = fuzzy_word_count / list_len * 100
        return inc_percentage

    def getLeadingMatchCount(k_item, item):
        def binary_match(loc_from, loc_to):
            f_len = len(loc_from)
            f_len_mid = (f_len // 2)
            f_list_0 = loc_from[:f_len_mid]

            t_len = len(loc_to)
            t_len_mid = (t_len // 2)
            t_list_0 = loc_to[:t_len_mid]

            is_same = (t_list_0.lower() == f_list_0.lower())
            if not is_same:
                return False

            f_list_1 = loc_from[f_len_mid+1:]
            t_list_1 = loc_to[t_len_mid+1:]
            is_same = (t_list_0.lower() == f_list_0.lower())
            if is_same:
                return True
            else:
                return binary_match(f_list_1, t_list_1)

        item_length = len(item)
        matched_total = 0
        for index, kw in enumerate(k_item):
            is_valid_index = (index < item_length)
            if not is_valid_index:
                break
            iw = item[index]
            is_matched = (iw == kw)
            if is_matched:
                matched_total += 1
            else:
                break
        return matched_total

    def findUntranslatedWords(orig_txt, fuzzy_txt):
        def insertEntryIntoRemainDict():
            orig_loc = orig_locs[index]
            entry = {orig_loc: orig_word}
            remain_dict.update(entry)

        # expecting to find fuzzy_txt within orig_txt, try to locate the range
        orig_txt_copy = str(orig_txt)
        orig_word_list = Common.findInvert(df.SPACES, orig_txt)
        fuzzy_word_list = Common.findInvert(df.SPACES, fuzzy_txt)

        fuzzy_locs = list(fuzzy_word_list.keys())
        fuzzy_words = list(fuzzy_word_list.values())

        orig_locs = list(orig_word_list.keys())
        orig_words = list(orig_word_list.values())

        remain_dict = OrderedDict()
        is_finished = False
        for index, orig_word in enumerate(orig_words):
            try:
                fuzzy_word = fuzzy_words[index]
                ratio = fuzz.ratio(orig_word, fuzzy_word)
                sounds_similar = (ratio >= df.FUZZY_ACCEPTABLE_RATIO)
                if sounds_similar:
                    continue

                insertEntryIntoRemainDict()
            except Exception as e:
                insertEntryIntoRemainDict()

        reversed_remain = list(remain_dict.items())
        reversed_remain.reverse()
        rev_remain = OrderedDict(reversed_remain)
        return rev_remain

    def splitExpVar(item, k):
        i_list = item.split(df.SENT_STRUCT_SYMB)

        i_left = i_list[0]
        i_right = i_list[1]
        i_left_len = len(i_left)
        i_right_len = len(i_right)

        i_left_list = i_right_list = []
        if i_left:
            i_left_list = i_left.split()

        if i_right:
            i_right_list = i_right.split()

        i_left_word_count = len(i_left_list)
        i_right_word_count = len(i_right_list)
        i_exp_word_count_total = (i_left_word_count + i_right_word_count)

        k_length = len(k)
        k_word_list = df.SPACES.split(k)
        k_word_count = len(k_word_list)

        is_less_than_expected = (k_word_count < i_exp_word_count_total)
        if is_less_than_expected:
            return i_left, i_right, None, None

        k_left = k_right = ""
        if i_left_word_count:
            k_left = ' '.join(k_word_list[:i_left_word_count])

        if i_right_word_count:
            k_right = ' '.join(k_word_list[i_right_word_count:])

        return i_left, i_right, k_left, k_right

    def getListOfVariations(txt):
        list_var = []
        for i in range(len(txt), 0, -1):
            entry = txt[0:i]
            list_var.append(entry)
        return list_var

    def getNoneAlphaPart(msg, is_start=True):
        if not msg:
            return ""

        non_alnum_part = ""
        if is_start:
            non_alpha = df.START_WORD_SYMBOLS.search(msg)
        else:
            non_alpha = df.END_WORD_SYMBOLS.search(msg)

        if non_alpha:
            non_alnum_part = non_alpha.group(0)
        return non_alnum_part

    def getRemainedWord(orig_txt: str, new_txt: str):
        def isInNewFuzzy(search_word):
            for loc, word in new_txt_word_list:
                match_rat = fuzz.ratio(word, search_word)
                is_same = (match_rat >= df.FUZZY_MODERATE_ACCEPTABLE_RATIO)
                if is_same:
                    return True
            return False

        blank_orig_txt = str(orig_txt)
        orig_word_dict = Common.patternMatchAll(df.CHARACTERS, orig_txt)
        orig_word_list = list(orig_word_dict.items())

        new_txt_word_dict = Common.patternMatchAll(df.CHARACTERS, new_txt)
        new_txt_word_list = list(orig_word_dict.items())

        remain_word_dict={}
        i = 0
        try:
            for i, entry in enumerate(orig_word_list):
                orig_loc, mm = entry
                (s, e), orig_word = mm.getOriginAsTuple()
                is_in_new = isInNewFuzzy(orig_word)
                if is_in_new:
                    continue

                entry = {orig_loc: orig_word}
                remain_word_dict.append(entry)

        except Exception as e:
            max = len(orig_word)
            if i < max:
                remain_sub_list = orig_word_list[i:]
                remain_sub_dict = OrderedDict(remain_sub_list)
                remain_word_dict.update(remain_sub_dict)

        return remain_word_dict

    def getTextWithinWithDiffLoc(msg, to_matcher_record=False):
        # should really taking bracket pairs into account () '' ** "" [] <> etc.. before capture
        left_part = Common.getNoneAlphaPart(msg, is_start=True)
        right_part = Common.getNoneAlphaPart(msg, is_start=False)
        ss = len(left_part)
        ee = (-len(right_part) if right_part else len(msg))
        mid_part = msg[ss:ee]
        length_ee = len(right_part)
        diff_loc = (ss, length_ee)

        main_record: MatcherRecord = None
        if to_matcher_record:
            ls=0
            le=ss
            ms=le
            me=ms + len(mid_part)
            rs=me
            re=rs + len(right_part)

            main_record=MatcherRecord(s=0, e=len(msg), txt=msg)
            if left_part:
                main_record.addSubMatch(ls, le, left_part)
                test_txt = left_part[ls: le]
            else:
                main_record.addSubMatch(-1, -1, None)
            if mid_part:
                main_record.addSubMatch(ms, me, mid_part)
                test_txt = left_part[ms: me]
            else:
                main_record.addSubMatch(ls, re, msg)
            if right_part:
                main_record.addSubMatch(rs, re, right_part)
                test_txt = left_part[rs: re]
            else:
                main_record.addSubMatch(-1, -1, None)

        return diff_loc, left_part, mid_part, right_part, main_record

    def getTextWithin(msg):
        diff_loc, left, mid, right,_ = Common.getTextWithinWithDiffLoc(msg)
        return left, mid, right

    def replaceWord(orig_word: str, new_word: str, replace_word: str) -> str:

        is_inclusive = (new_word in orig_word)
        if is_inclusive:
            ss = orig_word.find(new_word)
            ee = ss + len(new_word)
            left_part = orig_word[:ss]
            right_part = orig_word[ee:]
            matcher = df.WORD_END_REMAIN.search(left_part)
            if matcher:
                grp = matcher.group(0)
                ss -= len(grp)

            matcher = df.WORD_START_REMAIN.search(right_part)
            if matcher:
                grp = matcher.group(0)
                ee += len(grp)

            left_part = orig_word[:ss]
            right_part = orig_word[ee:]
            final_part = left_part + replace_word + right_part
            return final_part
        else:
            left_part = Common.getNoneAlphaPart(orig_word, is_start=True)
            right_part = Common.getNoneAlphaPart(orig_word, is_start=False)
            final_part = left_part + replace_word + right_part
        return final_part

    # def getSentenceList(input_text:str) -> list:
    #     t_list = {}
    #     doc = Common.nlp(input_text)
    #     sen = []
    #     last_e = 0
    #     for token in doc:
    #         is_punct = (token.pos_ == 'PUNCT')
    #         if not is_punct:
    #             txt = token.text
    #             sen.append(token.text)
    #             continue
    #
    #         if not sen:
    #             continue
    #
    #         sen_text = ' '.join(sen)
    #         ss = input_text.find(sen_text, last_e)
    #         is_error = (ss < 0)
    #         if is_error:
    #             raise ValueError(f'Common.getSentenceList(): Unable to find text [{sen_text}] in [{input_text}]')
    #
    #         ee = ss + len(sen_text)
    #         last_e = ee
    #         loc = (ss, ee)
    #         entry = {loc: sen_text}
    #         t_list.update(entry)
    #         sen = []
    #
    #     return t_list

    def matchTextPercent(t1: str, t2: str):
        match_percent = 0.0
        try:
            l1 = t1.split()
            l2 = t2.split()
            l1_count = len(l1)
            l1_per_each_word = (100 / l1_count)

            for i in range(0, l1_count):
                w1 = l1[i]
                w2 = l2[i]
                word_percent = Common.matchWordPercent(w1, w2)
                is_tool_small = (word_percent <= df.FUZZY_PERFECT_MATCH_PERCENT)
                if is_tool_small:
                    break
                match_percent += (l1_per_each_word * word_percent / 100)
        except Exception as e:
            pass
        return match_percent

    def matchWordPercent(t1:str, t2:str):
        match_percent = 0.0
        try:
            l1 = len(t1)
            l2 = len(t2)

            lx = max(l1, l2)
            lc = 100 / lx
            for i, c1 in enumerate(t1):
                c2 = t2[i]
                is_matched = (c1 == c2)
                if not is_matched:
                    # print(f'stopped at [{i}], c1:[{c1}], c2:[{c2}]')
                    break
                match_percent += lc
        except Exception as e:
            pass
        return match_percent

    def isFullyTranslated(txt):
        is_all_filler_and_spaces = (df.FILLER_CHAR_AND_SPACE_ONLY_PATTERN.search(txt) is not None)
        return is_all_filler_and_spaces

    def isTranslated(txt):
        is_overlapped = (df.FILLER_CHAR_PATTERN.search(txt) is not None)
        return is_overlapped

    def patchingBeforeReturn(left, right, patch_txt, orig_txt):

        is_in_valid = not (left or right)
        if is_in_valid:
            return patch_txt

        patch_txt_right = patch_txt_left = ''
        if left:
            patch_txt_left = patch_txt[:len(left)]
        if right:
            patch_txt_right = patch_txt[-len(right)]

        is_patching_left = (patch_txt_left != left)
        is_patching_right = (patch_txt_right != right)

        return_text = patch_txt
        if is_patching_left:
            return_text = left + patch_txt
        if is_patching_right:
            return_text = patch_txt + right

        return return_text

    def isBetweenRange(number, range_s, range_e):
        is_between = (range_s <= number <= range_e)
        return is_between

    def isOverlappedLoc(locf, loct):
        fs, fe = locf
        ts, te = loct
        is_ovrlap = Common.isOverlapped(fs, fe, ts, te)
        return is_ovrlap

    def isOverlapped(fs, fe, ts, te):
        is_fs_between = (ts <= fs <= te)
        is_fe_between = (ts <= fe <= te)
        is_ovrlap = (is_fs_between or is_fe_between)
        return is_ovrlap

    def stripSpaces(txt):
        start = 0
        end = 0
        leading_spaces: re.Match = df.START_SPACES.search(txt)
        if leading_spaces:
            start = leading_spaces.end()

        trailing_spaces: re.Match = df.END_SPACES.search(txt)
        if trailing_spaces:
            end = trailing_spaces.start()

        end_count = 0
        if end:
            end_count=(len(txt) - end)
        else:
            end = len(txt)
        return_txt = txt[start: end]
        return start, end_count, return_txt

    def subtractText(minuend_loc, minuend, subtrahend_loc, subtrahend):
        this_s, this_e = minuend_loc
        other_s, other_e = subtrahend_loc

        min_start = min(this_s, other_s)
        max_end = max(this_e, other_e)
        mask_orig = (' ' * max_end)

        start_part = (df.FILLER_CHAR * min_start)
        other_part = (df.FILLER_CHAR * (other_e - other_s))
        mask = start_part + mask_orig[min_start:]
        mask = mask[:other_s] + other_part + mask[other_e:]

        this_part = mask[this_s: this_e]
        # spaces to keep, FILLER_CHAR to remove
        this_txt = minuend
        list_of_remain = Common.patternMatchAll(df.SPACES, this_part)
        this_txt_dict = {}
        for loc, mm in list_of_remain:
            (s, e), txt_part = mm.getOriginAsTuple()
            is_not_worth_keeping = (df.SYMBOLS_ONLY.search(txt_part) is not None)
            if is_not_worth_keeping:
                continue

            start_count, end_count, new_txt_part = Common.stripSpaces(txt_part)
            new_loc = (s + start_count, e - end_count)
            entry = {new_loc: new_txt_part}
            this_txt_dict.update(entry)
        # this list could be empty, in which case remove left part, keep the right part (A - B = empty => keep B only)
        return this_txt_dict

    def jointText(orig: str, tran: str, loc: tuple):
        if not bool(tran):
            return orig

        s, e = loc
        left = orig[:s]
        right = orig[e:]
        orig = left + tran + right
        return orig

    def patStructToListOfWords(txt):
        mm: MatcherRecord = None
        struct_pat_dict = Common.patternMatchAll(df.SENT_STRUCT_PAT, txt)
        struct_pat_list = list(struct_pat_dict.items())

        struct_txt_dict = Common.findInvert(df.SENT_STRUCT_PAT, txt)
        struct_txt_dict_list = list(struct_txt_dict.items())

        list_of_words = []
        for loc, mm in struct_pat_list:
            entry = (mm.getMainLoc(), mm.getMainText())
            list_of_words.append(entry)

        for loc, mm in struct_txt_dict_list:
            entry = (mm.getMainLoc(), mm.getMainText())
            list_of_words.append(entry)

        list_of_words.sort()
        return list_of_words

    def formPattern(list_of_words: list):
        pat = ""
        # (?<=\S)\s+$
        for loc, txt in list_of_words:
            is_any = (df.SENT_STRUCT_SYMB in txt)
            txt = (f'\s?(.*\S)\s?' if is_any else f'({txt})')
            pat += txt

        pattern_txt = r'^%s$' % (pat)
        return_pat = re.compile(pattern_txt)
        return return_pat

    def creatSentRecogniserPatternRecordPair(key, value):
        recog_pattern = Common.creatSentRecogniserPattern(key)
        record_mm, record_txt_list = Common.createSentRecogniserRecord(value)
        return {recog_pattern: (key, value, record_mm, record_txt_list)}

    def creatSentRecogniserPattern(key):
        the_txt_word_list = Common.patStructToListOfWords(key)
        recog_pattern = Common.formPattern(the_txt_word_list)
        return recog_pattern

    def createSentRecogniserRecord(the_txt):
        the_txt_word_list = Common.patStructToListOfWords(the_txt)
        mm = MatcherRecord(txt=the_txt)
        mm.initUsingList(the_txt_word_list)
        return mm, the_txt_word_list

    def genmap(msg):
        def simplifiesMatchedRecords():
            mm: MatcherRecord = None
            for loc, mm in matched_list:
                txt = mm.txt
                entry = {loc: txt}
                loc_dic.update(entry)

        def genListOfDistance(max):
            dist_list = []
            for s in range(0, max):
                for e in range(0, max):
                    is_valid = (s < e)
                    if not is_valid:
                        continue

                    entry = (s, e)
                    if entry not in dist_list:
                        dist_list.append(entry)
            return dist_list

        part_list = []
        matched_dict = Common.patternMatchAll(df.SPACE_WORD_SEP, msg)
        matched_list = list(matched_dict.items())
        max = len(matched_dict)
        loc_dic = {}
        try:
            dist_list = genListOfDistance(max)
            dist_list.sort(reverse=True)
            for dist in dist_list:
                from_index, to_index = dist
                start_loc, start_mm = matched_list[from_index]
                end_loc, end_mm = matched_list[to_index]

                ss1, ee1 = start_loc
                ss2, ee2 = end_loc
                sentence = msg[ss1: ee2]

                sub_loc = (ss1, ee2)
                entry = {sub_loc: sentence}
                loc_dic.update(entry)
        except Exception as e:
            dd(f'genmap():{e}')
            raise e

        simplifiesMatchedRecords()
        part_list = list(loc_dic.items())
        # sort out by the number of spaces (indicating word counts) rather than by common string length
        part_list.sort(key=lambda x: (x[1].count(' '), len(x[1])), reverse=True)    # this is how to sort with multi keys, in brackets
        # part_list.sort(key=lambda x: (x[1].count(' ')), reverse=True)
        # dd('genmap():')
        # dd('-' * 80)
        # pp(part_list)
        # dd('-' * 80)
        # dd(f'for []{msg}')
        return part_list

    def debugging(txt):
        msg = "and without another"
        is_debug = (msg and txt and (msg.lower() in txt.lower()))
        # is_debug = (msg and txt and (msg.lower() == txt.lower()))
        # is_debug = (msg and txt and txt.startswith(msg))
        if is_debug:
            print(f'Debugging text: {msg} at line txt:{txt}')