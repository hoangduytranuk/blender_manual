from functionbase import FunctionBase
from hashlib import sha256
impor re

class ApplyDictionary(FunctionBase):

    def setLocalVars(self):
        self.your_name="Hoang Duy Tran"
        self.your_email="hoangduytran1960@googlemail.com"
        self.your_id="{} <{}>".format(self.your_name, self.your_email)
        self.translation_team="London, UK {}".format(self.your_email)
        self.language_code="vi"
        self.re_language_code="\"Language: \\\\n\"\n".format(self.language_code)

        self.dic = {
            #"^Standard image input.$":"Đầu vào tiêu chuẩn của hình ảnh.",
            #"^Standard image output.$":"Đầu ra tiêu chuẩn của hình ảnh.",
            "Last-Translator: FULL NAME.*>":"Last-Translator: {}".format(self.your_id),
            "FIRST AUTHOR.*SS>":self.your_id,
            "PO-Revision-Date.*[[:digit:]]\{4\}":"PO-Revision-Date: {}".format(self.timeNow()),
            "PO-Revision-Date: YEAR.*ZONE":"PO-Revision-Date: {}".format(self.timeNow()),
            "Language-Team:.*>":"Language-Team: {}".format(self.translation_team),
            "\"MIME-Version":"{}\"MIME-Version".format(self.re_language_code)
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
        }

    def changePattern(self, m, key, value):
        #print("key:{}, value:{}".format(key, value))
        is_id_matching = (re.search(key, m.string) != None)
        is_translated = (re.search(value,m.string) != None)
        is_replace = (is_id_matching and not is_translated)
        is_diry = False
        if (is_replace):
            old_string = str(m.string)
            old_sha256sum = sha256(old_string.encode()).hexdigest()
            #m.string = value
            new_string = re.sub(key, value, old_string)
            new_sha256sum = sha256(new_string.encode()).hexdigest()
            is_changed = (old_sha256sum != new_sha256sum)
            if (is_changed):
                m.string = new_string
                self.setChanged()
                is_diry = True
                #self.updateChangesCount()
                #print("m.id:{}".format(m.id))
                #print("old_string:{}\nold_sha256sum:{}".format(old_string, old_sha256sum))
                print("new_string:{}\nnew_sha256sum:{}".format(new_string, new_sha256sum))
                #print("File Count:{}; Changes Count:{}".format(self.getFileCount(), self.getChangesCount(), m.string, new_sha256sum))
        return is_diry

    def run(self):
        self.unsetChanged()
        for m in self.cat:
            #print("dir(m){}".format(dir(m)))
            #print("m.user_comments:{}".format(m.user_comments))
            ##print("m.context:{}".format(m.context))
            #print("m.fuzzy:{}".format(m.fuzzy))
            index = 0
            is_dirty = False
            for key, value in self.dic.items():
                is_first = (index == 0)
                if (is_first):
                    is_dirty = self.changePattern(m, key, value)
                elif (is_dirty):
                    self.changePattern(m, key, value)
                index += 1
        if (self.isChanged()):
            #print("File has been changed:{}".format(self.filename))
            self.updateFileCount()
            #print("File:{}".format(self.filename))
            #exit(1)
