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

try:
    import html
except ImportError:
    html = None

YOUR_NAME = "Hoang Duy Tran"
YOUR_EMAIL = "hoangduytran1960@gmail.com"
YOUR_ID = "{} <{}>".format(YOUR_NAME, YOUR_EMAIL)
YOUR_TRANSLATION_TEAM = "London, UK <{}>".format(YOUR_EMAIL)
YOUR_LANGUAGE_CODE = "vi"
TIME_ZONE='Europe/London'
trans_finder = tf()

def doctree_resolved(app, doctree, docname):

    def getTimeNow(self):
        local_time=timezone('Europe/London')
        fmt='%Y-%m-%d %H:%M%z'
        loc_dt=local_time.localize(datetime.datetime.now())
        formatted_dt=loc_dt.strftime(fmt)
        return formatted_dt

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
    current_po_cat : Catalog = c.load_po(po_path)
    rst_output_location = os.path.join(blender_docs_path, build_dir)
    output_path = os.path.join(rst_output_location, po_file_path)

    local_time=timezone(TIME_ZONE)
    time_now =local_time.localize(datetime.datetime.now())

    local_locale = locale.getlocale()[0]
    current_header = current_po_cat._get_header_comment()
    new_po_cat = Catalog(
                locale="vi",
                header_comment=current_header,
                project="Blender 2.8 Manual",
                version="2.8",
                copyright_holder=YOUR_ID,
                creation_date=current_po_cat.creation_date,
                revision_date=time_now,
                last_translator=YOUR_ID,
                language_team=YOUR_TRANSLATION_TEAM,
                charset="UTF-8"
                )

    _("#" * 80)
    _("filename: {}".format(output_path))

    for node, msg in extract_messages(doctree):
        # msg = unescape(msg).strip()
        msg = msg.strip()
        #_("=" * 80)
        #_("msgid:[{}]".format(msg))

        #clean up po file


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


        #clean up po


        # msg = "The *Bake Action* tool will apply interpolated frames into individual keyframes. This can be useful for adding deviation to a cyclic action like a :term:`walk cycle`. This can also useful for keyframe animations created from drivers or constraints."
        # ref_list = RefList(msg, translation_finder=trans_finder, keep_orig=is_keep_original)
        # ref_list.parseMessage()
        # ref_list.translateRefList()
        # #_(ref_list)
        # ref_list.dumpRefList(trans_finder.master_dic_backup_list)

        # return

        msg = ":abbr:`IES (Illuminating Engineering Society of North America)`, :abbr:`TL;DR (Too long; didn't read.)`, use *Crop* and/or *Offset* in the Input panel to move and select a region of the image within the output. When you use *Crop* or *Offset*, the auto-scaling will be disabled and you can manually re-scale by adding the Transform effect. ``TEXT``, ``MTEXT``, **1.30 -- April 1998:**, also :kbd:`Shift-W` :menuselection:`--> (Deform, ...)`, **Always** position ``-f`` or ``-a`` as the last arguments. *Push/Pull*, ``/tmp``, 1.0×10\ :sup:`15`, :class:`blender_api:bpy.types.KeyMapItem`, :doc:`3D View Alignment </editors/3dview/navigate/align>`, :kbd:`Alt-MMB`, :menuselection:`Armature --> Transform --> Align Bones`, :menuselection:`... --> Show/Hide`, :menuselection:`Add`, :ref:`Knife <tool-mesh-knife>`, :ref:`3dview-nav-zoom-region`. :ref:`Push/Pull <tool-transform-push_pull>`, :term:`non-manifold`,  :term:`Anti-aliasing`, :term:`Color Space`. :term:`Camera Projections <projection>`"

        ref_list = RefList(msg, translation_finder=trans_finder, keep_orig=is_keep_original)
        ref_list.parseMessage()
        ref_list.translateRefList()
        # _(ref_list)
        #ref_list.dumpRefList(trans_finder.master_dic_backup_list)
        return

        orig_msg = str(msg)

        is_ignore = ig.isIgnored(msg)
        if is_ignore:
            tran = None
        else:
            # print("Not ignore:", msg)
            is_added = False
            has_translation = (msg in po_dic)
            if has_translation:
                tran = po_dic[msg]
                is_added = trans_finder.addEntryToDic(msg, tran, trans_finder.master_dic_backup_list)
                if is_added:
                    entry = (msg, tran)
                    print("found in PO, added entry:", entry)
            else:
                has_translation = (not is_added) and (msg in trans_finder.master_dic_list)
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

        exit(0)
        # if not is_ignore:
        #     has_translation = (msg in trans_finder.master_dic_list)
        #     if has_translation:
        #         tran = trans_finder.master_dic_list[msg]
        #         if is_keep_original:
        #             if tran:
        #                 has_orig = cm.hasOriginal(msg, tran)
        #                 if not has_orig:
        #                     tran = "{} -- {}".format(tran, msg)
        #             else:
        #                 tran = "-- {}".format(msg)
        #         print("Origianl translation:",msg, "=>", tran)
        #     else:
        #         ref_list = RefList(msg, translation_finder=trans_finder, keep_orig=is_keep_original)
        #         ref_list.parseMessage()
        #         ref_list.translateRefList()
        #         tran = ref_list.getTranslation()

        #         print("ref_list translation:",msg, "=>", tran)
        #         is_same = cm.isTextuallySame(msg, tran)
        #         if is_same:
        #             tran = None

        # else:
        #     tran = None

        # if tran is not None:
        #     is_same = cm.isTextuallySame(msg, tran)
        #     if not is_same:
        #         new_po_cat.add(msg, string=tran)
        #         if not is_ignore:
        #             entry={msg:tran}
        #             trans_finder.master_dic_backup_list.update(entry)
        # else:
        #     new_po_cat.add(msg, string="")
        #     if not is_ignore:
        #         entry={msg:""}
        #         trans_finder.master_dic_backup_list.update(entry)

    #     print("msgid \"", msg, "\"")
    #     if tran is not None:
    #         print("msgstr \"", tran, "\"")
    #     else:
    #         print("msgstr \"\"")

    # print("Output to the path:", new_po_cat, output_path)
    # c.dump_po(output_path, new_po_cat)





def builder_inited(app):
    #trans_finder.mergePODict()
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

    #file_name = "/Users/hoangduytran/ref_dict_0001.json"
    # dic = cm.removeLowerCaseDic(loc_dic_list)
    # dic = trans_finder.master_dic_backup_list
    # dic.update(trans_finder.master_dic_list)

    # dic = trans_finder.dic_list
    # has_dic = (len(dic) > 0)
    # if not has_dic:
    #     return


    #clean_dic = trans_finder.removeIgnoredEntries(dic)
    #dic = clean_dic
    #pp(dic)
    #exit(0)
    #sorted_list = sorted(dic.items(), key=lambda x: x[1])
    dic = trans_finder.master_dic_backup_list
    file_name = trans_finder.master_dic_backup_file
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
