#!/usr/bin/env python3
import sys
sys.path.append("/home/htran/bin/python")

from collections import OrderedDict, defaultdict

#from stack import Stack
import datetime
from time import gmtime, strftime
from pytz import timezone
import math
import re
#from Levenshtein import distance
from difflib import SequenceMatcher as SM
#from fuzzywuzzy import fuzz as fz
from pprint import pprint as PP
# from bs4 import BeautifulSoup as BS
import os
import html
from queue import Queue as Q
from pyparsing import *
from collections import Counter
#from subprocess import PIPE, Popen, run
import subprocess as sub


alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

class TextMap(OrderedDict):
    def __init__(self, text=None, dic=None):
        self.dictionary = dic
        self.text = text
        self.wordsep = re.compile(r'[^\ ]+', re.I)

    def genmap(self):
        self.clear()
        part_list = []
        loc_dic = getLocationList(self.wordsep, self.text)
        loc_key = list(loc_dic.keys())

        max_len = len(loc_dic)
        for step in range(1, max_len):
            for i in range(0, max_len):
                l=[]
                for k in range(i, min(i+step, max_len)):
                    loc = loc_key[k]
                    # print(f'step:{step}; i:{i}; k:{k}, loc:{loc}')
                    l.append(loc_key[k])

                s = []
                for loc in l:
                    word = loc_dic[loc]
                    s.append(word)
                t = " ".join(s)
                print(f's location:{l}, text:{t}')

                s_len = len(s)
                ss = l[0][0]
                ee = l[s_len-1][1]
                k = (len(t), ee)
                v = ((ss, ee), t)
                entry=(k, v)
                is_in = (entry in part_list)
                if not is_in:
                    part_list.append(entry)

        sorted_partlist = list(reversed(sorted(part_list)))
        for e in sorted_partlist:
            k, v = e
            dict_entry = {k: v}
            self.update(dict_entry)

    def blindTranslation(self, text=None, dic=None):
        translated_dic = OrderedDict()
        is_new_text = (self.text != text)

        if is_new_text:
            self.text = text
            self.genmap()

        if dic:
            self.dictionary = dic

        translated_dic = OrderedDict()
        for k, v in self.items():
            loc, orig_sub_text = v
            has_tran = (orig_sub_text in self.dictionary)
            if not has_tran:
                continue
            tran_sub_text = self.dictionary[orig_sub_text]
            ss, ee = loc
            entry = {ee: (ss, ee, tran_sub_text)}
            translated_dic.update(entry)

        sored_translated = list(reversed(sorted(translated_dic.items())))

        tran_msg = str(msg)
        for k, v in sored_translated:
            ss, ee, tran_sub_text = v
            left = tran_msg[:ss]
            right = tran_msg[ee:]
            tran_msg = left + tran_sub_text + right

        return tran_msg


class WCKLCIOrderedDict(defaultdict):
    class Key(str):
        def __init__(self, key):
            str.__init__(key)

        def __hash__(self):
            k = self.lower()
            hash_value = hash(k)
            # _(f'key:{k}, hash_value:{hash_value}')
            return hash_value

        def __eq__(self, other):
            local = self.lower()
            extern = other.lower()
            cond = (local == extern)
            # _(f'__eq__: local:{local} extern:{extern}')
            return cond

    def __init__(self, data=None):
        super(WCKLCIOrderedDict, self).__init__()
        if data is None:
            data = {}
        for key, val in data.items():
            self[key] = val

    def __contains__(self, key):
        key = self.Key(key)
        is_there = super(WCKLCIOrderedDict, self).__contains__(key)
        # _(f'__contains__:{key}, is_there:{is_there}')
        return is_there

    def __setitem__(self, key, value):
        key = self.Key(key)
        super(WCKLCIOrderedDict, self).__setitem__(key, value)


    def __getitem__(self, key):
        key = self.Key(key)
        return super(WCKLCIOrderedDict, self).__getitem__(key)

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]

#import AdvancedHTMLParser as AH
#from sphinx_intl import catalog as c
#from Levenshtein import distance as DS
#from PO.common import Common as cm
#from nltk import sent_tokenize

#p =re.compile(r':[\w]+:\`(?![\s\)\\.(]+)([\w \-]+)(\<([^<]+)\>)*(?<!([\s\:]))\`')
#GA_REF = re.compile(r'(:[\w]+:)*[\`]+(?![\s\)\.\(]+)([^\`\("\'\*\<]+)(((\s\<([^<]+)\>)*)|(\(([^(]+)\))*)(?<!([\s\:]))([\`]+)([\_]+)*')
#GA_REF = re.compile(r'(:\w+:)*[\`]+([^\`\<\>\<\(\)]+)(((\s\<([^\<\>]+)\>)*)|(\(([^(]+)\))*)(?<!([\s\:]))([\`]+)([\_]+)*')
#GA_REF = re.compile(r'[\`]*(:\w+:)*[\`]+(?![\s]+)([^\`\<\>\(\)]+)(((\s\<([^\<\>]+)\>)*)|(\([^\(\)]+\)))[\`]+')

GA_REF = re.compile(r'[\`]*(:\w+:)*[\`]+(?![\s]+)([^\`]+)(?<!([\s\:]))[\`]+[\_]*')
#ARCH_BRAKET = re.compile(r'[\(]+(?![\s\.\,\`]+)([^\(\)]+)[\)]+(?<!([\s\.\,]))')
AST_QUOTE = re.compile(r'[\*]+(?![\s\.\,\`\"]+)([^\*]+)[\*]+(?<!([\s\.\,\`\"]))')
DBL_QUOTE = re.compile(r'[\"]+(?![\s\.\,\`]+)([^\"]+)[\"]+(?<!([\s\.\,]))')
SNG_QUOTE = re.compile(r'[\']+(?![\`\s\.(s|re|ll|t)]+)([^\']+)[\']+')

LINK_WITH_URI=re.compile(r'([^\<\>\(\)]+\w+)[\s]+[\<\(]+([^\<\>\(\)]+)[\>\)]+[\_]*')
MENU_PART = re.compile(r'(?![\s]?[-]{2}[\>]?[\s]+)(?![\s\-])([^\<\>]+)(?<!([\s\-]))') # working but with no empty entries

WORD_ONLY_FIND = re.compile(r'\b[\w\-\_\']+\b')

ENDS_WITH_EXTENSION = re.compile(r'\.([\w]{2,5})$')
MENU_KEYBOARD = re.compile(r':(kbd|menuselection):')
MENU_TYPE = re.compile(r'^([\`]*:menuselection:[\`]+([^\`]+)[\`]+)$')
KEYBOARD_TYPE = re.compile(r'^([\`]*:kbd:[\`]+([^\`]+)[\`]+)$')
KEYBOARD_SEP = re.compile(r'[^\-]+')

WORD_ONLY = re.compile(r'\b([\w\.\/\+\-\_]+)\b')
REF_SEP = ' -- '
NON_WORD_ONLY = re.compile(r'^([\W]+)$')
NON_WORD = re.compile(r'([\W]+)')


DEBUG=True


def pp(object, stream=None, indent=1, width=80, depth=None, *args, compact=False):
    if DEBUG:
        pprint(object, stream=stream, indent=indent, width=width, depth=depth, *args, compact=compact)
        print('-' * 30)

def _(*args, **kwargs):
    if DEBUG:
        print(args, kwargs)
        print('-' * 30)

ignore_list = [
        "(htt)([ps]{1}).*",
        "Poedit",
        "([.*]{1})",  # single anything
        "bpy\.([\w\.\-\_]+)",
        "\:([\w\-\_]+)\:$",
        "\|([\w\-\_]+)\|$",
        "[\W]{1}$",
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
        "\|[^\|]+\|",  # |BLENDER_...|
        "#[\w\-\_]+",  # blender-coders <literal>#blender-coders</literal>
        "Babel",
        "Ge2Kwy5EGE0",
        "([\+\-])*(([\d\.]+))",  # simple number
        "TortoiseSVN",
        "Poedit",
        "\:sup\:\`™\`",
        "(([\w]+)\.([^\.]+))+",
        "rst",
        "pot",
        "html",
        "^svn$",
        "^git$",
        "msgstr",
        "\.bashrc",
        "bin",
        "Français",
        "Redhat/Fedora",
        "Arch Linux",
        "\"fr\": \"Fran&ccedil;ais\"",
        "[\-]*\d+(\.[\w]{2,5})", # -0001.jpg
        "\*(\.[\w]{2,5})",  # *.jpg
        "(\.[\w]{2,5})",  # .jpg, .so
        "(mil|mile|millimeter|meter|meters|mi|location[0]|cd|ch|cm|asin|atan|atan2|st|sRGB)",
        "(k[\w]+)",
        "(:math:)\`[^\`]+\`",
        "(([\w]+[\s]*[\+\-\*\/\%][\s]*)*([\w]+[\s]*[=][\s]*[\w]+))", #formular a + b * c = d
        "([\w]+[\s]*[=][\s]*[\w]+)*(([\s]*[\+\-\*\/\%][\s]*[\w]+)+)", #formular a = b * c / d
    ]

FORMULAR = re.compile(r'([\=\+\-\%\*\/])')



def getLocationList(pat, text):
    matching_list = {}
    for m in pat.finditer(text):
        s = m.start()
        e = m.end()
        orig = m.group(0)
        k = (s, e)
        entry = {k: orig}
        matching_list.update(entry)
    return matching_list


class HoldString(list):
    GLOBAL_COUNT: int = 0
    def __init__(self, txt):
        self.name = str(self.getNextCount())
        if txt:
            self.append(txt)

    def getNextCount(self):
        c = HoldString.GLOBAL_COUNT + 1
        HoldString.GLOBAL_COUNT = c
        return c
        #p = FORMULAR.search("1 + 2 - 3")
        #print(p)
        #return 1

    def __repr__(self):
        result = "[" + self.name + "]"
        result += "{"
        result += ", ".join(self)
        result += "}"
        return result

class test(object):
    timenow=None

    def __init__(self):
        self.your_name="Hoang Duy Tran"
        self.your_email="hoangduytran1960@googlemail.com"
        self.your_id="{} <{}>".format(self.your_name, self.your_email)
        self.translation_team="London, UK {}".format(self.your_email)
        self.language_code="vi"
        self.re_language_code="\"Language: \\\\n\"\n".format(self.language_code)

        self.count=0
        self.dic = {
            #"^Standard image input.$":"Đầu vào tiêu chuẩn của hình ảnh.",
            #"^Standard image output.$":"Đầu ra tiêu chuẩn của hình ảnh.",
            "FIRST AUTHOR.*SS>":self.your_id,
            "Last-Translator.*>":"Last-Translator: {}".format(self.your_id),
            #"PO-Revision-Date.*[[:digit:]]\{4\}":self.timeNow(),
            #"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE":self.timeNow(),
            "Language-Team:.*>":"Language-Team: {}".format(self.translation_team),
            "\"MIME-Version":"{}\"MIME-Version".format(self.re_language_code)
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
        }

        self.YOUR_NAME="Hoang Duy Tran"
        self.YOUR_EMAIL="hoangduytran1960@googlemail.com"
        self.YOUR_ID="{} <{}>".format(self.YOUR_NAME, self.YOUR_EMAIL)
        self.YOUR_TRANSLATION_TEAM="London, UK <{}>".format(self.YOUR_EMAIL)
        self.YOUR_LANGUAGE_CODE="vi"

        #the replace string for revision date, which include the time_now value
        self.po_revision_date_value="PO-Revision-Date: {}".format(self.getTimeNow())

        #the list of pattern to find and the value strings to be replaced
        #"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n
        self.pattern_list= {
            r"FIRST AUTHOR.*SS\>":self.YOUR_ID,
            r"Last-Translator.*\>":"Last-Translator: {}".format(self.YOUR_ID),
            r"PO-Revision-Date.*[[:digit:]]\{4\}":self.po_revision_date_value,
            r"PO-Revision-Date: YEAR.*ZONE":self.po_revision_date_value,
            r"Language-Team:.*\>":"Language-Team: {}".format(self.YOUR_TRANSLATION_TEAM)
        }

        #This is for the language line. This line is required by POEdit, if you're using it for editing PO files.
        #Inserting this line before the MIME-Version.
        self.re_language_code=r'Language:.*{}'.format(self.YOUR_LANGUAGE_CODE)
        self.language_code=r'"Language: {}\\n"\n'.format(self.YOUR_LANGUAGE_CODE)
        self.pattern_insert={
            r"\"MIME-Version":"{}\"MIME-Version".format(self.language_code)
        }

        self.RE_COMMENTED_LINE=r'^#~.*$'


    def getTimeNow(self):
        local_time=timezone('Europe/London')
        fmt='%Y-%m-%d %H:%M%z'
        loc_dt=local_time.localize(datetime.datetime.now())
        formatted_dt=loc_dt.strftime(fmt)
        return formatted_dt

    def isFormular(self, msg):
        result = FORMULAR.split(msg)
        print(msg, result)
        return result

    def isIgnoredWord(self, text_line : str):
        if (text_line is None) or (len(text_line) == 0):
            return True

        try:
            for x in ignore_list:
                m = re.compile(r'^{}$'.format(x), flags=re.I)
                is_found = (m.search(text_line) is not None)
                if is_found:
                    _("[{}] matched [{}]".format(text_line, x))
                    return True
        except Exception as e:
            _(e)
            _("isIgnoredWord ERROR:", text_line)
        return False

    def timeNow(self):
        if (test.timenow == None):
            local_time=timezone('Europe/London')
            fmt='%Y-%m-%d %H:%M%z'
            loc_dt=local_time.localize(datetime.datetime.now())
            formatted_dt=loc_dt.strftime(fmt)
            test.timenow = formatted_dt
        return test.timenow

    def test01(self):
        index = 0
        for key, value in self.dic.items():
            is_first = (index == 0)
            if (is_first):
                print("Dealing with first:{} => {}".format(key, value))
            else:
                print("Dealing with:{} => {}".format(key, value))
            index += 1

    def readText(self, file_path):
        try:
            with open(file_path) as in_file:
                data = in_file.read()
                in_file.close()
            return data
        except Exception as e:
            print("Exception readText:{}".format(file_path))
            raise e

    def getByKeyword(self, keyword, text):
        #<title>Import</title>
        result_list=[]
        pattern = r"<{}[^>]*>([^\.\!<]+)</{}>".format(keyword, keyword)
        titles = re.compile(pattern)
        m  = titles.findall(text)

        pattern = r"<{}[^>]*>([^\.\!<]+)*<".format(keyword)
        titles = re.compile(pattern)
        n  = titles.findall(text)

        is_found_m = (m != None)
        is_found_n = (n != None)

        if (is_found_m):
            result_list= result_list + m

        if (is_found_n):
            result_list= result_list + n

        is_found = (len(result_list) > 0)
        if (is_found):
            result_list = sorted(result_list)
            #print("sorted:{}".format(result_list))
            unique_set = sorted(set(result_list))
            #print("set:{}".format(unique_set))
            result_list = sorted(list(unique_set))
            #print("back to list:{}".format(result_list))
            return result_list
        else:
            return None

    def test_0001(self):
        file_name = "/home/htran/example_rst_content.txt"
        data = self.readText(file_name)

        kw = ['title', 'field_name', 'term', 'strong', 'rubric']
        l = []
        for k in kw:
            result = self.getByKeyword(k, data)
            if (result != None):
                l.extend(result)
        l = sorted(l)
        print(l)

    def test_0002(self):
        t1="-s"
        t2="``{}``".format(t1)
        t3="--"
        t4="``{}``".format(t3)
        t5="-12345.67"
        t6="``{}``".format(t5)
        t7="-a and -b"
        t8="``{}``".format(t7)


        pf=re.compile(r"(?P<rst_box>[\`]+)(.*?)(?P=rst_box)$")
        po=re.compile(r"(^[-]+)([a-zA-Z]{0,1})$")

        pp = re.compile(r"(^[-]+)([a-zA-Z]{0,1})$")
        #test_item=t4
        #ml = pf.findall(test_item)
        #print("ml:{}".format(ml))
        #if (len(ml) > 0):
            #found_item=ml[0][1]
            #print("ml[0][1]:{}".format(ml[0][1]))
            #mo=po.search(found_item)
            #if (mo != None):
                #print("mo[0]:{}".format(mo[0]))
        #else:
            #print("test_item:{}".format(test_item))
            #mo=po.search(test_item)
            #if (mo != None):
                #print("mo[0]:{}".format(mo[0]))

    def test_0003(self):
        t = "(:menuselection:`Armature --> Bone Roll --> Recalculate`)"
        p = re.compile(r":menuselection:`(.*)`")
        m = p.findall(t)
        tt = m[0]
        print("m:{}".format(m[0]))
        ll = tt.split("-->")
        print("ll:{}".format(ll))
        for w in ll:
            w = w.strip()
            wrp = "({})".format(w)
            if (t.find(wrp) < 0):
                t = (t.replace(w, wrp))
        print("new t:{}".format(t))

    def test_0004(self):
        p= re.compile(r"(?<=:doc:`\/)(.*)`$")
        t1=":doc:`/sculpt_paint/index/what/is/this`"
        t2=":doc:`Glossary </glossary/index>`"
        m = p.search(t2)
        print(m)

    def test_0005(self):
        t_list = ["Đổi Tỷ Lệ Mép Nhòe :kbd:`Alt-S`",
        "Móc :kbd:`K`",
        "Hiển Thị Tay Cầm :kbd:`Ctrl-H`",
        "Hiển Thị/Ẩn Giấu Cảnh Kết Xuất :kbd:`F11`",
        "Sức Mạnh/Cường Độ :kbd:`Shift-F`",
        "Bật/Tắt Khả Năng Biên Soạn của Kênh :kbd:`Tab`",
        "Lật Đảo Tự Do/Thẳng Hàng :kbd:`V T`",
        "Tùy Chọn của Người Dùng :kbd:`Ctrl-Alt-U`; :kbd:`Ctrl-Alt-A`",
        "Hiển thị tất cả các Trình tự :kbd:`Home`",
        "Thu-Phóng :kbd:`Ctrl-MMB`, :kbd:`Wheel`",
        "Hiển Thị Toàn Bộ  -- Show All :kbd:`Alt-H`",
        ":kbd:`LMB`",
        ":kbd:`MMB`",
        ":kbd:`Numpad0`",
        ":kbd:`Wheel`",
        ":kbd:`NumpadPlus`",
        ":kbd:`OS-Key`",
        ":kbd:`D-LMB`",
        "Cường Độ -- Strength :kbd:`Ctrl-F`/:kbd:`Shift-Bánh Xe (Wheel)`",
        ":kbd:`Shift`, :kbd:`Ctrl`, :kbd:`Alt`",
        ":kbd:`Bàn Số 0` (`Numpad0`) tới :kbd:`Bàn Số 9` (`Numpad9`), :kbd:`Bàn Số +` (`NumpadPlus`)",
        ":kbd:`Bánh Xe`",
        "Phím Chức Năng (F-Keys) (:kbd:`F5` - :kbd:`F10`)",
        "Phím Hệ Điều Hành (:kbd:`OS-Key`) (còn được biết với những cái tên khác như *phím Cửa Sổ* (``Windows-Key``), phím Lệnh (``Cmd``) hoặc phím Quản Lý (``Super``))",
        ":kbd:`Ctrl-Alt-T`"
        "Use Grab/Move :kbd:`G`, Rotate :kbd:`R`, Scale :kbd:`S`, to transform the cube."
        ]

        p= re.compile(r":kbd:`.*`")
        #p= re.compile(r"(:kbd:`)(?P<word>[\w\d]+)(\-(?P=word))*(`)")
        p1=re.compile(r":kbd:`(?P<key>[\w\d]+)|(?P<modifier>(Enter|Ctrl|Alt|Shift|Home|Insert|PageUp|PageDown|Delete)+[-+](?P=key))*`")
        pex_vn_part=re.compile(r"(NCT)|(NCP)|(NCG)|(LMB)|(MMB)|(RMB)|(Numpad)|(Wheel)|(OS)|(Win)")
        pdel=re.compile(r"(\.)|(,)|(;)|(and)|(or)|(--)")


        is_remove_pattern = False
        for text_line in t_list:
            found_string = ""
            has_trans=(text_line.find(" -- ") > 1)
            if (has_trans):
                text_line = text_line.split(" -- ")[0]
            m = p.search(text_line)
            if (m != None):
                is_remove_pattern = True
                print("Any Pattern:[{}]".format(m.group(0)))
                found_string=m.group(0)
                n=pex_vn_part.search(found_string)
                if (n != None):
                    print("Exclude Pattern:[{}]".format(n.group(0)))
                    is_remove_pattern = False

            print("Text line before remove:[{}]".format(text_line))
            if (is_remove_pattern):
                text_line = text_line.replace(found_string, "").strip()
                print("Text line after removed:[{}]".format(text_line))
            #m1 = p1.search(found_string)
            #print(m1.group(0))

    def fuzzyTermMatch(self, s1, s2):
        match_pat=re.compile(r".*({}).*".format(s1))
        match_m = match_pat.search(s2)
        is_found = (match_m != None)
        if (is_found):
            return match_m.group(0)
        else:
            return None

    def fuzzyWordMatch(self, s1, s2):
        pat=re.compile(r"\W*(\w+)\W*")
        s1_word_list=pat.findall(s1)
        s2_word_list=pat.findall(s2)
        #for each word in s1_word_list, find occurence in S2 and distance between matches in s2, the closer have higher match rate
        s2_string = " ".join(s2_word_list)
        s2_word_list_len = len(s2_string)
        distance_list=[]
        for s1_w in s1_word_list:
            try:
                index = s2_string.index(s1_w)
            except ValueError as e:
                index = s2_word_list_len
            percentage = (index / s2_word_list_len) * 100
            distance_list.append(percentage)

        fuzzyDistance = 100
        for dist in distance_list:
            fuzzyDistance -= dist
        fuzzyDistance = max(0.0, fuzzyDistance)
        return fuzzyDistance
        #print("s1_word_list:{}".format(s1_word_list))
        #print("s2_word_list:{}".format(s2_word_list))
        #print("distance_list:{}".format(distance_list))
        #print("fuzzyDistance:{}".format(fuzzyDistance))
        #print("=" * 50)

    def fuzzySearch(self, search_text_line, possible_list):
        match_list=[]
        for index, entry in enumerate(possible_list):
            candicate, ratio = entry
            fuzzy_dist = self.fuzzyWordMatch(search_text_line, candicate)
            match_list.append((fuzzy_dist, index))
        sorted_list = sorted(match_list, reverse=True)
        print("sorted_list:{}".format(sorted_list))
        return match_list

    def test_0006(self):
        data_list=[('Examples', 44,':ref:`Shape Keys <animation-shape_keys-index>`', 39,':ref:`Armatures <armatures-index>`', 26,':ref:`Constraints <constraints-index>`', 23,':ref:`Drivers <animation-drivers-index>`', 18,':ref:`Object Modifiers <modifiers-index>`', 17,'To control the kinds of motions that make sense and add functionality to the rig.', 16,'To support different target shapes *(such as facial expressions)* to be controlled.', 16,'Rigging often involves using one or more of the following features:', 11,'This allows mesh objects to have flexible joints and is often used for skeletal animation.', 10,'Mesh deformation can be quite involved, there are multiple modifiers that help control this.', 10,'So your rig can control many different values at once, as well as making some properties automatically update based on changes elsewhere.', 10,'An armature is often used with a modifier to deform a mesh for character animation.', 9,'Rigging can be as advanced as your project requires, rigs are effectively defining own user interface for the animator to use, without having to be concerned the underlying mechanisms.', 7,'Rigging is a general term used for adding controls to objects, typically for the purpose of animation.', 5,'A camera rig can be used instead of animating the camera object directly to simulate real-world camera rigs *(with a boom arm, mounted on a rotating pedestal for example, effects such as camera jitter can be added too).*', 5,"The content of this chapter is simply a reference to how rigging is accomplished in Blender. It should be paired with additional resources such as Nathan Vegdahl's excellent (and free!) introduction to the fundamental concepts of character rigging, `Humane Rigging <https://www.youtube.com/playlist?list=PL3wFcRXImVPOQpi-wi7uriXBkykXVUntv>`__.", 5)]
        search_term="Shape Keys"

        self.fuzzySearch(search_term, data_list)

    def test_0007(self):
        s1="menuselection:`Collapse`"
        s2_1=":menuselection:`Mesh --> Delete`"
        s2_2=":kbd:`Alt-M`, :menuselection:`Collapse`"

        pat=re.compile(r"\W*(\w+)\W*")
        s1_word_list=pat.findall(s1)
        s2_word_list=pat.findall(s2)
        #for each word in s1_word_list, find occurence in S2 and distance between matches in s2, the closer have higher match rate
        s2_string = " ".join(s2_word_list)
        s2_word_list_len = len(s2_string)
        distance_list=[]
        for s1_w in s1_word_list:
            try:
                index = s2_string.index(s1_w)
            except ValueError as e:
                index = s2_word_list_len
            percentage = (index / s2_word_list_len) * 100
            distance_list.append(percentage)


    def test_0008(self):
        s1="menuselection:`Collapse`"
        s2_1=":menuselection:`Mesh --> Delete`"
        s2_2=":kbd:`Alt-M`, :menuselection:`Collapse`"
        d1 = distance(s1, s2_1)
        d2 = distance(s1, s2_2)
        print("s1:{}, s2_1:{}, d1:{}".format(s1, s2_1, d1))
        print("s1:{}, s2_2:{}, d2:{}".format(s1, s2_2, d2))

    def test_0009(self):
        s1="menuselection:`Collapse`"
        s2_1=":menuselection:`Mesh --> Delete`"
        s2_2=":kbd:`Alt-M`, :menuselection:`Collapse`"
        d1 = distance(s1, s2_1)
        d2 = distance(s1, s2_2)

        print("Levenshtein s1:{}, s2_1:{}, d1:{}".format(s1, s2_1, d1))
        print("Levenshtein s1:{}, s2_2:{}, d2:{}".format(s1, s2_2, d2))

        d1 = fz.ratio(s1, s2_1)
        d2 = fz.ratio(s1, s2_2)
        print("fuzzy s1:{}, s2_1:{}, d1:{}".format(s1, s2_1, d1))
        print("fuzzy s1:{}, s2_2:{}, d2:{}".format(s1, s2_2, d2))


        d1=SM(None, s1, s2_1).ratio()*100
        d2=SM(None, s1, s2_2).ratio()*100
        print("SM s1:{}, s2_1:{}, d1:{}".format(s1, s2_1, d1))
        print("SM s1:{}, s2_2:{}, d2:{}".format(s1, s2_2, d2))

        #pat=re.compile(r"\W*(\w+)\W*")
        #s1_word_list=pat.findall(s1)
        #s2_word_list=pat.findall(s2)

    def binaryWord(self, search_word_list, data_word_list):
        binary_data_list=[]
        for index, data_word in enumerate(data_word_list):
            if (data_word in search_word_list):
                binary_data_list.append("1")
            else:
                binary_data_list.append("0")
        return "".join(binary_data_list)

    def binaryDistance(self, search_word_binary_present, candicate_binary_present):
        distance=0
        line_len = len(binary_present)
        letter_weight=(100.0/line_len)

        is_on=False
        distance=0
        for index, char in enumerat(binary_present):
            digit = (int(char))
            #is_on = (True if (is_on))

    def calculateDistance(search_word_list, candicate_list):
        sep_pat = re.compile(r"(\w+)")
        search_word_binary_present = self.binaryWord(search_word_list, search_word_list)
        for candicate_line in enumerate(candicate_list):
            candicate_line_word_list = sep_pat.findall(candicate_line)
            binary_present = self.binaryWord(search_word_list, candicate_line_word_list)


    def test_0010(self):
        s=":menuselection:`Collapse`"
        data_list=[
            ":menuselection:`Mesh --> Delete`", \
            ":kbd:`Alt-M`, :menuselection:`Collapse`", \
            ":kbd:`Alt-M`, :menuselection:`Collapse` and this is another text",
        ]

        data_list=[":kbd:`Alt-M`, :menuselection:`Collapse`", \
                    ":menuselection:`Mesh --> Delete`", \
                    "Edge Collapse", \
                    "Edge ring collapsed.", \
                    ":kbd:`X`, :kbd:`Delete`", \
                    ":kbd:`Ctrl-X`", \
                    "Selected edge loop.", \
                    "Reference", \
                    "Delete", \
                    "Limited Dissolve", \
                    "Selected edge ring.", \
                    ":ref:`mesh-unsubdivide`.", \
                    "Vertices", \
                    "Only Edges & Faces", \
                    "Only Faces", \
                    "Dissolve", \
                    "Tear Boundaries", \
                    "Dissolve Faces", \
                    "Original mesh.", \
                    "All Boundaries", \
                    "Edge Loop", \
                    "Deleting & Dissolving", \
                    "Edit Mode", \
                    "Panel", \
                    "Menu", \
                    "Dissolve Vertices", \
                    "Examples", \
                    "Dissolve Edges", \
                    "Max Angle", \
                    "Delimit", \
                    "Edge loop deleted.", \
                    "Mode", \
                    "Hotkey", \
                    "Edges", \
                    "Faces", \
                    "Face Split", \
                    "Dissolve (Context-Sensitive)", \
                    "Example", \
                    ":ref:`mesh-faces-tristoquads`.", \
                    "Result of Limited Dissolve.", \
                    ":menuselection:`Mesh --> Delete --> Edge Collapse`", \
                    ":menuselection:`Mesh --> Delete --> Edge Loop`"
        ]

        #sep_pat = re.compile(r"(\w+)")
        sep_pat = re.compile(r"([^\W]+)")

        s_word_list=sep_pat.findall(s)
        print("s_word_list:{}".format(s_word_list))
        has_words = (len(s_word_list) > 0)
        if (not has_words): return

        search_pat = []
        for word in s_word_list:
            search_pat.append("{}.*".format(word))
        search_pat = "".join(search_pat)

        matched_lines = []
        p = re.compile(search_pat)
        for line in data_list:
            m = p.search(line)
            if (m != None): matched_lines.append(line)

        print("matched_lines:{}".format(matched_lines))

        for line in matched_lines:
            #d = fz.ratio(s, line)
            d = distance(s, line)
            print("d:{}; line:{}".format(d, line))

        #binary_data_list={}
        #for line in data_list:
            #data_word_list = sep_pat.findall(line)
            #bin_line=self.binaryWord(s_word_list, data_word_list)
            #k=bin_line
            #v=line
            #binary_data_list.update({k:v})

        #has_matches_data_list=[]
        #for k, v in binary_data_list.items():
            #has_match=("1" in k)
            #if (has_match):
                #has_matches_data_list.append({k:v})
                #print("k:{}, v:{}".format(k, v))



    def test_0011(self):
        transtable = {
                "A":"Một",
                "About":"Về",
                "Always":"Luôn Luôn",
                "And":"Và",
                "Anti-Aliasing":"Chống Răng Cưa",
                "Approximate":"Ước Lượng",
                "Array":"Mảng",
                "Aspect":"Tương Quan",
                "Assigning":"Chỉ Định",
                "Assignment":"Sự Chỉ Định",
                "At":"Tại",
                "Attract":"Hấp Dẫn",
                "Available":"Có Thể Sử Dụng",
                "Axis/Angle":"Trục/Góc",
                "Backbone":"Xương Lưng",
                "Be":"Làm",
                "Bent":"Bị Bẻ Cong",
                "Best":"Tốt Nhất",
                "Blackbody":"Vật Đen",
                "Blender'S":"Của Blender",
                "Body":"Thân Thể",
                "Brick":"Gạch",
                "Button":"Nút",
                "Bézier":"Bézier",
                "Caches":"Bộ Đệm Nhớ",
                "Calculate":"Tính Toán",
                "Calculating":"Tính Toán",
                "Calculation":"Tính Toán",
                "Cascade":"",
                "Cascaded":"",
                "Chain":"Dây Chuyền",
                "Changing":"Thay Đổi",
                "Check":"Kiểm Tra",
                "Checkbox":"Hộp Kiểm",
                "Checkboxes":"Hộp Kiểm",
                "Clearing":"Làm Sạch/Dọn Dẹp",
                "Click":"Bấm",
                "Close":"Đóng/Kín/Gần",
                "Clump":"Khóm",
                "Clumping":"Khóm Lại",
                "Comparison":"So Sánh",
                "Compilation":"Biên Dịch",
                "Computer":"Máy Tính",
                "Concave":"Lõm",
                "Config":"Cấu Hình",
                "Continuous":"Tiếp Tục",
                "Cpu":"Bộ Xử Lý",
                "Datafile":"Tập Tin Dữ Liệu",
                "Datafiles":"Tập Tin Dữ Liệu",
                "Decrease":"Giảm",
                "Delete":"Xóa",
                "Deleting":"Xóa",
                "Depend":"Tùy Thuộc",
                "Deselection":"Hủy Chọn",
                "Different":" Khác",
                "Dimensional":"Kích Thước",
                "Directory":"Thư Mục",
                "Do":"Làm",
                "Does":"Làm",
                "Done":"Xong",
                "Elliptical":"Hình Elip",
                "Equal":"Bằng",
                "Error":"Lỗi",
                "Every":"Mỗi",
                "Example":"Ví Dụ",
                "Fail":"Thất Bại",
                "Failed":"Thất Bại",
                "Firefly":"Đom Đóm",
                "For":"Cho",
                "Glitch":"Hỏng Hóc",
                "Glitches":"Hỏng Hóc",
                "Group":"Nhóm",
                "Horse":"Con Ngựa",
                "In":"Trong",
                "Invalid":"Bất Hợp Lệ",
                "Is":"Là",
                "It":"Nó",
                "Kernel":"Ruột",
                "Locking":"Khóa",
                "Map":"Ánh Xạ",
                "Match":"Khớp",
                "Match":"Khớp",
                "Memory":"Bộ Nhớ",
                "Memory":"Bộ Nhớ",
                "Might":"Có Thể",
                "N-Gon":"Đa Giác",
                "Need":"Cần Thiết",
                "Not":"Không",
                "Numpad":"Bảng Số",
                "Numpadperiod":"Dấu Chấm Trên Bảng Số",
                "Of":"Của",
                "On":"Trên",
                "Only":"Duy",
                "Only":"Duy",
                "Order":"Trật Tự",
                "Panel":"Bảng",
                "Please":"Làm Ơn",
                "Point":"Điểm",
                "Preferable":"Ưa Hơn",
                "Problem":"Vấn Đề/Sự Cố",
                "Processing":"Xử Lý",
                "Profiles":"Mặt Cắt",
                "Progress":"Tiến Trình",
                "Projective":"Dự Phóng",
                "Provide":"Cung Cấp",
                "Sample":"Mẫu Vật",
                "Sampling":"Lấy Mẫu Vật",
                "Set":"Đặt",
                "Shader":"Bộ Tô Bóng",
                "Simulation":"Mô Phỏng",
                "So":"Hầu Cho",
                "Spring":"Lò Xo",
                "Start":"Bắt Đầu",
                "State":"Trạng Thái",
                "Structure":"Cấu Trúc",
                "Take":"Lấy",
                "The":"Cái",
                "Time":"Thời Gian",
                "Type":"Thể Loại",
                "Unknown":"Chưa Biết",
                "Use":"Sử Dụng",
                "Used":"Sử Dụng",
                "Using":"Dùng",
                "Variation":"Biến Thể",
                "When":"Khi",
                "While":"Trong Khi",
                "With":"Với",
                "Workaround":"Phương Pháp Khắc Phục",
                "X/Y":"X/Y",
                "Zero":"Zê-Rô",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                }

        sorted_list = sorted(transtable.items())
        word_to_find="Horse"
        trans = self.binSearch(sorted_list, word_to_find)
        print(word_to_find, trans)


    def binSearch(self, sorted_list , item_to_find):
        #print("sorted_list: {}, len:{}".format(sorted_list, len(sorted_list)))
        lo  = 0
        hi  = len(sorted_list)
        mid = -1
        while (lo < hi):
            mid  = (lo + hi) // 2
            item_on_sorted_list, trans = sorted_list[mid]
            #print("mid:{}, item_on_sorted_list: {}".format(mid, item_on_sorted_list))
            if (item_on_sorted_list == item_to_find):
                return trans
            elif (item_on_sorted_list < item_to_find):
                lo = mid + 1  # range in the higher part
            else:
                hi = mid  # range in the lower part
        return None

    def test_0012(self):
        s=":kbd:`NCT` one :ref:`irc-chat <irc-channels>` two  :doc:`History </interface/undo_redo>` three ``#blenderwiki`` four '`Mailing list <https://lists.blender.org/mailman/listinfo/bf-docboard>`__ five :abbr:`SSAO (Screen Space Ambient Occlusion)` six :menuselection:`File --> Recover Last Session` end"

        s1 = "%s: confirm, %s: cancel, %s: gravity (%s), %s|%s|%s|%s: move around, %s: fast, %s: slow, %s|%s: up and down, %s: teleport, %s: jump, %s: increase speed, %s: decrease speed. And than this!"

        s = "Updating: fk:[templates Not all of the folders have to be present."
        print("-" * 50)
        print(s)
        print("-" * 60)
        s2 = re.sub(r"((:kbd:)|(:ref:)|(:doc:)|(:abbr:)|(:menuselection:)|(:class:))", "", s, flags=re.I)
        print("removed kbd|ref|doc..\n", s2)

        s1 = re.sub(r"(<[^>]*>)", "", s2)
        print("removed <link>:\n", s1)

        s2 = re.sub(r"(%[\d]{0,2}[sfdi]+)", "", s1, flags=re.I)
        print("removed printf flags:\n", s2)

        s1 = re.sub(r"(\(\))|([_]+)", "", s2, flags=re.I)
        print("removed brackets:\n", s1)


        ##p=re.compile(r"([\,\.])|(%[isdf])|(:(kbd)|(ref)|(doc)|(abbr)|(menuselection):)|(<[^>]*>)")
        ##p=re.compile(r"([\,\.])|(%[isdf])|(:(kbd)|(ref)|(doc)|(abbr)|(menuselection):)")
        #ss = re.sub(r"([\,\.]+)", "", s)
        #print(ss)
        #ss = re.sub(r"(:(kbd)|(ref)|(doc)|(abbr)|(menuselection):)", "", ss)
        #print(ss)
        #ss = re.sub(r"(:)|(_)|(`)|([-]+>)|(#[\w]+)", "", ss)
        #print(ss)
        #ss = re.sub(r"(<[^>]*>)", "", ss)
        #print(ss)

        #s2 = "Updating: fk:[:class:`blender_api:bpy.types.KeyMapItems.new`"


        #ss = re.sub(r"(%[\d]{0,2}[sfdi]+)", "", ss, flags=re.I)
        #tt = re.sub(r"[\,\.\:\;]", "", s1)
        #ss = re.sub(r"(<[^>]*>)|(\`[^\`]*\`)", "", s1)
        #ss = re.findall(r"([^\s]+)", tt)
        #ss = re.findall(r"([\(\)\w -']+)", s1)
        word_list = re.findall(r"[^\W]+", s1)
        print("-" * 5)
        pp(s1)
        print("-" * 5)
        pp(word_list)
        print("-" * 5)
        #print(s2, " ==> ", ss)

    def test_0013(self):
        base_dir=os.path.dirname(os.path.realpath(__file__))
        print(base_dir)

    def test_0014(self):
        text = "<field_list classes=\"last\"><field><field_name>Chế Độ -- Mode</field_name><field_body><paragraph>Chế Độ Vật Thể -- Object Mode</paragraph></field_body></field><field><field_name>Bảng -- Panel</field_name><field_body><paragraph><inline classes=\"menuselection\" rawtext=\":menuselection:`Giá Công Cụ (Tool Shelf) --> Hoạt Họa (Animation) --> Hoạt Họa (Animation) --> Khung Khóa: Chèn Thêm (Keyframes: Insert)`\">Giá Công Cụ (Tool Shelf) ‣ Hoạt Họa (Animation) ‣ Hoạt Họa (Animation) ‣ Khung Khóa: Chèn Thêm (Keyframes: Insert)</inline></paragraph></field_body></field><field><field_name>Trình Đơn -- Menu</field_name><field_body><paragraph><inline classes=\"menuselection\" rawtext=\":menuselection:`Vật Thể (Object) --> Hoạt Họa (Animation) --> Chèn Khung Khóa (Insert Keyframe...)`\">Vật Thể (Object) ‣ Hoạt Họa (Animation) ‣ Chèn Khung Khóa (Insert Keyframe...)</inline></paragraph></field_body></field><field><field_name>Phím Tắt -- Hotkey</field_name><field_body><paragraph><literal classes=\"kbd\">I</literal></paragraph></field_body></field></field_list>"

        text = "<field_body><paragraph><inline classes=\"menuselection\" rawtext=\":menuselection:`Tư Thế (Pose) --> Sao Chép Tư Thế Hiện Tại (Copy Current Pose)`\">Tư Thế (Pose) ‣ Sao Chép Tư Thế Hiện Tại (Copy Current Pose)</inline>, <inline classes=\"menuselection\" rawtext=\":menuselection:`Tư Thế (Pose) --> Dán Tư Thế (Paste Pose)`\">Tư Thế (Pose) ‣ Dán Tư Thế (Paste Pose)</inline>, <inline classes=\"menuselection\" rawtext=\":menuselection:`Tư Thế (Pose) --> Dán Tư Thế Đảo-Lật theo Trục X (Paste X-Flipped Pose)`\">Tư Thế (Pose) ‣ Dán Tư Thế Đảo-Lật theo Trục X (Paste X-Flipped Pose)</inline></paragraph></field_body>"

        #/home/htran/blender_documentations/blender_docs/build/rstdoc/rigging/armatures/posing/editing.html
        #/home/htran/blender_documentations/blender_docs/manual/rigging/armatures/posing/editing.rst
        #msgid ":menuselection:`Pose --> Copy Current Pose`, :menuselection:`Pose --> Paste Pose`, :menuselection:`Pose --> Paste X-Flipped Pose`"
        #msgstr ":menuselection:`Tư Thế (Pose) --> Sao Chép Tư Thế Hiện Tại (Copy Current Pose)`, :menuselection:`Tư Thế (Pose) --> Dán Tư Thế (Paste Pose)`, :menuselection:`Tư Thế (Pose) --> Dán Tư Thế Đảo-Lật theo Trục X (Paste X-Flipped Pose)`"

        #Copy/Paste Pose
        #===============

        #.. admonition:: Reference
        #:class: refbox

        #:Mode:      Pose Mode
        #:Header:    Copy/Paste (|copy-paste|)
        #:Panel:     :menuselection:`Tool Shelf --> Tool --> Pose Tools --> Pose: Copy, Paste`
        #:Menu:      :menuselection:`Pose --> Copy Current Pose`,
                    #:menuselection:`Pose --> Paste Pose`,
                    #:menuselection:`Pose --> Paste X-Flipped Pose`

        #Blender allows you to copy and paste a pose, either through the *Pose* menu, or
        #directly using the three copy/paste buttons found at the right part of the 3D View's header:

        soup = BS(text, "html.parser")
        data_output = soup.prettify()
        print(data_output)

        para = soup.find_all('paragraph')
        men = soup.find_all('inline', {'classes' : 'menuselection'})
        kbd = soup.find_all('literal', {'classes' : 'kbd'})
        txt = soup.text

        #is_parent_field_body = (p.parent.name == 'field_body')
        #if (not is_parent_field_body):
            #print("not is_parent_field_body:{}".format(p.text))
            #continue

        #print("p={}".format(p))
        #print("p.text={}".format(p.text))
        #print("p.parent={}".format(p.parent))
        #print("type(p.parent)={}".format(type(p.parent)))
        #print("p.parent.name={}".format(p.parent.name))

        #print("para:{}".format(para))
        #print("men:{}".format(men))
        #print("kbd:{}".format(kbd))
        #print("txt:{}".format(txt))

        data=[]
        for p in para:
            t = p.text
            use_para_text = True
            men = p.find_all('inline', {'classes' : 'menuselection'})
            kbd = p.find_all('literal', {'classes' : 'kbd'})

            for k in kbd:
                k.replaceWith(":kbd:`{}`".format(k.text))

            for m in men:
                rawtext = "{}".format(m['rawtext'])
                rawtext = html.unescape(rawtext)
                m.replaceWith(rawtext)
                #print("rawtext:{}".format(rawtext))

            #print("use_para_text:{}".format(use_para_text))
            data.append(p.text)
            #print("para.text:[{}]".format(p.text))

        print(", ".join(data))

    def test_0015(self):
        #text = ":kbd:`MMB`, :kbd:`Numpad2`, :kbd:`Numpad4`, :kbd:`Numpad6`, :kbd:`Numpad8`, \
        #:kbd:`Ctrl-Alt-Wheel`, :kbd:`Shift-Alt-Wheel`"
        #text = ":kbd:`MMB`, :kbd:`Numpad2`, :kbd:`Numpad4`, :kbd:`Numpad6`, :kbd:`(Numpad8)`, \
        #:kbd:`Ctrl-Alt-Wheel`, :kbd:`Shift-Alt-Wheel`"
        text = ":menuselection:`Góc Nhìn (View) --> Điều Hướng (Navigation) --> Xoáy (Roll)`"
        wl = re.findall("[^\:\`\,\s \(\)]+", text, re.M)
        pp(wl)
        ntext = str(text)
        for w in wl:
            is_kbd = (w == 'kbd')
            if (is_kbd): continue
            nw = "({})".format(w)

            if (not nw in ntext):
                ntext = ntext.replace(w, nw)
        print(ntext)

    def test_0016(self):
        q = []
        l=["this", "that", "here", "there"]
        for ll in l:
            q.append(ll)
        pp(q)
        last = len(q)
        i = last-1
        print(q[i])
        q.remove("there")
        pp(q)


    def test_0017(self):
        text = "<field_body><paragraph><inline classes=\"menuselection\" rawtext=\":menuselection:`Tư Thế (Pose) --> Sao Chép Tư Thế Hiện Tại (Copy Current Pose)`\">Tư Thế (Pose) ‣ Sao Chép Tư Thế Hiện Tại (Copy Current Pose)</inline>, <inline classes=\"menuselection\" rawtext=\":menuselection:`Tư Thế (Pose) --> Dán Tư Thế (Paste Pose)`\">Tư Thế (Pose) ‣ Dán Tư Thế (Paste Pose)</inline>, <inline classes=\"menuselection\" rawtext=\":menuselection:`Tư Thế (Pose) --> Dán Tư Thế Đảo-Lật theo Trục X (Paste X-Flipped Pose)`\">Tư Thế (Pose) ‣ Dán Tư Thế Đảo-Lật theo Trục X (Paste X-Flipped Pose)</inline></paragraph></field_body>"

        text = "<section ids=\"animation-playback-options\" names=\"animation\ playback\ options\"><title>Animation Playback Options</title><definition_list><definition_list_item><term><literal>-a</literal> <literal><options></literal> <literal><file(s)></literal></term><definition><paragraph>Playback <literal><file(s)></literal>, only operates this way when not running in background.</paragraph><definition_list><definition_list_item><term><literal>-p</literal> <literal><sx></literal> <literal><sy></literal></term><definition><paragraph>Open with lower left corner at <literal><sx></literal>, <literal><sy></literal>.</paragraph></definition></definition_list_item><definition_list_item><term><literal>-m</literal></term><definition><paragraph>Read from disk (Do not buffer).</paragraph></definition></definition_list_item><definition_list_item><term><literal>-f</literal> <literal><fps></literal> <literal><fps-base></literal></term><definition><paragraph>Specify FPS to start with.</paragraph></definition></definition_list_item><definition_list_item><term><literal>-j</literal> <literal><frame></literal></term><definition><paragraph>Set frame step to <literal><frame></literal>.</paragraph></definition></definition_list_item><definition_list_item><term><literal>-s</literal> <literal><frame></literal></term><definition><paragraph>Play from <literal><frame></literal>.</paragraph></definition></definition_list_item><definition_list_item><term><literal>-e</literal> <literal><frame></literal></term><definition><paragraph>Play until <literal><frame></literal>.</paragraph></definition></definition_list_item></definition_list></definition></definition_list_item></definition_list></section>"

        html_file="/home/htran/blender_documentations/blender_docs/build/rstdoc/advanced/command_line/arguments.html"
        parser = AH.AdvancedHTMLParser()
        #parser.parseFile(html_file)
        parser.parseStr(text)
        items = parser.getAllNodes()
        print("items:{}".format(items))
        print("type(items):{}".format(type(items)))
        print("dir(items):{}".format(dir(items)))
        print("len(items):{}".format(len(items)))

        '''
        dir(item):['_AdvancedTag__rawGet', '_AdvancedTag__rawSet', '__class__', '__copy__', '__deepcopy__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_attributes', '_classNames', '_indent', '_old__str__', 'addClass', 'append', 'appendBlock', 'appendBlocks', 'appendChild', 'appendInnerHTML', 'appendNode', 'appendText', 'asHTML', 'attributes', 'attributesDOM', 'attributesDict', 'attributesList', 'blocks', 'childBlocks', 'childElementCount', 'childNodes', 'children', 'classList', 'className', 'classNames', 'cloneNode', 'contains', 'containsUid', 'filter', 'filterAnd', 'filterOr', 'firstChild', 'firstElementChild', 'getAllChildNodeUids', 'getAllChildNodes', 'getAllNodeUids', 'getAllNodes', 'getAttribute', 'getAttributesDict', 'getAttributesList', 'getBlocksTags', 'getBlocksText', 'getChildBlocks', 'getChildren', 'getElementById', 'getElementsByAttr', 'getElementsByClassName', 'getElementsByName', 'getElementsCustomFilter', 'getElementsWithAttrValues', 'getEndTag', 'getFirstElementCustomFilter', 'getHTML', 'getParentElementCustomFilter', 'getPeers', 'getPeersByAttr', 'getPeersByClassName', 'getPeersByName', 'getPeersCustomFilter', 'getPeersWithAttrValues', 'getStartTag', 'getStyle', 'getStyleDict', 'getTagName', 'getUid', 'hasAttribute', 'hasChild', 'hasChildNodes', 'hasClass', 'innerHTML', 'innerText', 'insertAfter', 'insertBefore', 'isEqualNode', 'isSelfClosing', 'isTagEqual', 'lastChild', 'lastElementChild', 'nextElementSibling', 'nextSibling', 'nextSiblingElement', 'nodeName', 'nodeType', 'nodeValue', 'outerHTML', 'ownerDocument', 'parentElement', 'parentNode', 'peers', 'previousElementSibling', 'previousSibling', 'previousSiblingElement', 'remove', 'removeAttribute', 'removeBlock', 'removeBlocks', 'removeChild', 'removeChildren', 'removeClass', 'removeNode', 'removeText', 'removeTextAll', 'setAttribute', 'setAttributes', 'setStyle', 'setStyles', 'style', 'tagBlocks', 'tagName', 'text', 'textBlocks', 'textContent', 'toHTML', 'uid']
        '''
        for item in items:
            print("type(item):{}".format(type(item)))
            print("item:{}".format(item))
            print("-" * 50)

            #print("type(item):{}".format(type(item)))
            #print("dir(item):{}".format(dir(item)))
            #exit(0)


    def test_0018(self):
        n1=34
        n2=65
        n3=11
        m_of=5

        list_of_combinations=[]
        list_of_op = ['+','-','*','/']
        m1, m2 = None, None
        for m1 in range(0,4):
            op1 = list_of_op[m1]
            for m2 in range(0, 4):
                op2 = list_of_op[m2]
                list_of_combinations.append((n1, op1, n2, op2, n3))
                print('res = ', n1, op1, n2, op2, n3)

        #pp(list_of_combinations)

        res =  34 + 65 + 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 + 65 + 11")
        res =  34 + 65 - 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 + 65 - 11")
        res =  34 + 65 * 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 + 65 * 11")
        res =  34 + 65 / 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 + 65 / 11")
        res =  34 - 65 + 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 - 65 + 11")
        res =  34 - 65 - 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 - 65 - 11")
        res =  34 - 65 * 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 - 65 * 11")
        res =  34 - 65 / 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 - 65 / 11")
        res =  34 * 65 + 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 * 65 + 11")
        res =  34 * 65 - 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 * 65 - 11")
        res =  34 * 65 * 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 * 65 * 11")
        res =  34 * 65 / 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 * 65 / 11")
        res =  34 / 65 + 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 / 65 + 11")
        res =  34 / 65 - 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 / 65 - 11")
        res =  34 / 65 * 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 / 65 * 11")
        res =  34 / 65 / 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 / 65 / 11")

    def test_0019(self):
        po_file="/home/htran/blender_documentations/blender_docs/locale/vi/LC_MESSAGES/modeling/meshes/editing/vertices.po"
        po_data = c.load_po(po_file)
        s2=":menuselection:Mesh --> Vertices"
        found_list=[]
        for m in po_data:
            s1=m.id
            distance = DS(s1, s2)
            found_list.append((distance, s1))
            #print("distance:{}; s1=[{}]; s2=[{}]".format(distance, s1, s2))
        sorted_found_list=sorted(found_list)
        pp(sorted_found_list)


    def test_0020(self):
        #html    :[:kbd:`MMB`, :kbd:`Numpad2`, :kbd:`Numpad4`, :kbd:`Numpad6`, :kbd:`Numpad8`, :kbd:`Ctrl-Alt-Wheel`, :kbd:`Shift-Alt-Wheel`]
        #html-hex:
        s1="3a6b62643a604d4d42602c203a6b62643a604e756d70616432602c203a6b62643a604e756d70616434602c203a6b62643a604e756d70616436602c0a3a6b62643a604e756d70616438602c203a6b62643a604374726c2d416c742d576865656c602c203a6b62643a6053686966742d416c742d576865656c60"

        #po      :[:kbd:`MMB`, :kbd:`Numpad2`, :kbd:`Numpad4`, :kbd:`Numpad6`, :kbd:`Numpad8`, :kbd:`Ctrl-Alt-Wheel`, :kbd:`Shift-Alt-Wheel`]
        #po-hex  :
        s2="3a6b62643a604d4d42602c203a6b62643a604e756d70616432602c203a6b62643a604e756d70616434602c203a6b62643a604e756d70616436602c203a6b62643a604e756d70616438602c203a6b62643a604374726c2d416c742d576865656c602c203a6b62643a6053686966742d416c742d576865656c60"
        is_found = (s1 == s2)

        length = len(s1)
        for i in range(0, length):
            s1_c = s1[i]
            s2_c = s2[i]
            is_equal = (s1_c == s2_c)
            range_size=3
            if (not is_equal):
                print("[{}]: s1_c=[{}]; s2_c=[{}]".format(i, s1_c, s2_c))
                start_index = (i-range_size if (i > range_size) else 0)
                end_index = (i+range_size if (i < length-(range_size+1)) else length-1)
                s1_s = s1[start_index:end_index]
                s2_s = s2[start_index:end_index]
                print("[{}]: s1_s=[{}]; s2_s=[{}]".format(i, s1_s, s2_s))
                break

        print("is_found:{}".format(is_found))

    def test_0021(self):
        k_list={
            ":kbd:`A`": "",
            ":kbd:`Alt-B`": "",
            ":kbd:`Alt-C`": "",
            ":kbd:`Alt-Comma`": "",
            ":kbd:`Alt-D`": "",
            ":kbd:`Alt-E`": "",
            ":kbd:`Alt-F1`": "",
            ":kbd:`Alt-F3`": "",
            ":kbd:`Alt-F`": "",
            ":kbd:`Alt-G`": "",
            ":kbd:`Alt-G`, :kbd:`Alt-R`, :kbd:`Alt-S`": "",
            ":kbd:`Alt-G`, :kbd:`Alt-S`, :kbd:`Alt-R`, :kbd:`Alt-O`": "",
            ":kbd:`Alt-I`": "",
            ":kbd:`Alt-J`": "",
            ":kbd:`Alt-M`": "",
            ":kbd:`Alt-M`, :menuselection:`Collapse`": ":kbd:`Alt-M`, :menuselection:`Thu Lại (Collapse)`",
            ":kbd:`Alt-O`": "",
            ":kbd:`Alt-P`": "",
            ":kbd:`Alt-Period`": "",
            ":kbd:`Alt-RMB`": "",
            ":kbd:`Alt-RMB` or :kbd:`Shift-Alt-RMB` for modifying existing selection": "",
            ":kbd:`Alt-RMB`, or :kbd:`Shift-Alt-RMB` for modifying existing selection": "",
            ":kbd:`Alt-R`": "",
            ":kbd:`Alt-S`": "",
            ":kbd:`Alt-Spacebar`": "",
            ":kbd:`Alt-V`": "",
            ":kbd:`B`": "",
            ":kbd:`C`": "",
            ":kbd:`Comma`": "",
            ":kbd:`Ctrl-A`": "",
            ":kbd:`Ctrl-Alt-A`": "",
            ":kbd:`Ctrl-Alt-C`": "",
            ":kbd:`Ctrl-Alt-D`": "",
            ":kbd:`Ctrl-Alt-Numpad0`": "",
            ":kbd:`Ctrl-Alt-P`": "",
            ":kbd:`Ctrl-Alt-Q`": "",
            ":kbd:`Ctrl-Alt-RMB`": "",
            ":kbd:`Ctrl-Alt-RMB`, or :kbd:`Shift-Ctrl-Alt-RMB` for modifying existing selection": "",
            ":kbd:`Ctrl-Alt-S`": "",
            ":kbd:`Ctrl-Alt-Spacebar`": "",
            ":kbd:`Ctrl-Alt-T`": "",
            ":kbd:`Ctrl-Alt-Z`": "",
            ":kbd:`Ctrl-B`": "",
            ":kbd:`Ctrl-B`, :kbd:`Ctrl-Alt-B`": "",
            ":kbd:`Ctrl-Comma`": "",
            ":kbd:`Ctrl-D`": "",
            ":kbd:`Ctrl-E`": "",
            ":kbd:`Ctrl-F3`": "",
            ":kbd:`Ctrl-F`": "",
            ":kbd:`Ctrl-G`": "",
            ":kbd:`Ctrl-G`, etc.": "",
            ":kbd:`Ctrl-H`": "",
            ":kbd:`Ctrl-J`": "",
            ":kbd:`Ctrl-LMB`": "",
            ":kbd:`Ctrl-LMB`, :kbd:`Shift-Ctrl-LMB`": "",
            ":kbd:`Ctrl-L`": "",
            ":kbd:`Ctrl-MMB`, :kbd:`Wheel`, :kbd:`NumpadPlus`, :kbd:`NumpadMinus`": "",
            ":kbd:`Ctrl-M`": "",
            ":kbd:`Ctrl-N`": "",
            ":kbd:`Ctrl-N` and :kbd:`Shift-Ctrl-N`": "",
            ":kbd:`Ctrl-Numpad0`": "",
            ":kbd:`Ctrl-NumpadPlus` / :kbd:`Ctrl-NumpadMinus`": "",
            ":kbd:`Ctrl-NumpadPlus`, :kbd:`Ctrl-NumpadMinus`": "",
            ":kbd:`Ctrl-O` or :kbd:`F1`": "",
            ":kbd:`Ctrl-P`": "",
            ":kbd:`Ctrl-P`, :kbd:`Alt-P`": "",
            ":kbd:`Ctrl-Period`": "",
            ":kbd:`Ctrl-RMB`": "",
            ":kbd:`Ctrl-R`": "",
            ":kbd:`Ctrl-Spacebar`": "",
            ":kbd:`Ctrl-T`": "",
            ":kbd:`Ctrl-T`, :kbd:`Alt-T`": "",
            ":kbd:`Ctrl-Tab`": "",
            ":kbd:`Ctrl-U`": "",
            ":kbd:`Ctrl-V`": "",
            ":kbd:`Ctrl-W`, :kbd:`Shift-Alt-A`, ...": "",
            ":kbd:`Ctrl-X`": "",
            ":kbd:`Ctrl-Z`": "",
            ":kbd:`Ctrl` and/or :kbd:`Shift`": "",
            ":kbd:`E-LMB`": "",
            ":kbd:`E`": "",
            ":kbd:`E`, :kbd:`Ctrl-LMB`": "",
            ":kbd:`E`, :kbd:`Shift-E`": "",
            ":kbd:`F3`": "",
            ":kbd:`F6`": "",
            ":kbd:`F`": "",
            ":kbd:`G`": "",
            ":kbd:`G`, :kbd:`R`, :kbd:`S`": "",
            ":kbd:`I`": "",
            ":kbd:`J`": "",
            ":kbd:`K`": "",
            ":kbd:`K` or :kbd:`Shift-K`": "",
            ":kbd:`LMB`": ":kbd:`NCT`",
            ":kbd:`L`": "",
            ":kbd:`L`, :kbd:`Ctrl-L`, :kbd:`Shift-L`": "",
            ":kbd:`MMB`": ":kbd:`NCG`",
            ":kbd:`MMB`, :kbd:`Numpad2`, :kbd:`Numpad4`, :kbd:`Numpad6`, :kbd:`Numpad8`, :kbd:`Ctrl-Alt-Wheel`, :kbd:`Shift-Alt-Wheel`": "",
            ":kbd:`M`": "",
            ":kbd:`M` or :kbd:`Ctrl-Alt-M` in the VSE editor": "",
            ":kbd:`Numpad0`": "",
            ":kbd:`Numpad0` to :kbd:`Numpad9`, :kbd:`NumpadPlus`": ":kbd:`Bàn Số 0` (`Numpad0`) tới :kbd:`Bàn Số 9` (`Numpad9`), :kbd:`Bàn Số +` (`NumpadPlus`)",
            ":kbd:`Numpad5`": "",
            ":kbd:`NumpadSlash`": "",
            ":kbd:`OS-Key` (also known as the ``Windows-Key``, ``Cmd`` or ``Super``)": "Phím Hệ Điều Hành (:kbd:`OS-Key`) (còn được biết với những cái tên khác như *phím Cửa Sổ* (``Windows-Key``), phím Lệnh (``Cmd``) hoặc phím Quản Lý (``Super``))",
            ":kbd:`O`": "",
            ":kbd:`O`, :kbd:`Alt-O`, :kbd:`Shift-O`": "",
            ":kbd:`P`": "",
            ":kbd:`P`, :kbd:`Alt-P`": "",
            ":kbd:`Period`": "",
            ":kbd:`Q`": "",
            ":kbd:`RMB`": ":kbd:`NCP` - Nút Chuột Phải",
            ":kbd:`RMB` and :kbd:`Shift-RMB`": "",
            ":kbd:`RMB`, :menuselection:`Online Manual`": ":kbd:`NCP`, :menuselection:`Hướng dẫn sử dụng trực tuyến, trên mạng (Online Manual)`",
            ":kbd:`R`": "",
            ":kbd:`S`": "",
            ":kbd:`Shift-A`": "",
            ":kbd:`Shift-Alt-F`": "",
            ":kbd:`Shift-Alt-G`, :kbd:`Shift-Alt-R`, and :kbd:`Shift-Alt-S`": "",
            ":kbd:`Shift-Alt-S`": "",
            ":kbd:`Shift-B`": "",
            ":kbd:`Shift-Ctrl-A`": "",
            ":kbd:`Shift-Ctrl-Alt-C`": "",
            ":kbd:`Shift-Ctrl-Alt-S`": "",
            ":kbd:`Shift-Ctrl-B` (vertex-only)": "",
            ":kbd:`Shift-Ctrl-C`": "",
            ":kbd:`Shift-Ctrl-MMB`": "",
            ":kbd:`Shift-Ctrl-M`": "",
            ":kbd:`Shift-Ctrl-R`": "",
            ":kbd:`Shift-Ctrl-T`": "",
            ":kbd:`Shift-Ctrl-Tab`": "",
            ":kbd:`Shift-Ctrl-Z`": "",
            ":kbd:`Shift-D`": "",
            ":kbd:`Shift-E`": "",
            ":kbd:`Shift-F1` or :kbd:`Ctrl-Alt-O`": "",
            ":kbd:`Shift-F`": "",
            ":kbd:`Shift-G`": "",
            ":kbd:`Shift-K`": "",
            ":kbd:`Shift-LMB`": "",
            ":kbd:`Shift-L`": "",
            ":kbd:`Shift-MMB`, :kbd:`Ctrl-Numpad2`, :kbd:`Ctrl-Numpad4`, :kbd:`Ctrl-Numpad6`, :kbd:`Ctrl-Numpad8`": "",
            ":kbd:`Shift-M`": "",
            ":kbd:`Shift-Numpad4`, :kbd:`Shift-Numpad6`, :kbd:`Shift-Ctrl-Wheel`": "",
            ":kbd:`Shift-R`": "",
            ":kbd:`Shift-S`": "",
            ":kbd:`Shift-T`, :kbd:`Shift-Alt-T`": "",
            ":kbd:`Shift-Tab`": "",
            ":kbd:`Shift-V`": "",
            ":kbd:`Shift-W`": "",
            ":kbd:`Shift-W`, :kbd:`Shift-Ctrl-W`, :kbd:`Alt-W`": "",
            ":kbd:`Shift-X`, :kbd:`Shift-Y`, :kbd:`Shift-Z` or :kbd:`Shift-MMB` after moving the mouse in the desired direction.": "",
            ":kbd:`Shift`, :kbd:`Ctrl`, :kbd:`Alt`": "",
            ":kbd:`T`": "",
            ":kbd:`Tab`": "",
            ":kbd:`Tab`, :kbd:`Ctrl-Tab`": "",
            ":kbd:`U`": "",
            ":kbd:`V`": "",
            ":kbd:`W`": "",
            ":kbd:`Wheel`": ":kbd:`Bánh Xe`",
            ":kbd:`X`": "",
            ":kbd:`X` or :kbd:`Delete`, :menuselection:`Edge Loop`": ":kbd:`X` or :kbd:`Delete`, :menuselection:`Vòng Mạch (Edge Loop)`",
            ":kbd:`X`, :kbd:`Delete`": "",
            ":kbd:`X`, :kbd:`Delete`; :kbd:`Ctrl-X`": "",
            ":kbd:`X`, :kbd:`Y`, :kbd:`Z` or :kbd:`MMB` after moving the mouse in the desired direction.": "",
            ":kbd:`Y`": "",
            }

       #SINGLE_KEY_KEYBOARD_DEF = re.compile(r"^:kbd:`\
                                                #(?P<single_key>(([\w])|(Tab)|(F[\d])|(Delete)){1})|\
                                                #((?P<modifier>(Alt)|(Ctrl)|(Shift))-\
                                                #(?P=single_key))*\
                                                #`$")

        #|
                #((?P<modifier>((Ctrl)|(Alt)|(Shift)))
                #((?P=modifier)|(?P=single_key)))
        p = r"""
                ^:kbd:`[^`]
                (?P<single_key>(
                    ([\w])|
                    ([\+\-\/\\/|/~/#/?/,/./]])|
                    (F[\d])|
                    (Space)|
                    (Spacebar)|
                    (Enter)|
                    (Return)|
                    (Esc)|
                    (Escape)|
                    (Del)|
                    (Delete)|
                    (Ins)|
                    (Insert)|
                    (Home)|
                    (End)|
                    (PgUp)|
                    (PageUp)|
                    (PgDown)|
                    (PageDown)|
                    ){1,1})|
                (?P<modifier>((Ctrl)|(Alt)|(Shift)))\-((?P=modifier)|(?P=single_key))
                `$"""
        SINGLE_KEY_KEYBOARD_DEF = re.compile(p, re.VERBOSE)


        keyboard_def=r":kbd:`[^`]*`"
        only_keyboard_def = r"^{}$".format(keyboard_def)
        special_def = r"((Wheel)|(Numpad)|(MMB)|(LMB)|(RMB)|(Period))"
        #pattern = ":kbd:`(?P<single_key>[\w]{1})|((?P<modifier><(Alt)|(Ctrl)|(Shift))-(?P=single_key))*`"

        for k,v in k_list.items():
            print(k)

            word_list=re.findall(keyboard_def, k)
            pp(word_list)
            for w in word_list:
                w = re.sub("[,;\. ]", "", w)
                w = w.strip()
                #is_single_key = (SINGLE_KEY_KEYBOARD_DEF.search(w) != None)
                is_only_keyboard = (re.search(only_keyboard_def, w) != None)
                is_keep = (is_only_keyboard) and (re.search(special_def, w) != None)
                print(w, is_keep)
            print("-" * 50)

    def test_0022(self):
        text = ":abbr:`SDLS (Selective Damped Least Square)`, :abbr:`DLS (Damped Least Square)`"
        text = "this is another"
        pattern = r"\(([^\)]*)\)"
        word_list = re.findall(pattern, text);
        has_list = (len(word_list) > 0)

        print(word_list)
        if (not has_list):
            print(text)
            return text

        new_word_list = []
        for w in word_list:
            new_word = "-- {}".format(w)
            new_word_list.append((w, new_word))

        new_text = str(text)
        for w, n_w in new_word_list:
            new_text = new_text.replace(w, n_w)

        print(word_list, new_word_list)
        print(new_text)

    #re.compile(r"((Wheel)|(Numpad)|(MMB)|(LMB)|(RMB)|(Period))")
    def translateKeyBoard(self, k):
        has_keyboard_def = (cm.KEYBOARD_DEF.search(k) != None)
        if (not has_keyboard_def):
            return k

        has_translatable_def = (cm.SPECIAL_DEF.search(k))
        if (not has_translatable_def):
            return k

        new_k = cm.translateKeyboardDef(k)
        return new_k

    def test_0023(self):
        t = ":kbd:`Shift-MMB`, :kbd:`Ctrl-Numpad2`, :kbd:`Ctrl-Numpad4`, :kbd:`Ctrl-Numpad6`, :kbd:`Ctrl-Numpad8`"
        t = "You can increase or decrease the radius of the proportional editing influence with the mouse wheel :kbd:`WheelUp`, :kbd:`WheelDown` or :kbd:`PageUp`, :kbd:`PageDown`, :kbd:`Wheel` respectively. As you change the radius, the points surrounding your selection will adjust their positions accordingly."
        nt = self.translateKeyBoard(t)
        print(t, nt)

    def test_0024(self):
        t = [
            "When mapping transform properties to location (i.e. Location, Destination button is enabled),",
            "Square Power of Two",
            "In order to save in a blend-user a custom brush, set a Fake User."
            ]
        p = re.compile(r"([\W]{1,1})$")
        for tt in t:
            is_end_with_symbol = (p.search(tt) != None)
            print("{}; is_end_with_symbol:{}".format(tt, is_end_with_symbol))

    def test_0025(self):
        item_to_find = "The translations are licensed under the same :doc:`License  as the original."
        list_item = "The translations are licensed under the same :doc:`/about/license` as the original."
        distance = DS(item_to_find, list_item)
        print("item_to_find:{}".format(item_to_find))
        print("list_item:{}".format(list_item))
        print("distance:{}".format(distance))

    def test_0026(self):
        pat="(\w+)(_[\w]+)*"
        pt=r'^{}$'.format(pat)
        p=re.compile(pt, re.I)
        t="TOPBAR_MT_edit_curve_add"
        print(p.search(t))

    def test_0027(self):
        d = {'one':1, 'two':2}
        for e in d.items():
            print(e)


    #case NODE_MATH_PINGPONG: {
      #if (in1 == 0.0f) {
        #*out = 0.0f;
      #}
      #else {
        #*out = fabsf(fractf((in0 - in1) / (in1 * 2.0f)) * in1 * 2.0f - in1);
      #}
      #break;
    #}

    #case NODE_MATH_WRAP: {
      #float in2 = tex_input_value(in[2], p, thread);
      #*out = wrapf(in0, in1, in2);
      #break;
    #}


    #/* Adapted from godotengine math_funcs.h. */
    #MINLINE float wrapf(float value, float max, float min)
    #{
    #float range = max - min;
    #return (range != 0.0f) ? value - (range * floorf((value - min) / range)) : min;
    #}

    def test_0028(self):
        def wrapf(value : float, f_max: float, f_min: float):
            f_range : float = (f_max - f_min)
            if (f_range != 0.0):
                wrap_value = value - (f_range * math.floor((value - f_min) / f_range))
            else:
                wrap_value = f_min
            return wrap_value

        range_min = 1.0
        range_max = 3.0
        v = 0.5
        wrap_value = wrapf(v, range_min, range_max)
        print("wrap_value:{}, {}, {}".format(v, range_min, range_max))
        print(wrap_value)

    def test_0029(self):
        CONTAINT_AST = re.compile(r'[\*\"]+(?![\s\)\(\.]+)([^\*\"]+)(?<!([\s\:]))[\*\"]+')
        t="Bones have an extra \"mirror extruding\" tool, called by pressing :kbd:`Shift-E`. By default, it behaves exactly like the standard extrusion. But once you have enabled the `X-Axis Mirror`_ editing option, each extruded tip will produce *two new bones*, having the same name except for the \"_L\"/ \"_R\" suffix (for left/right, see the :ref:`next page <armature-editing-naming-conventions>`). The \"_L\" bone behaves like the single one produced by the default extrusion -- you can move/rotate/scale it exactly the same way. The \"_R\" bone is its mirror counterpart (along the armature's local X axis), see Fig. :ref:`fig-rig-bone-mirror`."
        f_list = CONTAINT_AST.findall(t)
        print(f_list)

    def patternMatchAll(self, pat, text):
        original=[]
        break_down=[]
        try:
            for i, m in enumerate(pat.finditer(text)):
                s = m.start()
                e = m.end()
                orig = m.group(0)
                original.append((s, e, orig))

                for i, g in enumerate(m.groups()):
                    if g:
                        i_s = orig.find(g)
                        ss = i_s + s
                        ee = ss + len(g)
                        v=(ss, ee, g)
                        break_down.append(v)
        except Exception as e:
            _("patternMatchAll")
            _("pattern:", pat)
            _("text:", text)
            _(e)
        return original, break_down

    #def patternMatchAll(self, pat, text):
        #find_list= defaultdict(OrderedDict)
        #try:
            #for i, m in enumerate(pat.finditer(text)):
                #s = m.start()
                #e = m.end()
                #orig = m.group(0)

                #v=[(s, e, orig)]
                #k = s
                #entry={k:v}
                #find_list.update(entry)
                #for i, g in enumerate(m.groups()):
                    #if g:
                        #i_s = orig.find(g)
                        #ss = i_s + s
                        #ee = ss + len(g)
                        #v=(ss, ee, g)
                        #find_list[k].append(v)
        #except Exception as e:
            #_("patternMatchAll")
            #_("pattern:", pat)
            #_("text:", text)
            #_(e)
        #return find_list

    def getListOfLocation(self, find_list):
        loc_list={}
        for k,v in find_list.items():
            s = v[0][0]
            e = v[0][1]
            t = v[0][2]
            entry={k:[s, e, t]}
            loc_list.update(entry)
        return loc_list

    def inRange(self, item, ref_list):
        i_s, i_e, i_t = item
        for k, v in ref_list.items():
            r_s, r_e, r_t = v
            is_in_range = (i_s >= r_s) and (i_e <= r_e)
            if is_in_range:
                return True
        else:
            return False

    def diffLocation(self, ref_list, keep_list):
        loc_keep_list={}
        for k, v in keep_list.items():
            in_forbiden_range = self.inRange(v, ref_list)
            if not in_forbiden_range:
                s, e, txt = v
                ee = (s, e, txt)
                entry={s:[ee]}
                loc_keep_list.update(entry)

        return loc_keep_list

    def getTextListForMenu(self, text_entry):
        #print("getTextListForMenu", text_entry, txt_item)
        entry_list = []


        its, ite, txt = text_entry
        print("menu_list: its, ite, txt")
        print(its, ite, txt)

        menu_list = self.patternMatchAll(MENU_PART, txt)
        print("menu_list")
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

        return entry_list


    def getTextListForURI(self, text_entry, uri_list):
        #print("getTextListForURI", text_entry, uri_list)
        entry_list = []
        for uri_k, uri_v in uri_list.items():
            uri_orig_text, uri_text, uri_link = uri_v
            tes, tee, text = text_entry
            uris, urie, uritext = uri_text
            uss = tes + uris
            use = uss + len(uritext)
            entry=(uss, use, uritext)
            entry_list.append(entry)
        return entry_list

    def getTextListForABBR(self, text_entry):
        entry_list = []

        s, e, txt = text_entry
        abbr_list = self.patternMatchAll(LINK_WITH_URI, txt)
        has_abbr = (len(abbr_list) > 0)
        if has_abbr:
            for abbr_k, abbr_v in abbr_list.items():
                abbr_orig_text, abbr_text, abbr_full_text = abbr_v

                tes, tee, text = text_entry
                abbr_s, abbr_e, abbr_entry_text = abbr_full_text

                print("abbr_s, abbr_e, abbr_entry_text")
                print(abbr_s, abbr_e, abbr_entry_text)

                abr_s = tes + abbr_s
                abr_e = s + len(abbr_entry_text)
                entry=(abr_s, abr_e, abbr_entry_text)
                entry_list.append(entry)
        print("exit from entry_list:", entry_list)
        return entry_list


    def refEntry(self, ref_list):
        entry_list = {}
        k, v = None, None
        v_len = -1
        s = e = ss = se = xs = xe = 0
        txt = xtype = origin_entry = type_entry = text_entry = None
        try:
            for k, v in ref_list.items():
                orig = v[0]
                o_s, o_e, o_txt = orig
                key = o_s
                entry={o_s:[(o_s, o_e, o_txt)]}
                entry_list.update(entry)
                #print("ORIGINAL ENTRY:", entry)
                v_len = len(v)
                s, e, txt, xtype = None, None, None, None
                if (v_len == 1):
                    #print("v_len == 1")
                    #print(v_len, v)
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
                uri_list = self.patternMatchAll(LINK_WITH_URI, txt)
                has_uri = (len(uri_list) > 0)
                if has_uri and not (has_abbr or has_menu):
                    print("has_uri and not has_abbr")
                    uri_entry_list = self.getTextListForURI(text_entry, uri_list)
                    entry_list[key].append(uri_entry_list)
                    #print("has_uri:", uri_entry_list)
                elif has_xtype:
                    if has_abbr:
                        print("has_abbr")
                        abbr_list = self.getTextListForABBR(text_entry)
                        entry_list[key].append(abbr_list)
                        print(entry_list[key])
                    elif has_menu:
                        print("has_menu")
                        menu_text_list = self.getTextListForMenu(text_entry)
                        pp(menu_text_list)
                        entry_list[key].append(menu_text_list)
                    elif has_kbd:
                        has_commond_keyboard = NORMAL_KEYBOARD_COMBINATION.search(o_txt)
                        if (has_commond_keyboard):
                            print("has_commond_keyboard:", o_txt)
                            print(has_commond_keyboard)
                    else:
                        print("has_xtype but NOT ABBR OR MENU:", txt)
                        entry_list[key].append([text_entry])
                else:
                    entry_list[key].append([text_entry])
        except Exception as e:
            print(ref_list)
            print("k, v, v_len")
            print(k, v, v_len)
            raise e
        return entry_list

    def filteredTextList(self, ref_list, norm_list):
        loc_ref_list = self.getListOfLocation(ref_list)
        loc_norm_list = self.getListOfLocation(norm_list)
        keep_norm_list = self.diffLocation(loc_ref_list, loc_norm_list)
        return keep_norm_list


    def mergeTwoLists(self, primary, secondary):

        loc_primary_list = self.getListOfLocation(primary)
        loc_secondary_list = self.getListOfLocation(secondary)
        keep_list = self.diffLocation(loc_primary_list, loc_secondary_list)

        #pp(keep_list)
        for k, v in keep_list.items():
            keep_v = secondary[k]
            entry={k:keep_v}
            primary.update(entry)

        return primary


    #def checkParenth(self, str):
        #stack = Stack()
        #pushChars, popChars = "<({[", ">)}]"
        #for c in str:
            #if c in pushChars:
                #stack.push(c)
            #elif c in popChars:
                #if stack.isEmpty():
                    #return False
                #else:
                    #stackTop = stack.pop()
                    ## Checks to see whether the opening bracket matches the closing one
                    #balancingBracket = pushChars[popChars.index(c)]
                    #if stackTop != balancingBracket:
                        #return False
            #else:
                #return False

        #return not stack.isEmpty()

    #def parseArchedBrackets(self, msg:str, para_list:list):

        #is_valid = self.checkParenth(msg)
        #print("is_valid:", is_valid)
        #return {}

        ##ref_item: RefItem = None
        ##para = []
        ##end_loc = start_loc
        ##msg_length = len(msg)
        ##for i in range(start_loc, msg_length):
            ##char = msg[i]
            ##para.append(char)
            ##print("char:", char, "i:", i)
            ##is_open = ('(' == char)
            ##is_close = (')' == char)
            ##if is_open:
                ##para.clear()
                ##self.parseArchedBrackets(msg, i+1, para_list)
            ##elif is_close:
                ##end_loc = i
                ##valid_close = (start_loc < end_loc) and (para is not None) and (len(para) > 0)
                ##if valid_close:
                    ##parsed_para = (start_loc, end_loc, "".join(para))
                    ##para_list.append(parsed_para)
                ##return


    def parsePair(self, open_char, close_char, msg):
        valid = (open_char is not None) and (close_char is not None) and (msg is not None) and (len(msg) > 0)
        if not valid:
            return None

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
                except Exception as e:
                    raise Exception("Unbalanced pair [{},{}] at location:{}".format(open_char, close_char, i))

        has_unprocessed_pair = (len(b_list) > 0)
        if has_unprocessed_pair:
            raise Exception("Unbalanced pair [{},{}] at location:{}".format(open_char, close_char, b_list))

        has_loc = (len(loc_list) > 0)
        sorted_loc_list = sorted(loc_list, key=lambda x: x[0])
        return sorted_loc_list

    def parseArchedBrackets(self, msg):
        loc_list = self.parsePair('(',')', msg)

        pp(loc_list)
        for s, e, txt in loc_list:
            n_txt = msg[s:e]
            print(s, e, n_txt)

    def test_0030(self):

        t = ":doc:`command line </advanced/command_line/index>`"
        #t = ':menuselection:`Sidebar region --> Item`, :menuselection:`Bones tab --> Bones panel`'
        #t = "Render frame ``<frame>`` and save it. ``+<frame>`` start frame relative, ``:kbd:`LMB``` -- keyboard and mouse shortcuts. ``*Mirror*`` -- interface labels. ``:menuselection:`3D View --> Add --> Mesh --> Monkey``` -- menus."
        t = '''
        Render frame ``<frame>`` and save it. ``+<frame>`` start frame relative, ``-<frame>`` end frame relative. press :kbd:`Ctrl-G`, :menuselection:`Group --> Make Group`; :Description: Save and restore user defined views, :abbr:`POV (Point Of View)` and camera locations. ::kbd:`Shift-LMB` toggle the use of :ref:`Stabilizer <grease-pencil-draw-brushes-stabilizer>`; See also `Importance sampling <https://en.wikipedia.org/wiki/Importance_sampling>`__ on Wikipedia; Visually, the result is to zero the reds and bring up (by \"symmetry\" -- the real values remain unchanged!); (e.g. ``*-0001.jpg``, ``*-0002.jpg``, ``*-0003.jpg``, etc, of any image format), you have a choice:; which can act as subtitles, to a `SubRip <https://en.wikipedia.org/wiki/SubRip>`__ file (``.srt``);Now the tool calculates the average weight of all connected **and** unselected vertices; is connected to one unselected vertex with ``weight = 1``;  When Factor is set to 0.0 then the `Smooth`_ tool does not do anything; For example 5.25 would allow the following weights ``[0.0, 0.2, 0.4, 0.6, 0.8, 1.0]``. The bone automatically scales together with its parent in *Pose Mode*. For more details, see the :ref:`relations page <bone-relations-parenting>`. When you add a single still image (``*.jpg``, ``*.png``, etc.), Blender creates a 25 frames long strip which will show this image along the strips range. Most bones' properties (except the transform ones) are regrouped in each bone's panels, in the *Bones* tab in *Edit Mode*. Let us detail them. you can filter the Bright/Contrast modifier by placing a Mask modifier -- In the 3D View; (also :kbd:`Shift-W` :menuselection:`--> (Deform, ...)`). (also :kbd:`Shift-W` :menuselection:`--> (Multiply Vertex Group by Envelope, ...)`). and ``#docs`` :ref:`blender-chat`; :Maintainer: Brendon Murphy (meta-androcto); Blender has a tool called *UV Layout* (:menuselection:`UV Editor --> UVs --> Export UV Layout`); :Menu:      :menuselection:`Pose --> Bone Groups --> ...`; :Menu:      :menuselection:`File --> Export --> Pointcache (.pc2)`; :Menu:      :menuselection:`Armature --> Names --> AutoName Left/Right, Front/Back, Top/Bottom`, :Menu:      :menuselection:`Pose --> Bone Groups --> ...`

        :menuselection:`Properties --> Object Data --> Geometry Data --> Clear Sculpt-Mask Data`,
        :menuselection:`Sculpt`
        See `N-poles & E-poles <https://blender.stackexchange.com/a/133676/55>`__.
        in Fig. :ref:`fig-mesh-screw-wood` and Fig. :ref:`fig-mesh-screw-spring`
        as we're here; and 'here' but not 'in this place' and I couln't refuse what shouldn't for he's not she's

        :kbd:`Shift-'` -- Link only to selected nodes that have the same name/label as active node (:kbd:`Shift-'` to replace existing links)
        <->
        <=
        <Matrix>
        <file(s)>
        <fps-base>
        <instance_node>
        <w>
        @CTRL
        @MCH

        timeline-view-menu
        tool-select-box
        tool-select-circle
        resolution_x
        rest_mat
        rig_ui
        object:index
        kUniformScope
        kVertexScope
        keyframe-type

        result = previous + value * influence

        :menuselection:`File --> Import/Export --> X3D Extensible 3D (.x3d/.wrl)`


        '''

        t = '''
        Selects all objects whose name matches a given pattern. Supported wild-cards: \* matches everything, ? matches any single character, [abc] matches characters in "abc", and [!abc] match any character not in "abc". As an example \*house\* matches any name that contains "house", while floor\* matches any name starting with "floor".
        '''


        #t = ":Menu:      :menuselection:`File --> Export --> Pointcache (.pc2)`"
        #t = ":Menu:      :menuselection:`Armature --> Names --> AutoName Left/Right, Front/Back, Top/Bottom`"
        #t = ":Menu:      :menuselection:`Pose --> Bone Groups --> ...`"
        #t = ":Menu:      :menuselection:`Object --> Animation --> Insert Keyframe...`"
        #t = "(also :kbd:`Shift-W` :menuselection:`--> (Multiply Vertex Group by Envelope, ...)`)."
        #t = "'msgid:', '(also :kbd:`Shift-W` :menuselection:`--> (Multiply Vertex Group by Envelope, ...)`). :doc:`command line </advanced/command_line/index>`"
        #t = "::kbd:`Shift-LMB` toggle the use of :ref:`Stabilizer <grease-pencil-draw-brushes-stabilizer>`"
        #t = ":Location: :menuselection:`Properties --> Armature, Bone`, :menuselection:`3D View --> Tools panel`, also :kbd:`Shift-W` :menuselection:`--> (Locked, ...)`) This will prevent all editing of the bone in *Edit Mode*; see :doc:`previous page </animation/armatures/bones/editing/bones>`"
        #t = ":Location: :menuselection:`3D View --> Edit Mode Context Menu --> Relax`"
        #t = ":Description: Save and restore user defined views, :abbr:`POV (Point Of View)` and camera locations."
        #l = map(lambda x: x.group(), p.finditer(t))
        #t = "also :kbd:`Shift-W` :menuselection:`--> (Locked, ...)`) This will prevent all editing of the bone in *Edit Mode*; see :doc:`previous page </animation/armatures/bones/editing/bones>`."

        #t="ranging from 0.0 to 1.0 from the left to right side and bottom to top of the render. This is well suited for blending two objects"

        #t = "For Factor > 0 the weights of the affected vertices gradually shift from their original value towards the average weight of all connected **and** unselected vertices (see examples above)"
        #t = "To clear the mask of areas with the *Lasso Mask* tool, first invert the mask,"
        #t = "To hide a part of a mesh inside the selection. This works similar to :ref:`Box Select <tool-select-box>` tool."
        #t = "Save and restore user defined views, :abbr:`POV (Point Of View)` and camera locations."
        #t = ":doc:`modifier </modeling/modifiers/modify/data_transfer>`"
        #t = "Unit Circle <https://en.wikipedia.org/wiki/Unit_circle>"

        t = "Transformations (without translation): ``Quaternion(...)``/ ``Euler(...)``"
        t = "To clear (the mask of areas) with (the (Lasso Mask) tool), first invert the mask,"
        t = '''(something glTF allows multiple animations per file, with animations targeted to particular objects at time of export. To ensure that an animation is included, either (a) make it the active Action on the object, (b) create a single-strip NLA track, or (c) stash the action.

        Camera: ``POINT`` or ``VIEW`` or ``VPORT`` or (wip: ``INSERT(ATTRIB+XDATA)``)

        3D View: (wip: ``VIEW``, ``VPORT``)'''


        #elem_list=[]
        #self.parseArchedBrackets(t, elem_list)
        #print(elem_list)

        s = "(c>5 or (p==4 and c<4))"

        #s = "(online) or URL (in print)"

        ##It's pyparsing.printables without ()
        #r = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'*+,-./:;<=>?@[\]^_`{|}~'
        #parens = nestedExpr( '(', ')',  content=Word(r))
        #parens.setParseAction(lambda locn,tokens: (locn, tokens[0]))

        ##res = parens.parseString(s)[0].asList()
        #res = parens.parseString(s)
        #print(res.asList())

        #GREED = Word(alphas) + "," + Word(alphas) + "!"
        #greeting = GREED.parseString("Hello, world!")

        #SIGN=Word("+-", max=1)
        #INTEGER = Combine(SIGN[0,1] + Word(nums))
        #VARIABLE = Word(alphas, max=1)
        #ARITH_OP = Word("+-*/%", max=1)
        #REAL_NUM = Combine(SIGN[0,1] + Word(nums) + '.' + Word(nums))
        #EXPRESSION = (INTEGER|REAL_NUM) + (ARITH_OP + (INTEGER|REAL_NUM))[0, ...]
        #EQUATION = VARIABLE + "=" + EXPRESSION[1, ...]

        #eq = EQUATION.parseString("a = 3.0 * 2 + 1.005")
        #print(eq)

        #print("text:", t)
        #result_list = self.patternMatchAll(LINK_WITH_URI, t)
        ##result_list = self.patternMatchAll(URI, t)
        #pp(result_list)

        #ARCH_BRAKET = re.compile(r'[\(]+(?![\s\.\,\`]+)([^\)]+)[\)]+(?<!([\s\.\,]))')
        #ARCH_BRAKET = re.compile(r'[\(]+([^\)]+)(\([^\)]+\))*([^\)]+)?[\)]+')
        EXTRA_WORD = r'([^\s\,\.\:\;]+)?'
        #ARCH_BRAKET_LOOKAHEAD = r'(?=' + EXTRA_WORD + r'\([^)]+\)' + EXTRA_WORD + r')'
        ARCH_BRAKET_LOOKAHEAD = r'(?=\([^)]+\))'
        #ARCH_BRAKET_PATTERN = EXTRA_WORD + r'[\(]+' + ARCH_BRAKET_LOOKAHEAD + r'(.*)' + r'[\)]+' + EXTRA_WORD
        #ARCH_BRAKET_PATTERN = r'[\(]+' + r'(.*)' + r'[\)]+'
        # (?=(\([^)]+\)))
        #ARCH_BRAKET_PATTERN = r'[\(]+(([^\)]+)|(.*))[\)]+([^\s]+\))*'
        #ARCH_BRAKET_PATTERN = r'[\(]+(([^)])|(.*))[\)]+'
        # ARCH_BRAKET_PATTERN = r'[\(]+([^)])[\)]+'
        # (?!([\s\:\,\.]))
        #ARCH_BRAKET_PATTERN = r'(?=[\(][^\)]+[\)])([\(]+(.*)[\)]+)'
        #ARCH_BRAKET_PATTERN = r'([\(]+(.*)[\)]+)'
        #ARCH_BRAKET_PATTERN = r'([\(]+([^\)]+)[\)]+)'
        #ARCH_BRAKET_PATTERN = r'([\(]+(.*)[\)]+)'

        #ARCH_BRAKET_PATTERN = r'[\(]+((\([^\)]+\))*|(.*))[\)]+'
        ARCH_BRAKET_PATTERN = r'[\(]+(.*)[\)]+'
        ARCH_BRAKET = re.compile(ARCH_BRAKET_PATTERN)

        #t = None
        #filename="/home/htran/arched_brakets.log"
        #with open(filename, encoding='utf8') as f:
            #t = f.read()

        self.parseArchedBrackets(t)

        #ref_list = self.patternMatchAll(ARCH_BRAKET, t)
        #pp(ref_list)
        #for k, v in ref_list.items():
            #orig = v[0]
            #print("orig:", orig)

            #c = Counter(orig)
            #brack_count = c['(']
            #if (brack_count > 1):
                #sub_ref_list = self.patternMatchAll(ARCH_BRAKET, t)
                #for k, v in sub_ref_list.items():
                    #sub_orig = v[0]
                    #print("sub_orig:", sub_orig)


        #pp(ref_list, width=4096, compact=False, indent=0)

        #t = "Mr. James told me Dr. Brown is not available today. I will try tomorrow."
        #t_list = sent_tokenize(t)
        #pp(t_list)
        #for par in t_list:
            #print(par)
            #print()

        #t="1a + 2b - 3d / 400 = 5abc"

        #t=":math:`((420 + 180) modulo 360) - 180 = 60 - ...`"
        #is_ignore = self.isFormular(t)
        #print(t, is_ignore)

        #split_list = re.split(r'[\n][\s]+', t)
        #print("split_list")
        #pp(split_list)
        #for t in split_list:
            ##is_ignore = self.isIgnoredWord(t)
            ##print(t, is_ignore)

            #ref_list = self.patternMatchAll(GA_REF, t)
            ##ref_list = self.patternMatchAll(PARAMS, t)
            #print("ref_list")
            #pp(ref_list)

        ##norm_txt_list = self.patternMatchAll(NORMAL_TEXT, t)
        ##pp(norm_txt_list)

        ##filtered_txt_list = self.filteredTextList(ref_list, norm_txt_list)
        ##print("filtered_txt_list")
        ##pp(filtered_txt_list)

            #ref_norm_list = self.refEntry(ref_list)
            #print("ref_norm_list")
            #pp(ref_norm_list)

        #txt_norm_list = self.refEntry(filtered_txt_list)
        #print("txt_norm_list")
        #pp(txt_norm_list)

        #pp(ref_list)
        #pp(norm_list)

        #filtered_list = self.refEntry(ref_list)
        #print("filtered_list:")
        #pp(filtered_list)

    def test_0031(self):
        t = "1,000,000.00"
        #t = "1, 2, 3, 4"
        p = re.compile(r"^(([\d]+)([\,\.]?[\s]?[\d]+)*)+$")
        is_number = p.search(t)
        print(is_number)

    def test_0032(self):
        h = None
        for t in ignore_list:
            h = HoldString(t)
            print(hex(id(h)), h)

        print("last one", h)


    def test_0033(self):
        GA_REF = re.compile(r'[\`]*(:\w+:)*[\`]+(?![\s]+)([^\`]+)(?<!([\s\:]))[\`]+[\_]*')
        GA_REF_ONLY = re.compile(r'^[\`]*(:\w+:)*[\`]+(?![\s]+)([^\`]+)(?<!([\s\:]))[\`]+[\_]*$')
        t='''
        debugging :abbr:, ``:kbd:`LMB```, ``*Mirror*``, ``:menuselection:`3D View --> Add --> Mesh --> Monkey```
        '''
        # t = '``:kbd:`LMB```'
        # t = '``:menuselection:`3D View --> Add --> Mesh --> Monkey```'
        orig, break_down = self.patternMatchAll(GA_REF_ONLY, t)
        pp(break_down)


    def cmdline(self, command):
        process = Popen(
            args=command,
            stdout=PIPE,
            shell=True
        )
        return process.communicate()[0]

    def cmd_out(self, command):
        result = sub.run(command, stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True, shell=True)
        return result.stdout

    def test_0034(self):
        out1=self.cmdline("cat /etc/services")
        out2=self.cmdline('ls')
        #out3=self.cmdline('rpm -qa | grep "php"')
        out4=self.cmdline('nslookup google.com')

        print(out2)

    def test_0035(self):
        my_output = self.cmd_out("echo hello world")
        print(my_output)
        my_output = self.cmd_out("ls -l")
        print(my_output)
        my_output = self.cmd_out("git status | grep \'modified\' | awk \'{ print $2 }\' | grep \".po\"")
        print(my_output)
        my_output = self.cmd_out("svn status | grep \"^M\" | awk \'{ print $2 }\' | grep \".po\"")
        #print(my_output)
        #print(type(my_output))
        #file_list = my_output.split()
        #print(type(file_list))
        #print(file_list)
        #pp(file_list)

        #my_output = self.cmd_out("find . -type f -name \"*.po\" -exec ls -al --time-style=+%D\ %H:%M:%S \{\} \; | grep \`$date_bin +%D\` | awk \'{ print $6,$7,$8 }\' | sort | tail -1 | awk \'{ print $3 }\'")

        my_output = self.cmd_out("find . -maxpath 1 -name \"*.po\" -mtime -1 -print")

        #my_output = self.cmd_out("**/*.po")
        print(my_output)

        changed_file = "/home/htran/new_vi.po"
        sha256_cmd = "sha256sum " + changed_file + " |  awk '{ print $1 }'"
        my_output = self.cmd_out(sha256_cmd)

        #output = sub.check_output("ls **/*.po", shell=True)
        print(my_output)


        #my_output = self.cmd_out(["echo", "hello world"])
        #print(my_output)


    def writeTextFile(self, file_name, data):
        with open(file_name, "w+") as f:
            f.write(data)

    def readTextFile(self, file_name):
        data=None
        with open(file_name) as f:
            data = f.read();
        return data

    def test_0036(self):
        changed_file = "/home/htran/test_index.po"
        new_changed_file = "/home/htran/test_index_new.po"
        data = self.readTextFile(changed_file)
        old_data = str(data)
        for k, v in self.pattern_list.items():
            # print("k:[{}], v:[{}]".format(k, v))
            data, number_of_changes = re.subn(k, v, data)
            if number_of_changes > 0:
                changed = True
                print("Pattern: [{}], replaced with: [{}]".format(k, v))

        has_language_code = (re.search(self.re_language_code, data) != None)
        if not has_language_code:
            for k, v in self.pattern_insert.items():
                data, number_of_changes = re.subn(k, v, data)
                if number_of_changes > 0:
                    changed = True
                    print("Pattern: [{}], replaced with: [{}]".format(k, v))

        if changed:
            self.writeTextFile(changed_file, data)
            print("Wrote changed to:", changed_file)

    def test_0037(self):
        t = "'to_space -- tới không gian' '%s' I'd to do it's and I'll là không hợp lệ khi chưa được cung cấp xương tư thế nào cả 'but this'"
        SNG_QUOTE = re.compile(r'[\']+([^\']+)[\']+(?!([\w]))')
        find_all_list = re.findall(SNG_QUOTE, t)
        pp(find_all_list)



    def test_0038(self):
        t = '''
To clear (the mask of areas) with (the (Lasso Mask) tool), first invert the mask,
(something glTF allows multiple animations per file, with animations targeted to particular objects at time of export. To ensure that an animation is included, either          (a) make it the active Action on the object, (b) create a single-strip NLA track, or (c) stash the action.
Camera: ``POINT`` or ``VIEW`` or ``VPORT`` or (wip: ``INSERT(ATTRIB+XDATA)``)
3D View: (wip: ``VIEW``, ``VPORT``)
            '''
        # p = re.compile(r'[\.\,\:\!](\s+)?')
        # part_list = p.split(t)
        # pp(part_list)
        part_list = split_into_sentences(t)
        pp(part_list)

    def test_0039(self):
        p = re.compile(r'(?!\s)([^\(\)]+)(?<!\s)')
        t = 'ABBREV (something: other)'
        found_text = p.findall(t)
        print(found_text)

        p = re.compile(r'([^\`]+)\s\-\-\s([^\<]+)(?<![\s])')
        t = 'REF -- and something <and/link>'
        found_text = p.findall(t)
        print(found_text)

        p = re.compile(r'(?!\s)([^\(\)\-\>]+)(?<!\s)')
        t = '''
        Góc Nhìn 3D (MENU 3D View) --> Cộng Thêm (Add) --> Khung Lưới (Mesh)
        '''
        found_text = p.findall(t)
        print(found_text)


    def test_0040(self):
        p = re.compile(r'\b[\w\-\_\']+\b')
        t = '''
        Góc Nhìn 3D (MENU 3D View) --> Cộng Thêm (Add) --> Khung Lưới (Mesh)
        '''
        word_list = p.findall(t)
        print(word_list)

    def patternMatchAllToDict(self, pat, text):
        matching_list = {}
        for m in pat.finditer(text):
            s = m.start()
            e = m.end()
            orig = m.group(0)
            k = (s, e)
            entry = {k: orig}
            matching_list.update(entry)
        return matching_list

    def test_0041(self):
        t = '''
        Góc Nhìn 3D (MENU 3D View) --> Cộng Thêm (Add) --> Khung Lưới (Mesh) --> And Add to (Mesh)
        and this one mesh at the end of menu item to add (mesh)
        '''
        str = re.escape('(Mesh)')
        p = re.compile(str, re.I)
        matching_dict = self.patternMatchAllToDict(p, t)
        print(matching_dict)

    def test_0042(self):
        wl = ['this', 'thinking', 'the']
        dd = {}
        for w in wl:
            dd.update({len(w): w})
        k_list = reversed(sorted(list(dd.keys())))

        v_list = []
        for k in k_list:
            print(k)
            v_list.append(dd[k])

        pp(v_list)

    def test_0043(self):
        t = {
            "#docs": "#tài liệu",
            "#today": "#hôm nay",
            "$xdg_config_home": "THƯ MỤC CẤU HÌNH GỐC của XDG",
            "%.2f fps": "%.2f khung hình/giây",
            "%.4g fps": "%.4g khung hình/giây",
            "%d %s mirrored": "%d %s được đối xứng",
            "%d %s mirrored, %d failed": "%d %s được đối xứng, %d bị thất bại"
        }

        dict = WCKLCIOrderedDict(t)
        # dict.update(t)
        # pp(dict.keys())
        print('Listing:')
        for k, v in dict.items():
            print(f'k:{k}; v:{v}')

        print('selective:')
        f_word=['#docs']
        select_set = dict.getSetUpToWordCount(3, first_word=f_word, is_reversed=True)
        for k, v in select_set.items():
            print(f'k:{k}; v:{v}')

    def test_0044(self):
        t = {
            "#docs": "#tài liệu",
            "#today": "#hôm nay",
            "$xdg_config_home": "THƯ MỤC CẤU HÌNH GỐC của XDG",
            "%.2f fps": "%.2f khung hình/giây",
            "%.4g fps": "%.4g khung hình/giây",
            "%d %s mirrored": "%d %s được đối xứng",
            "%d %s mirrored, %d failed": "%d %s được đối xứng, %d bị thất bại",
            "zoom in/out": "Thu-Phóng Vào/Ra",
            "zoom in/out in the view": "Thu-phóng vào/ra trong khung nhìn",
            "zoom in/out the background image": "Phóng to/thu nhỏ hình ảnh nền",
            "zoom in/out the image": "Thu nhỏ/phóng to hình ảnh",
            "zoom in/out the view": "Thu-Phóng vào/ra góc nhìn",
            "zoom keyframes": "Số Khung Khóa Thu-Phóng",
            "zoom method": "Phương Pháp Thu-Phóng",
            "zoom options": "Tùy Chọn về Thu-Phóng",
            "zoom out": "lùi xa ra, thu nhỏ",
            "zoom out eight zoom levels (:kbd:`numpadminus` -- eight times)": "Thu ra tám lần (bấm phím :kbd:`Dấu Trừ (-) Bàn Số (NumpadMinus)` -- tám lần)",
            "zoom out the image (centered around 2d cursor)": "Thu nhỏ hình ảnh (trung tâm là con trỏ 2D)",
            "zoom out the view": "Thu nhỏ góc nhìn",
            "zoom path": "Đường Dẫn cho Thu-Phóng",
            "zoom preview to fit in the area": "Thu-phóng vùng duyệt thảo cho khít vừa diện tích",
            "zoom ratio": "Tỷ Lệ Thu-Phóng",
            "zoom ratio, 1.0 is 1:1, higher is zoomed in, lower is zoomed out": "Tỷ lệ thu-phóng, 1.0 nghĩa là 1:1, lớn hơn nghĩa là phóng to gần vào, nhỏ hơn là thu nhỏ ra",
            "zoom region": "Thu-Phóng trên Khu Vực",
            "zoom seconds": "Số Giây Thu-Phóng",
            "zoom style": "Mốt Thu-Phóng",
            "zoom the sequencer on the selected strips": "Thu-phóng bộ phối hình trên các dải được chọn",
            "zoom the view in/out": "Thu-phóng vào/ra góc nhìn",
            "zoom to border": "Phóng vào Đường Ranh Giới",
            "zoom to frame type": "Kiểu Thu-Phóng vào Khung Hình",
            "zoom to mouse position": "Thu-Phóng vào Vị Trí của Chuột",
            "zoom to the maximum zoom level (hold :kbd:`numpadplus` or :kbd:`ctrl-mmb` or similar)": "Phóng vào đến mức tối đa (bấm và giữ xuống :kbd:`Dấu Cộng (+) Bàn Số (NumpadPlus)` hoặc :kbd:`Ctrl-NCG (MMB)` hoặc tương tự)",
            "zoom using opposite direction": "Thu-phóng dùng hướng nghịch chiều",
            "zoom view": "Thu Phóng Khung Nhìn",
            "zooming": "Thu-Phóng"
        }
        l = WCKLCIOrderedDict(t)
        # for k, v in t.items():
        #     word_list = k.split()
        #     first_word = word_list[0]
        #     wc = len(word_list)
        #     length = len(k)
        #     wc_dict_entry={(length, first_word): k}
        #     wc_key = f'{wc}'
        #     wc_dict = hasattr(l, wc_key)
        #     if not wc_dict:
        #         setattr(l, wc_key, {})
        #     wc_dict = getattr(l, wc_key)
        #     wc_dict.update(wc_dict_entry)

        print(l)
        k = 'zoom region'
        v = l[k]
        print(f'{k}; {v}')

        t = 'zoom region to #docs'
        tran = l.blindTranslation(t)
        print(f'{t}: {tran}')



        # set_2 = l.getWCDict(2)
        # for k, v in reversed(sorted(set_2.items())):
        #     print(f'{k}:{v}')
        print('Paused')


    def test_0045(self):
        t = {
            "#docs": "#tài liệu",
            "#today": "#hôm nay",
            "$xdg_config_home": "THƯ MỤC CẤU HÌNH GỐC của XDG",
            "%.2f fps": "%.2f khung hình/giây",
            "%.4g fps": "%.4g khung hình/giây",
            "%d %s mirrored": "%d %s được đối xứng",
            "%d %s mirrored, %d failed": "%d %s được đối xứng, %d bị thất bại",
            "zoom in/out": "Thu-Phóng Vào/Ra",
            "zoom in/out in the view": "Thu-phóng vào/ra trong khung nhìn",
            "zoom in/out the background image": "Phóng to/thu nhỏ hình ảnh nền",
            "zoom in/out the image": "Thu nhỏ/phóng to hình ảnh",
            "zoom in/out the view": "Thu-Phóng vào/ra góc nhìn",
            "zoom keyframes": "Số Khung Khóa Thu-Phóng",
            "zoom method": "Phương Pháp Thu-Phóng",
            "zoom options": "Tùy Chọn về Thu-Phóng",
            "zoom out": "lùi xa ra, thu nhỏ",
            "zoom out eight zoom levels (:kbd:`numpadminus` -- eight times)": "Thu ra tám lần (bấm phím :kbd:`Dấu Trừ (-) Bàn Số (NumpadMinus)` -- tám lần)",
            "zoom out the image (centered around 2d cursor)": "Thu nhỏ hình ảnh (trung tâm là con trỏ 2D)",
            "zoom out the view": "Thu nhỏ góc nhìn",
            "zoom path": "Đường Dẫn cho Thu-Phóng",
            "zoom preview to fit in the area": "Thu-phóng vùng duyệt thảo cho khít vừa diện tích",
            "zoom ratio": "Tỷ Lệ Thu-Phóng",
            "zoom ratio, 1.0 is 1:1, higher is zoomed in, lower is zoomed out": "Tỷ lệ thu-phóng, 1.0 nghĩa là 1:1, lớn hơn nghĩa là phóng to gần vào, nhỏ hơn là thu nhỏ ra",
            "zoom region": "Thu-Phóng trên Khu Vực",
            "zoom seconds": "Số Giây Thu-Phóng",
            "zoom style": "Mốt Thu-Phóng",
            "zoom the sequencer on the selected strips": "Thu-phóng bộ phối hình trên các dải được chọn",
            "zoom the view in/out": "Thu-phóng vào/ra góc nhìn",
            "zoom to border": "Phóng vào Đường Ranh Giới",
            "zoom to frame type": "Kiểu Thu-Phóng vào Khung Hình",
            "zoom to mouse position": "Thu-Phóng vào Vị Trí của Chuột",
            "zoom to the maximum zoom level (hold :kbd:`numpadplus` or :kbd:`ctrl-mmb` or similar)": "Phóng vào đến mức tối đa (bấm và giữ xuống :kbd:`Dấu Cộng (+) Bàn Số (NumpadPlus)` hoặc :kbd:`Ctrl-NCG (MMB)` hoặc tương tự)",
            "zoom using opposite direction": "Thu-phóng dùng hướng nghịch chiều",
            "zoom view": "Thu Phóng Khung Nhìn",
            "zooming": "Thu-Phóng",
            "should do": "Nên làm",
            "is": "Là/được",
            "what": 'Cái gì',
            "you": 'bạn',
            "on": "trên, tại"
        }
        dic = WCKLCIOrderedDict(t)

        part_list = []
        # msg = 'zoom out on zoom view is what you should do'
        msg = ' is '
        # t = 'z-buffer input, but could also be a (grayscale) image used as a mask, or a single value input'
        print(t)

        wordsep = re.compile(r'[^\ ]+', re.I)
        loc_dic = getLocationList(wordsep, msg)
        print(loc_dic)

        # word_list = t.split(' ')
        loc_key = list(loc_dic.keys())
        print(loc_key)
        # exit(0)

        max_len = len(loc_dic)

        print(f'max_len:{max_len}')
        step = 1
        is_finished = False
        while not is_finished:
            for i in range(0, max_len):
                l=[]
                for k in range(i, min(i+step, max_len)):
                    loc = loc_key[k]
                    # print(f'step:{step}; i:{i}; k:{k}, loc:{loc}')
                    l.append(loc_key[k])

                s = []
                for loc in l:
                    word = loc_dic[loc]
                    s.append(word)
                t = " ".join(s)
                print(f's location:{l}, text:{t}')

                s_len = len(s)
                ss = l[0][0]
                ee = l[s_len-1][1]
                k = (len(t), ee)
                v = ((ss, ee), t)
                entry=(k, v)
                is_in = (entry in part_list)
                if not is_in:
                    part_list.append(entry)
            step += 1
            is_finish = (step > max_len)
            if is_finish:
                break

        sorted_partlist = list(reversed(sorted(part_list)))
        text_dic = OrderedDict()
        for e in sorted_partlist:
            k, v = e
            dict_entry = {k: v}
            text_dic.update(dict_entry)

        print('-' * 30)
        PP(text_dic)

        translated_dic = OrderedDict()
        for k, v in text_dic.items():
            loc, orig_sub_text = v
            has_tran = (orig_sub_text in dic)
            if not has_tran:
                continue
            tran_sub_text = dic[orig_sub_text]
            ss, ee = loc
            entry = {ee: (ss, ee, tran_sub_text)}
            translated_dic.update(entry)

        print('-' * 30)
        sored_translated = list(reversed(sorted(translated_dic.items())))
        PP(sored_translated)
        print(msg)

        tran_msg = str(msg)
        for k, v in sored_translated:
            ss, ee, tran_sub_text = v
            left = tran_msg[:ss]
            right = tran_msg[ee:]
            tran_msg = left + tran_sub_text + right
        print('-' * 30)
        print(tran_msg)

    def getOverlap(self, a, b):
        return max(0, min(a[1], b[1]) - max(a[0], b[0]))

    from operator import itemgetter, attrgetter, methodcaller

    def test_0046(self):
        def distKey(x):
            dist = (x[1] - x[0])
            return dist
        def removeOverlapped(loc_list, len):
            sample_str = (" "*len)
            marker='¶'
            len_list = []
            # for loc in loc_list:
            #     length = (loc[1] - loc[0])
            #     key = (length, loc)
            #     len_list.append(key)
            sorted_loc = sorted(loc_list, key=lambda x: x[1]-x[0], reverse=True )
            # sorted_loc = sorted_len_list
            # sorted_loc = []
            # for k_loc in sorted_len_list:
            #     key, loc = k_loc
            #     sorted_loc.append(loc)

            retain_l = []
            for loc in sorted_loc:
                substr = sample_str[loc[0]:loc[1]]
                is_overlapped = (marker in substr)
                if not is_overlapped:
                    maker_substr = (marker * (loc[1] - loc[0]))
                    left_part = sample_str[:loc[0]]
                    right_part = sample_str[loc[1]:]
                    sample_str = left_part + maker_substr + right_part
                    retain_l.append(loc)
            # sorted_retain_l = list(reversed(sorted(retain_l)))
            # return sorted_retain_l
            return retain_l

        l = [(0, 63), (4, 10), (11, 13), (14, 21), (22, 25), (26, 32), (26, 126), (33, 41), (42, 44), \
             (45, 53), (45, 63), (54, 63), (64, 67), (64, 126), (68, 78), (68, 89), (83, 89), (90, 92), (96, 102), \
             (103, 107), (108, 113), (114, 126), (117, 126), (127, 132), (127, 251), (138, 143), (144, 146), \
             (147, 155), (147, 164), (156, 164), (165, 168), (176, 186), (187, 191), (192, 198), (205, 207), (208, 212), (228, 230), (245, 251)]

        retain_l = removeOverlapped(l, 251)
        print(sorted(retain_l))


    def test_0047(self):
        COMMON_SENTENCE_BREAKS = re.compile(r'(?!\s)([^\.\,\:\!]+)\s?(?<!\s)')
        t = "A new Blender version is targeted to be released every 3 months. The actual `release cycle <https://wiki.blender.org/wiki/Process/Release_Cycle>`__ for a specific release is longer, and overlaps the previous and next release cycle."
        text_list = self.patternMatchAllToDict(COMMON_SENTENCE_BREAKS, t)
        for loc, text in text_list.items():
            print(f'{loc} = [{text}]')

    def test_0048(self):
        MSG_WITH_ID_PATTERN = re.compile(r'(msgid|msgstr)\s"(.*)"')
        # p = re.compile(r'((?<![\\])[\'\"])((?:.(?!(?<![\\])\1))*.?)\1')
        # p = re.compile(r'((?<![\\])[\'"])((?:.(?!(?<![\\])\1))*.?)\1')
        # p = re.compile(r'((?<![\\])[\'"])((?:.)*.?)\1')
        # p = re.compile(r'((msgid|msgstr)\s((?<![\\])[\'"])"(.?)"')
        p = re.compile(r'"(?:[^\\"]|\\.)*"')
        t = '''
        # SOME DESCRIPTIVE TITLE.# Copyright (C) : This page is licensed under a CC-BY-SA 4.0 Int. License# This file is distributed under the same license as the Blender 2.79 Manual# package.# Hoang Duy Tran <hoangduytran1960@gmail.com>, 2018.##, fuzzymsgid ""msgstr """Project-Id-Version: Blender 2.79 Manual 2.79\n""Report-Msgid-Bugs-To: \n""POT-Creation-Date: 2020-06-01 12:14+1000\n""PO-Revision-Date: 2020-06-14 04:43+0100\n""Last-Translator: Hoang Duy Tran <hoangduytran1960@gmail.com>\n""Language: vi\n""Language-Team: London, UK <hoangduytran1960@gmail.com>\n""Plural-Forms: nplurals=1; plural=0\n""MIME-Version: 1.0\n""Content-Type: text/plain; charset=utf-8\n""Content-Transfer-Encoding: 8bit\n""Generated-By: Babel 2.8.0\n"#: ../../manual/about/index.rst:5msgid "Contribute Documentation"msgstr "Đóng Góp Tài Liệu -- Contribute Documentation"#: ../../manual/about/index.rst:7msgid "The Blender Manual is a community driven effort to which anyone can contribute. Whether you like to fix a tiny spelling mistake or rewrite an entire chapter, your help with the Blender manual is most welcome!"msgstr "Bản Hướng Dẫn Sử Dụng Blender là một cố gắng do cộng đồng điều vận và ai ai cũng có thể đóng góp phần mình vào được. Cho dù bạn muốn sửa đổi một lỗi đánh vần nhỏ, hoặc muốn viết lại toàn bộ nội dung của một chương đi chăng nữa, thì sự giúp đỡ của bạn với bản Hướng Dẫn Sử Dụng Blender cũng sẽ rất được hoan nghênh!"#: ../../manual/about/index.rst:11msgid "If you find an error in the documentation, please `report the problem <https://developer.blender.org/maniphest/task/edit/form/default/?project=PHID-PROJ-c4nvvrxuczix2326vlti>`__"msgstr "Nếu bạn tìm thấy một lỗi nào đó trong bản tài liệu thì xin làm ơn `báo cáo vấn đề -- report the problem <https://developer.blender.org/maniphest/task/edit/form/default/?project=PHID-PROJ-c4nvvrxuczix2326vlti>`__ cho chúng tôi biết"#: ../../manual/about/index.rst:14msgid "Get involved in discussions through the any of the project `Contacts`_"msgstr "Xin bạn hãy tham gia các cuộc bàn luận thông qua các `Đầu Mối Liên Lạc -- Contacts`_ của đề án"#: ../../manual/about/index.rst:20msgid "Getting Started"msgstr "Khởi Đầu -- Getting Started"#: ../../manual/about/index.rst:22msgid "The following guides lead you through the process."msgstr "Hướng dẫn sau đây sẽ dẫn dắt bạn qua toàn bộ quá trình."#: ../../manual/about/index.rst:35msgid "Guidelines"msgstr "Hướng Dẫn -- Guidelines"#: ../../manual/about/index.rst:46msgid "Translations"msgstr "Phiên Dịch -- Translations"#: ../../manual/about/index.rst:58msgid "Contacts"msgstr "Mối Liên Lạc -- Contacts"#: ../../manual/about/index.rst:60msgid "`Project Page <https://developer.blender.org/project/profile/53/>`__."msgstr "`Trang Của Đề Án -- Project Page <https://developer.blender.org/project/profile/53/>`__."#: ../../manual/about/index.rst:61msgid "An overview of the documentation project."msgstr "Một số khái quá về đề án viết tài liệu."#: ../../manual/about/index.rst:62msgid "`Mailing list <https://lists.blender.org/mailman/listinfo/bf-docboard>`__"msgstr "`Danh Sách Liên Lạc Thư Điện Tử -- Mailing list <https://lists.blender.org/mailman/listinfo/bf-docboard>`__"#: ../../manual/about/index.rst:63msgid "A mailing list for discussing ideas, and keeping track of progress."msgstr "Một bản danh sách liên lạc qua thư từ để bàn bạc các ý tưởng, đồng thời cũng là nơi để theo dõi sự tiến triển của của chúng."#: ../../manual/about/index.rst:65msgid "`Devtalk <https://devtalk.blender.org/c/documentation/12>`__"msgstr "`Trò Chuyện về Xây Dựng Phần Mềm -- Devtalk <https://devtalk.blender.org/c/documentation/12>`__"#: ../../manual/about/index.rst:65msgid "A forum based discussions on writing and translating documentation. This includes the user manual, wiki, release notes, and code docs."msgstr "Bàn luận trên diễn đàn về viết và dịch tài liệu. Tài liệu ở đây bao gồm bản hướng dẫn sử dụng, trang bách khoa toàn thư mở wiki, các các tài liều về mã nguồn."#: ../../manual/about/index.rst:67msgid ":ref:`blender-chat`"msgstr ""#: ../../manual/about/index.rst:68msgid "``#docs`` channel for informal discussions in real-time."msgstr "Kênh ``#docs`` (*tài liệu*) là kênh dùng cho các cuộc bàn bạc thân thiện, không chính thức, thời gian thật."#: ../../<generated>:1msgid "`Project Workboard <https://developer.blender.org/project/board/53/>`__"msgstr "`Bảng Phân Công Nhiệm Vụ Của Đề Án -- Project Workboard <https://developer.blender.org/project/board/53/>`__"#: ../../manual/about/index.rst:70msgid "Manage tasks such as bugs, todo lists, and future plans."msgstr "Quản lý các nhiệm vụ, như các lỗi trong phần mềm, danh sách những việc cần làm, và các kế hoạch trong tương lai."
getMsgAsDict:{(251, 4678): '""msgstr """Project-Id-Version: Blender 2.79 Manual 2.79\\n""Report-Msgid-Bugs-To: \\n""POT-Creation-Date: 2020-06-01 12:14+1000\\n""PO-Revision-Date: 2020-06-14 04:43+0100\\n""Last-Translator: Hoang Duy Tran <hoangduytran1960@gmail.com>\\n""Language: vi\\n""Language-Team: London, UK <hoangduytran1960@gmail.com>\\n""Plural-Forms: nplurals=1; plural=0\\n""MIME-Version: 1.0\\n""Content-Type: text/plain; charset=utf-8\\n""Content-Transfer-Encoding: 8bit\\n""Generated-By: Babel 2.8.0\\n"#: ../../manual/about/index.rst:5msgid "Contribute Documentation"msgstr "Đóng Góp Tài Liệu -- Contribute Documentation"#: ../../manual/about/index.rst:7msgid "The Blender Manual is a community driven effort to which anyone can contribute. Whether you like to fix a tiny spelling mistake or rewrite an entire chapter, your help with the Blender manual is most welcome!"msgstr "Bản Hướng Dẫn Sử Dụng Blender là một cố gắng do cộng đồng điều vận và ai ai cũng có thể đóng góp phần mình vào được. Cho dù bạn muốn sửa đổi một lỗi đánh vần nhỏ, hoặc muốn viết lại toàn bộ nội dung của một chương đi chăng nữa, thì sự giúp đỡ của bạn với bản Hướng Dẫn Sử Dụng Blender cũng sẽ rất được hoan nghênh!"#: ../../manual/about/index.rst:11msgid "If you find an error in the documentation, please `report the problem <https://developer.blender.org/maniphest/task/edit/form/default/?project=PHID-PROJ-c4nvvrxuczix2326vlti>`__"msgstr "Nếu bạn tìm thấy một lỗi nào đó trong bản tài liệu thì xin làm ơn `báo cáo vấn đề -- report the problem <https://developer.blender.org/maniphest/task/edit/form/default/?project=PHID-PROJ-c4nvvrxuczix2326vlti>`__ cho chúng tôi biết"#: ../../manual/about/index.rst:14msgid "Get involved in discussions through the any of the project `Contacts`_"msgstr "Xin bạn hãy tham gia các cuộc bàn luận thông qua các `Đầu Mối Liên Lạc -- Contacts`_ của đề án"#: ../../manual/about/index.rst:20msgid "Getting Started"msgstr "Khởi Đầu -- Getting Started"#: ../../manual/about/index.rst:22msgid "The following guides lead you through the process."msgstr "Hướng dẫn sau đây sẽ dẫn dắt bạn qua toàn bộ quá trình."#: ../../manual/about/index.rst:35msgid "Guidelines"msgstr "Hướng Dẫn -- Guidelines"#: ../../manual/about/index.rst:46msgid "Translations"msgstr "Phiên Dịch -- Translations"#: ../../manual/about/index.rst:58msgid "Contacts"msgstr "Mối Liên Lạc -- Contacts"#: ../../manual/about/index.rst:60msgid "`Project Page <https://developer.blender.org/project/profile/53/>`__."msgstr "`Trang Của Đề Án -- Project Page <https://developer.blender.org/project/profile/53/>`__."#: ../../manual/about/index.rst:61msgid "An overview of the documentation project."msgstr "Một số khái quá về đề án viết tài liệu."#: ../../manual/about/index.rst:62msgid "`Mailing list <https://lists.blender.org/mailman/listinfo/bf-docboard>`__"msgstr "`Danh Sách Liên Lạc Thư Điện Tử -- Mailing list <https://lists.blender.org/mailman/listinfo/bf-docboard>`__"#: ../../manual/about/index.rst:63msgid "A mailing list for discussing ideas, and keeping track of progress."msgstr "Một bản danh sách liên lạc qua thư từ để bàn bạc các ý tưởng, đồng thời cũng là nơi để theo dõi sự tiến triển của của chúng."#: ../../manual/about/index.rst:65msgid "`Devtalk <https://devtalk.blender.org/c/documentation/12>`__"msgstr "`Trò Chuyện về Xây Dựng Phần Mềm -- Devtalk <https://devtalk.blender.org/c/documentation/12>`__"#: ../../manual/about/index.rst:65msgid "A forum based discussions on writing and translating documentation. This includes the user manual, wiki, release notes, and code docs."msgstr "Bàn luận trên diễn đàn về viết và dịch tài liệu. Tài liệu ở đây bao gồm bản hướng dẫn sử dụng, trang bách khoa toàn thư mở wiki, các các tài liều về mã nguồn."#: ../../manual/about/index.rst:67msgid ":ref:`blender-chat`"msgstr ""#: ../../manual/about/index.rst:68msgid "``#docs`` channel for informal discussions in real-time."msgstr "Kênh ``#docs`` (*tài liệu*) là kênh dùng cho các cuộc bàn bạc thân thiện, không chính thức, thời gian thật."#: ../../<generated>:1msgid "`Project Workboard <https://developer.blender.org/project/board/53/>`__"msgstr "`Bảng Phân Công Nhiệm Vụ Của Đề Án -- Project Workboard <https://developer.blender.org/project/board/53/>`__"#: ../../manual/about/index.rst:70msgid "Manage tasks such as bugs, todo lists, and future plans."msgstr "Quản lý \\"các nhiệm vụ\\", như các lỗi trong phần mềm, danh sách những việc cần làm, và các kế hoạch trong tương lai."
                 

        '''
        # all_list = self.patternMatchAllToDict(MSG_WITH_ID_PATTERN, t)
        all_list = self.patternMatchAllToDict(p, t)
        print(all_list)
        exit(0)
        result_dict = {}
        count=0
        entry=None
        msgid_part = msgstr_part = None
        for loc, v in all_list.items():
            msg = v[1:-1]
            msg = msg.replace('"', '\\"')
            msg = msg.replace("'", "\\'")
            is_even_line_index = (count % 2 == 0)
            if is_even_line_index:
                msgid_part = msg
            else:
                msgstr_part = msg
                entry = {msgid_part: msgstr_part}
                result_dict.update(entry)
            count += 1

        print(result_dict)



    def test_0049(self):
        def cleanForward(txt, pair_dict, leading_set):
            temp_txt = str(txt)
            count = 0
            for sym_on in leading_set:
                is_sym_on_in_dict = (sym_on in pair_dict)
                if not is_sym_on_in_dict:
                    continue

                sym_off = pair_dict[sym_on]
                temp = temp_txt[1:]
                is_balance = isBalancedSymbol(sym_on, sym_off, temp)
                if is_balance:
                    temp_txt = temp
                    count += 1
            if count > 0:
                leading_set = leading_set[count:]
            return temp_txt, leading_set

        def cleanBackward(txt, pair_dict, trailing_set):
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
                is_balance = isBalancedSymbol(sym_on, sym_off, temp)
                if is_balance:
                    temp_txt = temp
                    count += 1
            if count > 0:
                trailing_set = trailing_set[:-count]
            return temp_txt, trailing_set

        def cleanBothEnds(txt, pair_dict, leading_set, trailing_set):
            count = 0
            temp_txt = str(txt)
            symbol_set = leading_set + trailing_set
            for sym_on in symbol_set:
                is_sym_off_there = (sym_on in pair_dict)
                if not is_sym_off_there:
                    break

                sym_off = pair_dict[sym_on]
                is_both_ends = (temp_txt.startswith(sym_on) and temp_txt.endswith(sym_off))
                if not is_both_ends:
                    continue

                temp = temp_txt[1:-1]
                is_balance = isBalancedSymbol(sym_on, sym_off, temp)
                if is_balance:
                    temp_txt = temp
                    count += 1
            if count > 0:
                leading_set = leading_set[count:]
                trailing_set = trailing_set[:-count]
            return temp_txt, leading_set, trailing_set

        txt = '   ({this}....,!'
        txt = '(also :kbd:`Shift-W` :menuselection:`--> (Locked, ...)`) This will prevent all editing of the bone in *Edit Mode*; see :ref:`bone locking <animation_armatures_bones_locking>`'
        txt = '(Top/Side/Front/Camera...)'
        txt = '**this**'
        txt = "'I'd like to have this cleaned'"
        txt = txt.strip()

        pair_list = [('{', '}'), ('[', ']'), ('(', ')'), ('<', '>'), ('$', '$'),(':', ':'), ('*', '*'), ('\'', '\''), ('"', '"'), ('`', '`'),]
        pair_dict = {}
        for p in pair_list:
            s, e = p
            entry_1 = {s:e}
            entry_2 = {e:s}
            pair_dict.update(entry_1)
            pair_dict.update(entry_2)

        leading_set = REMOVABLE_SYMB_FULLSET_FRONT.findall(txt)
        if leading_set:
            leading_set = leading_set[0]

        trailing_set = REMOVABLE_SYMB_FULLSET_BACK.findall(txt)
        if trailing_set:
            trailing_set = trailing_set[0]

        temp_txt = str(txt)
        temp_txt, leading_set, trailing_set = cleanBothEnds(temp_txt, pair_dict, leading_set, trailing_set)

        temp_txt, leading_set = cleanForward(temp_txt, pair_dict, leading_set)
        temp_txt, trailing_set = cleanBackward(temp_txt, pair_dict, trailing_set)

        temp_txt, _, _ = cleanBothEnds(temp_txt, pair_dict, leading_set, trailing_set)
        print(f'temp_txt:[{temp_txt}]')

    def test_0050(self):
        quoted_msg = re.compile(r'((?<![\\])[\'"])((?:.)*.?)')
        text = '2.2 An :ref:`Object Selector <ui-eyedropper>` to select an object (usually an empty), which position and rotation will be used to define mirror planes (instead of using the ones from the modified object) $1,200.00.'
        #s_pat = re.compile(r'(?<!\w\.\w.)(?<!\w\.)(?<=\.|\?)\s')
        # s_pat = re.compile(r'(?<![\.\,]\w)((?:.)*.?)')\
        # t_list = re.split(r'(?<=[^\w]\.[.?]) +(?=[\w])', t)
        # t_list = s_pat.findall(t)
        # s_pat = re.compile(r'([^\.\,]+)')
        # t_list = patternMatchAllToDict(s_pat, t)
        t_list = re.findall(r'\S+([\,\.]\S+)', text)
        # t_list = re.split('(?<!\w[\.\,]\w.)(?<![\w\d]\.)(?<=\.|\,|\?)(\s|[A-Z].*)',text)
        # t_list = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', text)
        print(t_list)
        # text = ":abbr:`CSG (Constructive solid geometry: Hình Học Lập Thể [Đặc] Suy Diễn)`"
        # ABBREV_PATTERN_PARSER = re.compile(r':abbr:[\`]+([^(]+)\s\(([^\)]+)(:[^\)]+)?\)[\`]+')
        # abbrev_dic = patternMatchAllAsDictNoDelay(ABBREV_PATTERN_PARSER, text)
        # # t_list = ABBREV_PATTERN_PARSER.findall(text)
        #
        # abbrev_list = list(abbrev_dic.items())
        # orig = abbrev_list[0]
        # loc, txt = orig
        # print(f'{orig}\n{loc}\n{txt}\n')
        #
        # orig = abbrev_list[1]
        # loc, txt = orig
        # print(f'{orig}\n{loc}\n{txt}\n')
        #
        # orig = abbrev_list[2]
        # loc, txt = orig
        # print(f'{orig}\n{loc}\n{txt}\n')

    def run(self):
        self.test_0050()


def patternMatchAllAsDictNoDelay(pat, text):
    try:
        return_dict = {}
        for m in pat.finditer(text):
            original = ()
            # break_down = []

            s = m.start()
            e = m.end()
            orig = m.group(0)
            original = (s, e, orig)
            entry = {(s,e): orig}
            return_dict.update(entry)

            for g in m.groups():
                if g:
                    i_s = orig.find(g)
                    ss = i_s + s
                    ee = ss + len(g)
                    v=(ss, ee, g)
                    # break_down.append(v)
                    entry = {(ss, ee): g}
                    return_dict.update(entry)
    except Exception as e:
        _("patternMatchAll")
        _("pattern:", pat)
        _("text:", text)
        _(e)
    return return_dict

def patternMatchAllToDict(pat, text):
    matching_list = {}
    for m in pat.finditer(text):
        s = m.start()
        e = m.end()
        orig = m.group(0)
        k = (s, e)
        entry = {k: orig}
        matching_list.update(entry)
    return matching_list

REMOVABLE_SYMB_FULLSET_FRONT = re.compile(r'^[\s\:\!\'$\"\\\(\{\|\[\*\?\<\`\-\+\/\#\&]+')
REMOVABLE_SYMB_FULLSET_BACK = re.compile(r'[\s\:\!\'$\"\\\)\}\|\]\*\?\>\`\-\+\/\#\&\,\.]+$')

def removeLeadingTrailingSymbs(txt):
    leading_set = REMOVABLE_SYMB_FULLSET_FRONT.findall(txt)

def isBalancedSymbol(symb_on, symb_off, txt):
    p_str = f'\{symb_on}([^\{symb_on}\{symb_off}]+)\{symb_off}'
    p_exp = r'%s' % (p_str.replace("\\\\", "\\"))
    pattern = re.compile(p_exp)
    p_list = patternMatchAllToDict(pattern, txt)
    has_p_list = (len(p_list) > 0)
    if has_p_list:
        temp_txt = str(txt)
        for loc, txt in p_list.items():
            s, e = loc
            left = temp_txt[:s]
            right = temp_txt[e:]
            temp_txt = left + right
        return not ((symb_on in temp_txt) or (symb_off in temp_txt))
    else:
        return True

    # default_last_i = 0xffffffff
    # counter = 0
    # last_i = default_last_i
    # off_happened_first = False
    # for i, c in enumerate(txt):
    #     is_on = (i != last_i) and (c == symb_on)
    #     if is_on:
    #         counter += 1
    #         last_i = i
    #     else:
    #         is_off = (i != last_i) and (c == symb_off)
    #         if is_off:
    #             off_happened_first = (last_i == default_last_i)
    #             counter -= 1
    #             last_i = i
    #
    # return (counter == 0) and not (off_happened_first)

x = test()
x.run()
