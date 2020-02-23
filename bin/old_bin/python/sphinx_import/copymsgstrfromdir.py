from functionbase import FunctionBase
import os
import os.path as P

class CopyMsgStrFromDir(FunctionBase):
    def setLocalVars(self):
        #print("self.filename:{}".format(self.filename))
        self.from_file_path ="../new_{}".format(self.filename)
        self.is_from_file = P.isfile(self.from_file_path)
        #print("from_file_path:{}, exist:{}".format(self.from_file_path, self.is_from_file))

        self.from_dic = {}
        self.c = self.getMasterCat()
        self.from_cat = self.c.load_po(self.from_file_path)
        self.catToDict(self.from_cat, self.from_dic)
        #self.printDict(self.from_dic, self.from_file_path)
        self.to_cat = self.cat

    #def printCat(self, cat):
        #print("printCat:=============================")
        #for m in cat:
            #print("msgid \"{}\"".format(m.id))
            #print("msgstr \"{}\"".format(m.string))
            #print("")

    def printDict(self, dic, filename):
        print("printDict:{}".format(filename))
        print("=" * 80)
        for key, value in dic.items():
            print("msgid \"{}\"".format(key))
            print("msgstr \"{}\"".format(value))
            print("")


    def catToDict(self, cat, dic):
        dic.clear()
        for m in cat:
            key = m.id
            value = m
            dic.update({key:value})
        return dic

    def run(self):
        is_dirty = False
        print("self.filename:{}".format(self.filename))
        for index, m in enumerate(self.to_cat):
            is_first_message = (index == 0)

            if (is_first_message):
                continue;

            to_id = m.id
            is_there = (to_id in self.from_dic)

            if (not is_there): continue

            from_entry = self.from_dic[to_id]

            from_str = from_entry.string
            to_str = m.string

            is_same = (from_str == to_str)
            if (is_same): continue

            m.string = from_str
            is_dirty = True

            print("to_id:{}".format(m.id))
            #print("from_str:{}".format(from_str))
            print("to_str:{}".format(m.string))
            print("=" * 80)

        if (is_dirty):
            print("Saving changes to: {}".format(self.to_file))
            #c.dump_po(self.to_file, self.to_cat)
            exit(0)
