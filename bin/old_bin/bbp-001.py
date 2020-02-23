#!/usr/bin/env python
""" This file should run on the top directory of the html directory where all html and resource files should either
	resides on it or in subdirectories. The routine will start a directory walk from the current to all subdirectories
	and try to find instances of "htm" files in all directories and try to locate broken links of href, img, src,
	background - see handle_starttag() for details - and will try to locate resources and link in the local directories
	only. Out put is a sed command on console - with inline replacement option - and they should be captured into a
	shell script file and it should be ran separately. The routine and the sed script can take a long time to complete.
	Run as: bbp.py > sed.sh; chmod u+x sed.sh; ./sed.sh - wait... """
import fileinput
import fnmatch
import sys
import os
import urllib2
import urlparse
from HTMLParser import HTMLParser
from os.path import relpath

""" This is to solve the problem with html files and its resources has been re-organised
	where the html link is now broken. This class will try to solve it by parsing through
	the URL and list out broken links, with relative path of files and resources.
	The pair of original file (key) and it's new value is inserted (single instance) into
	the internal dictionary (__replace_list). The class is dealing with a single URL only """

#constants
__HASH		  = "#"
__SED_OPT		= '-sed'
__OPTIONS		= [__SED_OPT]
__EXCLUDE_LIST  = ['ms-its']
__INCLUDE_LIST  = ['href', 'background', 'img', 'src', 'value']
__FILE_EXT_LIST = ['.htm', '.html']

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
	__root_dir = ""
	__dir_name = ""
	__file_name = ""
	__replace_list = {}
	__path = ""

	def __init__(self, url, root_dir):
		HTMLParser.__init__(self)
		parse_result = urlparse.urlparse(url)
		path = parse_result.path
		self.__root_dir = root_dir
		self.__file_name = os.path.basename(path)
		self.__dir_name = os.path.dirname(path)
		self.__path = path
		print 'Path:', path
		print 'basename:', self.__file_name
		print 'dirname:', self.__dir_name

		self.url = url
		self.data = urllib2.urlopen(url).read()
		self.in_title = False
		self.title = ''
		self.feed(self.data)

	def get_url_path(self):
		return self.__path

	def get_root_dir(self):
		return self.__root_dir

	def get_result_list(self):
		return self.__replace_list

	def insert_tuple(self, d, k, tup):
		if k not in d:
			d[k] = tup

	def handle_starttag(self, tag, attrs):
		#print "handle_starttag:", tag, "attribs:", attrs
		for attrib in attrs:
			key = attrib[0]
			value = attrib[1]
			is_of_concerns = (key in __INCLUDE_LIST) and (str(value).find("ms-its") == -1)
			#print 'Key:', key, 'value:', value
#			not_is_ms_link_value = (str(value).find("ms-its") == -1)
#			is_of_concerns = not_is_ms_link_value and \
#							((key == "href") or \
#							(key == "background") or \
#							(key == "img") or \
#							(key == "src") or \
#							(key == "value"))
			if (is_of_concerns):
				print 'is_of_concerns Key:', key, 'value:', value
				self.process_key_value_pair(key, value)


	def process_key_value_pair(self, key, value):
		string_list = None
		filename_only = os.path.basename(value)
		hash_link_index = filename_only.rfind("#")
		has_hash_link = (hash_link_index >= 0)
		if has_hash_link:
			string_list = filename_only.split('#')
			#print string_list
			filename_only = string_list[0]
			#print "filename_only: ", filename_only

		found_list = self.find_file(filename_only)
		is_found = (len(found_list) > 0)
		#print "is_found: ", is_found
		#print "found_list:", found_list
		if is_found:
			found_file = found_list[0]
			#print "found file:", found_file
			if has_hash_link:
				found_file = found_file + "#" + string_list[1]
			is_different = (value != found_file)
			if (is_different):
				#print 'is_different:', value, ' != ', found_file
				self.insert_tuple(self.__replace_list, value, found_file)


	def find_file(self, file_to_be_found):
		matches = []
		root_dir = self.get_root_dir()
		dir_name = self.__dir_name
		for root, dirnames, filenames in os.walk(root_dir):
			for found_file in filenames:
				is_found = (found_file == file_to_be_found)
				if (is_found):
					relative_path = relpath(root, dir_name)
					#print 'relative path:', relative_path
					is_current_dir = (relative_path == ".")
					if (is_current_dir):
						matches.append(found_file)
					else:
						#print 'is_current_dir:', is_current_dir
						matches.append(os.path.join(relative_path, found_file))
			return matches

'''
	def handle_endtag(self, tag):
		print "handle_endtag:", tag
	def handle_data(self, data):
		print "handle_data:", data
'''

#def replace_in_file(path, find_pattern, replace_pattern):


def process_one_file_sed(url, root_dir):
	parser = MyHTMLParser(url, root_dir)
	result_list = parser.get_result_list()
	old_file = parser.get_url_path()

	for k, v in result_list.items():
		#print 'entry:', k, '=', v
		old_value = os.path.normpath(k)
		new_value = os.path.normpath(v)
		print "sed -i \'s|%s|%s|g\' %s" % (old_value, new_value, old_file)

def process_one_file(url, root_dir):
	parser = MyHTMLParser(url, root_dir)
	result_list = parser.get_result_list()
	old_file = parser.get_url_path()

	filedata = None
	f1 = open(old_file, 'r')
	filedata = f1.read()
	f1.close()

	#print 'result:', result_list
	for old_value, new_value in result_list.items():
		#print 'entry:', old_value, '=>', new_value
		filedata = filedata.replace(old_value, new_value)

	#print "replaced:", filedata

	new_file = old_file+".new"
	f2 = open(new_file, 'w')
	f2.write(filedata)
	f2.close()

	os.remove(old_file)
	os.rename(new_file, old_file)



def process_all_files(root_dir, is_using_sed_output):
	for root, dirnames, filenames in os.walk(root_dir, topdown=True):
		for file_name in fnmatch.filter(filenames, '*.htm'):
			found_file = os.path.join(root, file_name)
			#print "found: ", found_file
			url = "%s%s" % ("file://", found_file)
			if (is_using_sed_output):
				print "process_one_file_sed(url, root_dir)"
				#process_one_file_sed(url, root_dir)
			else:
				print "process_one_file(url, root_dir)"
				#process_one_file(url, root_dir)

def selective_process(path_index, cwd, is_sed):
	#print "path_index:", path_index
	path =  str(sys.argv[path_index])
	if (os.path.isfile(path)):
		url = "%s%s" % ("file://", path)
		if (is_sed):
			#print "process_one_file_sed(url, cwd), file:", path
			process_one_file_sed(url, cwd)
		else:
			#print "process_one_file(url, cwd), file:", path
			process_one_file(url, cwd)


def is_using_sed(argv):
	is_sed = False
	sed_index = -1
	argc = len(argv)
	for i in range(1, argc):
		arg = str(sys.argv[i])
		lower_case_opt = str(arg).lower()
		is_sed = (lower_case_opt == __SED_OPT)
		if (is_sed):
			sed_index = i
			break;
	return sed_index, is_sed;

def is_using_file(argv):
	is_file = False
	file_index = -1
	argc = len(argv)
	for i in range(1, argc):
		arg = str(sys.argv[i])		
		lower_case_opt = str(arg).lower()
		is_file = (arg not in __OPTIONS) and (os.path.isfile(arg))
		if (is_file):
			file_index = i
			break;
	return file_index, is_file;
		
	
def main():
	argc = len(sys.argv)
	cwd = os.getcwd()
	sed_index, is_sed = is_using_sed(sys.argv)
	print 'sed_index:', sed_index, "is_sed:", is_sed
	file_index, is_file = is_using_file(sys.argv)
	print 'file_index:', file_index, "is_file:", is_file
	process_all = not is_file
	
	if (process_all):
		print "process_all_files(cwd, is_sed: = ", is_sed
		#process_all_files(cwd, is_sed)
	else:
		selective_process(file_index, cwd, is_sed)




print 'Number of arguments', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
print 'Argument[0]:', str(sys.argv[0])
#sed_index, is_sed = is_using_sed(sys.argv)
#print 'sed_index:', sed_index, "is_sed:", is_sed
#file_index, is_file = is_using_file(sys.argv)
#print 'file_index:', file_index, "is_file:", is_file
#print 'basename:', os.path.basename(path) #filename
#print 'dirname:', os.path.dirname(path) #directory
if __name__ == "__main__":
	main()


