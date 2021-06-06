#!/usr/bin/env python3
#cython: language_level=3
import re
import os
import json
from collections import OrderedDict, defaultdict

import datetime
import math
from collections import deque
from difflib import SequenceMatcher as SM
from pprint import pprint as PP
# import html
import subprocess as sub

from translation_finder import TranslationFinder
from ignore import Ignore as IG
from fuzzywuzzy import fuzz

from sphinx_intl import catalog as c
from pytz import timezone
from common import Common as cm, dd, pp
from matcher import MatcherRecord
from definition import Definitions as df, RefType, TranslationState
from reflist import RefList
import inspect as INP
import copy as CP
import cProfile


def readJSON(file_path):
    with open(file_path) as in_file:
        dic = json.load(in_file, object_pairs_hook=OrderedDict)
    return dic

def writeJSON(file_path, data):
    with open(file_path, 'w+', newline='\n', encoding='utf8') as out_file:
        json.dump(data, out_file, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ': '))

class test(object):

    def resort_dictionary(self):
        home_dir = os.environ['BLENDER_GITHUB']
        from_file = os.path.join(home_dir, 'ref_dict_0006_0003.json')
        to_file = os.path.join(home_dir, 'ref_dict_0006_0002.json')

        to_dic = readJSON(from_file)

        sorting = sorted(list(to_dic.items()), key=lambda x: x[0].lower())
        new_dic = OrderedDict(sorting)

        for t_k, t_v in to_dic.items():
            entry = {t_k: t_v}
            new_dic.update(entry)

        sorting = sorted(list(new_dic.items()), key=lambda x: x[0].lower())
        new_dic = OrderedDict(sorting)

        writeJSON(to_file, new_dic)


    def test_translate_0001(self, text_list=None):
        from paragraph_cy import Paragraph as PR
        from sentence import StructRecogniser as SR

        if not text_list:
            t_list = [
                # "like a theater stage",
                # "like an armature or shape key",
                # "like an empty instancing a collection containing instances of some other collections",
                # "like bleed for baking",
                # "like cameras, lights, etc.",
                # "like circles, squares, and so on",
                # "like e.g. a cube with all its six faces",
                # "like e.g. from a shading node",
                # "like e.g. the :doc:`\"copy\" ones </animation/constraints/transform/copy_location>`",
                # "like e.g. the main blend-file *Open* one",
                # "like images, textures, materials, lights and world shaders",
                # "like in the real world due to friction between the colliding surfaces",
                # "like invisible meta objects",
                # "like mesh, curve, camera...",
                # "like object modifiers do",
                # "like opening or saving a blend-file",
                # "like parenting the hand to the head",
                # "like seen in the sphere above",
                # "like simulating a human ear lit from behind",
                # "like textures and symmetry",
                # "like the *X-Axis Mirror* editing tool",
                # "like the :doc:`\"limit\" ones </animation/constraints/transform/limit_location>`",
                # "like the Arc tool",
                # "like the color of the coordinate axes in the 3D Viewport",
                # "like the copy/paste buttons, and snapping type",
                # "like the ones present in normal screws that you can buy in hardware stores",
                # "like the ones used for wood; as shown in the example at the beginning of this page",
                # "like the result of fluid simulations",
                # "like the single property :ref:`driver variables <drivers-variables>`",
                # "like the yellow/green/purple colors of animated/driven ones",
                # "like three minutes for a mesh with 4,000 points",
                # "like thumbnails",
                # "like trees, humans, etc.",
                # "like with some modes of the :ref:`Displace modifier <bpy.types.DisplaceModifier>`",
                # "limbs",
                # "limbs, spines, tails, fingers, faces...",
                # "lime green",
                # "limitation of FFmpeg",
                # "linked and instantiated",
                # "linking",
                # "list of GCN generations",
                # "list of Nvidia graphics cards",
                # "listed below",
                # "listed from top to bottom",
                # "listed with corresponding operator functions",
                # "lists",
                # "literally",
                # "little jiggle",
                # "loaded in the preferences",
                # "local target's axes",
                # "local, system and user paths",
                # "locale/fr",
                # "located in the Properties, *Modifiers* tab",
                # "location 0, 0, 0",
                # "location and rotation in the virtual space",
                # "location, rotation and scale",
                # "location, rotation or scale along/around one of its axes",
                # "location, rotation, scale",
                # "location, scale or rotation",
                # "location[0]",
                # "locks pie menu",
                # "loolarge",
                # "lower is faster",
                # "lower right corner",
                # "lowers the simulation stability a little so use only when necessary",
            ]
        else:
            t_list = text_list

        tf = TranslationFinder()
        for t in t_list:
            pr = PR(t, translation_engine=tf)
            # pr.translateAsIs()
            pr.translateSplitUp()
            # output = pr.getTranslation()
            output = pr.getTextAndTranslation()
            df.LOG(output)

    # def grepPOTFindPath(self, txt):
    #     ref_dict_list, obs = cm.getRefDictList(txt)
    #     for entry in ref_dict_list:
    #         df.LOG(entry)
    #     return ref_dict_list

    def run(self):
        import cProfile
        # self.test_sorted_list()
        # self.test_forward_slashes()
        # self.test_find_invert()
        # self.test_re()
        # self.test_parsing_link()
        # self.test_ref_link()
        # self.test_remove_blank()
        # self.test_ref_link()
        # self.test_bracket()
        # self.test_abbr()
        # self.test_globals()
        # self.matchingVIPOChangesToDict()
        # self.vipotoJSON()
        # self.test_0074()
        # self.test_0073()
        # self.plistToText()
        # self.test_binary_search()
        # self.sorting_temp_05()
        self.resort_dictionary()
        # self.test_translate_json_file()
        # cProfile.run(self.test_translate_0001())
        self.test_translate_0001()
        # t_list = self.grepPOT(re.compile(r'[^\w\s\-\_\;]+(\w)[\w\s\-\_\.\,\;]+(\w)[^\w\s\-\_\.\,\;]+'))
        # self.test_translate_0001(text_list=t_list)
        # mnu_p = re.compile(r':menuselection:[`]([^`]+)[`]')
        # sep_pat = re.compile(r'\s?(-->)\s?')
        # self.grepPOT(mnu_p, is_sub_group=True, separator=sep_pat, is_translate=True)
        # p = re.compile(r'(?!(\w[\.\,]\w))(\w[^\.\,]+\S)[\.\,](\s|$)')
        # p = re.compile(r'\w+\s\w+\s(chance)\s\w+\s\w+')
        # word = r'(\w+\s)?'
        # l_txt = r'(modifier)'
        # p_txt = r'%s%s%s%s%s' % (word, word, word, word, l_txt)
        # p = re.compile(p_txt)
        # self.grepPOTFindPath(t)
        # self.grepPOT(None, using_function=self.grepPOTFindPath)
        # self.grepPOT(df.GA_REF, is_sub_group=True)
        # simple_bracket = re.compile(r'\s?\([^\(\)]+\)\s?')
        # self.grepPOT(simple_bracket, is_sub_group=False)
        # self.grepPOT(df.FUNCTION, is_sub_group=False)
        # self.grepPOT('have more', is_considering_side_words=True)
        # self.cleanWorkingTextFile()
        # self.translatePO()
        # self.test_0063()
        # print(self.recur(4))
        # self.parseSVG()
        # self.translate_po_file()
        # self.test_pattern_0001()
        # self.test_insert_abbr()
        # self.test_capt_0001()
        # self.test_refs_0001()
        # self.test_0064()
        # self.test_0066()
        # self.test_0067()
        # self.test_0068()
        # self.test_0069()
        # self.test_0070()
        # self.test_0072()
        # self.test_0071()
        # self.cleanDictionary()
        # self.diffPOTFile()
        # self.test_loc_remain()
        # self.mergeVIPOFiles()


# # trans_finder = TranslationFinder()
# def tranRef(msg, is_keep_original):
#     ref_list = RefList(msg=msg, keep_orig=is_keep_original, tf=trans_finder)
#     ref_list.parseMessage()
#     ref_list.translateRefList()
#     tran = ref_list.getTranslation()
#     trans_finder.addDictEntry((msg, tran))
#     print("Got translation from REF_LIST")
#     return tran

x = test()
# cProfile.run('x.run()', 'test_profile.dat')
#
# import pstats
# from pstats import SortKey
#
# with open('output_time.txt', 'w') as f:
#     p = pstats.Stats('test_profile.dat', stream=f)
#     p.sort_stats('time').print_stats()
#
# with open('output_calls.txt', 'w') as f:
#     p = pstats.Stats('test_profile.dat', stream=f)
#     p.sort_stats('calls').print_stats()

x.run()


