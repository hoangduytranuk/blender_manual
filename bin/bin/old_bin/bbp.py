#!/usr/bin/env python
'''
      This file should run on the top directory of the html directory where all html and resource files should either
      resides on it or in subdirectories. The routine will start a directory walk from the current to all subdirectories
      and try to find instances of "htm" files in all directories and try to locate broken links of href, img, src,
      background - see handle_starttag() for details - and will try to locate resources and link in the local directories
      only. Out put is a sed command on console - with inline replacement option - and they should be captured into a
      shell script file and it should be ran separately. The routine and the sed script can take a long time to complete.
      Run as: bbp.py > sed.sh; chmod u+x sed.sh; ./sed.sh - wait...
'''
import fileinput
import fnmatch
import sys
import os
import urllib2
import urlparse
import codecs
import re #regular expression
from HTMLParser import HTMLParser
from os.path import relpath

'''
	This is to solve the problem with html files and its resources has been re-organised
	where the html link is now broken. This class will try to solve it by parsing through
	the URL and list out broken links, with relative path of files and resources.
	The pair of original file (key) and it's new value is inserted (single instance) into
	the internal dictionary (__replace_list). The class is dealing with a single URL only
'''


#constants
__SED_OPT = '-sed'
__HELP_OPT = '-help'
__OPTIONS= [__SED_OPT, __HELP_OPT]
__PATTERN_FOR_FILE_EXTS = r'*\.(htm|html)$'

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
	__HASH		  	= "#"
	__EXCLUDE_LIST  = "ms-its"
	__INCLUDE_LIST  = ['href', 'background', 'img', 'src']

	__root_dir = None
	__dir_name = None
	__file_name = None
	__replace_list = None
	__path = None

	def __init__(self, url, root_dir):
		HTMLParser.__init__(self)
		parse_result = urlparse.urlparse(url)
		path = parse_result.path
		self.__replace_list = {}
		self.__root_dir = root_dir
		self.__file_name = os.path.basename(path)
		self.__dir_name = os.path.dirname(path)
		self.__path = path
#		print 'Path:', path
#		print 'basename:', self.__file_name
#		print 'dirname:', self.__dir_name

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
			is_of_concerns = (key in self.__INCLUDE_LIST) and (re.search(r'ms-its', value) == None)
			#is_of_concerns = (key in self.__INCLUDE_LIST) and (re.search(self.__EXCLUDE_LIST, value) == None)
			#is_of_concerns = (key in self.__INCLUDE_LIST)
			if (is_of_concerns):
				#print 'is_of_concerns Key:', key, 'value:', value
				self.process_key_value_pair(key, value)

	def process_key_value_pair(self, key, value):
		string_list = None
		filename_only = os.path.basename(value)
		hash_link_index = filename_only.rfind(self.__HASH)
		has_hash_link = (hash_link_index >= 0)
		#print "filename_only:", filename_only, "has_hash_link:", has_hash_link
		if has_hash_link:
			string_list = filename_only.split(self.__HASH)
			#print string_list
			filename_only = string_list[0]
			#print "filename_only: ", filename_only

		found_list = self.find_file(filename_only)
		is_found = (len(found_list) > 0)
		#print "is_found: ", is_found
		#print "key: [%s] value: [%s] found: [%s]" % (key, value, found_list)
		if is_found:
			found_file = found_list[0]
			#print "found file:", found_file
			if has_hash_link:
				found_file = found_file + self.__HASH + string_list[1]
			is_different = (value != found_file)
			if (is_different):
				#print 'is_different:', value, ' != ', found_file
				self.insert_tuple(self.__replace_list, value, found_file)

	def find_file(self, file_to_be_found):
		matches = []
		root_dir = self.get_root_dir()
		dir_name = self.__dir_name
		for root, dirs, files in os.walk(root_dir):
			for found_file in files:
				is_found = (found_file == file_to_be_found)
				if (is_found):
					relative_path = relpath(root, dir_name)
					is_current_dir = (relative_path == ".")
					if not is_current_dir:
						found_file = os.path.join(relative_path, found_file)

#					print "===================================================="
#					print "working_file:", self.__path
#					print "root_dir:", root_dir
#					print "dir_name:",dir_name
#					print "file_to_be_found:", file_to_be_found
#					print "relative path:", relative_path
#					print "found_file:", found_file
					matches.append(found_file)

		return matches


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
	f1 = codecs.open(old_file, 'r', 'utf-8')
	filedata = f1.read()
	f1.close()

	#print 'result:', result_list
	for old_value, new_value in result_list.items():
		#print 'entry:', old_value, '=>', new_value
		old_value = old_value.decode('utf-8')
		new_value = new_value.decode('utf-8')
		filedata = filedata.replace(old_value, new_value)

	#print "replaced:", filedata

	new_file = old_file+".new"
	f2 = codecs.open(new_file, 'w', 'utf-8')
	f2.write(filedata)
	f2.close()

	os.remove(old_file)
	os.rename(new_file, old_file)



def process_all_files(root_dir, is_using_sed_output):
	for root, dirs, files in os.walk(root_dir, topdown=True):
		#files = [os.path.join(root, f) for f in filenames]
		#files = [f for f in files if re.match(__FILE_EXT_LIST, f)]

#		for file_name in fnmatch.filter(filenames, '*.htm'):
#			found_file = os.path.join(root, file_name)

		for one_file in files:
			match = re.search(r'\.(htm|html)$', one_file, re.I|re.M)
			if (match):
				found_file = os.path.join(root, one_file)
				url = "%s%s" % ("file://", found_file)
				#print 'found_file:', found_file
				if (is_using_sed_output):
					#print "process_one_file_sed(%s, %s)" % (url, root_dir)
					process_one_file_sed(url, root_dir)
				else:
					#print "process_one_file(%s, %s)" % (url, root_dir)
					process_one_file(url, root_dir)

def selective_process(file_list, cwd, is_sed):
	#print "path_index:", path_index
	for path in file_list:
		if (os.path.isfile(path)):
			is_absolute_path = os.path.isabs(path)
			if not is_absolute_path:
				path = os.path.abspath(path)
			url = "%s%s" % ("file://", path)
			if (is_sed):
				#print "process_one_file_sed(url, cwd), file:", path
				process_one_file_sed(url, cwd)
			else:
				#print "process_one_file(url, cwd), file:", path
				process_one_file(url, cwd)


def is_using_option(argv, option):
	is_opt = False
	opt_index = -1
	argc = len(argv)
	for i in range(1, argc):
		arg = str(sys.argv[i])
		lower_case_opt = str(arg).lower()
		is_opt = (lower_case_opt == option)
		#print "lower_case_opt:", lower_case_opt," option:", option, "is_opt:", is_opt
		if (is_opt):
			opt_index = i
			break;
	return opt_index, is_opt

def is_using_file(argv):
	is_file = False
	file_list = []
	argc = len(argv)
	for i in range(1, argc):
		arg = str(sys.argv[i])
		lower_case_opt = str(arg).lower()
		is_file = (arg not in __OPTIONS) and (os.path.isfile(arg))
		if (is_file):
			file_list.append(arg)
	return file_list

def get_pipe_input():
	filelist=[]
	is_using_pipe = (sys.stdin.isatty() == False)
	#print "is_using_pipe:", is_using_pipe
	if not is_using_pipe:
		return filelist
	for line in sys.stdin:
		line = str(line).strip()
		is_file = os.path.isfile(line)
		if is_file:
			is_absolute_path = os.path.isabs(line)
			if not is_absolute_path:
				#cwd = os.getcwd();
				#path = os.path.join(cwd, line)
				path = os.path.abspath(line)
			else:
				path = line
			filelist.append(path)
			#print "path:", path
	return filelist

def process_pipe_input(file_list):
	#print file_list
	sed_index, is_sed = is_using_option(sys.argv, __SED_OPT)
	for path in file_list:
		url = "%s%s" % ("file://", path)
		cwd = os.getcwd()
		if (is_sed):
			#print "process_one_file_sed(url, cwd), file:", path
			process_one_file_sed(url, cwd)
		else:
			#print "process_one_file(url, cwd), file:", path
			process_one_file(url, cwd)
		#print "process_one_file(url, cwd), file:", path

def process_arguments():
#	argc = len(sys.argv)
	help_index, is_help = is_using_option(sys.argv, __HELP_OPT)
	#print "is_help", is_help
	if is_help:
		help()
		sys.exit(1)

	cwd = os.getcwd()
	sed_index, is_sed = is_using_option(sys.argv, __SED_OPT)
	#print 'sed_index:', sed_index, "is_sed:", is_sed
	file_list = is_using_file(sys.argv)
	is_file = (len(file_list) > 0)
	#print 'file_list:', file_list, "is_file:", is_file
	process_all = not is_file
	if (process_all):
		#print "process_all_files(cwd, is_sed: = ", is_sed
		process_all_files(cwd, is_sed)
	else:
		#print "selective_process(file_index:", file_index, "cwd, is_sed:", is_sed
		selective_process(file_list, cwd, is_sed)

def help():
	prog=os.path.basename(sys.argv[0])
	msg = \
"This facility will try to fix broken links against local files within the directory  \
that includes background images, href links and images. It must be stretched that this  \
facility only try to find broken links on local files and replace the broken links with  \
links that are found locally. It has no capability to check and validate or replace the \
remote links. \n \
Usage: \n \
====== \n \
1. %s {-sed} {<file.html> | <file.htm>} \n\n \
All options within brackets are OPTIONAL. \
- When running without arguments, the program will treat the current directory as the top \
directory and all (html|htm) files under the current directory will be search for broken links \
and all reference will be found and replaced silently. This process can take some times. \n \
- When running with -sed option, the program WILL NOT automatically replace the broken links that \
it found, but the replacement statements will be output in a sed command in the following form: \n\n \
	sed 's|<broken link>|<replacement>|g' <file> \n\n \
User can redirect output commands to a file and then run it as a shell script, for example: \n\n \
	%s -sed > sed_command.sh \n \
	chmod u+x sed_command.sh \n \
	./sed_command.sh \n\n \
Note: this method can take a long time, but user can examine the program's output before deciding to go ahead \
with the process or not, and that any short-falls exist that should be addressed. \n \
- When running with files, only the content of the given files are examined and replaced, \
if sed option is not chosen. For example: \n\n \
	%s -sed file1.htm file2.htm file3.htm \n \
	%s file1.htm file2.htm file3.htm \n\n \
- The program can also accept files using piping option, such as: \n\n \
	find . -name \"*test.htm\" | %s -sed \n \
	find . -name \"*test.htm\" | %s \n \
	ls *.htm | %s -sed \n \
	ls *.htm | %s \n \
" % (prog, prog, prog, prog, prog, prog, prog, prog)

	print msg

def main():
	file_list = get_pipe_input()
	has_pipe_input = (len(file_list) > 0)
	#print "file_list:", file_list, "has_pipe_input:", has_pipe_input
	if (has_pipe_input):
		#print "process_pipe_input(file_list)"
		process_pipe_input(file_list)
	else:
		#print "process_arguments()"
		process_arguments()

#print 'Number of arguments', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)
#print 'Argument[0]:', str(sys.argv[0])
#sed_index, is_sed = is_using_sed(sys.argv)
#print 'sed_index:', sed_index, "is_sed:", is_sed
#file_index, is_file = is_using_file(sys.argv)
#print 'file_index:', file_index, "is_file:", is_file
#print 'basename:', os.path.basename(path) #filename
#print 'dirname:', os.path.dirname(path) #directory
if __name__ == "__main__":
	main()
