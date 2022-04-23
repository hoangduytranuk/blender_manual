# -*- coding: utf-8 -*-
#!/usr/local/bin/python3
import pprint
import sys


import os
import re
from pprint import pp
from translation_finder import TranslationFinder as tf
from nocasedict import NoCaseDict
import json
from definition import RefType, Definitions as df
from sphinx_intl import catalog as c
import datetime
from docutils import nodes

from pytz import timezone
from babel.messages import Catalog, Message
from sphinx.util.nodes import extract_messages
from bracket import RefAndBracketsParser as PSER
try:
    import html
except ImportError:
    html = None

YOUR_NAME = "Hoang Duy Tran"
YOUR_EMAIL = "hoangduytran1960@gmail.com"
YOUR_ID = "{} <{}>".format(YOUR_NAME, YOUR_EMAIL)
YOUR_TRANSLATION_TEAM = "London, UK <{}>".format(YOUR_EMAIL)
YOUR_LANGUAGE_CODE = "vi"
TIME_ZONE = 'Europe/London'

RUNNING_APP_ENVIRON_KEY = 'EXEC_TRANSLATE_PO'
po_data = None
po_path = None
po_out_path = None

class MessageProcessing(object):
    def __init__(self):
        self.message_list=[]
        home = os.environ['HOME']
        self.home = os.path.join(home, "Dev/tran")

    def builder_init(self, app):
        pass
        # trans_finder.loadVIPOtoDic(trans_finder.master_dic_list, trans_finder.master_dic_file, is_testing=True)
        # trans_finder.updateMasterDic(is_testing=True)
        # exit(0)
        # trans_finder.mergePODict()
        # pass
        # home = os.environ['HOME']
        # blender_man_vn = os.path.join(home, 'Dev/tran/blender_docs/locale/vi/LC_MESSAGES')
        # # vi_blender_manual_po_path = os.path.join(blender_man_vn, 'blender_manual.po')
        # vi_blender_manual_po_path = os.path.join(home, 'blender_manual_0003.po')
        # po_data = c.load_po(vi_blender_manual_po_path)
        #
        # trans_finder = tf()
        # tf_dict = trans_finder.getDict()
        # doctree_resolved.po_data = po_data
        # doctree_resolved.tf_dict = tf_dict
        # build_finished.po_data = po_data
        # blender_manual_po_data = c.load_po(blender_manual_po_path)

    def env_updated(app, env):
        pass

    def build_finished(app, exeption):
        home = os.environ['HOME']
        # # blender_man_vn = os.path.join(home, 'Dev/tran/blender_docs/locale/vi/LC_MESSAGES')
        # po_out_path = os.path.join(home, 'blender_manual_0003_0001.po')
        # # catalog, line_width=76
        # po_data = build_finished.po_data
        #
        # c.dump_po(po_out_path, po_data, line_width=4096)
        pass

    def getTimeNow(self):
        local_time = timezone('Europe/London')
        fmt = '%Y-%m-%d %H:%M%z'
        loc_dt = local_time.localize(datetime.datetime.now())
        formatted_dt = loc_dt.strftime(fmt)
        return formatted_dt

    def isDupOrig(self, node):
        is_inline = isinstance(node, nodes.inline)
        is_emphasis = isinstance(node, nodes.emphasis)
        is_title = isinstance(node, nodes.title)
        is_term = isinstance(node, nodes.term)
        is_rubric = isinstance(node, nodes.rubric)
        is_field_name = isinstance(node, nodes.field_name)
        is_reference = isinstance(node, nodes.reference)
        is_strong = isinstance(node, nodes.strong)
        is_caption = isinstance(node, nodes.caption)
        is_toc_tree = (node.tagname == 'toctree')

        is_keep_original = (is_inline or
                            is_emphasis or
                            is_title or
                            is_term or
                            is_rubric or
                            is_field_name or
                            is_reference or
                            is_strong or
                            is_toc_tree
                            )
        # if translate and the link is `ref text <link txt>`__ then DO NOT REPEAT,
        # translate as `translation (english) <link_txt>`__
        return is_keep_original

    def keepACopyOrNot(self, entry):
        msg = entry[0]
        node = entry[1]
        # is_debug = ('Installation Guide'.lower() in msg.lower())
        # if is_debug:
        #     print(msg)
        #     print(f'{type(node)}')
        #     print(f'{dir(node)}')
            # exit(0)
        is_keep_original = self.isDupOrig(node)
        if not is_keep_original:
            return None

        is_ending_with_dot = (msg.endswith('.') and not msg.endswith('...'))
        if is_ending_with_dot:
            return None
        else:
            return msg

    def readFile(self, file_name):
        with open(file_name, 'r') as f:
            data_lines = f.read().splitlines()
        return data_lines

    def writeFile(self, file_name, data):
        data_list = [(x + '\n') for x in data]
        print(f'WRITING: {len(data_list)} lines to {file_name}')
        with open(file_name, 'w+') as f:
            f.writelines(data_list)

    def removeIfNotRepeatable(self, non_repeat_list):
        def updateMessage(m: Message):
            mid = m.id
            valid = bool(mid)
            if not valid:
                return None

            mstr = m.string
            has_tran = bool(mstr)
            if not has_tran:
                return None

            is_valid_line = (mid in valid_keep_lines)
            if not is_valid_line:
                return None

            m.string = ""
            return mid

        home = self.home
        man_po = os.path.join(home, 'blender_manual_0003_0020.po')
        man_po_out = os.path.join(home, 'blender_manual_0003_0021.po')
        data = c.load_po(man_po)
        result_id_cleaned = list(map(updateMessage, data))
        result_id_cleaned = [x for x in result_id_cleaned if bool(x)]
        pp(result_id_cleaned)

    def makeKeepAndIgnoreFiles(self):
        def sortMessageList(entry):
            try:
                (node, msg) = entry
                return msg
            except Exception as e:
                print(f'Problem line: {entry}')
                print(e)
                raise e

        def splitToList(text_line: str):
            ignored_lines = splitToList.ignored_lines
            keep = splitToList.keep_list
            ignore = splitToList.ignore_list
            if bool(text_line):
                is_keep = not (text_line in ignored_lines)
                if is_keep:
                    keep.append(text_line)
                else:
                    ignore.append(text_line)
                return True
            else:
                return False

        try:
            home = self.home
            ref_file = os.path.join(home, 'keep_refs.log')
            ignored_file = os.path.join(home, 'ignore.log')
            keep_file = os.path.join(home, 'keep_20220421.log')
            ignore_file = os.path.join(home, 'ignore_20220421.log')
            all_entries = os.path.join(home, 'all_entries_20220421.log')
            ignored_lines = self.readFile(ignored_file)

            keep_list_report = list(map(self.keepACopyOrNot, self.message_list))

            splitToList.keep_list = []
            splitToList.ignore_list = []
            splitToList.ignored_lines = ignored_lines
            bool_list = list(map(splitToList, keep_list_report))
        except Exception as e:
            print(e)
            raise e

        keep_list = splitToList.keep_list
        ignore_list = splitToList.ignore_list

        keep_list = list(set(keep_list))
        ignore_list = list(set(ignore_list))
        ignore_list.sort()
        keep_list.sort()
        
        sort_list = [msg for (msg, node) in self.message_list]
        sort_list = list(set(sort_list))
        sort_list.sort()

        self.writeFile(keep_file, keep_list)
        self.writeFile(ignore_file, ignore_list)
        self.writeFile(all_entries, sort_list)

    def removeUnrepeatedEntries(self):
        home = self.home
        ignore_file = os.path.join(home, 'ignore.log')
        ignore_list = self.readFile(ignore_file)
        self.removeIfNotRepeatable(ignore_list)

    def run(self):
        # self.removeUnrepeatedEntries()
        self.makeKeepAndIgnoreFiles()

class POResultRecord(object):
    def __init__(self, line_no, msgid, msgstr, alternative_tran=None, alternative_label=None):
        self.line_no = line_no
        self.msgid = msgid
        self.msgstr = msgstr
        self.alt_msgstr = alternative_tran
        self.alt_lbl = (alternative_label if bool(alternative_label) else "alternative")

    def __repr__(self):
        self.msgid = ("" if not self.msgid else self.msgid)
        self.msgstr = ("" if not self.msgstr else self.msgstr)
        txt = f'[{self.line_no}];\nmsgid:"{self.msgid}";\nmsgstr:"{self.msgstr}"'
        if self.alt_msgstr:
            txt += f'\n{self.alt_lbl}:[{self.alt_msgstr}]\n\n'
        return txt

class POTaskBase(list):
    def __init__(self,
                 input_file=None,
                 output_to_file=None,
                 translation_file=None,
                 ):
        self.po_path = input_file
        self.opo_path = output_to_file
        self.tran_file = translation_file
        self.result = []
        self.line_count=0

        self.home = os.environ['HOME']
        self.blender_manual_path = os.path.join(self.home, 'Dev/tran/blender_docs/locale/vi/LC_MESSAGES')
        self.blender_manual_po_path = os.path.join(self.blender_manual_path, 'blender_manual.po')
        self.blender_manual_po_data: Catalog = None
        self.changed = False

    def writeJSONDic(self, dict_list=None, file_name=None):
        try:
            if not file_name:
                return

            if not dict_list:
                return

            with open(file_name, 'w+', newline='\n', encoding='utf8') as out_file:
                json.dump(dict_list, out_file, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            df.LOG(f'{e}; Length of read dictionary:{len(dict_list)}', error=True)
            raise e

    def loadJSONDic(self, file_name=None):
        return_dic = {}
        try:
            if not file_name:
                print(f'loadJSONDic - file_name is None.')
                return return_dic

            if not os.path.isfile(file_name):
                print(f'loadJSONDic - file_name:{file_name} cannot be found!')
                return return_dic

            dic = {}
            with open(file_name) as in_file:
                # dic = json.load(in_file, object_pairs_hook=NoCaseDict)
                return_dic = json.load(in_file)
        except Exception as e:
            df.LOG(f'{e}; Exception occurs while performing loadJSONDic({file_name})', error=True)

        return return_dic
    def outputToFile(self, path, data):
        self.writeJSONDic(data, path)

    def convertDataToDict(self, data=None):
        def sort_record(r: POResultRecord):
            return r.line_no

        result_dict={}
        r : POResultRecord = None

        working_data = (data if data else self)
        sorted_data = list(sorted(working_data, key=sort_record, reverse=False))
        for r in sorted_data:
            k = r.msgid
            v = r.msgstr
            dict_entry={k: v}
            result_dict.update(dict_entry)
        return result_dict

    def updateTranslation(self, msgid, msgstr, is_repeat=False):

        is_data_ready = (self.blender_manual_po_data is not None)
        if not is_data_ready:
            self.blender_manual_po_data = c.load_po(self.blender_manual_po_path)

        if is_repeat:
            msgstr = f'{msgstr} -- {msgid}'

        is_in = (msgid in self.blender_manual_po_data)
        msg = ""
        if is_in:
            current_tran = self.blender_manual_po_data[msgid]
            is_diff = (current_tran != msgstr)
            if is_diff:
                # self.blender_manual_po_data[msgid] = msgstr
                msg = f'UPDATE: msgid: "{msgid}"\nmsgstr: "{current_tran}"\n'
                msg += f"updated: {msgstr}"
            else:
                msg = f'CURRENT: msgid: "{msgid}"\nmsgstr: "{current_tran}"\n'
        else:
            msg = f'NEW: msgid: "{msgid}"\nmsgstr: "{msgstr}"\n'
        print(msg)

    def showResult(self):
        has_records = (len(self) > 0)
        if not has_records:
            msg = f'NOTHING is found.'
            print(msg)
            return

        has_output_file = bool(self.opo_path)
        if has_output_file:
            output_dict = self.convertDataToDict()
            self.outputToFile(self.opo_path, output_dict)
        else:
            for rec in self:
                print(rec)

        if self.count_number_of_lines:
            self.line_count = len(self)
            msg = f'{self.line_count} records is found!'
            print(msg)

# task = POTaskBase()
msg_proc = MessageProcessing()

def doctree_resolved(app, doctree, docname):
    try:
        for node, msg in extract_messages(doctree):
            entry = (msg, node)
            msg_proc.message_list.append(entry)
    except Exception as e:
        df.LOG(f'{e}', error=True)


def runAppOrNot():
    is_running = (RUNNING_APP_ENVIRON_KEY in os.environ)
    if not is_running:
        return False
    value = os.environ[RUNNING_APP_ENVIRON_KEY]
    is_running = (value == "YES")
    if not is_running:
        return False
    return True

def build_finished(app, exeption):
    msg_proc.run()

def setup(app):
    app.connect('doctree-resolved', doctree_resolved)
    app.connect('build-finished', build_finished)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }


# sphinx-build -t builder_html -b gettext  -j "8" manual build/locale

# !/usr/bin/python3


from sphinx.cmd.build import main

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
