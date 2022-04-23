import os
import re
from datetime import datetime, date
from pytz import timezone
from sphinx_intl import catalog as c
from potask_base import POTaskBase, POResultRecord
from babel.messages import Catalog, Message
from pprint import pp
from string_utils import StringUtils as su
from translation_finder import TranslationFinder

class CleanRepeatLines(POTaskBase):
    def __init__(self,
                 input_file=None,
                 output_to_file=None,
                 clean_repeat_ignore_file=None,
                 clean_repeat_keep_file=None,
                 ):
        POTaskBase.__init__(
            self,
            input_file=input_file,
            output_to_file=output_to_file,
            clean_repeat_ignore_file=clean_repeat_ignore_file,
            clean_repeat_keep_file=clean_repeat_keep_file
        )
        self.message_list=[]
        self.tf = TranslationFinder()

    def getTimeNow(self):
        local_time = timezone('Europe/London')
        fmt = '%Y-%m-%d %H:%M%z'
        loc_dt = local_time.localize(datetime.datetime.now())
        formatted_dt = loc_dt.strftime(fmt)
        return formatted_dt

    def keepACopyOrNot(self, entry):
        (node, msg) = entry
        is_keep_original = self.isDupOrig(node)
        if not is_keep_original:
            return None

        is_ending_with_dot = (msg.endswith('.') and not msg.endswith('...'))
        if is_ending_with_dot:
            return f'Full-stop ending: {msg}'
        else:
            return msg

    def readFile(self, file_name):
        with open(file_name, 'r') as f:
            data_lines = f.read().splitlines()
        return data_lines

    def writeFile(self, file_name, data):
        data_list = [(x + '\n') for x in data]
        with open(file_name, 'w+') as f:
            f.writelines(data_list)

    def removeIfNotRepeatable(self, non_repeat_list, keep_list):
        from definition import Definitions as df
        from pattern_utils import PatternUtils as pu

        def isInLocation(loc_entry):
            check_string = isInLocation.check_string
            (location_txt, line_no) = loc_entry
            is_in = (check_string in location_txt)
            if is_in:
                is_in = True
            return is_in

        def isGlossary(m: Message):
            check_string = 'manual/glossary/index'
            locations = m.locations
            isInLocation.check_string = check_string
            is_in_list = list(filter(isInLocation, locations))
            is_index = bool(is_in_list) and len(is_in_list) > 0
            return is_index

        def cleanRepeatedMsgstr(mid: str, mstr: str, is_glossary: bool):
            from matcher import MatcherRecord
            def searchDict(index: int):
                test_list = [(index in loc) for loc in dict_loc_list]
                return any(test_list)

            def replaceSymbol(txt: str, from_symb_list: list, to_symb_list: list):

                def isLocationFoundPartOfRefs(dict_loc):
                    ds = dict_loc[0]
                    de = dict_loc[1]
                    search_loc = isLocationFoundPartOfRefs.search_loc
                    s_s = search_loc[0]
                    s_e = search_loc[1]
                    is_within_ref_loc = (s_s >= ds) and (s_e <= de)
                    return is_within_ref_loc

                def replaceSymbol(work_entry):
                    work_txt = replaceSymbol.work_txt
                    brk_pair = work_entry[0]
                    loc = work_entry[1]
                    mm: MatcherRecord = work_entry[2]

                    isLocationFoundPartOfRefs.search_loc = loc
                    loc_in_ref_test_list = list(filter(isLocationFoundPartOfRefs, dict_loc_list))
                    is_loc_in_ref = any(loc_in_ref_test_list)
                    if is_loc_in_ref:
                        return False

                    from_symb = brk_pair[0]
                    to_symb = brk_pair[1]

                    is_from_symbol_in_original = (from_symb in mid)
                    if is_from_symbol_in_original:
                        return False

                    (s, e) = loc
                    left = work_txt[:s]
                    right = work_txt[e:]
                    replaceSymbol.work_txt = left + to_symb + right
                    return True

                from_sym_txt = re.escape(''.join(from_symb_list))
                sym_pat_txt = r'[%s]' % (from_sym_txt)
                try:
                    sym_pat = re.compile(sym_pat_txt)
                except Exception as e:
                    print(f'{sym_pat_txt}, {e}')
                    raise e
                found_dict = pu.patternMatchAll(sym_pat, txt, reversed=True)
                is_found = (len(found_dict) > 0)
                if not is_found:
                    return txt

                # matching up the [ with (, and ] with ), so they come into one tuple.
                symbol_pair_list = [(from_symb_list[i], to_symb_list[i]) for i in range(len(from_symb_list))]

                # form a working set, including "['[', ')], (2, 3), mm: MatcherRecord" to pass into the function
                # to replace all locations found on text
                work_list = [(pair, loc, mm) for (loc, mm) in found_dict.items() for pair in symbol_pair_list if mm.txt == pair[0]]

                # function must work on the same piece of text
                replaceSymbol.work_txt = txt
                result_list = list(filter(replaceSymbol, work_list))

                # get the worked text out of the function
                new_txt = replaceSymbol.work_txt
                return new_txt

            ref_dict = pu.patternMatchAll(df.ABBR_SEARCH, mstr)
            has_abbr = len(ref_dict) > 0
            if has_abbr:
                debug = True

            dict_loc_list = (list(ref_dict.keys()) if has_abbr else [])

            # is_debug = ('OCIO' in mid)
            # if is_debug:
            #     is_debug = True

            from_symb_list = ['(', ')']
            to_symb_list = ['[', ']']

            possible_repeat = [
                f"{mid} --- ",
                f" --- ({mid})",
                f"{mid} (",
                f" ({mid})",
                f"{mid} ",
                f" {mid}",
            ]
            new_mstr = str(mstr)
            changed = False
            for repeat_pat in possible_repeat:
                is_pattern_in = (repeat_pat in new_mstr)
                if is_pattern_in:
                    new_mstr = new_mstr.replace(repeat_pat, "")
                    changed = True
            if changed:
                mstr = new_mstr

            mstr = replaceSymbol(mstr, to_symb_list, from_symb_list)
            if is_glossary:
                to_symb_list = ['', '']
                mstr = replaceSymbol(mstr, from_symb_list, to_symb_list)
            return mstr

        def translateMsgid(mid: str, mstr: str):
            # mid_word = (df.CHARACTERS.findall(mid))
            # for word in mid_word:
            has_translation = len(mstr) > 0
            tran = mstr
            if not has_translation:

                tran = self.tf.isInDict(mid)
                has_translation = (tran is not None)
                if has_translation:
                    print(f'FOUND:{mid} -> {tran}')
                else:
                    print(f'NOT FOUND:{mid}')
            return tran

        def isRepeatedAlready(mid: str, mstr: str):
            def isWordInMstr(word: str):
                try:
                    is_found = (word in mstr)
                except Exception as e:
                    return False
                return is_found

            mid_word_list = df.CHARACTERS.findall(mid)
            result_list = list(filter(isWordInMstr, mid_word_list))
            return len(result_list) == len(mid_word_list)

        def updateMessage(m: Message):
            from refs.ref_driver import RefDriver
            mid = m.id
            valid = bool(mid)
            if not valid:
                return None

            is_title = (mid in keep_list)
            if not is_title:
                return None

            is_all_one_ref = df.GA_REF_ABS.search(mid)
            if is_all_one_ref:
                old_tran = str(m.string)
                ref_driver = RefDriver(tf=self.tf)
                temp_message: Message = ref_driver.translateRefs(m)
                if temp_message is not None:
                    new_tran = temp_message.string
                    m.string = new_tran
                    return m
                else:
                    return None

            is_glossary = isGlossary(m)

            mstr = m.string
            mstr = cleanRepeatedMsgstr(mid, mstr, is_glossary)
            mstr = translateMsgid(mid, mstr)

            is_already_repeated = isRepeatedAlready(mid, mstr)
            if not is_already_repeated:
                mstr = ("" if (mstr is None) else mstr)
                new_mstr = (f'{mid} --- {mstr}' if is_glossary else f'{mstr} --- {mid}')
            else:
                new_mstr = mstr
            m.string = new_mstr
            return m

        home = self.home
        data = c.load_po(self.po_path)
        out_file = self.opo_path
        msg_list = list(map(updateMessage, data))
        result_list = [m for m in msg_list if bool(m)]

        m: Message = None
        for m in result_list:
            msg = f'msgid: "{m.id}"\nmsgstr: "{m.string}"\n\n'
            print(msg)

        is_changed = (len(result_list) > 0) and (out_file is not None)
        if is_changed:
            c.dump_po(out_file, data, line_width=4096)
            print(f'Writing changes to: {out_file}')

    def removeUnrepeatedEntries(self):
        ignore_file = self.clean_repeat_ignore_file
        try:
            ignore_list = self.readFile(self.clean_repeat_ignore_file)
        except Exception as e:
            ignore_list = []

        try:
            keep_list = self.readFile(self.clean_repeat_keep_file)
        except Exception as e:
            keep_list = []

        self.removeIfNotRepeatable(ignore_list, keep_list)

    def performTask(self):
        self.removeUnrepeatedEntries()

# potask.py -clrep -f /Users/hoangduytran/Dev/tran/blender_manual_0003_0020.po -igf /Users/hoangduytran/Dev/tran/ignore.log -kpf /Users/hoangduytran/Dev/tran/keep_refs.log
# -