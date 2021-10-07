import re
import operator as OP
from matcher import MatcherRecord
from definition import RefType
from collections import OrderedDict
from definition import Definitions as df

class PatternUtils:

    def patternMatch(pat: re.Pattern, text) -> MatcherRecord:
        m = pat.search(text)
        is_found = (m is not None)
        if not is_found:
            return None

        match_record = MatcherRecord(matcher_record=m)
        return match_record

    def findInvert(pattern, text: str, is_reversed=False, is_removing_symbols=True):
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
            left_part = getNoneAlphaPart(msg, is_start=True)
            right_part = getNoneAlphaPart(msg, is_start=False)
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
            diff_loc, left, mid, right, _ = getTextWithinWithDiffLoc(msg)
            return left, mid, right


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
        mm: MatcherRecord = None
        matched_dict = PatternUtils.patternMatchAll(pat, text)
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
                    test_txt = text[ws: we]
                    invert_loc_list.append((ws, we))
                ws = e
            we = len(text)
            if (ws < we):
                test_txt = text[ws: we]
                invert_loc_list.append((ws, we))

            # 4: using the invert location list, extract words, exclude empties.
            for ws, we in invert_loc_list:
                found_txt = text[ws:we]

                if is_removing_symbols:
                    left, mid, right = getTextWithin(found_txt)
                    is_empty = (not bool(mid))
                    if is_empty:
                        continue
                    else:
                        found_txt = mid
                        ws += len(left)
                        we -= len(right)

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