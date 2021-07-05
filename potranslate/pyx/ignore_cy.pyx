import sys
import re
from os import sep as dirsep
from os.path import pathsep
import inspect as INP

from common_cy import Common as cm, DEBUG, dd, pp
from matcher_cy import MatcherRecord
from definition_cy import Definitions as df

class Ignore:

    def isReverseOrder(msg):
        for w in Ignore.reverse_order_list:
            is_reverse = (re.search(w, msg, flags=re.I) is not None)
            if is_reverse:
                dd(f'isReverseOrder -> pattern:[{w}] msg:[{msg}]')
                return True
        return False

    def isKeepContains(msg):
        found_item = cm.findInSortedList(msg, df.keep_contains_list)
        is_found = (found_item is not None)
        if is_found:
            return True
        else:
            return False

    def isKeep(msg):
        found_item = cm.findInSortedList(msg, df.keep_list)
        is_found = (found_item is not None)
        if is_found:
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

            is_ref_link = is_function = is_ignore_word = is_dos_command = is_ignore_start = False

            is_ref_link = cm.isLinkPath(find_msg)
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
                dd("IGNORING:", msg)
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
            for m in df.runtime_ignore_list:
                is_found = (m.search(text_line) is not None)
                if is_found:
                    dd(f'isIgnoredWord: pattern:[{m.pattern}] [{text_line}]')
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
