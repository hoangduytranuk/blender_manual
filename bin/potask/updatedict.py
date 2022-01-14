import os
from sphinx_intl import catalog as c
from babel.messages import Catalog, Message
from potask_base import POTaskBase, POResultRecord, writeJSONDic, loadJSONDic
from translation_finder import TranslationFinder
from nocasedict import NoCaseDict
from paragraph import Paragraph as PR
from ignore import Ignore as ig
from definition import Definitions as df
import pathlib as PL

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

    def loadDictFromFile(self):
        try:
            ext = PL.Path(self.tran_file).suffix
            ext_lower = ext.lower()
            is_json = (ext_lower == '.json')
            is_po = (ext_lower == '.po')

            dict_list = NoCaseDict()
            if is_json:
                tran_data = loadJSONDic(self.tran_file)
                dict_list.update(tran_data)
            else:
                tran_data = c.load_po(self.tran_file)
                for index, m in enumerate(tran_data):
                    is_first = (index == 0)
                    if is_first:
                        continue

                    tran_id = m.id
                    tran_ctx = m.context
                    tran_txt = m.string

                    # k = (lower_tran_id, tran_ctx)
                    entry={tran_id: tran_txt}
                    dict_list.update(entry)
            return dict_list
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

    # -updict -tran /Users/hoangduytran/Dev/tran/blender_ui/merged.po -ig -cl
    def performTask(self):
        # self.setFiles()
        # msg_data = c.load_po(self.po_path)

        self.tf = TranslationFinder(
            apply_case_matching_orig_txt=self.apply_case_matching_orig_txt
        )
        dict_list = None
        use_external_translation = (self.tran_file is not None) and (os.path.isfile(self.tran_file))
        if use_external_translation:
            dict_list = self.loadDictFromFile()


        changed = False
        new_tran: str = None
        new_dict = NoCaseDict()
        tf_master_dict = self.tf.master_dic_list
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