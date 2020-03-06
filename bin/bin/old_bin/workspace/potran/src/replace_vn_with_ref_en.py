#!/usr/bin/python
# coding: utf-8

'''
Created on 31 Jan 2017

@author: Hoang Duy Tran <hoangduytran1960@googlemail.com>
'''
import re
from pluginregister import RegisteredImplementation

class replaceVNReferenceEN(RegisteredImplementation):
    en_pattern = ""
    vn_word = ""
    vn_pattern = ""
    rep_vn_word = ""
    en_list = []
    vn_list= []
    LINES = []
    
    def __init__(self, en_pattern, vn_pattern, vn_word, rep_vn_word) :
        self.en_pattern = en_pattern
        self.vn_pattern = vn_pattern
        self.vn_word = vn_word
        self.rep_vn_word = rep_vn_word
        print("en_pattern:" + self.en_pattern)
        print("vn_pattern:" + self.vn_pattern)
        print("rep_vn_word:" + self.rep_vn_word)
    
    def replaceWord(self, matchObj):
        is_first_upper = False
#        print("replaceWord replacing:")
        original_word_found = matchObj.group(0)
        is_first_upper = original_word_found[0].isupper()        
        replace_words = self.rep_vn_word.lower()
        if (is_first_upper):
            replace_words = replace_words[0].upper()+replace_words[1:]
#        print(is_first_upper)
#        print(replace_words)
        return replace_words
    
    
    def replaceLine(self, en_line_index, vn_line_index):            
            #en_text
#            print("replaceLine:")
            vn_text_line = self.LINES[vn_line_index]            
#            myre = re.compile(self.vn_word, re.I | re.U | re.S)
#            vn_new_text_line = myre.sub(self.rep_vn_word, vn_text_line)
            self.printBothSimple("before replacing: ", en_line_index, vn_line_index)
            vn_new_text_line = re.sub(self.vn_word, self.replaceWord, vn_text_line, flags=re.IGNORECASE)
            self.LINES[vn_line_index] = vn_new_text_line
            self.printBothSimple("after replaced: ", en_line_index, vn_line_index)
            
#            iterator = myre.finditer(vn_text_line)
#            for match in iterator:
#                print match.span()
            
#            vn_new_text_line = myre.sub(self.rep_vn_word, vn_text_line)
#            print("replaced:")
#            self.LINES[vn_line_index] = vn_new_text_line
#            print(vn_new_text_line);
#            vn_new_text_line = re.sub(self.vn_word, self.rep_vn_word, vn_text_line, flags=re.IGNORECASE)    
    
    
    def replaceList(self):
        en_index = vn_index = 0
        en_count = len(self.en_list)
        vn_count = len(self.vn_list)
        loop_count = max(en_count, vn_count)
        
        for loop_index in xrange(0, loop_count-1):
            valid = (en_index < en_count and vn_index < vn_count)
            if not valid:
                break
            en_line_index = self.en_list[en_index]
            vn_line_index = self.vn_list[vn_index]
            valid = (vn_line_index == en_line_index+1) #might need to expand this to 2
            if not valid:
                #decide which index to increase
                if en_line_index < vn_line_index:
                    #self.printBoth("en++:", en_index, en_line_index, vn_index, vn_line_index, True, False)
                    en_index += 1
                else :
                    #self.printBoth("vn++:", en_index, en_line_index, vn_index, vn_line_index, False, True)
                    vn_index += 1                    
                continue
                
            #valid
            #replacing
            #print("replacing: ", self.vn_pattern, "=>", self.rep_vn_word)
            #self.printBoth("calling replaceLine:", en_index, en_line_index, vn_index, vn_line_index, True, True)
            self.replaceLine(en_line_index, vn_line_index)
            #self.printBoth("replaced:", en_index, en_line_index, vn_index, vn_line_index, True, True)
            en_index += 1
            vn_index += 1
    
    
    def run(self):
        self.LINES = self.load(self.po_file_path)
        self.en_list = self.findWord(self.en_pattern, self.LINES)
        self.vn_list = self.findWord(self.vn_pattern, self.LINES)
        #print("ENGLISH: ", self.en_list)
        #print("VN: ", self.vn_list)
        valid_en = len(self.en_list) > 0
        valid_vn = len(self.vn_list) > 0
        valid = (valid_en and valid_vn)
        if (valid):
            self.replaceList()

if __name__ == '__main__':    
    x = replaceVNReferenceEN(r'.*\bTool\b.*$', r'.*Dụng cụ.*$', "Dụng cụ",  "công cụ")
    x.run()

