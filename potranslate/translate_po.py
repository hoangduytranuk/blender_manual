# -*- coding: utf-8 -*-
#!/usr/local/bin/python3

import sys


import os
import re

from common import Common as cm
from utils import dd, pp
from translation_finder import TranslationFinder as tf
from ignore import Ignore as ig
import json
from reflist import RefList
from definition import RefType, Definitions as df
from sphinx_intl import catalog as c
import datetime

from pytz import timezone
from pprint import pprint as PP
from paragraph import Paragraph as PR
from babel.messages import Catalog, Message
from sphinx.util.nodes import extract_messages
from docutils import nodes
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
trans_finder = tf()



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

    def outputToFile(self, path, data):
        try:
            writeJSONDic(data, path)
        except Exception as e:
            raise RuntimeError(e)

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

result_list = POTaskBase()

def doctree_resolved(app, doctree, docname):

    def abbreviating():
        remove_items = []
        new_items = {}

        for k, v in trans_finder.master_dic.items():
            ref_list = RefList(msg=v)
            new_v = ref_list.quotedToAbbrev(k)
            has_new_v = (new_v is not None) and (len(new_v) > 0)
            if has_new_v:
                new_entry = {k: new_v}
                new_items.update(new_entry)

        has_remove_items = (len(remove_items) > 0)
        if has_remove_items:
            for k in remove_items:
                dd(f'Delete from dictionary:[{k}]')
                del trans_finder.master_dic[k]

        is_writing_changes = (len(new_items) > 0)
        if is_writing_changes:
            trans_finder.master_dic.update(new_items)
            dic_file = '/Users/hoangduytran/Dev/tran/blender_manual/test_dic.json'
            print(f'Writing changes to: {dic_file}, number of records:{len(new_items)}')
            trans_finder.writeJSONDic(dict_list=trans_finder.master_dic, file_name=dic_file)

    def checkDictForMultipleMeaningsInTrans():
        pattern = re.compile(r'(\w+(/\w+)+)')
        k: str = None
        v: str = None
        for k, v in trans_finder.master_dic.items():
            k_found_list = pattern.findall(k)
            v_found_list = pattern.findall(v)

            is_same = (len(k_found_list) == len(v_found_list))
            if is_same:
                continue

            k_is_single_word = (len(k.split(' ')) == 1)
            if k_is_single_word:
                continue

            PP(k_found_list)
            print('-'*3)
            PP(v_found_list)
            print('-'*3)
            print(f'{k}\n\n{v}')
            print('-'*40)

    def trimmingText(text):
        txt_has_trimmable_ending = (cm.TRIMMABLE_ENDING.search(text) is not None)
        txt_has_trimmable_beginning = (cm.TRIMMABLE_BEGINNING.search(text) is not None)
        is_trim = (txt_has_trimmable_ending or txt_has_trimmable_beginning)
        if not is_trim:
            return text, False
        text = cm.TRIMMABLE_BEGINNING.sub('', text)
        text = cm.TRIMMABLE_ENDING.sub('', text)
        return text, True

    def removeDictBeginAndEndingPuncts():
        remove_set={}
        add_set={}

        for k, v in trans_finder.master_dic.items():
            # is_debug = ('Cut to' in k)
            # if is_debug:
            #     dd('DEBUG')

            trimmed_k, is_trimmed_k = trimmingText(k)
            trimmed_v, is_trimmed_v = trimmingText(v)

            changed = (is_trimmed_k or is_trimmed_v)
            if changed:
                remove_entry={k:v}
                remove_set.update(remove_entry)

                add_entry = {trimmed_k:trimmed_v}
                add_set.update(add_entry)


            print(f'[{k}]')
            print(f'[{trimmed_k}]')
            print('-'*3)
            print(f'[{v}]')
            print(f'[{trimmed_v}]')
            print('-'*40)

        changed = False
        for k, v in remove_set.items():
            remove_entry = {k:v}
            print(f'remove:{remove_entry}')
            del trans_finder.master_dic[k]
            changed = True

        for k, v in add_set.items():
            add_entry = {k:v}
            trans_finder.master_dic.update(add_entry)
            print(f'added: {add_entry}')
            changed = True

        if changed:
            new_dict = cleanupLeadingTrailingPunct(trans_finder.master_dic)
            test_to_file='/Users/hoangduytran/blender_manual/ref_dict_0005.json'
            trans_finder.writeJSONDic(dict_list=new_dict, file_name=test_to_file)

    def removeDuplication(txt_with_punct):
        # is_debug = (txt_with_punct.endswith('::'))
        # if is_debug:
        #     dd('DEBUG')
        cropped_txt, begin_with_punctuations, ending_with_punctuations = cm.beginAndEndPunctuation(txt_with_punct,
                                                                                                   is_single=True)
        trans = trans_finder.isInList(cropped_txt)
        is_repeat = (trans is not None)
        if not is_repeat:
            cropped_txt, begin_with_punctuations, ending_with_punctuations = cm.beginAndEndPunctuation(txt_with_punct,
                                                                                                       is_single=False)
            trans = trans_finder.isInList(cropped_txt)

        is_repeat = (trans is not None)
        return is_repeat

    def cleanupLeadingTrailingPunct(d_dict):
        return_dict={}
        for k, v in d_dict.items():
            trimmed_k = str(k)
            trimmed_v = str(v)
            found_k = cm.WORD_WITHOUT_QUOTE.search(k)
            found_v = cm.WORD_WITHOUT_QUOTE.search(v)
            if found_k:
                trimmed_k = found_k.group(1)
            if found_v:
                trimmed_v = found_v.group(1)
            entry = {trimmed_k:trimmed_v}
            return_dict.update(entry)
        return return_dict

    def refToDictItems(ref_list):
        ref_dict = {}
        ref  = None
        interest_ref = [
            RefType.REF,
            RefType.DOC,
            RefType.GA,
            RefType.TERM,
        ]
        for ref in ref_list:
            # print(ref)
            type = ref.getOrigin().getRefType()
            first_ref = ref.getRefItemByIndex(0)
            ref_text = first_ref.getText()

            is_debug = ('Poor mans steadycam' in ref_text)
            if is_debug:
                dd('DEBUG')

            en_part = None
            vn_part = None
            d_dict = {}
            if type == RefType.MENUSELECTION:
                print(f'MENUSELECTION:{type}')
                text_list = cm.MENU_TEXT_REVERSE.findall(ref_text)
                length = len(text_list)
                i_index = 0
                for i in range(length):
                    tran = text_list[i_index]
                    if i_index + 1 < length:
                        orig = text_list[i_index + 1]
                    else:
                        print('ERROR: Orig is NOT THERE, use original')
                        orig = ref.getOrigin().getText()

                    entry={orig:tran}
                    print(f'menu:{entry}')
                    d_dict.update(entry)
                    i_index += 2
                    if i_index >= length:
                        break

            elif type == RefType.ABBR:
                print(f'ABBR:{type}')
                text_list = cm.ABBREV_TEXT_REVERSE.findall(ref_text)
                abbr = text_list[0]
                defin = text_list[1]
                has_further_explanation = (': ' in defin)
                if has_further_explanation:
                    exp_list = defin.split(': ')
                    orig_part = exp_list[0]
                    further_exp = exp_list[1]
                    print(f'abbr:{abbr}; orig_part:{orig_part}; further_exp:{further_exp}')

                    if abbr.isascii():
                        entry={abbr:f'{orig_part}, {further_exp}'}
                    elif orig_part.isascii():
                        entry={orig_part:f'{further_exp}, {abbr}'}
                    else:
                        entry={further_exp:f'{orig_part}, {abbr}'}
                    d_dict.update(entry)
                else:
                    print(f'abbr:{abbr}; defin:{defin}')
                    if defin.isascii():
                        entry={defin: abbr}
                    else:
                        entry={abbr: defin}
                    d_dict.update(entry)

            elif type in interest_ref:
                print(f'GENERIC_REF:{type}')
                text_list = cm.REF_TEXT_REVERSE.findall(ref_text)
                has_text = (len(text_list) > 0)
                if not has_text:
                    origin_text = ref.getOrigin().getText()
                    print(f'ERROR: origin_text:{origin_text}')
                    # print(f'{text_list}, appeared to be empty!!!')
                else:
                    vn_part, en_part = text_list[0]
                    print(f'en_part:{en_part} vn_part:{vn_part}')
                    entry={en_part:vn_part}
                    d_dict.update(entry)
            else:
                dd(f'{type} is not the type we are looking for.')
            ref_dict.update(d_dict)

        return_dict = cleanupLeadingTrailingPunct(d_dict)

        return return_dict

    def listDictRefsToDict():
        interest_ref_list = [
            RefType.MENUSELECTION,
            RefType.REF,
            RefType.DOC,
            RefType.GA,
            RefType.TERM,
            RefType.ABBR,
        ]

        ref_dict = {}
        ref_dict_filename='/Users/hoangduytran/blender_manual/ref_dict_refsonly.json'
        for k, v in trans_finder.master_dic.items():
            ref_list = RefList(msg=v, keep_orig=False, tf=trans_finder)
            ref_list.parseMessage()

            inter_ref_list = ref_list.getListOfRefType(interest_ref_list)
            has_ref = (len(inter_ref_list) > 0)
            if not has_ref:
                continue

            current_ref_dict = refToDictItems(inter_ref_list)
            ref_dict.update(current_ref_dict)

        has_dict_content = (len(ref_dict) > 0)
        if has_dict_content:
            trans_finder.writeJSONDic(dict_list=ref_dict, file_name=ref_dict_filename)


    def tranRef(msg, is_keep_original):
        ref_list = RefList(msg=msg, keep_orig=is_keep_original, tf=trans_finder)
        ref_list.parseMessage()
        ref_list.translateRefList()
        tran = ref_list.getTranslation()
        # trans_finder.addDictEntry((msg, tran))
        # print("Got translation from REF_LIST")
        return tran

    # def fuzzyTextSimilar(txt1 : str, txt2 : str, accept_ratio):
    #     try:
    #         similar_ratio = LE.ratio(txt1, txt2)
    #         is_similar = (similar_ratio >= accept_ratio)
    #         return is_similar
    #     except Exception as e:
    #         print(e)
    #         return False

    def getTimeNow(self):
        local_time = timezone('Europe/London')
        fmt = '%Y-%m-%d %H:%M%z'
        loc_dt = local_time.localize(datetime.datetime.now())
        formatted_dt = loc_dt.strftime(fmt)
        return formatted_dt

    # is_running = runAppOrNot()
    # if not is_running:
    #     return

    # correctingDictionary()
    # checkDictKeyboard()
    # checkDictRef()
    # checkNonTranslatedDictWords()
    # checkDictForMultipleMeaningsInTrans()
    # removeDictBeginAndEndingPuncts()
    # listDictRefsToDict()
    # trans_finder.saveMasterDict()
    # exit(0)

    try:

        # is_debug = ('vr_scene_inspection' in docname)
        # if is_debug:
        #     dd('DEBUG')
        #
        # ex_env_key = 'EX_PO_TRANS'
        # is_ex_env_set = (ex_env_key in os.environ)
        # if not is_ex_env_set:
        #     return
        # ex_env_key_value = os.environ[ex_env_key]
        # is_ex_set_true = (ex_env_key_value.lower() == 'true')
        # if not is_ex_set_true:
        #     return
        #
        # debug_file = cm.debug_file
        # if debug_file:
        #     is_debug_file = (debug_file in docname)
        #     if not is_debug_file:
        #         return
        #
        #
        for node, msg in extract_messages(doctree):
            msg = msg.strip()
            # dd("=" * 80)
            # dd("msgid:[{}]".format(msg))

            # clean up po file

            is_inline = isinstance(node, nodes.inline)
            is_emphasis = isinstance(node, nodes.emphasis)
            is_title = isinstance(node, nodes.title)
            is_term = isinstance(node, nodes.term)
            is_rubric = isinstance(node, nodes.rubric)
            is_field_name = isinstance(node, nodes.field_name)
            is_reference = isinstance(node, nodes.reference)
            is_strong = isinstance(node, nodes.strong)

            is_keep_original = (is_inline or
                                is_emphasis or
                                is_title or
                                is_term or
                                is_rubric or
                                is_field_name or
                                is_reference or
                                is_strong
                                )

            tran = None
            # is_debug = ('Get involved in discussions' in msg)
            # if is_debug:
            #     dd('DEBUG')
            is_ignore = ig.isIgnored(msg)
            if is_ignore:
                print(f'IGNORED: {msg}')
                continue

            # is_added = False
            pr = PR(msg, translation_engine=trans_finder)
            pr.translateAsIs()
            tran = pr.getTranslation()

            has_translation = (tran is not None)
            if has_translation:
                result_list.updateTranslation(msg, tran)
                # has_month = ('Tháng ' in tran)
                # has_original = (msg.lower() in tran.lower())
                # has_link = (df.REF_LINK.search(tran) is not None)
                # can_ignore = (has_month or has_original or has_link)
                # is_repeat = is_keep_original and not can_ignore
                # if is_repeat:
                #     tran = cm.matchCase(msg, tran)
                #     tran = f'{tran} -- {msg}'
                #     print(f'Repeating MSG:{tran}')
                # else:
                #     print(f'Found translation:{tran}')

        # dd('DEBUG')
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


def builder_inited(app):
    # trans_finder.loadVIPOtoDic(trans_finder.master_dic_list, trans_finder.master_dic_file, is_testing=True)
    # trans_finder.updateMasterDic(is_testing=True)
    # exit(0)
    # trans_finder.mergePODict()
    pass
    # blender_manual_po_data = c.load_po(blender_manual_po_path)


def env_updated(app, env):
    pass


def build_finished(app, exeption):
    pass

def setup(app):
    # app.connect('builder-inited', builder_inited)
    # app.connect('doctree-resolved', doctree_resolved)
    # app.connect('build-finished', build_finished)
    # app.connect('env-updated', env_updated)
    # env-updated

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
