#!/usr/bin/python3 -d
import sys
sys.path.append('/home/htran/bin/python/base')
sys.path.append('/home/htran/bin/python/PO')

from basefileio import BaseFileIO
from podocument import Document
from pobase import POBasic
from argparse import ArgumentParser

class CheckChanges(BaseFileIO):
    def __init__(self):
        self.target_dir = None

    def Start(self, target_dir):
        self.target_dir = target_dir

    def transferText(self, left_doc_path, right_doc_path, is_save=False):
        left_doc = Document()
        left_doc.setPath(left_doc_path)

        right_doc = Document()
        right_doc.setPath(right_doc_path)

        left_doc.loadText()
        right_doc.loadText()

        #print("left_doc:\n{}\n".format(left_doc))
        #print("right_doc:\n{}\n".format(right_doc))
        for(index, from_text_block) in enumerate(left_doc.block_list):
            is_first_block = (index == 0)
            if (is_first_block): continue

            from_msgid = from_text_block.msgid
            from_msgid_text = from_msgid.flatText()
            from_msgstr = from_text_block.msgstr
            from_msgstr_text = from_msgstr.flatText()

            try:
                to_msgid = right_doc.block_list[index].msgid
                to_msgid_text = to_msgid.flatText()
                to_msgstr = right_doc.block_list[index].msgstr
                to_msgstr_text = to_msgstr.flatText()
            except:
                return

            #print("from_msgid: {}\nto_msgid{}\n".format(from_msgid_text, to_msgid_text))
            is_same_msgid = (from_msgid_text == to_msgid_text)
            if (is_same_msgid):
                #print("SAME MSGID: [{}] = [{}]".format(from_msgid_text, to_msgid_text))
                is_transfer = (len(to_msgstr_text) == 0) or (len(from_msgstr_text) == 0)
                if (is_transfer):
                    print("******* {} [{}]=> {} [{}]".format(from_msgid_text, from_msgstr_text, to_msgid_text, to_msgstr_text))
                #else:
                #    print("text has been translated: [{}]".format(to_msgstr_text))


    def findFuzzy(self, target_dir):
        po_base = POBasic(target_dir, False)
        target_dir_list = po_base.getSortedPOFileList()
        for(index, file_name) in enumerate(target_dir_list):
            target_text = self.readFile(file_name).split('\n\n', 1)[1]
            has_fuzzy = (target_text.find("#, fuzzy") >= 0)
            if (has_fuzzy):
                print("{}".format(file_name))



parser = ArgumentParser()
parser.add_argument("-d", "--dir", dest="target_dir", help="The PO directory from which PO files are search and find to see if they contain \'fuzzy\' markers. These fuzzy entries will need special attentions and removal of 'fuzzy' makers.")
args = parser.parse_args()

print("args: {}".format(args))

x = CheckChanges()
x.Start(args.target_dir)
x.findFuzzy(args.target_dir)

