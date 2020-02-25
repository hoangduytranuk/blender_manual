# -*- coding: utf-8 -*-

import sys
sys.path.append('/Users/hoangduytran/PycharmProjects/potranslate')
print(sys.path)

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

print("import fine so far")
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
from pyparsing import *

try:
    import html
except ImportError:
    html = None

trans_finder = tf()


def doctree_resolved(app, doctree, docname):
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


    #loading local po file to get translation if any
    po_dic = trans_finder.loadPOAsDic(po_path)

    rst_output_location = os.path.join(blender_docs_path, build_dir)
    output_path = os.path.join(rst_output_location, po_file_path)

    #_("#" * 80)
    _("filename: {}".format(output_path))

    for node, msg in extract_messages(doctree):
        # msg = unescape(msg).strip()
        msg = msg.strip()
        _("=" * 80)
        #_("msgid:[{}]".format(msg))

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

        # MAYBE !!! should partitioning sentences at the punctuation mark's boundaries, so you can
        # retrieve sentence level translations. Done for none ref-links text parts.

        is_empty = (len(msg) == 0)
        is_ignored = is_empty or ig.isIgnored(msg)
        if is_ignored:
            print("IGNORED:", msg)
            continue

        has_translation = (msg in po_dic)
        if has_translation:
            tran = po_dic[msg]
            is_added = trans_finder.addEntryToDic(msg, tran, trans_finder.master_dic_backup_list)
            if is_added:
                entry = (msg, tran)
                print("found in PO, added entry:", entry)
            else:
                has_translation = (msg in trans_finder.master_dic_list)
                if has_translation:
                    tran = trans_finder.master_dic_list[msg]
                    is_added = trans_finder.addEntryToDic(msg, tran, trans_finder.master_dic_backup_list)
                    if is_added:
                        entry = (msg, tran)
                        print("found in master_dic_list, added entry:", entry)
                    else:
                        ref_list = RefList(msg, translation_finder=trans_finder, keep_orig=is_keep_original)
                        ref_list.parseMessage()
                        ref_list.translateRefList()
                        #_(ref_list)
                        ref_list.dumpRefList(trans_finder.master_dic_backup_list)




def builder_inited(app):
    trans_finder.mergePODict()

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
    

    file_name = "/Users/hoangduytran/ref_dict_0001.json"
    # dic = cm.removeLowerCaseDic(loc_dic_list)
    dic = trans_finder.master_dic_backup_list
    dic.update(trans_finder.master_dic_list)

    # dic = trans_finder.dic_list
    has_dic = (len(dic) > 0)
    if not has_dic:
        return


    #clean_dic = trans_finder.removeIgnoredEntries(dic)
    #dic = clean_dic
    #pp(dic)
    #exit(0)
    #sorted_list = sorted(dic.items(), key=lambda x: x[1])
    print("Writing dictionary to:", file_name)
    with open(file_name, 'w', newline='\n', encoding='utf8') as out_file:
        json.dump(dic, out_file, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
    
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
    #exit(0)

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
