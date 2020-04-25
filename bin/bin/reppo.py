#!/usr/bin/python
# coding: utf-8
import traceback
import logging
import sys
import os
import errno
import re

class findAndReplace:
	en_pattern = ""
	vn_word = ""
	vn_pattern = ""
	rep_vn_word = ""
	en_list = []
	vn_list= []
	blender_home = os.environ.get('BLENDER_HOME')
	my_home=os.environ.get('HOME')
	file_path=blender_home + "/release/datafiles/locale/po/vi.po"
	temp_out_file_path=my_home + "/vi.po"
	
	LINES = []
	FILE = ""	
	def __init__(self, en_pattern, vn_pattern, vn_word, rep_vn_word) :
		self.en_pattern = en_pattern
		self.vn_pattern = vn_pattern
		self.vn_word = vn_word
		self.rep_vn_word = rep_vn_word
		print("blender_home:" + self.blender_home)
		print("en_pattern:" + self.en_pattern)
		print("vn_pattern:" + self.vn_pattern)
		print("rep_vn_word:" + self.rep_vn_word)
		print("temp_out_file_path:" + self.temp_out_file_path)

	
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
##				find_list.append(line)
			index += 1			
		count = len(find_list)
		#print(count)
		#print(find_list)
		return find_list

				
	def printBoth(self, msg, en_index, en_line_index, vn_index, vn_line_index, is_en_skip, is_vn_skip):
		sep_line = "---------------------------"
		print(sep_line)
		if (msg): print(msg)
		
		if is_en_skip:
			print("EN: ", en_index, en_line_index)
			print(self.LINES[en_line_index])
		
		if is_vn_skip:
			print("VN: ", vn_index, vn_line_index)
			print(self.LINES[vn_line_index])

			
	def printBothSimple(self, msg, en_line_index, vn_line_index):
		sep_line = "---------------------------"
		print(sep_line)
		if (msg): print(msg)
		
		print("EN: ", en_line_index)
		print(self.LINES[en_line_index])
	
		print("VN: ", vn_line_index)
		print(self.LINES[vn_line_index])
			
	
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

	
	def replaceWord(self, matchObj):
		is_first_upper = False
#		print("replaceWord replacing:")
		original_word_found = matchObj.group(0)
		is_first_upper = original_word_found[0].isupper()		
		replace_words = self.rep_vn_word.lower()
		if (is_first_upper):
			replace_words = replace_words[0].upper()+replace_words[1:]
#		print(is_first_upper)
#		print(replace_words)
		return replace_words

	
		
	def replaceLine(self, en_line_index, vn_line_index):			
			#en_text
#			print("replaceLine:")
			vn_text_line = self.LINES[vn_line_index]			
#			myre = re.compile(self.vn_word, re.I | re.U | re.S)
#			vn_new_text_line = myre.sub(self.rep_vn_word, vn_text_line)
			self.printBothSimple("before replacing: ", en_line_index, vn_line_index)
			vn_new_text_line = re.sub(self.vn_word, self.replaceWord, vn_text_line, flags=re.IGNORECASE)
			self.LINES[vn_line_index] = vn_new_text_line
			self.printBothSimple("after replaced: ", en_line_index, vn_line_index)
			
#			iterator = myre.finditer(vn_text_line)
#			for match in iterator:
#				print match.span()
			
#			vn_new_text_line = myre.sub(self.rep_vn_word, vn_text_line)
#			print("replaced:")
#			self.LINES[vn_line_index] = vn_new_text_line
#			print(vn_new_text_line);
#			vn_new_text_line = re.sub(self.vn_word, self.rep_vn_word, vn_text_line, flags=re.IGNORECASE)			


	def printTextLine(self, msg, text_line):
		sep_line = "---------------------------"
		print(sep_line)
		if (msg): print(msg)	
		print(text_line)

		
	def sentenceCase(self, matchObj):
		#print("sentenceCase:")
		original_word_found = matchObj.group(0)
		#print("original_word_found:")
		#print(original_word_found)
		decode_utf8 = original_word_found.decode('utf-8')
		replace_words = decode_utf8[0] + decode_utf8[1].upper()+decode_utf8[2:].lower()
		replace_words = replace_words.encode('utf-8')
		#print("replace_words:")		
		#print(replace_words)
		return replace_words
		
	
	def uppercase(self, matchObj):
		#print("uppercaseSpecialWords_0001:")
		original_word_found = matchObj.group(0)
		#print("original_word_found:")
		#print(original_word_found)
		replace_words = original_word_found.decode('utf-8').upper().encode('utf-8');
		#print("uppercased:")		
		#print(replace_words)
		return replace_words
		
		
	def retainUppercaseSepcialWord(self, text_line):
		#print("retainUppercaseSepcialWord:")
		dict={#'\b\b':'',
			'-f':'-F',
			'- bộ':'- Bộ',
			'\bx\b':'X',
			'\by\b':'Y',
			'\bz\b':'Z',
			'\-x':'-X',
			'\-y':'-Y',
			'\-z':'-Z',
			'\+x':'+X',
			'\+y':'+Y',
			'\+z':'+Z',
			'\bfh\b':'Fh',
			'CL\/TC':'CL/TC',
			'\b2D\b':'2D',
			'\bNLA\b':'NLA',
			'\bRNA\b':'RNA',
			'\-B':'-B'
			}
		new_text_line = text_line
		for find_pattern in dict.keys():
			replace_pattern = dict.get(find_pattern)
			new_text_line = re.sub(find_pattern, replace_pattern, new_text_line, flags=re.IGNORECASE)
			
		#print(new_text_line)
		return new_text_line
	
		
	
	def func_text_line_resolver(self, line_pattern, word_pattern, word_function, original_list):
		#msgstr
		index_list = []
		print("func_text_line_resolver:")		
		self.findWord(line_pattern, index_list, original_list)
		for vn_line_index in index_list:
			vn_text_line = original_list[vn_line_index]
			#print("before calling sentenceCase:")
			#print(vn_text_line)
			vn_new_text_line = re.sub(word_pattern, word_function, vn_text_line, flags=re.IGNORECASE)
			original_list[vn_line_index] = vn_new_text_line
			#print("after calling sentenceCase:")
			#print(vn_new_text_line)
			
						
	def func_replaceVN_WithRef_EN(self):
		self.findWord(self.en_pattern, self.en_list, self.LINES)
		self.findWord(self.vn_pattern, self.vn_list, self.LINES)
		#print("ENGLISH: ", self.en_list)
		#print("VN: ", self.vn_list)
		self.replaceList()
	
	
	def uppercaseFirstLetterInBraclet(self, matchObj):
		#print("uppercaseSpecialWords_0001:")
		original_word_found = matchObj.group(0)
		#print("original_word_found:")
		#print(original_word_found)
		decode_utf8 = original_word_found.decode('utf-8')
		replace_words = decode_utf8[0] + decode_utf8[1].upper()+decode_utf8[2:]
		replace_words = replace_words.encode('utf-8')
		#print("uppercased:")		
		#print(replace_words)
		return replace_words
		
		
		
	def func_bracketUpper(self):
		print("func_bracketUpper:")
		line_pattern = "^msgstr.*(\().*(\)).*"
		case_change_pattern = "(\().*(\))"
		self.findWord(line_pattern, self.vn_list, self.LINES)		
		for vn_line_index in self.vn_list:
			vn_text_line = self.LINES[vn_line_index]
			print("before calling sentenceCase:")
			print(vn_text_line)			
			vn_new_text_line = re.sub(case_change_pattern, self.uppercaseFirstLetterInBraclet, vn_text_line, flags=re.IGNORECASE)
			self.LINES[vn_line_index] = vn_new_text_line
			print("after calling sentenceCase:")
			print(vn_new_text_line)
		
	
	def reportBoth(self, msg, orig_line_index, orig_text_line, new_line_index, new_text_line):
		sep_line = "---------------------------"
		if (msg): print(msg)	
		print("original:", orig_line_index)
		print(orig_text_line)
		print("new:", new_line_index)
		print(new_text_line)
		print(sep_line)
		
	
	def comparingTwoList(self, en_new_list, input_en_new_list, en_orig_list, input_en_orig_list):
		change_count = 0
		new_index = orig_index = 0
		new_count = len(en_new_list)
		orig_count = len(en_orig_list)
		loop_count = max(new_count, orig_count)
		
		for count in xrange(0, loop_count-1):
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
			if (is_similar and not is_identical):
				self.reportBoth("is_similar and not is_identical", orig_line_index, orig_text_line, new_line_index, new_text_line)
				input_en_new_list[new_line_index] = orig_text_line
				change_count += 1
			elif not is_similar:
				self.reportBoth("not similar", orig_line_index, orig_text_line, new_line_index, new_text_line)
				change_count += 1
				raise Exception("not similar", "original:", orig_line_index, orig_text_line, "new:", new_line_index, new_text_line)
			
			new_index += 1
			orig_index += 1
		
		return change_count
		
		
	def matchup_with_English_orig(self):
		sep_line = "---------------------------"
		sep_end_group = "*********************************"
		input_en_new_path = self.file_path		
		input_en_orig_path = self.my_home + "/Downloads/orig/blender-2.78a/release/datafiles/locale/po/vi.po"
		input_en_new_list = input_en_orig_list = []
		
		input_en_new_list = self.openFile(input_en_new_path)
		input_en_orig_list = self.openFile(input_en_orig_path)
		
		en_line_pattern = "^msgid.*$"
		en_new_list = en_orig_list = []
		en_new_list = self.findWord(en_line_pattern, input_en_new_list)
		en_orig_list = self.findWord(en_line_pattern, input_en_orig_list)
		change_count = self.comparingTwoList(en_new_list, input_en_new_list, en_orig_list, input_en_orig_list)
		if (change_count > 0):
			print("After replaced:")
			change_count = self.comparingTwoList(en_new_list, input_en_new_list, en_orig_list, input_en_orig_list)
			if (change_count > 0): raise Exception("Still not the same after replaced. SOMETHING IS WRONG!!!!")
			self.writeFile(input_en_new_path, input_en_new_list)
		
		return input_en_new_list
		
	def func_replaceWordWithMatchingLinesEN_VN(self):
		self.LINES = self.openFile(self.file_path)
		
		#writeFile(self.file_path, all_text_lines)
	
	def func_process(self):
		print("func_process:")
		#self.matchup_with_English_orig()
		func_text_line_resolver()
		
		
	def writeFile(self, path, list):
		file=""
		try:
			file = open(path, 'w')
			for text_line in list:
				file.write(text_line)
		except : # catch all exceptions			
			msg = "Can't open file for writing: " + path
			logging.exception(msg, exc_info=True)
		finally:
			file.close()
	
	
	def openFile(self, path):
		file=""
		list=[]
		try:
			file = open(path)
			list = file.readlines()			
		except : # catch all exceptions			
			msg = "Can't open file: " + path
			logging.exception(msg, exc_info=True)
		finally:
			file.close()
			return list

		

	
if __name__ == '__main__':	
	x = findAndReplace(r'.*factor.*$', r'.*trị số.*$', "trị số",  "hệ số")
	#x.openFile()
	x.func_process()
	#x.writeFile()
	