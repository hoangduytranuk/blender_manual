#!/usr/bin/env python3
import sys
sys.path.append("/home/htran/bin/python/PO")
from action import TwoDocumentAction

class DiffTwoDocumentAction(TwoDocumentAction):
    def __init__(self):
        self.from_doc_dic = None

    def run(self):
        has_from_doc = has_to_doc = False
        from_text_body = to_text_body = None

        has_to_doc = (self.to_doc != None)
        if (has_to_doc):
            #rough compare
            if (has_from_doc):
                from_text_body = self.from_doc.getTextWithIDFlat();
                to_text_body = self.from_doc.getTextWithIDFlat();
                is_diff = (from_text_body != to_text_body)
                if (not is_diff):
                    #print("Identical body text:\n{}\n{}".format(self.from_doc.path, self.to_doc.path))
                    return
                else:
                    print("DIFF:\n{}\n{}".format(self.from_doc.path, self.to_doc.path))

                if (self.is_compare_only):
                    return

            has_from_doc = ((self.from_doc != None) and (self.from_doc_dic == None))
            if (has_from_doc):
                self.from_doc_dic = self.from_doc.getDictionaryWithMSGIDAsKey()

            for(index, to_text_block) in enumerate(self.to_doc.block_list):
                is_first_block = (index == 0)
                if (is_first_block): continue

                from_text_block = None
                if (has_from_doc):
                    from_text_block = self.from_doc_dic[to_text_block.msgid.flatText()]
                    is_found = (from_text_block != None)
                    if (not is_found):
                        print("Entry NOT in: {}\n".format(to_text_block.getTextWithID()))
                        continue

                self.callback.setArgs(from_text_block, to_text_block)
                self.callback.run()
