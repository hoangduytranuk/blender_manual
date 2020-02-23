'''
Created on 31 Jan 2017

@author: Hoang Duy Tran <hoangduytran1960@googlemail.com>
'''
import abc
from pluginbase import PluginBase
import traceback
import logging
import sys
import os
import errno
import re
import math
from ntpath import devnull
from sys import exc_info


class RegisteredImplementation(object):
    sep_line = "---------------------------"
    __po_file = "vi.po"
#    __po_path = "/home/htran/blender-2.78a/release/datafiles/locale/po/" 
    __po_path = "/home/htran/Downloads/" 
    po_file_path = __po_path + __po_file
    my_home = my_home=os.environ.get('HOME')
    
    @property
    def popath(self):
        return self.po_file_path

    @popath.setter
    def popath(self, newvalue):
        self.po_file_path = newvalue
        

    def findWord(self, find_word, orig_list):        
        find_list = []
        pat = re.compile(find_word, re.IGNORECASE) ;
        index = 0        
        count = len(orig_list)
        print(pat)
        for x in xrange(0, count-1):
            line = orig_list[x]            
            if pat.match(line):                
                find_list.append(index)
##                find_list.append(line)
            index += 1  
        count = len(find_list)
        #print(count)
        #print(find_list)
        return find_list

    
    def reportBoth(self, msg, orig_line_index, orig_text_line, new_line_index, new_text_line):        
        if (msg): print(msg)    
        print("original: {}, {}new: {}, {}".format(orig_line_index, orig_text_line, new_line_index, new_text_line))
        print(self.sep_line)
        

    def printBoth(self, msg, en_index, en_line_index, vn_index, vn_line_index, is_en_skip, is_vn_skip):        
        print(self.sep_line)
        if (msg): print(msg)
        
        if is_en_skip:
            print("EN: ", en_index, en_line_index)
            print(self.LINES[en_line_index])
        
        if is_vn_skip:
            print("VN: ", vn_index, vn_line_index)
            print(self.LINES[vn_line_index])

            
    def printListSection(self, list_to_print, from_index, num_lines):
        print(self.sep_line)
        print_start_index = max(0, from_index) 
        total_num_lines = len(list_to_print)        
        print_end_index = max(0, min(total_num_lines, print_start_index + num_lines))
        print 'print_start_index: {} num_lines: {} total_num_lines: {} print_end_index: {}'.format(print_start_index, num_lines, total_num_lines, print_end_index)
        for i in xrange(print_start_index, print_end_index):
            text_line = list_to_print[i]
            print '{}:{}'.format(i, text_line.strip())
        print(self.sep_line)
        
        
    def printBothSimple(self, msg, en_line_index, vn_line_index):
        print(self.sep_line)
        if (msg): print(msg)
        
        print("EN: ", en_line_index)
        print(self.LINES[en_line_index])
    
        print("VN: ", vn_line_index)
        print(self.LINES[vn_line_index])
                
    def load(self, path):
        mylist=[]
        myfile = None
        try:
            myfile = open(path)
            mylist = myfile.readlines()
        except: # catch all exception
            msg = "Can#t open file for reading:" + path
            logging.exception(msg, exc_info=True)
        finally:
            if (myfile):
                myfile.close()
            return mylist
    
    def save(self, path, data_list):
        ok = False
        myfile = None
        try:
            myfile = open(path, 'w')
            for text_line in data_list:
                myfile.write(text_line)
            ok = True
        except: # catch all exception
            msg = "Can#t open file for writing:" + path
            logging.exception(msg, exc_info=True)            
        finally:
            if (myfile):
                myfile.close()
            return ok
            
    
PluginBase.register(RegisteredImplementation)

'''
if __name__ == '__main__':
    print('Subclass:', issubclass(RegisteredImplementation, PluginBase))
    print('Instance:', isinstance(RegisteredImplementation(), PluginBase))
'''
