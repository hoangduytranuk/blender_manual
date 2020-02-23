from functionbase import FunctionBase

class RemoveEntryByText(FunctionBase):
    def __init__(self):
        self.count=0
        self.dic = [
            "PROJECT VERSION",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
        ]

    def run(self):
        self.unsetChanged()
        remove_list=[]
        for m in self.cat:
            #print("dir(m){}".format(dir(m)))
            #print("m.user_comments:{}".format(m.user_comments))
            #print("m.context:{}".format(m.context))
            #print("m.fuzzy:{}".format(m.fuzzy))
            for key in self.dic:
                is_remove = (re.search(key, m.string, re.I) != None)
                if (is_remove):
                    print("File:{}".format(self.filename))
                    print("m.string:{}, is_remove:{}".format(m.string, is_remove))
                    self.count += 1
                    print("m:{}".format(m))
                    remove_list.append(m)
                    print("marked for removal")

        #for m in remove_list:
        #    self.cat.remove(m)
        #    self.setChanged()
