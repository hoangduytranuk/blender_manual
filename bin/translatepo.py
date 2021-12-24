import os
from sphinx_intl import catalog as c
from potask_base import POTaskBase, POResultRecord
from translation_finder import TranslationFinder
from nocasedict import NoCaseDict
from paragraph import Paragraph as PR
from ignore import Ignore as ig

class TranslatePO(POTaskBase):
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
            dict_list = {}
            tran_data = c.load_po(self.tran_file)
            for index, m in enumerate(tran_data):
                is_first = (index == 0)
                if is_first:
                    continue

                tran_id = m.id
                lower_tran_id = tran_id.lower()
                tran_ctx = m.context
                tran_txt = m.string

                k = (lower_tran_id, tran_ctx)
                entry={k: tran_txt}
                dict_list.update(entry)
            return dict_list
        except Exception as e:
            print(e)
            raise e

    def checkTranslation(self, orig_txt):
        tran = self.tf.isInDict(orig_txt)
        return (orig_txt, tran)

    # def isDiffCases(self, msgid, msgstr, dict_tran=None):

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

    # -s -f /Users/hoangduytran/bin -p "this" -ext ".xml"
    # -f /Users/hoangduytran/Dev/tran/blender_ui/2.79b/vi.po -tr -tran /Users/hoangduytran/test_283_no_abbrev_space_dot.po -fuz -o /Users/hoangduytran/retran_279b.po
    # -rpl -f /Users/hoangduytran/test_283_no_abbrev_space_dot.po -of /Users/hoangduytran/test_283_20211217.po
    #  -f /Users/hoangduytran/test_283_no_abbrev_space_dot.po -tr -fuz -o /Users/hoangduytran/retran_283.po
    # -f /Users/hoangduytran/retran_283.po -tr -fuz -o /Users/hoangduytran/retran_283_0001.po
    def performTask(self):
        self.setFiles()
        msg_data = c.load_po(self.po_path)

        self.tf = TranslationFinder(
            apply_case_matching_orig_txt=self.apply_case_matching_orig_txt
        )
        dict_list = None
        use_external_translation = (self.tran_file is not None) and (os.path.isfile(self.tran_file))
        if use_external_translation:
            dict_list = self.loadDictFromFile()

        changed = False
        # checkAndRemoveTranslated()
        for index, m in enumerate(msg_data):

            is_first_record = (index == 0)
            if is_first_record:
                continue

            if self.filter_ignored:
                is_ignore = ig.isIgnored(m.id)
                if is_ignore:
                    continue

            is_fuzzy = m.fuzzy
            msgid = m.id
            msgstr = m.string
            ctx = m.context

            # is_debug = ("Target Range" in msgid)
            # if is_debug:
            #     print('Debug')
            # is_not_emtpy = bool(msgstr)
            # is_not_fuzzy = (not is_fuzzy)
            # is_translated = (is_not_emtpy and is_not_fuzzy)
            # if is_translated:
            #     continue

            dict_tran = None
            key = (msgid, ctx)
            if dict_list:
                has_tran = (key in dict_list)
                dict_tran = (dict_list[key] if has_tran else None)
            else:
                pr = PR(msgid, translation_engine=self.tf)
                pr.translateAsIs()
                dict_tran = pr.getTranslation()

            has_tran = bool(dict_tran)
            if not has_tran:
                continue

            is_same = (msgid == dict_tran) or (msgstr == dict_tran)
            if is_same:
                continue

            # is_id_lower =
            msg = f'msgid:[{msgid}]\ndict:[{dict_tran}]\ncurrent:[{msgstr}]\n\n'
            print(msg)

            m.string = dict_tran

            set_fuzzy = (self.set_translation_fuzzy and not is_fuzzy)
            if set_fuzzy:
                m.flags.add('fuzzy')

            changed = True
            r = POResultRecord(index + 1, m.id, m.string)
            self.append(r)

        is_save = (changed) and (self.opo_path)
        if is_save:
            c.dump_po(self.opo_path, msg_data)
        else:
            self.showResult()



# -s -dmid -mstr -p "Delta" -of /Users/hoangduytran/test_0001.po

