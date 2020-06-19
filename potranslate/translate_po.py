# -*- coding: utf-8 -*-
#!/usr/local/bin/python3

import sys
sys.path.append('/usr/local/lib/python3.7/site-packages')
sys.path.append('/Users/hoangduytran/blender_manual/potranslate')
# print(sys.path)

# sys.path.append('/home/htran/bin/python/PO')
# sys.path.append('/home/htran/bin/python/base')
# sys.path.append('/home/htran/bin/python/algorithm')
# sys.path.append('/home/htran/bin/python/event')
# sys.path.append('/usr/lib/python36.zip')
# sys.path.append('/usr/lib/python3.6)
# sys.path.append('/usr/lib/python3.6/lib-dynload')
# sys.path.append('/usr/local/lib/python3.6/dist-packages')
# sys.path.append('/usr/lib/python3/dist-packages')
# sys.path.append('/usr/lib/python3.6/dist-packages')

import os
import re

# print("import fine so far")
from ignore import Ignore as ig
from common import Common as cm
from common import DEBUG, _, pp
from docutils import nodes
from sphinx.util.nodes import extract_messages
from translation_finder import TranslationFinder as tf
from ignore import Ignore as ig
from collections import OrderedDict, defaultdict
import json
from reflink import RefList, RefRecord, RefItem
from reftype import RefType
from sphinx_intl import catalog as c
from pyparsing import *
from babel.messages.catalog import Message, Catalog
import locale
import datetime
from time import gmtime, strftime, time
from pytz import timezone
import Levenshtein as LE
from pprint import pprint as PP

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

def doctree_resolved(app, doctree, docname):

    def abbreviating():
        remove_items = []
        new_items = {}

        for k, v in trans_finder.master_dic_list.items():
            ref_list = RefList(msg=v)
            new_v = ref_list.quotedToAbbrev(k)
            has_new_v = (new_v is not None) and (len(new_v) > 0)
            if has_new_v:
                new_entry = {k: new_v}
                new_items.update(new_entry)

        has_remove_items = (len(remove_items) > 0)
        if has_remove_items:
            for k in remove_items:
                _(f'Delete from dictionary:[{k}]')
                del trans_finder.master_dic_list[k]

        is_writing_changes = (len(new_items) > 0)
        if is_writing_changes:
            trans_finder.master_dic_list.update(new_items)
            dic_file = '/Users/hoangduytran/blender_manual/test_dic.json'
            print(f'Writing changes to: {dic_file}, number of records:{len(new_items)}')
            trans_finder.writeJSONDic(dict_list=trans_finder.master_dic_list, file_name=dic_file)

    def checkDictKeyboard():
        for k, v in trans_finder.master_dic_list.items():
            k_list = RefList(msg=k, tf=trans_finder)
            k_list.parseMessage()
            v_list = RefList(msg=v, tf=trans_finder)
            v_list.parseMessage()

            is_debug = ('in development' in k)
            if is_debug:
                _('DEBUG')
            k_kbd_list = k_list.getListOfKeyboard(is_translate=True)
            v_kbd_list = v_list.getListOfKeyboard()
            is_same = (k_kbd_list == v_kbd_list)
            if not is_same:
                print(f'en:{k_kbd_list}')
                print(f'vn:{v_kbd_list}')
                print(f'diff:{k} => {v}')
                print('-----')

    def checkDictRef():
        for k, v in trans_finder.master_dic_list.items():
            k_list = RefList(msg=k, tf=trans_finder)
            k_list.parseMessage()
            v_list = RefList(msg=v, tf=trans_finder)
            v_list.parseMessage()

            k_ref_list = k_list.getListOfRefs()
            v_ref_list = v_list.getListOfRefs()
            is_same = (k_ref_list == v_ref_list)

            is_ignore = (len(k_ref_list) == 0)
            is_ignored = (is_ignore or is_same)
            if is_ignored:
                continue

            PP(k_ref_list)
            print('--')
            PP(v_ref_list)
            print('--')
            print(f'{k}\n\n{v}')
            print('--------')

    def checkNonTranslatedDictWords():
        for k, v in trans_finder.master_dic_list.items():
            k_list = RefList(msg=k, tf=trans_finder)
            k_list.parseMessage()
            v_list = RefList(msg=v, tf=trans_finder)
            v_list.parseMessage()

            k_ref_list = k_list.getListOfNonRefWords()
            v_ref_list = v_list.getListOfNonRefWords()

            repeat_list=[]
            is_repeat = False
            for word in k_ref_list:
                is_found = (word in v_ref_list)
                if is_found:
                    if word not in repeat_list:
                        print(f'{word}')
                        repeat_list.append(word)
                    is_repeat = True

            if not is_repeat:
                continue

            # print(k_ref_list)
            print('-'*3)
            # print(v_ref_list)
            # print('--')
            print(f'{k}\n\n{v}')
            print('-'*40)

    def checkDictForMultipleMeaningsInTrans():
        pattern = re.compile(r'(\w+(/\w+)+)')
        k: str = None
        v: str = None
        for k, v in trans_finder.master_dic_list.items():
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

        for k, v in trans_finder.master_dic_list.items():
            # is_debug = ('Cut to' in k)
            # if is_debug:
            #     _('DEBUG')

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
            del trans_finder.master_dic_list[k]
            changed = True

        for k, v in add_set.items():
            add_entry = {k:v}
            trans_finder.master_dic_list.update(add_entry)
            print(f'added: {add_entry}')
            changed = True

        if changed:
            new_dict = cleanupLeadingTrailingPunct(trans_finder.master_dic_list)
            test_to_file='/Users/hoangduytran/blender_manual/ref_dict_0005.json'
            trans_finder.writeJSONDic(dict_list=new_dict, file_name=test_to_file)

    def removeDuplication(txt_with_punct):
        # is_debug = (txt_with_punct.endswith('::'))
        # if is_debug:
        #     _('DEBUG')
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
        ref : RefRecord = None
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
                _('DEBUG')

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
                _(f'{type} is not the type we are looking for.')
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
        for k, v in trans_finder.master_dic_list.items():
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
        trans_finder.addDictEntry((msg, tran))
        print("Got translation from REF_LIST")
        return tran

    def fuzzyTextSimilar(txt1 : str, txt2 : str, accept_ratio):
        try:
            similar_ratio = LE.ratio(txt1, txt2)
            is_similar = (similar_ratio >= accept_ratio)
            return is_similar
        except Exception as e:
            print(e)
            return False

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

    debug_file = cm.debug_file
    if debug_file:
        is_debug_file = (debug_file in docname)
        if not is_debug_file:
            return

    build_dir = "build/rstdoc"
    po_vi_dir = "locale/vi/LC_MESSAGES"

    po_file_path = "{}.po".format(docname)
    local_path = os.path.dirname(os.path.abspath(__file__))
    blender_docs_path = os.path.dirname(local_path)

    locale_vi_path = "locale/vi/LC_MESSAGES"

    po_path = os.path.join(blender_docs_path, os.path.join(locale_vi_path, po_file_path))

    if not os.path.isfile(po_path):
        raise Exception("po_path:", po_path, " NOT FOUND!")
        exit(0)

    # with open(po_path, "r") as f:
    #     data = f.read()
    # data_list=data.split('\n')
    # pp(data)
    # exit(0)

    # #trans_finder.cleanupPOFile(po_path, is_dry_run=False)
    # replace_dict = {
    #     #r'':r''
    #    #r'Language-Team.*MIME-Version':r'Language-Team: London, UK <hoangduytran1960@gmail.com>\\n"\n"Plural-Forms: nplurals=1; plural=0\\n"\n"MIME-Version',
    #    r'Language-Team.*MIME-Version':r'Something'
    # }
    # trans_finder.replacePOText(po_path, replace_dict, is_dry_run=True)

    # cm.file_count += 1
    # is_pausing = (cm.file_count == (cm.total_files / 10))
    # if is_pausing:
    #     nb = input("Press any key to continue:")
    #     cm.file_count = 0

    # #loading local po file to get translation if any
    po_dic, current_po_cat = trans_finder.loadPOAsDic(po_path)

    rst_output_location = os.path.join(blender_docs_path, build_dir)
    output_path = os.path.join(rst_output_location, po_file_path)

    local_time = timezone(TIME_ZONE)
    time_now = local_time.localize(datetime.datetime.now())

    local_locale = locale.getlocale()[0]
    current_header = current_po_cat._get_header_comment()
    new_po_cat = Catalog(
        locale="vi",
        header_comment=current_header,
        project=current_po_cat.project,
        version=current_po_cat.version,
        copyright_holder=YOUR_ID,
        creation_date=current_po_cat.creation_date,
        revision_date=time_now,
        last_translator=YOUR_ID,
        language_team=YOUR_TRANSLATION_TEAM
    )

    _("#" * 80)
    _("filename: {}".format(output_path))

    # msgid = "Lines should be less than 120 characters long."
    # msgstr = "Số chữ trong các dòng phải ít hơn 120 ký tự de lam gi."
    # trans_finder.addDictEntry((msgid, msgstr), False)
    # exit(0)

    for node, msg in extract_messages(doctree):
        msg = msg.strip()
        _("=" * 80)
        _("msgid:[{}]".format(msg))

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
        #     _('DEBUG')
        is_ignore = ig.isIgnored(msg)
        if is_ignore:
            print(f'IGNORED: {msg}')
            continue

        # is_added = False
        tran, is_ignore = trans_finder.findTranslation(msg)
        if is_ignore:
            continue

        has_translation = (tran is not None)
        if not has_translation:
            tran = tranRef(msg, is_keep_original)
            has_translation = (tran is not None)
            if not has_translation:
                tran = po_dic[msg]

        has_translation = (tran is not None)
        if has_translation:
            has_month = ('Tháng ' in tran)
            has_original = (msg.lower() in tran.lower())
            has_link = (cm.REF_LINK.search(tran) is not None)
            can_ignore = (has_month or has_original or has_link)
            is_repeat = is_keep_original and not can_ignore
            if is_repeat:
                print('Repeating MSG')
                tran = cm.matchCase(msg, tran)
                tran = f'{tran} -- {msg}'
                print(f'Repeating MSG:{tran}')

        if tran is not None:
            new_po_cat.add(msg, string=tran)
        else:
            new_po_cat.add(msg, string="")

        print(f'msgid \"{msg}\"')
        if tran is not None:
            print(f'msgstr \"{tran}\"')
        else:
            print('msgstr \"\"')

    print("Output to the path:", new_po_cat, output_path)
    # c.dump_po(output_path, new_po_cat, line_width=1024)
    c.dump_po(output_path, new_po_cat)
    # _('DEBUG')


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


def env_updated(app, env):
    pass


def build_finished(app, exeption):
    def refListGetKey(item):
        return item[1]

    def dicListGetKey(item):
        k, v = item
        trans, rep = v
        return rep

    # loc_dic_list={}
    # sorted_list = sorted(trans_finder.dic_list.items(), key=refListGetKey)
    # # pp(sorted_list)
    # for txt, rep in sorted_list:
    #     if ig.isIgnored(txt):
    #         continue
    #
    #     #txt = txt.strip()
    #     must_mark = False
    #     trans = trans_finder.findTranslation(txt)
    #     if not trans:
    #         trans = trans_finder.findTranslationByFragment(txt)
    #         must_mark = True
    #
    #     #is_same = (txt == trans)
    #     k = txt
    #     if (rep > 1) or must_mark:
    #         if trans is None:
    #             trans = ""
    #         v = "{}#{}#".format(trans, rep)
    #     else:
    #         v = trans
    #     entry={k:v}
    #     loc_dic_list.update(entry)

    # sorted_list = sorted(loc_dic_list.items(), key=dicListGetKey)

    # return

    # file_name = "/Users/hoangduytran/ref_dict_0001.json"
    # dic = cm.removeLowerCaseDic(loc_dic_list)
    # dic = trans_finder.master_dic_backup_list
    # dic.update(trans_finder.master_dic_list)

    # dic = trans_finder.dic_list
    # has_dic = (len(dic) > 0)
    # if not has_dic:
    #     return

    # clean_dic = trans_finder.removeIgnoredEntries(dic)
    # dic = clean_dic
    # pp(dic)
    # exit(0)
    # sorted_list = sorted(dic.items(), key=lambda x: x[1])

    # dic = trans_finder.master_dic_backup_list
    # file_name = trans_finder.master_dic_backup_file
    # print("Writing dictionary to:", file_name)
    # with open(file_name, 'w', newline='\n', encoding='utf8') as out_file:
    #     json.dump(dic, out_file, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

    # with open(file_name, "r") as f:
    #     data = json.load(f)

    # pp(data)

    # for k, v in data.items():
    #     is_null = (v == None)
    #     if is_null:
    #         entry={k:""}
    #         print("updating entry:", entry)
    #         data.update(entry)

    # with open(file_name, 'w', newline='\n', encoding='utf8') as out_file:
    #     json.dump(dic, out_file, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

    # with open(file_name, 'w', newline='\n', encoding='utf8') as out_file:
    #     json.dump(dic, out_file, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

    # trans_finder.writeJSONDic(dic_list=sorted_list, file_name="/home/htran/20191228_dict_0001.json")
    # pp(sorted_list)
    # exit(0)
    trans_finder.writeChosenDict(is_master=True)
    trans_finder.writeChosenDict(is_master=False)
    # trans_finder.writeBackupDict()
    # trans_finder.writeMasterDict()
    _('DEBUG')


def setup(app):
    app.connect('builder-inited', builder_inited)
    app.connect('doctree-resolved', doctree_resolved)
    app.connect('build-finished', build_finished)
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
