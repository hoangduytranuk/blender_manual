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

    def replaceTranslationsFromFile(self, tf: TranslationFinder):
        try:
            dict_list = []
            tran_data = c.load_po(self.tran_file)
            for index, m in enumerate(tran_data):
                is_first = (index == 0)
                if is_first:
                    continue

                tran_id = m.id
                lower_tran_id = tran_id.lower()
                tran_ctx = m.context
                tran_txt = m.string

                entry=((lower_tran_id, tran_ctx), tran_txt)
                dict_list.append(entry)
            dict_list.sort()

            dict_ptr: NoCaseDict = tf.master_dic_list
            dict_ptr.clear()
            dict_ptr.update(dict_list)

        except Exception as e:
            print(e)
            raise e

    def checkTranslation(self, orig_txt):
        tran = self.tf.isInDict(orig_txt)
        return (orig_txt, tran)

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
    def performTask(self):
        self.setFiles()
        msg_data = c.load_po(self.po_path)

        self.tf = TranslationFinder(
            apply_case_matching_orig_txt=self.apply_case_matching_orig_txt
        )
        use_external_translation = (self.tran_file is not None) and (os.path.isfile(self.tran_file))
        if use_external_translation:
            self.replaceTranslationsFromFile(self.tf)

        ignore_words = ['Volume']
        changed = False
        # checkAndRemoveTranslated()
        for index, m in enumerate(msg_data):
            is_first_record = (index == 0)
            if is_first_record:
                continue

            # is_ignore = ig.isIgnored(m.id) or (m.id in ignore_words)
            # if is_ignore:
            #     continue

            is_fuzzy = m.fuzzy
            msgid = m.id
            msgstr = m.string
            ctx = m.context

            key = (msgid, ctx)
            pr = PR(key, translation_engine=self.tf)
            pr.translateAsIs()
            dict_tran = pr.getTranslation()
            if not dict_tran:
                continue

            is_diff = (msgstr != dict_tran)
            if is_diff:
                msg = f'msgid:[{msgid}]\ndict:[{dict_tran}]\ncurrent:[{msgstr}]\n\n'
                print(msg)

            if not is_diff:
                continue

            m.string = dict_tran
            #
            # is_empty = (not m.string) or (len(m.string) == 0)
            # is_translate = (is_fuzzy or is_empty)
            #
            # if not is_translate:
            #     continue
            #
            #
            # is_same = (output == m.id)
            # if is_same:
            #     continue
            #
            set_fuzzy = (self.set_translation_fuzzy and not is_fuzzy)
            if set_fuzzy:
                m.flags.add('fuzzy')
            #
            # m.string = output
            changed = True

            r = POResultRecord(index + 1, m.id, m.string)
            self.append(r)

        is_save = (changed) and (self.opo_path)
        if is_save:
            c.dump_po(self.opo_path, msg_data)
        else:
            self.showResult()



# -s -dmid -mstr -p "Delta" -of /Users/hoangduytran/test_0001.po

