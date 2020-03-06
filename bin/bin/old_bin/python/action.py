from basefileio import BaseFileIO
from common import Common
from podocument import Document, TextBlock, TextBlockComponent

class DocumentAction:
    def __init__(self):
        self.from_doc: Document = None
        self.callback: object = None

    def setArgs(self, from_doc):
        self.from_doc : Document = from_doc

    def setCallBack(self, callback : object):
        self.callback  = callback

    def run(self):
        pass


class BasicDocumentAction(DocumentAction):
    def run(self):
        for(index, text_block) in enumerate(self.from_doc.block_list):
            is_first_block = (index == 0)
            if (is_first_block): continue

            self.callback.setArgs(text_block)
            self.callback.run()


class TwoDocumentAction:
    def __init__(self):
        self.from_doc : Document = None
        self.to_doc : Document = None
        self.callback : object = None
        self.is_compare_only:bool = False

    def setCompareOnly(self, is_compare_only):
        self.is_compare_only = is_compare_only

    def setArgs(self, from_doc : Document, to_doc : Document):
        self.from_doc = from_doc
        self.to_doc = to_doc

    def setCallBack(self, callback : object):
        self.callback = callback

    def run(self):
        pass


class BasicTwoDocumentAction(TwoDocumentAction):
    def __init__(self):
        self.to_doc_sorted : Document = None

    def run(self):
        if (self.to_doc_sorted == None):
            self.to_doc_sorted = self.to_doc.clone()
            self.to_doc_sorted.sortDocumentInMSGID()
            #print(self.to_doc_sorted)


        for(index, from_text_block) in enumerate(self.from_doc.block_list):
            is_first_block = (index == 0)
            if (is_first_block): continue

            to_text_block = self.to_doc_sorted.binarySearchMSGID(from_text_block)
            is_found = (to_text_block != None)
            if (not is_found):
                continue

            self.callback.setArgs(from_text_block, to_text_block)
            self.callback.run()


class TransferTextBlockAction:
    def __init__(self):
        self.from_block = None
        self.to_block = None
        self.callback = None

    def setArgs(self, from_block, to_block):
        self.from_block = from_block
        self.to_block = to_block

    def run(self):
        pass



class TransferComponents(TransferTextBlockAction):

    ignore_items = [
            'Blender',
            'ID',
            'OpenCL',
            'Gamma',
            'Alpha',
            'Z',
            'X',
            'Y',
            'UV',
            'Catmull-Rom',
            'Mitch',
            'Laplace',
            'Sobel',
            'Prewitt',
            'Kirsch',
            'DPI',
            'Iris',
            'Targa',
        ]

    def isDiffComment(self):
        is_diff = (self.from_block.comment.flatText() != self.to_block.comment.flatText())
        return is_diff

    def isDiffMsgid(self):
        is_diff = (self.from_block.msgid.flatText() != self.to_block.msgid.flatText())
        return is_diff

    def isDiffMsgstr(self):
        is_diff = (self.from_block.msgstr.flatText() != self.to_block.msgstr.flatText())
        return is_diff

    def run(self):
        is_wrong_block = (self.to_block.index == 0) or (self.from_block.index == 0)
        if (is_wrong_block): return

        id_copy_list = [Common.COMMENT, Common.MSGCTXT, Common.MSGID]

        is_changed = (self.isDiffComment() or self.isDiffMsgid())
        if (is_changed):
            self.to_block.copyContent(self.from_block, id_copy_list)

        is_to_blank_msgstr = (self.to_block.msgstr.isEmpty())
        is_from_msgstr_has_text = (self.from_block.msgstr.len() > 0)
        is_changed = (is_to_blank_msgstr and is_from_msgstr_has_text)
        if (is_changed):
            self.to_block.msgstr.copyContent(self.from_block.msgstr)

        if (is_changed):
            self.to_block.document.printTitleOnce()
            self.to_block.document.setDirty()
            print("self.to_block.msgstr:\n{}\n\n".format(self.to_block.getTextWithID()))

