import os
from babel.messages.catalog import Catalog, Message
from sphinx_intl import catalog as c
from potask_base import POTaskBase, POResultRecord
from translation_finder import TranslationFinder
from nocasedict import NoCaseDict
from paragraph import Paragraph as PR
from ignore import Ignore as ig

class SwapGlossaryTranslationEntries(POTaskBase):
    def __init__(self,
                 output_to_file=None,
                 translation_file=None
                 ):
        POTaskBase.__init__(
                self,
                output_to_file=output_to_file, # file to write the output to, while testing
                translation_file=translation_file # file blender_manual.po in locale/vi/LC_MESSAGES
        )
# manual/glossary/index.rst

    def performTask(self):
        self.setFiles()
        home = os.environ['BLENDER_MAN_EN']
        default_tran_file = os.path.join(home, 'locale/vi/LC_MESSAGES/blender_manual.po')
        if not bool(self.tran_file):
            self.tran_file = default_tran_file

        changed = False
        glossary_entry = 'manual/glossary/index.rst'
        # glossary_entry = 'manual/about/contribute/build.rst'
        m: Message = None
        tran_file_data = c.load_po(self.tran_file)
        for index, m in enumerate(tran_file_data):
            is_first_record = (index == 0)
            if is_first_record:
                continue

            auto_comment = m.auto_comments
            user_comment = m.user_comments
            locations = m.locations
            is_glossary = self.findInList(glossary_entry, locations)
            if not is_glossary:
                continue

            msgid = m.id
            msgstr = m.string

            is_debug = ('Z-buffer' == msgid)
            if is_debug:
                print('Debug')

            is_heading = (msgid == 'Glossary')
            if is_heading:
                continue

            is_term = (' -- ' in msgstr)
            if not is_term:
                continue

            msgstr_list_part = msgstr.split(' -- ')
            is_translated = len(msgstr_list_part) > 1
            if not is_translated:
                continue

            is_translation = ('.' in msgstr)
            if is_translation:
                continue

            vn = msgstr_list_part[0]
            en = msgstr_list_part[1]

            is_term = (en.lower() == msgid.lower())
            if not is_term:
                continue

            # orig_msg = f'msgid:{msgid}\nmsgstr:{msgstr}\n'
            # msg = orig_msg + f'en:{en} vn:{vn}\n\n'
            # print(msg)

            new_msgstr = f'{en} -- {vn}'
            m.string = new_msgstr
            changed = True

            r = POResultRecord(index + 1, msgid, new_msgstr)
            self.append(r)

        is_save = (changed) and (self.opo_path)
        if is_save:
            print(f'FAKING dumping po data to: {self.opo_path}')
            # c.dump_po(self.opo_path, tran_file_data)
        else:
            self.showResult()
