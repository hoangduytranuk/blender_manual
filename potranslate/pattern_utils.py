import re
import operator as OP
from matcher import MatcherRecord
from definition import RefType
from collections import OrderedDict
from definition import Definitions as df
from observer import LocationObserver

class PatternUtils:

    def patternMatch(pat: re.Pattern, text) -> MatcherRecord:
        m = pat.search(text)
        is_found = (m is not None)
        if not is_found:
            return None

        match_record = MatcherRecord(matcher_record=m)
        return match_record

    def findInvert(pattern, text: str, is_reversed=False, is_removing_symbols=False):
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

        pat = pattern

        is_string = isinstance(pattern, str)
        if is_string:
            # # form the invert character pattern
            # pat_string = r'(%s)(\w[^%s]+\w)(%s)' % (pattern, pattern, pattern)
            pat = compile(pattern)

        obs = LocationObserver(text)
        found_dict = obs.findInvert(pat, is_reverse=is_reversed, is_removing_symbol=is_removing_symbols)
        return found_dict

    def patternMatchAll(pat: re.Pattern, text, ref_type=None, reversed=False, is_including_surrounding_symbols=False, start_at=-1, end_at=-1, loc=None, using_origin_loc=None):
        return_dict = {}
        try:
            if loc:
                start_at = loc[0]
                end_at = loc[1]
                is_debug = (start_at > 0)
                if is_debug:
                    is_debug = True

            start = (start_at if start_at >= 0 else 0)
            end = (end_at if end_at >= 0 else len(text))
            m: re.Match = None
            for m in pat.finditer(text, start, end):
                match_record = MatcherRecord(matcher_record=m, ref_type=ref_type)
                is_using_orig_loc = (using_origin_loc is not None)
                if is_using_orig_loc:
                    match_record.updateMasterLocTuple(using_origin_loc)
                match_record.pattern = pat
                sub_list = match_record.getSubEntriesAsList()
                try:
                    ref_type = match_record.type
                    is_unbracketable = (ref_type in df.ref_type_unquoteable)
                    can_remove_quotes = (not is_including_surrounding_symbols) and is_unbracketable
                    if can_remove_quotes:
                        (loc, entry_txt) = sub_list[1]
                    else:
                        (loc, entry_txt) = sub_list[0]
                except Exception as e:
                    (loc, entry_txt) = sub_list[0]

                dict_entry = {loc: match_record}
                return_dict.update(dict_entry)

            if reversed:
                reversed_list = list(sorted(list(return_dict.items()), reverse=True))
                return_dict = OrderedDict(reversed_list)
        except Exception as e:
            pass
            # df.LOG(e)
        return return_dict