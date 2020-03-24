import os
import re

class Common:
    COMMENT="#"
    MSGID="msgid"
    MSGCTXT="msgctxt"
    MSGSTR="msgstr"
    SPACE=" "
    QUOTE="\""
    NEWLINE = os.linesep
    FUZZY="#, fuzzy"
    DOT="."
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
    RE_TODO=r"(\btodo\b)"
    RE_QUOTED_WELL=r"^\"(.*)\"$"
    RE_QUOTED_STRING = "(?P<quote>['\"])(?P<string>.*?)(?<!\\)(?P=quote)"


    QUOTED_STRING_RE = re.compile(r"(?P<quote>['\"])(?P<string>.*?)(?<!\\)(?P=quote)")
    QUOTED_CHAR_RE = re.compile(r"(?P<quote_char>['\"])")

    DQ=re.compile(r"(?P<double_quote>[\"])(?P<string>.*?)(?<!\\)(?P=double_quote)")
    SQ=re.compile(r"(?P<single_quote>['])(?P<string>.*?)(?<!\\)(?P=single_quote)")

    DC=re.compile(r"(?P<dquote_char>[\"])")
    SC=re.compile(r"(?P<squote_char>['])")


    RST_HEADER=["#", "*", "=", "-", "^", "\""]

    end_char_list=set(['.','!',')', ',', '>', ':','*','`',])
    COMMENT_FLAG="#: "
    LANGUAGE_SEPARATOR=" -- "

    ignore_list=[
        "OBJ","PLY","STL","SVG","Web3D","Linux",
        "Apple macOS","Microsoft Windows",
        "OpenVDB","Alembic","Collada","OpenGL","CUDA","OpenCL","BSDF","Alpha","iTaSC",
        "Tab","PYTHONPATH","Python","Blender", "Arch Linux", "Redhat/Fedora",
        "Gamma", "RGB", "X", "Y", "Z", "XYZ", "Alpha", "X, Y", "Debian/Ubuntu", "UVs",
        "NURBS", "UV", "H.264", "MPEG", "Xvid", "QuickTime", "Ogg Theora", "X/Y",
        "AVI Jpeg", "OpenEXR", "Bézier", "Euler", "Verlet", "RK4", "CUDA", "OpenMP", "MS-Windows",
        "macOS", "Sigma", "X, Y, Z", "2D", "Nabla", "Musgrave", "Stucci", "Voronoi", "Lennard-Jones",
        "B-Spline", "CPU", "BSSRDF", "Boolean", "OpenSubdiv", "Nabla", "Python", "Blender", "PYTHONPATH",
        "MS-Windows", "YCbCr", "Catmull-Clark", "Blosc", "Zip", "OpenAL", "GLSL", "SDL", "Mono"
        "GGX", "Christensen-Burley", "Blackman-Harris", "Sobol", "DOF", "FSAA", "HDRI", "MIS", "NURBS",
        "glTF 2.0", "Catmull-Rom", "Mitch", "Laplace", "Sobel", "Prewitt", "Kirsch", "Doppler",
        "Alpha :kbd:`Ctrl-H`", "VD16", "HSV/HSL", "Mono", "GGX", "RRT", "Windows", "Laptops",
        "bpy.context", "bpy.data", "bpy.ops"
    ]


    COMMON_KEYS = ["ctrl", "alt", "windows", "tab", "shift", "spacebar", "enter", "delete", "pgup", "pageup",
                   "pgdown", "pagedown", "end", "esc", "return","backspace", "home",
                   "f0", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12"]

    ALPHABET = r"(\w){1}"

    # , ""
    ignore_start_with_list = [
        "bpy", "def", "bpy", "def", "for", "while", "print", "if", "bl_info", "class", "return", "paths", "dx"
    ]
    RE_NONTRANS="^([\ |\t]?-- ).*$"
    RE_KEYBOARD=r"(:kbd:`)(.*?)(`)"


    def isLeadingWithHyphen(text_line):
        m = re.match(Common.RE_NONTRANS, text_line)
        is_found = (m != None)
        return is_found

    def isLeadingAlpha(text_line:str) -> bool:
        #a = text_line[:1]
        #is_found = a.isalpha()
        m = re.match(Common.RE_IS_ALPHA, text_line)
        #print("isLeadingAlpha: {}, a={}, is_alpha:{}, m={}".format(text_line, a, is_found, m))
        is_found = (m != None)
        return is_found

    def startWithHyphen(text_line:str) -> bool:
        result = re.match(Common.RE_LEADING_HYPHENS, text_line)
        is_found = (result != None)
        return is_found

    def checkIfWellQuoted(text_line) -> str:
        counter=[0,0] #single quote index 0, double quote index = 1
        ic_state=[False, False]

        ci = -1

        for c in text_line:
            is_squote = SC.match(c)
            is_dquote = DC.match(c)
            ci = (0) if (is_squote) else ((1) if (is_dquote) else (-1))

            if (is_squote):
                ci = 0
                if (not ic_state[ci]): ic_state[ci] = True
                counter[ci] += 1
            elif (is_dquote):
                ci = 1
                if (not ic_state[ci]): ic_state[ci] = True
                counter[ci] += 1
            else:
                if (ic_state[ci]):
                    ic_state[ci] = False
                    counter[ci] -= 1




    def stripQuote(text_line):
        #print("stripQuote:[{}]".format(text_line))
        output_line = text_line
        is_starts_with_quote = text_line.startswith(Common.QUOTE)
        if (is_starts_with_quote):
            output_line = (text_line[1:] if (is_starts_with_quote) else text_line)

        #print("stripQuote [{}], is_starts_with_quote:{}".format(output_line, is_starts_with_quote))
        is_ends_with_quote = output_line.endswith(Common.QUOTE)
        if (is_ends_with_quote):
            length = len(output_line)
            is_checkable = (length > 1)
            if (is_checkable):
                char_before_last = output_line[length-2]
                is_ends_with_quote = (char_before_last != Common.B_SLASH)

#        is_debug = (text_line.find("Chỉ số cho vòng kết xuất") >= 0)
#        if (is_debug):
#            print("Before [{}], is_starts_with_quote:{}, is_ends_with_quote:{}".format(text_line, is_starts_with_quote, is_ends_with_quote))

        output_line = (output_line[:length-1] if (is_ends_with_quote) else output_line)
        #print("stripQuote [{}], is_ends_with_quote:{}".format(output_line, is_ends_with_quote))
#        if (is_debug):
#            print("after [{}], is_starts_with_quote:{}, is_ends_with_quote:{}".format(txt_line, is_starts_with_quote, is_ends_with_quote))
#            exit(1)

        return output_line

    def isIgnoredIfStartsWith(text_line : str):
        for x in Common.ignore_start_with_list:
            is_starts_with = (text_line.lower().startswith(x.lower()))
            if (is_starts_with):
                return True
        return False

    def isIgnored(text_line : str):
        for x in Common.ignore_list:
            is_found = (text_line.lower() == x.lower())
            if (is_found):
                return True
        return False

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
            #print("*** {}{}{}".format(leading, key_def, trailing))
            key_list = key_def.split("-")
            spacing_list = key_def.split(" ")
            # print(os.linesep.join(key_list))
            for part in key_list:
                is_ignore = __is_ignore__(part)
                if (not is_ignore): break

            if (not is_ignore):
                for part in spacing_list:
                    is_ignore = __is_ignore__(part)
                    if (not is_ignore): break
        return (not is_ignore)
