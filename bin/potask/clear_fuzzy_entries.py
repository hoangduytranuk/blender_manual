import os
from babel.messages.catalog import Catalog, Message
from sphinx_intl import catalog as c
from potask_base import POTaskBase, POResultRecord
from translation_finder import TranslationFinder
from nocasedict import NoCaseDict
from paragraph import Paragraph as PR
from ignore import Ignore as ig

class ClearFuzzyEntries(POTaskBase):
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
        m: Message = None
        tran_file_data = c.load_po(self.tran_file)
        for index, m in enumerate(tran_file_data):
            is_first_record = (index == 0)
            if is_first_record:
                continue

            auto_comment = m.auto_comments
            user_comment = m.user_comments
            locations = m.locations
            msgid = m.id
            is_fuzzy = m.fuzzy
            msgstr = m.string

            is_debug = ('Intersect Curves' == msgid)
            if is_debug:
                print('Debug')

            if not is_fuzzy:
                continue

            m.string = ""
            m.flags.remove('fuzzy')
            changed = True

            r = POResultRecord(index + 1, msgid, m.string, alternative_tran=msgstr, alternative_label="old_translation:")
            self.append(r)

        is_save = (changed) and (self.opo_path)
        if is_save:
            print(f'dumping po data to: {self.opo_path}')
            c.dump_po(self.opo_path, tran_file_data)
        else:
            self.showResult()

# -swap -of /Users/hoangduytran/new_blender_manual.po