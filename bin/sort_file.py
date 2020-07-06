#!/usr/local/bin/python3
import re
import os
import json
from collections import OrderedDict
from pprint import pprint as pp
from translation_finder import TranslationFinder, NoCaseDict

home_dir = os.environ['HOME']
in_file_name_1 = 'blender_manual/sorted_temp03.json'
in_file_name_2 = 'blender_manual/bracketed_text.json'
out_file_name = 'blender_manual/sorted_temp04.json'
out_file_name_1 = 'blender_manual/sorted_temp05.json'
out_file_name_2 = 'blender_manual/sorted_temp06.json'

in_file_path_1 = os.path.join(home_dir, in_file_name_1)
in_file_path_2 = os.path.join(home_dir, in_file_name_2)

out_file_path = os.path.join(home_dir, out_file_name)
out_file_path_1 = os.path.join(home_dir, out_file_name_1)
out_file_path_2 = os.path.join(home_dir, out_file_name_2)

def keyFunction(x):
	# print(f'x:{x}')
	# print(f'length:{len(x)}')
	return len(x[0])

def remove_quote(txt):
	p_end = re.compile(r'[\",]+$')
	p_start = re.compile(r'^[\"]')

	new_txt = p_end.sub('', txt)
	new_txt = p_start.sub('', new_txt)
	return new_txt


def readJSON(file_path):
	with open(file_path) as in_file:
		dic = json.load(in_file, object_pairs_hook=OrderedDict)
	return dic

def writeJSON(file_path, data):
	with open(file_path, 'w+', newline='\n', encoding='utf8') as out_file:
		json.dump(data, out_file, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ': '))

def readText(file_path):
	with open(file_path, 'r') as in_file:
		data_list = in_file.readlines()
	return data_list

def sorted_0001(in_file, out_file):
	tf = TranslationFinder()
	data_list = []

	data_list = readText(in_file)
	data_dict = OrderedDict()
	for data_line in data_list:
		data_line = data_line.strip()
		if not data_line:
			continue

		line_list = data_line.split('": "')
		old_k = old_v = None
		new_k = new_v = None
		try:
			old_k = line_list[0]
			old_v = line_list[1]

			new_k = remove_quote(old_k)
			new_v = remove_quote(old_v)

			tran = tf.isInListByDict(new_k, True)
			if tran:
				print(f'Already in master_dict:{new_k}, {tran}')
				continue

			if new_k in data_dict:
				print(f'ALREADY in data_dict, data_line:[{data_line}]')
				print(f'Repeated new_k:[{new_k}], new_v:[{new_v}]')
				old_v = data_dict[new_k]
				is_ignore = (old_k and not new_v)
				if is_ignore:
					print(f'IRNORE - data_line:[{data_line}]')
					continue
				else:
					print(f'data_line:[{data_line}]')
					print(f'Repeated check: k:[{new_k}], old_v:[{old_v}], new_v:[{new_v}]')

			data_dict.update({new_k: new_v})
		except Exception as e:
			print(e)

	sorted_dict = list(sorted(list(data_dict.items())))
	sorted_length_dic = list(sorted(sorted_dict, key=keyFunction))
	sorted_dict = OrderedDict(sorted_length_dic)
	writeJSON(in_file, sorted_dict)

def sorted_0002(in_file, out_file):
	data_dict = readJSON(in_file)
	sorted_dict = list(sorted(list(data_dict.items())))
	sorted_length_dic = list(sorted(sorted_dict, key=keyFunction))
	order_dict = OrderedDict(sorted_length_dic)
	sorted_dict = NoCaseDict(order_dict)

	tf = TranslationFinder()
	del_list = OrderedDict()
	for k, v in sorted_dict.items():
		old_tran = tf.isInListByDict(k, True)
		if old_tran:
			entry = {k: (old_tran, v)}
			del_list.update(entry)

	for k, v in del_list.items():
		print(f'del:{k}; {v}')
		del sorted_dict[k]

	writeJSON(out_file, sorted_dict)

def merge_json_0001(file_1, file_2, out_file):
	data_dict_1 = readJSON(file_1)
	data_dict_2 = readJSON(file_2)

	log=[]
	count = 0
	for k2, v2 in data_dict_2.items():
		if not k2:
			continue

		not_in_dict_1 = (k2 not in data_dict_1)
		if not_in_dict_1:
			entry = {k2: v2}
			log.append(f'added {entry}')
			data_dict_1.update(entry)
			count += 1
			continue

		in_both = (k2 in data_dict_1)
		if in_both:
			v1 = data_dict_1[k2]
			log.append(f'CHECK: [{k2}] => [{v1}]; [{v2}]')
			continue

	is_changed = (count > 0)
	if is_changed:
		sorted_dict = list(sorted(list(data_dict_1.items())))
		sorted_length_dic = list(sorted(sorted_dict, key=keyFunction))
		sorted_dict = OrderedDict(sorted_length_dic)
		writeJSON(out_file, sorted_dict)
		print(f'Write changes to {out_file}')

	pp(sorted(log))

def patternMatch(pat, text):
	try:
		return_dict = {}
		for m in pat.finditer(text):
			s = m.start()
			e = m.end()
			orig = m.group(0)
			original = (s, e, orig)
			entry = {(s,e): orig}
			return_dict.update(entry)

			for g in m.groups():
				if g:
					i_s = orig.find(g)
					ss = i_s + s
					ee = ss + len(g)
					v=(ss, ee, g)
					# break_down.append(v)
					entry = {(ss, ee): g}
					return_dict.update(entry)

	except Exception as e:
		_("patternMatchAll")
		_("pattern:", pat)
		_("text:", text)
		_(e)
	return return_dict

def numbers_to_VN_format(in_file, out_file):
	def changeNumberFormat(txt, matched_sorted_list):
		changed = False
		new_txt = str(txt)
		for loc, matched_txt in matched_sorted_list:
			is_dot = (matched_txt == '.')
			is_comma = (matched_txt == ',')
			is_valid = (is_dot or is_comma)
			if not is_valid:
				continue

			s, e = loc
			left = txt[:s]
			right = txt[e:]

			if is_comma:
				mid = '.'
			else:
				mid = ','
			new_txt = left + mid + right
			changed = True

		if changed:
			print(f'CHANGE: txt:{txt} => new_txt:{new_txt}')
		return new_txt

	data_dict_1 = readJSON(in_file)
	p_num = re.compile(r'\d+([,.])\d+')
	log=[]
	count = 0
	changed_list={}
	for k, v in data_dict_1.items():
		has_number = patternMatch(p_num, k)
		if not has_number:
			continue

		take_k_as_v = (has_number and not v)
		if take_k_as_v:
			print(f'take k as v:{k}')
			v = k

		found_list = patternMatch(p_num, v)
		is_found = bool(found_list)
		if not is_found:
			continue

		print(f'found: {k} {v}')
		sorted_found_list = sorted(list(found_list.items()), key=lambda x: x[1], reverse=False)
		pp(sorted_found_list)
		new_v = changeNumberFormat(v, sorted_found_list)
		new_entry = {k: new_v}
		changed_list.update(new_entry)
		print('-'*30)

	print('-'*80)
	for k, v in changed_list.items():
		print(f'{k}=>{v}')
	# pp(changed_list)

def txt_vnedict_to_dict():
	in_file = os.path.join(home_dir, 'blender_manual/vnedict.txt')
	out_file = os.path.join(home_dir, 'blender_manual/vnedict.json')
	data_list = readText(in_file)
	data_dict = OrderedDict()

	for text_line in data_list:
		text_line = text_line.strip()
		if not text_line:
			continue

		parts = text_line.split(' : ')
		vn_word = en_line = None
		try:
			vn_word = parts[0]
			en_line = parts[1]
			en_word_list = en_line.split(', ')
			for en_word in en_word_list:
				entry={en_word: vn_word}
				data_dict.update(entry)
		except Exception as e:
			print(e)

	sorted_dict = list(sorted(list(data_dict.items())))
	sorted_length_dic = list(sorted(sorted_dict, key=keyFunction))
	sorted_dict = OrderedDict(sorted_length_dic)
	writeJSON(out_file, sorted_dict)

	for en_word, vn_word in data_dict.items():
		print(f'{en_word} => {vn_word}')

def txt_vnedict_to_dict_startdict_en_vi():
	in_file = os.path.join(home_dir, 'Downloads/kindle-dict-master/dict/stardict_en_vi.txt')
	out_file = os.path.join(home_dir, 'blender_manual/vnedict_0001.json')
	data_list = readText(in_file)
	data_dict = OrderedDict()

	# p = re.compile(r'([^@]+)@[^-]+?(.*)', flags=re.M)
	for text_line in data_list:
		text_line = text_line.strip()
		if not text_line:
			continue

		# found_list = patternMatch(p, text_line)
		found_list = text_line.split('\\n-')
		# print(f'found_list:{found_list}')
		en = found_list[0].split('@')[0].strip()
		# print(f'EN:{en}')
		vn = []
		for i in range(1, len(found_list)):
			vn_found_list = found_list[i].split('\\n')
			for vn_term in vn_found_list:
				is_spec = vn_term.startswith('@')
				if is_spec:
					continue
				vn_term = vn_term.strip()
				is_new_term = vn_term.startswith('=')
				if is_new_term:
					new_vn_term = vn_term.strip('=')
					term_list = new_vn = new_vn = None
					has_plus_separator = (new_vn_term.find('+') >= 0)
					has_new_line_separator = (new_vn_term.find('\\n') >= 0)
					has_separator = (has_plus_separator or has_new_line_separator)
					if has_separator:
						if has_plus_separator:
							term_list = new_vn_term.split('+')
						if has_new_line_separator:
							term_list = new_vn_term.split('\\n')
						try:
							new_en = term_list[0]
							new_vn = term_list[1].strip()
							data_dict.update({new_en: new_vn})
						except Exception as e:
							print(e)
					else:
						print('debug')
				else:
					data_dict.update({en: vn_term})

	sorted_dict = list(sorted(list(data_dict.items())))
	sorted_length_dic = list(sorted(sorted_dict, key=keyFunction))
	sorted_dict = OrderedDict(sorted_length_dic)
	writeJSON(out_file, sorted_dict)
	#
	# for en_word, vn_word in data_dict.items():
	# 	print(f'{en_word} => {vn_word}')


# sorted_0002()
# merge_json_0001(in_file_path_1, in_file_path_2, out_file_path)
# sorted_0002(out_file_path, out_file_path_1)
# numbers_to_VN_format(out_file_path_1, out_file_path_2)
# txt_vnedict_to_dict()
txt_vnedict_to_dict_startdict_en_vi()
