import os
import operator as OP
from re import compile
from collections import OrderedDict
import hashlib
import time
from collections import deque
from fuzzywuzzy import fuzz
from bisect import bisect_left
from matcher import MatcherRecord
from err import ErrorMessages as ER
import re
from observer import LocationObserver
import json
import concurrent.futures

from definition import Definitions as df, \
    SentStructMode as SMODE, \
    SentStructModeRecord as SMODEREC, \
    RefType
from pprint import pprint as pp
import inspect as INP

DEBUG=True
# DEBUG=False
DIC_LOWER_CASE=True

def dd(*args, **kwargs):
    if DEBUG:
        print(args, kwargs)
        if len(args) == 0:
            print('-' * 80)

class Common:
    def writeJSONDic(dict_list=None, file_name=None):
        try:
            if not file_name:
                return

            if not dict_list:
                return

            with open(file_name, 'w+', newline='\n', encoding='utf8') as out_file:
                json.dump(dict_list, out_file, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            df.LOG(f'{e}; Length of read dictionary:{len(dict_list)}', error=True)
            raise e

    def loadJSONDic(file_name=None):
        return_dic = {}
        try:
            if not file_name:
                dd(f'loadJSONDic - file_name is None.')
                return return_dic

            if not os.path.isfile(file_name):
                dd(f'loadJSONDic - file_name:{file_name} cannot be found!')
                return return_dic

            dic = {}
            with open(file_name) as in_file:
                # dic = json.load(in_file, object_pairs_hook=NoCaseDict)
                return_dic = json.load(in_file)
        except Exception as e:
            df.LOG(f'{e}; Exception occurs while performing loadJSONDic({file_name})', error=True)

        return return_dic

    def isPath(txt: str) -> bool:
        if not txt:
            return False

        is_path = (df.PATH_CHECKER.search(txt) is not None)
        if is_path:
            return True

        urls = df.urlx_engine.find_urls(txt, get_indices=True)
        if not urls:
            return False

        # 1. Find the list of urls and put into dictionary so locations can be extracted, uing keys
        obs = LocationObserver(txt)
        for url, loc in urls:
            obs.markLocAsUsed(loc)

        # 2. find all the text outside the links and see if they are just spaces and symbols only, which can be classified as
        # IGNORABLE
        text_outside_url_list = obs.getUnmarkedPartsAsDict()

        # 3. Find out if text outside are but all symbols (non-alpha), which means they are discardable (non-translatable)
        is_ignorable = True
        for loc, text_outside_mm in text_outside_url_list.items():
            text_outside = text_outside_mm.txt
            is_all_symbols = df.SYMBOLS_ONLY.search(text_outside)
            if not is_all_symbols:
                is_ignorable = False

        return is_ignorable

    def isLinkPath(txt: str) -> bool:
        invalid_combination = ('.,' in txt) or (' ' in txt)
        if invalid_combination:
            return False

        is_blank_quote = df.BLANK_QUOTE_ABS.search(txt)
        if is_blank_quote:
            return False

        is_path = Common.isPath(txt)
        if is_path:
            return True

        is_url = df.urlx_engine.has_urls(txt)
        if is_url:
            return False

        left, mid, right = Common.getTextWithin(txt)
        is_path = Common.isPath(mid)
        if is_path:
            return True
        else:
            return False

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
        source_word_count = (len(from_str.split()))
        target_word_count = (len(to_str.split()))

        is_first_upper = (first_char.isupper() and remain_part.islower())
        if is_first_upper:
            first_char = new_str[0].upper()
            both_have_multi_words = (source_word_count > 1) and (target_word_count > 1)
            both_only_have_one_word = (source_word_count == 1) and (target_word_count == 1)
            is_first_only = (both_only_have_one_word or both_have_multi_words)
            if is_first_only:
                remain_part = new_str[1:].lower()
                new_str = first_char + remain_part
            else:
                new_str = new_str.title()
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
                        is_source_single_word = (source_word_count == 1)
                        is_target_single_word = (target_word_count == 1)
                        # is_both_single = (is_target_single_word and is_target_single_word)
                        is_title_target = (is_source_single_word and not is_target_single_word)

                        if is_title_target:
                            new_str = new_str.title()
                        else:
                            new_str = new_str.upper()

        # ensure ref keywords ':doc:' is always lowercase
        ga_ref_dic = Common.patternMatchAll(df.GA_REF_PART, new_str)
        new_str = lowercase(ga_ref_dic, new_str)
        for lcase_word in WORD_SHOULD_BE_LOWER:
            p = re.compile(r'\b%s\b' % lcase_word)
            p_list_dic = Common.patternMatchAll(p, new_str)
            new_str = lowercase(p_list_dic, new_str)

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

    # def correctTextListWithoutSpaces(loc_txt_list):
    #     try:
    #         temp_dict = OrderedDict(loc_txt_list)
    #         loc_list = temp_dict.values()
    #         list_length = len(temp_dict)
    #
    #         last_loc = loc_list[list_length-1]
    #         (ls, le) = last_loc
    #
    #         q_list=[]
    #         problem_list=[]
    #         blank_str = (' ' * list_length)
    #         for index, (loc, txt) in enumerate(list(temp_dict.items())):
    #             has_end_space = has_start_space = False
    #
    #             left, mid, right = Common.getTextWithin(txt)
    #
    #             (ls, le) = loc
    #             is_first = (index == 0)
    #             is_last = (index >= list_length-1)
    #             is_mid = (not (is_first and is_last))
    #
    #             check_end = (is_first or is_mid)
    #             check_begin = (is_last or is_mid)
    #
    #             if check_end:
    #                 has_end_space = (right and (df.SYMBOLS_ONLY.search(right) is not None))
    #
    #             if check_begin:
    #                 has_start_space = (left and (df.SYMBOLS_ONLY.search(left) is not None))
    #
    #             if is_first:
    #                 q_list.append((index, txt))
    #                 q_list.append((index, has_end_space))
    #                 if not has_end_space:
    #                     problem_list.append(index)
    #             elif is_mid:
    #                 q_list.append((index, has_start_space))
    #                 if not has_start_space:
    #
    #                 q_list.append((index, txt))
    #                 q_list.append((index, has_end_space))
    #             elif is_last:
    #                 q_list.append((index, has_start_space))
    #                 q_list.append((index, txt))
    #
    #         for (index, item) in q_list:
    #
    #
    #         new_list=[]
    #         status_list=[]
    #         txt: str = None
    #         for loc, txt in loc_txt_list:
    #             has_start_space = (df.START_SPACES.search(txt) is not None)
    #             has_end_space = (df.END_SPACES.search(txt) is not None)
    #             status_entry = (loc, (has_start_space, has_end_space, txt))
    #
    #     except Exception as e:
    #         return loc_txt_list

    def jointTextsWithSingleSpaceInBetween(text_list):
        try:
            first_try = ' '.join(text_list)
            final_string = re.sub(r'\s{2}', ' ', first_try)
            return final_string
        except Exception as e:
            return text_list

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
            pass
            # df.LOG(e)
        return return_dict


    def findInvert(pattern, text:str, is_reversed=False, is_removing_symbols=True):
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

                if is_removing_symbols:
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
            df.LOG(f'{e}; k:[{k}] v:[{v}]', error=True)
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
                    pass

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
        # msg = ":abbr:`kiến tạo/sửa đổi (create/modify)`"
        ga_dict = Common.patternMatchAll(df.GA_REF, txt)
        if not ga_dict:
            return False

        mm: MatcherRecord = None
        mm = list(ga_dict.values())[0]
        type_txt = mm.getType()
        ref_type = RefType.getRef(type_txt)
        is_abbrev = (ref_type == RefType.ABBR)

        return is_abbrev

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
                df.LOG(f'[{e}]; Finding message: [{item}], found index:[{found_index}]', error=True)
                raise e

    def removeStartEndBrackets(input_txt, start_bracket=None, end_bracket=None):
        try:
            str_len = len(input_txt)
            start_loc = 0
            end_loc = str_len

            s_brk = (start_bracket if start_bracket else '(')
            e_brk = (end_bracket if end_bracket else ')')

            bracket_pattern_txt = r'([\%s\%s])' % (s_brk, e_brk)
            bracket_pattern = re.compile(bracket_pattern_txt)
            found_dict = Common.patternMatchAll(bracket_pattern, input_txt)
            found_list = list(found_dict.items())
            if not found_list:
                orig_loc = (start_loc, end_loc)
                orig_entry = (orig_loc, input_txt)
                return orig_entry

            q = deque()
            for loc, mm in found_dict.items():
                brk = mm.txt
                is_open = (brk == s_brk)
                is_close = (brk == e_brk)
                current_entry = (loc, brk)
                if is_open:
                    q.append(current_entry)
                if is_close:
                    if not q:
                        continue

                    q_entry = q.pop()
                    (cs, ce), cbrk = current_entry
                    (qs, qe), qbrk = q_entry
                    is_start_string_bracket = (qs == 0)
                    is_end_string_bracket = (ce == str_len)
                    is_remove_start_and_end = (is_start_string_bracket and is_end_string_bracket)
                    if is_remove_start_and_end:
                        start_loc = qs + len(start_bracket)
                        end_loc = ce - len(end_bracket)
                        break
            new_txt = input_txt[start_loc: end_loc]
            new_loc = (start_loc, end_loc)
            return (new_loc, new_txt)

        except Exception as e:
            df.LOG(f'{e} [{input_txt}]', error=True)
            raise e

    def getTextWithinBrackets(
            start_bracket: str,
            end_bracket: str,
            input_txt:str,
            is_include_bracket:bool =False,
            replace_internal_start_bracket:str = None,
            replace_internal_end_bracket:str = None
    ) -> list:

        def pop_q(pop_s, pop_e) -> bool:
            last_s = q.pop()
            ss = last_s
            ee = pop_e

            # for 'function()', do not store as a bracketed text
            txt_line = input_txt[ss:ee]
            if not txt_line:
                return False

            loc = (ss, ee)
            entry = (loc, txt_line)
            sentence_list.append(entry)
            return True

        def getBracketList():
            # split at the boundary of start and end brackets
            try:
                # 1. find positions of start bracket
                if is_same_brakets:
                    p_txt = r'\%s' % start_bracket
                else:
                    p_txt = r'[\%s\%s]' % (start_bracket, end_bracket)

                p = re.compile(p_txt)
                brk_list = Common.patternMatchAll(p, input_txt)
                return brk_list, p
            except Exception as e:
                df.LOG(f'{e} [{input_txt}]', error=True)
                raise e
            return brk_list

        def getSentenceList():
            bracket_list, pattern = getBracketList()
            if not bracket_list:
                return sentence_list, pattern

            # detecting where start/end and take the locations
            mm: MatcherRecord = None
            if is_same_brakets:
                for loc, mm in bracket_list.items():
                    s, e = loc
                    bracket = mm.txt
                    is_bracket = (bracket == start_bracket)
                    if is_bracket:
                        if not q:
                            q.append(s)
                        else:
                            pop_q(s, e)
            else:
                for loc, mm in bracket_list.items():
                    s, e = loc
                    bracket = mm.txt
                    is_open = (bracket == start_bracket)
                    is_close = (bracket == end_bracket)
                    if is_open:
                        q.append(s)
                    if is_close:
                        if not q:
                            continue
                        else:
                            pop_q(s, e)
            return sentence_list, pattern

        def sortSentencesFunction(item):
            (loc, txt) = item
            sort_key = (len(txt), loc)
            return sort_key

        output_dict = OrderedDict()
        sentence_list = []
        q = deque()
        txt_len = len(input_txt)
        is_same_brakets = (start_bracket == end_bracket)
        if is_same_brakets:
            dd(f'getTextWithinBracket() - WARNING: start_bracket and end_braket is THE SAME {start_bracket}. '
                  f'ERRORS might occurs!')

        sentence_list, pattern = getSentenceList()
        if not sentence_list:
            return output_dict

        loc_list=[]
        obs = LocationObserver(input_txt)
        sentence_list.sort(key=sortSentencesFunction, reverse=True)
        for loc, txt in sentence_list:
            is_finished = obs.isCompletelyUsed()
            if is_finished:
                break

            is_used = obs.isLocUsed(loc)
            if is_used:
                continue

            if not is_include_bracket:
                (sub_loc, actual_txt) = Common.removeStartEndBrackets(txt, start_bracket=start_bracket, end_bracket=end_bracket)
                (cs, ce) = loc
                (ss, se) = sub_loc
                actual_loc = (cs + ss, cs + se)
            else:
                actual_loc = loc
                actual_txt = txt

            obs.markLocAsUsed(loc)
            (ss, ee) = actual_loc
            mm = MatcherRecord(s=ss, e=ee, txt=actual_txt)
            mm.pattern = pattern
            mm.type = RefType.ARCH_BRACKET
            dict_entry = {actual_loc: mm}
            output_dict.update(dict_entry)

        return output_dict

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

    def isStrEQ(str1: str, str2: str):
        return (str1.lower() == str2.lower())

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
            temp_from = original_word.lower()
            temp_to = new_word.lower()

            max_len = len(temp_from)
            ss = temp_from.find(new_word)
            ee = ss + len(new_word)

            found_test = temp_from[ss:ee]
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
            df.LOG(f'{e}', error=True)
            raise e

        return (-1, -1), new_word

    def checkWordEndedBoundaries(txt: str, word_to_check: str, location: tuple):
        map = Common.genmap(txt, is_removing_symbols=True)
        selective_list = []
        for map_loc, map_word in map:
            is_selected = (word_to_check in map_word)
            if not is_selected:
                continue

            rat = fuzz.ratio(map_word, word_to_check)
            entry = (rat, map_loc, map_word)
            selective_list.append(entry)
        selective_list.sort(reverse=True)

        return None

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
        fuzzy_word_list = Common.findInvert(df.SPACES, fuzzy_txt, is_removing_symbols=False)

        # fuzzy_locs = list(fuzzy_word_list.keys())
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
            except Exception as e:
                pass
            insertEntryIntoRemainDict()

        reversed_remain = list(remain_dict.items())
        reversed_remain.reverse()
        rev_remain = OrderedDict(reversed_remain)
        return rev_remain

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
        def findMatchingWordInNewTxt(search_word):
            for new_loc, new_txt_segment in new_txt_map:
                match_rat = fuzz.ratio(new_txt_segment, search_word)
                is_same = (match_rat >= df.FUZZY_MODERATE_ACCEPTABLE_RATIO)
                if is_same:
                    return True
            return False

        new_txt_map = Common.genmap(new_txt)
        obs = LocationObserver(orig_txt)
        map = Common.genmap(orig_txt)
        for loc, orig_txt_segment in map:
            is_fully_translated = obs.isCompletelyUsed()
            if is_fully_translated:
                break

            is_used = obs.isLocUsed(loc)
            if is_used:
                continue

            is_in_selection = findMatchingWordInNewTxt(orig_txt_segment)
            if is_in_selection:
                obs.markLocAsUsed(loc)

        remain_word_dict = obs.getUnmarkedPartsAsDict()
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

    def getTextWinthinSpaces(msg):
        start_spaces_match = df.START_SPACES.search(msg)
        end_spaces_match = df.END_SPACES.search(msg)
        left = ("" if not start_spaces_match else start_spaces_match.group(0))
        right = ("" if not end_spaces_match else end_spaces_match.group(0))
        length_left = len(left)
        length_right = len(right)
        length_right = (len(msg) if not length_right else -length_right)
        mid = msg[length_left:length_right]

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
                    # dd(f'stopped at [{i}], c1:[{c1}], c2:[{c2}]')
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

    def removeTheWord(trans):
        try:
            trans = df.THE_WORD.sub("", trans)
            trans = df.POSSESSIVE_APOS.sub("", trans)
        except Exception as e:
            pass
        return trans

    def jointText(orig: str, tran: str, loc: tuple):
        backup = [str(orig), str(tran)]
        if not bool(tran):
            return orig

        new_str = str(orig)
        s, e = loc
        left = new_str[:s]
        right = new_str[e:]
        new_str = left + tran + right
        return new_str

    def splitWordAt(pattern: str, txt: str):
        is_char = isinstance(pattern, str)
        is_pat = isinstance(pattern, re.Pattern)
        try:
            pat = (re.compile(pattern) if is_char else pattern)
            txt_dict = Common.findInvert(pat, txt)
            return txt_dict, (len(txt_dict) > 1)
        except Exception as e:
            df.LOG(f'{e}', error=True)
        return ({}, False)

    def splitWordAtToList(pattern: str, txt: str):
        is_char = isinstance(pattern, str)
        is_pat = isinstance(pattern, re.Pattern)
        word_list=[]
        try:
            pat = (re.compile(pattern, flags=re.I) if is_char else pattern)
            txt_dict = Common.findInvert(pat, txt)
            for loc, word_mm in txt_dict.items():
                entry=(loc, word_mm.txt)
                word_list.append(entry)
            return word_list
        except Exception as e:
            df.LOG(f'{e}', error=True)
        return word_list

    def wordCount(txt):
        try:
            l = txt.split()
            return len(l)
        except Exception as e:
            return 0

    def patStructToListOfWords(txt, removing_symbols=True):
        mm: MatcherRecord = None
        obs = LocationObserver(txt)
        struct_pat_dict = Common.patternMatchAll(df.SENT_STRUCT_PAT, txt)
        struct_pat_list = list(struct_pat_dict.items())

        struct_txt_dict = Common.findInvert(df.SENT_STRUCT_PAT, txt, is_removing_symbols=removing_symbols)
        struct_txt_dict_list = list(struct_txt_dict.items())

        list_of_words = []
        for loc, mm in struct_pat_list:
            entry = (mm.getMainLoc(), mm.getMainText())
            obs.markLocAsUsed(loc)
            list_of_words.append(entry)

        for loc, mm in struct_txt_dict_list:
            entry = (mm.getMainLoc(), mm.getMainText())
            list_of_words.append(entry)

        list_of_words.sort()
        return list_of_words

    def formPattern(list_of_words: list):
        final_pat = ""
        # (?<=\S)\s+$
        txt: str = None
        pattern_list=[]
        word = r'[\w_\-]+'
        word_space = r'[\w\-_\s]+'
        word_any = r'.*[\w\W]+.*(?<!\s)'
        # ending = r'(\s|$)?'
        embpart_terminator = r'(\s|\b|$)?'
        # embpart_terminator = ''
        ending = r'(\W\b|$)?'
        leading = r'(\W\b|^)?'
        for loc, txt in list_of_words:
            emb_pat = None
            is_any = (df.SENT_STRUCT_PAT.search(txt) is not None)
            if is_any:
                pat_txt = r'(%s)' % (word_any)

                is_excluded = df.EXCLUDE.search(txt)
                not_leading = df.NOT_LEADING.search(txt)
                not_trailing = df.NOT_TRAILING.search(txt)
                is_equal = df.EQUAL.search(txt)
                is_embedded_with = df.EMBEDDED_WITH.search(txt)
                is_ending_with = df.TRAILING_WITH.search(txt)
                is_leading_with = df.LEADING_WITH.search(txt)
                is_claused = bool(is_leading_with or is_ending_with or is_embedded_with or is_equal or is_excluded or not_leading or not_trailing)
                is_accepting_not_equal = (is_excluded and not (is_equal or is_ending_with or is_leading_with or is_embedded_with))
                if is_claused:
                    embs = df.CLAUSED_PART.search(txt)
                    emb_part = embs.group(1)
                    if is_ending_with:
                        pat_txt = r'%s(%s%s)%s' % (leading, word, emb_part, ending)
                    elif is_leading_with:
                        pat_txt = r'%s((%s)%s)%s' % (leading, emb_part, word, ending)
                    elif is_embedded_with:
                        pat_txt = r'%s(%s(%s)%s)%s' % (leading, word, emb_part, word, ending)
                    elif is_equal:
                        pat_txt = r'%s(%s)%s' % (leading, emb_part, ending)
                    elif not_leading:
                        pat_txt = r'%s(?!(%s)\w+)%s' % (leading, emb_part, ending)
                    elif not_trailing:
                        pat_txt = r'%s(\w+(?<!(%s)))%s' % (leading, emb_part, ending)
                    elif is_accepting_not_equal:
                        pat_txt = r'%s(?!(%s)\w+)%s' % (leading, emb_part, ending)
                    # dd('')
                pattern_embedded = df.PATTERN_PART.search(txt)
                if pattern_embedded:
                    emb_pat_txt = pattern_embedded.group(1)
                    pat_txt = r'(%s)' % (emb_pat_txt)
            else:
                pat_txt = r'(%s)' % (txt)
            pattern_list.append(pat_txt)

        final_pat = "".join(pattern_list)
        simplified_pat = final_pat.replace('\\s?\\s?', '\\s?')
        simplified_pat = simplified_pat.replace('\\s?( )\\s?', '\\s?')

        # test_pat = "".join(simplified_pat)
        # test_txt= "**not** the orientation",
        #
        # match_1 = re.search(test_pat, test_txt, flags=re.I)
        # match_2 = re.compile(test_pat, flags=re.I)
        # grp = match_2.findall(test_pat)
        # #
        # match = Common.patternMatchAll(re.compile(test_pat, flags=re.I), test_txt)
        #
        # is_match = bool(match or match_1 or grp)
        # if is_match:
        #     pass

        pattern_txt = r'^%s$' % (simplified_pat)
        # df.LOG(pattern_txt, error=False)
        return pattern_txt

    def creatSentRecogniserPatternRecordPair(key, value):
        recog_pattern = Common.creatSentRecogniserPattern(key)
        record_mm, record_txt_list = Common.createSentRecogniserRecord(value)
        return {recog_pattern: (key, record_mm, record_txt_list)}

    def creatSentRecogniserPattern(key):
        the_txt_word_list = Common.patStructToListOfWords(key, removing_symbols=False)
        recog_pattern = Common.formPattern(the_txt_word_list)
        return recog_pattern

    def getStructureModeFromTheMatcher(element_txt):
        mm_rec: MatcherRecord = None
        smode_list=[]
        try:
            mode_flag_components = [x for x in element_txt.split('/') if x]
            for mode_txt in mode_flag_components:
                extra_param = 0
                mode = SMODE.getName(mode_txt)

                is_any = (mode == SMODE.ANY)
                is_order = (mode == SMODE.ORDERED_GROUP)
                is_pattern = (mode == SMODE.PATTERN)
                is_trailing_with = (mode == SMODE.TRAILING_WITH)
                is_leading_with = (mode == SMODE.LEADING_WITH)
                is_embedded_with = (mode == SMODE.EMBEDDED_WITH)
                is_claused = (is_leading_with or is_embedded_with or is_trailing_with)
                is_max_up_to = (mode == SMODE.MAX_UPTO)

                if is_max_up_to:
                    max_up_to_match = df.MAX_VAR_PAT.search(mode_txt)
                    max_up_value = max_up_to_match.group(2)
                    extra_param = int(max_up_value)
                elif is_order:
                    extra_param = int(mode_txt)
                elif is_pattern:
                    mode_txt_match = df.PATTERN_PART.search(mode_txt)
                    mode_txt = mode_txt_match.group(1)
                elif is_claused:
                    ending_match = df.CLAUSED_PART.search(mode_txt)
                    mode_txt = ending_match.group(1)

                mode_entry = SMODEREC(smode_txt=mode_txt, smode=mode, extra_param=extra_param)
                smode_list.append(mode_entry)
        except Exception as e:
            pass
        return smode_list

    def createSentRecogniserRecord(the_txt):
        mode_list = [SMODE.ANY]
        the_txt_word_list = Common.patStructToListOfWords(the_txt)
        the_smode_dict = OrderedDict()
        for txt_loc, txt in the_txt_word_list:
            match = df.SENT_STRUCT_PAT.search(txt)
            if match:
                matched_group = [x for x in match.groups() if x]
                item_count = len(matched_group)
                item_index = max(0, item_count-1)
                pat_txt = matched_group[item_index]
                mode_and_param_list = Common.getStructureModeFromTheMatcher(pat_txt)
            else:
                mode_and_param_list = None
            entry= {txt_loc: (txt, mode_and_param_list)}
            the_smode_dict.update(entry)
        mm = MatcherRecord(txt=the_txt)
        mm.smode = the_smode_dict
        mm.initUsingList(the_txt_word_list, original_text=the_txt)
        return mm, the_txt_word_list

    def isRef(txt) -> bool:
        for pat in df.pattern_list_absolute:
            matcher = pat.search(txt)
            is_found = (matcher is not None)
            if is_found:
                return True
        return False

    def getRefDictList(txt) -> dict:
        obs = LocationObserver(txt)
        local_found_dict_list = {}
        for pat, ref_type in df.pattern_list:
            local_found_dict = None
            is_bracket = (ref_type == RefType.ARCH_BRACKET)
            if is_bracket:
                local_found_dict = Common.getTextWithinBrackets('(', ')', txt, is_include_bracket=False)
            else:
                local_found_dict = Common.patternMatchAll(pat, txt)

            if local_found_dict:
                local_found_dict_list.update(local_found_dict)
                loc_list = local_found_dict.keys()
                for loc in loc_list:
                    obs.markLocAsUsed(loc)
        return_dict = OrderedDict(sorted(local_found_dict_list.items(), reverse=True))
        return (return_dict, obs)

    def genmap(msg, is_reverse=True, is_removing_symbols=False, using_pattern=None):
        def simplifiesMatchedRecords():
            mm: MatcherRecord = None
            for loc, mm in matched_list:
                can_location_be_used = obs.isUsableLoc(loc)
                if not can_location_be_used:
                    continue

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

                    distance = (e - s)
                    entry = (distance, s, e)
                    if entry not in dist_list:
                        dist_list.append(entry)
            return dist_list

        def sortGetWordLen(item):
            (loc, txt) = item
            wc = len(txt.split())
            txt_len = len(txt)
            return (txt_len, wc)

        part_list = []
        obs: LocationObserver = None
        ref_dict_list, obs = Common.getRefDictList(msg)
        occupied_list = ref_dict_list.keys()

        sep_pattern = (df.SPACE_WORD_SEP if not is_removing_symbols else df.SYMBOLS)
        actual_pattern = (using_pattern if using_pattern else sep_pattern)
        matched_dict = Common.patternMatchAll(actual_pattern, msg)
        matched_list = list(matched_dict.items())
        max = len(matched_dict)
        loc_dic = {}
        try:
            dist_list = genListOfDistance(max)
            dist_list.sort(reverse=is_reverse)
            for entry in dist_list:
                distance, from_index, to_index = entry
                start_loc, start_mm = matched_list[from_index]
                end_loc, end_mm = matched_list[to_index]

                ss1, ee1 = start_loc
                ss2, ee2 = end_loc

                sentence = msg[ss1: ee2]
                word_count = (ee2 - ss1)

                sub_loc = (ss1, ee2)
                can_location_be_used = obs.isUsableLoc(sub_loc)
                if not can_location_be_used:
                    continue

                entry = {sub_loc: sentence}
                loc_dic.update(entry)
        except Exception as e:
            df.LOG(e, error=True)
            raise e

        simplifiesMatchedRecords()

        part_list = list(loc_dic.items())
        part_list.sort(key=sortGetWordLen, reverse=True)
        return part_list

    def dictKeyFunction(item):
        is_pattern = (isinstance(item, re.Pattern))
        is_string = (isinstance(item, str))
        is_matcher = (isinstance(item, re.Match))
        if is_pattern:
            key = item.pattern
        if is_matcher:
            key = item.re.pattern
        if is_string:
            key = item
        return key

    def binarySearch(sorted_list, find_txt, key=None):
        def basicKeyFunction(found_item):
            try:
                return found_item
            except Exception as e:
                return ""

        extract_function = (key if key else basicKeyFunction)
        lo = 0
        hi = len(sorted_list) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            mid_item = sorted_list[mid]
            list_item = extract_function(mid_item)
            finding_item = extract_function(find_txt)
            is_equal = (list_item == finding_item)
            if is_equal:
                return mid
            elif list_item < finding_item:
                lo = mid + 1
            else:
                hi = mid
        return -1

    def getListOfDuplicatedLoc(list_of_loc_txt: list):
        try:
            list_length = len(list_of_loc_txt)
            last_item = list_of_loc_txt[list_length-1]
            (last_loc, last_txt) = last_item

            (last_s, last_e) = last_loc
            blank_string = (' ' * last_e)
            obs = LocationObserver(blank_string)

            list_of_indexes_to_be_removed = []

            temp_dict = OrderedDict(list_of_loc_txt)
            list_of_loc = temp_dict.keys()
            for index, temp_loc in enumerate(list_of_loc):
                if obs.isLocUsed(temp_loc):
                    list_of_indexes_to_be_removed.append(index)
                obs.markLocAsUsed(temp_loc)
        except Exception as e:
            pass
        return list_of_indexes_to_be_removed

    def removeDuplicationFromlistLocText(list_of_loc_txt: list, list_of_removing_index=None):
        try:
            list_of_indexes_to_be_removed = list_of_removing_index
            if not list_of_removing_index:
                list_of_indexes_to_be_removed = Common.getListOfDuplicatedLoc()

            list_of_indexes_to_be_removed.sort(reverse=True)
            for index in list_of_indexes_to_be_removed:
                list_of_loc_txt.pop(index)
        except Exception as e:
            pass

        return list_of_loc_txt

    def createMatcherRecord(mm: re.Match):
        return MatcherRecord(matcher_record=mm)

    def simplifiedSS(ss_dict):
        def getOrEntries(txt):
            mm: MatcherRecord = None
            any_part = r'([^()`]+)?'
            bracketted_part = r'(\(([^\(\)]+)\))|\`([^\`]+)\`'
            pat_txt = r'%s(%s)%s' % (any_part, bracketted_part, any_part)
            pat = re.compile(pat_txt)
            part_match_dict = Common.patternMatchAll(pat, txt)
            found_parts = []
            for loc, mm in part_match_dict.items():
                txt_loc = mm.getSubLoc()
                txt = mm.getSubText()
                if not txt:
                    txt = mm.getType()
                    txt_loc = mm.getTypeLoc()

                or_list = txt.split('|')
                is_or_list = (len(or_list) > 1)
                if not is_or_list:
                    continue

                entry = (txt_loc, or_list)
                found_parts.append(entry)
            return found_parts

        def composeSubEntries(orig_txt_list, loc, or_list):
            new_line_list = []
            for orig_txt in orig_txt_list:
                for or_clause in or_list:
                    new_line = Common.jointText(orig_txt, or_clause, loc)
                    new_line_list.append(new_line)
            return new_line_list

        def cleanLine(old_line):
            clean_new_k_pat_txt = r'[()`\[\]\^\\]'
            clean_spaces_pat_txt = r'[\s]+'
            clean_spaces_pat = re.compile(clean_spaces_pat_txt)
            clean_new_k_pat = re.compile(clean_new_k_pat_txt)

            # has_spaces = ('\\s' in old_line)
            # if has_spaces:
            #     dd('debug')
            new_line = old_line.replace('\\s', ' ')

            new_line = clean_new_k_pat.sub('', new_line)
            new_line = clean_spaces_pat.sub(' ', new_line)
            new_line = new_line.strip()
            return new_line

        rep_keywords = r'(\/?(\d|ED|LD|EX|EQ|NP|NC|MX\d+|\\w|\+|\?|\\d|\\W))'
        re_pat_txt = r'(\$\{)|%s?|(\})' % (rep_keywords)
        pat = re.compile(re_pat_txt)

        # home_dir = os.environ['BLENDER_GITHUB']
        # sent_struct_file = os.path.join(home_dir, "ref_dict_ss_0001.json")
        # ss_dict = self.loadData(sent_struct_file, is_lower=False)

        simplified_dict = OrderedDict()
        for k, v in ss_dict.items():
            # dd(f'orig:[{k}]')
            new_k = pat.sub("", k)
            is_or = ('|' in new_k)
            if is_or:
                found_or_list = getOrEntries(new_k)
                found_or_list.sort(reverse=True)

                group_of_new_lines=[new_k]
                for loc, or_list in found_or_list:
                    new_group = composeSubEntries(group_of_new_lines, loc, or_list)
                    group_of_new_lines = new_group
            else:
                group_of_new_lines = [new_k]

            cleaned_group = map(cleanLine, group_of_new_lines)
            cleaned_group_list = list(cleaned_group)
            simple_entries = [(simple_key, v) for simple_key in cleaned_group_list]
            simplified_dict.update(simple_entries)

        return simplified_dict

    def bestMatchSectionString(match_str, in_str, target_ratio=None):
        def fuzzyRatioCompute(item):
            (loc, txt) = item
            rat = fuzz.ratio(match_str, txt)
            return_entry = (rat, (loc, txt))
            return return_entry

        in_str_map = Common.genmap(in_str)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            found_results = executor.map(fuzzyRatioCompute, in_str_map)

        found_results_list = list(found_results)
        found_results_list.sort(reverse=True)
        matched_rate, selected_part = found_results_list[0]
        return selected_part

    def debugging(txt):
        msg = "Target Velocity, a"
        is_debug = (msg and txt and (msg.lower() in txt.lower()))
        # is_debug = (msg and txt and (msg.lower() == txt.lower()))
        # is_debug = (msg and txt and txt.startswith(msg))
        if is_debug:
            dd(f'Debugging text: {msg} at line txt:{txt}')