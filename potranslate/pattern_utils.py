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

    def patternMatchAll(pat, text):
        return_dict = {}
        try:
            for m in pat.finditer(text):
                match_record = MatcherRecord(matcher_record=m)
                match_record.pattern = pat
                loc = (match_record.s, match_record.e)
                dict_entry = {loc: match_record}
                return_dict.update(dict_entry)
        except Exception as e:
            pass
            # df.LOG(e)
        return return_dict