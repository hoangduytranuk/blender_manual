import os

class MyMsg:
    def __init__(self, m):
        self.comment=None
        self.context=None
        self.id=None
        self.string=None
        self.flags=None
        self.cloneFromMsg(m)


    def __repr__(self):
        l=[]

        valid = (self.flags != None)
        if (valid):
            l.append(self.flags)

        valid = (self.comment != None)
        if (valid):
            l.append(self.comment)

        valid = (self.context != None)
        if (valid):
            l.append(self.context)

        valid = (self.id != None)
        if (valid):
            l.append(''.join(self.id))

        valid = (self.string != None)
        if (valid):
            l.append(''.join(self.string))

        return os.linesep.join(l)

    def __compare__(self, other):
        if (other == None):
            return 1
        this_str = str(self)
        other_str = str(other)
        if (this_str < other_str): return -1
        if (this_str > other_str): return 1
        if (this_str == other_str): return 0

    def __gt__(self, other):
        return (self.__compare__(other) > 0)

    def __lt__(self, other):
        return (self.__compare__(other) < 0)

    def __eq__(self, other):
        return (self.__compare__(other) == 0)

    def isEmpty(self):
        is_empty = (self.comment == None) and \
            (self.context == None) and \
            (self.id == None) and \
            (self.string == None)
        return is_empty

    def cloneFromMsg(self, m):
        try:
            #if (isinstance(m, Message)):
            valid = hasattr(m, 'flags') and (m.flags != None) and (len(''.join(m.flags)) > 0)
            if (valid):
                fuzzy_str = ', '.join(m.flags)
                self.flags = fuzzy_str
                print("self.flags:{}".format(self.flags))

            valid = hasattr(m, 'auto_comments') and (m.auto_comments != None)
            if (valid):
                self.comment = os.linesep.join(m.auto_comments)

            valid = hasattr(m, 'user_comments') and (m.user_comments != None)
            if (valid):
                if (self.comment == None):
                    self.comment = ""
                self.comment += os.linesep.join(m.user_comments)

            if (self.comment != None):
                print("self.comment:{}".format(self.comment))

            valid = hasattr(m, 'context') and (m.context != None)
            if (valid):
                self.context = str(m.context)
                print("self.context:{}".format(self.context))

            valid = (m.id != None) and (len(m.id) > 0)
            if (valid):
                self.id = str(m.id)
                print("self.id:{}".format(self.id))

            #valid = hasattr(m, 'string') and (len(m.string) > 0)
            #if (valid):
                #self.string = str(m.string)
                #print("self.string:{}".format(self.string))

            print("-" * 80)
            #print(self)
            #print("-" * 80)

        except Exception as e:
            print("cloneFromMsg Exception: {}".format(e))
            print("m = {}".format(m))
            raise e

