import re
from definition import Definitions as df
from matcher import MatcherRecord

class StringUtils:
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

    def getTextWithin(msg):
        diff_loc, left, mid, right, _ = StringUtils.getTextWithinWithDiffLoc(msg)
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