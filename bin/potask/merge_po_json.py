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

    def filteringLowerCaseSet(self):
        home = os.environ['HOME']
        home_github = os.path.join(home, 'Dev/tran/blender_manual')
        home_po = os.path.join(home, 'Dev/tran/blender_ui')
        input_po = os.path.join(home_github, 'ref_dict_0001.po')
        output_po = os.path.join(home_github, 'ref_dict_0002.po')

        data = c.load_po(input_po)
        lower_set = Catalog(
            project="Blender 3.0.0 Release Candidate (b'd2e608733507'",
            locale="vi",
            last_translator="Hoang Duy Tran <hoangduytran1960@googlemail.com>",
            language_team="London, UK <hoangduytran1960@gmail.com>"
        )

        other_set = Catalog(
            project="Blender 3.0.0 Release Candidate (b'd2e608733507'",
            locale="vi",
            last_translator="Hoang Duy Tran <hoangduytran1960@googlemail.com>",
            language_team="London, UK <hoangduytran1960@gmail.com>"
        )

        for m in data:
            msgid: str = m.id
            is_lower = msgid.islower()
            set_to_use = (lower_set if is_lower else other_set)
            set_to_use.add(msgid,
                       string=m.string,
                       locations=m.locations,
                       flags=m.flags,
                       auto_comments=m.auto_comments,
                       user_comments=m.user_comments,
                       previous_id=m.previous_id,
                       lineno=m.lineno,
                       context=m.context
                       )
        msg = f'lowerset contains {len(lower_set)} other_set contains: {len(other_set)}'
        print(msg)
        removed_count=0
        for m in other_set:
            msgid: str = (m.id.lower())
            is_in_lower_set = (msgid in lower_set)
            if is_in_lower_set:
                removed_count+=1
                del lower_set[msgid]

        for m in lower_set:
            other_set.add(m.id,
                       string=m.string,
                       locations=m.locations,
                       flags=m.flags,
                       auto_comments=m.auto_comments,
                       user_comments=m.user_comments,
                       previous_id=m.previous_id,
                       lineno=m.lineno,
                       context=m.context
                       )

        msg = f'AFTER FILTERING LOWERCASE: lowerset contains {len(lower_set)} other_set contains: {len(other_set)}, removed: {removed_count}'
        print(msg)
        print(f'writing: {output_po} with {len(other_set)} records:')
        c.dump_po(output_po, other_set)
        exit(0)

    def highlight_comment_diff(self):
        home = os.environ['HOME']
        in_pot = os.path.join(home, '20220116_blender_manual_0001.po')
        ref_po = os.path.join(home, 'blender_manual.pot')

        m: Message = None
        ref_m: Message = None
        ref_data = c.load_po(ref_po)
        in_data = c.load_po(in_pot)
        changed = False
        for index, m in enumerate(in_data):
            is_first = (index == 0)
            if is_first:
                continue
            msgid = m.id
            is_in_ref = (msgid in ref_data)
            if not is_in_ref:
                continue

            ref_m = ref_data[msgid]
            ref_locations = ref_m.locations
            m_locations = m.locations
            is_loc_diff = (m_locations != ref_locations)
            if not is_loc_diff:
                continue

            msgstr = m.string
            msg = f'msgid "{msgid}"\nmsgstr "{msgstr}"\n---------\n\n'
            print(msg)
        exit(0)

    def correctLocations(self):
        home = os.environ['HOME']
        out_po = os.path.join(home, '20220115_blender_manual_flat_0003.po')
        in_pot = os.path.join(home, '20220115_blender_manual_0002.po')
        ref_po = os.path.join(home, 'blender_manual.pot')

        m: Message = None
        ref_m: Message = None
        ref_data = c.load_po(ref_po)
        in_data = c.load_po(in_pot)
        changed = False

        for index, m in enumerate(in_data):
            is_first = (index == 0)
            if is_first:
                continue
            msgid = m.id
            is_in_ref = (msgid in ref_data)
            if not is_in_ref:
                msg = f'NOT IN REF: {msgid}'
                print(msg)
                continue

            ref_m = ref_data[msgid]
            ref_locations = ref_m.locations
            m_locations = m.locations
            is_loc_diff = (m_locations != ref_locations)
            if not is_loc_diff:
                continue

            m.locations = ref_locations
            changed = True

        if changed:
            msg = f'writing: [{len(in_data)}] to file: [{out_po}]'
            print(msg)
            c.dump_po(out_po, in_data)
        exit(0)

    def mergePOT(self):
        home = os.environ['HOME']
        home_github = os.path.join(home, 'Dev/tran/blender_manual')
        # out_po = os.path.join(home, '20220115_blender_manual_flat_0001.po')
        out_po = os.path.join(home, 'blender_manual_flat.po')
        # in_pot = os.path.join(home, 'blender_manual.pot')
        in_pot = os.path.join(home, '20220115_blender_manual_flat.po')
        # ref_po = os.path.join(home_github, '20220114_merge_blender_manual.po')
        # ref_po = os.path.join(home, '20220115_merge_blender_manual_flat.po')
        ref_po = os.path.join(home, 'blender_manual.pot')

        m: Message = None
        ref_data = c.load_po(ref_po)
        in_data = c.load_po(in_pot)
        changed = False
        for index, m in enumerate(in_data):
            is_first = (index == 0)
            if is_first:
                continue
            msgid = m.id
            is_in_ref = (msgid in ref_data)
            if not is_in_ref:
                msg = f'NOT IN REF: {msgid}'
                print(msg)
                continue

            msgstr = ref_data[msgid]
            msg = f'[{msgid}] => [{msgstr}]'
            print(msg)
            m.string = msgstr
            changed = True

        if changed:
            msg = f'writing: [{len(in_data)}] to file: [{out_po}]'
            print(msg)
            c.dump_po(out_po, in_data)

        exit(0)

    def performTask(self):

        # self.mergePOT()
        # self.correctLocations()
        self.highlight_comment_diff()

        # self.filteringLowerCaseSet()

        home = os.environ['HOME']
        home_github = os.path.join(home, 'Dev/tran/blender_manual')
        home_po = os.path.join(home, 'Dev/tran/blender_ui')
        # target_po = os.path.join(home, 'ref_dict_0001.po')
        target_po = os.path.join(home_github, 'ref_dict_ss_0001.po')

        po_file_list = [
            # os.path.join(home_po, '2.79b/vi.po'),
            # os.path.join(home_po, '2.83/vi.po'),
            # os.path.join(home_po, '3x/vi.po'),
            # os.path.join(home_github, 'ref_dict_0006_0010.json')
            # os.path.join(home_github, 'ref_dict_ss_0001.json')
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
