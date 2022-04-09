import re
import os
from collections import OrderedDict, defaultdict
from sphinx_intl import catalog as c
from common import Common as cm
from utils import dd, pp
from matcher import MatcherRecord
from definition import Definitions as df, RefType, TranslationState
from pattern_utils import PatternUtils as pu
from enum import Enum
from babel.messages import Catalog, Message
from pprint import pprint as pp
from potask_base import POTaskBase


class CaseType(Enum):
    UPPER = 0
    TITLE = 1
    LOWER = 2
    MIXED = 3
    NONE = 4
    ERASE = 5

# class ProblemDomain(Enum):
#     REF_WITH_LINK = 0
#     REF_WRONG_CASES = 1
#     GA_WITH_LINK = 2
#
#     @classmethod
#     def getListOfMembers(self):
#         if not hasattr(self, 'member_list'):
#             member_list = [member for (name, member) in self.__members__.items()]
#             setattr(self, 'member_list', member_list)
#         return getattr(self, 'member_list', [])

class CleanRef(POTaskBase):
    quotes = r'[\%s\%s\%s]+' % (RefType.AST_QUOTE.value,
                                RefType.DBL_QUOTE.value,
                                RefType.SNG_QUOTE.value
                                )

    begin_quote_pattern_txt = r'^%s' % quotes
    end_quote_pattern_txt = r'%s$' % quotes
    all_quoted_txt = r'^(%s|\s+)$' % quotes
    ALL_QUOTES = re.compile(all_quoted_txt)

    BEGIN_QUOTED = re.compile(begin_quote_pattern_txt)
    END_QUOTED = re.compile(end_quote_pattern_txt)
    MIXED_CASE_ONEWORD = re.compile(r'([A-Z]+[a-z]+[A-Z]+)|([a-z]+[A-Z]+[a-z]+)')
    MIXED_CASES = re.compile(r'([A-Z]+[a-z]+)|([a-z]+[A-Z]+)|([A-Z]+).*?([a-z]+)|([a-z]+).*?([A-Z]+)')
    REF_GENERIC_STARTER = re.compile(r':\w+:')
    REF_LINK = re.compile(r'(<[^<>]+>)')
    excluded_ref_type = [
        RefType.KBD
    ]
    must_be_upper_case = [
        'GNU',
        'GPL',
        'HTML',
        'RGB',
        'RGBA',
        'Alpha',
        'PDF',
        'UV',
        '2D',
        '3D',
        '4D',
    ]
    ignore_start_with = [
        'tham chiếu nhắc nhở',
        'ngôi thứ nhất',
        'SVN Checkout ...',
        'URL of repository',
        '\'locale\' is not under version control',
        'góc nhìn VR',
        'Cắt Nội Khung Xương Thẳng Đứng',
        'thông điệp',
    ]
    start_with_list = [
        # '^(([A-Z][a-z]+)(([A-Z][a-z]+){1,}))+$',
        # '^(([A-Z]+[a-z]+[A-Z]+)|([a-z]+[A-Z]+[a-z]+))$',
        # '^([A-z]+([\/][A-z]+){1,}(\.[A-z]+)?)$',
        # '^()$',
        # '^()$',
        '^#',
        '^(([0-9]D))$',
        '^(AOV|object hooks)$',
        '^(API|ellipsoid|Gaussian|bilateral|Vài Giây|make help|make|\d+\.\w+|DCT)$',
        '^(API)$',
        '^(ASCII)$',
        '^(AnimD\w+)$',
        '^(Azimuth)$',
        '^(B-Bone)$',
        '^(BVH)$',
        '^(BW)$',
        '^(Basis)$',
        '^(Blend)$',
        '^(Blender[\-\{\}\w]+)$',
        '^(Bone(\.\d+)?)$',
        '^(C-key)$',
        '^(cmd|HDTV|build)$',
        '^(C4D TRACER)$',
        '^(CCW)$',
        '^(CPU|Suzanne|LDR|Premul\.|HSV, XYZ|min|max|text3D|OSKey|hectometer|GNU)$',
        '^(CW)$',
        '^(DMG)$',
        '^(DOF)$',
        '^(DPI)$',
        '^(Diff file)$',
        '^(F-K)',
        '^(FBX AnimS)',
        '^(FFV1)$',
        '^(False)$',
        '^(Flip)$',
        '^(Float)$',
        '^(fuzzy)$',
        '^(GIT)$',
        '^(GPU)$',
        '^(HDR)$',
        '^(HTML)$',
        '^(ID\w?)$',
        '^(Key\s\d+)',
        '^(LSCM)$',
        '^(Lattice)$',
        '^(LocRotScale)$',
        '^(MIP)$',
        '^(MULTIRES)$',
        '^(Maya)$',
        '^(MixRGB)$',
        '^(NDKDH)$',
        '^(NURBS)$',
        '^(NaN)$',
        '^(No\-Op)',
        '^(None)$',
        '^(Null)$',
        '^(OBJ)$',
        '^(OPEN_\w+)$',
        '^(OSA)$',
        '^(off|on|not|none|url|[234]D|nothing|press\/release|50\/50|' \
        'vtx|vram|vse|vr|vp\d+|v2x|jpeg|jpg|json|kde|rst|dev|parts|mirror|figure|version|' \
        'ssao|pip(3)?|modeling|color|modelling|colour|xyz is|Checkout directory|OK|tag(s)?|' \
        'patch(es)?|svn update|commit|change|commit hash|hash|bcon\d?|Subscriber(s)?|' \
        'msgstr|msgid|locale|batch\/shell|PO editor|Preferences|gpl|mathutils|measureit|HMD|haptics|' \
        'VR Session|BTracer|Doodads|chan|STL|DXF|IPO|FBX|X3D|Analemma|HDRI|XALL|BIX|LRT|IOR|Include|' \
        'Rainbow|Power Sequencer|SYSTEM|USER|LOCAL|core API|OSKey|Tweak|iTaSC|DLS|HSV|remap|foot, feet|' \
        'mile|micrometer|millimeter|meter|dekameter, decimeter|furlong|IES|Tiger|Jello|subsurf|IME)$',
        '^(PBR)$',
        '^(PCTD)$',
        '^(PDB)$',
        '^(PIC)$',
        '^(POV)$',
        '^(PYTHON\w+?)$',
        '^(Python API)$',
        '^(QCD)$',
        '^(QI)$',
        '^(RCSB)$',
        '^(RGB)$',
        '^(RGBA)$',
        '^(RIG\w+)$',
        '^(Root|AO|blogs)$',
        '^(subversion|svn|Hosek\/Wilkie|Closure|BSDF|Sphere Sweep|VFX|HSL|I‑frame(s)?|n\-Dimensions|OpenColorIO)$',
        '^(SDLS)$',
        '^(SDL_)',
        '^(SFX)$',
        '^(SPH)$',
        '^(SRID)$',
        '^(SSLT)$',
        '^(SSR)$',
        '^(SSS)$',
        '^(SVN)$',
        '^(TCKDH)$',
        '^(TCKDH)$',
        '^(THTQXMT)$',
        '^(TV)$',
        '^(True)$',
        '^(UV)$',
        '^(VBO)$',
        '^(Wmownerid)$',
        '^(YCC)$',
        '^([-]{2})',
        '^([A-z]&[A-z])$',
        '^([Bb]]lender(\s\w+)?)$',
        '^([Bb]lender(\.\w+)?)$',
        '^([IF]K)$',
        '^([\-]+)',
        '^(((\w+[-\.\_]){1,})+\w+)$',
        '^([\w\.])$',
        '^([\w_])$',
        '^([_][RL])$',
        '^(\.[LR])$',
        '^(\/)',
        '^(\w+([\_]\w+){1,})$',
        '^(\w{1})$',
        '^(dash)$',
        '^(dyntopo)$',
        '^(enum)$',
        '^(float)$',
        '^(float)$',
        '^(fuzzy)$',
        '^(gap)$',
        '^(grayscale)$',
        '^(handLeft)$',
        '^(handRight)$',
        '^(int)$',
        '^(left)$',
        '^(math)$',
        '^(mip-map)$',
        '^(multum in parvo)$',
        '^(null)$',
        '^(on-demand)$',
        '^(on-the-fly)$',
        '^(os\w+?)$',
        '^(it is)$',
        "'pic' ture 'el' ement",
        '^(poly(\w+))$',
        '^(pixel(\w+)?)$',
        '^(pa\.s)$',
        '^(pose\w+)$',
        '^(pyd|AA)',
        '^(right|fps)$',
        '^(to_spa)',
        '^(vgroup|vividlight|workbench|gizmo|vr|bu|dpi|dots|rdp|gui|motion|blender publisher|xml|uuid|usd|udim|ai|integer)$',
        '^(callback|add|set|press|click|spacebar|dof|restructuredtext|vbo|cannot|cad|hdmi|:\w+:|user(\w+?))$',
        '^(\$[^\$]+|TOC|Blender UI|bindpose|Freestyle|PCTD|dot|[75]\.1 Surround|mono|stereo|Hilbert Spiral|boolean)$',
        '^(TMP|TEMP|RegionV|mikkt|microf|equirect)',
        '(\.\w+)|(404)$',
        '^(wmOwnerID|ge|fisheye|AOV|nurbs|statefull|shaderfx|path|polygon\w+|super|mpeg)$',
        '^(z-buffer)$',
        '^UI',
        '^\/',
        '^\|',

        # '^(THTQXMT|HDR|SSR|True|False|Bone(\.\d+)?|Basis|\w{1}|dash|MIP|multum in parvo|Null|Root)$',
        # '^(\w+([\_]\w+){1,})|handLeft|handRight|C-key|RGB|RGBA|(([A-Z][a-z]+)(([A-Z][a-z]+){1,}))+$',
        # '^(\.([LR]|left|right))|([0-9]D)|(wmOwnerID|Wmownerid|float|Float|BVH|NaN|gap|MixRGB|LocRotScale)$'
    ]

    translation_outside_pattern = re.compile(r'^:(term|ref):\`')
    is_gui_pattern = re.compile(r'^:guilabel:\`')
    solved_count = 0

    def __init__(self,
                 input_file=None,
                 output_to_file=None
                 ):
        POTaskBase.__init__(
            self,
            input_file=input_file,
            output_to_file=output_to_file
        )
        self.resetVars()
        self.title_file = os.path.join(self.home, 'keep.log')
        self.title_list = self.readFile(self.title_file)

    def resetVars(self):
        self.oloc = None
        self.otxt = None
        self.typeloc = None
        self.type_txt = None
        self.vnloc = None
        self.vn_txt = None
        self.enloc = None
        self.en_txt = None
        self.lkloc = None
        self.link_txt = None
        self.has_link = None
        self.is_link_changed = False

        self.m = None

        self.is_en_first = False
        self.orig_en_txt = None
        self.orig_link_txt = None
        self.begin_quote = None
        self.end_quote = None
        self.new_txt = None
        self.old_txt = None
        self.problem_list = None
        self.message = None
        self.matcher_record = None
        self.solved_count = 0
        self.result_list = None
        self.orig_mm_list = None
        self.pair_prob_orig = None

        self.is_link_changed = False
        self.is_translation_outside = False
        self.has_orig = False
        self.has_orig_link = False
        self.is_gui_label = False
        self.message_list = None
        self.is_changed = False
        self.vn_ref_list = []
        self.begin_quote_removable = None
        self.end_quote_removable = None
        self.ref_text = None
        self.ref_loc = None
        self.is_continue_if_no_paring_found=True

    def isInStartWithList(self, txt: str):
        def compare(pattern_txt):
            m: re.Match = None
            try:
                p_txt = r'%s' % (pattern_txt)
                p = re.compile(p_txt, re.I)
                m = p.search(txt)
                # if bool(m):
                #     print(f'isEnTextGoesFirst(): [{pattern_txt}] in the [{txt}], English goes first {self.en_txt} => {self.vn_txt}')
            except Exception as e:
                msg = f'ERROR: isEnTextGoesFirst() compare():\ntxt:[{txt}]\npattern:[{p_txt}]\n{e}'
                raise RuntimeError(msg)
            return (m is not None)

        has_start_with_list = list(filter(compare, CleanRef.start_with_list))
        # if has_start_with_list:
        #     msg = f'isInStartWithList(), txt:{txt}, {has_start_with_list}'
        #     print(msg)
        return (len(has_start_with_list) > 0)

    def getMsgstrPattern(self):
        return None

    def getMsgidPattern(self):
        return None

    def getTextFunction(self, matcher_record: MatcherRecord):
        return None

    def formatOutput(self):
        pass

    def isIgnoreEntry(self, mm: MatcherRecord):
        return False

    def reportIfRepeatQuoted(self, txt, quote):
        try:
            is_emtpy = not bool(quote)
            if is_emtpy:
                return

            pat_txt = r'[\%s]{2, }' % (quote)
            pat_begin_txt = r'^(%s)' % (pat_txt)
            pat_end_txt = r'(%s)$' % (pat_txt)
            pattern_begin = re.compile(pat_begin_txt)
            pattern_end = re.compile(pat_end_txt)
            is_begin_repeated = (pattern_begin.search(txt) is not None)
            is_end_repeated = (pattern_begin.search(txt) is not None)
            is_repeated = (is_begin_repeated or is_end_repeated)
            if is_repeated:
                msg = f'{self.__class__.__name__} REPEATED QUOTE: {txt}, quote:[{quote}]'
                raise RuntimeError(msg)
        except Exception as e:
            raise e

    def findMatchingPair(self, vn_word):
        txt_word_pat_txt = r'%s' % (vn_word)
        p = re.compile(txt_word_pat_txt, re.I)
        match = p.search(self.orig_en_txt)
        is_found = (match is not None)
        if is_found:
            en_word = match.group(0)
            return (vn_word, en_word)
        else:
            return (None, None)

    def repeatWordsInOrigin(self):
        def replace_word(word_to_replace):
            replace_txt = r'%s' % (word_to_replace)
            is_escape = (df.NOT_CHARS_AND_SPACES.search(replace_txt) is not None)
            replace_pattern_txt = (re.escape(replace_txt) if is_escape else replace_txt)
            replace_pattern_txt = r'\b%s\b' % (replace_pattern_txt)
            replace_pattern = re.compile(replace_pattern_txt, re.I)
            (self.vn_txt, replaced_count) = replace_pattern.subn(word_to_replace, self.vn_txt)
            # if replaced_count > 0:
            #     is_debug = True
            return replaced_count

        is_valid = bool(self.orig_en_txt) and bool(self.vn_txt)
        if not is_valid:
            return

        # is_debug = ('The *RGB Curves Node* allows' in self.m.id)
        # if is_debug:
        #     is_debug = True

        old_vn_str = str(self.vn_txt)
        replaced_count = replace_word(self.orig_en_txt)
        orig_en_word_list = (self.orig_en_txt.split())
        replaced_count_list = list(map(replace_word, orig_en_word_list))
        replaced_count_list.append(replaced_count)
        replaced_count_list = [x for x in replaced_count_list if x > 0]
        is_replaced = bool(replaced_count_list) and (len(replaced_count_list) > 0)
        # if is_replaced:
        #     print(replaced_count_list)


    def enforceLowerCase(self, orig_en_txt: str, txt: str, char_before_first='`') -> str:
        def to_lower(pattern: re.Pattern, old_txt: str, is_first_title_if_possible=False):
            parts = pu.patternMatchAll(pattern, old_txt, reversed=True)
            has_work_to_be_done = (bool(parts) and len(parts) > 0)
            if not has_work_to_be_done:
                return old_txt

            new_txt = str(old_txt)
            for index, (loc, mm) in enumerate(parts.items()):
                should_be_title = False
                if is_first_title_if_possible:
                    (ss, ee) = loc
                    prev_ss = (ss - 1)
                    prev_char = (new_txt[prev_ss] if prev_ss >= 0 else None)
                    is_orig_lower = (bool(orig_en_txt) and orig_en_txt.islower())
                    should_be_title = (bool(prev_char) and prev_char == char_before_first and not is_orig_lower)
                if should_be_title:
                    new_txt = cm.jointText(new_txt, mm.txt.title(), loc)
                else:
                    new_txt = cm.jointText(new_txt, mm.txt.lower(), loc)
            return new_txt

        new_txt = to_lower(df.GA_REF_PART, txt)
        new_txt = to_lower(df.ALL_WORDS_SHOULD_BE_LOWER, new_txt, is_first_title_if_possible=True)
        return new_txt

    def swap_text(self):
        def swap_value(first, second):
            temp = first
            first = second
            second = temp
            return (first, second)

        is_en_started = self.isInStartWithList(self.en_txt)
        is_vn_started = self.isInStartWithList(self.vn_txt)
        if is_en_started:
            (self.en_txt, self.vn_txt) = swap_value(self.en_txt, self.vn_txt)
        elif is_vn_started:
            return
        else:
            is_en_ascii = self.en_txt.isascii()
            is_vn_ascii = self.vn_txt.isascii()
            if is_vn_ascii:
                (self.en_txt, self.vn_txt) = swap_value(self.en_txt, self.vn_txt)

    def extract_orig_records(self):
        mm: MatcherRecord = None
        orig_dict = OrderedDict()
        for mm in self.orig_mm_list:
            sub_list = mm.getSubEntriesAsList()
            (oloc, orig_otxt) = sub_list[0]
            (typeloc, orig_type_txt) = sub_list[1]
            try:
                (oloc, orig_en_txt) = sub_list[2]
            except Exception as e:
                is_debug = True

            has_link = (len(sub_list) > 3)
            if has_link:
                (oloc, orig_link_txt) = sub_list[3]
            else:
                orig_link_txt = None

            entry = {(orig_type_txt.lower(), orig_en_txt.lower()): (orig_en_txt, orig_link_txt)}
            orig_dict.update(entry)
        return orig_dict

    def removeQuotesSurroundingText(self, txt):
        begin_match = CleanRef.BEGIN_QUOTED.search(txt)
        end_match = CleanRef.END_QUOTED.search(txt)
        is_begin_quoted = (begin_match is not None)
        is_end_quoted = (end_match is not None)
        is_remove_quote = (is_begin_quoted and is_end_quoted)

        begin_match_txt = ""
        end_match_txt = ""
        if is_remove_quote:
            begin_match_txt = begin_match.group(0)
            end_match_txt = end_match.group(0)
            new_txt = txt[len(begin_match_txt):-len(end_match_txt)]
        else:
            new_txt = txt
        return (new_txt, begin_match_txt, end_match_txt)

    def get_list_of_possible_patterns(self):
        has_symbols = (df.SYMBOLS.search(self.en_txt) is not None)
        if has_symbols:
            en_escaped_txt = re.escape(self.en_txt)
            case_one = r'%s(%s)%s' % (CleanRef.quotes, en_escaped_txt, CleanRef.quotes)
            case_two = r'%s' % (en_escaped_txt)
            case_three = r'\b(%s)\b' % (en_escaped_txt)
        else:
            case_one = r'%s(%s)%s' % (CleanRef.quotes, self.en_txt, CleanRef.quotes)
            case_two = r'%s' % (self.en_txt)
            case_three = r'\b(%s)\b' % (self.en_txt)

        possible_patterns = [
            case_three,
            case_one,
            case_two,
        ]
        return possible_patterns

    def extract_orig_en_record(self, msg: Message):
        orig_dict = self.extract_orig_records()
        key = (self.type_txt.lower(), self.en_txt.lower())
        is_in = (key in orig_dict)
        if is_in:
            (self.orig_en_txt, self.orig_link_txt) = orig_dict[key]

    def find_orig(self, msg: Message):
        # self.orig_en_txt, self.orig_link_txt
        # is_debug = ('At very low values' in msg.id)
        # if is_debug:
        #     is_debug = True
        self.orig_en_txt = None
        self.orig_link_txt = None
        self.extract_orig_en_record(msg)

        orig_txt = None
        possible_patterns = self.get_list_of_possible_patterns()
        try:
            # case_three = possible_patterns[0]
            # case_one = possible_patterns[1]
            # case_two = possible_patterns[2]
            is_found = False
            error_patterns = []
            for index, pat_txt in enumerate(possible_patterns):
                find_pattern = re.compile(pat_txt, re.I)
                match = pu.patternMatchAll(find_pattern, msg.id)
                is_in_orig = bool(match) and (len(match) > 0)
                if is_in_orig:
                    is_found = True
                    (loc, mm) = list(match.items())[0]
                    sub_list = mm.getSubEntriesAsList()
                    sub_list_index = (0 if (index in [0, 2]) else 1)
                    entry = sub_list[sub_list_index]
                    self.orig_en_txt = entry[1]
                    o_loc = entry[0]
                    break
                else:
                    error_patterns.append(pat_txt)
            if not is_found:
                error_msg = f'NOT FOUND ERROR: Unable to find: {error_patterns} in original message:\nmsgid: [{msg.id}]'
                print(error_msg)
                # error_msg += f'{error_patterns}'
        except Exception as e:
            error_msg = f'Exception ERROR: Unable to find: {error_patterns} in original message:\nmsgid: [{msg.id}]'
            start_index = (str(msg.id).find(self.en_txt))
            is_in_orig = (start_index >= 0)
            if not is_in_orig:
                print(error_msg + f'\nException: {e}')
                # raise RuntimeError(error_msg + f'\nException: {e}')
            else:
                end_index = (start_index + len(self.en_txt))
                self.orig_en_txt = (msg.id[start_index: end_index])

    def transpose_matching_case(self, orig: str, old: str, prefer_case=CaseType.NONE, when=False):
        def convert_case_op(entry):
            flag : CaseType = None
            txt : str = None
            (flag, txt) = entry
            if flag == CaseType.TITLE:
                new_txt = txt.title()
            elif flag == CaseType.LOWER:
                new_txt = txt.lower()
            elif flag == CaseType.UPPER:
                new_txt = txt.upper()
            elif flag == CaseType.MIXED:
                new_txt = txt.title()
            else:
                new_txt = txt
            return new_txt

        valid = bool(orig) and bool(old)
        if not valid:
            return old

        # deb_p = re.compile('adding extra options', re.I)
        # is_debug = (deb_p.search(self.m.id) is not None)
        # if is_debug:
        #     is_debug = True

        has_start_with = self.isInStartWithList(old)
        if has_start_with:
            return old

        current_ref_type = (RefType.getRef(self.type_txt) if bool(self.type_txt) else None)
        valid = bool(current_ref_type) and (current_ref_type not in CleanRef.excluded_ref_type)
        if not valid:
            return old

        # en_txt_word_list = self.en_txt.split()
        # has_colon_in_vn = (': ' in self.vn_txt)
        # is_en_single_word_and_is_upper = (len(en_txt_word_list) == 1) and (self.en_txt.isupper())

        old_copy = str(old)
        is_use_prefer_case = when and (prefer_case != CaseType.NONE)
        if is_use_prefer_case:
            new = convert_case_op((prefer_case, old))
        else:
            # is_mixed_case_oneword = (CleanRef.MIXED_CASE_ONEWORD.search(old) is not None)
            is_mixed = (CleanRef.MIXED_CASES.search(orig) is not None)
            is_upper = orig.isupper()
            is_lower = orig.islower()
            is_title = orig.istitle()
            possible_actions = [
                (is_upper, CaseType.TITLE, old),
                (is_lower, CaseType.LOWER, old),
                (is_title, CaseType.TITLE, old),
                (is_mixed, CaseType.MIXED, old),
                # (is_mixed_case_oneword, CaseType.MIXED, old),
             ]
            selected_action = [(case_type, old) for (is_condition_true, case_type, old) in possible_actions if is_condition_true]
            has_more_than_one = (len(selected_action) > 1)
            if has_more_than_one:
                selected_action = [selected_action[0]]
            try:
                [new] = list(map(convert_case_op, selected_action))
            except Exception as e:
                new = old

        # is_diff = (old_copy != new)
        # if is_diff:
        #     msg = f'transpose_matching_case(): orig:{orig};old:{old_copy};new:{new}'
        #     print(msg)
        return new

    def isEnTextGoesFirst(self, txt: str):
        has_start_with = self.isInStartWithList(txt)
        is_en_goes_first = bool(has_start_with)
        is_debug = is_en_goes_first
        if is_debug:
            is_debug = True

        # msg = f'isEnTextGoesFirst(): {txt} EN part should go first. ORDER should be: {self.en_txt} => {self.vn_txt}'
        # print(msg)
        return is_en_goes_first

    def dealWithQuotes(self):
        # is_debug = ('root is the same as the tip' in self.m.id)
        # if is_debug:
        #     is_debug = True

        (self.en_txt, en_begin_quote, en_end_quote) = self.removeQuotesSurroundingText(self.en_txt)
        (self.vn_txt, vn_begin_quote, vn_end_quote) = self.removeQuotesSurroundingText(self.vn_txt)
        # self.begin_quote = (en_begin_quote if en_begin_quote else vn_begin_quote)
        # self.end_quote = (en_end_quote if en_end_quote else vn_end_quote)

        # is_containing_symbols = (df.SYMBOLS.search(self.en_txt) is not None)
        # pattern_core_text = (re.escape(self.en_txt) if is_containing_symbols else self.en_txt)
        # ast_quoted_txt = r'([%s]+)(%s)([%s]+)' % (RefType.AST_QUOTE.value, pattern_core_text, RefType.AST_QUOTE.value)
        # ast_quoted_pattern = re.compile(ast_quoted_txt, re.I)
        # matched_dict = pu.patternMatchAll(ast_quoted_pattern, self.m.id)
        # try:
        #     mm: MatcherRecord = None
        #     matched_entry: MatcherRecord = None
        #     [matched_entry] = [mm for (loc, mm) in matched_dict.items() if (ast_quoted_pattern.search(mm.txt) is not None)]
        #     # if not match is found, exception should happens here, the next few lines of code won't have any effect at all
        #     # these lines of codes here is there to show the actual content of the matched_entry. Should be commented out
        #     sub_list = matched_entry.getSubEntriesAsList()
        #     (oloc, otxt) = sub_list[0]
        #     (oloc, self.begin_quote_removable) = sub_list[1]
        #     (oloc, self.orig_en_txt) = sub_list[2]
        #     (oloc, self.end_quote_removable) = sub_list[3]
        #     self.begin_quote = RefType.DBL_QUOTE.value
        #     self.end_quote = RefType.DBL_QUOTE.value
        # except Exception as e:
        #     pass

    def dealWithCases(self):
        def isKeptVnTextAsIs(orig, current):
            is_eng_single_word_and_upper = (len(orig.split()) == 1) and (orig.isupper() or orig.istitle()) and (len(current.split()) > 2)
            can_keep_as_is = (is_eng_single_word_and_upper)
            if can_keep_as_is:
                is_debug = True
            # can_keep_as_is = False
            return can_keep_as_is

        # deb_p = re.compile('root is the same as the tip', re.I)
        # is_debug = (deb_p.search(self.m.id) is not None)
        # if is_debug:
        #     is_debug = True
        is_debug = ('Analemma' in self.en_txt)
        if is_debug:
            is_debug = True

        self.has_orig = bool(self.orig_en_txt)
        self.has_orig_link = bool(self.orig_link_txt)
        if self.has_orig:
            (self.orig_en_txt, orig_en_begin_quote, orig_en_end_quote) = self.removeQuotesSurroundingText(self.orig_en_txt)
            self.en_txt = self.transpose_matching_case(self.orig_en_txt, self.en_txt)
            can_keep_orig = (isKeptVnTextAsIs(self.orig_en_txt, self.vn_txt))
            if not can_keep_orig:
                self.vn_txt = self.transpose_matching_case(self.orig_en_txt, self.vn_txt, prefer_case=CaseType.TITLE, when=(self.orig_en_txt.isupper()))
        else:
            self.orig_en_txt = self.en_txt
            can_keep_orig = (isKeptVnTextAsIs(self.orig_en_txt, self.vn_txt))
            if not can_keep_orig:
                self.vn_txt = self.transpose_matching_case(self.en_txt, self.vn_txt, prefer_case=CaseType.TITLE, when=(self.en_txt.isupper()))

        self.is_link_changed = False
        if self.has_orig_link:
            self.orig_link = str(self.link_txt)
            self.link_txt = self.transpose_matching_case(self.orig_link_txt, self.link_txt)
            self.is_link_changed = (self.orig_link != self.link_txt)

    def setWordsMustNotChangeCase(self, txt: str):
        new_txt = str(txt)
        for word in CleanRef.must_be_upper_case:
            pattern_txt = r'\b%s\b' % (word)
            pattern = re.compile(pattern_txt, re.I)
            (new_txt, count) = pattern.subn(word, new_txt)
        return new_txt

    def workoutTextLocation(self):
        if self.has_link and self.is_link_changed:
            self.new_loc = (self.vnloc[0] - self.oloc[0], self.lkloc[1] - self.oloc[0])
        else:
            self.new_loc = (self.vnloc[0] - self.oloc[0], self.enloc[1] - self.oloc[0])
            test_txt = self.otxt[self.new_loc[0]:self.new_loc[1]]
            # is_debug = True

    def finalizeOutput(self, matcher_record: MatcherRecord):
        is_diff = (bool(self.new_txt) and bool(self.old_txt)) and (self.new_txt != self.old_text)
        if is_diff:
            self.is_changed = True
            is_diff = (self.has_orig_link and self.has_link and self.orig_link_txt.strip() != self.link_txt.strip())
            if is_diff:
                self.link_txt = self.orig_link_txt
                self.new_txt.replace(self.link_txt, self.orig_link_txt)
                msg = f'finalizeOutput:() replaced link: {self.link_txt} => {self.orig_link_txt}'
                print(msg)

            self.new_txt = self.enforceLowerCase(self.orig_en_txt, self.new_txt)
            self.new_txt = self.setWordsMustNotChangeCase(self.new_txt)
            matcher_record.translation = self.new_txt
        return matcher_record

    def solveProblem(self,
                    msg: Message,
                    matcher_record: MatcherRecord,
                    ):
        # # print(f'base solveProblem(): {self.__class__.__name__}')
        # is_debug = ('fade to black' in matcher_record.txt)
        # # deb_p = re.compile('Hypertext Markup Language: Ngôn Ngữ Đánh', re.I)
        # is_debug = (deb_p.search(self.m.id) is not None)
        # if is_debug:
        #     is_debug = True

        if self.isIgnoreEntry(matcher_record):
            return matcher_record

        self.old_text = str(matcher_record.txt)
        self.getTextFunction(matcher_record) # this will expand and fill data in __init__ function
        is_ignore = self.ignoreIfStartWith()
        is_type_kbd = (bool(self.type_txt) and (RefType.getRef(self.type_txt) == RefType.KBD))
        if is_ignore or is_type_kbd:
            return matcher_record

        self.swap_text() # self.vn_txt, self.en_txt swapping content if en = isascii()
        self.find_orig(msg) # (self.orig_en_txt, self.orig_link_txt)
        self.dealWithQuotes()
        self.dealWithCases()
        self.repeatWordsInOrigin() # replace EN word in original en_txt in self.vn_txt, so self.vn_txt contains exact copy of originals

        self.is_translation_outside = False
        self.is_en_first = self.isEnTextGoesFirst(self.en_txt)
        self.workoutTextLocation()
        self.new_txt = self.formatOutput()
        if not self.new_txt:
            return matcher_record
        else:
            return self.finalizeOutput(matcher_record)

    def solve_each_instance(self, problem_entry):
        (m, loc, matcher_record) = problem_entry
        self.matcher_record = matcher_record
        self.m = m
        solved_record = self.solveProblem(m, matcher_record)
        return solved_record

    def ignoreIfStartWith(self):
        try:
            examine_txt = self.vn_txt
            is_ignore = (examine_txt in CleanRef.ignore_start_with)
            return is_ignore
        except Exception as e:
            pass
        return False

    def isContinueIfNoPairingFound(self):
        return True

    def solve_each_message(self, msg: Message):
        def sortedByLocation(mm: MatcherRecord):
            return mm.s

        def pairing(mm_orig: MatcherRecord):
            pair = (None, None)
            try:
                prob_mm: MatcherRecord = None
                prob_entries = pairing.problem_entries
                for (loc, prob_mm) in prob_entries.items():
                    prob_txt = prob_mm.txt
                    orig_txt = mm_orig.txt
                    orig_txt_list = df.CHARACTERS.findall(orig_txt)
                    prob_txt_list = df.CHARACTERS.findall(prob_txt)
                    is_prob_menu_selection = (RefType.MENUSELECTION.value in prob_txt)
                    is_orig_menu_selection = (RefType.MENUSELECTION.value in orig_txt)
                    if is_prob_menu_selection:
                        if not is_orig_menu_selection:
                            return pair

                    boolean_list = [(word in prob_txt) for word in orig_txt_list]
                    is_found = not (False in boolean_list)
                    if is_found:
                        pair = (prob_mm, mm_orig)
                        break
            except Exception as e:
                pass
            return pair

        m: Message = None
        msgstr_pattern = self.getMsgstrPattern()
        msgid_pattern = self.getMsgidPattern()

        is_debug = ('to_space' in msg.id)
        if is_debug:
            is_debug = True

        self.m = msg
        problem_entries = pu.patternMatchAll(msgstr_pattern, msg.string, reversed=True)
        has_problem = bool(problem_entries)
        if not has_problem:
            return [None]
        else:
            orig_match_dict = pu.patternMatchAll(msgid_pattern, msg.id, reversed=True)

            ref_list = [mm for (loc, mm) in problem_entries.items()]
            self.vn_ref_list.extend(ref_list)

            pairing.problem_entries = problem_entries
            self.orig_mm_list = [matcher_record for (loc, matcher_record) in orig_match_dict.items()]
            pair_prob_orig = list(map(pairing, self.orig_mm_list))
            self.pair_prob_orig = [(prob, orig) for (prob, orig) in pair_prob_orig if (bool(prob) and bool(orig))]
            if self.pair_prob_orig:
                print('PAIRING: --- ')
                print(self.pair_prob_orig)
                print('xxxx')
            else:
                is_continue = self.is_continue_if_no_paring_found
                if not is_continue:
                    return []

            problem_entry = [(msg, loc, matcher_record)
                             for (loc, matcher_record) in problem_entries.items()]
            solved_record_list = list(map(self.solve_each_instance, problem_entry))
            self.solved_count += len(solved_record_list)
            reversed_solved_record_list = list(sorted(solved_record_list, key=sortedByLocation, reverse=True))
            result_records = list(map(self.assemble_result, reversed_solved_record_list))
            return result_records

    def assemble_result(self, matcher_record: MatcherRecord, overriding_loc=None):
        msg_record: Message = self.m

        has_translation = not (matcher_record.translation is None)
        if not has_translation:
            return matcher_record

        is_diff = (matcher_record.txt != matcher_record.translation)
        if not is_diff:
            return matcher_record

        self.is_changed = True
        new_txt = matcher_record.translation
        msgstr = msg_record.string
        old_txt = str(msgstr)
        actual_loc = (overriding_loc if bool(overriding_loc) else matcher_record.loc)
        msgstr = cm.jointText(msgstr, new_txt, actual_loc)
        msg_record.string = msgstr

        is_changed = (old_txt != msgstr)
        if is_changed:
            msg = f'\nassemble_result: {self.__class__.__name__}\nen:[{self.m.id}]\n\nold:[{old_txt}]\n\nnew:[{msgstr}]\n\n\n'
            print(msg)
            is_empty = bool(old_txt) and (not bool(msgstr) or len(msgstr) == 0)
            if is_empty:
                raise RuntimeError(msg)

        return matcher_record

    def performTask(self):
        self.result_list = list(map(self.solve_each_message, self.message_list))