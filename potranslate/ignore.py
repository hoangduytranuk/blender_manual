import sys
import re
from os import sep as dirsep
from os.path import pathsep
from matcher import MatcherRecord
from definition import Definitions as df
import inspect as INP
from bisect import bisect_left
from pprint import pprint as pp
from observer import LocationObserver

class Ignore:

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

    def isReverseOrder(msg):
        for w in Ignore.reverse_order_list:
            is_reverse = (re.search(w, msg, flags=re.I) is not None)
            if is_reverse:
                df.LOG(f'isReverseOrder -> pattern:[{w}] msg:[{msg}]')
                return True
        return False

    def isKeepContains(msg):
        found_item = Ignore.findInSortedList(msg, df.keep_contains_list)
        is_found = (found_item is not None)
        if is_found:
            return True
        else:
            return False

    def isKeep(msg):
        found_item = Ignore.findInSortedList(msg, df.keep_list)
        is_found = (found_item is not None)
        if is_found:
            return True
        else:
            return False

    def isLinkPath(txt: str) -> bool:
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

        def getTextWithin(msg):
            diff_loc, left, mid, right, _ = getTextWithinWithDiffLoc(msg)
            return left, mid, right

        invalid_combination = ('.,' in txt) or (' ' in txt)
        if invalid_combination:
            return False

        is_blank_quote = df.BLANK_QUOTE_ABS.search(txt)
        if is_blank_quote:
            return False

        is_path = isPath(txt)
        if is_path:
            return True

        is_url = df.urlx_engine.has_urls(txt)
        if is_url:
            return False

        left, mid, right = getTextWithin(txt)
        is_path = isPath(mid)
        if is_path:
            return True
        else:
            return False


    def isIgnored(msg):

        if not msg:
            return True

        try:
            find_msg = msg.lower()
            is_keep = Ignore.isKeep(find_msg)
            if is_keep:
                return False

            is_allowed_contains = Ignore.isKeepContains(find_msg)
            if is_allowed_contains:
                return False

            is_ignore_outright = (find_msg in df.ignore_txt_list)
            if is_ignore_outright:
                return True

            is_ref_link = is_function = is_ignore_word = is_dos_command = is_ignore_start = False

            is_ref_link = Ignore.isLinkPath(find_msg)
            if not is_ref_link:
                is_function = (df.FUNCTION.search(find_msg) is not None)
                if not is_function:
                    is_ignore_word = Ignore.isIgnoredWord(find_msg)
                    if not is_ignore_word:
                        is_dos_command = Ignore.isDosCommand(find_msg)
                        if not is_dos_command:
                            is_ignore_start = Ignore.isIgnoredIfStartsWith(find_msg)

            is_ignore = (is_function or
                        is_ignore_word or
                        is_dos_command or
                        is_ignore_start or
                        is_ref_link )
            # is_ignore = (is_ignore_word or is_dos_command or is_ignore_start)
            if is_ignore:
                #dd("checking for ignore")
                dict_ignore = {"is_ignore_word": is_ignore_word,
                               "is_dos_command": is_dos_command,
                               "is_ignore_start": is_ignore_start,
                               "is_function": is_function,
                               "is_ref_link": is_ref_link
                               }
                df.LOG(f"IGNORING: [{msg}]")
                pp(dict_ignore)

            return is_ignore
        except Exception as e:
            df.LOG(f'{e}; msg:{msg}', error=True)
            raise e

    def isIgnoredIfStartsWith(text_line : str):
        if (text_line is None) or (len(text_line) == 0):
            return True

        for x in df.ignore_start_with_list:
            is_starts_with = (text_line.lower().startswith(x.lower()))
            if is_starts_with:
                #dd("isIgnoredIfStartsWith:", x)
                return True
        else:
            return False

    def isIgnoredSimple(text_line : str):
        if (text_line is None) or (len(text_line) == 0):
            return True

        for x in df.ignore_list:
            if len(x) == 0:
                continue

            p = re.compile(x, flags=re.I)
            m = p.search(text_line)
            is_found = (m != None)
            if (is_found):
                df.LOG(f'text_line:[{text_line}]; p:[{p}] m:[{m}]')
                return True
        return False

    def isIgnoredWord(text_line : str):
        if (text_line is None) or (len(text_line) == 0):
            return True

        is_create_runtime_ignore_list = (df.runtime_ignore_list == None)
        if is_create_runtime_ignore_list:
            df.runtime_ignore_list = []
            for pattern in df.ignore_list:
                if len(pattern) == 0:
                    continue

                m = re.compile(pattern, flags=re.I)
                df.runtime_ignore_list.append(m)

        pattern = None
        try:
            for index, m in enumerate(df.runtime_ignore_list):
                is_found = (m.search(text_line) is not None)
                if is_found:
                    df.LOG(f'isIgnoredWord: [{index}] pattern:[{m.pattern}] text_line:[{text_line}]')
                    return True
            else:
                return False
        except Exception as e:
            df.LOG(f'{e}; text_line:[{text_line}]; pattern:[{pattern}]', error=True)
        return False

    def isDosCommand(text):
        if (text is None) or (len(text) == 0):
            return False

        for w in df.DOS_COMMANDS:
            p = re.compile(r'^\b{}\b$'.format(w))
            is_dos_command = (p.search(text) != None)
            if is_dos_command:
                return True
        return False

    def isFilePath(text_line : str):
        if (text_line is None) or (len(text_line) == 0):
            return False

        has_path_characters = (df.PATH_CHAR.search(text_line) is not None) and ('kbd' not in text_line)

        #check to see if any word is title case, ie. Selected/Unselected, in which case it's not a PATH
        if has_path_characters:
            word_list = text_line.split(dirsep)
            word : str = None
            for word in word_list:
                is_title_case = (word.istitle())
                if is_title_case:
                    return False

        starts_with_path_chars = text_line.startswith('~')
        ends_with_extensions = (df.ENDS_WITH_EXTENSION.search(text_line) is not None)
        contain_spaces = (" " in text_line)
        is_path = (has_path_characters or starts_with_path_chars or ends_with_extensions) and not contain_spaces

        if is_path:
            dd("isFilePath", text_line)
            #exit(0)

        return is_path
