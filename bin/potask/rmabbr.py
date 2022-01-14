from sphinx_intl import catalog as c
from potask_base import POTaskBase, POResultRecord
from ignore import Ignore as ig
from definition import Definitions as df
from common import Common as cm

class RemoveAbbr(POTaskBase):
    def __init__(self,
                 input_file=None,
                 output_to_file=None
                 ):
        POTaskBase.__init__(
                self,
                input_file=input_file,
                output_to_file=output_to_file
        )
        self.tf = None

    # def replaceTranslationsFromFile(self, tf: TranslationFinder):
    #     try:
    #         tran_data = c.load_po(self.tran_file)
    #         dict_ptr: NoCaseDict = tf.master_dic_list
    #
    #         for index, m in enumerate(tran_data):
    #             is_first = (index == 0)
    #             if is_first:
    #                 continue
    #
    #             tran_id = m.id
    #             lower_tran_id = tran_id.lower()
    #             tran_txt = m.string
    #
    #             has_tran = bool(tran_txt) and (len(tran_txt) > 0)
    #             if not has_tran:
    #                 continue
    #
    #             entry={lower_tran_id: tran_txt}
    #             dict_ptr.update(entry)
    #
    #     except Exception as e:
    #         print(e)
    #         raise e
    #
    # def checkTranslation(self, orig_txt):
    #     tran = self.tf.isInDict(orig_txt)
    #     return (orig_txt, tran)
    #
    # def checkAndRemoveTranslated(self):
    #     tran_list = list(map(self.checkTranslation, t_list))
    #     remove_list = []
    #     keep_list = []
    #     for (orig_txt, tran) in tran_list:
    #         if tran:
    #             remove_list.append(orig_txt)
    #         else:
    #             keep_list.append(orig_txt)
    #     print(f'removed: [{len(remove_list)}]')
    #     for txt in keep_list:
    #         msg = f'"{txt}",'
    #         print(msg)


    def performTask(self):
        self.setFiles()
        abbrev_pattern = df.ABBREV_PATTERN_PARSER

        msg_data = c.load_po(self.po_path)

        # self.tf = TranslationFinder()
        # use_external_translation = (self.tran_file is not None) and (os.path.isfile(self.tran_file))
        # if use_external_translation:
        #     self.replaceTranslationsFromFile(self.tf)

        changed = False
        # checkAndRemoveTranslated()
        for index, m in enumerate(msg_data):
            is_first_record = (index == 0)
            if is_first_record:
                continue

            if self.filter_ignored:
                is_ignored = (ig.isIgnored(msgid, is_debug=False))
                if is_ignored:
                    continue

            msgid = m.id
            msgstr = m.string
            abbrev_match = abbrev_pattern.search(msgstr)
            has_abbrev = (abbrev_match is not None)
            if not has_abbrev:
                continue

            new_msgstr = cm.removeAbbr(msgstr)
            if not new_msgstr:
                continue

            m.string = new_msgstr
            r = POResultRecord(index+1, msgid, new_msgstr)
            self.append(r)

            changed = True

        is_save = (changed) and (self.opo_path)
        if is_save:
            c.dump_po(self.opo_path, msg_data)
        else:
            self.showResult()



# -s -dmid -mstr -p "Delta" -of /Users/hoangduytran/test_0001.po

