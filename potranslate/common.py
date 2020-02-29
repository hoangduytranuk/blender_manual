import html #for escaping html
import sys
import os
import re
import inspect
import copy as cp
from collections import OrderedDict, defaultdict
from pprint import pprint, pformat
#import logging

DEBUG=True
DIC_INCLUDE_LOWER_CASE_SET=False

#logging.basicConfig(filename='/home/htran/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def pp(object, stream=None, indent=1, width=80, depth=None, *args, compact=False):
    if DEBUG:
        pprint(object, stream=stream, indent=indent, width=width, depth=depth, *args, compact=compact)
        print('-' * 30)

def _(*args, **kwargs):
    if DEBUG:
        print(args, kwargs)
        print('-' * 30)

# def pp(object, stream=None, indent=1, width=80, depth=None, *args, compact=False):
#     if DEBUG:
#         logging.info(pformat(args))
#
# def _(*args, **kwargs):
#     if DEBUG:
#         logging.info(args, kwargs)


class Common:
    s = "( c>5 or (p==4 and c<4) )"
    total_files = 1358
    file_count = 0
    # It's pyparsing.printables without ()
    CHAR_NO_ARCHED_BRAKETS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'*+,-./:;<=>?@[\]^_`{|}~'

    WEAK_TRANS_MARKER = "#-1#"
    debug_current_file_count = 0
    debug_max_file_count = 5
    debug_file = None
    debug_file = "getting_started/about/community"
    #debug_file = "animation/actions"
    # debug_file = "video_editing/sequencer/strips/transitions/wipe" # :ref:`easings <editors-graph-fcurves-settings-easing>`
    # debug_file = "about/contribute/editing"
    # debug_file = "about/contribute/build/windows"
    # debug_file = "about/contribute/build/macos"
    # debug_file = "about/contribute/guides/maintenance_guide"
    # debug_file = "about/contribute/guides/markup_guide" # debugging :term: :abbr:, ``:kbd:`LMB```, ``*Mirror*``, ``:menuselection:`3D View --> Add --> Mesh --> Monkey```
    # debug_file = "about/contribute/install/windows"
    # debug_file = "about/license" # (online) or URL (in print) to manual
    # debug_file = "addons/3d_view/3d_navigation" # debugging :menuselection:
    # debug_file = "addons/add_curve/index"
    # debug_file = "addons/add_curve/ivy_gen"
    # debug_file = "addons/import_export/anim_nuke_chan"
    # debug_file = "addons/import_export/io_scene_gltf2" # either (a) make it the active Action on the object, (b) create a single-strip NLA track, or (c)
    # debug_file = "addons/import_export/io_scene_x3d"
    # debug_file = "addons/node/node_wrangler"
    # debug_file = "addons/object/carver"
    # debug_file = "advanced/command_line/arguments"
    # debug_file = "advanced/command_line/introduction"
    # debug_file = "advanced/command_line/launch/macos"
    # debug_file = "animation/armatures/bones/editing/properties"
    # debug_file = "animation/constraints/relationship/shrinkwrap"
    # debug_file = "animation/constraints/tracking/damped_track"
    # debug_file = "compositing/types/color/color_balance"
    # debug_file = "compositing/types/color/hue_saturation"
    # debug_file = "editors/dope_sheet/introduction" # Pan the view vertically (values) or horizontally (time) with click and drag (:kbd:`MMB`).
    # debug_file = "editors/graph_editor/channels" # Box Select: (:kbd:`LMB` drag) or :kbd:`B` (:kbd:`LMB` drag)
    # debug_file = "editors/preferences/system"
    # debug_file = "editors/texture_node/types/converter/rgb_to_bw"
    # debug_file = "editors/timeline"
    # debug_file = "editors/uv/introduction"
    # debug_file = "files/media/image_formats"
    # debug_file = "getting_started/about/history"
    # debug_file = "grease_pencil/modes/draw/tool_settings/line"
    # debug_file = "interface/controls/nodes/editing"
    # debug_file = "manual/modeling/meshes/primitives"
    # debug_file = "modeling/meshes/editing/vertices"
    # debug_file = "modeling/meshes/structure"
    # debug_file = "modeling/surfaces/structure"
    # debug_file = "movie_clip/tracking/clip/properties/stabilization/introduction"
    # debug_file = "render/shader_nodes/textures/white_noise"
    # debug_file = "scene_layout/object/selecting"
    # debug_file = "scene_layout/scene/properties"
    # debug_file = "sculpt_paint/sculpting/hide_mask"
    # debug_file = "sculpt_paint/weight_paint/editing"
    # debug_file = "video_editing/sequencer/properties/strip"
    # debug_file = "video_editing/sequencer/strips/movie_image"

    KBD='kbd'
    MNU='menuselection'
    DOC='doc'
    ABBREV='abbr'
    STD_REF='std-ref'
    X_REF = 'xref'
    REF_URI='refuri'
    GUI_LAB = 'guilabel'
    TAG_ABBR='abbreviation'
    TAG_NAME='tagname'
    CLASS='classes'

    ENDS_PUNCTUAL = re.compile(r'([\.\,\:\!\?\"\*\'\`]+$)')
    BEGIN_PUNCTUAL = re.compile(r'^([\.\,\:\!\?\"\*\'\`]+)')

    WORD_ONLY = re.compile(r'\b([\w\.\/\+\-\_\<\>]+)\b')

    # dictionary: {start_location: [[s, e, match_0],[(s, e, :type:), (s, e, text), (s, e, link if any), (s, e, text-within-link | or abbreviation) ]]}
    #SPECIAL_REF = re.compile(r'(:[\w]+:)*[\`\"\'\*]+(?![\s\)\.\(]+)([^\`\("\'\*\<\>]+)(((\<([\w\-\s]+)\>\*)*)|(\(([^(]+)\))*)(?<!([\s\:]))[\`\"\'\*]+')
    #SPECIAL_REF = re.compile(r'(:[\w]+:)*[\`]+([^\`])+(((\s\<([^\<\>]+)\>)*)|(\(([^\(\)]+)\))*)(?<!([\s\:]))[\`\]+([\_]+)*')
    #SPECIAL_REF = re.compile(r'[\`]*(:\w+:)*[\`]+(?![\s]+)([^\`]+)[\`]+')
    #GA_REF = re.compile(r'[\`]*(:\w+:)*[\`]+(?![\s]+)([^\`]+)(?<!([\s\:]))[\`]+[\_]*')
    #BRACKETED = re.compile(r'(?![\s]+)[\*\"\'\(\<]+(?![\s]+)([\w\s\-]+[^\`\*\"\'\)\(\<\>]+)(?<!([\s\:]))[\*\"\'\)\>]+')

    #LITERALS = re.compile(r'([]+)*(:\w+:)*[\`]+(?![\s]+)([^\`]+)[\`]+')

    #DOUBLE_GA_REF = re.compile(r'[\`]{2}(?![\s]+)([^\`]+)(?<!([\s]))[\`]{2}')
    #MENU_PART = re.compile(r'(?![\s]+)([^\-\>]+)(?<!([\s]))')
    #NORMAL_TEXT = re.compile(r'(?![\s\-\_\.]+)([\w\-\ \/\.\']+)(?<!([\s\-\_\.\,]))')
    #NORMAL_TEXT = re.compile(r'(?![\s\-\_\.\(\)]+)(([\w\-\_\'\ \.\/]+))(?<!([\s\.\,\(\)]))')
    #NORMAL_TEXT = re.compile(r'(?![\s\.\_])([\w\s\.\']+)(?<!([\s\.]))')

    #NORMAL_TEXT = re.compile(r'(?![\s])(?![\_\.\,\:]+[\s]+[\w])(([\w\s\'\<\>\/]+)(([\=\+\*\/\.\-][\w]+)*))+(?<!([\s]))')

    #BRACKETED = re.compile(r'(?![\s]+)[\*\"\']+(?![\s]+)([\w\s\-]+[^\`\*\"\']+)(?<!([\s\:]))[\*\"\']+')
    #BRACKETED = re.compile(r'[\*\"]+(?![\s\.\,]+)([^\`\*\"]+)[\*\"]+(?<!([\s\.\,]))')

    #NORMAL_TEXT = re.compile(r'(?![\s])(?![\_\.\,\:]+[\s]+[\w])(([\w\s\'\<\>\/]+)(([\=\+\*\/\.\-][\w]+)*))+(?<!([\s]))')
    #MENU_PART = re.compile(r'(?![\s]+)([^\-\>]+)(?<!([\s]))')
    #MENU_PART = re.compile(r'(?!([-]{2}\>))(.*)')
    #MENU_PART = re.compile(r'\b((?![\s]?[-]{2}[>]?[\s]+).)*\b') #working but with empty entries

    GA_REF = re.compile(r'[\`]*(:\w+:)*[\`]+(?![\s]+)([^\`]+)(?<!([\s\:]))[\`]+[\_]*')
    GA_REF_ONLY = re.compile(r'^[\`]*(:\w+:)*[\`]+(?![\s]+)([^\`]+)(?<!([\s\:]))[\`]+[\_]*$')
    #ARCH_BRAKET = re.compile(r'[\(]+(?![\s\.\,]+)([^\(\)]+)[\)]+(?<!([\s\.\,]))')

    # this (something ... ) can have other links inside of it as well as others
    # the greedy but more accurate is r'[\(]+(.*)?[\)]+'
    # ARCH_BRAKET_SINGLE_PARTS = re.compile(r'[\)]+([^\(]+)?[\(]+')
    # ARCH_BRAKET_SINGLE_FULL = re.compile(r'[\(]+([^\)]+)?[\)]+')
    #ARCH_BRAKET_MULTI = re.compile(r'[\(]+(.*)?[\)]+')

    ARCH_BRAKET_MULTI = re.compile(r'[\(]+(.*)[\)]+')

    AST_QUOTE = re.compile(r'[\*]+(?![\s\.\,\`\"]+)([^\*]+)[\*]+(?<!([\s\.\,\`\"]))')
    DBL_QUOTE = re.compile(r'[\"]+(?![\s\.\,\`]+)([^\"]+)[\"]+(?<!([\s\.\,]))')
    SNG_QUOTE = re.compile(r'[\']+(?![\`\s\.(s|re|ll|t)]+)([^\']+)[\']+')

    LINK_WITH_URI=re.compile(r'([^\<\>\(\)]+[\w]+)[\s]+[\<\(]+([^\<\>\(\)]+)[\>\)]+[\_]*')
    MENU_PART = re.compile(r'(?![\s]?[-]{2}[\>]?[\s]+)(?![\s\-])([^\<\>]+)(?<!([\s\-]))') # working but with no empty entries

    WORD_ONLY_FIND = re.compile(r'\b[\w\-\_\']+\b')

    ENDS_WITH_EXTENSION = re.compile(r'\.([\w]{2,5})$')
    MENU_KEYBOARD = re.compile(r':(kbd|menuselection):')
    MENU_TYPE = re.compile(r'^([\`]*:menuselection:[\`]+([^\`]+)[\`]+)$')
    KEYBOARD_TYPE = re.compile(r'^([\`]*:kbd:[\`]+([^\`]+)[\`]+)$')
    KEYBOARD_SEP = re.compile(r'[^\-]+')
    SPECIAL_TERM = re.compile(r'^[\`\*\"\'\(]+(.*)[\`\*\"\'\)]+$')

    def isSpecialTerm(msg: str):
        is_special = (Common.SPECIAL_TERM.search(msg) is not None)
        return is_special

    def matchCase(from_str, to_str):
        new_str = str(to_str)
        is_title = (from_str.istitle())
        if is_title:
            new_str = new_str.title()
        else:
            is_upper = (from_str.isupper())
            if is_upper:
                new_str = new_str.upper()
            else:
                is_lower = (from_str.islower())
                if is_lower:
                    new_str = new_str.lower()
        return new_str

    def removeOriginal(msg, trans):
        msg = re.escape(msg)
        p = r'\b{}\b'.format(msg)
        has_original = (re.search(p, trans, flags=re.I) != None)
        endings=("", "s", "es", "ies", "ed", "ing", "lly",)

        if has_original:
            for end in endings:
                p = r'-- {}{}'.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

                p = r' ({}{})'.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

            for end in endings:
                p = r'{}{} --'.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

                p = r'({}{}) '.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

            for end in endings:
                p = r'\\b{}{}\\b'.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

                p = r'\\b({}{})\\b'.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

            trans = trans.strip()
            is_empty = (len(trans) == 0)
            if is_empty:
                trans = None

        return trans


    def patternMatchAll(pat, text):
        try:
            # itor = pat.finditer(text)
            # print("itor", type(itor))
            # print("dir", dir(itor))

            for m in pat.finditer(text):
                original = ()
                break_down = []

                s = m.start()
                e = m.end()
                orig = m.group(0)
                original = (s, e, orig)

                for g in m.groups():
                    if g:
                        i_s = orig.find(g)
                        ss = i_s + s
                        ee = ss + len(g)
                        v=(ss, ee, g)
                        break_down.append(v)
                yield original, break_down

        except Exception as e:
            _("patternMatchAll")
            _("pattern:", pat)
            _("text:", text)
            _(e)
        return None, None

    def getListOfLocation(find_list):
        loc_list = {}
        for k, v in find_list.items():
            s = v[0][0]
            e = v[0][1]
            t = v[0][2]
            entry = {k: [s, e, t]}
            loc_list.update(entry)
        return loc_list

    def inRange(item, ref_list):
        i_s, i_e, i_t = item
        for k, v in ref_list.items():
            r_s, r_e, r_t = v
            is_in_range = (i_s >= r_s) and (i_e <= r_e)
            if is_in_range:
                return True
        else:
            return False

    def diffLocation(ref_list, keep_list):
        loc_keep_list = {}
        for k, v in keep_list.items():
            in_forbiden_range = Common.inRange(v, ref_list)
            if not in_forbiden_range:
                s, e, txt = v
                ee = (s, e, txt)
                entry = {s: [ee]}
                loc_keep_list.update(entry)

        return loc_keep_list

    def mergeTwoLists(primary, secondary):

        loc_primary_list = Common.getListOfLocation(primary)
        loc_secondary_list = Common.getListOfLocation(secondary)
        keep_list = Common.diffLocation(loc_primary_list, loc_secondary_list)

        #pp(keep_list)
        for k, v in keep_list.items():
            keep_v = secondary[k]
            entry={k:keep_v}
            primary.update(entry)

        return primary

    def filteredTextList(ref_list, norm_list):
        loc_ref_list = Common.getListOfLocation(ref_list)
        loc_norm_list = Common.getListOfLocation(norm_list)
        keep_norm_list = Common.diffLocation(loc_ref_list, loc_norm_list)
        return keep_norm_list

    def getTextListForMenu(text_entry):
        #print("getTextListForMenu", text_entry, txt_item)
        entry_list = []

        its, ite, txt = text_entry
        _("menu_list: its, ite, txt")
        _(its, ite, txt)

        menu_list = Common.patternMatchAll(Common.MENU_PART, txt)
        _("menu_list")
        pp(menu_list)
        for mk, mi in menu_list.items():
            ms, me, mtxt = mi[0]
            is_empty = (ms == me)
            if (is_empty):
                continue

            ss = its + ms
            se = ss + len(mtxt)
            entry=(ss, se, mtxt)
            entry_list.append(entry)
        pp(entry_list)
        return entry_list

    def getTextListForURI(text_entry, uri_list):
        # print("getTextListForURI", text_entry, uri_list)
        entry_list = []
        for uri_k, uri_v in uri_list.items():
            uri_orig_text, uri_text, uri_link = uri_v
            tes, tee, text = text_entry
            uris, urie, uritext = uri_text
            uss = tes + uris
            use = uss + len(uritext)
            entry = (uss, use, uritext)
            entry_list.append(entry)
        return entry_list

    def getTextListForABBR(text_entry):
        entry_list = []

        s, e, txt = text_entry
        abbr_list = Common.patternMatchAll(Common.LINK_WITH_URI, txt)
        has_abbr = (len(abbr_list) > 0)
        if has_abbr:
            for abbr_k, abbr_v in abbr_list.items():
                abbr_orig_text, abbr_text, abbr_full_text = abbr_v

                tes, tee, text = text_entry
                abbr_s, abbr_e, abbr_entry_text = abbr_full_text

                _("abbr_s, abbr_e, abbr_entry_text")
                _(abbr_s, abbr_e, abbr_entry_text)

                abr_s = tes + abbr_s
                abr_e = s + len(abbr_entry_text)
                entry = (abr_s, abr_e, abbr_entry_text)
                entry_list.append(entry)
        _("exit from entry_list:", entry_list)
        return entry_list

    def isListEmpty(list_elem):
        is_empty = (list_elem is None) or (len(list_elem) == 0)
        return is_empty

    def refEntry(ref_list):
        entry_list = {}
        is_empty = Common.isListEmpty(ref_list)
        if is_empty:
            return entry_list

        k, v = None, None
        v_len = -1
        s = e = ss = se = xs = xe = 0
        txt = xtype = origin_entry = type_entry = text_entry = None
        try:
            for k, v in ref_list.items():
                orig = v[0]
                o_s, o_e, o_txt = orig

                is_menu_or_keyboard = (Common.MENU_KEYBOARD.search(o_txt) is not None)
                has_commond_keyboard = Common.NORMAL_KEYBOARD_COMBINATION.search(o_txt)
                if has_commond_keyboard:
                    continue

                key = o_s
                entry={o_s:[(o_s, o_e, o_txt)]}
                entry_list.update(entry)
                v_len = len(v)
                s, e, txt, xtype = None, None, None, None
                if (v_len == 1):
                    s, e, txt = orig
                    text_entry = (s, e, txt)
                elif (v_len == 2):
                    origin_entry, text_entry = v
                    s, e, txt = text_entry
                elif (v_len == 3):  # :kbd:,
                    origin_entry, type_entry, text_entry = v
                    xs, xe, xtype = type_entry
                    s, e, txt = text_entry
                else:
                    raise Exception("Impossible List, there are more items than expected!")

                has_xtype = (xtype is not None)
                has_menu = has_xtype and ("menuselection" in xtype)
                has_abbr = has_xtype and ("abbr" in xtype)
                has_kbd = has_xtype and ("kbd" in xtype)
                uri_list = Common.patternMatchAll(Common.LINK_WITH_URI, txt)

                has_uri = not Common.isListEmpty(uri_list)
                if has_uri and not (has_abbr or has_menu):
                    _("has_uri and not has_abbr")
                    uri_entry_list = Common.getTextListForURI(text_entry, uri_list)
                    entry_list[key].append(uri_entry_list)
                elif has_xtype:
                    if has_abbr:
                        _("has_abbr")
                        abbr_list = Common.getTextListForABBR(text_entry)
                        entry_list[key].append(abbr_list)
                        pp(entry_list[key])
                    elif has_menu:
                        _("has_menu")
                        menu_text_list = Common.getTextListForMenu(text_entry)
                        entry_list[key].append(menu_text_list)
                        pp(menu_text_list)
                    else:
                        _("has_xtype but NOT ABBR OR MENU:", text_entry)
                        entry_list[key].append([text_entry])
                else:
                    entry_list[key].append([text_entry])
        except Exception as e:
            _(ref_list)
            _("k, v, v_len")
            _(k, v, v_len)
            raise e
        return entry_list

    def removeLowerCaseDic(dic_list):
        l_case = {}
        u_case = {}
        k = None
        v = None
        try:
            for i, e in enumerate(dic_list.items()):
                k, v = e
                if not k:
                    continue

                is_lower_k = (k.islower())
                if is_lower_k:
                    l_case.update({k: v})
                else:
                    u_case.update({k: v})

            u_l_case = dict((k.lower(), v) for k, v in u_case.items())

            l_case_remain = {}
            for k, v in l_case.items():
                if k in u_l_case:
                    continue
                else:
                    l_case_remain.update({k: v})
            u_case.update(l_case_remain)
        except Exception as e:
            _("k:", k)
            _("v:", k)
            _(e)
            raise e
        return u_case

    def isTextuallySimilar(from_txt, to_txt, is_absolute=False):
        from_list = Common.WORD_ONLY_FIND.findall(from_txt.lower())
        to_list = Common.WORD_ONLY_FIND.findall(to_txt.lower())

        # convert list to set of words, non-repeating
        to_set = set(to_list)
        from_set = set(from_list)

        # perform set intersection to find common set
        common_set = to_set.intersection(from_set)

        common_len = len(common_set)
        from_len = len(from_set)
        # to_len = len(to_set)
        considering_match = (float(common_len) >= (float(from_len) * 0.5))  # matching more than 50%

        is_considered_the_same = (common_set == from_set) or (common_set == to_set)
        if not is_absolute:
            is_considered_the_same = (is_considered_the_same or considering_match)
        
        if is_considered_the_same:
            entry={from_set: to_set}
            print("isTextuallySimilar:", entry)

        return is_considered_the_same


    def isTextuallySame(from_txt, to_txt):
        from_list = Common.WORD_ONLY_FIND.findall(from_txt.lower())
        to_list = Common.WORD_ONLY_FIND.findall(to_txt.lower())

        # convert list to set of words, non-repeating
        to_set = set(to_list)
        from_set = set(from_list)

        # perform set intersection to find common set
        common_set = to_set.intersection(from_set)
        is_same = (common_set == from_set)
        return is_same

    def isTextuallySubsetOf(msg, tran):
        msg_list = Common.WORD_ONLY_FIND.findall(msg.lower())
        tran_list = Common.WORD_ONLY_FIND.findall(tran.lower())

        # convert list to set of words, non-repeating
        tran_set = set(tran_list)
        msg_set = set(msg_list)

        # perform set intersection to find common set
        is_subset = msg_set.issubset(tran_set)
        return is_subset

    def alterValue(orig_value, alter_value=0, op=None):
        altering = (op is not None)
        if altering:
            if op == "+":
                orig_value += alter_value
            elif op == "=":
                orig_value -= alter_value
            elif op == "*":
                orig_value *= alter_value
            elif op == "/":
                orig_value /= alter_value
            elif op == "%":
                orig_value %= alter_value
            elif op == "=":
                orig_value = alter_value
        return orig_value

    def parseMessageWithDelimiterPair(open_char, close_char, msg):
        valid = (open_char is not None) and (close_char is not None) and (msg is not None) and (len(msg) > 0)
        if not valid:
            return None

        is_pair_same_char = (open_char == close_char)
        if is_pair_same_char:
            raise Exception("Open and close symbols must not be the same!")

        loc_list:list = []
        b_list=[]
        l = len(msg)
        s = e = 0
        k = -1
        for i in range(0, l):
            c = msg[i]
            is_open = (c == open_char)
            is_close = (c == close_char)
            if is_open:
                b_list.append(i)
            elif is_close:
                try:
                    last_s = b_list[-1]
                    b_list.pop()
                    txt = msg[last_s:i+1]
                    loc_list_entry=(last_s, i+1, txt)
                    loc_list.append(loc_list_entry)

                    ll = msg[:last_s]
                    rr = msg[i+1:]
                    ltxt = ll + txt + rr
                    is_same = (ltxt == msg)
                    if not is_same:
                        raise Exception("ERROR in location calculation for: [", txt, "] at start:", last_s, " end:", i+1, " in:[", msg, "]")
                except Exception as e:
                    continue
                    # msg = "Unbalanced pair [{},{}] at location:{}, message:[{}]".format(open_char, close_char, i, msg)
                    # print(e)
                    # raise Exception(msg)

        # has_unprocessed_pair = (len(b_list) > 0)
        # if has_unprocessed_pair:
        #     # msg = "Unbalanced pair [{},{}] at location:{}, message:[{}]".format(open_char, close_char, b_list, msg)
        #     # raise Exception(msg)

        has_loc_list = (len(loc_list) > 0)
        if not has_loc_list:
            return []
        else:
            sorted_loc_list = []
            sorted_loc_list = sorted(loc_list, key=lambda x: x[0])
            return sorted_loc_list


