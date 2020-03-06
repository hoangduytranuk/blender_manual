#!/usr/bin/env python
# -*- coding: utf-8 -*- 

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

other_terms = [
('Read the Bible In One Year', 'Đọc Kinh-Thánh trong một năm'),
('Day', '<h3>Ngày</h3>'),
('Reading', '<h3>Đọc</h3>')
]

monthlist = [
('January', 'Tháng Giêng'),
('February', 'Tháng Hai'),
('March', 'Tháng Ba'),
('April', 'Tháng Tư'),
('May', 'Tháng Năm'),
('June', 'Tháng Sáu'),
('July', 'Tháng Bảy'),
('August', 'Tháng Tám'),
('September', 'Tháng Chín'),
('October', 'Tháng Mười'),
('November', 'Tháng Mười Một'),
('December', 'Tháng Mười Hai')]

booklist = [
('Genesis','Sáng-Thế Ký'),
('Exodus','Xuất Ê-díp-tô Ký'),
('Leviticus','Lê-vi Ký'),
('Numbers','Dân số ký'),
('Deuteronomy','Phục-truyền Luật-lệ Ký'),
('Joshua','Giô-suê'),
('Judges','Các quan xét'),
('Ruth','Ru-tơ'),
('1st Samuel','I Sa-mu-ên'),
('2nd Samuel','II Sa-mu-ên'),
('1st Kings','I Các Vua'),
('2nd Kings','II Các Vua'),
('1st Chronicles','I Sử Ký'),
('2nd Chronicles','II Sử Ký'),
('Ezra','E-xơ-ra'),
('Nehemiah','Nê-hê-mi'),
('Esther','Ê-xơ-tê'),
('Job','Gióp'),
('Psalms','Thi-thiên'),
('Proverbs','Châm-ngôn'),
('Ecclesiastes','Truyền-đạo'),
('Song of Solomon','Nhã-ca'),
('Isaiah','Ê-sai'),
('Jeremiah','Giê-rê-mi'),
('Lamentations','Ca-thương'),
('Ezekiel','Ê-xê-chi-ên'),
('Daniel','Đa-ni-ên'),
('Hosea','Ô-sê'),
('Joel','Giô-ên'),
('Amos','A-mốt'),
('Obadiah','Áp-đi-a'),
('Jonah','Giô-na'),
('Micah','Mi-chê'),
('Nahum','Na-hum'),
('Habakkuk','Ha-ba-cúc'),
('Zephaniah','Sô-phô-ni'),
('Haggai','A-ghê'),
('Zechariah','Xa-cha-ri'),
('Malachi','Ma-la-chi'),
('Matthew','Ma-thi-ơ'),
('Mark','Mác'),
('Luke','Lu-ca'),
('John','Giăng'),
('Acts','Công vụ các sứ đồ'),
('Romans','Rô-ma'),
('1st Corinthians','I Cô-rinh-tô'),
('2nd Corinthians','II Cô-rinh-tô'),
('Galatians','Ga-la-ti'),
('Ephesians','Ê-phê-sô'),
('Philippians','Phi-líp'),
('Colossians','Cô-lô-se'),
('1st Thessalonians','I Tê-sa-lô-ni-ca'),
('2nd Thessalonians','II Tê-sa-lô-ni-ca'),
('1st Timothy','I Ti-mô-thê'),
('2nd Timothy','II Ti-mô-thê'),
('Titus','Tít'),
('Philemon','Phi-lê-môn'),
('Hebrews','Hê-bơ-rơ'),
('James','Gia-cơ'),
('1st Peter','I Phi-e-rơ'),
('2nd Peter','II Phi-e-rơ'),
('1st John','I Giăng'),
('2nd John','II Giăng'),
('3rd John','III Giăng'),
('Jude','Giu-đe'),
('Revelation','Khải-huyền')]

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

#	def handle_starttag(self, tag, attrs):
#		print "handle_starttag:", tag, "attribs:", attrs

#		for attrib in attrs:
#			key = attrib[0]
#			value = attrib[1]
#			print "key:", key, "value:", value '''

	def is_number(self, s):
		try:
			float(s)
			return True
		except:
			return False

#	def handle_data(self, data):
#		data = str(data).strip()
#		valid = (len(data) > 0) and (not self.is_number(data))
#		if (valid):
#			print data

#	def handle_startendtag(self, tag, attrs):
#		print "handle_startendtag:", tag, "attribs:", attrs

def process_one_file(url, root_dir):
	parser = MyHTMLParser(url, root_dir)
	result_list = parser.get_result_list()
	old_file = parser.get_url_path()

def main():
#	print 'Number of arguments: %s' % len(sys.argv)
#	print 'Argument List:', str(sys.argv)
#	print 'Argument[0]:', str(sys.argv[0])
	path = str(sys.argv[1])
	if not os.path.isabs(path):
		path = os.path.abspath(path)
#	url = "%s%s" % ("file://", path)
#	cwd = os.getcwd()
#	booklist.extend(monthlist)
#	for k,v in booklist:
#		print k, v
	process_one_file(path)
	#reverse_date(path)

def reverse_date(old_file):
	#output to sed and run the sed script, quicker and accurate
	filedata = None
	f1 = codecs.open(old_file, 'r', 'utf-8')
	filedata = f1.readlines()
	f1.close()

	new_filedata = []
	pat = re.compile(u'(Tháng.*\;)([0-9]+)', re.U)
	for line in filedata:
#		line = line.rstrip()
		m = re.search(pat, line)
		if m:
#			print "[%s]" % line
			g = m.groups()
			g0 = m.group(0)
			g1 = m.group(1)			
			g2 = m.group(2)
#			print "g1:", g1, "g2:", g2			
			temp = "|||"
			line = line.replace(g1, temp)
			line = line.replace(g2, g1)
			g2 = g2 + "-"
			line = line.replace(temp, g2)

			#g2_with_space = g2 + r"&nbsp;"
#			g2_with_sep = g2 + "-"
#			print "g2_with_space:", g2_with_sep
#			line = line.replace(g2, g2_with_sep)
#			print "[%s]" % line
		new_filedata.append(line)

#	print new_filedata
		
	new_file = old_file+".new"
	f2 = codecs.open(new_file, 'w', 'utf-8')	
	f2.writelines(new_filedata)
	f2.close()

	os.remove(old_file)
	os.rename(new_file, old_file)
	

	
def process_one_file(old_file):
	#output to sed and run the sed script, quicker and accurate
	filedata = None
	f1 = codecs.open(old_file, 'r', 'utf-8')
	filedata = f1.read()
	f1.close()

	new_file = old_file+".new"
	f2 = codecs.open(new_file, 'w', 'utf-8')
	f2.write(filedata)
	f2.close()

	os.remove(old_file)
	os.rename(new_file, old_file)

	#print filedata
	booklist.extend(monthlist)
	booklist.extend(other_terms)	
	#print 'result:', result_list
	for old_value, new_value in booklist:		
		#cmd = "sed -i \'s|%s|%s|g\' %s" % (old_value, new_value, old_file)
		#print cmd                
		#reg = "\b%s\b" % old_value
		#pat = re.compile(u'\b%s\b' % old_value, re.U|re.X)		
		#print 'pattern:', pat.pattern, "new_value:", new_value
		#filedata = re.sub(pat, new_value, filedata)
		#print 'entry:', old_value, '=>', new_value
		#old_value = u'%s' % (old_value)
		#new_value = u'%s' % (new_value)                
		#filedata = filedata.decode("utf-8").replace(old_value, new_value).encode("utf-8")
		#old_value = repr(old_value)
		#new_value = repr(new_value)
		old_value = old_value.decode('utf-8')
		new_value = new_value.decode('utf-8')
		filedata = filedata.replace(old_value, new_value)
	#print filedata
	#print filedata.encode('utf8')

	new_file = old_file+".new"
	f2 = codecs.open(new_file, 'w', 'utf-8')
	f2.write(filedata)
	f2.close()

	os.remove(old_file)
	os.rename(new_file, old_file)

if __name__ == "__main__":
	main()
