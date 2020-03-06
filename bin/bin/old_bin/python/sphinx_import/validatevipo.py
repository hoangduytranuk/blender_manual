import sys
sys.path.append("/home/htran/.local/lib/python3.6/site-packages")
#sys.path.append("/home/htran/.local/lib/python3.6/site-packages/babel/message")
sys.path.append("/home/htran/.local/lib/python3.6/site-packages/sphinx_intl")


print(sys.path)

#exit(0)
import os
import catalog as c
from functionbase import FunctionBase
from mymsg import MyMsg
from babel.messages.catalog import Message

#print("dir(c):{}".format(dir(c)))
#exit(0)

class ValidateVIPO(FunctionBase):
    def setLocalVars(self):
        self.from_file = "/home/htran/blender_documentations/po/blender.pot"
        #self.to_file = "/home/htran/blender_documentations/po/vi.po"
        self.to_file = "/home/htran/blender_documentations/po/vi.po"
        self.from_dic = {}

        self.from_cat = c.load_po(self.from_file)
        self.to_cat = c.load_po(self.to_file)
        self.sortFrom(self.from_cat, self.from_dic)
        #print("self.from_dic:{}".format(self.from_dic))
        #self.printCat(self.to_cat)
        #self.printCat(self.from_cat)
        #print("self.to_cat:{}".format(self.to_cat))
        #exit(0)

    def getMessageAsString(self, m, filename):
        s = []
        #is_message = (isinstance(m, Message))
        #if (not is_message):
            #print("NOT Message:{}, file:{}".format(m, filename))
            ##exit(0)

        try:
            valid = hasattr(m, 'flags') and (m.flags != None)
            if (valid):
                fuzzy_str = ', '.join(m.flags)
                s.append(fuzzy_str)
        except Exception as e:
            print("flags ValidateVIPO Exception: {}".format(e))
            print("m = {}, file:{}".format(m, filename))
            raise e

        try:

            valid = hasattr(m, 'auto_comments') and (m.auto_comments != None)
            if (valid):
                l=os.linesep.join(m.auto_comments)
                s.append(l)
        except Exception as e:
            print("auto_comments ValidateVIPO Exception: {}".format(e))
            print("m = {}, file:{}".format(m, filename))
            raise e

        try:

            valid = hasattr(m, 'user_comments')
            if (valid):
                l=os.linesep.join(m.user_comments) and (m.user_comments != None)
                s.append(l)
        except Exception as e:
            print("user_comments ValidateVIPO Exception: {}".format(e))
            print("m = {}, file:{}".format(m, filename))
            raise e


        try:

            valid = hasattr(m, 'context') and (m.context != None)
            if (valid):
                s.append(m.context)
        except Exception as e:
            print("context ValidateVIPO Exception: {}".format(e))
            print("m = {}, file:{}".format(m, filename))
            raise e

        try:
            valid = (m.id != None) and (m.id != None)
            if (valid):
                s.append(m.id)

            #valid = hasattr(m, 'string') and (m.string != None and len(m.string) != 0)
            #if (valid):
            #    s.append(m.string)
        except Exception as e:
            print("ID ValidateVIPO Exception: {}".format(e))
            print("m = {}, file:{}".format(m, filename))
            raise e

        return os.linesep.join(s)


    def printCat(self, cat):
        for m in cat:
            print(m)
            print("")

    def sortFrom(self, cat, dic):
        for m in cat:
            key = m.id
            msg = MyMsg(m)
            #print("{}".format(msg))
            dic.update({key:msg})

    def reportDiff(self, from_str, to_str):
        print("DIFF FROM:{}\nTO:{}".format(from_str, to_str))
        print("")

    def catToString(self, cat, filename):
        l=[]
        for m in cat:
            string = self.getMessageAsString(m, filename)
            l.append(string)
        return os.linesep.join(l)

    def run(self):
        is_dirty = False
        fr = self.catToString(self.from_cat, self.from_file)
        to = self.catToString(self.to_cat, self.to_file)
        #print(fr)
        #print("=" * 20)
        #print(to)
        #print("=" * 20)

        is_diff = (fr != to)
        print(is_diff)
        if (not is_diff):
            print("No difference is found between:{} => {}".format(self.from_file, self.to_file))
            print("=" * 80)
            exit(0)
        else:
            print("Checking differences:{} => {}".format(self.from_file, self.to_file))
            print("=" * 80)

        for index, to_m in enumerate(self.to_cat):
            #is_first_record = (index == 0)
            #if (is_first_record):
                #continue

            from_m = self.from_dic[to_m.id]
            is_found = (from_m != None)
            if (not is_found):
                #from_m = self.getMessageAsString(m)
                print("Not in the source -- to_str: {}, file:{}".format(to_m, self.to_file))
                print("")


            from_msg = MyMsg(from_m)
            print("from_msg:{}".format(str(from_msg)))
            exit(0)

            to_msg = MyMsg(to_m)

            ##to_str = self.getMessageAsString(to_m, self.to_file)

            ##print("from_m:{}".format(from_m))
            ##print("to_m:{}".format(to_m))


            ##from_str = self.getMessageAsString(from_m, self.from_file)
            ##is_same = (from_str == to_str)
            ##if (is_same):
                ##continue

            ##print("DIFF: from_str: {}=>{}".format(from_str, self.from_file))
            ##print("DIFF: to_str: {}=>{}".format(to_str, self.to_file))
            ##print("")


        exit(0)
"""
            if (m_to == None or m_to.id == None):
                continue

            m_from = self.from_dic[m_to.id]
            #is_found = (m_from != None)
            if (not is_found):
                continue

            from_str = self.getMessageAsString(m_from)
            is_same = (from_str == to_str)
            if (is_same):
                continue

            self.reportDiff(from_str, to_str)
        exit(0)
"""
