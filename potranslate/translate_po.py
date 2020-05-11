# -*- coding: utf-8 -*-
#!/usr/bin/env python3

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
from sphinx_intl import catalog as c
from pyparsing import *
from babel.messages.catalog import Message, Catalog
import locale
import datetime
from time import gmtime, strftime, time
from pytz import timezone
import Levenshtein as LE

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
    def removeDuplication(txt_with_punct):
        # is_debug = (txt_with_punct.endswith('::'))
        # if is_debug:
        #     _('DEBUG')
        cropped_txt, begin_with_punctuations, ending_with_punctuations = cm.beginAndEndPunctuation(txt_with_punct,
                                                                                                   is_single=True)
        trans = trans_finder.isInList(cropped_txt, is_lower=True)
        is_repeat = (trans is not None)
        if not is_repeat:
            cropped_txt, begin_with_punctuations, ending_with_punctuations = cm.beginAndEndPunctuation(txt_with_punct,
                                                                                                       is_single=False)
            trans = trans_finder.isInList(cropped_txt, is_lower=True)

        is_repeat = (trans is not None)
        return is_repeat

    def correctingDictionary():
        remove_items = []
        new_items = {}
        for k, v in trans_finder.master_dic_list.items():
            is_end_with_dot = (k.endswith('.') and not (k.endswith('..') or k.endswith('...')))
            if is_end_with_dot:
                txt_without_dot = k[:-1]
                is_repeat = (txt_without_dot in trans_finder.master_dic_list) and (k in trans_finder.master_dic_list)
                if (is_repeat):
                    remove_items.append(k)
                    _(f'ignore this message: [{k}]')
                    continue

            ref_list = RefList(msg=v)
            new_v = ref_list.quotedToAbbrev(k)
            has_new_v = (new_v is not None)
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
        exit(0)

    def tranRef(msg, is_keep_original):
        ref_list = RefList(msg=msg, keep_orig=is_keep_original, tf=trans_finder)
        ref_list.parseMessage()
        ref_list.translateRefList()
        tran = ref_list.getTranslation()
        print("Got translation from REF_LIST")
        return tran

    def fuzzyTextSimilar(txt1, txt2, accept_ratio):
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

    correctingDictionary()

    debug_file = cm.debug_file
    if debug_file:
        is_debug_file = (debug_file == docname)
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
    po_dic = trans_finder.loadPOAsDic(po_path)
    current_po_cat: Catalog = c.load_po(po_path)

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

        # MAYBE !!! should partitioning sentences at the punctuation mark's boundaries, so you can
        # retrieve sentence level translations. Done for none ref-links text parts.

        # is_empty = (len(msg) == 0)
        # is_ignored = is_empty or ig.isIgnored(msg)
        # if is_ignored:
        #     # print("IGNORED:", msg)
        #     continue

        # clean up po

        # msg = "The *Bake Action* tool will apply interpolated frames into individual keyframes. This can be useful for adding deviation to a cyclic action like a :term:`walk cycle`. This can also useful for keyframe animations created from drivers or constraints."
        # ref_list = RefList(msg, translation_finder=trans_finder, keep_orig=is_keep_original)
        # ref_list.parseMessage()
        # ref_list.translateRefList()
        # #_(ref_list)
        # # ref_list.dumpRefList(trans_finder.master_dic_backup_list)
        #
        # return

        # msg = ":abbr:`IES (Illuminating Engineering Society of North America)`, :abbr:`TL;DR (Too long; didn't read.)`, use *Crop* and/or *Offset* in the Input panel to move and select a region of the image within the output. When you use *Crop* or *Offset*, the auto-scaling will be disabled and you can manually re-scale by adding the Transform effect. ``TEXT``, ``MTEXT``, **1.30 -- April 1998:**, also :kbd:`Shift-W` :menuselection:`--> (Deform, ...)`, **Always** position ``-f`` or ``-a`` as the last arguments. *Push/Pull*, ``/tmp``, 1.0×10\ :sup:`15`, :class:`blender_api:bpy.types.KeyMapItem`, :doc:`3D View Alignment </editors/3dview/navigate/align>`, :kbd:`Alt-MMB`, :menuselection:`Armature --> Transform --> Align Bones`, :menuselection:`... --> Show/Hide`, :menuselection:`Add`, :ref:`Knife <tool-mesh-knife>`, :ref:`3dview-nav-zoom-region`. :ref:`Push/Pull <tool-transform-push_pull>`, :term:`non-manifold`,  :term:`Anti-aliasing`, :term:`Color Space`. :term:`Camera Projections <projection>`"

        # has_translation = (msg in po_dic)
        # if has_translation:
        #     current_tran = po_dic[msg]
        #     ref_list = RefList(msg, translation_finder=trans_finder, keep_orig=is_keep_original)
        #     ref_list.transferTranslatedRefs(msg, current_tran)
        # else:
        #     print("Not transfer:", msg)

        # ref_list = RefList(msg, translation_finder=trans_finder, keep_orig=is_keep_original)
        #
        # ref_list.transferTranslatedRefs(msg, )
        # ref_list.parseMessage()
        # ref_list.translateRefList()
        # # _(ref_list)
        # #ref_list.dumpRefList(trans_finder.master_dic_backup_list)
        # return

        # msg = "LimbNode' FBX node, a regular joint between two bones..."
        tran = None
        orig_msg = str(msg)

        is_ignore = ig.isIgnored(msg)
        if is_ignore:
            continue
        else:
            # print("Not ignore:", msg)
            is_added = False
            has_translation = (msg in po_dic)
            if has_translation:
                tran = po_dic[msg]
                is_too_similar = fuzzyTextSimilar(msg, tran, 0.8)
                if is_too_similar:
                    tran = tranRef(msg, is_keep_original)
                else:
                    entry = {msg: tran}
                    trans_finder.master_dic_list.update(entry)
                    print("Got translation from PO file")
            else:
                has_translation = (not is_added) and (msg in trans_finder.master_dic_list)
                if has_translation:
                    tran = trans_finder.master_dic_list[msg]
                    is_too_similar = fuzzyTextSimilar(msg, tran, 0.8)
                    if is_too_similar:
                        tran = tranRef(msg, is_keep_original)
                    else:
                        print("Got translation from MASTER_DIC_LIST")
                else:
                    tran = tranRef(msg, is_keep_original)

        if tran is not None:
            new_po_cat.add(msg, string=tran)
        else:
            new_po_cat.add(msg, string="")

        print("msgid \"", msg, "\"")
        if tran is not None:
            print("msgstr \"", tran, "\"")
        else:
            print("msgstr \"\"")

    print("Output to the path:", new_po_cat, output_path)
    # c.dump_po(output_path, new_po_cat, line_width=1024)
    # c.dump_po(output_path, new_po_cat, line_width=4096)


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
