import os
import io
import re
import json
from common import Common as cm
from pobase import POBasic
import docutils
from docutils import nodes
from sphinx import addnodes, roles
from pprint import pprint as PP
from six import text_type
from sphinx.util.nodes import extract_messages, traverse_translatable_index
from distutils import log as logger
from sphinx.locale import _, __
from sphinx_intl import catalog as c
from babel.messages import pofile
from babel.messages.catalog import Message, Catalog
from pprint import pprint as pp
from googletrans import Translator as GTR

#from Levenshtein import distance as DS
from markupsafe import Markup
try:
    import html
except ImportError:
    html = None

unescape = getattr(html, 'unescape', None)
if unescape is None:
    # HTMLParser.unescape is deprecated since Python 3.4, and will be removed
    # from 3.9.
    unescape = html_parser.HTMLParser().unescape


# sudo apt install python-pip python3-pip
# pip3 install googletrans
from googletrans import Translator

use_google_translate = False

class TranslationFinder:
    def __init__(self):
        self.dic_path = "/home/htran/blender_documentations/new_po/vi.po"
        self.current_po_dir = "/home/htran/blender_documentations/blender_docs/locale/vi/LC_MESSAGES"
        self.json_dic_file = "/home/htran/Documents/menuselection_new_dictionary_sorted_translated_0028.json"

        self.json_dic_list = self.loadJSONDic()
        self.json_dic_list_lower = self.makeJSONLowerCaseDic(self.json_dic_list)
        self.dic_cat = c.load_po(self.dic_path)
        self.dic_cat_lower = self.poCatDictLower(self.dic_cat)
        self.translated_po_dic = None
        self.translated_po_dic_lower = None
        self.translated_po_dic, self.translated_po_dic_lower = self.loadTranslatedPO()
        self.tr = Translator()

        #po_dic = self.poCatToList(dic_cat)

        #po_dic_lower = self.poCatToListLower(dic_cat)
        #sorted_po_dic = sorted(po_dic)
        #PP(po_dic_lower)
        #sorted_lower_po_dic = sorted(po_dic_lower)

    def removeJSONDicNoTranslation(self, dic):
        dic_removable=[]
        for k,v in dic.items():
            has_translation = (len(v)>0)
            if not has_translation:
                dic_removable.append(k)

        new_dic = dic
        for k in dic_removable:
            new_dic.pop(k)
        return new_dic

    def makeJSONLowerCaseDic(self, dic):
        lcase_dic={}
        for k,v in dic.items():
            lk = k.lower()
            lv = v
            lcase_dic.update({lk:lv})
        #PP(lcase_dic)
        #exit(0)
        return lcase_dic

    def loadJSONDic(self, file_name=None):
        dic = None
        try:
            file_path = (self.json_dic_file if (file_name == None) else file_name)
            with open(file_path) as in_file:
                dic = json.load(in_file)
                if dic:
                    print("Loaded:{}".format(len(dic)))
                else:
                    raise Exception("dic [{}] is EMPTY. Not expected!", file_path)
        except Exception as e:
            print("Exception readDictionary Length of read dictionary:")
            print(e)
            raise e

        dic = self.removeJSONDicNoTranslation(dic)
        print("after cleaned:{}".format(len(dic)))
        return dic


    def POContentToDic(self, po_cat, dict, dict_lowercase):
        for m in po_cat:
            k = m.id
            v = m.string
            # is_debug = ("POV" in k)
            # if is_debug:
            #     print("{} => {}".format(k, v))
            #     exit(0)

            has_trans = v and (len(v) > 0)
            if (has_trans):
                is_same = (k == v)
                if (is_same):
                    continue
                else:
                    dict.update({k:m})
                    dict_lowercase.update({k.lower():m})


    def loadTranslatedPO(self):
        all_po_dict={}
        all_po_dict_lower = {}
        getter = POBasic(self.current_po_dir, False)
        po_dir_list = getter.getSortedPOFileList()
        for(index, po_file_path) in enumerate(po_dir_list):
            if (len(po_file_path) <= 0):
                continue
            po_cat = c.load_po(po_file_path)
            self.POContentToDic(po_cat, all_po_dict, all_po_dict_lower)

        # print("all_po_dict:")
        # pp(all_po_dict)
        # exit(0)
        return all_po_dict, all_po_dict_lower

    def poCatToList(self, po_cat):
        l = []
        for index, m in enumerate(po_cat):
            k = m.id
            v = m
            l.append((k, v))
        return l

    def poCatToListLower(self, po_cat):
        l = []
        for index, m in enumerate(po_cat):
            k = m.id.lower()
            v = m
            l.append((k, v))
        return l

    def poCatDictLower(self, po_cat):
        l = {}
        for index, m in enumerate(po_cat):
            k = m.id.lower()
            v = m
            l.update({k: v})
        return l

    # PP(sorted_lower_po_dic)

    def dump_po(self, filename, catalog):
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # Because babel automatically encode strings, file should be open as binary mode.
        with io.open(filename, 'wb') as f:
            pofile.write_po(f, catalog, width=4096)

    def translateKeyboard(self, kbd_ref):
        print("translateKeyboard:", kbd_ref)
        trans = cm.translateKeyboardDef(kbd_ref)
        print(kbd_ref, " => ", trans)
        return trans


    def translateDocRef(self, doc_ref):
        print("translateDocRef:", doc_ref)
        trans = str(doc_ref)

        is_a_packed_ref = (cm.PACKED_REF.search(doc_ref) != None)
        if is_a_packed_ref:
            print("PACKED REF, needed to expand further")

        for rl_start, rl_end, ref_link, rl_link_1 in cm.patternMatchAsList(cm.REF_LINKS, doc_ref):
            print("rl_start, rl_end, ref_link, rl_link_1")
            print(rl_start, rl_end, ref_link, rl_link_1)
            text_without_ref_link = doc_ref[:rl_start-1]
            print("text_without_ref_link:[{}]".format(text_without_ref_link))

            trans = self.findTranslation(text_without_ref_link)
            if not trans:
                trans = self.findTranslationByFragment(text_without_ref_link)

            if trans:
                trans = self.removeOriginal(text_without_ref_link, trans)
                trans = "{} -- {} {}".format(trans, text_without_ref_link, ref_link)
            else:
                trans = "-- {} {}".format(text_without_ref_link, ref_link)

        print("translateDocRef doc_ref:[{}] trans:[{}]".format(doc_ref, trans))

        return trans

    def translateMenu(self, menu_ref):
        print("translateMenu:", menu_ref)
        trans = str(menu_ref)
        item_list = menu_ref.split(" --> ")
        tr_list = []
        pp(item_list)
        for item in item_list:
            item = item.strip()
            tr = self.findTranslation(item)
            if not tr:
                tr = self.findTranslationByFragment(item)

            if tr:
                trans = "{} ({})".format(tr, item)
            else:
                trans = "({})".format(item)
            print("translateMenu trans:", trans)
            tr_list.append(trans)

        trans = " --> ".join(tr_list)
        print(menu_ref, " ==> ", trans)
        return trans

    def translateAbbrev(self, abbrev):
        print("translateAbbrev:", abbrev)
        trans = str(abbrev)

        for wo_start, wo_end, wo_match_0, wo_match_1 in cm.patternMatchAsList(cm.WORD_INSIDE_BRAKET, abbrev):
            print("wo_start, wo_end, wo_match_0, wo_match_1")
            print(wo_start, wo_end, wo_match_0, wo_match_1)

            trans = self.findTranslation(wo_match_1)
            if not trans:
                trans = self.findTranslationByFragment(wo_match_1)

            print("translateAbbrev trans:", trans)
            if trans:
                trans = self.removeOriginal(wo_match_1, trans)
                trans = "{} -- {}".format(trans, wo_match_1)
            else:
                trans = "-- {}".format(wo_match_1)
            start = wo_start+1
            end = wo_end-1
            trans = abbrev[:start] + trans + abbrev[end:]
            print("translateAbbrev trans:", trans)
        return trans

    def translateOtherRef(self, other_ref):
        # ``manual``
        # ``.rst``
        # ``C:\blender_docs\build\html``
        # `create a task <https://developer.blender.org/maniphest/task/edit/form/default/?project=PHID-PROJ-c4nvvrxuczix2326vlti>`
        # ``#docs``
        # ``build/html``
        # ``:kbd:`LMB``` -- keyboard and mouse shortcuts.
        # ``*Mirror*``


        print("translateOtherRef:", other_ref)
        trans = str(other_ref)

        has_ref_link = (cm.REF_LINKS.search(other_ref) != None)
        if has_ref_link:
            rl_start, rl_end, ref_link, rl_link_1 = cm.patternMatchAsParts(cm.REF_LINKS, other_ref)
            text_without_ref_link = other_ref[:rl_start] + other_ref[rl_end:]
            text_without_ref_link = text_without_ref_link.strip()
            print("rl_start, rl_end, ref_link, rl_link_1, text_without_ref_link")
            print(rl_start, rl_end, ref_link, rl_link_1, text_without_ref_link)
        else:
            text_without_ref_link = other_ref

        is_path = cm.isFilePath(text_without_ref_link)
        is_start_ignore = cm.isIgnoredIfStartsWith(text_without_ref_link)
        is_word_ignored = cm.isIgnoredWord(text_without_ref_link)
        is_ignored = is_path or is_start_ignore or is_word_ignored
        print("is_path, is_start_ignore, is_word_ignored")
        print(is_path, is_start_ignore, is_word_ignored)
        if is_ignored:
            return None

        print("text_without_ref_link:[{}]".format(text_without_ref_link))
        text_trans = self.findTranslation(text_without_ref_link)
        if not text_trans:
            text_trans = self.findTranslationByFragment(text_without_ref_link)

        if text_trans:
            text_trans = self.removeOriginal(text_without_ref_link, text_trans)
            #put back with ref_link here
            if has_ref_link:
                trans = "{} -- {} {}".format(text_trans, text_without_ref_link, ref_link)
            else:
                trans = "{} -- {}".format(text_trans, text_without_ref_link)
        else:
            if has_ref_link:
                trans = "-- {} {}".format(text_without_ref_link, ref_link)
            else:
                trans = "-- {}".format(text_without_ref_link)

        print("other_ref:", other_ref, "trans:", trans)

        # text_without_ref_link = cm.REF_LINKS.sub("", other_ref)
        # text_without_ref_link = text_without_ref_link.strip()
        # is_ignored = cm.isFilePath(text_without_ref_link)
        # if is_ignored:
        #     return None
        #
        # text_trans = self.findTranslation(text_without_ref_link)
        # if not text_trans:
        #     text_trans = self.findTranslationByFragment(text_without_ref_link)
        #
        # if text_trans:
        #     text_trans = self.removeOriginal(text_without_ref_link, text_trans)
        #     #put back with ref_link here
        #     trans = "{} -- {}".format(text_trans.strip(), text_without_ref_link.strip())
        #     print("other_ref:", other_ref, "trans:", trans)
        # else:
        # trans = None

        # for wo_start, wo_end, wo_match_0, wo_match_1 in cm.patternMatchAsList(cm.BUTTON_LABEL, other_ref):
        #     print("wo_match_0:", wo_match_0, "wo_match_1:", wo_match_1)


        # trans = " --> ".join(tr_list)
        # print(menu_ref, " ==> ", trans)
        return trans


    def translateReferences(self, ref_entry):
        # (67, 106, '``KHR_materials_pbrSpecularGlossiness``', None)
        # (0,66, ':menuselection:`File --> Import/Export --> glTF 2.0 (.glb, .gltf)`', ':menuselection:`File --> Import/Export --> glTF 2.0 (.glb, .gltf)`')
        # (130, 197, ':doc:`generic wrapper </addons/import_export/io_node_shaders_info>`', ':doc:`generic wrapper </addons/import_export/io_node_shaders_info>`')
        # (115, 169, ':ref:`easings <editors-graph-fcurves-settings-easing>`', ':ref:`easings <editors-graph-fcurves-settings-easing>`')
        # (176, 203, ':doc:`/interface/undo_redo`', ':doc:`/interface/undo_redo`')
        # (7, 31, ':ref:`timeline-playback`', ':ref:`timeline-playback`')
        # (0, 20, ':ref:`ui-data-block`', ':ref:`ui-data-block`')
        # (35, 43, ':kbd:`I`', ':kbd:`I`')
        # (69, 82, ':kbd:`Ctrl-G`', ':kbd:`Ctrl-G`')
        # (0, 14, ':kbd:`Shift-K`', ':kbd:`Shift-K`')
        # (90, 100, ':kbd:`LMB`', ':kbd:`LMB`')
        # (39, 47, '``.png``', None),
        # (41, 55, '``quit.blend``', None)
        # (48, 62, '``*-0001.jpg``', None)
        # (211, 251, '``filename + frame number + .extension``', None)
        # (552, 574, '``5 × 60 × 30 = 9000``', None)
        # (0, 43, '``new_length = real_length / speed_factor``', None)
        # (58, 109, '``<path of original footage>/BL_proxy/<clip name>``', None)
        # (0, 36, '``Read prefs: {DIR}/userpref.blend``', None)
        # (0, 31, '``found bundled python: {DIR}``', None)
        # ``:abbr:`SSAO (Screen Space Ambient Occlusion)```
        # start, end, match_0, match_1

        print("translateReferences:", ref_entry)
        start, end, match_0, match_1 = ref_entry

        print("start, end, match_0, match_1")
        print(start, end, match_0, match_1)

        is_doc = ":doc:" in match_0
        is_ref = ":ref:" in match_0
        is_kbd = ":kbd:" in match_0
        is_menu = ":menuselection:" in match_0
        is_abbrev = ":abbr:" in match_0
        is_term = ":term:" in match_0
        trans = str(ref_entry)

        print("is_menu:", is_menu)
        print("is_doc:", is_doc)
        print("is_kbd:", is_kbd)
        print("is_ref:", is_ref)
        print("is_abbrev:", is_abbrev)
        print("is_term:", is_term)

        is_two_ga = (cm.TWO_GA.search(match_0) != None)
        is_one_ga = (cm.ONE_GA.search(match_0) != None)
        if is_two_ga:
            print("TWO_GA")
            ref_list = cm.patternMatchAsList(cm.TWO_GA, match_0)
        elif is_one_ga:
            print("ONE_GA")
            ref_list = cm.patternMatchAsList(cm.ONE_GA, match_0)
        pp(ref_list)

        for w_start, w_end, w_match_0, w_match_1 in ref_list:
            print("w_start:", w_start, "w_end:", w_end, "w_match_0:", w_match_0, "w_match_1:", w_match_1)
            if is_doc or is_ref or is_term:
                trans = self.translateDocRef(w_match_1)
            elif is_menu:
                trans = self.translateMenu(w_match_1)
            elif is_kbd:
                trans = self.translateKeyboard(w_match_1)
            elif is_abbrev:
                trans = self.translateAbbrev(w_match_1)
            else:
                trans = self.translateOtherRef(w_match_1)

            result = None
            if trans:
                result = match_0.replace(w_match_1, trans)
                print("RESULT: start, end, match_0, result")
                print(start, end, match_0, result)
                return start, end, match_0, result


        #     if is_doc or is_ref or is_term:
        #         trans = self.translateDocRef(w_match_1)
        #         return w_start, w_end, w_match_1, trans
        #     elif is_menu:
        #         is_ref_embedded = cm.REF_KEYS.search(w_match_1)
        #         if is_ref_embedded:
        #             for em_start, em_end, em_match_0, em_match_1 in cm.patternMatchAsList(cm.TEXT_BETWEEN_REFS, w_match_1):
        #                 print("em_start, em_end, em_match_0, em_match_1")
        #                 print(em_start, em_end, em_match_0, em_match_1)
        #
        #         trans = self.translateMenu(w_match_1)
        #         return w_start, w_end, w_match_1, trans
        #     elif is_kbd:
        #         trans = self.translateKeyboard(w_match_1)
        #         return w_start, w_end, w_match_1, trans
        #     elif is_ref:
        #         trans = self.translateRef(w_match_1)
        #         return w_start, w_end, w_match_1, trans
        #     elif is_abbrev:
        #         trans = self.translateAbbrev(w_match_1)
        #         return w_start, w_end, w_match_1, trans
        #     else:
        #         trans = self.translateOtherRef(w_match_1)
        #         return w_start, w_end, w_match_1, trans

        # for two_start, two_end, two_match_0, two_match_1 in cm.patternMatchAsList(cm.TWO_GA, match_0):
        # for two_start, two_end, two_match_0, two_match_1 in cm.patternMatchAsList(cm.ONE_GA, match_0):

        # for w_start, w_end, w_match_0, w_match_1 in cm.patternMatchAsList(cm.TEXT_BETWEEN_REFS, match_0):
        #     #check to see if the whole sentence can be translated before broke down to words
        #     #must exclude ref links
        #     print("w_start:",w_start, "w_end:", w_end, "w_match_0:", w_match_0, "w_match_1:",w_match_1)
        #     if is_doc or is_ref or is_term:
        #         trans = self.translateDocRef(w_match_1)
        #         return w_start, w_end, w_match_1, trans
        #     elif is_menu:
        #         is_ref_embedded = cm.REF_KEYS.search(w_match_1)
        #         if is_ref_embedded:
        #             for em_start, em_end, em_match_0, em_match_1 in cm.patternMatchAsList(cm.TEXT_BETWEEN_REFS, w_match_1):
        #                 print("em_start, em_end, em_match_0, em_match_1")
        #                 print(em_start, em_end, em_match_0, em_match_1)
        #
        #         trans = self.translateMenu(w_match_1)
        #         return w_start, w_end, w_match_1, trans
        #     elif is_kbd:
        #         trans = self.translateKeyboard(w_match_1)
        #         return w_start, w_end, w_match_1, trans
        #     elif is_ref:
        #         trans = self.translateRef(w_match_1)
        #         return w_start, w_end, w_match_1, trans
        #     elif is_abbrev:
        #         trans = self.translateAbbrev(w_match_1)
        #         return w_start, w_end, w_match_1, trans
        #     else:
        #         trans = self.translateOtherRef(w_match_1)
        #         return w_start, w_end, w_match_1, trans
        #
        #         # print("NONE of the special cases: is_menu/is_doc/is_kbd/is_ref")
        #         # print(w_start, w_end,"w_match_0: ", w_match_0)
        #         # for wo_start, wo_end, wo_match_0, wo_match_1 in cm.patternMatchAsList(cm.WORD_ONLY, w_match_0):
        #         #     print(wo_start, wo_end, "wo_match_0: ", wo_match_0)
        #
        # trans = None
        #
        # # w_start, w_end, w_match_0, w_match_1 = text_between_ref
        # # word_list = cm.patternMatchAsList(cm.WORD_ONLY, w_match_0)
        # # print("word_list: ", word_list)

        return (-1, -1, match_0, trans)


    def removeOriginal(self, msg, trans):
        # print("removeOriginal msg = [{}], trans = [{}]".format(msg, trans))
        orig_index = -1
        # if trans:
        #     orig_index = trans.find(trans, "-- ")
        #     has_orig = (msg in trans) and (orig_index > 0)
        #     is_empty_trans = (orig_index == 0)
        #     if is_empty_trans:
        #         return None
        #
        #     if has_orig:
        #         word_list = trans.split("-- ")
        #         trans = word_list[0]
        #         return trans
        # return None

        msg = re.escape(msg)
        p = r'\b{}\b'.format(msg)
        has_original = (re.search(p, trans, flags=re.I) != None)
        endings=("", "s", "es", "ies", "ed", "ing", "lly",)
        if has_original:
            for end in endings:
                p = r'-- {}{}'.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

            for end in endings:
                p = r'{}{} --'.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

            for end in endings:
                p = r'\\b{}{}\\b'.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)
            trans = trans.strip()
            is_empty = (len(trans) == 0)
            if is_empty:
                trans = None

            # if trans:
            #     print("removeOriginal msg: [{}] => trans: [{}]".format(msg, trans))
            # else:
            #     print("removeOriginal REMOVED AND EMPTY")
        # else:
        #     print("removeOriginal DO NOT HAVE ORIGINAL in translation")

        return trans

    def isInList(self, msg, find_list, is_lower=False):
        orig_msg = str(msg)
        trans = None
        if is_lower:
            msg = msg.lower()
        if msg in find_list:
            trans = find_list[msg]
        else:
            trams = None

        if isinstance(trans, Message):
            trans = trans.string
        else:
            trans = trans

        # is_debug = ("POV" in msg)
        # if is_debug:
        #     print("DEBUG: msg [{}] => [{}]".format(msg, trans))

        has_translation = trans and (len(trans) > 0) and (trans != 'None')
        if has_translation:
            trans = trans.strip()
            trans = self.removeOriginal(msg, trans)
            trans = cm.matchCase(orig_msg, trans)
        else:
            trans = None
        return  trans

    def findTranslationByFragment(self, msg):
        print("findTranslationByFragment:[{}]".format(msg))
        msg = unescape(msg)

        trans_list = []
        trans = str(msg)
        for w_start, w_end, w_match_0, w_match_1 in cm.patternMatchAsList(cm.WORD_ONLY_FIND, msg):
            trans_word = trans_finder.findTranslation(w_match_0)
            trans_word_entry = (w_start, w_end, w_match_0, trans_word)

            print("FIND TRANS: w_start, w_end, w_match_0, w_match_1, trans_word")
            print(w_start, w_end, w_match_0, w_match_1, trans_word)

            trans_list.append(trans_word_entry)

        print("findTranslationByFragment trans_list")
        pp(trans_list)

        for w_start, w_end, w_match_0, trans_word in reversed(trans_list):
            print("REPLACING: w_start, w_end, w_match_0, trans_word")
            print(w_start, w_end, w_match_0, trans_word)
            if trans_word:
                w_end = w_start + len(w_match_0)
                st = trans[:w_start]
                se = trans[w_end:]
                trans = st + trans_word + se
                print("findTranslationByFragment st:[{}], se:[{}], trans:[{}]".format(st, se, trans))
                #trans = trans.strip()
            print("findTranslationByFragment trans:[{}]".format(trans))

        is_changed = (trans != msg)
        if not is_changed:
            trans = None

        if trans:
            print("RESULT findTranslationByFragment: [{}] => [{}]".format(msg, trans))

        return trans

    def findTranslation(self, msg):
        list_name = "self.dic_cat"
        trans = self.isInList(msg, self.dic_cat)
        if not trans:
            list_name = "self.dic_cat_lower"
            trans = self.isInList(msg, self.dic_cat_lower, is_lower=True)
            if not trans:
                list_name = "self.translated_po_dic"
                trans = self.isInList(msg, self.translated_po_dic)
                if not trans:
                    list_name = "self.translated_po_dic_lower"
                    trans = self.isInList(msg, self.translated_po_dic_lower, is_lower=True)
                    if not trans:
                        list_name = "self.json_dic_list"
                        trans = self.isInList(msg, self.json_dic_list)
                        if not trans:
                            list_name = "self.json_dic_list_lower"
                            trans = self.isInList(msg, self.json_dic_list_lower, is_lower=True)
                            if not trans:
                                list_name = ""
                                return None

        has_translation = trans and (len(trans) > 0) and (trans != 'None')
        if has_translation:
            trans = trans.strip()
            trans = self.removeOriginal(msg, trans)
            print("findTranslation in {} [{}] => [{}]".format(list_name, msg, trans))
        else:
            trans = None
        return trans


trans_finder = TranslationFinder()

MNU_SEL = 'menuselection'
MNU_SEP = '-->'
CLASS = 'classes'
RAWTXT = 'rawtext'
DOC = 'doc' #:doc:`keyframe
STD_REF="std std-ref" #:ref:`easings
X_REF="xref std std-term" #:term:`walk cycle
BACKQUOTE="`"
TR_ED='translated'
def print_separator(output_path):
    print("docname:", output_path)
    print("-" * 30)

def print_result_list(result):
    PP(result)

class NoTranslationNodeVisitor(nodes.GenericNodeVisitor):

    def emptyNode(self):
        return nodes.Text('')

    def default_visit(self, node):
        # type: (nodes.Node) -> None
        raise nodes.NodeFound
        # this is where no visit has been implemented????
        #pass

    def visit_emphasis(self, node):
        n_node = self.emptyNode()
        node.replace_self(n_node)
        raise nodes.SkipNode

    def visit_inline(self, node):
        n_node = self.emptyNode()
        node.replace_self(n_node)
        raise nodes.SkipNode

    def visit_literal(self, node):
        n_node = self.emptyNode()
        node.replace_self(n_node)
        raise nodes.SkipNode

    def visit_reference(self, node):
        n_node = self.emptyNode()
        node.replace_self(n_node)
        raise nodes.SkipNode


class TranslationNodeVisitor(nodes.TreeCopyVisitor):
    """Raise `nodes.NodeFound` if non-simple list item is encountered.

    Here 'simple' means a list item containing only a paragraph with a
    single reference in it.
    """
    def setVars(self, node, msg, trans, is_title_node=False):
        self.current_node = node
        self.current_msg = msg
        if trans:
            self.current_trans = trans
        else:
            self.current_trans = msg
        self.fuzzy_list = []
        self.is_fuzzy = False
        self.is_title_node = False
        self.tr = None
        self.ref_trans=[]

    def setBlanking(self, value):
        self.is_blanking_out = value

    def default_visit(self, node):
        print("default_visit")
        msg = node.astext()
        print("rawsource", node.rawsource)
        print("msg: [{}]".format(msg))

        # print("type:", type(node))
        # print("dir:", dir(node))
        # print("len:", len(node))

        for index, n in enumerate(node):
            print("type:", type(n))
            print("index", index, "n", n)

            if isinstance(n, docutils.nodes.reference):
                self.visit_reference(n)
            elif isinstance(n, docutils.nodes.literal):
                self.visit_literal(n)
            elif isinstance(n, docutils.nodes.inline):
                self.visit_inline(n)
            elif isinstance(n, docutils.nodes.emphasis):
                self.visit_emphasis(n)
            elif isinstance(n, docutils.nodes.strong):
                self.visit_strong(n)

            # class 'docutils.nodes.emphasis' ##>
            # class 'docutils.nodes.image'>
            # class 'docutils.nodes.inline' ##>
            # class 'docutils.nodes.literal' ##>
            # class 'docutils.nodes.math'>
            # class 'docutils.nodes.reference' ##>
            # class 'docutils.nodes.strong' ##>
            # class 'docutils.nodes.Text'>

            #elif isinstance(nodes.)
        # type: (nodes.Node) -> None
        raise nodes.SkipNode
        # this is where no visit has been implemented????
        #pass

    def visit_emphasis(self, node):
        print("visit_emphasis")
        msg = node.astext()
        print("rawsource", node.rawsource)
        print(msg)
        print("")
        #raise nodes.SkipNode

    def visit_strong(self, node):
        print("visit_strong")
        msg = node.astext()
        print("rawsource", node.rawsource)
        print(msg)
        print("")
        #raise nodes.SkipNode

    # def trans_doc(self, node):
    # def trans_std_ref(self, node):
    # def trans_xref(self, node):
    # classes="xref py py-class"

    def trans_keyboard(self, node):
        # obj.hasattr('classes')
        trans = None
        KEY='kbd'
        classes = node.get('classes')
        if classes in [[KEY]]:
            #print("IS KEYBOARD")
            msg = node.astext()
            trans = cm.translateKeyboardDef(msg)
        return trans

    def setNodeTranslated(self, node):
        node[TR_ED] = True
        print("NODE TRANSLATED!!!")

    def getNodeTranslated(self, node):
        try:
            transed = node[TR_ED]
            print("NODE TRANSLATION:{}".format(transed))
            return transed
        except Exception as e:
            return False

    def connectMenuItems(self, list_of_menu_items):
        trans_list = []
        for item in list_of_menu_items:
            item = item.strip()
            print("item:", item)
            trans = trans_finder.findTranslation(item, remove_original=True)
            if (trans):
                trans = "{} ({})".format(trans, item)
            else:
                trans = "({})".format(item)
            print("trans:", trans)
            trans_list.append(trans)
        return trans_list

    # /home/htran/blender_documentations/blender_docs/build/rstdoc/addons/3d_view/3d_navigation.html
    def trans_menuselection(self, node):

        mnu = self.getMenuText(node)
        if mnu:
            msg = mnu
            list_of_menu_items = msg.split(MNU_SEP)
            PP(msg)
            PP(list_of_menu_items)
            trans_list = self.connectMenuItems(list_of_menu_items)
            if (len(trans_list) > 0):
                trans = " {} ".format(MNU_SEP).join(trans_list)
            else:
                trans = None
            print("FINAL {}".format(trans))
        else:
            msg = node.astext()
            msg = unescape(msg)
            is_menu = (MNU_SEP in msg)
            if not is_menu:
                return None
            list_of_menu_items = msg.split(MNU_SEP)
            if (len(trans_list) > 0):
                trans = " {} ".format(MNU_SEP).join(trans_list)
            else:
                trans = None
        return trans

    #
    def my_replace(self, from_s, to_s, in_s):
        new_s = in_s
        from_s_index = in_s.find(from_s)
        print("from_s_index of {} in {} is {}".format(from_s, in_s, from_s_index))
        return new_s

    def setMergeTransToCurrent(self, msg, trans):

        if not trans:
            return

        print("msg: [{}]; current trans: [{}]; new trans: [{}]".format(msg, self.current_trans, trans))

        old_trans = self.current_trans
        new_trans = self.current_trans.replace(msg, trans)

        is_replaced = (old_trans != new_trans)
        if not is_replaced:
            return

        print("REPLACED old: {}, new: {}".format(old_trans, new_trans))
        self.fuzzy_list.append(trans)
        self.fuzzy_list.append(self.current_trans)
        print("Set in self.fuzzy_list: [{}]".format(trans))
        print("")



    # def visit_bullet_list(self, node):
    #     # type: (nodes.Node) -> None
    #     pass
    def visit_emphasis(self, node):
        print("visit_emphasis")
        msg = node.astext()
        print("rawsource", node.rawsource)
        print(msg)
        print("")
        raise nodes.SkipNode


        msg = node.astext()
        msg = unescape(msg)
        is_ignore = cm.isIgnoredWord(msg) or cm.isDosCommand(msg)
        if is_ignore:
            return

        mnu = self.getMenuText(node)
        if mnu:
            msg = mnu

        print("type:{}".format(type(node)))
        print("emphasis text:", msg)
        print("parent text:", node.parent)

        trans = trans_finder.findTranslation(msg)
        is_repeat = (trans == msg)
        valid_trans = (trans and not is_repeat)
        if valid_trans:
            #print("has trans for emphasis:")
            has_original = (re.search(msg, trans, flags=re.I) != None)
            if has_original:
                trans = re.sub(msg, "", trans, flags=re.I).strip()
            trans = "{} ({})".format(trans, msg)
        else:
            #emphasis text: Add New Ivy
            #print("emphasis using original:")
            trans = trans_finder.findTranslationByFragment(msg)

            is_repeat = (trans == msg)
            valid_trans = (trans and not is_repeat)
            if valid_trans:
                trans = "{} ({})".format(trans, msg)
            else:
                trans = "-- {}".format(msg)
        self.setMergeTransToCurrent(msg, trans)
        self.setNodeTranslated(node)
        self.ref_trans
        #raise nodes.SkipNode

    def getMenuText(self, node):
        try:
            is_menu = (MNU_SEL in node[CLASS])
            if is_menu:
                orig_text = node[RAWTXT]
                rep_txt = ":{}:".format(MNU_SEL)
                menu_text = re.sub(rep_txt, "", orig_text)
                menu_text = menu_text.strip("`")
                msg = menu_text
                return msg
        except Exception as e:
            pass
        return None

    def getRefText(self, node):
        try:
            is_std_ref = (STD_REF in node[CLASS])
            is_xref = (X_REF in node[CLASS])
            is_doc = (DOC in node[CLASS])
            is_ref = (is_std_ref or is_xref or is_doc)
            if is_ref:
                orig_text = node.astext()
                key_word = ('ref' if is_std_ref else 'term' if is_xref else 'doc' if is_doc else None)
                msg = ":{}:`".format(key_word)
                return msg
        except Exception as e:
            pass
        return None

    def visit_reference(self, node):
        print("visit_reference")
        print("rawsource", node.rawsource)
        for index, n in enumerate(node):
            print("type:", type(n))
            print("index:", index, "n=", n)
            msg = n.astext()
            print(msg)
        print("")
        raise nodes.SkipNode

    def visit_inline(self, node):
        print("visit_inline")
        print("rawsource", node.rawsource)
        for index, n in enumerate(node):
            print("type:", type(n))
            print("index:", index, "n=", n)
            msg = n.astext()
            print(msg)
        print("")
        raise nodes.SkipNode

        msg = node.astext()
        msg = unescape(msg)
        is_ignore = cm.isIgnoredWord(msg) or cm.isDosCommand(msg)
        if is_ignore:
            return

        print("visit_inline:[{}]".format(msg))
        mnu = self.getMenuText(node)
        if mnu:
            msg = mnu
            print("mnu: [{}]".format(mnu))


        print("type:{}".format(type(node)))
        print("inline text:", msg)
        print("parent text:", node.parent)

        print("node['classes']:", node['classes'])
        #print("node['rawtext']", node['rawtext'])

        # Getting Started
        # /home/htran/blender_documentations/blender_docs/build/rstdoc/about/contribute/translations/add_language.html
        trans = trans_finder.findTranslation(msg)
        is_repeat = (trans == msg)
        valid_trans = (trans and not is_repeat)
        if valid_trans:
            print('has translation:', trans)
        else:
            trans = self.trans_keyboard(node)
            if not trans:
                trans = self.trans_menuselection(node)
                if not trans:
                    trans = trans_finder.findTranslationByFragment(msg)
                    if not trans:
                        trans = None

        if trans:
            print("trans: [{}]".format(trans))
        # tail = " -- {}".format(msg)
        # is_repeated = (tail in trans)
        # if is_repeated:
        #     tran = re.sub(tail, "", trans)
        # trans = "{} -- {}".format(trans, msg)

        doc_xref_ref = self.getRefText(node)
        if doc_xref_ref:
            msg = "{}{}".format(doc_xref_ref, msg)
            trans= "{}{}".format(doc_xref_ref, trans)
        self.setMergeTransToCurrent(msg, trans)
        self.setNodeTranslated(node)
        self.ref_trans.append((msg, trans))
        raise nodes.SkipNode

    def visit_literal(self, node):
        print("visit_literal")
        msg = node.astext()
        msg = unescape(msg)
        print("type:", type(node))
        print(msg)
        for index, n in enumerate(node):
            print("type:", type(n))
            print("index:", index, "n=", n)
            msg = n.astext()
            print(msg)
        print("")

        raise nodes.SkipNode

        is_ignore = cm.isIgnored(msg) or cm.isDosCommand(msg)
        if is_ignore:
            return

        print("visit_literal:[{}]".format(msg))
        mnu = self.getMenuText(node)
        if mnu:
            msg = mnu
            print("mnu: [{}]".format(mnu))


        print("type:{}".format(type(node)))
        print("literal text:", node.astext())
        print("parent text:", node.parent)
        print("node['classes']:", node['classes'])


        trans = trans_finder.findTranslation(msg)
        if not trans:
            trans = self.trans_keyboard(node)
            if not trans:
                trans = self.trans_menuselection(node)
                if not trans:
                    trans = trans_finder.findTranslationByFragment(msg)
                    if not trans:
                        trans = None

        if trans:
            print("trans: [{}]".format(trans))

        tail = " -- {}".format(msg)
        is_repeated = (tail in trans)
        if is_repeated:
            tran = re.sub(tail, "", trans)
        trans = "{} -- {}".format(trans, msg)
        self.setMergeTransToCurrent(msg, trans)
        self.setNodeTranslated(node)
        self.ref_trans.append((msg, trans))
        raise nodes.SkipNode
        # type: (nodes.Node) -> None
        # children = []  # type: List[nodes.Node]
        # isinstance(child, nodes.Invisible):
        # for child in node.children:
        #     if not isinstance(child, nodes.Invisible):
        #         children.append(child)
        # if len(children) != 1:
        #     raise nodes.NodeFound
        # if not isinstance(children[0], nodes.paragraph):
        #     raise nodes.NodeFound
        # para = children[0]
        # if len(para) != 1:
        #     raise nodes.NodeFound
        # if not isinstance(para[0], addnodes.pending_xref):
        #     raise nodes.NodeFound
        # raise nodes.SkipChildren

    def invisible_visit(self, node):
        # type: (nodes.Node) -> None
        """Invisible nodes should be ignored."""
        pass
# --------------------------------------------------------------

gtr = GTR() #Google translator

def dump_po(filename, catalog):
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    # Because babel automatically encode strings, file should be open as binary mode.
    with io.open(filename, 'wb') as f:
        pofile.write_po(f, catalog, width=4096)

def isInRefList(reflist, entry):
    is_empty_list = (not reflist or len(reflist) == 0)
    if is_empty_list:
        return False

    is_empty_entry = (not entry or len(entry) == 0)
    if is_empty_entry:
        return False

    start_post_list = []
    end_post_list = []
    extract_list = []

    es, ee, eorig, eextract = entry
    for s, e, orig, extract in reflist:
        is_entry = (s == es) and (e == ee) and (orig == eorig) and (eextract == extract)
        if is_entry:
            continue

        start_post_list.append(s)
        end_post_list.append(e)
        extract_list.append(extract)

    # print("es, ee, eorig, eextract")
    # print(es, ee, eorig, eextract)
    #
    # pp(start_post_list)
    # pp(end_post_list)
    # pp(orig_list)

    is_in = (es in start_post_list) and (ee in end_post_list) and (eextract in extract_list)
    # print("is_in", is_in)

    return is_in


def doctree_resolved(app, doctree, docname):

    def replaceRefTrans(msg, ref_trans_list):
        print("replaceRefTrans:")
        print("msg:[{}]".format(msg))
        print("ref_trans_list:")
        pp(ref_trans_list)

        orig_msg = str(msg)
        for w_start, w_end, ref, orig, trans in reversed(ref_trans_list):
            msg = msg.replace(orig, trans)
            print("trans_text:[{}]".format(trans))
            print("new_msg:[{}]".format(msg))

        print(orig_msg, " |==>| ", msg)
        return msg

    build_dir = "build/rstdoc"
    po_vi_dir = "locale/vi/LC_MESSAGES"

    po_file_path="{}.po".format(docname)
    local_path = os.path.dirname(os.path.abspath( __file__ ))
    blender_docs_path = os.path.dirname(local_path)

    rst_output_location = os.path.join(blender_docs_path, build_dir)
    output_path = os.path.join(rst_output_location, po_file_path)

    print_separator(output_path)

    # is_debug = "/about/contribute/guides/markup_guide" in output_path
    # if not is_debug:
    #     return


    # for node in doctree.traverse():
    #     is_literal = (isinstance(node, nodes.literal))
    #     if (is_literal):
    #         print("is_literal, type:", type(node))
    #         print("is_literal, text:", node.astext())

    trans_doctree = doctree.deepcopy()

    cat = Catalog()
    visitor_inited = False
    empty_node_visitor = None

    visitor_inited = False
    visitor = None

    for node, msg in extract_messages(doctree):
        msg = unescape(msg).strip()

        if (not visitor_inited):
            visitor = TranslationNodeVisitor(node.document)
            visitor_inited = True

        try:
            node.walk(visitor)
        except Exception as e:
            print(e)

        # chosen_ref_list = []
        # print("msg: [{}]".format(msg))
        # ref_list_1 = cm.patternMatchAsList(cm.DOUBLE_GRAVE_ACCENT_SURROUND, msg)
        # ref_list_2 = cm.patternMatchAsList(cm.REFS, msg)
        # len_1 = len(ref_list_1)
        # len_2 = len(ref_list_2)
        #
        # print("ref_list_1 count:", len(ref_list_1))
        # pp(ref_list_1)
        # print("-"*10)
        # print("ref_list_2", len(ref_list_2))
        # pp(ref_list_2)
        # print("-"*10)
        #
        # join_ref = ref_list_1 + ref_list_2
        # print("join_ref")
        # pp(join_ref)
        #
        # for ref in join_ref:
        #     start, end, orig, extract = ref
        #     is_ref = (cm.SINGLE_REF.search(orig) != None) and (not isInRefList(join_ref, ref))
        #     if is_ref:
        #         chosen_ref_list.append(ref)
        #     else:
        #         print("Entry is considered NOT A SINGLE REF")
        #         pp(ref)


        # is_one = (len_1 == 1) and (len_1 == len_2)
        # is_diff = (len_1 != len_2)
        # if is_one:
            #take one where extract_msg_1 and extract_msg_2 is not None

        # has_ref = (len(ref_list_1) > 0) and (len(ref_list_2) > 0)
        #
        # if has_ref:
        #     start, end, orig_1, extract_msg_1 = ref_list_1[0]
        #     start, end, orig_2, extract_msg_2 = ref_list_2[0]
        #     chosen_ref_list = (ref_list_1 if extract_msg_1 else ref_list_2)
        # else:
        #     chosen_ref_list = None

        # elif is_diff:
        #     #take one with more entries
        #     chosen_ref_list = (ref_list_1 if (len_1 > len_2) else ref_list_2)
        # else:
        #     #print("NO REF: [{}]".format(msg))
        #     chosen_ref_list = None

        # has_ref = (len(chosen_ref_list) > 0)
        # if has_ref:
        #     print("chosen_ref_list")
        #     pp(chosen_ref_list)
        #     print("-" * 10)
        #
        #     ref_trans_list = []
        #     for ref in chosen_ref_list:
        #         print("ref:", ref)
        #         w_start, w_end, orig, trans = trans_finder.translateReferences(ref)
        #         if trans:
        #             r_start, r_end, m_0, m_1 = ref
        #             ref_tran_entry = (w_start, w_end, ref, orig, trans)
        #             ref_trans_list.append(ref_tran_entry)
        #
        #     has_entries = len(ref_trans_list) > 0
        #
        #     if has_entries:
        #         print("ref_trans_list:")
        #         pp(ref_trans_list)
        #         msg = replaceRefTrans(msg, ref_trans_list)
        #         print("")

        # is_empty = ref_list and ((len(ref_list) == 0) or (len(ref_list[0]) == 0))
        # if not is_empty:
        #     print("ref_list:")
        #     pp(ref_list)
        #     print("")
        #
        #     ref_trans_list = []
        #     for ref in ref_list:
        #         print("ref:", ref)
        #         w_start, w_end, orig, trans = trans_finder.translateReferences(ref)
        #         if trans:
        #             r_start, r_end, m_0, m_1 = ref
        #             ref_tran_entry = (w_start, w_end, ref, orig, trans)
        #             ref_trans_list.append(ref_tran_entry)
        #     has_entries = len(ref_trans_list) > 0
        #     if has_entries:
        #         print("ref_trans_list:")
        #         pp(ref_trans_list)
        #         msg = replaceRefTrans(msg, ref_trans_list)
        # print("")

    print_separator(output_path)
    # cat_is_not_empty = (len(cat) > 0)
    # if cat_is_not_empty:
    #     dump_po(output_path, cat)

# def doctree_resolved(app, doctree, docname):
#     build_dir = "build/rstdoc"
#     po_vi_dir = "locale/vi/LC_MESSAGES"
#
#     po_file_path="{}.po".format(docname)
#     local_path = os.path.dirname(os.path.abspath( __file__ ))
#     blender_docs_path = os.path.dirname(local_path)
#
#     rst_output_location = os.path.join(blender_docs_path, build_dir)
#     output_path = os.path.join(rst_output_location, po_file_path)
#
#     result={}
#
#     # for node in doctree.traverse():
#     #     is_literal = (isinstance(node, nodes.literal))
#     #     if (is_literal):
#     #         print("is_literal, type:", type(node))
#     #         print("is_literal, text:", node.astext())
#
#     trans_doctree = doctree.deepcopy()
#
#     cat = Catalog()
#     visitor_inited = False
#     empty_node_visitor = None
#     for node, msg in extract_messages(doctree):
#         msg = unescape(msg).strip()
#
#         if (not visitor_inited):
#             visitor = TranslationNodeVisitor(node.document)
#             empty_node_visitor = NoTranslationNodeVisitor(node.document)
#
#
#         # n, clone_node_msg = extractMessage(clone_node)
#         # print("clone_node_msg:{}".format(clone_node_msg))
#
#         is_title = (isinstance(node, nodes.title))
#         is_term = (isinstance(node, nodes.term))
#         is_rubric = (isinstance(node, nodes.rubric))
#         is_field_name = (isinstance(node, nodes.field_name))
#         is_paragraph = (isinstance(node, nodes.paragraph))
#
#         is_repeat = (is_title or is_term or is_rubric or is_field_name)
#
#         trans = trans_finder.findTranslation(msg)
#
#         # is_debug = ("POV" in msg)
#         # if is_debug:
#         #     print("{} => {}".format(msg, trans))
#         #     exit(0)
#
#         has_translation = trans and (len(trans) > 0) and (trans != 'None')
#         if has_translation:
#             trans = trans.strip()
#
#         translation = None
#         is_repeatable = (has_translation and is_repeat)
#         is_repeated_without_trans = (not has_translation) and is_repeat
#         is_non_repeated = (has_translation and not is_repeat)
#
#         is_duplicated = has_translation and (trans == msg)
#
#         if is_duplicated:
#             print("REPEATED:")
#             translation = trans
#         elif is_repeatable:
#             has_original = (msg in trans)
#             if has_original:
#                 translation = trans
#             else:
#                 translation = "{} -- {}".format(trans, msg)
#         elif is_repeated_without_trans:
#             translation = trans_finder.findTranslationByFragment(msg)
#             has_translation = trans and (len(trans) > 0) and (trans != 'None')
#             if has_translation:
#                 translation = "{} -- {}".format(trans, msg)
#             else:
#                 translation = "-- {}".format(msg)
#         elif is_non_repeated:
#             translation = trans
#
#         visitor.setVars(node, msg, translation, is_title_node=(is_duplicated or not is_paragraph) )
#         try:
#             node.walk(visitor)
#         except Exception as e:
#             print(e)
#
#         # if not translation:
#         #     translation = trans_finder.findTranslationByFragment(msg)
#
#         # if is_debug:
#         #     print("msg : ", msg)
#         #     print("trans : ", translation)
#         #     #exit(0)
#
#         print("visitor.ref_trans:")
#         pp(visitor.ref_trans)
#
#         if not has_translation:
#             if use_google_translate:
#                 trans = gtr.translate(msg, dest='vi')
#                 translation = trans.text
#                 print("GTR: [{}] -> [{}]".format(trans.origin, trans.text))
#             else:
#
#                 print("NO TRANSLATION visitor.ref_trans:")
#                 pp(visitor.ref_trans)
#
#                 print("SEPARATE reflist and text for:", msg)
#                 ref_list = cm.getRefsAsList(msg)
#                 text_only = cm.getTextOnly(msg)
#                 print("REFLIST:")
#                 pp(ref_list)
#                 print("text_only:[{}]".format(text_only))
#
#                 translation = trans_finder.findTranslationByFragment(text_only)
#
#                 if translation and is_repeat:
#                     translation = "{} -- {}".format(translation, msg)
#                 elif not translation and is_repeat:
#                     translation = "-- {}".format(msg)
#                 elif not translation:
#                     translation = ""
#         cat.add(msg, string=translation, user_comments=visitor.fuzzy_list)
#
#         print("msgid \"{}\"".format(msg))
#         print("msgstr \"{}\"".format(translation))
#
#         fuz = visitor.fuzzy_list
#         curtran = visitor.current_trans
#
#         has_fuz = fuz and (len(fuz) > 0)
#         has_curtran = curtran and (len(curtran) > 0)
#         if has_fuz:
#             print("visitor.fuzzy_list: {}".format(fuz))
#         if has_curtran:
#             print("visitor.current_trans: {}".format(curtran))
#         print("")
#
#             #node.clear()
#             #txt = node.astext()
#             #print("Removed children:{}".format(txt))
#             # print("Node type:{}".format(type(node)))
#             # print("dir(node):{}".format(dir(node)))
#             #print("children:{}".format(node.children))
#             #pp(node_list)
#             #exit(0)
#         # else:
#         #     try:
#         #         node.walk(empty_node_visitor)
#         #     except Exception as e:
#         #         print(e)
#         #
#         #     msg = node.astext()
#         #     translation = trans_finder.findTranslationByFragment(msg)
#         #     if translation:
#         #         cat.add(msg, string=translation)
#         #     else:
#         #         translation = ""
#         #     print("After empty_node_visitor: [{}] => [{}]".format(msg, translation))
#
#     print_separator(output_path)
#     # cat_is_not_empty = (len(cat) > 0)
#     # if cat_is_not_empty:
#     #     dump_po(output_path, cat)

# def source_read(app, docname, source):
#     #load corresponding po file from locale/vi/LC_MESSAGE
#     #references are placed in app
#     #print("source_read docname:", docname)
#     regis = app.registry
#     print("regis:", regis.get_transforms())
#
#
# def builder_inited(app):
#     app.registry.add_transform(LocalVar)
#     print("builder_inited")
#
#     #read vipo translated file
#     #form normal sorted list
#     #form lower case sorted list
#     #pass


def setup(app):
    # app.connect('builder-inited', builder_inited)
    # app.connect('source-read', source_read)
    app.connect('doctree-resolved', doctree_resolved)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

