import os
import operator as OP
from re import Pattern, Match, compile
from collections import OrderedDict
from pprint import pp
import hashlib
import time
from reftype import RefType
from collections import deque
from fuzzywuzzy import fuzz
from bisect import bisect_left
from matcher import MatcherRecord
from urlextract import URLExtract as URLX
import operator
import re
import copy as CP

DEBUG=True
# DEBUG=False
DIC_LOWER_CASE=True

def dd(*args, **kwargs):
    if DEBUG:
        print(args, kwargs)
        if len(args) == 0:
            print('-' * 80)

KEYBOARD_TRANS_DIC = {
    r'\bWheelUp\b': "Lăn Bánh Xe về Trước (WheelUp)",
    r'\bWheelDown\b': "Lăn Bánh Xe về Sau (WheelDown)",
    r'\bWheel\b': 'Bánh Xe (Wheel)',
    "NumpadPlus": "Dấu Cộng (+) Bàn Số (NumpadPlus)",
    "NumpadMinus": "Dấu Trừ (-) Bàn Số (NumpadMinus)",
    "NumpadSlash": "Dấu Chéo (/) Bàn Số (NumpadSlash)",
    "NumpadDelete": "Dấu Xóa/Del Bàn Số (NumpadDelete)",
    "NumpadPeriod": "Dấu Chấm (.) Bàn Số (NumpadPeriod)",
    "Numpad0": "Số 0 Bàn Số (Numpad0)",
    "Numpad1": "Số 1 Bàn Số (Numpad1)",
    "Numpad2": "Số 2 Bàn Số (Numpad2)",
    "Numpad3": "Số 3 Bàn Số (Numpad3)",
    "Numpad4": "Số 4 Bàn Số (Numpad4)",
    "Numpad5": "Số 5 Bàn Số (Numpad5)",
    "Numpad6": "Số 6 Bàn Số (Numpad6)",
    "Numpad7": "Số 7 Bàn Số (Numpad7)",
    "Numpad8": "Số 8 Bàn Số (Numpad8)",
    "Numpad9": "Số 9 Bàn Số (Numpad9)",
    "Spacebar": "Dấu Cách (Spacebar)",
    r'\bDown\b': "Xuống (Down)",
    r'\bUp\b': "Lên (Up)",
    r'\bComma\b': "Dấu Phẩy (Comma)",
    r'\bMinus\b': "Dấu Trừ (Minus)",
    r'\bPlus\b': "Dấu Cộng (Plus)",
    "Left": "Trái (Left)",
    "=": "Dấu Bằng (=)",
    "Equals": "Dấu Bằng (=)",
    "Right": "Phải (Right)",
    "Backslash": "Dấu Chéo Ngược (Backslash)",
    r'\bSlash\b': "Dấu Chéo (Slash)",
    "AccentGrave": "Dấu Huyền (AccentGrave)",
    "Delete": "Xóa (Delete)",
    "Period": "Dấu Chấm (Period)",
    "Comma": "Dấu Phẩy (Comma)",
    "PageDown": "Trang Xuống (PageDown)",
    "PageUp": "Trang Lên (PageUp)",
    "PgDown": "Trang Xuống (PgDown)",
    "PgUp": "Trang Lên (PgUp)",
    "OSKey": "Phím Hệ Điều Hành (OSKey)",
    "Slash": "Dấu Chéo (Slash)",
    "Minus": "Dấu Trừ (Minus)",
    "Plus": "Dấu Cộng (Plus)",
    "Down": "Xuống (Down)",
    "Up": "Lên (Up)",
    "MMB": "NCG (MMB)",
    "LMB": "NCT (LMB)",
    "RMB": "NCP (RMB)",
    "Pen": "Bút (Pen)"
}

KEYBOARD_TRANS_DIC_PURE = {
    "OSKey": "Phím Hệ Điều Hành (OSKey)",
    "WheelUp": "Lăn Bánh Xe về Trước (WheelUp)",
    "WheelDown": "Lăn Bánh Xe về Sau (WheelDown)",
    "Wheel": "Bánh Xe (Wheel)",
    "NumpadPlus": "Dấu Cộng (+) Bàn Số (NumpadPlus)",
    "NumpadMinus": "Dấu Trừ (-) Bàn Số (NumpadMinus)",
    "NumpadSlash": "Dấu Chéo (/) Bàn Số (NumpadSlash)",
    "NumpadDelete": "Dấu Xóa/Del Bàn Số (NumpadDelete)",
    "NumpadPeriod": "Dấu Chấm (.) Bàn Số (NumpadPeriod)",
    "NumpadAsterisk": "Dấu Sao (*) Bàn Số (NumpadAsterisk)",
    "Numpad0": "Số 0 Bàn Số (Numpad0)",
    "Numpad1": "Số 1 Bàn Số (Numpad1)",
    "Numpad2": "Số 2 Bàn Số (Numpad2)",
    "Numpad3": "Số 3 Bàn Số (Numpad3)",
    "Numpad4": "Số 4 Bàn Số (Numpad4)",
    "Numpad5": "Số 5 Bàn Số (Numpad5)",
    "Numpad6": "Số 6 Bàn Số (Numpad6)",
    "Numpad7": "Số 7 Bàn Số (Numpad7)",
    "Numpad8": "Số 8 Bàn Số (Numpad8)",
    "Numpad9": "Số 9 Bàn Số (Numpad9)",
    "Spacebar": "Dấu Cách (Spacebar)",
    "Down": "Xuống (Down)",
    "Up": "Lên (Up)",
    "Comma": "Dấu Phẩy (Comma)",
    "Minus": "Dấu Trừ (Minus)",
    "Plus": "Dấu Cộng (Plus)",
    "Left": "Trái (Left)",
    "=": "Dấu Bằng (=)",
    "Equals": "Dấu Bằng (=)",
    "Right": "Phải (Right)",
    "Backslash": "Dấu Chéo Ngược (Backslash)",
    "Slash": "Dấu Chéo (Slash)",
    "AccentGrave": "Dấu Huyền (AccentGrave)",
    "Delete": "Xóa (Delete)",
    "Period": "Dấu Chấm (Period)",
    "PageDown": "Trang Xuống (PageDown)",
    "PageUp": "Trang Lên (PageUp)",
    "PgDown": "Trang Xuống (PgDown)",
    "PgUp": "Trang Lên (PgUp)",
    "OSKey": "Phím Hệ Điều Hành (OSKey)",
    "MMB": "NCG (MMB)",
    "LMB": "NCT (LMB)",
    "RMB": "NCP (RMB)",
    "Pen": "Bút (Pen)"
}

numeric_prefix = 'hằng/lần thứ/bộ/bậc'
numeric_postfix = 'mươi/lần/bậc'
numeral_dict = {
    '@{1t}': 'ức',
    '@{1b}': 'tỉ',
    '@{1m}': 'triệu',
    '@{1k}': 'nghìn',
    '@{1h}': 'trăm',
    '@{10}': 'chục/mươi/mười',
    '@{0}': 'không/vô/mươi',
    '@{1}': 'một/nhất/đầu tiên',
    '@{2}': 'hai/nhì/nhị/phó/thứ/giây đồng hồ',
    '@{3}': 'ba/tam',
    '@{4}': 'bốn/tứ/tư',
    '@{5}': 'năm/lăm/nhăm/Ngũ',
    '@{6}': 'Sáu/Lục',
    '@{7}': 'Bảy/Thất',
    '@{8}': 'Số tám/bát',
    '@{9}': 'Chín/cửu',
}

numeric_trans = {
    'a|an': '@{1} con/cái/thằng',
    'zero|none|empty|nullary': '@{0}',
    'one|first|monuple|unary': '@{1}',
    'two|second|couple|binary': '@{2}',
    'three|third|triple|ternary': '@{3}',
    'four(th)?|quadruple|Quaternary': '@{4}',
    'five|fifth|quintuple|Quinary': '@{5}',
    'six(th)?|sextuple|Senary': '@{6}',
    'seven(th)?|septuple|Septenary': '@{7}',
    'eight(th)?|octa|octal|octet|octuple|Octonary': '@{8}',
    'nine(th)?|nonuple|Novenary|nonary': '@{9}',
    'ten(th)?|decimal|decuple|Denary': '@{10}',
    'eleven(th)?|undecuple|hendecuple': 'Mười @{1}',
    'twelve(th)?|doudecuple': 'Mười @{2}',
    'thirteen(th)?|tredecuple': 'Mười @{3}',
    'fourteen(th)?|quattuordecuple': 'Mười @{4}',
    'fifteen(th)?|quindecuple': 'Mười @{5}',
    'sixteen(th)?|sexdecuple': 'Mười @{6}',
    'seventeen(th)?|septendecuple': 'Mười @{7}',
    'eighteen(th)?|octodecuple': 'Mười @{8}',
    'nineteen(th)?|novemdecuple': 'Mười @{9}',
    '(twent(y|ie(s|th))+?)|vigintuple': '@{2} @{10}',
    '(thirt(y|ie(s|th))+?)|trigintuple': '@{3} @{10}',
    '(fort(y|ie(s|th))+?)|quadragintuple': '@{4} @{10}',
    '(fift(y|ie(s|th))+?)|quinquagintuple': '@{5} @{10}',
    '(sixt(y|ie(s|th))+?)|sexagintuple': '@{6} @{10}',
    '(sevent(y|ie(s|th))+?)|septuagintuple': '@{7} @{10}',
    '(eight(y|ie(s|th))+?)|octogintuple': '@{8} @{10}',
    '(ninet(y|ie(s|th))+?)|nongentuple': '@{9} @{10}',
    '(hundred(s|th)?)|centuple': '@{1h}',
    '(thousand(s|th)?)|milluple': '@{1k}',
    'million(s|th)?': '@{1m}',
    'billion(s|th)?': '@{1t}',
    'trillion(s|th)?': '@{1t}',
}

class LocationObserver(OrderedDict):
    def __init__(self, msg, tran_finder=None):
        self.blank = str(msg)

    def markAsUsed(self, s: int, e: int):
        blk = (Common.FILLER_CHAR * (e - s))
        left = self.blank[:s]
        right = self.blank[e:]
        self.blank = left + blk + right

    def markedLocAsUsed(self, loc: tuple):
        ss, ee = loc
        self.markAsUsed(ss, ee)

    def isUsed(self, s: int, e: int):
        part = self.blank[s:e]
        is_dirty = (Common.FILLER_PARTS.search(part) is not None)
        return is_dirty

    def isLocUsed(self, loc: tuple):
        s, e = loc
        return self.isUsed(s, e)

    def isCompletelyUsed(self):
        is_fully_done = (Common.FILLER_CHAR_ALL_PATTERN.search(self.blank) is not None)
        return is_fully_done

    def getUnmarkedPartsAsDict(self):
        untran_dict = Common.findInvert(Common.FILLER_PARTS, self.blank, is_removing_surrounding_none_alphas=True)
        return untran_dict


class Common:
    total_files = 1358
    file_count = 0
    PAGE_SIZE = 20 * 4096
    MAX_FUZZY_LIST = 100
    MAX_FUZZY_TEST_LENGTH = 0.5
    FUZZY_ACCEPTABLE_RATIO = 90
    FUZZY_MODERATE_ACCEPTABLE_RATIO = 85
    FUZZY_LOW_ACCEPTABLE_RATIO = 70
    FUZZY_VERY_LOW_ACCEPTABLE_RATIO = 45
    FUZZY_PERFECT_MATCH_PERCENT = 60

    APOSTROPHE_CHAR = "'"
    MAX_FUZZY_ACCEPTABLE_RATIO = 95
    FUZZY_RATIO_INCREMENT = 5
    AWESOME_COSSIM_FUZZY_ACCEPTABLE_RATIO = 50
    FUZZY_KEY_LENGTH_RATIO = 0.3
    SENT_STRUCT_SYMB = '$$$'
    SENT_STRUCT_PAT = re.compile(r'\s*\${3}\s*')
    TRAN_REF_PATTERN = re.compile(r'\@\{([^{@}]+)?\}')
    PYTHON_FORMAT = re.compile(r'(?:\s|^)(\'?%\w\')(?:\W|$)')

    WEAK_TRANS_MARKER = "#-1#"
    debug_current_file_count = 0
    debug_max_file_count = 5
    debug_file = None

    # debug_file = 'addons/3d_view'
    # debug_file = 'animation/armatures/posing/bone_constraints/introduction' # e.g.
    # debug_file = 'animation/armatures/posing/bone_constraints/inverse_kinematics/introduction' # kbd WheelDown/Up
    # debug_file = "video_editing/sequencer/strips/effects/subtract"
    # debug_file = "video_editing/introduction"
    # debug_file = "about/contribute/index"
    # debug_file="interface/window_system/topbar"
    # debug_file = "advanced/app_templates"
    # debug_file = "modeling/empties"
    # debug_file = "animation/armatures/posing/editing"
    # debug_file = "index"
    # debug_file = "animation/constraints/relationship/shrinkwrap"
    # debug_file = "getting_started/about/community"
    # debug_file = "animation/actions"
    # debug_file = "video_editing/sequencer/strips/transitions/wipe" # :ref:`easings <editors-graph-fcurves-settings-easing>`
    # debug_file = "about/contribute/editing"
    # debug_file = "about/contribute/build/windows"
    # debug_file = "about/contribute/build/macos"
    # debug_file = "about/contribute/guides/maintenance_guide"
    # debug_file = "about/contribute/guides/markup_guide" # debugging :term: :abbr:, ``:kbd:`LMB```, ``*Mirror*``, ``:menuselection:`3D View --> Add --> Mesh --> Monkey```
    # debug_file = "about"
    # debug_file = "about/contribute/install/windows"
    # debug_file = "about/license" # (online) or URL (in print) to manual
    # debug_file = "addons/3d_view/3d_navigation" # debugging :menuselection:
    # debug_file = "addons/add_curve/index"
    # debug_file = "addons/add_curve/ivy_gen"
    # debug_file = "addons/import_export/anim_nuke_chan"
    # debug_file = "addons/node/node_wrangler"
    # debug_file = "addons/object/carver"
    # debug_file = "advanced/command_line/arguments" # trouble some file
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

    leading=r'([\`\<]+)'
    ending=r'([\`\>]+)'
    word = r'([\w\d\#]+)'
    sep = r'([<>\\\/\-\_\.{}:]+)'
    sep_first = r'((%s(%s%s)+)+)' % (sep, word, sep)
    word_first = r'((%s(%s%s)+)+%s?)' % (word, sep, word, sep)
    word_first_with_leading_ending = r'(%s%s%s)' % (leading, word_first, ending)
    pat = r'%s|%s' % (word_first, sep_first)
    path_with_leading_and_ending = r'%s|%s' % (word_first_with_leading_ending, sep_first)
    pat_full = r'^(%s)$' % (pat)

    word = r'([\w\#]+)'
    ignore_words = r'((M[ris]+|Dr|etc|e.g)[\.])'
    url_leading = r'((http|https|file)\:\/\/)'
    URL_LEADING_PATTERN = re.compile(url_leading, re.I)

    path_sep = r'([\~\\\\////\\\/\_\-\.\:\*\?\=\{\}\|]{1,2})'
    leading_hyphens = r'(^[-]+)'
    ref_tag = r'(^:%s:$)' % (word)
    single_hyphen = r'(^%s[-:*_\/]%s$)' % (word, word)
    number_format = r'(\d+[.]\d+)'
    hour_format = r'(%s:%s(:%s)?([.]%s)?)' % (word, word, word, word)
    whatever = r'(%s?)[*]{1}(%s?)' % (word, word)
    file_extension = r'^([.]%s)$' % (word)
    return_linefeed = r'^(\\[nr])$'
    bold_word = r'^(\*%s\*)$' % (word)
    not_allowed = r'(?!(%s|%s|%s|%s|%s|%s|%s|%s))' % (ignore_words, bold_word, leading_hyphens, single_hyphen, ref_tag, hour_format, number_format, return_linefeed)
    path = r'(%s|%s)?((%s(%s)?%s)+)+' % (word, path_sep, path_sep, path_sep, word)
    variable = r'[\w_-]+'
    api_path = r'((%s\.%s)+)+' % (variable, variable)
    blender_api = r'^(blender_api\:%s)$' % (api_path)

    extension_0001 = r'(%s\.%s)' % (word, word)
    extension_0002 = r'(%s\.%s)' % (whatever, word)
    extension_0003 = r'(%s\.%s)' % (word, whatever)
    extension_0004 = r'(%s\.%s)' % (whatever, whatever)

    ending_extension = r'(%s|%s|%s|%s)' \
                       % ( \
                           extension_0001, \
                           extension_0002, \
                           extension_0003, \
                           extension_0004,
                       )
    path_def = r'^(%s|%s)%s?(%s)?$' % (path, url_leading, path_sep, ending_extension)
    # path_def = r'^%s(%s)%s?$' % (not_allowed, path, path_sep)
    path_pattern = r'%s(%s|%s|%s)' % (not_allowed, path_def, file_extension, blender_api)
    PATH_CHECKER = re.compile(path_pattern, flags=re.I)

    # meta_char_list = "[].^$*+?{}()\|"
    METACHAR_PATTERN = re.compile(r'[\[\]\.\^\$\*\+\?\{\}\(\)\\\|]', re.M)
    PREFIX_END = r'[^0-9@#.,]'
    NUMBER_TOKEN = r'[0-9@#.,E+]'

    PREFIX_PATTERN = r"(?P<prefix>(?:'[^']*'|%s)*)" % PREFIX_END
    NUMBER_PATTERN = r"(?P<number>%s*)" % NUMBER_TOKEN
    SUFFIX_PATTERN = r"(?P<suffix>.*)"

    NUMBER_RE = re.compile(r"%s%s%s" % (PREFIX_PATTERN, NUMBER_PATTERN,
                                        SUFFIX_PATTERN))
    WHITESPACE = re.compile('[\n\r\t\v\f]')
    EMAIL_ADDRESS = re.compile(r"^\s*.+@[^\.].*\.[a-z]{2,}$")      # start to end
    DOC_LINK = re.compile(r'^(\/\w+)+$')

    WORD_SEPARATION = re.compile('('
                      r'\s+|'                                 # any whitespace
                      r'[^\s\w]*\w+[a-zA-Z]-(?=\w+[a-zA-Z])|'  # hyphenated words
                      r'(?<=[\w\!\"\'\&\.\,\?])-{2,}(?=\w)'   # em-dash
                      ')')

    REF_PATH = re.compile(r'^\w+([\-\.]\w+){1,}$')
    DOC_PATH = re.compile(r'^(\/\w+)+$')

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

    # var = r'[\w\_\.\-]+'
    # param = r'(%s(\,(\s+)?)?)+' % (var)
    # funct = r'^(%s\((%s)?\))$' % (var, param)
    var = r'[\w\_\.\-]+'
    param = r'(%s(\,(\s+)?)?)+' % (var)
    multiple = r'^\w+\(s\)$'
    ga_multi = r'([\`]+)?'
    funct = r'^%s(%s\((%s)?\))%s$' % (ga_multi, var, param, ga_multi)
    FUNCTION = re.compile(funct)

    email = r'(<)?(\w+@\w+(?:\.\w+)+)(?(1)>|$)'
    sentence_elements = r'([^\.\,\:\!]+)'
    not_follow_by_a_space = r'(?!\s)'
    follow_by_a_space_or_end = r'(?:(\s|$))'
    not_precede_by_a_space = r'(?<![\s\d])'
    # setence_break_pat_txt = r'%s%s%s' % (not_precede_by_a_space, sentence_elements, follow_by_a_space_or_end)
    setence_break_pat_txt = r'%s%s' % (sentence_elements, follow_by_a_space_or_end)
    COMMON_SENTENCE_BREAKS = re.compile(setence_break_pat_txt)

    TRIMMABLE_ENDING = re.compile(r'([\s\.\,\:\!]+)$')
    TRIMMABLE_BEGINNING=re.compile(r'^([\s\.\,]+)')
    TRAILING_WITH_PUNCT = re.compile(r'[\s\.\,\:\!\'\%\$\"\\\)\}\|\]\*\?\>\`\-\+\/\#\&]$')
    HEADING_WITH_PUNCT = re.compile(r'^[\s\.\,\:\!\'\%\$\"\\\(\{\|\[\*\?\>\`\-\+\/\#\&]')

    TRAILING_WITH_PUNCT_MULTI = re.compile(r'[\s\.\,\:\!\'\%\$\"\\\*\?\-\+\/\#\&]+$')
    HEADING_WITH_PUNCT_MULTI = re.compile(r'^[\s\.\,\:\!\'\%\$\"\\\*\?\-\+\/\#\&]+')

    REMOVABLE_SYMB_FULLSET_FRONT = re.compile(r'^[\s\:\!\'$\"\\\(\{\|\[\*\?\;\<\`\-\+\/\#\&]+')
    REMOVABLE_SYMB_FULLSET_BACK = re.compile(r'[\s\:\!\'$\"\\\)\}\|\]\*\?\>\;\`\-\+\/\#\&\,\.]+$')

    RETAIN_FIRST_CHAR = re.compile(r'^[\*\'\"]+')
    RETAIN_LAST_CHAR = re.compile(r'[\*\'\"]+$')

    LEADING_WITH_SYMBOL = re.compile(r'^[\(\[]+')
    TRAILING_WITH_SYMBOL = re.compile(r'[\)\]]+$')

    GA_PATTERN_PARSER = re.compile(r':[\w]+:[\`]+([^\`]+)?[\`]+')
    ABBREV_PATTERN_PARSER = re.compile(r':abbr:[\`]+([^\`]+)[\`]+')
    ABBREV_CONTENT_PARSER = re.compile(r'([^(]+)\s\(([^\)]+)\)')

    punctuals = r'([\\\/\.\,\:\;\!\?\"\*\'\`]+)'
    basic_punctuals = r'([\.\,\`]+)'
    PUNCTUALS = re.compile(punctuals)
    BASIC_PUNCTUALS = re.compile(basic_punctuals)

    begin_punctuals = r'^%s' % (punctuals)
    end_punctuals = r'%s$' % (punctuals)
    single = r'{1}'
    punctual_single = r'(%s%s)' % (punctuals, single)
    end_punctual_single = r'%s$' % (punctual_single)
    begin_punctual_single = r'^%s' % (punctual_single)

    BEGIN_PUNCTUAL_MULTI = re.compile(begin_punctuals)
    BEGIN_PUNCTUAL_SINGLE = re.compile(begin_punctual_single)
    ENDS_PUNCTUAL_MULTI = re.compile(end_punctuals)
    ENDS_PUNCTUAL_SINGLE = re.compile(end_punctual_single)

    WORD_ONLY = re.compile(r'\b([\w\.\/\+\-\_\<\>]+)\b')
    REF_SEP = ' -- '
    NON_WORD_ONLY = re.compile(r'^([\W]+)$')
    NON_WORD = re.compile(r'([\W]+)')
    NON_WORD_ENDING = re.compile(r'([\W]+)$')
    NON_WORD_STARTING = re.compile(r'^([\W]+)')
    TRANSLATABLE_CHARACTERS = re.compile(r'[a-zA-Z]+')

    GA_REF_PART = re.compile(r':[\w]+:')
    # GA_REF = re.compile(r'[\`]*(:[^\:]+:)*[\`]+(?![\s]+)([^\`]+)(?<!([\s\:]))[\`]+[\_]*')
    GA_REF = re.compile(r'[\`]*(:[^\:]+:)*[\`]+([^\`]+)[\`]+[\_]*')
    GA_REF_ONLY = re.compile(r'^[\`]*(:[^\:]+:)*[\`]+(?![\s]+)([^\`]+)(?<!([\s\:]))[\`]+[\_]*$')
    #ARCH_BRAKET = re.compile(r'[\(]+(?![\s\.\,]+)([^\(\)]+)[\)]+(?<!([\s\.\,]))')
    OSL_ATTRIB = re.compile(r'[\`]?(\w+:\w+)[\`]?')
    COLON_CHAR = re.compile(r'\:')
    # this (something ... ) can have other links inside of it as well as others
    # the greedy but more accurate is r'[\(]+(.*)?[\)]+'
    # ARCH_BRAKET_SINGLE_PARTS = re.compile(r'[\)]+([^\(]+)?[\(]+')
    ARCH_BRAKET_SINGLE_FULL = re.compile(r'\b\(([^\)]+)\)\b')
    #ARCH_BRAKET_MULTI = re.compile(r'[\(]+(.*)?[\)]+')
    ARCH_BRAKET_MULTI = re.compile(r'\b\((.*?)\)\b')
    ARCH_BRACKET_SPLIT = re.compile(r'\s*([()])\s*')

    # AST_QUOTE = re.compile(r'[\*]+(?![\s\.\,\`\"]+)([^\*]+)[\*]+(?<!([\s\.\,\`\"]))')
    AST_QUOTE = re.compile(r"(?<!\w)(\*+)([^\*]+)(?:\b)(\*+)")
    # DBL_QUOTE = re.compile(r'[\\\"]+(?![\s\.\,\`]+)([^\\\"]+)[\\\"]+(?<!([\s\.\,]))')
    DBL_QUOTE = re.compile(r'(?<!\\")(")(.*?)(")')
    # SNG_QUOTE = re.compile(r'[\']+([^\']+)[\']+(?!([\w]))')
    SNG_QUOTE = re.compile(r"(?<!\w)(\')([^\']+)(?:\b)(\')")
    DBL_QUOTE_SLASH = re.compile(r'\\[\"]+(?![\s\.\,\`]+)([^\\\"]+)\\[\"]+(?<!([\s\.\,]))')
    WORD_WITHOUT_QUOTE = re.compile(r'^[\'\"\*]*([^\'\"\*]+)[\'\"\*]*$')

    LINK_WITH_URI=re.compile(r'([^\<\>\(\)]+[\w]+)[\s]+[\<\(]+([^\<\>\(\)]+)[\>\)]+[\_]*')
    MENU_PART = re.compile(r'([\s]?[-]{2}[\>]?[\s]+)(?![\s\-])([^\<\>]+)(?<!([\s\-]))') # working but with no empty entries
    MENU_PART_1 = re.compile(r'(?!\s)([^\->])+(?<!\s)')
    MENU_SEP = re.compile(r'\s?([\-]+\>)\s?')

    ABBREV_TEXT_REVERSE = re.compile(r'(?!\s)([^\(\)]+)(?<!\s)')
    REF_TEXT_REVERSE = re.compile(r'([^\`]+)\s\-\-\s([^\<]+)(?<![\s])')
    REF_PART = re.compile(r'([<(][^<>()]+[>)])')
    END_WITH_REF = re.compile(r'([<][^<>]+[>])$')
    HYPHEN_REF_LINK = re.compile(r'^(\w+)(\-\w+){2,}$')
    LINK_ALL = re.compile(r'^([/][\w_]+)+$')
    MENU_TEXT_REVERSE = re.compile(r'(?!\s)([^\(\)\-\>]+)(?<!\s)')

    path_sep = r'[\\\/\-\_\.]'
    PATH_SEP = re.compile(path_sep)
    NON_PATH_SEP = re.compile(r'^[^\\\/\-\_\.]+$')

    WORD_ONLY_FIND = re.compile(r'\b[\w\-\_\']+\b')
    NON_WORD_FIND = re.compile(r'\W+')
    WORD_START_REMAIN = re.compile(r'^\w+')
    WORD_END_REMAIN = re.compile(r'\w+$')

    ENDS_WITH_EXTENSION = re.compile(r'\.([\w]{2,5})$')
    MENU_KEYBOARD = re.compile(r':(kbd|menuselection):')
    MENU_TYPE = re.compile(r'^([\`]*:menuselection:[\`]+([^\`]+)[\`]+)$')
    MENU_EX_PART = re.compile(r'(\s?[\-]{2}\>\s?)')

    KEYBOARD_TYPE = re.compile(r'^([\`]*:kbd:[\`]+([^\`]+)[\`]+)$')
    KEYBOARD_SEP = re.compile(r'[^\-]+')
    SPECIAL_TERM = re.compile(r'^[\`\*\"\'\(]+(.*)[\`\*\"\'\)]+$')
    ALPHA_NUMERICAL = re.compile(r'[\w]+')
    EXCLUDE_GA= re.compile(r'^[\`\'\"\*\(]+?([^\`\'\"\*\(\)]+)[\`\'\"\*\)]+?$')
    OPTION_FLAG=re.compile(r'^[\-]{2}([^\`]+)')
    FILLER_CHAR='¶'
    filler_char_pattern_str = r'[%s]+' % FILLER_CHAR
    FILLER_CHAR_PATTERN = re.compile(filler_char_pattern_str)

    filler_char_and_space_pattern_str = r'[%s\s]+' % (FILLER_CHAR)
    FILLER_CHAR_INVERT = re.compile(filler_char_and_space_pattern_str)

    filler_parts = r'\s?([%s]+)\s?' % (FILLER_CHAR)
    FILLER_PARTS = re.compile(filler_parts)

    filler_char_and_space_pattern_str = r'^[\s%s]+$' % FILLER_CHAR
    FILLER_CHAR_AND_SPACE_ONLY_PATTERN = re.compile(filler_char_and_space_pattern_str)

    filler_char_all_pattern_str = r'^[%s\s]+$' % FILLER_CHAR
    FILLER_CHAR_ALL_PATTERN = re.compile(filler_char_all_pattern_str)

    NEGATE_FILLER = r"[^\\" + FILLER_CHAR + r"]+"
    NEGATE_FIND_WORD=re.compile(NEGATE_FILLER)
    ABBR_TEXT = re.compile(r'\(([^\)]+)\)')
    ABBR_TEXT_ALL = re.compile(r'([^\(]+[\w])\s\(([^\)]+)\)')
    REF_WITH_LINK = re.compile(r'([^\<\>\(\)]+)\s+?([\<\(]([^\<\>\(\)]+)[\)\>])?')
    REF_WITH_HTML_LINK = re.compile(r'([^\<\>]+)\s+?(\<([^\<\>]+)\>)?')

    IS_A_PURE_LINK = re.compile(r'^(?P<sep>[\/\-\\\.])?[^.*(?P=sep)]+(.*(?P=sep).*[^(?P=sep)]+){2,}$')

    REF_LINK = re.compile(r'[\s]?[\<]([^\<\>]+)[\>][\s]?')
    TERM_LINK = re.compile(r'([^\`]+)\<?[^\`]+\>?')
    PURE_PATH = re.compile(r'^(([\/\\][\w]+)([\/\\][\w]+)*)+[\/\\]?$')
    PURE_REF = re.compile(r'^([\w]+([\-][\w]+)+)+$')
    API_REF = re.compile(r'^blender_api:.*$')

    SPACE_WORD_SEP = re.compile(r'[\S]+')
    ACCEPTABLE_WORD = re.compile(r'[\w\-]+([\'](t|ve|re|m|s))?')

    QUOTED_MSG_PATTERN = re.compile(r'((?<![\\])[\'"])((?:.)*.?)')

    BLENDER_DOCS= os.path.join(os.environ['HOME'], 'blender_docs')

    # WORD_SEP = re.compile(r'[\s\;\:\.\,\/\!\-\dd\<\>\(\)\`\*\"\|\']')
    CHARACTERS = re.compile(r'\w+')
    WORD_SEP = re.compile(r'[^\W]+')
    SYMBOLS_ONLY = re.compile(r'^[\W\s]+$')
    SYMBOLS = re.compile(r'[\W]+')
    SPACES = re.compile(r'\s+')
    START_SPACES = re.compile(r'^\s+')
    END_SPACES = re.compile(r'\s+$')

    NOT_SYMBOLS = re.compile(r'[\w]+')
    SPACE_SEP_WORD = re.compile(r'[^\s]+')
    THE_WORD = re.compile(r'\bthe\b[\s]?', re.I)
    MULTI_SPACES = re.compile(r'[\s]{2,}')
    HYPHEN = re.compile(r'[\-]')
    SPACE_SEP = re.compile(r'\s')

    START_WORD = '^'
    END_WORD = '$'
    BOTH_START_AND_END = '^$'

    START_WORD_SYMBOLS = re.compile(r'^\W+')
    END_WORD_SYMBOLS = re.compile(r'\W+$')

    EN_DUP_ENDING = re.compile(r'[aeiou]\w{1}$')

    FILE_EXTENSION = re.compile(r'^[\.//]\w{2,}$')
    FILE_NAME_WITH_EXTENSION = re.compile(r'(?:[^\+\-\=\s])[\w\-\_\*]+\.\w+$')
    WORD_SPLITTER = None
    # nlp = spacy.load('en_core_web_sm')

    REF_TYPE_NAME_TO_REGISTER_STARTER_PAT = re.compile(r'(_QUOTE|_BRACKET)')

    verb_with_ending_y = [
        'aby', 'bay', 'buy', 'cry', 'dry', 'fly', 'fry', 'guy', 'hay',
        'joy', 'key', 'lay', 'pay', 'ply', 'pry', 'ray', 'say', 'shy',
        'sky', 'spy', 'toy', 'try', 'ally', 'baby', 'body', 'bray', 'buoy',
        'bury', 'busy', 'cloy', 'copy', 'defy', 'deny', 'eddy', 'envy',
        'espy', 'flay', 'fray', 'gray', 'grey', 'levy', 'obey', 'okay',
        'pity', 'play', 'pray', 'prey', 'rely', 'scry', 'slay',
        'spay', 'stay', 'sway', 'tidy', 'vary', 'allay', 'alloy', 'annoy',
        'apply', 'array', 'assay', 'bandy', 'belay', 'belly', 'berry',
        'bogey', 'bully', 'caddy', 'candy', 'carry', 'chevy', 'chivy',
        'colly', 'curry', 'dally', 'decay', 'decoy', 'decry', 'deify', 'delay',
        'dirty', 'dizzy', 'dummy', 'edify', 'empty', 'enjoy', 'ensky', 'epoxy',
        'essay', 'fancy', 'ferry', 'foray', 'glory', 'harry', 'honey', 'hurry',
        'imply', 'inlay', 'jelly', 'jimmy', 'jolly', 'lobby', 'marry', 'mosey',
        'muddy', 'palsy', 'parry', 'party', 'putty', 'query', 'rally', 'ready',
        'reify', 'relay', 'repay', 'reply', 'retry', 'savvy', 'splay', 'spray',
        'stray', 'study', 'stymy', 'sully', 'tally', 'tarry', 'toady', 'unify',
        'unsay', 'weary', 'worry', 'aerify', 'argufy', 'basify', 'benday',
        'betray', 'bewray', 'bloody', 'canopy', 'chivvy', 'citify', 'codify',
        'comply', 'convey', 'convoy', 'curtsy', 'defray', 'deploy', 'descry',
        'dismay', 'embody', 'employ', 'flurry', 'gasify', 'jockey', 'minify',
        'mislay', 'modify', 'monkey', 'motley', 'mutiny', 'nazify', 'notify',
        'occupy', 'ossify', 'outcry', 'pacify', 'parlay', 'parley', 'parody',
        'prepay', 'purify', 'purvey', 'quarry', 'ramify', 'rarefy', 'rarify',
        'ratify', 'rebury', 'recopy', 'remedy', 'replay', 'sashay', 'scurry',
        'shimmy', 'shinny', 'steady', 'supply', 'survey', 'tumefy', 'typify',
        'uglify', 'verify', 'vilify', 'vinify', 'vivify', 'volley', 'waylay',
        'whinny', 'acetify', 'acidify', 'amnesty', 'amplify', 'atrophy', 'autopsy',
        'beatify', 'blarney', 'calcify', 'carnify', 'certify', 'clarify', 'company',
        'crucify', 'curtsey', 'dandify', 'destroy', 'dignify', 'disobey', 'display',
        'dulcify', 'falsify', 'fancify', 'fantasy', 'fortify', 'gainsay', 'glorify',
        'gratify', 'holiday', 'horrify', 'jellify', 'jollify', 'journey', 'justify',
        'lignify', 'liquefy', 'liquify', 'magnify', 'metrify', 'misally', 'misplay',
        'mollify', 'mortify', 'mummify', 'mystify', 'nigrify', 'nitrify', 'nullify',
        'opacify', 'outplay', 'outstay', 'overfly', 'overjoy', 'overlay', 'overpay',
        'petrify', 'pillory', 'portray', 'putrefy', 'qualify', 'rectify', 'remarry',
        'reunify', 'satisfy', 'scarify', 'signify', 'specify', 'stupefy', 'terrify',
        'testify', 'tourney', 'verbify', 'versify', 'vitrify', 'alkalify', 'ammonify',
        'beautify', 'bioassay', 'causeway', 'classify', 'corduroy', 'denazify', 'detoxify',
        'disarray', 'downplay', 'emulsify', 'esterify', 'etherify', 'fructify', 'gentrify',
        'humidify', 'identify', 'lapidify', 'misapply', 'miscarry', 'multiply', 'overplay',
        'overstay', 'prettify', 'prophesy', 'quantify', 'redeploy', 'revivify', 'rigidify',
        'sanctify', 'saponify', 'simplify', 'solidify', 'stratify', 'stultify', 'travesty',
        'underlay', 'underpay', 'accompany', 'butterfly', 'decalcify', 'decertify', 'demulsify',
        'demystify', 'denitrify', 'devitrify', 'disembody', 'diversify', 'electrify', 'exemplify',
        'frenchify', 'indemnify', 'intensify', 'inventory', 'microcopy', 'objectify', 'overweary',
        'personify', 'photocopy', 'preachify', 'preoccupy', 'speechify', 'syllabify', 'underplay',
        'blackberry', 'complexify', 'declassify', 'dehumidify', 'dillydally', 'disqualify',
        'dissatisfy', 'intermarry', 'oversupply', 'reclassify', 'saccharify', 'understudy',
        'hypertrophy', 'misidentify', 'oversimplify', 'transmogrify', 'interstratify',
    ]

    verb_with_ending_s = [
        'Bus', 'Gas', 'Bias', 'Boss', 'Buss', 'Cuss', 'Diss', 'Doss', 'Fuss', 'Hiss',
        'Kiss', 'Mass', 'Mess', 'Miss', 'Muss', 'Pass', 'Sass', 'Suds', 'Toss', 'Amass',
        'Bless', 'Class', 'Cross', 'Degas', 'Dress', 'Floss', 'Focus', 'Glass', 'Gloss',
        'Grass', 'Gross', 'Guess', 'Press', 'Truss', 'Access', 'Assess', 'Bypass', 'Callus',
        'Canvas', 'Caress', 'Caucus', 'Census', 'Chorus', 'Egress', 'Emboss', 'Harass',
        'Obsess', 'Precis', 'Recess', 'Rumpus', 'Schuss', 'Stress', 'Address', 'Aggress',
        'Callous', 'Canvass', 'Compass', 'Concuss', 'Confess', 'Degauss', 'Depress', 'Digress',
        'Discuss', 'Dismiss', 'Engross', 'Express', 'Harness', 'Impress', 'Nonplus', 'Oppress',
        'Percuss', 'Possess', 'Precess', 'Premiss', 'Process', 'Profess', 'Redress', 'Refocus',
        'Regress', 'Repress', 'Succuss', 'Summons', 'Surpass', 'Teargas', 'Trellis', 'Uncross',
        'Undress', 'Witness', 'Bollocks', 'Buttress', 'Compress', 'Distress', 'Outclass', 'Outguess',
        'Progress', 'Reassess', 'Suppress', 'Trespass', 'Waitress', 'Backcross', 'Embarrass',
        'Encompass', 'Overdress', 'Repossess', 'Reprocess', 'Unharness', 'Verdigris', 'Crisscross',
        'Decompress', 'Dispossess', 'Eyewitness', 'Misaddress', 'Overstress', 'Prepossess', 'Rendezvous',
        'Retrogress', 'Transgress', 'Disembarrass',
    ]

    common_prefixes = [
        'a', 'an', 'co', 'de', 'en', 'ex', 'il', 'im', 'in', 'ir', 'in',
        'un', 'up', 'com', 'con', 'dis', 'non', 'pre', 'pro', 'sub', 'sym',
        'syn', 'tri', 'uni', 'ante', 'anti', 'auto', 'homo', 'mono', 'omni',
        'post', 'tele', 'extra', 'homeo', 'hyper', 'inter', 'intra', 'intro',
        'macro', 'micro', 'trans', 'circum', 'contra', 'contro', 'hetero',
    ]
    
    common_prefix_trans = {
        'auto': (START_WORD, 'tự động'),
        'pre': (START_WORD, 'tiền/trước'),
    }

    noun_001 = 'sự/chỗ/phần/vùng/bản/cái/mức/độ/tính/sự/phép'
    noun_002 = 'mọi/nhiều/những/các/phần/bản/sự/chỗ'
    noun_003 = 'chủ nghĩa/tính/trường phái'
    noun_0004 = 'mọi/những chỗ/cái/các/nhiều/một số/vài vật/bộ/trình/người/viên/nhà/máy/phần/bản/cái/con/trình/bộ/người/viên/vật'
    adj_0001 = 'trong/thuộc/có tính/sự/chỗ/phần/trạng thái'
    adj_0002 = 'trong/là/nói một cách/có tính/theo'
    adv_0001 = 'đáng/có khả năng/thể'
    past_0001 = 'đã/bị/được'

    common_sufix_trans = {
        's': (START_WORD, noun_0004),
        'ed': (START_WORD, past_0001),
        'es': (START_WORD, noun_0004),
        'er': (END_WORD, 'hơn/trình/bộ/người/viên/nhà'),
        'ic': (START_WORD, 'giống/liên quan đến/hoạt động trong'),
        'or': (START_WORD, noun_0004),
        'al': (START_WORD, adj_0001),
        'inal': (START_WORD, adj_0001),
        'ly': (START_WORD, adj_0002),
        'ty': (START_WORD, adj_0001),
        '(s)': (START_WORD, 'những/các'),
        'ers': (START_WORD, noun_0004),
        'ies': (START_WORD, noun_0004),
        'ier': (END_WORD, 'hơn'),
        '\'s': (START_WORD, 'của'),
        'ors': (START_WORD, noun_0004),
        'est': (END_WORD, 'nhất'),
        'dom': (START_WORD, noun_001),
        'ful': (START_WORD, 'có/rất/nhiều'),
        'nce': (START_WORD, noun_001),
        'ily': (START_WORD, adj_0002),
        'ity': (START_WORD, noun_001),
        'ive': (START_WORD, adj_0001),
        'ish': (START_WORD, 'hơi hơi/có xu hướng/gần giống'),
        'ism': (START_WORD, noun_003),
        'isms': (START_WORD, noun_003),
        'als': (START_WORD, noun_0004),
        'ure': (START_WORD, noun_001),
        '\'ll': (START_WORD, 'sẽ'),
        'able': (START_WORD, adv_0001),
        'ably': (START_WORD, adv_0001),
        'ence': (START_WORD, noun_001),
        'doms': (START_WORD, noun_001),
        'ible': (START_WORD, adv_0001),
        'ibly': (START_WORD, adv_0001),
        'iest': (END_WORD, 'nhất'),
        'sion': (START_WORD, noun_001),
        'tion': (START_WORD, noun_001),
        'ness': (START_WORD, noun_001),
        'ency': (START_WORD, noun_001),
        'ment': (START_WORD, noun_001),
        'less': (START_WORD, 'vô/không/phi'),
        'like': (START_WORD, 'Thích/Giống Như/Tương Tự'),
        'than': (END_WORD, 'hơn'),
        'ures': (START_WORD, noun_001),
        'lable': (START_WORD, adv_0001),
        'ities': (START_WORD, noun_002),
        'iness': (START_WORD, noun_001),
        'ation': (START_WORD, noun_001),
        'ively': (START_WORD, adj_0002),
        'ments': (START_WORD, noun_001),
        'ption': (START_WORD, noun_001),
        'ations': (START_WORD, noun_002),
        'encies': (START_WORD, noun_002),
        'ization': (START_WORD, noun_001),
        'isation': (START_WORD, noun_001),
        'izations': (START_WORD, noun_002),
        'isations': (START_WORD, noun_002),
    }

    common_suffixes_replace_dict = {
        'a': list(sorted(
            [
                'ic',
             ],
            key=lambda x: len(x), reverse=True)),
        'e': list(sorted(
            ['able', 'ation', 'ations', 'ion', 'ions',
             'ity', 'ities', 'ing', 'ings', 'ously', 'ous', 'ive', 'ily',
             'ively', 'or', 'ors', 'iness', 'ature',
             'atures', 'ition', 'itions', 'itiveness',
             'itivenesses', 'itively', 'ative', 'atives',
             'ant', 'ants', 'ator', 'ators', 'ure', 'ures',
             'al', 'ally', 'als', 'iast', 'iasts', 'iastic', 'ial', 'y',
             'ary', 'ingly', 'ian', 'inal', 'ten'
             ],
            key=lambda x: len(x), reverse=True)),
        't': list(sorted(
            ['ce','cy', 'ssion', 'ssions'],
            key=lambda x: len(x), reverse=True)),
        'x': list(sorted(
            ['ce','ces', ],
            key=lambda x: len(x), reverse=True)),
        'y':list(sorted(
            ['ies', 'ied', 'ier', 'iers', 'iest', 'ily', 'ic', 'ical', 'ically', 'iness', 'inesses',
             'ication', 'ications',
             ],
            key=lambda x: len(x), reverse=True)),
        'ion':['ively'],
        'be':list(sorted(
            ['ption', 'ptions',],
            key=lambda x: len(x), reverse=True)),
        'de':list(sorted(
            ['sible', 'sion', 'sions', 'sive' ],
            key=lambda x: len(x), reverse=True)),
        'ce':list(sorted(
            ['tific', 'tist', 'tists'],
            key=lambda x: len(x), reverse=True)), # science, scientific, scientist, scientists
        'ate':['ant'],
        'cy':['t'],
        'ze':['s'],
        'te':list(sorted(
            ['cy', 'ry'],
            key=lambda x: len(x), reverse=True)),
        'le':['ility'],
        'le':list(sorted(
            ['ility', 'ilities', ],
            key=lambda x: len(x), reverse=True)),
       'ic':list(sorted(
           ['ism', 'isms', ],
           key=lambda x: len(x), reverse=True)),
    }

    common_allowed_appostrophes = {
        "'": ['ll', 've', ', ', 's', 'd', ' ', '.'] # keep this sorted in length
    }

    common_suffixes = [
        'd', 'r', 'y', 's', 't', 'al', 'an', 'ce', 'cy', 'de', 'er', 'es', 'or', 'th', 'ic', 'ly',
        'ed', 'en', 'er', 'ic', 'ly', 'ry', 'st', 'ty', 'ze', 'ze', '\'s', '\'t', '\'m', 'als', 'ate',
        'age', 'aging', 'ages', 'ated', 'ates', 'ces', 'dom', 'ors', 'ers', 'est', 'eer', 'ial', 'ked',
        'ian', 'ism', 'ied', 'ier', 'iers', 'ion', 'ity', 'ics', 'ies', 'like', 'ful', 'less', 'ant',
        'ent', 'ary', 'ful', 'nce', 'ous', 'ive', 'ism', 'isms', 'ing', 'inal', 'ily', 'ity', 'ize',
        'ise', 'ish', 'ite', 'ful', 'ten', 'ual', 'ure', 'ous', '(s)', '\'re', '\'ve', '\'ll', 'n\'t',
        'ally', 'ator', 'ants', 'ance', 'doms', 'ence', 'ency', 'ents', 'ings', 'ures', 'ions', 'sion',
        'sions', 'sive', 'iest', 'iast', 'iasts', 'iastic', 'lier', 'less', 'liest', 'ment', 'ness',
        'ning', 'sion', 'ship', 'able', 'ably', 'ible', 'ical', 'ally', 'ious', 'less', 'ally', 'ward',
        'wise', 'ency', 'ators', 'sible', 'ively', 'ility', 'ually', 'ingly', 'ption', 'ation', 'iness',
        'ities', 'ition', 'itive', 'ments', 'sions', 'ssion', 'ships', 'aries', 'ature', 'ingly', 'izing',
        'ising', 'iness', 'ional', 'lable', 'ously', 'ptions', 'ility', 'ilities', 'itives', 'itions',
        'ication', 'ications', 'atures', 'ations', 'aceous', 'nesses', 'iously', 'ically', 'encies',
        'ssions', 'itively', 'ization', 'isation', 'itiveness', 'itivenesses', 'perception', 'perceive',
        'tific', 'tist', 'tists'
    ]

    common_infix = [
        '-',
    ]

    common_conjuctions = {
        'a minute later': '',
        'accordingly': '',
        'actually': '',
        'after': '',
        'after a while': '',
        'after a short time': '',
        'afterward': '',
        'also': '',
        'and': '',
        'another': '',
        'as an example': '',
        'as a result': '',
        'as soon as': '',
        'at last': '',
        'at length': '',
        'because': '',
        'because of this': '',
        'before': '',
        'besides': '',
        'briefly': '',
        'but': '',
        'consequently': '',
        'conversely': '',
        'equally': '',
        'finally': '',
        'first': '',
        'first of all': '',
        'first and last': '',
        'first time': '',
        'at first': '',
        'firstly': '',
        'for example': '',
        'for instance': '',
        'for this purpose': '',
        'for this reason': '',
        'fourth': '',
        'from here on': '',
        'further': '',
        'furthermore': '',
        'gradually': '',
        'hence': '',
        'however': '',
        'how are you': '',
        'in addition': '',
        'in conclusion': '',
        'in contrast': '',
        'in fact': '',
        'in short': '',
        'in spite of': '',
        'in spite of this': '',
        'despite of': '',
        'despite of this': '',
        'in summary': '',
        'in the end': '',
        'whereas': '',
        'whomever': '',
        'whoever': '',
        'in the meanwhile': '',
        'in the meantime': '',
        'in the same manner': '',
        'in the sameway': '',
        'just as important': '',
        'of equal importance': '',
        'on the contrary': '',
        'on the following day': '',
        'on the other hand': '',
        'other hands': '',
        'otherwise': '',
        'on purpose': '',
        'on the head': '',
        'hit the nail on the head': '',
        'least': '',
        'the least I can': '',
        'in the least': '',
        'last': '',
        'the last of': '',
        'last of all': '',
        'lastly': '',
        'later': '',
        'later on': '',
        'meanwhile': '',
        'moreover': '',
        'nevertheless': '',
        'next': '',
        'next to': '',
        'nonetheless': '',
        'now': '',
        'nor': '',
        'neither': '',
        'or': '',
        'when': '',
        'while': '',
        'presently': '',
        'second': '',
        'similarly': '',
        'since': '',
        'since then': '',
        'so': '',
        'so much': '',
        'so many': '',
        'soon': '',
        'so soon': '',
        'very soon': '',
        'as soon as possible': '',
        'as much as possible': '',
        'as many as possible': '',
        'as long as possible': '',
        'still': '',
        'subsequently': '',
        'such as': '',
        'such that': '',
        'as such': '',
        'the next week': '',
        'then': '',
        'thereafter': '',
        'there and then': '',
        'therefore': '',
        'and thus': '',
        'thus': '',
        'to be specific': '',
        'to begin with': '',
        'to be precise': '',
        'to be exact': '',
        'to illustrate': '',
        'to repeat': '',
        'to sum up': '',
        'too': '',
        'ultimately': '',
        'what': '',
        'with this in mind': '',
        'with that in mind': '',
        'yet': '',
        'not yet': '',
        'and yet': '',
        'although': '',
        'as if': '',
        'although': '',
        'as though': '',
        'even': '',
        'even if': '',
        'even though': '',
        'if': '',
        'if only if': '',
        'if only': '',
        'if when': '',
        'if then': '',
        'if you can': '',
        'if I can': '',
        'if it is possible': '',
        'inasmuch': '',
        'in order that': '',
        'just as': '',
        'lest': 'hầu cho không/e ngại/rằng',
        'now and then': '',
        'for now': '',
        'for now that is': '',
        'so for now': '',
        'but for now': '',
        'now since': '',
        'now that': '',
        'now that\'s what I call': '',
        # '': '',
        # '': '',
        # '': '',
        # '': '',
        # '': '',
        # '': '',
        # '': '',
        # '': '',
        # '': '',
        # '': '',
        # '': '',
        # '': '',
        # '': '',
        # '': '',
        # '': '',
        # '': '',
        # '': '',
        # '': '',
        # '': '',
        # '': '',
        # '': '',
        # '': '',

    }
    common_sufix_translation = list(sorted( list(common_sufix_trans.items()), key=lambda x: len(x[0]), reverse=True))
    common_prefix_translation = list(sorted( list(common_prefix_trans.items()), key=lambda x: len(x[0]), reverse=True))

    ascending_sorted = list(sorted(common_prefixes))
    common_prefix_sorted = list(sorted(ascending_sorted, key=lambda x: len(x), reverse=False))

    ascending_sorted = list(sorted(common_suffixes))
    common_suffix_sorted = list(sorted(ascending_sorted, key=lambda x: len(x), reverse=False))

    ascending_sorted = list(sorted(common_infix))
    common_infix_sorted = list(sorted(ascending_sorted, key=lambda x: len(x), reverse=False))

    numberal = r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|((thir|four|fif|six|seven|eigh|nine)teen)|((twen|thir|four|fif|six|seven|eigh|nine)ty)|(hundred|thousand|(mil|tril)lion))[s]?\b"
    urlx_engine = URLX()

    def isPath(txt: str) -> bool:
        def insertTextOutsideEntry():
            is_valid = (ee > ss)
            if not is_valid:
                return False

            text_outside_url = txt[ss:ee]
            ex_loc = (ss, ee)
            entry = {ex_loc: text_outside_url}
            text_outside_url_list.update(entry)
            return True

        if not txt:
            return False

        is_path = (Common.PATH_CHECKER.search(txt) is not None)
        if is_path:
            return True

        urls = Common.urlx_engine.find_urls(txt, get_indices=True)
        if not urls:
            return False

        # 1. Find the list of urls and put into dictionary so locations can be extracted, uing keys
        url_loc_list = {}
        for url, loc in urls:
            url_length = len(url)
            entry = {loc: url}
            url_loc_list.update(entry)


        # 2. find all the text outside the links and see if they are just spaces and symbols only, which can be classified as
        # IGNORABLE
        text_outside_url_list = {}
        ss = 0
        for loc in url_loc_list.keys():
            s, e = loc
            ee = s
            insertTextOutsideEntry()
            ss = e
        url = url_loc_list[loc]
        ee = len(url)
        insertTextOutsideEntry()

        # 3. Find out if text outside are but all symbols (non-alpha), which means they are discardable (non-translatable)
        is_ignorable = True
        for loc, text_outside in text_outside_url_list.items():
            is_all_symbols = Common.SYMBOLS_ONLY.search(text_outside)
            if not is_all_symbols:
                is_ignorable = False

        return is_ignorable

    def isLinkPath(txt: str) -> bool:
        # is_file_extension = Common.FILE_EXTENSION.search(txt)
        # is_file_name = Common.FILE_NAME_WITH_EXTENSION.search(txt)
        is_path = Common.isPath(txt)
        if is_path:
            return True

        left, mid, right = Common.getTextWithin(txt)
        is_path = Common.isPath(mid)
        return is_path
        # is_path_link = (is_file_extension or is_file_name or is_path)
        # return is_path_link

    def shouldHaveDuplicatedEnding(cutoff_part, txt):
        is_verb_cutoff = (cutoff_part in ['ed', 'ing', 'es'])
        if not is_verb_cutoff:
            return False

        is_dup = (Common.EN_DUP_ENDING.search(txt) is not None)
        return is_dup

    def replaceArchedQuote(txt):
        new_txt = str(txt)
        new_txt = re.sub('\)', ']', new_txt)
        new_txt = re.sub('\(', '[', new_txt)
        # new_txt = new_txt.replace('"', '\\\"')
        return new_txt

    def hasOriginal(msg, tran):
        orig_list = Common.ALPHA_NUMERICAL.findall(msg)
        orig_set = "".join(orig_list)

        tran_list = Common.ALPHA_NUMERICAL.findall(tran)
        tran_set = "".join(tran_list)

        has_orig = (orig_set in tran_set)
        #print("orig_set:", orig_set)
        #print("tran_set:", tran_set)
        #print("has_orig:", has_orig)
        return has_orig

    def isSpecialTerm(msg: str):
        is_special = (Common.SPECIAL_TERM.search(msg) is not None)
        return is_special

    def matchCase(from_str : str , to_str : str):
        WORD_SHOULD_BE_LOWER = [
            'trong',
            'các',
            'những',
            'và',
            'thì'
            'là',
            'hoặc',
            'mà',
            'có',
            'của',
            'với',
            'đến',
            'tới',
        ]
        def lowercase(loc_text_dict, new_str):
            mm: MatcherRecord = None
            for loc, mm in ga_ref_dic.items():
                (s, e), text = mm.getOriginAsTuple()
                lcase_text = text.lower()
                left_part = new_str[:s]
                right_part = new_str[e:]
                new_str = left_part + lcase_text + right_part
            return new_str

        valid = (from_str and to_str)
        if not valid:
            return to_str

        new_str = str(to_str)

        first_char = from_str[0]
        remain_part = from_str[1:]

        from_str_has_multi_words = (Common.SYMBOLS.search(from_str) is not None)
        to_str_has_multi_words = (Common.SYMBOLS.search(to_str) is not None)

        from_string_is_to_first_upper = (first_char.isupper() and remain_part.islower())
        to_string_is_to_first_upper = not (from_str_has_multi_words or to_str_has_multi_words)

        is_first_upper = (first_char.isupper() and remain_part.islower())
        if is_first_upper:
            first_char = new_str[0].upper()
            remain_part = new_str[1:].lower()
            new_str = first_char + remain_part
        else:
            is_lower = (from_str.islower())
            if is_lower:
                new_str = new_str.lower()
                return new_str
            else:
                is_title = (from_str.istitle())
                if is_title:
                    new_str = new_str.title()
                else:
                    is_upper = (from_str.isupper())
                    if is_upper:
                        new_str = new_str.upper()

        # ensure ref keywords ':doc:' is always lowercase
        ga_ref_dic = Common.patternMatchAll(Common.GA_REF_PART, new_str)
        new_str = lowercase(ga_ref_dic, new_str)
        for lcase_word in WORD_SHOULD_BE_LOWER:
            p = re.compile(r'\b%s\b' % lcase_word)
            p_list = Common.patternMatchAll(p, new_str)
            new_str = lowercase(p_list, new_str)

        return new_str

    def beginAndEndPunctuation(msg, is_single=False):
        if is_single:
            begin_with_punctuations = (Common.BEGIN_PUNCTUAL_SINGLE.search(msg) is not None)
            ending_with_punctuations = (Common.ENDS_PUNCTUAL_SINGLE.search(msg) is not None)
            if begin_with_punctuations:
                msg = Common.BEGIN_PUNCTUAL_SINGLE.sub("", msg)
            if ending_with_punctuations:
                msg = Common.ENDS_PUNCTUAL_SINGLE.sub("", msg)
        else:
            begin_with_punctuations = (Common.BEGIN_PUNCTUAL_MULTI.search(msg) is not None)
            ending_with_punctuations = (Common.ENDS_PUNCTUAL_MULTI.search(msg) is not None)
            if begin_with_punctuations:
                msg = Common.BEGIN_PUNCTUAL_MULTI.sub("", msg)
            if ending_with_punctuations:
                msg = Common.ENDS_PUNCTUAL_MULTI.sub("", msg)

        return msg, begin_with_punctuations, ending_with_punctuations

    def removeOriginal(msg, trans):
        if not trans:
            return trans

        has_abbr = Common.hasAbbr(trans)
        if has_abbr:
            return trans

        msg = re.escape(msg)
        p = r'\b{}\b'.format(msg)
        has_original = (re.search(p, trans, flags=re.I) is not None)
        endings_list = ["", "s", "es", "ies", "ed", "ing", "lly",]
        endings = sorted(endings_list, key=lambda x: len(x), reverse=True)

        if has_original:
            for end in endings:
                p = r'{}{}:\ '.format(msg, end)
                trans = re.sub(p, "", trans, flags=re.I)

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

    def cleanSlashesQuote(msg):
        if not msg:
            return msg

        msg = msg.replace("\\\\", "\\")
        msg = msg.replace("\\\"", "\"")
        return msg

    def patternMatchAll(pat, text):
        return_dict = {}
        for m in pat.finditer(text):
            match_record = MatcherRecord(matcher_record=m)
            first_record = list(match_record.items())[0]
            loc, _ = first_record
            dict_entry = {loc: match_record}
            return_dict.update(dict_entry)
            count = len(match_record.getSubEntriesAsList())
            # dd(f'patternMatchAll: added entry:{dict_entry}, count:{count}')
        # dd(f'patternMatchAll: entries: {dict_entry}; total length:{len(return_dict)}')
        return return_dict


    def findInvert(pattern, text:str,
                   is_removing_surrounding_none_alphas=False,
                   to_matcher_record=False,
                   new_root_location=None):
        '''
        findInvert:
            Find list of words that are NOT matching the pattern.
            can use to find words amongst puntuations for instance.
            The routine uses internally declared FILLER_CHAR to mark the
            boundaries of unmatched words and then SPLIT at these boundaries
        :param pattern:
            the re.compile(d) pattern to use to find/replace
        :param text:
            the string of text that words are to be found
        :param is_remove_empty:
            If this is set to True, removing empty strings while processing,
            and these empty strings (or just contain spaces) won't be
            in the returning list
        :param is_removing_surrounding_none_alphas:
            removing empty spaces and symbols surrounding words
        :return:
            list of words that are NOT matching the pattern input
        '''

        def dealWithOptions(mm_found_list):
            result_list = []
            mm_record: MatcherRecord = None
            backup_mm_copy: MatcherRecord = None
            for found_loc, found_txt, mm_record in mm_found_list:
                backup_mm_copy = CP.deepcopy(mm_record)
                sub_loc = sub_txt = left = right = None
                have_sub_record = False
                # 1. Tried to open the record with all expected entries and see if all are there
                # if not, then take the alternative approach to get sub-elements in the exception handling section
                try:
                    mm_record_list = mm_record.getSubEntriesAsList()
                    found_loc, found_txt =mm_record_list[0]
                    left_loc, left = mm_record_list[1]
                    sub_loc, sub_txt = mm_record_list[2]
                    right_loc, right = mm_record_list[3]
                except Exception as e:
                    sub_loc, left, sub_txt, right, sub_record = Common.getTextWithinWithDiffLoc(found_txt, to_matcher_record=True)
                    is_all_non_alpha = (not bool(sub_txt))
                    if is_all_non_alpha:
                       continue

                    mm_record.addSubRecordFromAnother(sub_record)

                have_sub_record = (bool(left) or bool(right))
                if is_removing_surrounding_none_alphas:
                    index_to_use = (2 if have_sub_record else 0)
                    mm_record.setMainToUseExistingIndex(index_to_use)

                if new_root_location:
                    mm_record.updateMasterLoc(new_root_location)

                actual_loc = (mm_record.s, mm_record.e)
                if to_matcher_record:
                    entry=(actual_loc, mm_record)
                else:
                    entry=(actual_loc, mm_record.txt)
                result_list.append(entry)
            return result_list
        try:
            is_string = (isinstance(pattern, str))
            is_pattern = (isinstance(pattern, Pattern))
            is_acceptable = (is_string or is_pattern)
            if not is_acceptable:
                raise ValueError(f'{pattern} is invalid. Only accept string or re.Pattern types.')
        except Exception as e:
            raise e

        invert_required = False
        pat = pattern
        if is_string:
            # form the invert character pattern
            pat_string = r'(%s)(\w[^%s]+\w)(%s)' % (pattern, pattern, pattern)
            pat = compile(pat_string)
        else:
            invert_required = True

        found_list = []
        mm : MatcherRecord = None
        matched_dict = Common.patternMatchAll(pat, text)
        if not invert_required:
            for mmloc, mm in matched_dict.items():
                loc, found_txt = mm.getOriginAsTuple()
                entry = (loc, found_txt, mm)
                found_list.append(entry)
        else:
            # 2: extract location list
            loc_list = matched_dict.keys()

            # 3: extract invert locations, using the location list above
            invert_loc_list = []
            ws = we = 0
            for s, e in loc_list:
                we = s
                if (ws < we):
                    invert_loc_list.append((ws, we))
                ws = e
            we = len(text)
            if (ws < we):
                invert_loc_list.append((ws, we))

            # 4: using the invert location list, extract words, exclude empties.
            for ws, we in invert_loc_list:
                found_txt = text[ws:we]
                loc = (ws, we)
                mm = MatcherRecord(s=ws, e=we, txt=found_txt)
                entry = (loc, found_txt, mm)
                found_list.append(entry)

        result_list_final = dealWithOptions(found_list)
        result_list_final.sort(key=OP.itemgetter(0), reverse=True)
        return_dict = OrderedDict(result_list_final)
        dd('findInvert() found_list:')
        dd('-' * 30)
        pp(return_dict)
        dd('-' * 30)

        return return_dict

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
        entry_list = []

        matched_list = Common.findInvert(Common.MENU_SEP, text_entry)
        for loc, mtxt in matched_list.items():
            ss, ee = loc
            entry=(ss, ee, mtxt)
            entry_list.append(entry)
        return entry_list

    def isListEmpty(list_elem):
        is_empty = (list_elem is None) or (len(list_elem) == 0)
        return is_empty

    def removeLowerCaseDic(dic_list : dict ):
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
            dd("k:", k)
            dd("v:", k)
            dd(e)
            raise e
        return u_case

    def isTextuallySimilar(from_txt, to_txt):
        from_list = Common.WORD_ONLY_FIND.findall(from_txt.lower())
        to_list = Common.WORD_ONLY_FIND.findall(to_txt.lower())

        # convert list to set of words, non-repeating
        to_set = "".join(to_list)
        from_set = "".join(from_list)

        is_similar = (to_set in from_set) or (from_set in to_set)
        if not is_similar:
            from_set = set(from_set)
            to_set = set(to_set)
            intersect_set = from_set.intersection(to_set)
            is_similar = (intersect_set == from_set) or (intersect_set == to_set)
        return is_similar

    # def isTextuallyVerySimilar(from_txt, to_txt):
    #     similar_ratio = LE.ratio(from_txt, to_txt)
    #     acceptable = (similar_ratio >= 0.75)
    #     return acceptable

    def isTextuallySame(from_txt:str, to_txt:str):

        is_valid = (from_txt is not None) and (to_txt is not None)
        is_both_none = (from_txt is None) and (to_txt is None)
        if is_both_none:
            return True
        if not is_valid:
            return False

        from_list = Common.WORD_ONLY_FIND.findall(from_txt.lower())
        to_list = Common.WORD_ONLY_FIND.findall(to_txt.lower())

        # convert list to set of words, non-repeating
        to_set = "".join(to_list)
        from_set = "".join(from_list)

        # perform set intersection to find common set
        is_same = (to_set == from_set)
        return is_same

    def isTextuallySubsetOf(msg, tran):
        msg_list = Common.WORD_ONLY_FIND.findall(msg.lower())
        tran_list = Common.WORD_ONLY_FIND.findall(tran.lower())
        msg_str = "".join(msg_list)
        tran_str = "".join(tran_list)

        # perform set intersection to find common set
        is_subset = (msg_str in tran_str)
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

    # https://stackoverflow.com/questions/22058048/hashing-a-file-in-python , answered Jul 2 '17 at 17:23 - maxschlepzig (Georg Sauthoff)
    #
    # maxschlepzig
    # 23.3k99 gold badges9393 silver badges126
    def sha256sum(filename):
        h = hashlib.sha256()
        b = bytearray(Common.PAGE_SIZE) # PAGE_SIZE = 20 * 4096, original 128*1024
        mv = memoryview(b)
        with open(filename, 'rb', buffering=0) as f:
            for n in iter(lambda : f.readinto(mv), 0):
                h.update(mv[:n])
        return h.hexdigest()

    def getFileModifiedTime(filename):
        return time.ctime( os.path.getmtime(filename))

    def getFileCreatedTime(filename):
        return time.ctime( os.path.getctime(filename))

    def removeLeadingTrailingSymbs(txt):
        def cleanForward(txt, pair_dict, leading_set):
            if not leading_set:
                return txt, leading_set

            temp_txt = str(txt)
            count = 0
            for sym_on in leading_set:
                is_sym_on_in_dict = (sym_on in pair_dict)
                if not is_sym_on_in_dict:
                    continue

                sym_off = pair_dict[sym_on]
                temp = temp_txt[1:]
                is_balance = Common.isBalancedSymbol(sym_on, sym_off, temp)
                if is_balance:
                    temp_txt = temp
                    count += 1
            if count > 0:
                leading_set = leading_set[count:]
            return temp_txt, leading_set

        def cleanBackward(txt, pair_dict, trailing_set):
            if not trailing_set:
                return txt, trailing_set

            temp_txt = str(txt)
            count = 0
            for sym_off in reversed(trailing_set):
                is_controlled = (sym_off in pair_dict)
                if not is_controlled:
                    temp_txt = temp_txt[:-1]
                    count += 1
                    continue

                sym_on = pair_dict[sym_off]
                temp = temp_txt[:-1]
                is_balance = Common.isBalancedSymbol(sym_on, sym_off, temp)
                if is_balance:
                    temp_txt = temp
                    count += 1
            if count > 0:
                trailing_set = trailing_set[:-count]
            return temp_txt, trailing_set

        def cleanBothEnds(txt, pair_dict, leading_set, trailing_set):
            count = 0
            temp_txt = str(txt)

            if leading_set and trailing_set:
                symbol_set = leading_set + trailing_set
            elif leading_set:
                symbol_set = leading_set
            elif trailing_set:
                symbol_set = trailing_set
            else:
                return temp_txt, leading_set, trailing_set

            for sym_on in symbol_set:
                is_sym_off_there = (sym_on in pair_dict)
                if not is_sym_off_there:
                    break

                sym_off = pair_dict[sym_on]
                is_both_ends = (temp_txt.startswith(sym_on) and temp_txt.endswith(sym_off))
                if not is_both_ends:
                    continue

                temp = temp_txt[1:-1]
                is_balance = Common.isBalancedSymbol(sym_on, sym_off, temp)
                if is_balance:
                    temp_txt = temp
                    count += 1
            if count > 0:
                leading_set = leading_set[count:]
                trailing_set = trailing_set[:-count]
            return temp_txt, leading_set, trailing_set

        # txt = '   ({this}....,!'
        # # txt = '(also :kbd:`Shift-W` :menuselection:`--> (Locked, ...)`) This will prevent all editing of the bone in *Edit Mode*; see :ref:`bone locking <animation_armatures_bones_locking>`'
        # # txt = '(Top/Side/Front/Camera...)'
        txt = txt.strip()

        pair_list = [('{', '}'), ('[', ']'), ('(', ')'), ('<', '>'), ('$', '$'),(':', ':'), ('*', '*'), ('\'', '\''), ('"', '"'), ('`', '`'),]
        pair_dict = {}
        for p in pair_list:
            s, e = p
            entry_1 = {s:e}
            entry_2 = {e:s}
            pair_dict.update(entry_1)
            pair_dict.update(entry_2)

        leading_set = Common.REMOVABLE_SYMB_FULLSET_FRONT.findall(txt)
        if leading_set:
            leading_set = leading_set[0]

        trailing_set = Common.REMOVABLE_SYMB_FULLSET_BACK.findall(txt)
        if trailing_set:
            trailing_set = trailing_set[0]

        temp_txt = str(txt)
        temp_txt, leading_set, trailing_set = cleanBothEnds(temp_txt, pair_dict, leading_set, trailing_set)

        temp_txt, leading_set = cleanForward(temp_txt, pair_dict, leading_set)
        temp_txt, trailing_set = cleanBackward(temp_txt, pair_dict, trailing_set)

        temp_txt, _, _ = cleanBothEnds(temp_txt, pair_dict, leading_set, trailing_set)
        return temp_txt

    def isBalancedSymbol(symb_on, symb_off, txt):
        p_str = f'\{symb_on}([^\{symb_on}\{symb_off}]+)\{symb_off}'
        p_exp = r'%s' % (p_str.replace("\\\\", "\\"))
        pattern = re.compile(p_exp)
        p_list = Common.patternMatchAll(pattern, txt)
        has_p_list = (len(p_list) > 0)
        if has_p_list:
            temp_txt = str(txt)
            for loc, mm in p_list.items():
                s, e = loc
                left = temp_txt[:s]
                right = temp_txt[e:]
                temp_txt = left + right
            return not ((symb_on in temp_txt) or (symb_off in temp_txt))
        else:
            return True

    def hasAbbr(txt):
        abbr_str = RefType.ABBR.value
        has_abbr = (abbr_str in txt)
        return has_abbr

    def extractAbbr(abbr_txt):
        if not abbr_txt:
            return None, None, None

        abbr_dict = Common.patternMatchAll(Common.ABBREV_PATTERN_PARSER, abbr_txt)
        if not abbr_dict:
            return None, None, None

        abbrev_orig_rec = abbrev_part = exp_part = None
        mm: MatcherRecord = None

        for s, mm in abbr_dict.items():
            abbrev_orig_rec = mm.getOriginAsTuple()
            l = mm.getSubEntriesAsList()
            for loc, txt in l:
                found_texts = Common.ABBR_TEXT_ALL.findall(txt)
                first_entry = found_texts[0]
                abbrev_part, exp_part = first_entry

        return abbrev_orig_rec, abbrev_part, exp_part

    def testDict(dic_to_use):
        key_list = list(dic_to_use.keys())
        debug_text = 'trick'
        is_there = (debug_text.lower() in key_list)
        if not is_there:
            print(f'debug_text:{debug_text} IS NOT THERE')
        else:
            print(f'debug_text:[{debug_text}] exists:{is_there}')

    def findInSortedList(item, sorted_list):
        if not sorted_list:
            return None
        if not item:
            return None
        
        lower_item = item.lower()
        lo = 0
        hi = len(sorted_list)
        found_index = bisect_left(sorted_list, lower_item, lo, hi)        
        is_found = (found_index >= 0 and found_index < hi)
        if not is_found:            
            return None
        else:
            try:
                found_item = sorted_list[found_index]
                is_found = (found_item == lower_item)
                if is_found:
                    return found_item
                else:
                    return None
            except Exception as e:
                print(f'Finding message: [{item}], found index:[{found_index}]')
                raise e

    def getTextWithinBrackets(
            start_bracket: str,
            end_bracket: str,
            text:str,
            is_include_bracket:bool =False,
            replace_internal_start_bracket:str = None,
            replace_internal_end_bracket:str = None
    ) -> list:

        def pop_q(pop_s, pop_e) -> bool:
            last_s = q.pop()
            orig_txt = text[last_s:pop_e]
            orig_s = last_s
            orig_e = pop_e

            ss = (last_s if is_include_bracket else last_s + len(start_bracket))
            ee = (pop_e if is_include_bracket else pop_s)

            txt_line = text[ss:ee]
            if not txt_line:
                return False

            is_replace_internal_bracket = (replace_internal_start_bracket and (start_bracket in txt_line))
            if is_replace_internal_bracket:
                txt_line = txt_line.replace(start_bracket, replace_internal_start_bracket)

            loc = (orig_s, orig_e)
            entry = {loc: orig_txt}
            sentence_list.update(entry)
            return True

        def getBracketList():
            # 1. find positions of start bracket
            if is_same_brakets:
                p_txt = r'\%s' % start_bracket
            else:
                p_txt = r'\%s|\%s' % (start_bracket, end_bracket)

            p = re.compile(p_txt)

            # split at the boundary of start and end brackets
            brk_list=[]
            m_list = p.finditer(text)
            for m in m_list:
                ss = m.start()
                ee = m.end()
                brk = m.group(0)
                entry=(ss, ee, brk)
                brk_list.append(entry)
            return brk_list

        def getSentenceList():
            bracket_list = getBracketList()
            if not bracket_list:
                return sentence_list

            # detecting where start/end and take the locations
            mm: MatcherRecord = None
            if is_same_brakets:
                for s, e, bracket in bracket_list:
                    is_bracket = (bracket == start_bracket)
                    if is_bracket:
                        if not q:
                            q.append(s)
                        else:
                            is_finished = pop_q(s, e)
                            if not is_finished:
                                continue
            else:
                for s, e, bracket in bracket_list:
                    is_open = (bracket == start_bracket)
                    is_close = (bracket == end_bracket)
                    if is_open:
                        q.append(s)
                    if is_close:
                        if not q:
                            continue
                        else:
                            is_finished = pop_q(s, e)
                            if not is_finished:
                                continue
            return sentence_list

        sentence_list = {}
        q = deque()
        s: int = -1
        e: int = -1
        last_s: int = -1
        is_same_brakets = (start_bracket == end_bracket)
        if is_same_brakets:
            print(f'getTextWithinBracket() - WARNING: start_bracket and end_braket is THE SAME {start_bracket}. '
                  f'ERRORS might occurs!')

        sentence_list = getSentenceList()
        result_dict = OrderedDict()
        sorted_sentence_list = list(sentence_list.items())
        sorted_sentence_list.sort()
        obs: LocationObserver = None
        for index, (sub_loc, sub_txt) in enumerate(sorted_sentence_list):
            is_first = (index == 0)
            if is_first:
                obs = LocationObserver(msg=sub_txt)

            is_covered = obs.isLocUsed(sub_loc)
            if is_covered:
                continue

            part_dict = Common.findInvert(Common.FILLER_PARTS,
                                          sub_txt,
                                          is_removing_surrounding_none_alphas=True,
                                          to_matcher_record=True,
                                          new_root_location=sub_loc)
            result_dict.update(part_dict)

        temp_list = list(result_dict.items())
        temp_list.reverse()
        sentence_list = OrderedDict(temp_list)
        return sentence_list

    def removingNonAlpha(original_word: str):
        default_loc = (0, 0)
        is_empty_word = (original_word is None) or (len(original_word) == 0)
        if original_word is None:
            return (default_loc, original_word)

        max_len = len(original_word)
        s = max_len // 2
        e = s

        left_part = original_word[0:s]
        right_part = original_word[e:max_len]
        matcher = Common.WORD_END_REMAIN.search(left_part)
        if matcher:
            grp = matcher.group(0)
            s -= len(grp)

        matcher = Common.WORD_START_REMAIN.search(right_part)
        if matcher:
            grp = matcher.group(0)
            e += len(grp)

        loc = (s, e)
        new_word = original_word[s:e]
        return (loc, new_word)

    def insertTranslation(orig_word: str, new_word: str, current_trans: str) -> str:
        is_valid = (orig_word and new_word and current_trans)
        if not is_valid:
            return current_trans

        loc, actual_new_word = Common.locRemain(orig_word, new_word)
        ss, ee = loc
        left = orig_word[:ss]
        right = orig_word[ee:]
        new_tran = left + current_trans + right
        return new_tran

    def locRemain(original_word: str, new_word: str) -> list:
        '''
        locRemain:
            Find where the remainder starts, ends, excluding alphanumeric characters, so can decide
            if remainder can be removed or not and how far
        :param original_word: word where new_word is extracted from
        :param new_word: word from which dictionary has found from original word
        :return:
            list of locations (start, end) within the original where original word including
            but not containing any alpha-numerical characters, which can be removed (ie. remainder
            parts of the word in the original_word)
        '''
        # REWRITE THIS, MAKE IT SHORTER
        try:
            max_len = len(original_word)
            ss = original_word.find(new_word)
            ee = ss + len(new_word)

            found_test = original_word[ss:ee]
            ok = (found_test == new_word)
            if not ok:
                raise Exception(f'FAILED TO LOCATE [{new_word}] in [{original_word}]')

            left_part = original_word[0:ss]
            right_part = original_word[ee:max_len]

            matcher = Common.WORD_END_REMAIN.search(left_part)
            if matcher:
                grp = matcher.group(0)
                ss -= len(grp)

            matcher = Common.WORD_START_REMAIN.search(right_part)
            if matcher:
                grp = matcher.group(0)
                ee += len(grp)

            loc = (ss, ee)
            return loc, original_word[ss:ee]
        except Exception as e:
            raise e

        return (-1, -1), new_word

    def replaceStr(from_str: str, to_str: str, txt: str) -> str:
        '''
        Replace a sub-string (from_str) with another sub-string (to_str) in the
        string input (txt), with return count
        :param from_str:
            the sub-string to be replaced
        :param to_str:
            the sub-string acting as the replacement, to be replaced by.
        :param txt:
            the string to perform the replacement upon.
        :return:
            result_str, count

            the string with replacements performed upon,
            the count for number of replaced instances, how many times the replacement succeeded
        '''
        prev_txt = str(txt)
        rep_count: int = 0
        result_txt = str(txt)
        is_finished = False
        while not is_finished:
            result_txt = result_txt.replace(from_str, to_str, 1)
            has_changed = not (result_txt == prev_txt)
            if has_changed:
                rep_count += 1
                prev_txt = str(result_txt)
            else:
                is_finished = True
        return result_txt, rep_count

    def bracketParser(text):
        def error_msg(item, text_string):
            return f'Imbalanced parenthesis! Near the "{item}" text_string:[{text_string}]'

        _tokenizer = Common.ARCH_BRACKET_SPLIT.split
        def tokenize(text_line: str):
            return list(filter(None, _tokenizer(text_line)))

        def _helper(tokens):
            outside_brackets = []
            bracketed = []
            q = []
            max = len(tokens)
            chosen_items = []
            start_loc = end_loc = 0
            for i in range(0, max):
                item = tokens[i]
                if item == '(':
                    q.append(i)
                elif item == ')':
                    if not q:
                        raise ValueError(error_msg(item, text))
                    q.pop()
                    bracketed.extend(chosen_items)
                    chosen_items = []
                else:
                    start_loc = text.find(item, end_loc)
                    end_loc = start_loc + len(item)
                    loc = (start_loc, end_loc)
                    entry = (loc, item)
                    if q:
                        chosen_items.append(entry)
                    else:
                        outside_brackets.append(entry)
            if q:
                raise ValueError(error_msg(item, text))
            return bracketed, outside_brackets
        tokens = tokenize(text)
        bracketed_list, outside_bracket_list = _helper(tokens)
        return bracketed_list, outside_bracket_list

    def wordInclusiveLevel(orig_txt:str, fuzzy_txt:str) -> int:
        '''
        Expected to see 0 to indicate every fuzzy word is included in
        original text
        :param orig_txt: original text
        :param fuzzy_txt: fuzzily found text
        :return:
            0 if all words in fuzzy text is included in the original text, fuzzily
            > 0 number of words NOT included in the original text
        '''
        def isFuzzilyInList(word_to_find, word_list):
            for word in word_list:
                ratio = fuzz.ratio(word, word_to_find)
                acceptable = (ratio >= Common.FUZZY_ACCEPTABLE_RATIO)
                if acceptable:
                    return True
            return False

        fuzzy_list = fuzzy_txt.split()
        orig_list = orig_txt.split()
        list_len = len(fuzzy_list)
        fuzzy_word_count = 0
        for fuzzy_word in fuzzy_list:
            is_in_original = (fuzzy_word in orig_list) or isFuzzilyInList(fuzzy_word, orig_list)
            fuzzy_word_count += (1 if is_in_original else 0)

        inc_percentage = fuzzy_word_count / list_len * 100
        return inc_percentage

    def getLeadingMatchCount(k_item, item):
        def binary_match(loc_from, loc_to):
            f_len = len(loc_from)
            f_len_mid = (f_len // 2)
            f_list_0 = loc_from[:f_len_mid]

            t_len = len(loc_to)
            t_len_mid = (t_len // 2)
            t_list_0 = loc_to[:t_len_mid]

            is_same = (t_list_0.lower() == f_list_0.lower())
            if not is_same:
                return False

            f_list_1 = loc_from[f_len_mid+1:]
            t_list_1 = loc_to[t_len_mid+1:]
            is_same = (t_list_0.lower() == f_list_0.lower())
            if is_same:
                return True
            else:
                return binary_match(f_list_1, t_list_1)

        item_length = len(item)
        matched_total = 0
        for index, kw in enumerate(k_item):
            is_valid_index = (index < item_length)
            if not is_valid_index:
                break
            iw = item[index]
            is_matched = (iw == kw)
            if is_matched:
                matched_total += 1
            else:
                break
        return matched_total

    def findUntranslatedWords(orig_txt, fuzzy_txt):
        def insertEntryIntoRemainDict():
            orig_loc = orig_locs[index]
            entry = {orig_loc: orig_word}
            remain_dict.update(entry)

        # expecting to find fuzzy_txt within orig_txt, try to locate the range
        orig_txt_copy = str(orig_txt)
        orig_word_list = Common.findInvert(Common.SPACES, orig_txt)
        fuzzy_word_list = Common.findInvert(Common.SPACES, fuzzy_txt)

        fuzzy_locs = list(fuzzy_word_list.keys())
        fuzzy_locs.reverse()

        fuzzy_words = list(fuzzy_word_list.values())
        fuzzy_words.reverse()

        orig_locs = list(orig_word_list.keys())
        orig_locs.reverse()

        orig_words = list(orig_word_list.values())
        orig_words.reverse()

        remain_dict = OrderedDict()
        is_finished = False
        for index, orig_word in enumerate(orig_words):
            try:
                fuzzy_word = fuzzy_words[index]
                ratio = fuzz.ratio(orig_word, fuzzy_word)
                sounds_similar = (ratio >= Common.FUZZY_ACCEPTABLE_RATIO)
                if sounds_similar:
                    continue

                insertEntryIntoRemainDict()
            except Exception as e:
                insertEntryIntoRemainDict()

        reversed_remain = list(remain_dict.items())
        reversed_remain.reverse()
        rev_remain = OrderedDict(reversed_remain)
        return rev_remain

    def splitExpVar(item, k):
        i_list = item.split(Common.SENT_STRUCT_SYMB)

        i_left = i_list[0]
        i_right = i_list[1]
        i_left_len = len(i_left)
        i_right_len = len(i_right)

        i_left_list = i_right_list = []
        if i_left:
            i_left_list = i_left.split()

        if i_right:
            i_right_list = i_right.split()

        i_left_word_count = len(i_left_list)
        i_right_word_count = len(i_right_list)
        i_exp_word_count_total = (i_left_word_count + i_right_word_count)

        k_length = len(k)
        k_word_list = Common.SPACES.split(k)
        k_word_count = len(k_word_list)

        is_less_than_expected = (k_word_count < i_exp_word_count_total)
        if is_less_than_expected:
            return i_left, i_right, None, None

        k_left = k_right = ""
        if i_left_word_count:
            k_left = ' '.join(k_word_list[:i_left_word_count])

        if i_right_word_count:
            k_right = ' '.join(k_word_list[i_right_word_count:])

        return i_left, i_right, k_left, k_right

    def getListOfVariations(txt):
        list_var = []
        for i in range(len(txt), 0, -1):
            entry = txt[0:i]
            list_var.append(entry)
        return list_var

    def getNoneAlphaPart(msg, is_start=True):
        if not msg:
            return ""

        non_alnum_part = ""
        if is_start:
            non_alpha = Common.START_WORD_SYMBOLS.search(msg)
        else:
            non_alpha = Common.END_WORD_SYMBOLS.search(msg)

        if non_alpha:
            non_alnum_part = non_alpha.group(0)
        return non_alnum_part

    def getRemainedWord(orig_txt: str, new_txt: str):
        def isInNewFuzzy(search_word):
            for loc, word in new_txt_word_list:
                match_rat = fuzz.ratio(word, search_word)
                is_same = (match_rat >= Common.FUZZY_MODERATE_ACCEPTABLE_RATIO)
                if is_same:
                    return True
            return False

        blank_orig_txt = str(orig_txt)
        orig_word_dict = Common.patternMatchAll(Common.CHARACTERS, orig_txt)
        orig_word_list = list(orig_word_dict.items())

        new_txt_word_dict = Common.patternMatchAll(Common.CHARACTERS, new_txt)
        new_txt_word_list = list(orig_word_dict.items())

        remain_word_dict={}
        i = 0
        try:
            for i, entry in enumerate(orig_word_list):
                orig_loc, mm = entry
                (s, e), orig_word = mm.getOriginAsTuple()
                is_in_new = isInNewFuzzy(orig_word)
                if is_in_new:
                    continue

                entry = {orig_loc: orig_word}
                remain_word_dict.append(entry)

        except Exception as e:
            max = len(orig_word)
            if i < max:
                remain_sub_list = orig_word_list[i:]
                remain_sub_dict = OrderedDict(remain_sub_list)
                remain_word_dict.update(remain_sub_dict)

        return remain_word_dict

    def getTextWithinWithDiffLoc(msg, to_matcher_record=False):
        # should really taking bracket pairs into account () '' ** "" [] <> etc.. before capture
        left_part = Common.getNoneAlphaPart(msg, is_start=True)
        right_part = Common.getNoneAlphaPart(msg, is_start=False)
        ss = len(left_part)
        ee = (-len(right_part) if right_part else len(msg))
        mid_part = msg[ss:ee]
        length_ee = len(right_part)
        diff_loc = (ss, length_ee)

        main_record: MatcherRecord = None
        if to_matcher_record:
            ls=0
            le=ss
            ms=le
            me=ms + len(mid_part)
            rs=me
            re=rs + len(right_part)

            main_record=MatcherRecord(s=0, e=len(msg), txt=msg)
            if left_part:
                main_record.addSubMatch(ls, le, left_part)
                test_txt = left_part[ls: le]
            else:
                main_record.addSubMatch(-1, -1, None)
            if mid_part:
                main_record.addSubMatch(ms, me, mid_part)
                test_txt = left_part[ms: me]
            else:
                main_record.addSubMatch(ls, re, msg)
            if right_part:
                main_record.addSubMatch(rs, re, right_part)
                test_txt = left_part[rs: re]
            else:
                main_record.addSubMatch(-1, -1, None)

        return diff_loc, left_part, mid_part, right_part, main_record

    def getTextWithin(msg):
        diff_loc, left, mid, right,_ = Common.getTextWithinWithDiffLoc(msg)
        return left, mid, right

    def replaceWord(orig_word: str, new_word: str, replace_word: str) -> str:

        is_inclusive = (new_word in orig_word)
        if is_inclusive:
            ss = orig_word.find(new_word)
            ee = ss + len(new_word)
            left_part = orig_word[:ss]
            right_part = orig_word[ee:]
            matcher = Common.WORD_END_REMAIN.search(left_part)
            if matcher:
                grp = matcher.group(0)
                ss -= len(grp)

            matcher = Common.WORD_START_REMAIN.search(right_part)
            if matcher:
                grp = matcher.group(0)
                ee += len(grp)

            left_part = orig_word[:ss]
            right_part = orig_word[ee:]
            final_part = left_part + replace_word + right_part
            return final_part
        else:
            left_part = Common.getNoneAlphaPart(orig_word, is_start=True)
            right_part = Common.getNoneAlphaPart(orig_word, is_start=False)
            final_part = left_part + replace_word + right_part
        return final_part

    # def getSentenceList(input_text:str) -> list:
    #     t_list = {}
    #     doc = Common.nlp(input_text)
    #     sen = []
    #     last_e = 0
    #     for token in doc:
    #         is_punct = (token.pos_ == 'PUNCT')
    #         if not is_punct:
    #             txt = token.text
    #             sen.append(token.text)
    #             continue
    #
    #         if not sen:
    #             continue
    #
    #         sen_text = ' '.join(sen)
    #         ss = input_text.find(sen_text, last_e)
    #         is_error = (ss < 0)
    #         if is_error:
    #             raise ValueError(f'Common.getSentenceList(): Unable to find text [{sen_text}] in [{input_text}]')
    #
    #         ee = ss + len(sen_text)
    #         last_e = ee
    #         loc = (ss, ee)
    #         entry = {loc: sen_text}
    #         t_list.update(entry)
    #         sen = []
    #
    #     return t_list

    def matchTextPercent(t1: str, t2: str):
        match_percent = 0.0
        try:
            l1 = t1.split()
            l2 = t2.split()
            l1_count = len(l1)
            l1_per_each_word = (100 / l1_count)

            for i in range(0, l1_count):
                w1 = l1[i]
                w2 = l2[i]
                word_percent = Common.matchWordPercent(w1, w2)
                is_tool_small = (word_percent <= Common.FUZZY_PERFECT_MATCH_PERCENT)
                if is_tool_small:
                    break
                match_percent += (l1_per_each_word * word_percent / 100)
        except Exception as e:
            pass
        return match_percent

    def matchWordPercent(t1:str, t2:str):
        match_percent = 0.0
        try:
            l1 = len(t1)
            l2 = len(t2)

            lx = max(l1, l2)
            lc = 100 / lx
            for i, c1 in enumerate(t1):
                c2 = t2[i]
                is_matched = (c1 == c2)
                if not is_matched:
                    # print(f'stopped at [{i}], c1:[{c1}], c2:[{c2}]')
                    break
                match_percent += lc
        except Exception as e:
            pass
        return match_percent

    def isFullyTranslated(txt):
        is_all_filler_and_spaces = (Common.FILLER_CHAR_AND_SPACE_ONLY_PATTERN.search(txt) is not None)
        return is_all_filler_and_spaces

    def isTranslated(txt):
        is_overlapped = (Common.FILLER_CHAR_PATTERN.search(txt) is not None)
        return is_overlapped

    def patchingBeforeReturn(left, right, patch_txt, orig_txt):

        is_in_valid = not (left or right)
        if is_in_valid:
            return patch_txt

        patch_txt_right = patch_txt_left = ''
        if left:
            patch_txt_left = patch_txt[:len(left)]
        if right:
            patch_txt_right = patch_txt[-len(right)]

        is_patching_left = (patch_txt_left != left)
        is_patching_right = (patch_txt_right != right)

        return_text = patch_txt
        if is_patching_left:
            return_text = left + patch_txt
        if is_patching_right:
            return_text = patch_txt + right

        return return_text

    def isBetweenRange(number, range_s, range_e):
        is_between = (range_s <= number <= range_e)
        return is_between

    def isOverlappedLoc(locf, loct):
        fs, fe = locf
        ts, te = loct
        is_ovrlap = Common.isOverlapped(fs, fe, ts, te)
        return is_ovrlap

    def isOverlapped(fs, fe, ts, te):
        is_fs_between = (ts <= fs <= te)
        is_fe_between = (ts <= fe <= te)
        is_ovrlap = (is_fs_between or is_fe_between)
        return is_ovrlap

    def stripSpaces(txt):
        start = 0
        end = 0
        leading_spaces: re.Match = Common.START_SPACES.search(txt)
        if leading_spaces:
            start = leading_spaces.end()

        trailing_spaces: re.Match = Common.END_SPACES.search(txt)
        if trailing_spaces:
            end = trailing_spaces.start()

        end_count = 0
        if end:
            end_count=(len(txt) - end)
        else:
            end = len(txt)
        return_txt = txt[start: end]
        return start, end_count, return_txt

    def subtractText(minuend_loc, minuend, subtrahend_loc, subtrahend):
        this_s, this_e = minuend_loc
        other_s, other_e = subtrahend_loc

        min_start = min(this_s, other_s)
        max_end = max(this_e, other_e)
        mask_orig = (' ' * max_end)

        start_part = (Common.FILLER_CHAR * min_start)
        other_part = (Common.FILLER_CHAR * (other_e - other_s))
        mask = start_part + mask_orig[min_start:]
        mask = mask[:other_s] + other_part + mask[other_e:]

        this_part = mask[this_s: this_e]
        # spaces to keep, FILLER_CHAR to remove
        this_txt = minuend
        list_of_remain = Common.patternMatchAll(Common.SPACES, this_part)
        this_txt_dict = {}
        for loc, mm in list_of_remain:
            (s, e), txt_part = mm.getOriginAsTuple()
            is_not_worth_keeping = (Common.SYMBOLS_ONLY.search(txt_part) is not None)
            if is_not_worth_keeping:
                continue

            start_count, end_count, new_txt_part = Common.stripSpaces(txt_part)
            new_loc = (s + start_count, e - end_count)
            entry = {new_loc: new_txt_part}
            this_txt_dict.update(entry)
        # this list could be empty, in which case remove left part, keep the right part (A - B = empty => keep B only)
        return this_txt_dict

    def debugging(txt):
        # msg = 'between root and tip'
        # msg = 'Profile Brush'
        # msg = ' reversed...'
        # msg = "BLENDER_SYSTEM_SCRIPTS"
        # msg = "command-line arguments"
        # msg = "Factory Settings"
        # msg = "limbs"
        # msg = "data-block"
        # msg = "Object"
        # msg = "and"
        # msg = "larger "
        # msg = "right-click-select"
        # msg = "Material Library VX"
        # msg = "Equals"
        # msg = "fig-mesh-screw-angle"
        msg = "Context"
        # is_debug = (msg and txt and (msg.lower() in txt.lower()))
        is_debug = (msg and txt and (msg.lower() == txt.lower()))
        # is_debug = (msg and txt and txt.startswith(msg))
        if is_debug:
            print(f'Debugging text: {msg} at line txt:{txt}')