#!/usr/bin/python3 -d
import sys
sys.path.append("/home/htran/bin/python/base")
sys.path.append("/home/htran/bin/python/")

import os
from argparse import ArgumentParser
from basefileio import BaseFileIO
from pprint import pprint as pp
from subprocess import Popen, PIPE, STDOUT

class SavingHistoryToFile(BaseFileIO):
    def __init__(self):
        self.is_clean : bool = False
        self.make_dir : str = None
        self.current_history_file="/home/htran/Documents/hoang_history_0002.txt"
        self.new_history_file="/home/htran/Documents/hoang_history_new.txt"

    def setVars(self, is_clean : bool, make_dir: str):
        self.is_clean = (True if (is_clean) else False)
        self.make_dir = (os.environ['BLENDER_MAN_EN'] if (make_dir == None) else make_dir)

    def GroupByLineNumber(self, text_list):
        hi_list=[]
        current_group=[]
        last_line_number = 1
        max_group_count = 0
        group_number = 1
        for line in text_list:
            line = line.strip()
            line_no, text_element = line.split(None, 1)
            current_line_number = int(line_no)

            is_the_same_group = (current_line_number == last_line_number)
            if is_the_same_group:
                current_group.append([current_line_number, text_element])
                #print("SAME group_number:", group_number, "current_line_number:", current_line_number, "text_element:", text_element)
            else:
                group_number += 1
                has_elements = (len(current_group) > 0)
                if has_elements:
                    hi_list.append(current_group)
                    current_group_count = len(current_group)
                    has_higher_group_count = (current_group_count > max_group_count)
                    if has_higher_group_count:
                        max_group_count = current_group_count
                current_group=[]
                last_line_number = current_line_number
                current_group.append([current_line_number, text_element])
                #print("SAVING GROUP: group_number:", group_number, "current_line_number:", current_line_number, "text_element:", text_element)

        #pp(hi_list)
        return hi_list, max_group_count

    def OrderingText(self, grouped_list, max_group_count):
        new_list=[]
        for index in range(0, max_group_count):
            group_index = index
            for group in grouped_list:
                group_length = len(group)
                is_valid_group = (group_index < group_length)
                if not is_valid_group:
                    continue
                else:
                    line_number, text_element = group[group_index]
                    #print("group_index:", group_index, "group_length:", group_length)
                    #print("line_number:", line_number, "; text_element:", text_element)
                    new_list.append(text_element)
        return new_list

        #print("current_line_number:", current_line_number)
        #print("text_element:", text_element)

    def getCurrentHistory(self):
        e = Popen("bash -i -c  'history -r;history' ", shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        output = e.communicate()
        current_history = str(output)
        #print()
        #os.system("history > /home/htran/temp_history.txt")
        current_list = current_history.split('\\n')
        #print("=" * 80)
        current_dict = []
        for line in current_list:
            line = line.strip()
            try:
                line_no, text_element = line.split(None, 1)
                current_dict.append(text_element)
                #print(int_line_no, text_element)
            except Exception as e:
                print(e)

        #print("=" * 80)
        #print("current_history:", repr(current_history), "current_history")
        return current_dict

    def getOldHistory(self):
        text_list = self.readTextFileAsList(self.current_history_file)
        #pp(text_list)
        group_list, max_group_length = self.GroupByLineNumber(text_list)
        ordered_list = self.OrderingText(group_list, max_group_length)
        old_dict = []
        for index, list_text in enumerate(ordered_list):
            k = index+1
            v = list_text
            old_dict.append(v)
            #print ("{:04d} {}".format(index, list_text))
            #print(index, list_text)
        return old_dict

    def mergeHistories(self):
        old_dict = self.getOldHistory()
        current_dict = self.getCurrentHistory()
        #print("=" * 80)
        #pp(old_dict)
        #print("=" * 80)
        #pp(current_dict)
        #print("=" * 80)

        merge_dict = old_dict + current_dict
        #self.saveAsText("/home/htran/old_hist.txt", old_dict)
        self.saveAsText("/home/htran/current_hist.txt", merge_dict)

    def saveAsText(self, file_path, dict_list):
        with open(file_path, "w") as file:
            for k, v in enumerate(dict_list):
                str="{:08d} {}\n".format(k+1, v)
                file.write(str)

    def run(self):
        os.environ.update({'LC_ALL':'C.UTF-8'})
        os.environ.update({'LANG':'C.UTF-8'})

        self.mergeHistories()

parser = ArgumentParser()
#parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_const', const=True)
parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_true')
parser.add_argument("-d", "--dir", dest="make_dir", help="Directory where MAKE is performed")
args = parser.parse_args()

print("args: {}".format(args))

x = SavingHistoryToFile()
x.setVars(args.clean_action, args.make_dir)
x.run()
