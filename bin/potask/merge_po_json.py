import os
from sphinx_intl import catalog as c
from babel.messages import Catalog, Message
from potask_base import POTaskBase, loadJSONDic
import pathlib as PL
import time

class MergeToPO(POTaskBase):
    slash = '/'
    def __init__(self,
                 input_file=None,
                 output_to_file=None,
                 ):
        POTaskBase.__init__(
                self,
                input_file=input_file,
                output_to_file=output_to_file,
        )
        self.tf = None
        self.catalog: Catalog = None

    def JSonToPOCat(self, json_file):
        data = loadJSONDic(json_file)
        new_cat = Catalog(locale='vi', last_translator='Hoang Duy Tran <hoangduytran1960@googlemail.com>')
        mess: Message = None
        for (key, value) in data.items():
            new_cat.add(key, string=value)
        return new_cat

    def loadDictFromFile(self):
        try:
            ext = PL.Path(self.tran_file).suffix
            ext_lower = ext.lower()
            is_json = (ext_lower == '.json')
            is_po = (ext_lower == '.po')

            if is_json:
                tran_data = loadJSONDic(self.tran_file)
            else:
                tran_data = c.load_po(self.tran_file)
            return tran_data, is_po, is_json
        except Exception as e:
            print(e)
            raise e

    # -updict -tran /Users/hoangduytran/Dev/tran/blender_ui/merged.po -ig -cl
    # -updict -tran /Users/hoangduytran/untran.po -fuz -cl
    #  -mergepo
    def performTask(self):
        home = os.environ['HOME']
        home_github = os.path.join(home, 'Dev/tran/blender_manual')
        home_po = os.path.join(home, 'Dev/tran/blender_ui')
        target_po = os.path.join(home, 'ref_dict_0001.po')

        po_file_list = [
            os.path.join(home_po, '2.79b/vi.po'),
            os.path.join(home_po, '2.83/vi.po'),
            os.path.join(home_po, '3x/vi.po'),
            os.path.join(home_github, 'ref_dict_0006_0010.json')
        ]

        po_cat: Catalog = None
        for pof in po_file_list:
            is_json = (pof.endswith('.json'))
            if is_json:
                tran_data = self.JSonToPOCat(pof)
            else:
                tran_data = c.load_po(pof)

            init_po_cat = (po_cat is None)
            if init_po_cat:
                po_cat = tran_data
            else:
                m: Message = None
                for m in tran_data:
                    new_msgid: str = m.id
                    has_ampersand_u = (new_msgid.endswith('&U'))
                    if has_ampersand_u:
                        new_msgid = new_msgid[:-2]

                    new_msgstr = m.string
                    is_in = (new_msgid in po_cat)
                    if not is_in:
                        # add(self, id, string=None, locations=(), flags=(), auto_comments=(),
                        #     user_comments=(), previous_id=(), lineno=None, context=None):
                        po_cat.add(new_msgid,
                                   string=new_msgstr,
                                   locations=m.locations,
                                   flags=m.flags,
                                   auto_comments=m.auto_comments,
                                   user_comments=m.user_comments,
                                   previous_id=m.previous_id,
                                   lineno=m.lineno,
                                   context=m.context
                                   )
                        continue
                    else:
                        current_m: Message = po_cat[new_msgid]
                        current_msgstr = current_m.string
                        msg = f'msgid: [{new_msgid}]\n'
                        msg += f'current_msgstr: [{current_msgstr}];\nnew_msgstr: [{new_msgstr}]\n'
                        is_translation_diff = (current_msgstr != new_msgstr)
                        if not is_translation_diff:
                            continue

                        del po_cat[new_msgid]
                        po_cat.add(new_msgid,
                                   string=new_msgstr,
                                   locations=m.locations,
                                   flags=m.flags,
                                   auto_comments=m.auto_comments,
                                   user_comments=m.user_comments,
                                   previous_id=m.previous_id,
                                   lineno=m.lineno,
                                   context=m.context
                                   )
                print(f'merging: {pof}')
                print(f'writing: {target_po} with {len(po_cat)} records:')
                c.dump_po(target_po, po_cat)

        # for file in file_list:
        #     self.tran_file = file
        #     one_cat, is_po, is_json = self.loadDictFromFile()
        #     msg = f'file:[{file}] is loaded with {len(one_cat)} records, type is po:{is_po} json:{is_json}.'
        #     print(msg)
        #     is_init = (self.catalog is None)
        #     if is_init:
        #         self.catalog = one_cat
        #     else:
        #         msg = f'merging {len(self.catalog)} records with new_cat which has [{len(one_cat)}] records'
        #         print(msg)
        #         t1 = time.process_time()
        #         self.catalog.update(one_cat)
        #         t2 = time.process_time()
        #         elaps = t2 - t1
        #
        #         msg = f'FINISHED merging {len(self.catalog)} records, time taken: [{elaps}]'
        #         print(msg)
        #
        #
        #     msg = f'dumping {len(self.catalog)} records to po file [{target_po}]'
        #     print(msg)
        #     c.dump_po(target_po, self.catalog)
        #     msg = f'Finished dumping {len(self.catalog)} to po file [{target_po}]'
        #     print(msg)
