import re
#sys.path.append("/home/htran/.local/lib/python3.6/site-packages")
#import os

#from sphinx_intl import catalog as c
from functionbase import FunctionBase
#from babel.messages.catalog import Message

#print("dir(c):{}".format(dir(c)))
#exit(0)

class ReplaceTranslation(FunctionBase):
    dic = {
        'Chỉ Mục của Lượt':'Chỉ Số Lượt',
        'Chỉ mục của lượt':'Chỉ số lượt',
        'chỉ mục của lượt':'chỉ số lượt',
        }

    def replaceUsingDic(self, text) -> bool:
        occ = 0
        new_text = text
        for t,v in ReplaceTranslation.dic.items():
           new_text, rep_occ = re.subn(t,v, new_text)
           occ += rep_occ
        return [new_text, occ]

    def run(self):
        old_string = None
        for m in self.pofileCategory:
            old_string = str(m.string)
            new_string, count = self.replaceUsingDic(old_string)
            m.string = new_string
            self.changed = (count > 0)
            if (self.changed):
                print("m.string changed:{} => {}: File:{}".format(old_string, m.string, self.fileName))
