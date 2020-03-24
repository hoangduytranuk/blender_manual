#_("Common imported")
import html #for escaping html
import os
import re
import inspect
import copy as cp

from pprint import pprint
#from Levenshtein import distance as DS

DEBUG=False

# class cmMatchGroup:
#     def __init__(self, parent=None, start=-1, end=-1, txt=None):
#         self.parent = parent
#         self.start = start
#         self.end = end
#         self.text = txt
#
# class cmMatch:
#     def __init__(self, txt=None, pattern=None, match_group=None):
#         self.orig_text = txt
#         self.pattern = pattern
#         self.match = match_group
#         self.subgroups = []
#
#     def appendSubGroup(self, ss, ee, txt):
#         g = cmMatchGroup(parent=self, start=ss, end=ee, txt=txt)
#         self.subgroups.append(g)
#
#     def hasSubGroup(self):
#         has = (self.subgroups is not None) and (len(self.subgroups) > 0)
#         return has


def refListGetKey(item):
    return item[0]

def pp(object, stream=None, indent=1, width=80, depth=None, *args, compact=False):
    if DEBUG:
        pprint(object, stream=stream, indent=indent, width=width, depth=depth, *args, compact=compact)
        print('-' * 30)

def _(*args, **kwargs):
    if DEBUG:
        print(args, kwargs)
        print('-' * 30)

class Common:
    debug_current_file_count = 0
    debug_max_file_count = 5
    debug_file = None
    #debug_file = "troubleshooting/gpu/common/other"
    debug_file = "animation/armatures/bones/editing/bones"
    #debug_file = "sculpt_paint/sculpting/tool_settings/symmetry"

    visitor = None
    trans_finder = None
    print_html = False
    COMMENT="#"
    MSGID="msgid"
    MSGCTXT="msgctxt"
    MSGSTR="msgstr"
    SPACE=" "
    QUOTE="\""
    NEWLINE = os.linesep
    FUZZY="#, fuzzy"
    DOT="."
    HYPHEN="-"
    COLLON=":"
    DASH="-"
    PO_EXT=".po"
    RST_EXT=".rst"
    COMMENTED_LINE="\#\~"
    KEYBOARD=":kbd:"
    FUZZY="#, fuzzy"
    B_SLASH='\\'
    PERCENTAGE="%"
    STAR="*"
    BLEND_FILE=".blend"
    COLON=":"
    TODO_LOWER=r"\btodo\b"
    TODO_TRANSLATED="Nội dung cần viết thêm"

    RE_COMMENTED_LINE = "^\#\~"
    RE_COMMENT="^#"
    RE_COMMENT_UNUSED="#~"
    RE_MSGID="^msgid"
    RE_MSGCTXT="^msgctxt"
    RE_MSGSTR="^msgstr"
    RE_EMPTYSTR=""
    RE_TWO_MORE_RETURN="{}{}".format(os.linesep, os.linesep)
    RE_ONE_RETURN="{}".format(os.linesep)
    RE_LEADING_SPACES = "^[\ |\t]+?"
    RE_RST_UNDERLINED = "^[\#|*|=|\-|^|\"]+?$"
    RE_RST_SPECIAL = "^[\.|:|`|\#]+?"
    RE_IS_ALPHA = "^[A-Za-z]+.*$"
    RE_LEADING_HYPHENS="^(-- ).*$"
    RE_ENDING_DOT="^(.*?)\.$"
    RE_KEYBOARD="(:kbd:`)(.*?)(`)"
    RE_NUMBER="\d+"
    RE_BRACKET=r"[\(\[\{]+"
    RE_XXX=r".*X{3}.*"
    RE_DOTDOT=r".*\.\..*"
    RE_HYPHEN=r".*\-.*"
    RE_XRAY=r".*X-Ray.*"
    RE_DD=r".*([23][Dd]).*"
    RE_REF=":ref:"
    RE_MENU=":menuselection:"
    RE_URL="http"
    RE_MOUSE_BUTTON="[(RMB)+|(LMB)+|(MMB)+]"
    RE_DOC=":doc:"
    RE_SECTION_TITLE=r"(msgstr \")([\ ]*)(-- )"
    RE_TODO=r"(\btodo\b)"
    RE_QUOTED_WELL=r"^\"(.*)\"$"
    RE_QUOTED_STRING = "(?P<quote>['\"])(?P<string>.*?)(?<!\\)(?P=quote)"
    RST_SUB_PARA=r"([\.]{2})\s(\w+)[:]{2}\s(.*)"


    QUOTED_STRING_RE = re.compile(r"(?P<quote>['\"])(?P<string>.*?)(?<!\\)(?P=quote)")
    QUOTED_CHAR_RE = re.compile(r"(?P<quote_char>['\"])")
    SECTION_TITLE_RE= re.compile(r"(^\")([\ ]*)(-- )")
    #SECTION_TITLE_RE= re.compile(r"msgstr")

    DQ=re.compile(r"(?P<double_quote>[\"])(?P<string>.*?)(?<!\\)(?P=double_quote)")
    SQ=re.compile(r"(?P<single_quote>['])(?P<string>.*?)(?<!\\)(?P=single_quote)")

    DC=re.compile(r"(?P<dquote_char>[\"])")
    SC=re.compile(r"(?P<squote_char>['])")
    NUMBER=re.compile(r"^[+-]?\d+([\.\,]?\d)*$")
    FILTER_RST_BOX=re.compile(r"(?P<rst_box>[\`]+)(.*?)(?P=rst_box)$")
    OPTION=re.compile(r"(^[-]+)([a-zA-Z0-9]{0,1})$")
    NON_ALPHA=re.compile(r"^([^\d\w]+)$")
    MNUSEL= re.compile(r":menuselection:`(.*)`")
    PURE_DOC_PATH= re.compile(r"(?<=:doc:`\/)(.*)`$")

    KEYBOARD = re.compile(r":kbd:`.*`")
    WORD_SEP = re.compile(r"([^\W]+)") #exclude non word characters
    SINGLE_KEY_KEYBOARD_DEF = re.compile(r":kbd:`(?P<single_key>(([\w])|(Tab)){1})|(((?P<modifier>(Alt)|(Ctrl)|(Shift))-)+(?P=single_key))*`")

    KEYBOARD_DEF=re.compile(r":kbd:`[^`]*`")
    ONLY_KEYBOARD_DEF = re.compile(r"^:kbd:`[^`]*`$")
    SPECIAL_DEF = re.compile(r"((Wheel)|(Numpad)|(MMB)|(LMB)|(RMB)|(Period))")
    ENDING_WITH_PUNCTUATIONS = re.compile(r"([\W]{1,1})$")
    RESOLUTION=re.compile(r'^(\d)+px$')
    KHZ = re.compile(r'^(\d)+(\.(\d)+)*([\ |k])*hz$', flags=re.I)

    #p1=re.compile(r":kbd:`(?P<key>[\w\d]+)|(?P<modifier>(Enter|Ctrl|Alt|Shift|Home|Insert|PageUp|PageDown|Delete)+[-+](?P=key))*`")
    pex_vn_part=re.compile(r"(NCT)|(NCP)|(NCG)|(LMB)|(MMB)|(RMB)|(Numpad)|(Wheel)|(OS)")
    pdel=re.compile(r"(\.)|(,)|(;)|(and)|(or)|(--)")

    RST_HEADER=["#", "*", "=", "-", "^", "\""]

    end_char_list=set(['.','!',')', ',', '>', ':','*','`',])
    COMMENT_FLAG="#: "
    LANGUAGE_SEPARATOR=" -- "

    KEYBOARD_TRANS_DIC={
        r"\bWheelUp\b":"Lăn Bánh Xe về Trước (WheelUp)",
        r"\bWheelDown\b":"Lăn Bánh Xe về Sau (WheelDown)",
        r"\bWheel\b":"Bánh Xe (Wheel)",
        "NumpadPlus":"Dấu Cộng (+) Bàn Số (NumpadPlus)",
        "NumpadMinus":"Dấu Trừ (-) Bàn Số (NumpadMinus)",
        "NumpadSlash":"Dấu Chéo (/) Bàn Số (NumpadSlash)",
        "NumpadDelete":"Dấu Xóa/Del Bàn Số (NumpadDelete)",
        "NumpadPeriod":"Dấu Chấm (.) Bàn Số (NumpadDelete)",
        "Numpad0":"Số 0 Bàn Số (Numpad0)",
        "Numpad1":"Số 1 Bàn Số (Numpad1)",
        "Numpad2":"Số 2 Bàn Số (Numpad2)",
        "Numpad3":"Số 3 Bàn Số (Numpad3)",
        "Numpad4":"Số 4 Bàn Số (Numpad4)",
        "Numpad5":"Số 5 Bàn Số (Numpad5)",
        "Numpad6":"Số 6 Bàn Số (Numpad6)",
        "Numpad7":"Số 7 Bàn Số (Numpad7)",
        "Numpad8":"Số 8 Bàn Số (Numpad8)",
        "Numpad9":"Số 9 Bàn Số (Numpad9)",
        "Spacebar":"Dấu Cách (Spacebar)",
        r"\bDown\b":"Xuống (Down)",
        r"\bUp\b": "Lên (Up)",
        r"\bComma\b": "Dấu Phẩy (Comma)",
        r"\bMinus\b": "Dấu Trừ (Minus)",
        r"\bPlus\b": "Dấu Cộng (Plus)",
        "Left": "Trái (Left)",
        "=": "Dấu Bằng (=)",
        "Right": "Phải (Right)",
        "Backslash": "Dấu Chéo Ngược (Backslash)",
        r"\bSlash\b": "Dấu Chéo (Slash)",
        "AccentGrave": "Dấu Huyền (AccentGrave)",
        "Period":"Dấu Chấm (Period)",
        "PageDown":"Trang Xuống (PageDown)",
        "PageUp":"Trang Lên (PageUp)",
        "PgDown":"Trang Xuống (PgDown)",
        "PgUp":"Trang Lên (PgUp)",
        "OSKey": "Phím Hệ Điều hành (OSKey)",
        "NumpadSlash": "Dấu Chéo Bàn Số (NumpadSlash)",
        "MMB":"NCG (MMB)",
        "LMB":"NCT (LMB)",
        "RMB":"NCP (RMB)",
        "Pen": "Bút (Pen)"
    }

    ignore_list=[
        "(htt)([ps]{1}).*",
        # "(Euler)+(\ \([A-Z]+\))*",
        # "([A-Z]+\ \-\>\ [A-Z]+)",
        # "(sin|cos|tan|arcsin|arccos|arctan)+(\(A\)|2)+",
        # "[\W|dsx\sYZ]+",
        # "(\W+\d+)(g fps)",
        # "\, RGB([A]*) byte",
        # "A(\ [\W|mod]+\ )*B",
        "Poedit",
        "^([.*]{1})$", #single anything
        "bpy\.([\w\.\-\_]+)",
        "^\:([\w\-\_]+)\:$",
        "^\|([\w\-\_]+)\|$",
        "^[\W]{1}$",
        "Diffusion",
        "Subversion",
        "LookDev HDRIs",
        "AVI Jpeg",
        "AVX",
        "AVX2",
        "AaBbCc",
        "Acrylic",
        "Albedo",
        "Alembic",
        "Alembic([\s\W|abc]+)*",
        "PAINT_GPENCILEDIT_GPENCILSCULPT_.*",
        "Alpha",
        "Alt",
        "Apple macOS",
        "Arch Linux",
        "Ascii",
        "Ashikhmin-Shirley",
        "B-Spline",
        "BSDF",
        "BSSRDF",
        "BU",
        "BVH",
        "Bezier",
        "Bindcode",
        "Bit",
        "Bits",
        "BkSpace",
        "Bksp",
        "Blackman-Harris",
        "Blender([\ \d\.]+)",
        "Blosc",
        "Boolean",
        "Byte([s]*)",
        "Bytecode",
        "Bézier",
        "CPU",
        "CUDA",
        "Catmull-Clark",
        "Catmull-Rom",
        "Catrom",
        "Chebychev",
        "Christensen-Burley",
        "Cineon",
        "Collada",
        "Ctrl",
        "Cycles",
        "Cycles:",
        "DNxHD",
        "DOF",
        "Debian/Ubuntu",
        "Deflate",
        "Del",
        "Del",
        "Delta",
        "Delta( \w)*",
        "Djv",
        "Doppler",
        "Dpi",
        "Dots/BU",
        "EWA",
        "Epsilon",
        "Esc",
        "FELINE",
        "FFT",
        "FSAA",
        "Flash",
        "FrameCycler",
        "GGX",
        "GGX",
        "GLSL",
        "GPU([s|:])*",
        "GPUs",
        "Gamma([s|:])*",
        "Gizmo( \w+)",
        "Gizmo([s|:])*",
        "H.264",
        "HDR(I)*",
        "HSV/HSL",
        "Hosek \/ Wilkie",
        "HuffYUV",
        "ITU (\d+)",
        "Ins",
        "Ins",
        "JPEG( \d+)*",
        "K1, K2",
        "Kirsch",
        "Laplace",
        "Laplacian",
        "Laptops",
        "Lennard-Jones",
        "LimbNode",
        "Linux",
        "Log",
        "Look Dev",
        "LookDev",
        "MIS",
        "MPEG([\-|\d]+)*(.*)",
        "MPlayer",
        "MS-Windows",
        "Manhattan",
        "MatCap",
        "MatCaps",
        "Matroska",
        "Mega",
        "Microsoft Windows",
        "Minkowski.*",
        "Mitch",
        "Mono",
        "Musgrave",
        "NDOF",
        "NURBS",
        "Nabla",
        "Ndof.*",
        "Null",
        "OBJ",
        "OSkey",
        "Ogawa",
        "Ogg Theora",
        "Ogg",
        "OpenAL",
        "OpenCL",
        "OpenEXR",
        "OpenGL",
        "OpenMP",
        "OpenSubdiv",
        "OpenVDB",
        "Opus",
        "PLY",
        "PYTHONPATH",
        "Pack Bits",
        "Page Down",
        "Page Up",
        "Pause",
        "Pause",
        "Preetham",
        "Prewitt",
        "Python",
        "QuickTime",
        "RGB(\w)*",
        "RK4",
        "RRT",
        "Redhat/Fedora",
        "SDL",
        "SSE2",
        "SSE3",
        "SSE41",
        "STL",
        "SVG",
        "ShaderFX",
        "Shift",
        "Sigma",
        "Sigma",
        "Sin",
        "Sobel",
        "Sobol",
        "Stucci",
        "Studio",
        "Tab",
        "Targa Raw",
        "Targa",
        "Theora",
        "TxtIn",
        "URL",
        "UV",
        "UVs",
        "Uv:",
        "VD16",
        "VRML2",
        "Verlet",
        "Vorbis",
        "Voronoi F([\d]+)?(\-F([\d]+))*",
        "Voronoi",
        "WEBM / VP9",
        "Web3D",
        "WebM",
        "Win",
        "Windows Ink",
        "Wintab",
        "ID",
        "X",
        "X/Y",
        "XYZ",
        "Xvid",
        "Y",
        "YCC",
        "YCC",
        "YCbCr (ITU 601)",
        "YCbCr (ITU 709)",
        "YCbCr (Jpeg)",
        "YCbCr",
        "YCbCr.*",
        "Z",
        "Zip",
        # "[X|Y]( \d+)",
        # "\W+(\d+)*(\W+)*", #only symbols
        # "\d+([k]*Hz)*",
        # "\d+(x)*", #16x
        # "\d{1}D",
        # "\s+%\s+[A-Z]+",
        "ac3",
        "alt",
        "bItasc",
        "bit",
        "bits",
        "bpy.context",
        "bpy.data",
        "bpy.ops",
        "byte([s]?)",
        "ctrl",
        "dx",
        "eevee",
        "esc",
        "f(\d+)",
        "fBM",
        "flac",
        "glTF 2.0",
        "iTaSC",
        "kbd",
        "macOS",
        "menuselection",
        "mp(\d+)",
        "Makefile",
        "pagedown",
        "pageup",
        "pgdown",
        "pgup",
        "sin\(x\)\ \/\ x",
        "tab",
        "wav",
        "blender_docs",
        "pip3",
        "pip",
        "FBX",
        "fr",
        "fr/",
        "^\|[^\|]+\|$",  # |BLENDER_...|
        # "\:[^\|]+\:",  # :linenos:
        "^#[\w\-\_]+", #blender-coders <literal>#blender-coders</literal>
        "Babel",
        "Ge2Kwy5EGE0",
        "([\+\-])*(([\d\.]+))", #simple number
        "TortoiseSVN",
        "Poedit",
        "\:sup\:\`™\`",
        "^(([\w]+)\.([^\.]+))+$",
        "rst",
        "pot",
        "html",
        "^svn$",
        "^git$",
        "msgstr",
        "^\.bashrc$",
        "^bin$",
        "Français",
        "Redhat/Fedora",
        "Arch Linux",
        "\"fr\": \"Fran&ccedil;ais\"",
        ]

    DOS_COMMANDS=[
        "BASICA",
        "CD",
        "CHDIR",
        "CHCP",
        "CHKDSK",
        "CLS",
        "COMP",
        "CTTY",
        "CV",
        "DBLBOOT",
        "DBLSPACE",
        "DELTREE",
        "DIR",
        "DISKCOMP",
        "DISKCOPY",
        "DOSKEY",
        "DRVSPACE",
        "EDLIN",
        "EMM386",
        "EXE2BIN",
        "FAKEMOUS",
        "FASTHELP",
        "FASTOPEN",
        "FC",
        "FDISK",
        "GOTO",
        "GRAFTABL",
        "INTERSVR",
        "INTERLNK",
        "KEYB",
        "LOADFIX",
        "LOADHIGH",
        "LH",
        "MD",
        "MKDIR",
        "MEM",
        "MEMMAKER",
        "MSAV",
        "MSBACKUP",
        "MSCDEX",
        "MSD",
        "MSHERC",
        "NLSFUNC",
        "PRINTFIX",
        "QBASIC",
        "RD",
        "RMDIR",
        "RECOVER",
        "REM",
        "REN",
        "SETVER",
        "SMARTDRV",
        "SUBST",
        "SYS",
        "TELNET",
        "TRUENAME",
        "VER",
        "VOL",
        "VSAFE",
        "XCOPY",
        ]

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


    TEXT_BETWEEN_REFS = re.compile(r'[\`\*\"]+(.*)[\`\*\"]+')

    GA_CHAR = "`"
    DBL_GA_CHAR = "``"
    AST_CHAR = "*"
    DBL_AST_CHAR = "**"
    QUOTE_CHAR = "\""
    DBL_QUOTE_CHAR = "\"\""
    PARA_SEP_CHAR = "€€€"
    DOT="\."
    COMMA="\,"
    COLON=";"
    HYPHEN='-'
    DBL_HYPHEN='--'
    ENDS_PUNCTUAL=re.compile(r'([\.\,\:\!\?]+$)')

    #WRONG_REF =re.compile(r'\`(?![\s\)([^\`]+)\`\ \-\-\ :[\w]+:\`([^\`]+)(?<!([\s\:]))\`')
    ALL_SINGLE_GA=re.compile(r'^[\`]{1}(.*)[\`]{1}$')
    ALL_DOUBLE_GA = re.compile(r'^[\`]{2}(.*)[\`]{2}$')

    CONTAINT_AST = re.compile(r'[\*\"]+(?![\s\)\(\.]+)([^\*\"]+)(?<!([\s\:]))[\*\"]+')
    SINGLE_GA=re.compile(r'(:[\w]+:)*\`(?![\s\)\\.(]+)([^\`]+)(?<!([\s\:]))\`')
    REF_SINGLE=re.compile(r':[\w]+:\`(?![\s]+)([^\`])(?<!(\s))\`') #(?<=(:[\w]:)) not ending with before end
    REF_SINGLE_ONLY=re.compile(r'^:[\w]+:\`([^\`]+)\`$')
    REF_WORD_ONLY_SINGLE = re.compile(r'[\`]+(.*)[\`]+')
    REF_DOUBLE=re.compile(r'[\`]{2}(?![\s]+)([^\`]+)[\`]{2}')
    REF_WORD_ONLY_DOUBLE = re.compile(r'[\`]{2}[\:\|]*([^\`\:\|]+)[\:\|]*[\`]{2}')
    REF_DOUBLE_PACKED=re.compile(r'[\`]{2}(?![\s]+)(\:[\w]+\:)(.*)[\`]{3}')
    REF_WORD_ONLY_DOUBLE_PACKED = re.compile(r'[\`]{2}:[\w]+:[\`]{1}([^\`]+)[\`]{3}')
    REF_WORD_ONLY = re.compile(r'[\`]+([^\`]+)[\`]+')
    REF_LINK_WITHOUT_REFWORD = re.compile(r'\<([^<]+)\>')

    SINGLE_GA_REF_AND_LINK = re.compile(r':[\w]+:\`(?![\s\)\\.(]+)([^\`]+)((\<([^<]+)\>)*)(?<!([\s\:]))\`')

    #PARA_SEP = re.compile(r'([^\.\,\;\_\(\)\'\"\[\]\:\!]+)')
    PARA_SEP = re.compile(r'(?![\s]+)([\w\-\ \']+)(?<!([\s]))')
    BRACKETTED = re.compile(r'[\(\[\*\'\"]+')
    NOT_MENU_SEP = re.compile(r'([^->]+)')

    WORD_ONLY=re.compile(r'\b([\w\.\/\+\-\_\<\>]+)\b')
    REF_LINKS=re.compile(r'<[^<]+>')
    MENU_WORDS = re.compile(r'[^<]+>')
    WORD_INSIDE_BRAKET = re.compile(r'\(([^\(\)]+)\)')
    DOUBLE_GRAVE_ACCENT_SURROUND = re.compile(r'\`\`(.*)\`\`')
    REF_KEYS = re.compile(r'(:(doc|ref|menuselection|kbd|abbr|term|guilabel):){1}')
    REF_PART=re.compile(r'^:[\w]+:\`([^\`]+)')
    REF_TAG_SEP = re.compile(r'(:[\w]+:)\`([^\`]+)\`')

    GA_BRACKETTED =re.compile(r'^[\`]+([^\`]+)[\`]+$')

    PACKED_REF=re.compile(r'(:(doc|ref|menuselection|kbd|abbr|term|guilabel):)((\`([^\`]+)\`)|(\`\`([^\`]+)\`\`))([_]*)+')
    SINGLE_REF = re.compile(r'^(:(doc|ref|menuselection|kbd|abbr|term|guilabel):)*((\`([^\`]+)\`)|(\`\`([^\`]+)\`\`))([_]*)+$')

    REFS = re.compile(r'(:(doc|ref|menuselection|kbd|abbr|term|guilabel):)*((\`([^\`]+)\`)|(\`\`([^\`]+)\`\`))([_]*)+')
    ONE_REF_LINK=re.compile(r'^([\w\-\_\.]+)$')
    PATH_PATTERN=re.compile(r'^([\w]{1}[\:]{1})*([\w\\\.\_\-\/\~\ \#]+)$')
    ONE_GA = re.compile(r'\`{1}(.*)\`{1}')
    TWO_GA = re.compile(r'\`{2}(.*)\`{2}')

    BUTTON_LABEL=re.compile(r'\`{2}(.*)\`{2}')
    POSSIBLE_FILE_PATH=re.compile(r'([\\\/\~]{1})')
    WORD_ONLY_FIND = re.compile(r'\b[\w\-\_\']+\b')



    #REFS = re.compile(r':(doc | ref | menuselection | kbd):\`[ ^\`]+\` | ``[ ^ ``]+``')

    COMMON_KEYS = ["ctrl", "alt", "windows", "tab", "shift", "spacebar", "enter", "delete", "pgup", "pageup",
                   "pgdown", "pagedown", "end", "esc", "return","backspace", "home",
                   "f0", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12"]

    ALPHABET = r"(\w){1}"

    # , ""
    ignore_start_with_list = [
        "bpy", "def", "bpy", "bl_info", "dx",
        "git", "mathutils", "blender_api", "Poedit", "PIP", "Subversion", "TortoiseSVN", "var ", "\"fr\"", "\"fr\":",
        "A (Alpha)",
    ]
    RE_NONTRANS="^([\ |\t]?-- ).*$"
    RE_KEYBOARD=r"(:kbd:`)(.*?)(`)"

    ESCAPE_DIC=str.maketrans({"-":  r"\-", \
                "]":  r"\]", \
                "\\": r"\\", \
                "^":  r"\^", \
                "$":  r"\$", \
                "*":  r"\*", \
                ".":  r"\."})

    UNTRANSLATED_STRINGS=[
        "The quick brown fox jumps over the lazy dog"
        ]

    def isBracketed(msg : str):
        is_bracketed = False
        try:
            f_char = msg[:1]
            l_char = msg[-1:]
            is_first = (Common.BRACKETTED.match(f_char) != None)
            is_last = (Common.BRACKETTED.match(l_char) != None)
            is_bracketed = (is_first and is_last)
        except Exception as e:
            _(msg)
            _(e)
        return is_bracketed

    def isNotTranslated(msg, tran):
        msg_list = Common.WORD_ONLY_FIND.findall(msg.lower())
        tran_list = Common.WORD_ONLY_FIND.findall(tran.lower())

        # convert list to set of words, non-repeating
        tran_set = set(tran_list)
        msg_set = set(msg_list)

        # perform set intersection to find common set
        common_set = tran_set.intersection(msg_set)
        is_not_translated = (common_set == msg_set)
        return is_not_translated


    def hasOriginal(msg, tran):
        msg_list = Common.WORD_ONLY_FIND.findall(msg.lower())
        tran_list = Common.WORD_ONLY_FIND.findall(tran.lower())

        # convert list to set of words, non-repeating
        tran_set = set(tran_list)
        msg_set = set(msg_list)

        # perform set intersection to find common set
        common_set = tran_set.intersection(msg_set)

        common_len = len(common_set)
        msg_len = len(msg_set)
        tran_len = len(tran_set)
        considering_match = (float(common_len) >= (float(msg_len) * 0.5))  # matching more than 50%

        is_encap = (common_set == msg_set) or considering_match
        return is_encap

    def hasPattern(pat, text):
        is_there = (pat.search(text) != None)
        return is_there

    def isDoubleGA(msg):
        is_double = (msg.startswith(Common.DBL_GA_CHAR) and msg.endswith(Common.DBL_GA_CHAR))
        return is_double

    def isSingleGA(msg):
        is_single = (msg.startswith(Common.GA_CHAR) and msg.endswith(Common.GA_CHAR))
        return is_single

    def splitRefParts(msg):
        tag = ref_text = None
        try:
            has_ref_tag = (Common.REF_KEYS.search(msg) != None)
            if not has_ref_tag:
                return None, msg
            #s, e, m0, m1 = Common.patternMatchAsParts(Common.REF_TAG_SEP, msg)
            match_list = []
            match_1 = match_2 = None
            for m in Common.REF_TAG_SEP.finditer(msg):
                start_index = m.start()
                end_index = m.end()
                match_0 = m.group(0)
                try:
                    match_1 = m.group(1)
                except Exception as e:
                    match_1 = None

                try:
                    match_2 = m.group(2)
                except Exception as e:
                    match_2 = None

                tag = match_1
                ref_text = match_2
                break

            return tag, ref_text
        except Exception as e:
            print(msg)
            print(e)
            raise e

    def removeGA(msg):
        _("removeGA", msg)
        state = 0
        is_double = (msg.startswith(Common.DBL_GA_CHAR) and msg.endswith(Common.DBL_GA_CHAR))
        is_double_ast = (msg.startswith(Common.DBL_AST_CHAR) and msg.endswith(Common.DBL_AST_CHAR))
        is_double_quote = (msg.startswith(Common.DBL_QUOTE_CHAR) and msg.endswith(Common.DBL_QUOTE_CHAR))
        is_dbl = (is_double or is_double_ast or is_double_quote)
        #s = cp.deepcopy(msg)
        if is_dbl:
            result = msg[2:-2]
            state = 2
        else:
            is_single = (msg.startswith(Common.GA_CHAR) and msg.endswith(Common.GA_CHAR))
            is_single_ast = (msg.startswith(Common.AST_CHAR) and msg.endswith(Common.AST_CHAR))
            is_single_quote = (msg.startswith(Common.QUOTE_CHAR) and msg.endswith(Common.QUOTE_CHAR))
            is_sgle = (is_single or is_single_ast or is_single_quote)
            if is_sgle:
                result = msg[1:-1]
                state = 1
            else:
                result = msg
        return result, state


    def removeRefLink(msg : str):
        if (msg is None) or (len(msg) == 0):
            return msg, None
        try:
            has_ref_link = (Common.REF_LINKS.search(msg) != None)
            if not has_ref_link:
                return (-1, -1, msg, None)
        except Exception as e:
            _(msg)
            _(e)
            raise e

        _("remove_ref_link input:", msg)
        s, e, ref_title, ref_link = Common.patternMatchAsParts(Common.SINGLE_GA_REF_AND_LINK, msg)
        _("s, e, m0, m1")
        _(s, e, m0, m1)

        return (s, e, ref_title, ref_link)

    def isFilePath(text_line : str):
        if (text_line is None) or (len(text_line) == 0):
            return False

        text_line = text_line.strip()
        is_menu = ('-->' in text_line)
        if is_menu:
            return False

        has_text_ref_link=(Common.REF_LINK_WITHOUT_REFWORD.search(text_line) != None)
        if has_text_ref_link:
            _("has_text_ref_link")
            return False

        # _("isFilePath")
        has_path_characters = ('\\' in text_line) or ('/' in text_line)
        starts_with_path_chars = text_line.startswith('~')

        dot_index = text_line.find(".")
        has_dot = (dot_index >= 0)
        ends_with_extensions = False
        if has_dot:
            end_part = text_line[dot_index+1:]
            ends_with_extensions = (len(end_part) >= 1) and (len(end_part) < 5) and end_part.isalnum()

        is_path = (has_path_characters or starts_with_path_chars or ends_with_extensions)

        if is_path:
            _("isFilePath", text_line)
            #exit(0)

        return is_path

    def getTextOnly(text_with_refs):
        text = Common.REFS.sub("", text_with_refs)
        return text

    def matchListEmptyEntry():
        empty_entry = (-1, -1, None, None)
        return empty_entry

    def isPatternMatchListEmpty(match_list):
        is_list_valid = (match_list is not None) and (len(match_list) > 0)
        if not is_list_valid:
            return True

        s, e, m0, m1 = match_list[0]
        is_empty = (m0 is None) and (m1 is None) and (s == -1) and (e == -1)
        return is_empty

    def patternMatchAsParts(pattern, text_with_refs):
        match_list = Common.patternMatchAsList(pattern, text_with_refs)
        return match_list[0]

    def patternMatchAll(pattern, text):
        match_list = {}
        try:
            for k, m in enumerate(pattern.finditer(text)):
                s = m.start()
                e = m.end()
                g = m.group(0)
                v = cmMatch()

                v = [[s, e, g]]
                match_list.update({k:v})
                matched_groups = m.groups()
                for g in matched_groups:
                    if g:
                        ss = text.find(g)
                        ee = ss + len(g)
                        v = [ss, ee, g]
                        match_list[k].append(v)
        except Exception as e:
            _(pattern, "[=>]", text)
            _(e)
            # raise e
        return match_list

    def patternMatchAsList(pattern, text):
        match_list = []
        try:
            for m in pattern.finditer(text):
                start_index = m.start()
                end_index = m.end()
                match_0 = m.group(0)
                try:
                    match_1 = m.group(1)
                except Exception as e:
                    match_1 = None

                #_("groups:", m.groups())
                match_list.append((start_index, end_index, match_0, match_1))

            has_result = (len(match_list) > 0)
            if has_result:
                return match_list
            else:
                empty_entry = Common.matchListEmptyEntry()
                return [empty_entry]
        except Exception as e:
            _(pattern, "[=>]", text)
            _(e)
            raise e

    def patternCollectMatches(matched_list, position=[]):
        item_list=[]
        has_items = not ((matched_list is None) or (len(matched_list) == 0) or Common.isPatternMatchListEmpty(matched_list))
        if not has_items:
            return item_list

        is_empty = (len(position) == 0)
        if is_empty:
            return matched_list

        is_a_tuple_required = (len(position) > 1)
        entry_list=[]
        for s, e, p0, p1 in matched_list:
            entry=[]
            if (0 in position):
                entry.append(s)
            if (1 in position):
                entry.append(e)
            if (2 in position):
                entry.append(p0)
            if (3 in position):
                entry.append(p1)
            if is_a_tuple_required:
                e = tuple(entry)
            else:
                e = entry[0]
            entry_list.append(e)
        return entry_list

    def isDosCommand(text):
        if (text is None) or (len(text) == 0):
            return False

        for w in Common.DOS_COMMANDS:
            p = re.compile(r'\b{}\b'.format(w))
            is_dos_command = (p.search(text) != None)
            if is_dos_command:
                return True
        return False

    def isTerm(text):
        pat=r'^\:.*\:$'
        is_term = (re.search(pat, text) != None)
        return is_term

    def assertFileExist(file_name):
        err_msg_head = "File "
        err_msg_tail = "doesn't exist!"
        assert os.path.isfile(file_name), "{}: [{}] {}".format(err_msg_head, file_name, err_msg_tail)

    def translateKeyboardDef(text_line):
        _("translateKeyboardDef:", text_line)
        new_text_line=str(text_line)
        for k, trans in Common.KEYBOARD_TRANS_DIC.items():
            new_text_line = re.sub(k, trans, new_text_line)
        _(text_line, " => ", new_text_line)
        return new_text_line

    def isEmpty(obj):
        is_empty = (obj == None) or (len(obj) == 0)
        return is_empty

    def isHz(text_line:str):
        is_found = (Common.KHZ.search(text_line) != None)
        return is_found

    def isRemovableKeyboardDef(text_line):
        have_special_def = (Common.SPECIAL_DEF.search(text_line) != None)
        if (have_special_def):
            return False

        #make a copy of text
        test_text_line = str(text_line)
        #search out for all keyboard defs
        word_list=Common.KEYBOARD_DEF.findall(text_line)
        if (len(word_list) == 0):
            return False

        for kbd in word_list:
            test_text_line = test_text_line.replace(kbd, "")
        test_text_line = re.sub("[\W]", "", test_text_line)
        have_words_other_than_keyboard_defs = (len(test_text_line) > 0)
        if (have_words_other_than_keyboard_defs):
            return False

        return True

    def escapeString(text_line):
        escaped = text_line.translate(Common.ESCAPE_DIC)
        return escaped

    def RSTGetSubParaHeading(text_line):
        found_list = RST_SUB_PARA.findall(text_line)
        is_found = (len(found_list) > 2)


    def isLeadingWithHyphen(text_line):
        m = re.match(Common.RE_NONTRANS, text_line)
        is_found = (m != None)
        return is_found

    def isLeadingAlpha(text_line:str) -> bool:
        #a = text_line[:1]
        #is_found = a.isalpha()
        m = re.match(Common.RE_IS_ALPHA, text_line)
        #_("isLeadingAlpha: {}, a={}, is_alpha:{}, m={}".format(text_line, a, is_found, m))
        is_found = (m != None)
        return is_found

    def isDocPath(text_line) -> bool:
        m = Common.PURE_DOC_PATH.search(text_line)
        result = (m != None)
        return (result)

    def isNonAlphaNumeric(text_line):
        return (Common.NON_ALPHA.search(text_line) != None)

    #def filterBoxChars(text_line) -> bool:
        #return (Common.FILTER_RST_BOX.match(text_line) != None)

    def getOption(text_line) -> bool:
        if (text_line is None) or (len(text_line) == 0):
            return None

        result = None
        #_("getOption() text_line:[{}]".format(text_line))
        ml = Common.FILTER_RST_BOX.findall(text_line)
        if (len(ml) > 0):
            found_item=ml[0][1]
            mo=Common.OPTION.search(found_item)
            if (mo != None):
                result = mo[0]
        else:
            mo=Common.OPTION.search(text_line)
            if (mo != None):
                result = mo[0]

        search_string = (result if (result != None) else text_line)
        mo = Common.NON_ALPHA.search(search_string)
        if (mo != None):
            result = mo[0]
        #_("getOption() result:[{}]".format(result))
        return result

    def isNumber(text_line) -> bool:
        if (text_line is None) or (len(text_line) == 0):
            return False

        return (Common.NUMBER.match(text_line) != None)

    def startWithHyphen(text_line:str) -> bool:
        if (text_line is None) or (len(text_line) == 0):
            return False

        result = re.match(Common.RE_LEADING_HYPHENS, text_line)
        is_found = (result != None)
        return is_found

    def checkIfWellQuoted(text_line) -> dict:
        dictionary={}
        counter=[0,0] #single quote index 0, double quote index = 1
        ic_state=[False, False]
        ci = -1
        for index, c in enumerate(text_line):
            is_squote = Common.SC.match(c)
            is_dquote = Common.DC.match(c)
            if (is_squote or is_dquote):
                ci = (0) if (is_squote) else (1)
                ic_state[ci] = not ic_state[ci]
                counter[ci] = (counter[ci] + 1) if (ic_state[ci]) else (counter[ci] - 1)
                key="{}{}".format(counter[0], counter[1])
                dictionary.update( {key:index} )
                _("Quoted:{}".format(counter))

        result = int(counter[0]) * 10 + int(counter[1])
        return [result==0, dictionary]

    def stripQuote(text_line):
        #_("stripQuote:[{}]".format(text_line))
        if (not isinstance(text_line, str)):
            raise Exception("ERROR - Common.stripQuote(text_line):{}".format(text_line))

        output_line = text_line
        is_starts_with_quote = text_line.startswith(Common.QUOTE)
        if (is_starts_with_quote):
            output_line = (text_line[1:] if (is_starts_with_quote) else text_line)

        #_("stripQuote [{}], is_starts_with_quote:{}".format(output_line, is_starts_with_quote))
        is_ends_with_quote = output_line.endswith(Common.QUOTE)
        if (is_ends_with_quote):
            length = len(output_line)
            is_checkable = (length > 1)
            if (is_checkable):
                char_before_last = output_line[length-2]
                is_ends_with_quote = (char_before_last != Common.B_SLASH)

        output_line = (output_line[:length-1] if (is_ends_with_quote) else output_line)

        return output_line

    def isIgnoredIfStartsWith(text_line : str):
        if (text_line is None) or (len(text_line) == 0):
            return True

        for x in Common.ignore_start_with_list:
            is_starts_with = (text_line.lower().startswith(x.lower()))
            if (is_starts_with):
                return True
        return False

    def isIgnored(text_line : str):
        if (text_line is None) or (len(text_line) == 0):
            return True

        for x in Common.ignore_list:
            p = re.compile(r'{}'.format(x), flags=re.I)
            m = p.search(text_line)
            is_found = (m != None)
            if (is_found):
                _("[{}] matched [{}]".format(text_line, x))
                return True

        is_ignored = (text_line in Common.UNTRANSLATED_STRINGS)
        return is_ignored

    def isIgnoredWord(text_line : str):
        if (text_line is None) or (len(text_line) == 0):
            return True

        try:
            for x in Common.ignore_list:
                m = re.compile(r'^{}$'.format(x), flags=re.I)
                is_found = (m.search(text_line) != None)
                if (is_found):
                    _("[{}] matched [{}]".format(text_line, x))
                    return True
        except Exception as e:
            _(e)
            _("isIgnoredWord ERROR:", text_line)
        return False

    def isUntranslated(text_line:str):
        ll = " ".join(Common.UNTRANSLATED_STRINGS).lower()
        ls = text_line.lower()
        is_found = (ll.find(ls) >= 0)
        return is_found

    def isResolution(text_line : str):
        is_found = (Common.RESOLUTION.search(text_line) != None)
        return is_found

    def isUnderlined(text_line):
        trimmed_copy = str(text_line).strip()
        found_list = re.findall(Common.RE_RST_UNDERLINED, trimmed_copy)
        is_found = (found_list != None)
        return is_found

    def isEndedFullStop(text_line):
        trimmed_copy = str(text_line).strip()
        found_list = re.findall(Common.RE_ENDING_DOT, trimmed_copy)
        is_found = (found_list != None)
        return is_found

    def isMustIncludedKeyboardPart(text_line):
        def __is_ignore__(part):
            is_single_unit = (len(part) == 1)
            is_common_key = (part.lower() in Common.COMMON_KEYS)
            is_ignore = (is_common_key or is_single_unit)
            return (is_ignore)

        found_list = re.findall(Common.RE_KEYBOARD, text_line)
        has_kbd = (len(found_list) > 0)
        if (not has_kbd):
            return False

        is_ignore = True
        for leading, key_def, trailing in found_list:
            #_("*** {}{}{}".format(leading, key_def, trailing))
            key_list = key_def.split("-")
            spacing_list = key_def.split(" ")
            # _(os.linesep.join(key_list))
            for part in key_list:
                is_ignore = __is_ignore__(part)
                if (not is_ignore): break

            if (not is_ignore):
                for part in spacing_list:
                    is_ignore = __is_ignore__(part)
                    if (not is_ignore): break
        return (not is_ignore)

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

    def getByName(var):
        callers_local_vars = inspect.currentframe().f_back.f_locals.items()
        return [var_name for var_name, var_val in callers_local_vars if var_val is var]

    def printRefList(ref_list, msg=None):
        if msg:
            _(msg)
        _('*'*30)
        pp(ref_list)
        _('*'*30)

    def isTextInRefList(text, ref_list):
        try:
            for index, item in enumerate(ref_list):
                s, e, w0, w1 = item
                is_in = (text in w0) or (text in w1)
                if is_in:
                    return index
        except Exception as e:
            _("isTextInRefList")
            _("text:", text)
            _("ref_list")
            pp(ref_list)
            _(e)
        return -1

    def findNoneExistsItem(from_l, to_l, output):
        for s, e, w0, w1 in from_l:
            found_index = (Common.isTextInRefList(w0, to_l))
            is_found = (found_index >= 0)
            if not is_found:
                pref_item = (s, e, w0, w1)
            else:
                pref_item = to_l[found_index]
            is_already_in_list = (pref_item in output)
            if not is_already_in_list:
                output.append(pref_item)

    def findPrefRef(from_list, to_list):
        pref=[]
        Common.findNoneExistsItem(from_list, to_list, pref)
        Common.findNoneExistsItem(to_list, from_list, pref)
        return pref

    def printRefListExtracted(extract_pattern, ref_list):
        if not DEBUG:
            return

        for s, e, m0, m1 in ref_list:
            wps, wpe, wp0, wp1 = Common.patternMatchAsParts(extract_pattern, m0)
            _("wps, wpe, wp0, wp1")
            _(wps, wpe, wp0, wp1)

    def findListOfLinks(msg):
        chosen_list = None

        single_ga_list = Common.patternMatchAsList(Common.SINGLE_GA, msg)
        ref_list_single = Common.patternMatchAsList(Common.REF_SINGLE, msg)
        ref_list_double = Common.patternMatchAsList(Common.REF_DOUBLE, msg)
        ref_list_double_packed = Common.patternMatchAsList(Common.REF_DOUBLE_PACKED, msg)
        contain_ast_list = Common.patternMatchAsList(Common.CONTAINT_AST, msg)

        list_of_lists = [
            (single_ga_list, Common.TEXT_BETWEEN_REFS, "single GA"),
            (ref_list_single, Common.REF_WORD_ONLY_SINGLE, "single REF"),
            (ref_list_double, Common.REF_WORD_ONLY_DOUBLE, "double"),
            (ref_list_double_packed, Common.REF_WORD_ONLY_DOUBLE_PACKED, "double_packed"),
            (contain_ast_list, Common.TEXT_BETWEEN_REFS, "contains AST"),
        ]

        # is_debug = ("bone behaves like the single one produced" in msg)
        # if is_debug:
        #     f_list = Common.CONTAINT_AST.findall(msg)
        #     print("DEBUG")

        print_list = []
        process_list = []
        for index, elem in enumerate(list_of_lists):
            l, pattern, list_desc = elem
            is_empty = Common.isPatternMatchListEmpty(l)
            if not is_empty:
                process_list.append(l)
                if DEBUG:
                    print_list.append((l,pattern,list_desc))

        number_of_lists = len(process_list)
        is_all_empty = (number_of_lists == 0)
        if is_all_empty:
            return

        #now reduce all entries to the largest matching set
        reduced_list = process_list[0]
        for i in range(1, number_of_lists):
            reduced_list = Common.findPrefRef(reduced_list, process_list[i])
            _("reduced_list")
            pp(reduced_list)

        sort_reduced_list = sorted(reduced_list, key=refListGetKey)
        uniq_list = Common.removeDuplicateRefEntries(sort_reduced_list)

        return uniq_list

    def removeDuplicateRefEntries(ref_list):
        three_tuples = []
        for s, e, m0, m1 in ref_list:
            entry=(s, e, m0)
            three_tuples.append(entry)
        thee_set = set(three_tuples)
        new_ref_list=[]
        for i, elem in enumerate(ref_list):
            s, e, m0, m1 = elem
            entry=(s, e, m0)
            if entry in thee_set:
                new_ref_list.append(elem)
                thee_set.remove(entry)
        return new_ref_list

    def replaceRefTrans(msg, current_trans, visitor, cat):
        #_("replaceRefTrans:")
        has_replacements = len(visitor.node_trans_list) > 0
        new_trans = str(msg)
        if has_replacements:
            _("-" * 30)
            for s, e, k, v in reversed(visitor.node_trans_list):
            # for k, v in visitor.node_trans_list.items():
                if v:
                    st = new_trans[:s]
                    se = new_trans[e:]
                    new_trans = st + v + se
                    _(s, e, k, ">>>" ,v)
                # if v:
                #     trans = trans.replace(k, v)
            _("-"*80)

        _("msgid", msg)
        has_both_and_diff = (current_trans and new_trans and (current_trans != new_trans))
        trans = (current_trans if current_trans else new_trans)
        if has_both_and_diff:
            _("00-msgstr", current_trans)
            _("01-msgstr", new_trans)
            cat.add(msg, string=trans, user_comments=[new_trans])
        else:
            _("00-msgstr", trans)
            cat.add(msg, string=trans)
        _("-" * 30)


    def findLinksEmbeddedInMessage(msg, title=None):
        emb_links=[]
        ref_list = Common.findListOfLinks(msg)
        has_ref = (not Common.isPatternMatchListEmpty(ref_list))
        if ref_list:
            for s, e, m0, m1 in ref_list:
                trans = Common.trans_finder.translateText(m0)
                entry = [s, e, m0, trans]
                emb_links.append(entry)

            _("findLinksEmbeddedInMessage:")
            pp(emb_links)
        return emb_links

    def reportHTMLTable(msg, trans, msg_links, trans_link):
        if not Common.print_html:
            return

        print("<p>")
        if msg:
            print("<b>msgid:</b><span>{}</span>".format(html.escape(msg)))
        if trans:
            print("<br/>")
            print("<b>msgstr:</b><span>{}</span>".format(html.escape(trans)))
        print("</p>")

        if (msg_links or trans_link):
            print("<table style=\"width:100%\" border=\"1\">")
            # print("<tr>")
            # print("<th>MSGID<th>")
            # print("<th>MSGSTR<th>")
            # print("</tr>")

        if msg_links:
            lms = len(msg_links)
        else:
            lms = 0

        if trans_link:
            trs = len(trans_link)
        else:
            trs = 0

        max = (lms if (lms > trs) else trs)
        for i in range(0, max):
            print("<tr>")
            print("<td style=\"width:50%\">")
            if i < lms:
                print(html.escape(str(msg_links[i])))
            else:
                print(" ")
            print("</td>")
            print("<td style=\"width:50%\">")
            if i < trs:
                print(html.escape(str(trans_link[i])))
            else:
                print(" ")
            print("</td>")
            print("</tr>")
        print("</table>")

    def splitTranslationAndOrigEnglish(msg):

        text, ga_state = Common.removeGA(msg)

        has_ref = Common.hasPattern(Common.REF_PART, msg_no_ga)
        if has_ref:
            s,e, m0, m1 = Common.patternMatchAsParts(Common.REF_PART, msg_no_ga)
            text = m1

        # keyboard with () - get origin by removing ()
        # abbr: with () - get origin by removing -- part within ()

        english_orig = text
        translation = None
        has_tran = ("-- " in english_orig)
        if has_tran:
            word_list = msg_no_ga.split("-- ")
            translation = word_list[0].strip()
            english_orig = word_list[1]

        return (english_orig, translation, ga_state)

    def reportHTML(msg, left, right):
        if not Common.print_html:
            return

        p = "<p><i>{}</i> [{}] => [{}]</p>".format(msg, html.escape(str(left)), html.escape(str(right)))
        print(p)

    def reportHTMLHead():
        if not Common.print_html:
            return

        page_head = [
            "<!DOCTYPE html>",
            "<head>",
            "</head>",
            "<meta charset=\"UTF-8\">",
            "<html>",
            "<body>",
            "<h2>Report</h2>",
        ]
        for l in page_head:
            print(l)

    def reportHTMLTail():
        if not Common.print_html:
            return

        page_tail = [
            "</body>",
            "</html>"
        ]
        for l in page_tail:
            print(l)

    def hasEncapOrigInTrans(msg, tran):
        msg_list = Common.WORD_ONLY_FIND.findall(msg.lower())
        tran_list = Common.WORD_ONLY_FIND.findall(tran.lower())

        # convert list to set of words, non-repeating
        tran_set = set(tran_list)
        msg_set = set(msg_list)

        # perform set intersection to find common set
        common_set = tran_set.intersection(msg_set)

        common_len = len(common_set)
        msg_len = len(msg_set)
        tran_len = len(tran_set)
        considering_match = (float(common_len) >= (float(msg_len) * 0.5))  # matching more than 50%

        is_encap = (common_set == msg_set) or considering_match
        return is_encap

    def isRefInRefList(msg_ref : str, trans_ref_list):
        possible_list=[]
        for index, e in enumerate(trans_ref_list):
            es, ee, e0, e1 = e

            #remove the leading grave accents (`)
            non_ga_tran, tr_ga_state = Common.removeGA(e0)
            non_ga_orig, orig_ga_state = Common.removeGA(msg_ref)

            #remove the link <..> if any
            trs, tre, tr_ref_str, tr_refuri = Common.removeRefLink(non_ga_tran)
            mrs, mre, msg_ref_str, msg_refuri = Common.removeRefLink(non_ga_orig)
            has_link = (tr_refuri and msg_refuri)
            is_found = has_link and (tr_refuri == msg_refuri)
            if is_found:
                Common.reportHTML("exact link", msg_ref, str(trans_ref_list[index]))
                return index
            elif has_link:
                #NEED to check of link has changed and that new link is needed to replace
                #this probably needs manual interventions then automatical replacements
                has_tr_str = (tr_ref_str and len(tr_ref_str.strip()) > 0)
                has_msg_str = (msg_ref_str and len(msg_ref_str.strip()) > 0)
                if has_tr_str and has_msg_str:
                    non_ga_tran = tr_ref_str
                    non_ga_orig = msg_ref_str
                else:
                    trans = trans_finder.findTranslation(msg_ref_str)
                    if trans:
                        non_ga_tran = tr_ref_str
                        non_ga_orig = trans
                    else:
                        continue

            #separate :ref: and 'text'
            tr_tag, tr_ref_txt = Common.splitRefParts(non_ga_tran)
            orig_tag, orig_ref_txt = Common.splitRefParts(non_ga_orig)

            #special case for :kbd: tag
            has_tag = (tr_tag and orig_tag)
            is_kbd = has_tag and (Common.KBD in tr_tag) and (Common.KBD in orig_tag)
            if is_kbd:
                #retranslate to get only the text part, later versions of files would need to rework this
                non_ga_orig = Common.translateKeyboardDef(orig_ref_txt)
                non_ga_tran = tr_ref_txt

            is_found = Common.hasEncapOrigInTrans(non_ga_orig, non_ga_tran)
            if is_found:
                Common.reportHTML("exact or considering match", msg_ref, str(trans_ref_list[index]))
                return index

        Common.reportHTML("MANUAL FIXINGS REQUIRED:", msg_ref, "")
        return -1


    def replaceReferenceToMsg(trans, ref_msg_lst, ref_trans_lst):
        has_ref_msg = (ref_msg_lst is not None)  and (len(ref_msg_lst) > 0)
        has_ref_trans = (ref_trans_lst is not None) and (len(ref_trans_lst) > 0)

        valid = (trans is not None) and (len(trans) > 0) and (has_ref_msg and has_ref_trans)
        if not valid:
            return

        unconnected_entries = []
        changed = False
        for ts, te, orig, tran in ref_msg_lst:
            has_translation = (tran != None)
            if not has_translation:
                continue

            found_index = (Common.isRefInRefList(orig, ref_trans_lst))
            is_found = (found_index >= 0)
            if is_found:
                fs, fe, from_ref, f1 = ref_trans_lst[found_index]
                to_ref = tran
                trans = trans.replace(from_ref, to_ref)
                changed = True
            else:
                #unconn_entry = (ts, te, t0, t1)
                #unconnected_entries.append(unconn_entry)
                unconnected_entries.append(tran)

                #reportHTML("Found link", t0, str(ref_trans_lst[found_index]))
            # if not is_found and t1:
            #     found_index = (isRefInRefList(t1, ref_trans_lst))
            #     is_found = (found_index > 0)

        # a rather blind option to change references when there is only one instance on both sides
        can_blind_assume = (not changed) and (len(ref_msg_lst) == 1) and (len(ref_trans_lst) == 1)
        if can_blind_assume:
            rs, re, orig, to_ref = ref_msg_lst[0]
            has_translation = (to_ref is not None)
            if has_translation:
                ts, te, from_ref, t_text = ref_trans_lst[0]
                trans = trans.replace(from_ref, to_ref)
                changed = True
                Common.reportHTML("blind assume", from_ref, to_ref)

        # if changed:
        #     print("<b>updated msgstr:</b><span>{}</span>".format(html.escape(trans)))
        # must try to remove translated links and return the list of UNTRANSLATED
        return trans, unconnected_entries

    def findTransForList(sentence_list):

        tran_list={}
        for s in sentence_list:
            t = trans_finder.findTranslation(s)
            if not t:
                t = trans_finder.findTranslationByFragment(s)
            tran_list.append({s:t})
        s_list = []
        for k,v in tran_list.items():
            if v:
                s_list.append(v)
            else:
                s_list.append(k)
        trans = ""


    def translateEachSegment(segment_list):

        is_empty = (segment_list is None) or (len(segment_list) == 0)
        if is_empty:
            return None

        para_tran_list=[]
        for index, segment in enumerate(segment_list):
            ss, se, m0 = segment

            # is_debug = ("moving folders around" in m0)
            # if is_debug:
            #     print("DEBUG")

            para_list = Common.patternMatchAsList(Common.PARA_SEP, m0)

            if Common.isPatternMatchListEmpty(para_list):
                continue

            segment_list = []
            for ps, pe, p0, p1 in para_list:
                temp = p0.strip() # strip off the spaces
                trans = Common.trans_finder.findTranslation(temp)
                if trans is None:
                    trans = Common.trans_finder.findTranslationByFragment(temp)

                if trans is not None:
                    # put back spaces using simple replace
                    trans = p0.replace(temp, trans)

                entry=(ps, pe, p0, trans)
                segment_list.append(entry)

            # # join all the translated sentence back into the text
            trans = str(m0)
            for ps, pe, orig, tran in reversed(segment_list):
                text = (tran if tran else orig)
                trans = trans[:ps] + text + trans[pe:]

            # insert the translated sentence to a translated list
            entry = (ss, se, m0, trans)
            para_tran_list.append(entry)

        if Common.isPatternMatchListEmpty(para_tran_list):
            empty_entry = Common.matchListEmptyEntry()
            para_tran_list.append(empty_entry)
        return para_tran_list

    def translateNoneTransText(msg, ref_list):

        if (msg is None) or (len(msg) == 0):
            return None

        ##### PROBLEM HERE ######
        _("translateNoneTransText, msg")
        _(msg)

        _("translateNoneTransText, ref_list")
        pp(ref_list)

        is_debug = ("This will prevent all editing of the bone" in msg)
        if is_debug:
            _("debug")
        translated_msg = None
        part_list=[]
        ep = sp = 0
        has_ref : bool = (ref_list is not None) and (len(ref_list) > 0)
        if has_ref:
            # make sure all ref links are in ascending order of positions
            # jump through text, assuming first to be 0
            sort_ref_list = sorted(ref_list, key=refListGetKey)
            for s, e, orig,tr_text in sort_ref_list:
                ep = s
                if ep != sp:
                    para = msg[sp:ep]
                    part_list.append((sp, ep, para))
                sp = ep + len(orig)

            ep = len(msg)
            if ep != sp:
                para = msg[sp:ep]
                part_list.append((sp, ep, para))
        else:
            # if no links represents then use the whole message
            sp = 0
            ep = len(msg)
            entry = (sp, ep, msg)
            part_list.append(entry)

        _("After splitting, part_list")
        pp(part_list)
        translated_part_list = Common.translateEachSegment(part_list)

        is_translation_empty : bool = Common.isPatternMatchListEmpty(translated_part_list)
        can_join_ref_list : bool = has_ref and not is_translation_empty
        reflist_is_trans : bool = has_ref and is_translation_empty
        can_join_no_ref : bool = (not has_ref) and not is_translation_empty
        translation_is_empty : bool = (not has_ref) and is_translation_empty

        if can_join_ref_list:
            translated_part_list = translated_part_list + ref_list
            translated_part_list = sorted(translated_part_list, key=refListGetKey)
            _("can_join_ref_list")
            pp(translated_part_list)

        translated_msg = str(msg)
        if can_join_ref_list or can_join_no_ref:
            for ss, se, orig, trans in reversed(translated_part_list):
                tran_txt = (trans if trans else orig)
                translated_msg = translated_msg[:ss] + tran_txt + translated_msg[se:]
            _("can_join_ref_list or can_join_no_ref")
            pp(translated_part_list)

        if reflist_is_trans:
            for ss, se, orig, trans in reversed(ref_list):
                tran_txt = (trans if trans else orig)
                translated_msg = translated_msg[:ss] + tran_txt + translated_msg[se:]

            _("reflist_is_trans")
            pp(ref_list)

        if translation_is_empty:
            translated_msg = None

        return translated_msg

    def translateMsg(msg, current_trans):
        unconnected_entries = None
        tran_links = None
        msg_links = Common.findLinksEmbeddedInMessage(msg, title="msgid")
        has_links = (len(msg_links) > 0)
        has_trans = (not current_trans is None) and (len(current_trans) > 0)

        if has_trans and has_links:
            tran_links = Common.findListOfLinks(current_trans)
            if tran_links:
                current_trans, unconnected_entries = Common.replaceReferenceToMsg(current_trans, msg_links, tran_links)
        elif has_links:
            #break up according to links and translate non link parts
            current_trans = Common.translateNoneTransText(msg, msg_links)
        elif not has_trans:
            #break up para and translate each part
            current_trans = Common.translateNoneTransText(msg, None)
        return (current_trans, msg_links, tran_links, unconnected_entries)

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
            print("k:", k)
            print("v:", k)
            print(e)
            raise e
        return u_case
