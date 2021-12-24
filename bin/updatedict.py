import os
from sphinx_intl import catalog as c
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
        new_dict = NoCaseDict()
        tf_master_dict = self.tf.master_dic_list
        for index, entry in enumerate(tf_master_dict.items()):
            (msgid, msgstr) = entry

            # is_debug = ('Volume' == msgid)
            # if is_debug:
            #     print('Debug')

            new_tran = (dict_list[msgid] if msgid in dict_list else "")
            has_tran = bool(new_tran)
            if not has_tran:
                msg = f'msgid:"{msgid}"\nmsgstr:"{msgstr}"\n\n'

            new_entry = {msgid: new_tran}
            new_dict.update(new_entry)
            changed = True
            # if self.filter_ignored:
            #     is_ignore = ig.isIgnored(msgid)
            #     if is_ignore:
            #         continue
            #
            # # is_in_old_dict = (msgid in tf_master_dict)
            # old_dict_tran = self.tf.isInDict(msgid)
            # is_same_tran = (old_dict_tran == msgstr)
            # if is_same_tran:
            #    continue
            #
            # is_debug = ('Note/Layer to add annotation strokes to' in msgid)
            # if is_debug:
            #     print('Debug')
            #
            # # msg = f'msgid:"{msgid}"\nmsgstr:"{msgstr}"\nold_dict_tran:"{old_dict_tran}"\n\n'
            # # print(msg)
            # #
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
            # update_entry = {msgid: msgstr}
            # tf_master_dict.update(update_entry)
            #
            # r = POResultRecord(index + 1, msgid, msgstr, alternative_tran=old_dict_tran, alternative_label="old_tran")
            # self.append(r)
            #
            # changed = True

        is_save = (changed and bool(self.opo_path))
        if is_save:
            writeJSONDic(new_dict, self.opo_path)
        else:
            self.showResult()