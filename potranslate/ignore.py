import sys
import re
from os import sep as dirsep
from os.path import pathsep
from common import Common as cm
from common import DEBUG, dd, pp

class Ignore:

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
        r"^\s*([\w\_\-]+\(([^\(\)]+)?\))\s*$", # function_name(param1, param2)
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
        r"^\s*([\d]?[\w]{1})\s*$",  # "4D"
        r"^\s*([\w\d]{2}\:){2}[\w\d]{2}\.[\w\d]{2}\.$",  # HH:MM:SS.FF
        r"^\s*(\.[\w]{2,5})\s*$",  # .jpg, .so
        r"^\s*(htt[ps][^\S]+)\s*$",
        r"^\s*(jpg|png|int)\s*$",
        r"^\s*(\-\-render\-frame 1|\-(ba|con|noaudio|setaudio)|Mem)\s*$",
        r"^\s*(([\d]+([\.[\d]+)?)*(mil|mi|mm|km|cm|ft|m|yd|dm|st|pi))\s*$",
        r"^\s*(mov|location[0]|cd|ch|hm|asin|um|tan|self|atan|atan2|Arctan2|sRGB)\s*$",
        r"^\s*(AAC|AVI Jpeg|AVX|AaBbCc|Albedo|Alembic|AC3|Alt|AMD|Ascii|AVX[\d]?|Acrylic)\s*$",
        r"^\s*Alembic([\s\W|abc]+)\s*$",
        r"^\s*(Alpha|Alt|Apple macOS|Arch Linux|Ashikhmin-Shirley)\s*$",
        r"^\s*(AVIJPEG|AVIRAW|BMP|DDS|DPX|IRIZ|JACK|JP2|RAWTGA|TGA|TIFF|[+-]<frame>|)\s*$",
        r"^\s*(B\-Spline|BSDF|BSSRDF|BU|BVH|Babel|Bezier|Bindcode|Bit[s]?|BkSpace|Bksp)\s*$",
        r"^\s*(Blackman\-Harris|Blosc|Barth|Byte\([s]*\)|Bytecode|Bézier|Backspace|(Blender\s(\d+[\d\.]+)))\s*$",
        r"^\s*Blender\([\s\d\.]+\)|Blender_id[\W]?|build\/html$",
        r"^\s*(CCEN|CPU|CUDA|Catmull\-(Clark|Rom)|Catrom|Chebychev|Clemens|Christensen\-Burley|Cineon|Collada)\s*$",
        r"^\s*(Ctrl|Cycles|Cycles:|Cinema(\s\(\d+\))?)\s*$",
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
        r"^\s*(NDOF((\W)|[\s]?(ESC|Alt|Ctrl|Shift))?|NURBS|Nabla|Ndof|Nabla|Null|NVIDIA|nn|Nishita)\s*$",
        r"^\s*(OBJ|OSkey|Ogawa|Ogg[\s]?(Theora)?|Open(AL|CL|EXR|MP|Subdiv|VDB)+|Opus|ObData|ILM\'s OpenEXR|OpenEXR|Ozone|OptiX)\s*$",
        r"^\s*PAINT_GPENCILEDIT_GPENCILSCULPT_.*$",
        r"^\s*(P(CM|LY|NG)|Pack Bits|Poedit|Preetham|Prewitt|PBR|PolyMesh|PO|pip|pip3|PIZ|PXR24|pc2|Preetham(\s?\d+)?|Python(\:\s[\.\%s]+)?)\s*$",
        r"^\s*(QuickTime|quasi\-)\s*$",
        r"^\s*(\d+[x]?)\s*$", # 16x
        r"^\s*(\%\d+[\w]?)\s*$", # %14s
        r"^\s*(\%[d](x%[d])?)\s*$", # %dx%d
        r"^\s*\%d(\s\w\s\%d)?(\W\s?)?$", # %d x %d
        r"^\s*(RGB\, HSV\, YUV\, YCbCr|RIFF|RONIN|Ryan Inch|Return)\s*$",
        r'^(\,\s)?(RGB[A]?)(\s(byte))?$',
        r'^(RGB[A]?)[\s]?(byte)?$',
        r'^(RGB[A]?)\([^\)]+\)$',
        r"^\s*(RK4|RRT|Redhat\/Fedora|RLE)\s*$",
        r"^\s*(SDL|SSE[\d]+|STL|SVG|ShaderFX|Sigma|Sin|Sobel|Sobol|Stucci|Studio|Subversion|setmessage|SubD|Subdiv|Silvio Falcinelli)\s*$",
        r"^\s*(Targa([\s]?Raw)?|Theora|TortoiseSVN|TxtIn|test1_|the|TAR-)\s*$",
        r"^\s*(URL|UV[s:]?|(\w )?&( \w)?|Uber)\s*$",
        r"^\s*(VD16|VP9|VRML2|Verlet|Vorbis|Voronoi([\s]F[\d]([-]F[\d])?)?|)\s*$",
        r"^\s*(WEBM \/ VP9|Web(3D|M)|Win(tab)?|Windows Ink|WGT-|ZX)\s*$",
        r"^\s*(X(/Y|YZ)?|Xvid|XY|XZ|YCbCr(\s\(ITU\s?\d+?\))?)\s*$",
        r"^\s*(Y(CC)?|YCbCr(\s\(Jpeg\))?|Z(ip)?|ZIPS)\s*$",
        r"^\s*(\w+(_\w+)+)\s*$", # MASK_MT_add
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

    # , ""
    ignore_start_with_list = [
        # "bpy", "bpy", "bl_info", "dx",
        #"", "", "", "", "",
        # "", "", "", "", "", "", "", "", "", "", "", "", "",
        "demohero, uriel, meta-androcto",
        "antonio vazquez (antonioya)",
        "vladimir spivak (cwolf3d)",
        "nuke (.chan)",
        #"a (alpha)",
        "(*x*\\ :sup:",
        #"+x, +y, +z, -x, -y, -z",
        #"",
        #"",
    ]

    keep_list = [
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

    keep_contains_list.sort()
    keep_list.sort()

    def isReverseOrder(msg):
        for w in Ignore.reverse_order_list:
            is_reverse = (re.search(w, msg, flags=re.I) is not None)
            if is_reverse:
                dd(f'isReverseOrder -> pattern:[{w}] msg:[{msg}]')
                return True
        return False

    def isKeepContains(msg):
        found_item = cm.findInSortedList(msg, Ignore.keep_contains_list)
        is_found = (found_item is not None)
        if is_found:
            return True
        else:
            return False

    def isKeep(msg):
        found_item = cm.findInSortedList(msg, Ignore.keep_list)
        is_found = (found_item is not None)
        if is_found:
            return True
        else:
            return False

    def isIgnored(msg):

        if not msg:
            return True

        # orig_msg = str(msg)
        # ex_ga_msg = cm.EXCLUDE_GA.findall(msg)
        # if (len(ex_ga_msg) > 0):
        #     msg = ex_ga_msg[0]
        #     dd("GA trimmed from:", orig_msg, msg)

        try:
            find_msg = msg.lower()
            is_keep = Ignore.isKeep(find_msg)
            if is_keep:
                return False

            is_allowed_contains = Ignore.isKeepContains(find_msg)
            if is_allowed_contains:
                return False

            is_ref_link = is_function = is_ignore_word = is_dos_command = is_ignore_start = False

            is_ref_link = cm.isLinkPath(find_msg)
            if not is_ref_link:
                is_function = (cm.FUNCTION.search(find_msg) is not None)
                if not is_function:
                    is_ignore_word = Ignore.isIgnoredWord(find_msg)
                    if not is_ignore_word:
                        is_dos_command = Ignore.isDosCommand(find_msg)
                        if not is_dos_command:
                            is_ignore_start = Ignore.isIgnoredIfStartsWith(find_msg)

            is_ignore = (is_function or
                        is_ignore_word or
                        is_dos_command or
                        is_ignore_start or
                        is_ref_link )
            # is_ignore = (is_ignore_word or is_dos_command or is_ignore_start)
            if is_ignore:
                #dd("checking for ignore")
                dict_ignore = {"is_ignore_word": is_ignore_word,
                               "is_dos_command": is_dos_command,
                               "is_ignore_start": is_ignore_start,
                               "is_function": is_function,
                               "is_ref_link": is_ref_link
                               }
                dd("IGNORING:", msg)
                pp(dict_ignore)
            return is_ignore
        except Exception as e:
            print(f'ERROR: {e}, msg:{msg}')
            raise e

    def isIgnoredIfStartsWith(text_line : str):
        if (text_line is None) or (len(text_line) == 0):
            return True

        for x in Ignore.ignore_start_with_list:
            is_starts_with = (text_line.lower().startswith(x.lower()))
            if is_starts_with:
                #dd("isIgnoredIfStartsWith:", x)
                return True
        else:
            return False

    def isIgnoredSimple(text_line : str):
        if (text_line is None) or (len(text_line) == 0):
            return True

        for x in Ignore.ignore_list:
            if len(x) == 0:
                continue

            p = re.compile(x, flags=re.I)
            m = p.search(text_line)
            is_found = (m != None)
            if (is_found):
                dd("[{}] matched [{}], escaped [{}]".format(text_line, x, escape_x))
                return True
        return False

    NUMBERS = re.compile(r"^\s*(([\d]+)([\,\.]?[\s]?[\d]+)*)+$")

    def isIgnoredWord(text_line : str):
        if (text_line is None) or (len(text_line) == 0):
            return True

        is_create_runtime_ignore_list = (Ignore.runtime_ignore_list == None)
        if is_create_runtime_ignore_list:
            Ignore.runtime_ignore_list = []
            for pattern in Ignore.ignore_list:
                if len(pattern) == 0:
                    continue

                m = re.compile(pattern, flags=re.I)
                Ignore.runtime_ignore_list.append(m)


        pattern = None
        try:
            for m in Ignore.runtime_ignore_list:
                is_found = (m.search(text_line) is not None)
                if is_found:
                    dd(f'isIgnoredWord: pattern:[{m.pattern}] [{text_line}]')
                    return True
            else:
                return False
        except Exception as e:
            dd(e)
            dd("isIgnoredWord ERROR:", text_line, " pattern:", pattern)
        return False

    def isDosCommand(text):
        if (text is None) or (len(text) == 0):
            return False

        for w in Ignore.DOS_COMMANDS:
            p = re.compile(r'^\b{}\b$'.format(w))
            is_dos_command = (p.search(text) != None)
            if is_dos_command:
                return True
        return False

    REF_LINK_WITHOUT_REFWORD = re.compile(r'\<([^<]+)\>')
    PATH_CHAR = re.compile(r'[\\\/]')
    file_path_pattern_list=[
        #r'^$',
        r'^(([\w]+|[~\.]|[\.]{2})[:]?)?([/]([^\]+)?)+)$',
    ]

    def isFilePath(text_line : str):
        if (text_line is None) or (len(text_line) == 0):
            return False

        has_path_characters = (Ignore.PATH_CHAR.search(text_line) is not None) and ('kbd' not in text_line)

        #check to see if any word is title case, ie. Selected/Unselected, in which case it's not a PATH
        if has_path_characters:
            word_list = text_line.split(dirsep)
            word : str = None
            for word in word_list:
                is_title_case = (word.istitle())
                if is_title_case:
                    return False

        starts_with_path_chars = text_line.startswith('~')
        ends_with_extensions = (cm.ENDS_WITH_EXTENSION.search(text_line) is not None)
        contain_spaces = (" " in text_line)
        is_path = (has_path_characters or starts_with_path_chars or ends_with_extensions) and not contain_spaces

        if is_path:
            dd("isFilePath", text_line)
            #exit(0)

        return is_path
