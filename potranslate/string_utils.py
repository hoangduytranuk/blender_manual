import re
from definition import Definitions as df
from matcher import MatcherRecord
from collections import deque, OrderedDict
from observer import LocationObserver
from definition import RefType

class StringUtils:
    def getTextWithinWithDiffLoc(msg, to_matcher_record=False):
        # should really taking bracket pairs into account () '' ** "" [] <> etc.. before capture
        left_part = StringUtils.getNoneAlphaPart(msg, is_start=True)
        right_part = StringUtils.getNoneAlphaPart(msg, is_start=False)
        ss = len(left_part)
        ee = (-len(right_part) if right_part else len(msg))
        mid_part = msg[ss:ee]
        length_ee = len(right_part)
        diff_loc = (ss, length_ee)

        main_record: MatcherRecord = None
        if to_matcher_record:
            ls = 0
            le = ss
            ms = le
            me = ms + len(mid_part)
            rs = me
            re = rs + len(right_part)

            main_record = MatcherRecord(s=0, e=len(msg), txt=msg)
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

    def getTextWithin(msg):
        # start_brk_set = '{[(<'
        # end_brk_set = '}])>'
        #
        # glob_obs = df.global_ref_map
        #
        # start_symb_set = StringUtils.getNoneAlphaPart(msg, is_start=True)
        # end_symb_set = StringUtils.getNoneAlphaPart(msg, is_start=False)
        #
        # start_check = [x for x in start_symb_set if x in start_brk_set]
        # end_check = [x for x in end_symb_set if x in end_brk_set]
        #
        # has_brk = (start_check or end_check)
        #
        # if not has_brk:
        #     return "", msg, ""
        #
        # start_pos = len(start_symb_set)
        # for index in range(start_pos-1, -1, -1):
        #     c = start_symb_set[index]
        #     is_brk = (c in start_brk_set)
        #     if not is_brk:
        #         continue

        diff_loc, left, mid, right, _ = StringUtils.getTextWithinWithDiffLoc(msg)
        return left, mid, right

    def removeStartEndBrackets(input_txt, start_bracket=None, end_bracket=None):
        try:
            str_len = len(input_txt)
            start_loc = 0
            end_loc = str_len

            s_brk = (start_bracket if start_bracket else '(')
            e_brk = (end_bracket if end_bracket else ')')

            bracket_pattern_txt = r'([\%s\%s])' % (s_brk, e_brk)
            bracket_pattern = re.compile(bracket_pattern_txt)
            found_dict = StringUtils.patternMatchAll(bracket_pattern, input_txt)
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

            is_ignore = (len(txt_line) < 3)
            if not is_ignore:
                loc = (ss, ee)
                entry = (loc, txt_line)
                sentence_list.append(entry)
            return True

        def getBracketList(start_brk, end_brk):
            # split at the boundary of start and end brackets
            try:
                # 1. find positions of start bracket
                if is_same_brakets:
                    p_txt = r'\%s' % start_brk
                else:
                    p_txt = r'[\%s\%s]' % (start_brk, end_brk)

                p = re.compile(p_txt)
                brk_list = StringUtils.patternMatchAll(p, input_txt)
                return brk_list, p
            except Exception as e:
                df.LOG(f'{e} [{input_txt}]', error=True)
                raise e
            return brk_list

        def getSentenceList(start_brk, end_brk):
            bracket_list, pattern = getBracketList(start_brk, end_brk)
            if not bracket_list:
                return sentence_list, pattern

            # detecting where start/end and take the locations
            mm: MatcherRecord = None
            if is_same_brakets:
                for loc, mm in bracket_list.items():
                    s, e = loc
                    bracket = mm.txt
                    is_bracket = (bracket == start_brk)
                    if is_bracket:
                        if not q:
                            q.append(s)
                        else:
                            pop_q(s, e)
            else:
                for loc, mm in bracket_list.items():
                    s, e = loc
                    bracket = mm.txt
                    is_open = (bracket == start_brk)
                    is_close = (bracket == end_brk)
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

        def findUsingBracketSet(start_brk, end_brk):
            output_dict = OrderedDict()
            txt_len = len(input_txt)

            if is_same_brakets:
                df.LOG(f'getTextWithinBracket() - WARNING: start_bracket and end_braket is THE SAME {start_bracket}. '
                   f'ERRORS might occurs!')

            sentence_list, pattern = getSentenceList(start_brk, end_brk)
            if not sentence_list:
                return output_dict

            loc_list = []
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
                    (sub_loc, actual_txt) = StringUtils.removeStartEndBrackets(txt, start_bracket=start_brk,
                                                                          end_bracket=end_brk)
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

        result={}
        is_same_brakets = False
        q = None
        sentence_list = None
        start_bracket_list = start_bracket.split('|')
        end_bracket_list = end_bracket.split('|')
        for index in range(0, len(start_bracket_list)):
            q = deque()
            sentence_list = []

            start_brk = start_bracket_list[index]
            end_brk = end_bracket_list[index]
            is_same_brakets = (start_brk == end_brk)
            result_set = findUsingBracketSet(start_brk, end_brk)
            if result_set:
                result.update(result_set)

        return result

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
            left_part = StringUtils.getNoneAlphaPart(orig_word, is_start=True)
            right_part = StringUtils.getNoneAlphaPart(orig_word, is_start=False)
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
                word_percent = StringUtils.matchWordPercent(w1, w2)
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
        list_of_remain = StringUtils.patternMatchAll(df.SPACES, this_part)
        this_txt_dict = {}
        for loc, mm in list_of_remain:
            (s, e), txt_part = mm.getOriginAsTuple()
            is_not_worth_keeping = (df.SYMBOLS_ONLY.search(txt_part) is not None)
            if is_not_worth_keeping:
                continue

            start_count, end_count, new_txt_part = StringUtils.stripSpaces(txt_part)
            new_loc = (s + start_count, e - end_count)
            entry = {new_loc: new_txt_part}
            this_txt_dict.update(entry)
        # this list could be empty, in which case remove left part, keep the right part (A - B = empty => keep B only)
        return this_txt_dict