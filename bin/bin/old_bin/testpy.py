#!/usr/bin/python3 -d
import re
import sys
import os

class t1:
    def __init__(self):
        #self.text=":menuselection:`Only one` To create a domain, add a cube :menuselection:`one --> one two --> one`, :kbd:`Shift-A` and transform it until it encloses the area where you want smoke. Translation, rotation, and scaling are all allowed. To turn it into a smoke domain, click *Smoke* in :menuselection:`Properties --> Physics`, then select *Domain* as the *Smoke Type*."

        #self.text = "Smoke baking settings are in :menuselection:`Properties --> Physics --> Smoke --> Smoke Cache`. Unlike most physics simulations smoke physics has some settings that are specific to smoke."
        self.text = ":menuselection:`File --> Import/Export --> Motion Capture (.bvh)`"
        self.trans = ":menuselection:`Tập Tin (File) --> Nhập/Xuất (Import/Export) --> Motion Capture (.bvh) (Nắm Bắt Cử Chỉ/Hành Động)`"
        self.pattern=r":menuselection:`[\w ][^`]*`"

    def getNewText(self, old_text):
        p=re.findall(r":menuselection:`(.*)`", old_text)
        if (len(p) == 0):
            return None

        #print("p[0]:[{}]".format(p[0]))
        word_list = p[0].split(" --> ")
        for index, text in enumerate(word_list):
            test_bracketed_text = "\({}\)".format(text)
            test_text = ":menuselection:`[\w ]+{}.*".format(test_bracketed_text)
            print("test_text:{}".format(test_text))

            test_result = re.search(test_text, self.trans)
            is_found = (test_result != None)
            print("test_result:{}, is_found:{}".format(test_result, is_found))

            bracketed_text = "({})".format(text)
            word_list[index] = bracketed_text

        new_text = " --> ".join(word_list)
        new_text = ":menuselection:`{}`".format(new_text)
        #print(new_text)
        return new_text


    def run(self):
        #findPattern()
        p = re.compile(self.pattern)

        #m  = p.search(self.text)

        new_text = str(self.text)
        for m in p.finditer(self.text):
            old_sub_text = m.group()
            print("m.start:{}, m.group:{}".format(m.start(), m.group()))
            new_sub_text = self.getNewText(old_sub_text)
            new_text = re.sub(old_sub_text, new_sub_text, new_text, count=1)
            print("new_text:[{}]".format(new_text))

        #print(m.lastindex)
        #print(dir(m))
        #print("text=[{}]".format(self.text))
        #print("found:{}".format(found_list))



x = t1()
x.run()

