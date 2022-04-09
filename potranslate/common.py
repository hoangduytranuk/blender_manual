import sys
import os
from collections import OrderedDict
import hashlib
import time
from collections import deque
# from fuzzywuzzy_src.build.fuzzywuzzy import fuzz
# from fuzzywuzzy import fuzz
from bisect import bisect_left
from matcher import MatcherRecord
import re
from observer import LocationObserver
import json
import concurrent.futures
from ignore import Ignore as ig
from textmap import TextMap as TM
from pattern_utils import PatternUtils as pu
from string_utils import StringUtils as st
from get_text_within import GetTextWithin as gt

from definition import Definitions as df, \
    SentStructMode as SMODE, \
    SentStructModeRecord as SMODEREC, \
    RefType
from pprint import pprint as pp
import inspect as INP

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
                print(f'loadJSONDic - file_name is None.')
                return return_dic

            if not os.path.isfile(file_name):
                print(f'loadJSONDic - file_name:{file_name} cannot be found!')
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

        left, mid, right = gt.getTextMargin(txt)
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

    def matchStartAndEndingNonAlpha(s1: str, s2: str):
        s1_start, s1_mid, s1_end = st.getTextWithin(s1)
        s2_start, s2_mid, s2_end = st.getTextWithin(s2)

        new_s2 = str(s2)
        need_change_start = (s1_start != s2_start)
        if need_change_start:
            new_s2 = s1_start + s2_mid + s2_end

        need_change_end = (s1_end != s2_end)
        if need_change_end:
            new_s2 = s2_start + s2_mid + s1_end
        return new_s2

    def matchCase(from_str : str , to_str : str, matching_from_begin_end=False) -> str:
        from case_action_list import CaseActionList
        new_txt = CaseActionList.matchCase(from_str, to_str, matching_from_begin_end=matching_from_begin_end)
        return new_txt

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
    #             left, mid, right = gt.getTextWithin(txt)
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
        p_list = pu.patternMatchAll(pattern, txt)
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
        ga_dict = pu.patternMatchAll(df.GA_REF, txt)
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

        abbr_dict = pu.patternMatchAll(df.ABBREV_CONTENT_PARSER, abbr_txt)
        if not abbr_dict:
            return None, None, None

        abbrev_orig_rec = abbrev_part = exp_part = None
        mm: MatcherRecord = None

        try:
            abbrev_mm: MatcherRecord = None
            (abbrev_loc, abbrev_mm) = list(abbr_dict.items())[0]
            sub_list = abbrev_mm.getSubEntriesAsList()
            abbrev_orig_rec = sub_list[0]
            ab_loc, abbrev_part = sub_list[1]
            exp_loc, exp_part = sub_list[2]
        except Exception as e:
            msg = f'abbr_txt:{abbr_txt}; exception:{e}'
            df.LOG(msg, error=True)

        return abbrev_orig_rec, abbrev_part, exp_part

    def removeAbbr(msg):
        try:
            abbr_dict = pu.patternMatchAll(df.ABBREV_PATTERN_PARSER, msg)
            if not abbr_dict:
                return None

            abbrev_orig_rec = abbrev_part = exp_part = None
            mm: MatcherRecord = None

            entries=[]
            for mm_loc, mm in abbr_dict.items():
                abbrev_orig_rec = mm.getOriginAsTuple()
                l = mm.getSubEntriesAsList()
                loc, txt = l[0]
                found_texts = df.ABBR_TEXT_ALL.findall(txt)
                first_entry = found_texts[0]
                abbrev_part, exp_part = first_entry
                entry = (mm_loc, abbrev_part, exp_part)
                entries.append(entry)

            is_replace = (len(entries) > 0)
            if not is_replace:
                return None

            new_txt = str(msg)
            sorted_entries = list(sorted(entries, reverse=True))
            for mm_loc, abbrev_part, exp_part in sorted_entries:
                ss, ee = mm_loc
                left = new_txt[:ss]
                right = new_txt[ee:]
                replace_txt = f'{abbrev_part} ({exp_part})'
                replace_txt = replace_txt.title()
                new_txt = left + replace_txt + right
            return new_txt

        except Exception as e:
            df.LOG(e)
            return None

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
        tm = TM(txt, is_removing_symbols=True)
        map = tm.genmap()
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

    def getRemainedWord(orig_txt: str, new_txt: str):
        def findMatchingWordInNewTxt(search_word):
            for new_loc, new_txt_segment in new_txt_map:
                match_rat = fuzz.ratio(new_txt_segment, search_word)
                is_same = (match_rat >= df.FUZZY_MODERATE_ACCEPTABLE_RATIO)
                if is_same:
                    return True
            return False

        tm = TM(new_txt)
        new_txt_map = tm.genmap()
        obs = LocationObserver(orig_txt)

        tm1 = TM(orig_txt)
        map = tm1.genmap()
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


    def removeTheWord(trans):
        try:
            trans = df.THE_WORD.sub("", trans)
            trans = df.POSSESSIVE_APOS.sub("", trans)
        except Exception as e:
            pass
        return trans

    def jointText(orig: str, tran: str, loc: tuple):
        s, e = loc
        left = orig[:s]
        right = orig[e:]
        has_tran = (tran is not None)
        if has_tran:
            new_str = left + tran + right
        else:
            new_str = left + right
        return new_str

    def jointTextAndRemove(orig: str, tran: str, loc: tuple):
        s, e = loc
        left = orig[:s]
        right = orig[e:]
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

        pattern_txt = r'^%s$' % (simplified_pat)
        # df.LOG(pattern_txt, error=False)
        return pattern_txt

    def patStructToListOfWords(txt, removing_symbols=True):
        mm: MatcherRecord = None
        obs = LocationObserver(txt)
        struct_pat_dict = pu.patternMatchAll(df.SENT_STRUCT_PAT, txt)
        struct_pat_list = list(struct_pat_dict.items())

        struct_txt_dict = pu.findInvert(df.SENT_STRUCT_PAT, txt, is_removing_symbols=removing_symbols)
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
                local_found_dict = st.getTextWithinBrackets('(', ')', txt, is_include_bracket=False)
            else:
                local_found_dict = pu.patternMatchAll(pat, txt)

            if local_found_dict:
                local_found_dict_list.update(local_found_dict)
                loc_list = local_found_dict.keys()
                for loc in loc_list:
                    obs.markLocAsUsed(loc)
        return_dict = OrderedDict(sorted(local_found_dict_list.items(), reverse=True))
        return (return_dict, obs)

    # def genmap(msg, is_reverse=True, is_removing_symbols=False, using_pattern=None):
    #     def simplifiesMatchedRecords():
    #         mm: MatcherRecord = None
    #         for loc, mm in matched_list:
    #             can_location_be_used = obs.isUsableLoc(loc)
    #             if not can_location_be_used:
    #                 continue
    #
    #             txt = mm.txt
    #             entry = {loc: txt}
    #             loc_dic.update(entry)
    #
    #     def removeIgnoredEntries(input_list):
    #         loc_obs = LocationObserver(msg)
    #         ignored = []
    #         non_ignore_list=[]
    #         for loc, txt in input_list:
    #             is_ignore = ig.isIgnored(txt)
    #             if is_ignore:
    #                 df.LOG(f'IGNORED:[{txt}]')
    #                 loc_obs.markLocAsUsed(loc)
    #
    #         for loc, txt in input_list:
    #             is_ignored = loc_obs.isLocUsed(loc)
    #             if is_ignored:
    #                 df.LOG(f'IGNORED:[{txt}]')
    #                 continue
    #             entry = (loc, txt)
    #             non_ignore_list.append(entry)
    #         return non_ignore_list
    #
    #     def genListOfDistance(max):
    #         dist_list = []
    #         for s in range(0, max):
    #             for e in range(0, max):
    #                 is_valid = (s < e)
    #                 if not is_valid:
    #                     continue
    #
    #                 distance = (e - s)
    #                 entry = (distance, s, e)
    #                 if entry not in dist_list:
    #                     dist_list.append(entry)
    #         return dist_list
    #
    #     def sortGetWordLen(item):
    #         (loc, txt) = item
    #         wc = len(txt.split())
    #         txt_len = len(txt)
    #         return (txt_len, wc)
    #
    #     part_list = []
    #     obs: LocationObserver = None
    #     # ref_dict_list, obs = Common.getRefDictList(msg)
    #     # occupied_list = ref_dict_list.keys()
    #
    #     sep_pattern = (df.SPACE_WORD_SEP if not is_removing_symbols else df.SYMBOLS)
    #     actual_pattern = (using_pattern if using_pattern else sep_pattern)
    #     matched_dict = pu.patternMatchAll(actual_pattern, msg)
    #     matched_list = list(matched_dict.items())
    #     max = len(matched_dict)
    #     loc_dic = {}
    #     try:
    #         dist_list = genListOfDistance(max)
    #         dist_list.sort(reverse=is_reverse)
    #         for entry in dist_list:
    #             distance, from_index, to_index = entry
    #             start_loc, start_mm = matched_list[from_index]
    #             end_loc, end_mm = matched_list[to_index]
    #
    #             ss1, ee1 = start_loc
    #             ss2, ee2 = end_loc
    #
    #             sentence = msg[ss1: ee2]
    #             # word_count = (ee2 - ss1)
    #
    #             sub_loc = (ss1, ee2)
    #             can_location_be_used = obs.isUsableLoc(sub_loc)
    #             if not can_location_be_used:
    #                 continue
    #
    #             entry = {sub_loc: sentence}
    #             loc_dic.update(entry)
    #     except Exception as e:
    #         df.LOG(e, error=True)
    #         raise e
    #
    #     simplifiesMatchedRecords()
    #
    #     part_list = list(loc_dic.items())
    #     part_list.sort(key=sortGetWordLen, reverse=True)
    #     non_ignored_list = removeIgnoredEntries(part_list)
    #
    #     return non_ignored_list

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
            part_match_dict = pu.patternMatchAll(pat, txt)
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

        tm = TM(in_str, using_pattern=df.WORD_ONLY)
        in_str_map = tm.genmap()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            found_results = executor.map(fuzzyRatioCompute, in_str_map)

        found_results_list = list(found_results)
        if found_results:
            found_results_list.sort(reverse=True)
            matched_rate, selected_part = found_results_list[0]
        else:
            # either match all or they are all ignored
            matched_rate = 100
            selected_part = in_str
        return selected_part

    def getBracketTextFromOBSBlank(obs: LocationObserver, is_include_bracket=False):
        from string_utils import StringUtils as st
        def adjustLocation(entry):
            orig_loc = adjustLocation.orig_loc
            loc = entry[0]
            mm: MatcherRecord = entry[1]
            txt = mm.txt
            (os, oe) = orig_loc
            (cs, ce) = loc
            ns = os + cs
            ne = ns + len(txt)
            new_loc = (ns, ne)
            mm.updateMasterLocTuple(new_loc)
            return mm

        def removeBlank(entry):
            loc = entry[0]
            mm: MatcherRecord = entry[1]
            txt = mm.txt
            found_dict = pu.findInvert(df.FILLER_CHAR_INVERT, txt)
            sub_mm: MatcherRecord
            adjustLocation.orig_loc = loc
            adjusted_list = list(map(adjustLocation, found_dict.items()))
            return adjusted_list

        local_found_dict = st.getTextWithinBrackets('<|(', '>|)', obs.blank, is_include_bracket=is_include_bracket)
        removed_blank_list = list(map(removeBlank, local_found_dict.items()))
        removed_blank_list = [x for y in removed_blank_list for x in y]
        return removed_blank_list

    def debugging(txt):
        msg = "Opposing"
        # is_debug = (msg and txt and (msg.lower() in txt.lower()))
        is_debug = (msg and txt and (msg.lower() == txt.lower()))
        # is_debug = (msg and txt and txt.startswith(msg))
        if is_debug:
            print(f'Debugging text: {msg} at line txt:{txt}')