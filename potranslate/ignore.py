import sys
import re
from os import sep as dirsep
from os.path import pathsep
from common import Common as cm
from common import DEBUG, dd, pp

class Ignore:

    DOS_COMMANDS = [
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

    STB = r'[\"\'\(\<\{\[]'
    EDB = r'[\"\'\)\>\}\]]'
    # NUMB = r'([+-]?[\d]+(([\.\,][\d]+)*)+[\W]?)'
    NUMB = r"[+-]?[\d]+([\.\,][\d]+)?"
    # PATH = r'(([a-zA-Z][:]?)?) ([\\\/]+)(([\w-dd]+)?)*)'
    PATH = r'([a-zA-Z][:]?)?'
    MATH_OPS = r'[\s]?([\+\-\*\/\%\=x])[\s]?'
    runtime_ignore_list = None
    ignore_list = [
        r'^(\w+)([\-\.]\w+){2,}$', # hyphen ref links: "mesh-faces-tristoquads"
        # r'^\/?(\w+)(\/\w+){3,}$', # slash ref links: "/animation/armatures/bones/properties/bendy_bones"
        # r'^()$',
        # r'^((\w)([\//,\s]?)[\/,\s]?|=[\d]+([\.]?[\d]+)?)+$', #X, Y, Z  X=0.0, Y=0.0
        # r'^(HS[VL][\s]?[\/]?[\s]?)+$', #HSV/HSL
        r'^((\/[^\/]+)*)$',
        r'([\.](org|com|uk|ac))$', # '/render/freestyle/parameter_editor/line_style/modifiers/color/noise'
        # r'([\`\'\"\*\(]+)?(\%[\w])([\`\'\"\*\(]+)?',
        # r'^(/\[\`\'\"\*\(]+)?\%[\w](/\[\`\'\"\*\)]+)?$',
        r'^(([\.]([\/][^\w]?[\w]+[^\w]?)+[\/]?)+([\s][\.]+)?)$', #``./datafiles/locale/{language}/``
        r'^(GPL[\s\w][\d][+])$',
        r'^(A \(Alpha\))$',
        r'^([\w][\d])$',
        r'^[\w]\s?(\+|\-|\*|\/|\%|\=|\!\=|\>|\<|\>\=|\<\=|\=\=|\>\>|\<\<)\s?[\w]$', # A - B, A >= B
        # r'^(([+-]+\w)(,\s)?)+$', #"+X, +Y, +Z, -X, -Y, -Z",
        r'^(:[\w]+:)([\`]+([\/][\w]+[\/]?)*[\`]+)', # :doc:`/something/somethingelse`
        r'^(:ref:)([\`]+(\w+[-]?)+[\`]+)[\.]?$',
        r'^(:kbd:[\`]((Shift|Alt|Ctrl|\-)*([^\`]{1}|Tab|F(\d+)))[\`](,\s|\s-\s)?)+$', #:kbd:`Shift-Ctrl-R`
        r'^([\w]+)\/$', # rendering/
        # r'(^([\`]+)?[^\`]+)\.([\w]{2,5})([\`]+)?$', #file name
        r"^([\d]+)(px|khz)?$", # 1024x2048
        r"^([\d]+[x][\d]+)$", # 1024x2048
        r'^(\|[\w]+([\-][\w]+)?.*(:kbd\:.*Alt-Backspace).*)$',  # |dagger|: ``|``, :kbd:`Alt-Backspace`, ``-``
        # r'^(\<([^\<\>]+)\>)$', # <something>
        #r"^((Ctrl|Alt|Shift)?[\-](F[\d]+)?)$",  # Ctrl|Alt|Shif-F1-12
        # r'^([\*]?[\-]?[\d]+[\.][\w]{2,5})$', # *-0001.jpg
        #r'^(' + r'([\+\-]?[\w]{1})([\,][\s]([\+\-]?[\w]))*' + r')$',
        r"^([\d]+\s?bit[s]?)$",
        r"^(" + NUMB + MATH_OPS + r".*" + NUMB + r")$",
        r"^(" + r"(cd|mk|mkdir)[\s]+" + r".*" + r")$",
        r"^(" + STB + r"?([\+\-]?[\d]+[\W]?)" + EDB + r"?)$",  # (+-180°)
        r"^(" + STB + r"?(" + NUMB + r"(([\,]+[\s]+)?" + NUMB + r")*)+" + EDB + r"?)$", # (-1.0 - 1.0), (-X, -Y, -Z, X, Y, Z)
        r"^(\*\-[\d]+[\.][\w]{3})$", #*-0001.jpg
        r"^(Bone[ABC]|COR\-|Cartesian|Bfont|ABC)$",
        r"^(F[\d]{1,2})$", # F1-12
        r"^([\w]([\s]+[\w\d])+)$", # :kbd:`S X 0`
        #r"^(Shift[-][\S]{1})$",
        r"^(([\d]+(\.[\d]+)?)([\s]?[\/\+\-\*\%\=]?[\s]?([\d]+(\.[\d]+)?))*)$",
        r"^([\W]+)$",
        r"^([-]{2}([\w-]+)*)$",
        # r"^(\w+\:\w+)$", # geom:curve_tangent_normal
        r"^([\w\_\-]+\(([^\(\)]+)?\))$", # function_name(param1, param2)
        r"^([\"\'\*]?[\d]+(\.[\d]+)?([\s]?([K]?hz|bit[s]?))?[\"\'\*]?)$",
        r"^([\d]D)$",
        r"^([\"\'][\.\s]?[\S]{1}[\"\'])$",
        # r"^(#[\w\-\_]+)$",  # blender-coders <literal>#blender-coders</literal>
        r"^(#fmod\(frame, 24\) / 24)$",
        r"^(([\w]+)?([\.][\w]+)+)$", # bpy.context, bpy.context.object
        r"^(:(math|class):)\`([^\`]+)\`$",
        r"^(ITU \d+,)+",
        r"^(" + STB + r"?[+-][\w]{1}[,.])*([\s]?[+-][\w]{1})" + EDB + r"?$",  # "+X, +Y, +Z, -X, -Y, -Z"
        r"^([^\S]{1})$",  # single anything non spaces
        r"^(" + STB + r"?([+-]?[\d]+)([\,\.]?[\s]?[\d]+)*)+" + EDB + r"?$",  # 1,000 or 0.00001 or 1, 2, 3, 4
        r"^([\d]+[.,][\s]?)*[\d]+bit$",
        r"^([\d]?[\w]{1})$",  # "4D"
        r"^([\w\d]{2}\:){2}[\w\d]{2}\.[\w\d]{2}\.$",  # HH:MM:SS.FF
        r"^(\.[\w]{2,5})$",  # .jpg, .so
        r"^(htt[ps][^\S]+)$",
        r"^(jpg|png|int)$",
        r"^(\-\-render\-frame 1|\-(ba|con|noaudio|setaudio)|Mem)$",
        r"^(([\d]+([\.[\d]+)?)*(mil|mi|mm|km|cm|ft|m|yd|dm|st|pi))$",
        r"^(mov|location[0]|cd|ch|hm|asin|um|tan|self|atan|atan2|Arctan2|sRGB)$",
        r"^(AAC|AVI Jpeg|AVX|AaBbCc|Albedo|Alembic|AC3|Alt|AMD|Ascii|AVX[\d]?|Acrylic)$",
        r"^Alembic([\s\W|abc]+)$",
        r"^(Alpha|Alt|Apple macOS|Arch Linux|Ashikhmin-Shirley)$",
        r"^(AVIJPEG|AVIRAW|BMP|DDS|DPX|IRIZ|JACK|JP2|RAWTGA|TGA|TIFF|[+-]<frame>|)$",
        r"^(B\-Spline|BSDF|BSSRDF|BU|BVH|Babel|Bezier|Bindcode|Bit[s]?|BkSpace|Bksp)$",
        r"^(Blackman\-Harris|Blosc|Byte\([s]*\)|Bytecode|Bézier|Backspace|(Blender\s(\d+[\d\.]+)))$",
        r"^Blender\([\s\d\.]+\)|Blender_id[\W]?$",
        r"^(CCEN|CPU|CUDA|Catmull\-(Clark|Rom)|Catrom|Chebychev|Christensen\-Burley|Cineon|Collada)$",
        r"^(Ctrl|Cycles|Cycles:|Cinema(\s\(\d+\))?)$",
        r"^(DNxHD|DOF|Debian\/Ubuntu|Deflate|Del|de|debian|Delete|Delta([\s][\w])?)$",
        r"^([^\w]+log.*wm.*)$",
        r"^(Djv|Doppler|Dots\/BU|Dpi|DWAA)$",
        r"^(EWA|Epsilon|Embree|Esc|exr|FBX|Euler|FELINE|FFT|FSAA|Flash|FrameCycler|Français|msgfmt|fr_FR|Enter|Euler\s?\(?\w{1,3}?\)?|Float[\d]?)$",
        r"^((GGX|GLSL|GPU)[s:]|Gamma[s:]?|Ge2Kwy5EGE0|Gizmo[s:]|GPL|GGX|GLSL|Gizmo[\s]?[\w]?)$",
        r"^(H\.264|Hosek \/ Wilkie|HuffYUV|Hyperbolic[\s]?(Sine|Cosine)|Hosek \/ Wilkie(\s\d+)?|HDRI[s]?)$",
        r"^(ID|Ins|JPEG 2000|(ITU(\s\d+)?)|Internet[\w\W]|iScale)$",
        r"^(KDE|K1, K2|Kirsch|komi3D)$",
        r"^(Lennard\-Jones|LimbNode|Linux|Log|Look[\s]?Dev(HDRIs)?)$",
        r"^MPEG([\-|\d]+)|MatCaps$",
        r"^(MIS|MPlayer|(MS|Microsoft)?[-]?Windows|Makefile|Makefile|Manhattan|Matroska|Mega|Minkowski(\s[\d]+)?|Minkowski \d+\/\d+|Mitch|Mono|Musgrave)$",
        r"^(NDOF((\W)|[\s]?(ESC|Alt|Ctrl|Shift))?|NURBS|Nabla|Ndof|Nabla|Null|NVIDIA|nn|Nishita)$",
        r"^(OBJ|OSkey|Ogawa|Ogg[\s]?(Theora)?|Open(AL|CL|EXR|MP|Subdiv|VDB)+|Opus|ObData|ILM\'s OpenEXR|OpenEXR|Ozone|OptiX)$",
        r"^PAINT_GPENCILEDIT_GPENCILSCULPT_.*$",
        r"^(P(CM|LY|NG)|Pack Bits|Poedit|Preetham|Prewitt|PBR|PolyMesh|PO|pip|pip3|PIZ|PXR24|pc2|Preetham(\s?\d+)?|Python(\:\s[\.\%s]+)?)$",
        r"^(QuickTime|quasi\-)$",
        r"^(\d+[x]?)$", # 16x
        r"^(\%\d+[\w]?)$", # %14s
        r"^(\%[d](x%[d])?)$", # %dx%d
        r"^\%d(\s\w\s\%d)?(\W\s?)?$", # %d x %d
        # r"^(RGB[\w]?)$",
        r"^(RGB\, HSV\, YUV\, YCbCr|RIFF|RONIN|Ryan Inch|Return)$",
        r'^(\,\s)?(RGB[A]?)(\s(byte))?$',
        r'^(RGB[A]?)[\s]?(byte)?$',
        r'^(RGB[A]?)\([^\)]+\)$',
        r"^(RK4|RRT|Redhat\/Fedora|RLE)$",
        r"^(SDL|SSE[\d]+|STL|SVG|ShaderFX|Sigma|Sin|Sobel|Sobol|Stucci|Studio|Subversion|setmessage|SubD|Subdiv|Silvio Falcinelli)$",
        r"^(Tab|Targa([\s]?Raw)?|Theora|TortoiseSVN|TxtIn|test1_|TAR-)$",
        r"^(URL|UV[s:]?|U & V|Uber)$",
        r"^(VD16|VP9|VRML2|Verlet|Vorbis|Voronoi([\s]F[\d]([-]F[\d])?)?|)$",
        r"^(WEBM \/ VP9|Web(3D|M)|Win(tab)?|Windows Ink|WGT-|ZX)$",
        r"^(X(/Y|YZ)?|Xvid|XY|XZ|YCbCr(\s\(ITU\s?\d+?\))?)$",
        r"^(Y(CC)?|YCbCr(\s\(Jpeg\))?|Z(ip)?|ZIPS)$",
        r"^(\w+(_\w+)+)$", # MASK_MT_add
        r"^[\-]*\d+(\.[\w]{2,5})$",  # -0001.jpg
        r"^[\W]{1}$",
        r"^\w([\s]?[<]?[\*\/\+\-\=][>]?[\s]?\w)+$",  # A * B + C; A -> B
        r"^(\"fr\"[:]?|\"fr\": \"Fran&ccedil;ais\"|)$",
        r"^\*(\.[\w]{2,5})$",  # *.jpg
        r"^\.bashrc$",
        r"^(the quick|brown fox|jumps over|the lazy dog)$",
        r"^\:([\w\-\_]+)\:$",
        r"^\:sup\:\`™\`$",
        r"^\|([\w\-\_]+)\|$",
        r"^\|[^\|]+\|$",  # |tick|cross|
        r"^(bItasc|bin|bit[s]?|bl\*er|blendcache_[filename]|blender \-[drE]+([\s]+help)?|blender_doc|blender_api)$",
        r"^(bpy\.(context|data|ops)|bpy\.([\w\.\-\_]+)|byte([s]?))$",
        r"^(cd|mkdir|ctrl)$",
        r"^(dam|deg|developer\.blender\.org|dir\(\)|dm|dx)$",
        r"^(eevee|emission\(\)|esc|etc[\.]+)$",
        r"^(f\(\d+\)|fBM|flac|fr|fr\/|ft)$",
        r"^gabhead, Lell, Anfeo, meta-androcto$",
        r"^(git([\s]+[^\`]+)?|glTF 2\.0)$",
        r"^(hm|html|iTaSC|jpeg|SubRip)$",
        r"^[\%s\s\'\:]+$", # %s: %s
        r"^(kConstantScope|kUniformScope|kUnknownScope|kVaryingScope|kVertexScope|kFacevaryingScope|kbd)$",
        r"^(mathutils|menuselection|microfacet_ggx\(N, roughness\)|microfacet_ggx_aniso\(N, T, ax, ay\))$",
        r"^(microfacet_ggx_refraction\(N, roughness, ior\)|mode=\'RENDER\'|mp[\d]+|msgstr|MPEG-4 \(divx\))$",
        r"^(oren_nayar\(N, roughness\)|wm\.operators\.\*|var all_langs \=(.*)|)$",
        r"^(Poedit|PIP|pagedown|pageup|pgdown|pgup|pip[\d]?|pot|print\(\)|unregister|)$",
        r"^(quit\.blend|path:ray_length|render\-output\-postprocess|temp\-dir)$",
        r"^(rig_ui|roaoao|rotation_[xyz]|resolution_[xyz]|reflection\(N\)|rest_mat|rst|refraction\(N, ior\))$",
        r"^(_socket[\.](py|pyd)|Subversion|s\-leger|sequencer\-edit\-change|sin\(x\) \/ x|sqrt|sqrt\([\d]?\)|svn)$",
        r"^(tab|TortoiseSVN|timeline\-playback|ui\-data\-block|view3d\-viewport\-shading|var[\s]+|wav)$",
        r"[\d]+([\.][\d]+[\d\w]?)\s[\-]+\s(Tháng|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)",
    ]

    # , ""
    ignore_start_with_list = [
        # "bpy", "bpy", "bl_info", "dx",
        #"", "", "", "", "",
        # "", "", "", "", "", "", "", "", "", "", "", "", "",
        "Demohero, uriel, meta-androcto",
        "Antonio Vazquez (antonioya)",
        "Vladimir Spivak (cwolf3d)",
        "Nuke (.chan)",
        "Houdini",
        "Nuke",
        "./",
        #"A (Alpha)",
        "(*x*\\ :sup:",
        #"+X, +Y, +Z, -X, -Y, -Z",
        #"",
        #"",
    ]

    keep_list = [
        "Add-on",
        "Off-Axis",
        "Toe-in",
        "Sub-Target",
        "Foam + Bubbles",
        "Spray + Foam + Bubbles",
        "Fire + Smoke",
        "Sub-Steps",
        "Z-Axis",
        "Normal/View"
        "F-Curve",
        "F-Modifier",
        "Counter-Clockwise",
        "Normal/Surface",
        "left/right",
        "top/bottom",
        "link/append",
        "fog/mist",
        "Exterior/Interior",
        "Flat/Smooth",
        "Mirror%s",
        "Un-Subdivide",
        "Un-Comment",
        "Shrink/Fatten",
        "Smoke + Fire",
        "Expand/Contract",
        "Open/Close",
        "Hide/Show",
        "Co-planar",
        "Hide/Unhide",
        "Lock/Unlock",
        "Major/Minor",
        "Click-Extrude",
        "Front/Back",
        "rotation/scale",
        "BLENDER_VERSION",
        "MPEG Preseek",
        "0 or 1",
        "anti-aliases",
        "anti-aliased",
        "anti-aliasing",
        "reflect/refract",
        "scattering/absorbtion",
        "inside/outside",
        "Dots/BU",
        "Model by © 2016 pokedstudio.com",
        "Video: From Blender 1.60 to 2.50",
        #"",
        #"",
    ]

    reverse_order_list = [
        r'khóa.*[\d]+(\s[\-]{2}\s(key))',
        r'\"Cơ Sở -- Basis\"',
        r'^\"xương -- bone\"$',
        r'^\"xương\"$',
        r'^\"bone\"$',
        r'xương\.[\d]+',
        r'bone\.[\d]+',
    ]
    keep_contains_list = [
        "xương",
        "bone",
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "Novemeber",
        "December",
        "|first|",
        "|previous|",
        "|rewind|",
        "|play|",
        "|next|",
        "|last|",
        "|pause|",
        "HH:MM:SS.FF",
        # "",
        # "",
    ]

    def isReverseOrder(msg):
        for w in Ignore.reverse_order_list:
            is_reverse = (re.search(w, msg, flags=re.I) is not None)
            if is_reverse:
                dd(f'isReverseOrder -> pattern:[{w}] msg:[{msg}]')
                return True
        return False

    def isKeepContains(msg):
        for term in Ignore.keep_contains_list:
            is_found = (term.lower() in msg.lower())
            if is_found:
                return True
        else:
            return False

    def isKeep(msg):
        for term in Ignore.keep_list:
            is_found = (term.lower() == msg.lower())
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
            is_keep = Ignore.isKeep(msg)
            if is_keep:
                return False

            is_allowed_contains = Ignore.isKeepContains(msg)
            if is_allowed_contains:
                return False

            is_ref_link = cm.isLinkPath(msg)
            is_ignore_word = Ignore.isIgnoredWord(msg)
            is_dos_command = Ignore.isDosCommand(msg)
            is_ignore_start = Ignore.isIgnoredIfStartsWith(msg)
            #is_ignore_path = Ignore.isFilePath(msg)

            is_ignore = (is_ignore_word or
                        is_dos_command or
                        is_ignore_start or
                        is_ref_link )
                        #         or is_ignore_path)
            # is_ignore = (is_ignore_word or is_dos_command or is_ignore_start)
            if is_ignore:
                #dd("checking for ignore")
                dict_ignore = {"is_ignore_word": is_ignore_word,
                               "is_dos_command": is_dos_command,
                               "is_ignore_start": is_ignore_start,
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

    NUMBERS = re.compile(r"^(([\d]+)([\,\.]?[\s]?[\d]+)*)+$")

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
