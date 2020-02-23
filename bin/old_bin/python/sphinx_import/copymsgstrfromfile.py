from . import catalog as c
from functionbase import FunctionBase

class CopyMsgStrFromFile(FunctionBase):
    def setLocalVars(self):
        self.dic = {
                "toán tử":"thao tác",
                "Toán tử":"Thao tác",
                "Toán Tử":"Thao Tác",
                "Toán Tử":"Thao Tác",
            }
        self.from_file = "/home/htran/blender_documentations/new_po/vi.po"
        self.to_file = "/home/htran/blender_documentations/po/vi.po"
        self.from_dic = {}

        self.from_cat = c.load_po(self.from_file)
        self.to_cat = c.load_po(self.to_file)
        self.sortFrom()

    #def printCat(self, cat):
        #print("printCat:=============================")
        #for m in cat:
            #print("msgid \"{}\"".format(m.id))
            #print("msgstr \"{}\"".format(m.string))
            #print("")

    #def printDict(self, dic):
        #print("printDict:=============================")
        #for key, value in dic.items():
            #print("msgid \"{}\"".format(key))
            #print("msgstr \"{}\"".format(value))
            #print("")


    def sortFrom(self):
        for m in self.from_cat:
            key = m.id
            value = m
            self.from_dic.update({key:value})

    def replaceFromDic(self, msgstr):
        new_msgstr = str(msgstr)
        for key, m in self.dic.items():
            msgstr = m.string
            new_msgstr = new_msgstr.replace(key, msgstr)

        return new_msgstr

    def run(self):
        is_dirty = False
        #self.printCat(self.from_cat)
        #self.printDict(self.from_dic)
        #exit(0)

        for index, m in enumerate(self.to_cat):
            is_first_message = (index == 0)

            if (is_first_message):
                continue;

            is_found = (m.id in self.from_dic)
            if (not is_found):
                print("Unfound:{}=>{}".format(m.id, m.string))
                print("")
                continue

            from_m = self.from_dic[m.id]
            from_msgstr = from_m.string
            from_msgstr = self.replaceFromDic(from_msgstr)
            from_comment = from_m.user_comments

            print("old_comment:{} => {}".format(m.id, m.user_comments))
            m.user_comments = from_comment
            m.string = from_msgstr
            is_dirty = True
            print("new_value:{} => {}".format(m.id, m.user_comments))
            print("")

        if (is_dirty):
            print("Saving changes to: {}".format(self.to_file))
            #c.dump_po(self.to_file, self.to_cat)
        exit(0)
