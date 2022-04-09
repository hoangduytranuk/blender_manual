import os
import time

from sphinx_intl import catalog as c
from babel.messages import Catalog, Message
from potask_base import POTaskBase, POResultRecord, writeJSONDic, loadJSONDic
from translation_finder import TranslationFinder
from nocasedict import NoCaseDict
from ignore import Ignore as ig
from definition import Definitions as df
# from common import Common as cm
import pathlib as PL
from get_text_within import GetTextWithin as gt

class UpdateDict(POTaskBase):
    slash = '/'
    def __init__(self,
                 input_file=None,
                 output_to_file=None,
                 translation_file=None,
                 set_translation_fuzzy=None,
                 apply_case_matching_orig_txt=None
                 ):
        POTaskBase.__init__(
                self,
                input_file=input_file,
                output_to_file=output_to_file,
                translation_file=translation_file,
                set_translation_fuzzy=set_translation_fuzzy,
                apply_case_matching_orig_txt=apply_case_matching_orig_txt
        )
        self.tf = None

    def whichFile(self):
        ext = PL.Path(self.tran_file).suffix
        ext_lower = ext.lower()
        is_json = (ext_lower == '.json')
        is_po = (ext_lower == '.po')
        return (is_json, is_po)

    def loadDictFromFile(self):
        try:
            (is_json, is_po) = self.whichFile()
            if is_json:
                tran_data = loadJSONDic(self.tran_file)
            else:
                tran_data = c.load_po(self.tran_file)
            return tran_data
        except Exception as e:
            print(e)
            raise e

    def countSlashInAbbrevs(self, txt):
        try:
            abbrev_list = df.ABBREV_PATTERN_PARSER.findall(txt)
            has_abbrev = (len(abbrev_list) > 0)
            if not has_abbrev:
                return 0

            slash_overall_count = 0
            abbrev: str = None
            for abbrev in abbrev_list:
                count_slash = abbrev.count(UpdateDict.slash)
                slash_overall_count += count_slash
            return slash_overall_count
        except Exception as e:
            msg = f'txt:{txt}; {e}'
            df.LOG(msg)
            raise e

    def correctCases(self, dict_m: Message):
        from enum import Enum
        class CheckCases(Enum):
            NONE = 0
            LOWER = 1
            UPPER = 2
            TITLE = 3

        def correct_start_case(check_case: CheckCases, s1: str, s2: str):
            is_lower = (check_case == CheckCases.LOWER)
            is_upper = (check_case == CheckCases.UPPER)
            is_title = (check_case == CheckCases.TITLE)

            is_valid = (s1 and s2)
            if not is_valid:
                return s2, False

            s1_first_char = s1[0]
            s2_first_char = s2[0]
            valid = (s1_first_char.isalpha() and s2_first_char.isalpha())
            if not valid:
                return s2, False

            s2_remainder = s2[1:]
            if is_title:
                s1_started = (s1_first_char.istitle())
                s2_started = (s1_first_char.istitle())
            elif is_upper:
                s1_started = (s1.isupper())
                s2_started = (s2.isupper())
            elif is_lower:
                s1_started = (s1.lower())
                s2_started = (s2.lower())

            diff_start_s1 = (s1_started and not s2_started)
            diff_start_s2 = (not s1_started and s2_started)

            new_s2 = str(s2)
            if diff_start_s1:
                if is_title:
                    new_s2 = f'{s2_first_char.title()}{s2_remainder}'
                elif is_upper:
                    new_s2 = s2.upper()
                elif is_lower:
                    new_s2 = s2.lower()
            elif diff_start_s2:
                if is_title:
                    new_s2 = f'{s2_first_char.lower()}{s2_remainder}'
                elif is_upper:
                    new_s2 = new_s2.lower()
                elif is_lower:
                    new_s2 = new_s2.upper()

            return new_s2, (new_s2 != s2)

        def correct_start_end_symbol(char: str, s1:str, s2:str):
            s1_started = (s1.startswith(char))
            s2_started = (s2.startswith(char))
            s1_ended = (s1.endswith(char))
            s2_ended = (s2.endswith(char))

            diff_start_s1 = (s1_started and not s2_started)
            diff_start_s2 = (not s1_started and s2_started)
            diff_end_s1 = (s1_ended and not s2_ended)
            diff_end_s2 = (not s1_ended and s2_ended)

            old_s2 = str(s2)
            new_s2 = str(s2)
            if diff_start_s1:
                new_s2 = f'{char}{s2}'
            elif diff_start_s2:
                new_s2 = s2[1:]
            elif diff_end_s1:
                new_s2 = f'{s2}{char}'
            elif diff_end_s2:
                new_s2 = s2[:-1]
            return new_s2, (new_s2 != old_s2)

        msgid:str = dict_m.id
        msgstr:str = dict_m.string

        is_s1 = bool(msgid)
        is_s2 = bool(msgstr)
        invalid = not (is_s1 and is_s2)
        if invalid:
            return False

        is_debug = ('RNA Blender' in msgid)
        if is_debug:
            print('Debug')

        changed = False
        old_msgstr = str(msgstr)
        msgstr = msgstr.strip()
        symb_list=[' ', '.', ':']
        for symb in symb_list:
            msgstr, is_changed = correct_start_end_symbol(symb, msgid, msgstr)
            if is_changed:
                changed = True
                break

        case_list=[CheckCases.TITLE, CheckCases.LOWER]
        for case in case_list:
            msgstr, is_changed = correct_start_case(case, msgid, msgstr)
            if is_changed:
                changed = True
                break

        if changed:
            dict_m.string = msgstr
        return changed

    def updateMatchCase(self):
        from case_action_list import CaseActionList
        home = os.environ['HOME']
        # po_file_path = os.path.join(home, 'Dev/tran/blender_manual/ref_dict_0003.po')
        # po_file_path = os.path.join(home, 'Dev/tran/blender_docs/locale/vi/LC_MESSAGES/blender_manual.po')
        po_file_path = os.path.join(home, 'new_ref_dict_0003.po')
        t1 = time.process_time()
        po_cat = c.load_po(po_file_path)
        t2 = time.process_time()
        diff = (t2 - t1)
        print(f'loading po time: [{diff}]')
        m: Message = None
        changed = False
        for m in po_cat:
            msgid = m.id
            is_empty = not bool(msgid)
            if is_empty:
                continue

            msgsgtr = m.string
            # t1 = time.process_time()
            new_msgstr = CaseActionList.matchCase(msgid, msgsgtr)
            # t2 = time.process_time()
            # diff = (t2 - t1)
            is_changed = (new_msgstr != msgsgtr)
            if is_changed:
                msg = f'msgid: "{msgid}"\nmsgstr: "{msgsgtr}"\nnewstr: "{new_msgstr}"\n\n'
                print(msg)
                m.string = new_msgstr
                changed = True
        is_saved = (changed and bool(self.opo_path))
        if is_saved:
            c.dump_po(self.opo_path, po_cat, line_width=4096)
        exit(0)

    # -updict -tran /Users/hoangduytran/Dev/tran/blender_ui/merged.po -ig -cl
    def performTask(self):
        self.updateMatchCase()

        # self.setFiles()
        # msg_data = c.load_po(self.po_path)
        # self.tf = TranslationFinder(
        #     apply_case_matching_orig_txt=self.apply_case_matching_orig_txt
        # )
        # dict_list = None
        # use_external_translation = (self.tran_file is not None) and (os.path.isfile(self.tran_file))
        # if not use_external_translation:
        #     raise RuntimeError('No external file presents! From where do I get the dictionary definitions from? (JSON/PO) only!')
        #
        # # tf_master_dict: NoCaseDict = self.tf.master_dic_list
        # (is_json, is_po) = self.whichFile()
        # if is_po:
        #     tf_master_dict.loadData(self.tran_file, is_update=True)
        #     # if self.opo_path:
        #     #     tf_master_dict.removePOLocations(tf_master_dict.catalog)
        # if is_json:
        #     tf_master_dict.updateFromJSON(self.tran_file)

        home = os.environ['HOME']
        pot_file = os.path.join(home, 'blender_manual.pot')
        pot_data = c.load_po(pot_file)
        pot_m: Message = None
        dict_m: Message = None
        changed = False
        new_list=[]
        for pot_m in pot_data:
            pot_id = pot_m.id
            is_in_orig = (pot_id in tf_master_dict.catalog)
            if not is_in_orig:
                print(f'NEW: {pot_m}')
            else:
                dict_m = tf_master_dict.catalog[pot_id]
                dict_m.flags = pot_m.flags
                dict_m.context = pot_m.context
                dict_m.auto_comments = pot_m.auto_comments
                dict_m.user_comments = pot_m.user_comments
                dict_m.locations = pot_m.locations
                print(f'UPDATE: {dict_m}')
                changed = True

        for dict_m in tf_master_dict.catalog:
            is_changed = self.correctCases(dict_m)
            if is_changed:
                changed = True

        is_saving = (changed and bool(self.opo_path))
        if is_saving:
            tf_master_dict.saveData(tf_master_dict.catalog, self.opo_path)
        exit(0)

        changed = False
        new_tran: str = None
        new_dict = NoCaseDict()
        tf_master_dict = self.tf.master_dic_list
        is_po_data = isinstance(dict_list, Catalog)
        is_dict_data = isinstance(dict_list, dict)
        for entry in enumerate(dict_list):
            if is_po_data:
                m: Message = entry
                msgid = m.id
                msgstr = m.string
                msgctx = m.context
            elif is_dict_data:
                (msgid, msgstr) = entry
                msgctx = None

            tf_master_dict.update(dict_list)

        is_save = (bool(self.opo_path))
        if is_save:
            writeJSONDic(tf_master_dict, self.opo_path)
        exit(0)

        untranslated_dict = {}
        del_list = []
        for index, entry in enumerate(tf_master_dict.items()):
            (msgid, msgstr) = entry

            is_gui_entries = (msgid.endswith('&U'))
            if is_gui_entries:
                msgid = msgid[:-2]

            current_tran = msgstr
            # is_debug = ('Volume' == msgid)
            # if is_debug:
            #     print('Debug')
            is_none = (current_tran == None) or (len(current_tran) == 0)
            if is_none:
                msgstr = ""
                is_ignore = ig.isIgnored(msgid)
                if is_ignore:
                    msg = f'TRANSLATION is IGNORED:\nmsgid:[{msgid}]\nmsgstr:[{msgstr}]\n\n'
                    continue

            if self.filter_ignored:
                is_ignore = ig.isIgnored(msgid)
                if is_ignore:
                    continue

            using_external = (use_external_translation and dict_list is not None and len(dict_list) > 0)
            if using_external:
                has_new_tran = (msgid in dict_list)
                new_tran = (dict_list[msgid] if has_new_tran else None)
                has_tran = (new_tran is not None) and (len(new_tran) > 0)
                # if not has_tran:
                #     msg = f'msgid:"{msgid}"\nmsgstr:"{msgstr}"\n\n'
            else:
                continue
                # new_tran = self.tf.isInDict(msgid)
                # has_tran = bool(new_tran) and (new_tran != msgstr)

            if not has_tran:
                continue

            is_same_tran = (msgstr == new_tran)
            if is_same_tran:
               continue


            # is_debug = ('Note/Layer to add annotation strokes to' in msgid)
            # if is_debug:
            #     print('Debug')

            # msg = f'msgid:"{msgid}"\nmsgstr:"{msgstr}"\nold_dict_tran:"{old_dict_tran}"\n\n'
            # print(msg)
            #
            # has_abbrev = bool(old_dict_tran) and (':abbr:' in old_dict_tran)
            # if not has_abbrev:
            #     continue
            #
            # has_slash = bool(old_dict_tran) and (UpdateDict.slash in old_dict_tran)
            # if not has_slash:
            #     continue
            #
            # id_overall_slash_count = (msgid.count(UpdateDict.slash))
            # id_abbrev_slash_count = self.countSlashInAbbrevs(msgid)
            # id_remain_slash = (id_overall_slash_count - id_abbrev_slash_count)
            #
            # old_tran_overall_slash_count = (old_dict_tran.count(UpdateDict.slash))
            # old_tran_abbrev_slash_count = self.countSlashInAbbrevs(old_dict_tran)
            # old_tran_abbrev_remain_slash = (old_tran_overall_slash_count - old_tran_abbrev_slash_count)
            # # old_tran_has_slashes_but_all_are_in_abbrev = (old_tran_abbrev_remain_slash == old_tran_abbrev_slash_count)
            #
            # same_amount_of_slash = (id_remain_slash == old_tran_abbrev_remain_slash)
            # if same_amount_of_slash:
            #     continue
            #
            has_dash = (' -- ' in new_tran)
            if has_dash:
                word_list = new_tran.split(' -- ')
                new_tran = word_list[0]
                new_en = word_list[1]
                is_swapped = (msgid.lower() == new_tran.lower())
                if is_swapped:
                    new_en = word_list[0]
                    new_tran = word_list[1]

                is_repeated = (msgid in word_list)
                is_same_tran = (is_repeated) and (new_tran == msgstr)
                if is_same_tran:
                    continue

            has_slash = ('/' in new_tran)
            if has_slash:
                word_list = new_tran.split('/')
                all_matched = False
                for word in word_list:
                    all_matched = (True if word.lower() in current_tran.lower() else False)
                if all_matched:
                    continue

            current_tran_has_multiple_meanings = ("/" in current_tran)
            if current_tran_has_multiple_meanings:
                need_adding = (new_tran.lower() not in current_tran.lower())
                if need_adding:
                    new_tran = f'{new_tran}/{current_tran}'
                else:
                    continue

            update_entry = {msgid: new_tran}
            tf_master_dict.update(update_entry)
            changed = True

            r = POResultRecord(index + 1, msgid, new_tran, alternative_tran=msgstr, alternative_label="old_tran")
            self.append(r)
            #
            # changed = True

        if untranslated_dict:
            cat = Catalog()
            for msgid, msgstr in untranslated_dict.items():
                cat.add(msgid)
            home = os.environ['HOME']
            path = os.path.join(home, "untran.po")
            c.dump_po(path, cat)

        if del_list:
            for msgid in del_list:
                del tf_master_dict[msgid]

        is_save = (changed and bool(self.opo_path))
        if is_save:
            writeJSONDic(tf_master_dict, self.opo_path)
        else:
            self.showResult()