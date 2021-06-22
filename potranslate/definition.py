import os
import re
from enum import Enum
from urlextract import URLExtract as URLX
import utils as UT

class OverLappingState(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    BOTH = 3
    WITHIN = 4

class TranslationState(Enum):
    UNTRANSLATED = 0
    ACCEPTABLE = 1
    FUZZY = 2
    IGNORED = 3
    REMOVE = 4

class TextStyle(Enum):
    NORMAL = 0
    ITALIC = 1
    BOLD = 2
    BOX = 3
    RAW = 4

class RefType(Enum):
    PYTHON_FORMAT = "%"
    FUNCTION = "func"
    GA = "\`"
    BLANK_QUOTE = "§"
    ARCH_BRACKET = "()"
    ARCH_BRACKET_OPEN = "("
    ARCH_BRACKET_CLOSE = ")"
    AST_QUOTE = "*"
    DBL_AST_QUOTE = "**"
    DBL_QUOTE = "\""
    SNG_QUOTE = "'"
    MM = ":MM:"
    ABBR = ":abbr:"
    CLASS = ":class:"
    DOC = ":doc:"
    GUILABEL = ":guilabel:"
    KBD = ":kbd:"
    LINENOS = ":linenos:"
    MATH = ":math:"
    MENUSELECTION = ":menuselection:"
    MOD = ":mod:"
    METHOD = ":meth:"
    FUNC = ":func:"
    REF = ":ref:"
    SUP = ":sup:"
    TERM = ":term:"
    OSL_ATTRIB = "w:w"
    TEXT = "generic_text"
    FILLER = "filler"
    ATTRIB = "var:var"

    @classmethod
    def getRef(cls, string_value: str):
        for name, member in cls.__members__.items():
            if member.value == string_value:
                return member
        return None

class Definitions:
    HOME = os.environ['DEV_TRAN']
    log_path = os.path.join(HOME, 'logme.log')

    LOG = UT.get_logger(log_path)

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

    split_sent_seg_txt = r'\s?([\,\.\-\;](?<!(e\.g\.|etc\.))\s)|([\(\)]|[{}])'
    SPLIT_SENT_PAT = re.compile(split_sent_seg_txt)

    total_files = 1358
    file_count = 0
    PAGE_SIZE = 20 * 4096
    MAX_FUZZY_LIST = 100
    MAX_FUZZY_TEST_LENGTH = 0.5
    FUZZY_ACCEPTABLE_RATIO = 90
    FUZZY_MODERATE_ACCEPTABLE_RATIO = 90
    FUZZY_LOW_ACCEPTABLE_RATIO = 70
    FUZZY_VERY_LOW_ACCEPTABLE_RATIO = 45
    FUZZY_PERFECT_MATCH_PERCENT = 60

    APOSTROPHE_CHAR = "'"
    MAX_FUZZY_ACCEPTABLE_RATIO = 95
    FUZZY_RATIO_INCREMENT = 5
    AWESOME_COSSIM_FUZZY_ACCEPTABLE_RATIO = 50
    FUZZY_KEY_LENGTH_RATIO = 0.4

    # sentence structure patternssent
    MAX_SENT_STRUCT_CHOSEN = 20
    sent_struct_start_symb_txt = r'\$\{'
    SENT_STRUCT_START_SYMB = '${'

    SENT_STRUCT_START_SYMB_PAT = re.compile(sent_struct_start_symb_txt, flags=re.I)

    SENT_STRUCT_POSITION_PRIORITY_WEIGHT = 15

    regular_var = r'(\$\{([^\{\}]+)?\})'
    REGULAR_VAR_PAT = re.compile(regular_var)

    max_var_pat_txt = r'(MX(\d+))'
    MAX_VAR_PAT = re.compile(max_var_pat_txt)

    extra_mode = r'(\/([^\/]+))*'
    VAR_EXTRA_MODE = re.compile(extra_mode)

    sent_struct_pat_txt = r'%s' % (regular_var)
    # SENT_STRUCT_PAT = re.compile(r'((\${3})(\w+)?(\/\w+)*)')
    SENT_STRUCT_PAT = re.compile(sent_struct_pat_txt)

    ANY = re.compile(r'^.*$', re.I)
    EXCLUDE = re.compile(r'EX\([^\(\)]+\)', re.I)
    NOT_TRAILING = re.compile(r'NT\([^\(\)]+\)', re.I)
    NOT_LEADING = re.compile(r'NL\([^\(\)]+\)', re.I)
    EQUAL = re.compile(r'EQ\((.*)\)', re.I)
    EMBEDDED_WITH = re.compile(r'EMB\([^\(\)]+\)', re.I)
    LEADING_WITH = re.compile(r'LD\([^\(\)]+\)', re.I)
    TRAILING_WITH = re.compile(r'ED\([^\(\)]+\)', re.I)
    CLAUSED_PART = re.compile(r'\((.*)\)', re.I)

    emb_pat_char = r'\¡'
    emb_pat_part_txt = r'%s([^%s]+)%s' % (emb_pat_char, emb_pat_char, emb_pat_char)
    emb_pat_txt = r'^%s$' % (emb_pat_part_txt)
    PATTERN = re.compile(emb_pat_part_txt, re.I)
    PATTERN_PART = re.compile(emb_pat_part_txt)

    NUMBER_ONLY = re.compile(r'^nbr$', re.I)
    POSITION_PRIORITY = re.compile(r'^pp$', re.I)
    ORDERED_GROUP = re.compile(r'^\d+$', re.I)
    NO_PUNCTUATION = re.compile(r'^np$', re.I)
    MAX_UPTO = re.compile(r'^mx\d+?$', re.I)
    NO_CONJUNCTIVES = re.compile(r'^nc$', re.I)
    NO_FULL_STOP = re.compile(r'^nfs$', re.I)

    TRAN_REF_PATTERN = re.compile(r'\@\{([^{@}]+)?\}')

    python_format_txt = r'(?:\s|^)(\'?%\w\')(?:\W|$)'
    python_format_txt_absolute = r'^%s$' % (python_format_txt)
    PYTHON_FORMAT = re.compile(python_format_txt)
    PYTHON_FORMAT_ABS = re.compile(python_format_txt_absolute)

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
    file_extension = r'([.]%s{2,5})$' % (word)
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
    # funct = r'^%s(%s\((%s)?\))%s$' % (ga_multi, var, param, ga_multi)
    funct = r'%s(%s\((%s[^\(\)]+)?\))%s' % (ga_multi, var, var, ga_multi)
    funct_pat_txt = r'^%s$' % (funct)
    FUNCTION = re.compile(funct_pat_txt)
    FUNCTION_ABS = FUNCTION

    FORWARD_SLASH = re.compile(r'[\w\s]?([\/]+)[\w\s]?')

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
    ABBREV_PATTERN_PARSER_FULL = re.compile(r'^:abbr:[\`]+([^\`]+)[\`]+$')
    ABBREV_CONTENT_PARSER = re.compile(r'([^(]+)\s\(([^\)]+)\)')

    ABBREV_FRONT=re.compile(r':abbr:[\`]+\(')
    GA_BACK=re.compile(r'\)[\`]+')

    punctuals = r'([\\\/\.\,\:\;\!\?\"\*\'\`]+)'
    basic_punctuals = r'([\.\,]+)'

    PUNCTUALS = re.compile(punctuals)
    BASIC_PUNCTUALS = re.compile(basic_punctuals)

    begin_punctuals = r'^%s' % (punctuals)
    end_punctuals = r'%s$' % (punctuals)
    begin_basic_punctuals = r'^%s' % (basic_punctuals)
    end_basic_punctuals = r'%s$' % (basic_punctuals)

    single = r'{1}'
    punctual_single = r'(%s%s)' % (punctuals, single)
    end_punctual_single = r'%s$' % (punctual_single)
    begin_punctual_single = r'^%s' % (punctual_single)

    simple_basic_punctuals = r'([\.\,\!\;]+)'
    end_punctual_in_mid_sentence = r'^%s\s?$' % (simple_basic_punctuals)
    BEGIN_AND_END_BASIC_PUNCTUAL_IN_MID_SENT = re.compile(end_punctual_in_mid_sentence)

    BEGIN_PUNCTUAL_MULTI = re.compile(begin_punctuals)
    BEGIN_PUNCTUAL_SINGLE = re.compile(begin_punctual_single)
    ENDS_PUNCTUAL_MULTI = re.compile(end_punctuals)
    ENDS_PUNCTUAL_SINGLE = re.compile(end_punctual_single)

    BEGIN_BASIC_PUNCTUAL = re.compile(begin_basic_punctuals)
    END_BASIC_PUNCTUAL = re.compile(end_basic_punctuals)


    WORD_ONLY = re.compile(r'\b([\w\.\/\+\-\_\<\>]+)\b')
    REF_SEP = ' -- '
    NON_WORD_ONLY = re.compile(r'^([\W]+)$')
    NON_WORD = re.compile(r'([\W]+)')
    NON_WORD_ENDING = re.compile(r'([\W]+)$')
    NON_WORD_STARTING = re.compile(r'^([\W]+)')
    TRANSLATABLE_CHARACTERS = re.compile(r'[a-zA-Z]+')

    attrib_pat_txt = r'(%s)\:(%s)' % (var, var)
    attrib_pat_abs_txt = r'^(%s)$' % (attrib_pat_txt)
    ATTRIB_REF = re.compile(attrib_pat_abs_txt)
    ATTRIB_REF_ABS = ATTRIB_REF

    GA_REF_PART = re.compile(r':[\w]+:')
    # GA_REF = re.compile(r'[\`]*(:[^\:]+:)*[\`]+(?![\s]+)([^\`]+)(?<!([\s\:]))[\`]+[\_]*')
    # GA_REF = re.compile(r'[\`]*(:[^\:]+:)*[\`]+([^\`]+)[\`]+[\_]*')
    NOT_SPACE= r'(?![\s]+)'
    GA_SYMB = r'\`'
    ga_value_ref_pat_txt = r'[%s]+(%s+[^%s]+%s)[%s]+' % (GA_SYMB, NOT_SPACE, GA_SYMB, NOT_SPACE, GA_SYMB)
    ga_ref_pat_txt = r'[\`]*(:[^\:]+:)*%s[\_]*' % (ga_value_ref_pat_txt)
    GA_REF = re.compile(ga_ref_pat_txt)
    GA_REF_ABS = re.compile(r'^[\`]*(:[^\:]+:)*[\`]+(?![\s]+)([^\`]+?)(?<!([\s\:]))[\`]+[\_]*(?:\W|$)?$')

    #ARCH_BRAKET = re.compile(r'[\(]+(?![\s\.\,]+)([^\(\)]+)[\)]+(?<!([\s\.\,]))')
    OSL_ATTRIB = re.compile(r'[\`]?(\w+:\w+)[\`]?')
    COLON_CHAR = re.compile(r'\:')
    # this (something ... ) can have other links inside of it as well as others
    # the greedy but more accurate is r'[\(]+(.*)?[\)]+'
    # ARCH_BRAKET_SINGLE_PARTS = re.compile(r'[\)]+([^\(]+)?[\(]+')
    arch_bracket_single_txt = r'\(([^\)\(]+)\)'
    arch_bracket_single_full = r'\b%s\b' % (arch_bracket_single_txt)
    arch_bracket_single_absolute = r'^%s(?:\W|$)?$' % (arch_bracket_single_txt)
    ARCH_BRAKET_SINGLE_FULL = re.compile(arch_bracket_single_full)
    ARCH_BRAKET_SINGLE_ABS = re.compile(arch_bracket_single_absolute)

    #ARCH_BRAKET_MULTI = re.compile(r'[\(]+(.*)?[\)]+')
    ARCH_BRAKET_MULTI = re.compile(r'\b\((.*?)\)\b')
    ARCH_BRACKET_SPLIT = re.compile(r'\s*([()])\s*')

    # AST_QUOTE = re.compile(r'[\*]+(?![\s\.\,\`\"]+)([^\*]+)[\*]+(?<!([\s\.\,\`\"]))')
    ast_quote_txt = r'([\*]+)(\w[^\*]+\w)([\*]+)'
    ast_quote_txt_absolute = r'^%s(?:\W|$)?$' % (ast_quote_txt)
    AST_QUOTE = re.compile(ast_quote_txt)
    AST_QUOTE_ABS = re.compile(ast_quote_txt_absolute)

    # DBL_QUOTE = re.compile(r'[\\\"]+(?![\s\.\,\`]+)([^\\\"]+)[\\\"]+(?<!([\s\.\,]))')
    dbl_quote_txt = r'(?<!\\")(")(.*?)(")'
    dbl_quote_txt_abs = r'^%s(?:\W|$)?$' % (dbl_quote_txt)
    DBL_QUOTE = re.compile(dbl_quote_txt)
    DBL_QUOTE_ABS = re.compile(dbl_quote_txt_abs)

    # SNG_QUOTE = re.compile(r'[\']+([^\']+)[\']+(?!([\w]))')
    single_quote_txt = r"(?<!\w)(\')([^\']+)(?:\b)(\')"
    single_quote_txt_absolute = r'^%s(?:\W|$)?$' % (single_quote_txt)
    SNG_QUOTE = re.compile(single_quote_txt)
    SNG_QUOTE_ABS = re.compile(single_quote_txt_absolute)
    BLANK_QUOTE_MARK = '§'
    DBL_QUOTE_SLASH = re.compile(r'\\[\"]+(?![\s\.\,\`]+)([^\\\"]+)\\[\"]+(?<!([\s\.\,]))')
    WORD_WITHOUT_QUOTE = re.compile(r'^[\'\"\*]*([^\'\"\*]+)[\'\"\*]*$')
    blank_quote_txt = r'(?<!\w)(\%s)([^\%s]+)(?:\b)(\%s)' % (BLANK_QUOTE_MARK, BLANK_QUOTE_MARK, BLANK_QUOTE_MARK)
    blank_quote_txt_abs = r'^%s(?:\W|$)?$' % (blank_quote_txt)
    BLANK_QUOTE = re.compile(blank_quote_txt)
    BLANK_QUOTE_ABS = re.compile(blank_quote_txt_abs)

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
    WORD_START_REMAIN = re.compile(r'^\w+', flags=re.I)
    WORD_END_REMAIN = re.compile(r'\w+$', flags=re.I)

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
    REF_FILLER_CHAR = '¢'
    ref_filler_char_pat_txt = r'[%s]+' % (REF_FILLER_CHAR)
    REF_FILLER_PAT = re.compile(ref_filler_char_pat_txt)

    FILLER_CHAR='¶'
    filler_char_pattern_str = r'[%s]+' % FILLER_CHAR
    FILLER_CHAR_PATTERN = re.compile(filler_char_pattern_str)

    filler_char_and_space_pattern_str = r'[%s\s]+' % (FILLER_CHAR)
    FILLER_CHAR_INVERT = re.compile(filler_char_and_space_pattern_str)

    filler_parts = r'\s?([%s]+)\s?' % (FILLER_CHAR)
    FILLER_PARTS = re.compile(filler_parts)

    filler_char_and_space_pattern_str = r'^[\s%s]+$' % FILLER_CHAR
    FILLER_CHAR_AND_SPACE_ONLY_PATTERN = re.compile(filler_char_and_space_pattern_str)

    filler_char_all_pattern_str = r'^[%s\s\W]+$' % FILLER_CHAR
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
    NON_SPACE_SYMBOLS = re.compile(r'[^\s\w\d]+')
    SYMBOLS = re.compile(r'[\W]+')
    UNDER_SCORE = re.compile(r'[\_]+')

    SPACES = re.compile(r'\s+')

    START_SPACES = re.compile(r'^\s+')
    END_SPACES = re.compile(r'\s+$')

    common_multi_word_connectors = r'[\s\-\,\/]'
    COMMON_WORD_SEPS = re.compile(common_multi_word_connectors)

    NOT_SYMBOLS = re.compile(r'[\w]+')
    SPACE_SEP_WORD = re.compile(r'[^\s]+')
    SPACE_SEP_WORD_AND_FSLASH = re.compile(r'[^\s\/]+')

    THE_WORD = re.compile(r'\bthe\b\s?', re.I)
    POSSESSIVE_APOS = re.compile(r'(\'s)\b')

    MULTI_SPACES = re.compile(r'[\s]{2,}')
    HYPHEN = re.compile(r'[\-]')
    SPACE_SEP = re.compile(r'\s')

    full_stop_in_middle = r'([\S][\.]\s[\S])'
    comma_in_middle = r'([\S]\,\s[\S])'
    punct_in_between_txt = r'(%s|%s)' % (full_stop_in_middle, comma_in_middle)
    PUNCT_IN_BETWEEN = re.compile(punct_in_between_txt)
    FULLSTOP_IN_BETWEEN = re.compile(full_stop_in_middle)

    ending_punct = r'(\w[\,\.!]+$)'
    ENDING_WITH_PUNCT = re.compile(ending_punct)

    basic_conjunctions = r'(for|to|is|are|was|were|and|nor|in|by|out|that|then|above|below|up|down|but|or|yet|so|etc(\W+)?)'

    basic_conjunctions_pat_txt = r'(\s|^)%s(\s|$)' % (basic_conjunctions)
    BASIC_CONJUNCTS = re.compile(basic_conjunctions_pat_txt)

    basic_conjunctions_only_pat_txt = r'^%s$' % (basic_conjunctions)
    BASIC_CONJUNCTS_ONLY = re.compile(basic_conjunctions_only_pat_txt)

    MAXWORD_UPTO_PAT = re.compile(r'^mx(\d+)$')

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

    BRACKET_OR_QUOTE_REF = re.compile(r'(_QUOTE|_BRACKET)')

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
             'ively', 'or', 'ors', 'iness', 'ature', 'er', 'en', 'ed', 'ied',
             'atures', 'ition', 'itions', 'itiveness',
             'itivenesses', 'itively', 'ative', 'atives',
             'ant', 'ants', 'ator', 'ators', 'ure', 'ures',
             'al', 'ally', 'als', 'iast', 'iasts', 'iastic', 'ial', 'y',
             'ary', 'ingly', 'ian', 'inal', 'ten'
             ],
            key=lambda x: len(x), reverse=True)),
        't': list(sorted(
            ['ce','cy', 'ssion', 'ssions', 'sion', 'sions'],
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
        '':list(sorted(
            ['ed', 'ly', ],
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

    NUMBERS = re.compile(r"^\s*(([\d]+)([\,\.]?[\s]?[\d]+)*)+$")

    REF_LINK_WITHOUT_REFWORD = re.compile(r'\<([^<]+)\>')
    PATH_CHAR = re.compile(r'[\\\/]')
    file_path_pattern_list=[
        #r'^$',
        r'^(([\w]+|[~\.]|[\.]{2})[:]?)?([/]([^\]+)?)+)$',
    ]

    DOS_COMMANDS = [
        "basica",
        "cd",
        "chdir",
        "chcp",
        "chkdsk",
        "cls",
        "comp",
        "ctty",
        "cv",
        "dblboot",
        "dblspace",
        "deltree",
        "dir",
        "diskcomp",
        "diskcopy",
        "doskey",
        "drvspace",
        "edlin",
        "emm386",
        "exe2bin",
        "fakemous",
        "fasthelp",
        "fastopen",
        "fc",
        "fdisk",
        "goto",
        "graftabl",
        "intersvr",
        "interlnk",
        "keyb",
        "loadfix",
        "loadhigh",
        "lh",
        "md",
        "mkdir",
        "mem",
        "memmaker",
        "msav",
        "msbackup",
        "mscdex",
        "msd",
        "msherc",
        "nlsfunc",
        "printfix",
        "qbasic",
        "rd",
        "rmdir",
        "recover",
        "rem",
        "ren",
        "setver",
        "smartdrv",
        "subst",
        "sys",
        "telnet",
        "truename",
        "ver",
        "vol",
        "vsafe",
        "xcopy",
    ]

    STB = r'[\"\'\(\<\{\[]'
    EDB = r'[\"\'\)\>\}\]]'
    # NUMB = r'([+-]?[\d]+(([\.\,][\d]+)*)+[\W]?)'
    NUMB = r"[+-]?[\d]+([\.\,][\d]+)?"
    # PATH = r'(([a-zA-Z][:]?)?) ([\\\/]+)(([\w-dd]+)?)*)'
    PATH = r'([a-zA-Z][:]?)?'
    MATH_OPS = r'[\s]?([\+\-\*\/\%\=x])[\s]?'
    runtime_ignore_list = None
    ignore_list = [
        r'^[\W\d]+$',   # symbols and numbersr
        # r'([\.](org|com|uk|ac))$',
        # r'^(([\.]([\/][^\w]?[\w]+[^\w]?)+[\/]?)+([\s][\.]+)?)$', #``./datafiles/locale/{language}/``
        r'^(GPL[\s\w][\d][+])$',
        r'^(A \(Alpha\))$',
        r'^(\w+\d+)$',
        r'^[\w]\s?(\+|\-|\*|\/|\%|\=|\!\=|\>|\<|\>\=|\<\=|\=\=|\>\>|\<\<)\s?[\w]$', # A - B, A >= B
        # r'^(:[\w]+:)([\`]+([\/][\w]+[\/]?)*[\`]+)', # :doc:`/something/somethingelse`
        r'^(:ref:)([\`]+(\w+[-]?)+[\`]+)[\.]?$',
        r'^(:kbd:[\`]((Shift|Alt|Ctrl|\-)*([^\`]{1}|F(\d+)))[\`](,\s|\s-\s)?)+$', #:kbd:`Shift-Ctrl-R`
        r"^\s*([\d]+)(px|khz)?$", # 1024x2048
        r"^\s*([\d]+[x][\d]+)\s*$", # 1024x2048
        r'^(\|[\w]+([\-][\w]+)?.*(:kbd\:.*Alt-Backspace).*)$',  # |dagger|: ``|``, :kbd:`Alt-Backspace`, ``-``
        r"^\s*([\d]+\s?bit[s]?)\s*$",
        r"^\s*(" + NUMB + MATH_OPS + r".*" + NUMB + r")\s*$",
        r"^\s*(" + r"(cd|mk|mkdir)[\s]+" + r".*" + r")\s*$",
        r"^\s*(" + STB + r"?([\+\-]?[\d]+[\W]?)" + EDB + r"?)\s*$",  # (+-180°)
        r"^\s*(" + STB + r"?(" + NUMB + r"(([\,]+[\s]+)?" + NUMB + r")*)+" + EDB + r"?)\s*$", # (-1.0 - 1.0), (-X, -Y, -Z, X, Y, Z)
        r"^\s*(\*\-[\d]+[\.][\w]{3})\s*$", #*-0001.jpg
        r"^\s*(Bone[ABC]|COR\-|Cartesian|Bfont|ABC)\s*$",
        r"^\s*(F[\d]{1,2})\s*$", # F1-12
        r"^\s*([\w]([\s]+[\w\d])+)\s*$", # :kbd:`S X 0`
        r"^\s*(([\d]+(\.[\d]+)?)([\s]?[\/\+\-\*\%\=]?[\s]?([\d]+(\.[\d]+)?))*)\s*$",
        r"^\s*([\W]+)\s*$",
        r"^\s*([-]{2}([\w-]+)*)\s*$",
        r"^\s*([\"\'\*]?[\d]+(\.[\d]+)?([\s]?([K]?hz|bit[s]?))?[\"\'\*]?)\s*$",
        r"^\W?(\dD)\W?$",
        r"^\s*([\"\'][\.\s]?[\S]{1}[\"\'])\s*$",
        r"^\s*(#fmod\(frame, 24\) / 24)\s*$",
        r"^\s*(([\w]+)?([\.][\w]+)+)\s*$", # bpy.context, bpy.context.object
        r"^\s*(:(math|class):)\`([^\`]+)\`$",
        r"^\s*(ITU \d+,)+",
        r"^\s*(" + STB + r"?[+-][\w]{1}[,.])*([\s]?[+-][\w]{1})" + EDB + r"?$",  # "+X, +Y, +Z, -X, -Y, -Z"
        r"^\s*([^\S]{1})\s*$",  # single anything non spaces
        r"^\s*(" + STB + r"?([+-]?[\d]+)([\,\.]?[\s]?[\d]+)*)+" + EDB + r"?$",  # 1,000 or 0.00001 or 1, 2, 3, 4
        r"^\s*([\d]+[.,][\s]?)*[\d]+bit$",
        # r"^\s*([\d]?[\w]{1})\s*$",  # "4D"
        r"^\s*([\w\d]{2}\:){2}[\w\d]{2}\.[\w\d]{2}\.$",  # HH:MM:SS.FF
        r"^\s*(\.[\w]{2,5})\s*$",  # .jpg, .so
        r"^\s*(htt[ps][^\S]+)\s*$",
        r"^\s*(jpg|png|int)\s*$",
        r"^\s*(\-\-render\-frame 1|\-(ba|con|noaudio|setaudio)|Mem)\s*$",
        r"^\s*(([\d]+([\.[\d]+)?)*(mil|mi|mm|km|cm|ft|m|yd|dm|st|pi))\s*$",
        r"^\s*(mov|location[0]|cd|ch|hm|asin|um|tan|atan|atan2|Arctan2|motorsep)\s*$",
        r"^\s*(AAC|AVI Jpeg|AVX|AaBbCc|Albedo|Alembic|AC3|Alt|AMD|Ascii|AVX[\d]?|Acrylic)\s*$",
        r"^\s*Alembic([\s\W|abc]+)\s*$",
        r"^\s*(Alpha|Alt|Apple macOS|Arch Linux|Ashikhmin-Shirley)\s*$",
        r"^\s*(AVIJPEG|AVIRAW|BMP|DDS|DPX|IRIZ|JACK|JP2|RAWTGA|TGA|TIFF|[+-]<frame>|)\s*$",
        r"^\s*(B\-Spline|BSDF|BSSRDF|BU|BVH|Babel|Bezier|Bindcode|Bit[s]?|BkSpace|Bksp)\s*$",
        r"^\s*(Blackman\-Harris|Blosc|Barth|Byte\([s]*\)|curv(\w+)\-(bezier|nurbs|POLYLINE)|Bytecode|Bézier|Backspace|(Blender\s(\d+[\d\.]+)))\s*$",
        r"^\s*Blender\([\s\d\.]+\)|Blender_id[\W]?|build\/html$",
        r"^\s*(Catmull\-(Clark|Rom)|Catrom|Chebychev|Clemens|Christensen\-Burley|Cineon|Collada)\s*$",
        r"^\s*(Cycles|Cycles:|Cinema(\s\(\d+\))?)\s*|(command_line-args)$",
        r"^\s*(DNxHD|DOF|Debian\/Ubuntu|Del|de|debian|Delta([\s][\w])?)\s*$",
        r"^\s*([^\w]+log.*wm.*)\s*$",
        r"^\s*(Djv|Doppler|Dots\/BU|Dpi|DWAA)\s*$",
        r"^\s*(EWA|Epsilon|Embree|Esc|exr|FBX|Euler|FELINE|FFT|FSAA|Flash|FrameCycler|Français|msgfmt|fr_FR|Enter|Euler\s?\(?\w{1,3}?\)?|Float[\d]?)\s*$",
        r"^\s*((GGX|GLSL|GPU)[s:]|Gamma[s:]?|Ge2Kwy5EGE0|Gizmo[s:]|GGX|GLSL|Gizmo[\s]?[\w]?)\s*$",
        r"^\s*(H\.264|Hosek \/ Wilkie|Houdini|HuffYUV|Hyperbolic[\s]?(Sine|Cosine)|Hosek \/ Wilkie(\s\d+)?|HDRI[s]?)\s*$",
        r"^\s*(ID|Ins|JPEG 2000|(ITU(\s\d+)?)|Internet[\w\W]|iScale)\s*$",
        r"^\s*(KDE|K1, K2|Kirsch|komi3D)\s*$",
        r"^\s*(Lennard\-Jones|LimbNode|Laplace Beltrami|Lightwave Point Cache \(\.mdd\)|Linux|Log|Look[\s]?Dev(HDRIs)?)\s*$",
        r"^\s*MPEG([\-|\d]+)|MPEG H.264|MPEG-4\(DivX\)|MatCaps$",
        r"^\s*(MIS|MPlayer|(MS|Microsoft)?[-]?Windows|MacBook [\`]+Retina[\`]+|Makefile|Makefile|Manhattan|Matroska|Mega|Minkowski(\s[\d]+)?|Minkowski \d+\/\d+|Mitch|Mono|Musgrave)\s*$",
        r"^\s*(NDOF((\W)|[\s]?(ESC|Alt|Ctrl|Shift))?|hardware-ndof|NURBS|Nabla|Ndof|Nabla|Null|NVIDIA|nn|Nishita)\s*$",
        r"^\s*(OBJ|OSkey|Ogawa|Ogg[\s]?(Theora)?|Open(AL|CL|EXR|MP|Subdiv|VDB)+|Opus|ObData|ILM\'s OpenEXR|OpenEXR|Ozone|OptiX)\s*$",
        r"^\s*PAINT_GPENCILEDIT_GPENCILSCULPT_.*$",
        r"^\s*(P(CM|LY|NG)|Pack Bits|Poedit|Preetham|Prewitt|PBR|PolyMesh|PO|pip|pip3|PIZ|PXR24|pc2|Preetham(\s?\d+)?|Python(\:\s[\.\%s]+)?)\s*$",
        r"^\s*(QuickTime|quasi\-)\s*$",
        r"^\s*(\d+[x]?)\s*$", # 16x
        r"^\s*(\%\d+[\w]?)\s*$", # %14s
        r"^\s*(\%[d](x%[d])?)\s*$", # %dx%d
        r"^\s*\%d(\s\w\s\%d)?(\W\s?)?$", # %d x %d
        r"^\s*(RONIN|Ryan Inch|Return)\s*$",
        r"^\s*(RK4|RRT|Redhat\/Fedora|RLE)\s*$",
        r"^\s*(SDL|SSE[\d]+|STL|SVG|ShaderFX|Sigma|Sin|Sobel|Sobol|Stucci|Studio|Subversion|setmessage|SubD|Subdiv|Silvio Falcinelli)\s*$",
        r"^\s*(Targa([\s]?Raw)?|Theora|TortoiseSVN|TxtIn|test1_|the|TAR-)\s*$",
        r"^\s*(URL|UV[s:]?|(\w )?&( \w)?|Uber)\s*$",
        r"^\s*(VD16|VP9|VRML2|Verlet|Vorbis|Voronoi([\s]F[\d]([-]F[\d])?)?|)\s*$",
        r"^\s*(WEBM \/ VP9|Web(3D|M)|Win(tab)?|Windows Ink|WGT-|ZX)\s*$",
        r"^\s*(X(/Y|YZ)?|Xvid|XY|XZ|YCbCr(\s\(ITU\s?\d+?\))?)\s*$",
        r"^\s*(Y(CC)?|YCbCr(\s\(Jpeg\))?|Z(ip)?|ZIPS)\s*$",
        # r"^\s*(\w+(_\w+)+)\s*$", # MASK_MT_add
        r"^\s*[\-]*\d+(\.[\w]{2,5})\s*$",  # -0001.jpg
        r"^\s*[\W]{1}$",
        r"^\s*\w([\s]?[<]?[\*\/\+\-\=][>]?[\s]?\w)+\s*$",  # A * B + C; A -> B
        r"^\s*(\"fr\"[:]?|\"fr\": \"Fran&ccedil;ais\"|)\s*$",
        r"^\s*\*(\.[\w]{2,5})\s*$",  # *.jpg
        r"^\s*\.bashrc$",
        r"^\s*(the quick|brown fox|jumps over|the lazy dog)\s*$",
        r"^\s*\:([\w\-\_]+)\:$",
        r"^\s*\:sup\:\`™\`$",
        r"^\s*\|([\w\-\_]+)\|$",
        r"^\s*\|[^\|]+\|$",  # |tick|cross|
        r"^blender_api[:]?",
        r"^\s*(bItasc|bin|bit[s]?|bl\*er|blendcache_[filename]|blender_doc|blender_api)\s*$",
        r"^\s*(bpy\.(context|data|ops)|bpy\.([\w\.\-\_]+)|byte([s]?))\s*$",
        r"^\s*(cd|mkdir|ctrl)\s*$",
        r"^\s*(dam|deg|developer\.blender\.org|dir\(\)|dm|dx)\s*$",
        r"^\s*(eevee|emission\(\)|esc|etc[\.]+)\s*$",
        r"^\s*(f\(\d+\)|fBM|flac|fr|fr\/|ft)\s*$",
        r"^\s*gabhead, Lell, Anfeo, meta-androcto$",
        r"^\s*(git([\s]+[^\`]+)?|glTF 2\.0)\s*$",
        r"^\s*(hm|html|iTaSC|jpeg|SubRip)\s*$",
        r"^\s*[\%s\s\'\:]+$", # %s: %s
        r"^\s*(kConstantScope|kUniformScope|kUnknownScope|kVaryingScope|kVertexScope|kFacevaryingScope|kbd)\s*$",
        r"^\s*(mathutils|menuselection|microfacet_ggx\(N, roughness\)|microfacet_ggx_aniso\(N, T, ax, ay\))\s*$",
        r"^\s*(microfacet_ggx_refraction\(N, roughness, ior\)|mp[\d]+|msgstr|MPEG-4 \(divx\))\s*$",
        r"^\s*(oren_nayar\(N, roughness\)|wm\.operators\.\*|var all_langs \=(.*)|)\s*$",
        r"^\s*(Poedit|PIP|pagedown|pageup|pgdown|pgup|pip[\d]?|pot|print\(\))\s*$",
        r"^\s*(quit\.blend|path:ray_length|render\-output\-postprocess|temp\-dir)\s*$",
        r"^\s*(rig_ui|roaoao|rotation_[xyz]|resolution_[xyz]|reflection\(N\)|rest_mat|rst|refraction\(N, ior\))\s*$",
        r"^\s*(_socket[\.](py|pyd)|Subversion|s\-leger|sequencer\-edit\-change|sqrt|sqrt\([\d]?\)|svn)\s*$",
        r"^\s*(TortoiseSVN|timeline\-playback|ui\-data\-block|view3d\-viewport\-shading|var[\s]+|wav)\s*$",
        r"[\d]+([\.][\d]+[\d\w]?)\s[\-]+\s(Tháng|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)",
        r"^(\w[\W]+)$",
        ]

    # MAKE SURE all entries in this table are in LOWERCASE
    ignore_txt_list = [
        "\"agent\"",
        "yadif",
        "ui-eyedropper",
        "ui_template_list diff",
        "translucent(N)",
        "topbar-app_menu",
        "topbar-render",
        "top -o %MEM",
        "top -o MEM",
        "tool-annotate",
        "svn add /path/to/file",
        "svn rm /path/to/file",
        "sudo nano /etc/paths",
        "supported platforms",
        "sin(x)/x",
        "sid",
        "sculpt_mask_clear-data",
        "screw spring example.blend",
        "screw hardware example.blend",
        "quaternion",
        "prefs-index",
        "prefs-menu",
        "object-proxy",
        "manual/images",
        "material:index",
    ]

# , ""
    ignore_start_with_list = [
        # "bpy", "bpy", "bl_info", "dx",
        #"", "", "", "", "",
        # "", "", "", "", "", "", "", "", "", "", "", "", "",
        "MPEG-4(DivX)",
        "demohero, uriel, meta-androcto",
        "antonio vazquez (antonioya)",
        "vladimir spivak (cwolf3d)",
        "nuke (.chan)",
        #"a (alpha)",
        "(*x*\\ :sup:",
        "0 + (cos(frame / 8) * 4)",
        #"+x, +y, +z, -x, -y, -z",
        #"",
        #"",
    ]

    keep_list = [
        "switching/enabling/disabling",
        "toggle/enable/disable",
        "cycles only",
        "yellow/green/purple",
        "/base",
        "_right",
        "_left",
        "vertices/edges/faces",
        "(translation/scale/rotation)",
        "translation/scale/rotation",
        "path/curve-deform",
        "a",
        "an",
        "etc",
        "etc.",
        "e.g",
        "e.g.",
        "i.e",
        "i.e.",
        "add-on",
        "off-axis",
        "toe-in",
        "sub-target",
        "foam + bubbles",
        "spray + foam + bubbles",
        "fire + smoke",
        "sub-steps",
        "z-axis",
        "normal/view"
        "f-curve",
        "f-modifier",
        "counter-clockwise",
        "normal/surface",
        "left/right",
        "top/bottom",
        "link/append",
        "fog/mist",
        "exterior/interior",
        "flat/smooth",
        "mirror%s",
        "un-subdivide",
        "un-comment",
        "shrink/fatten",
        "smoke + fire",
        "expand/contract",
        "open/close",
        "hide/show",
        "co-planar",
        "hide/unhide",
        "lock/unlock",
        "major/minor",
        "click-extrude",
        "front/back",
        "rotation/scale",
        "blender_version",
        "mpeg preseek",
        "0 or 1",
        "anti-aliases",
        "anti-aliased",
        "anti-aliasing",
        "marker-and-cell grid",
        "reflect/refract",
        "scattering/absorbtion",
        "inside/outside",
        "dots/bu",
        "model by © 2016 pokedstudio.com",
        "video: from blender 1.60 to 2.50",
        "right-click-select",
        #"",
        #"",
    ]

    reverse_order_list = [
        r'khóa.*[\d]+(\s[\-]{2}\s(key))',
        r'\"cơ sở -- basis\"',
        r'^\"xương -- bone\"$',
        r'^\"xương\"$',
        r'^\"bone\"$',
        r'xương\.[\d]+',
        r'bone\.[\d]+',
    ]

    keep_contains_list = [
        "i.e.",
        "etc.",
        "/etc",
        "e.g.",
        "xương",
        "bone",
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "novemeber",
        "december",
        "|first|",
        "|previous|",
        "|rewind|",
        "|play|",
        "|next|",
        "|last|",
        "|pause|",
        "hh:mm:ss.ff",
        # "",
        # "",
    ]

    symbol_splitting_pattern_list = [
        NON_SPACE_SYMBOLS,
        SYMBOLS,
        UNDER_SCORE,
    ]

    keep_contains_list.sort()
    keep_list.sort()

    pattern_list = [
        (ARCH_BRAKET_SINGLE_FULL, RefType.ARCH_BRACKET),
        (PYTHON_FORMAT, RefType.PYTHON_FORMAT),
        (FUNCTION, RefType.FUNCTION),
        (AST_QUOTE, RefType.AST_QUOTE),
        (DBL_QUOTE, RefType.DBL_QUOTE),
        (SNG_QUOTE, RefType.SNG_QUOTE),
        (BLANK_QUOTE, RefType.BLANK_QUOTE),
        (ATTRIB_REF, RefType.ATTRIB),
        (GA_REF, RefType.GA),
    ]

    pattern_list_absolute = [
        ARCH_BRAKET_SINGLE_ABS,
        PYTHON_FORMAT_ABS,
        FUNCTION_ABS,
        AST_QUOTE_ABS,
        DBL_QUOTE_ABS,
        SNG_QUOTE_ABS,
        BLANK_QUOTE_ABS,
        ATTRIB_REF_ABS,
    ]

class SentStructModeRecord:
    def __init__(self, smode_txt=None, smode=None, extra_param=None):
        self.smode_txt: str = smode_txt
        self.smode: SentStructModeRecord = smode
        self.extra_param = extra_param

class SentStructMode(Enum):
    ANY = Definitions.ANY
    EXCLUDE = Definitions.EXCLUDE
    NOT_TRAILING = Definitions.NOT_TRAILING
    NOT_LEADING = Definitions.NOT_LEADING
    EQUAL = Definitions.EQUAL
    TRAILING_WITH = Definitions.TRAILING_WITH
    LEADING_WITH = Definitions.LEADING_WITH
    EMBEDDED_WITH = Definitions.EMBEDDED_WITH
    PATTERN = Definitions.PATTERN
    NUMBER_ONLY = Definitions.NUMBER_ONLY
    POSITION_PRIORITY = Definitions.POSITION_PRIORITY
    ORDERED_GROUP = Definitions.ORDERED_GROUP
    NO_PUNCTUATION = Definitions.NO_PUNCTUATION
    MAX_UPTO = Definitions.MAX_UPTO
    NO_CONJUNCTIVES = Definitions.NO_CONJUNCTIVES
    NO_FULL_STOP = Definitions.NO_FULL_STOP

    @classmethod
    def getName(cls, string_value: str):
        for name, member in cls.__members__.items():
            is_any = (member == cls.ANY)
            if is_any:
                continue

            is_match = (member.value.search(string_value) is not None)
            if bool(is_match):
                return member
        return cls.ANY
