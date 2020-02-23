#!/usr/bin/python
# coding: utf-8

'''
Created on 31 Jan 2017

@author: Hoang Duy Tran <hoangduytran1960@googlemail.com>
'''
from pluginregister import RegisteredImplementation

class MatchUpWithEnglishOriginal(RegisteredImplementation):
    
    en_line_pattern = None
    
    def distanceToNextMatch(self, orig_list, orig_current_index, new_list, new_current_index, is_target_original):
        source_list = (new_list if (is_target_original) else orig_list)
        target_list = (orig_list if (is_target_original) else new_list)
        source_count = len(source_list)
        
        source_current_index = (new_current_index if (is_target_original) else orig_current_index)
        target_current_index = (orig_current_index if (is_target_original) else new_current_index)
        
        distance = 0
        
        target_current_text_line = target_list[target_current_index]
        print("target_current_text_line: {}".format(target_current_text_line))        
        for i in xrange(source_current_index, source_count-1):
            source_current_text_line = source_list[i]            
            is_same = (source_current_text_line == target_current_text_line)
            distance += (0 if (is_same) else 1)
            print("source_current_text_line:{}".format(source_current_text_line))                        
            if (is_same):
                print("is_same found @ line:{}".format(i))
                break
            
        return distance
    
    
    def balanceList(self, input_en_orig_list, orig_current_line_index, input_en_new_list, new_current_line_index):
        #fixing the imbalance, find out which list need to insert or remove
        missing_count = self.distanceToNextMatch(input_en_orig_list, orig_current_line_index, input_en_new_list, new_current_line_index, True)
        is_del_new = (missing_count > 0)
        if (not is_del_new):
            missing_count = self.distanceToNextMatch(input_en_orig_list, orig_current_line_index, input_en_new_list, new_current_line_index, False)
        print("missing_count:{}\nis_del_new:{}".format(missing_count, is_del_new))
        
        next_line_index = new_current_line_index + 1
        if (is_del_new): #delete lines from new
            remove_new_line_index = new_current_line_index
            for i in xrange(0, missing_count):                
                text_line_to_be_removed = input_en_orig_list[remove_new_line_index]
                print('remove_new_line_index: {} text_line_to_be_removed: {}'.format(remove_new_line_index, text_line_to_be_removed))
                input_en_new_list.pop(remove_new_line_index)                
        else:#insert original lines into new list 
            next_line_index = new_current_line_index + missing_count + 1
            #insert from original to new_list 
            for i in xrange(0, missing_count):
                insert_new_line_index = new_current_line_index + i
                text_line_to_be_insert = input_en_orig_list[orig_current_line_index + i]
                print("insert_new_line_index:", insert_new_line_index, " text_line_to_be_insert:", text_line_to_be_insert)
                input_en_new_list.insert(insert_new_line_index, text_line_to_be_insert)
        
        #debugging printing last 5 lines to max missing_count lines
        spacing=5
        numb_lines_to_print = (spacing * 2 if (is_del_new) else missing_count+2)
        self.printListSection(input_en_new_list, new_current_line_index-spacing, numb_lines_to_print)
        return next_line_index
        
        
    def toHex(self, string_input):
	hex_string = ":".join("{:02x}".format(ord(c)) for c in string_input)
	return hex_string

    def comparingTwoList(self, en_new_list, input_en_new_list, en_orig_list, input_en_orig_list, start_index):
        
        is_end = (start_index >= len(input_en_new_list))
        if (is_end):
            return;
                        
        change_count = 0
        new_index = orig_index = start_index
        new_count = len(en_new_list)        
        orig_count = len(en_orig_list)
        loop_count = max(new_count, orig_count)
        
        for count in xrange(start_index, loop_count-1):
            valid = (new_index < new_count and orig_index < orig_count)
            if not valid:
                break
            new_line_index = en_new_list[new_index]
            orig_line_index = en_orig_list[orig_index]
            new_text_line = input_en_new_list[new_line_index]
            orig_text_line = input_en_orig_list[orig_line_index]

            #print("original:")
            #print(orig_text_line)
            #print("new:")
            #print(new_text_line)
            
            is_similar = (new_text_line.lower() == orig_text_line.lower())
            is_identical = (new_text_line == orig_text_line)
            if (is_similar):
		if  not is_identical:
	                self.reportBoth("is_similar and not is_identical", orig_line_index, orig_text_line, new_line_index, new_text_line)
        	        input_en_new_list[new_line_index] = orig_text_line		
            else:
                self.reportBoth("not similar", orig_line_index, orig_text_line, new_line_index, new_text_line)
                msg_old = "\noriginal:\n" + str(orig_line_index+1) + ":" + orig_text_line + " ["+ self.toHex(orig_text_line) + "]\n"
                msg_new = "new:\n" + str(new_line_index+1) + ":" + new_text_line + " [" + self.toHex(new_text_line) + "]"
                #new_start_index = self.balanceList(input_en_orig_list, orig_line_index, input_en_new_list, new_line_index)
                #en_new_list = self.findWord(self.en_line_pattern, input_en_new_list)                
                #self.comparingTwoList(en_new_list, input_en_new_list, en_orig_list, input_en_orig_list, new_start_index)            
                raise Exception(msg_old + msg_new)
            new_index += 1
            orig_index += 1
                    
     

    def run(self):
        sep_line = "---------------------------"
        sep_end_group = "*********************************"
        input_en_new_path = self.po_file_path
        #input_en_new_path = self.my_home + "/blender-git/blender/release/datafiles/locale/po/vi.po"
        #input_en_orig_path = self.my_home + "/Downloads/orig/blender-2.78a/release/datafiles/locale/po/vi.po"
        #input_en_orig_path = self.my_home + "/blender-git/blender/release/datafiles/locale/po/vi.po"
	input_en_orig_path = self.my_home + "/blender-svn/bf-translations/trunk/po/vi.po"
        
        input_en_new_list = self.load(input_en_new_path)
        input_en_orig_list = self.load(input_en_orig_path)
        
        self.en_line_pattern = "^msgid.*$"
#        self.en_line_pattern = "^msgctxt.*$"
        en_new_list = self.findWord(self.en_line_pattern, input_en_new_list)
        en_orig_list = self.findWord(self.en_line_pattern, input_en_orig_list)
        self.comparingTwoList(en_new_list, input_en_new_list, en_orig_list, input_en_orig_list, 0)

#        self.en_line_pattern = "^msgctxt.*$"
#        en_new_list = self.findWord(self.en_line_pattern, input_en_new_list)
#        en_orig_list = self.findWord(self.en_line_pattern, input_en_orig_list)
#        self.comparingTwoList(en_new_list, input_en_new_list, en_orig_list, input_en_orig_list, 0)

##        
#        if (change_count > 0):
#            print("After replaced:")
#            change_count = self.comparingTwoList(en_new_list, input_en_new_list, en_orig_list, input_en_orig_list)
#            if (change_count > 0): raise Exception("Still not the same after replaced. SOMETHING IS WRONG!!!!")
#            num_lines = len(input_en_new_list)
#            if (num_lines > 0):
#                print("Writing changes to file")
#                #self.writeFile(input_en_new_path, input_en_new_list)
            
    
if __name__ == '__main__':
    x = MatchUpWithEnglishOriginal()
    x.run()
