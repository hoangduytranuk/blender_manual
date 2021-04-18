#!/usr/bin/env python3
import sys
# sys.path.append('/usr/local/lib/python3.7/site-packages')
# sys.path.append('/Users/hoangduytran/blender_manual/potranslate')

from common import Common as cm, dd
from ignore import Ignore as ig
from reftype import RefType
from copy import copy
from reftype import TranslationState, TextStyle

class RefItem:

    def __init__(self, start=-1, end=-1, txt=None, ref_type=RefType.TEXT, keep_orig=False, translation_finder=None, my_parent=None):
        self.start: int = start
        self.end: int = end
        self.text: str = txt
        self.translation: str = None
        self.old_translation: str = None
        self.translation_state: TranslationState = TranslationState.UNTRANSLATED
        self.translation_include_original: bool = keep_orig
        self.reftype: RefType = ref_type
        self.text_style: TextStyle = TextStyle.NORMAL
        self.converted_to_abbr = False
        self.extra_list=[]
        self.tf=translation_finder
        self.parent = my_parent
        self.starter_txt = None
        self.ender_txt = None

    def __repr__(self):
        result = "(" + str(self.start) + ", " + \
                 str(self.end) + ", " + \
                 self.text + ", [TYPE]" + \
                 self.reftype.name + ", [STYLE]" + \
                 self.text_style.name + ", [INC]" + \
                 str(self.translation_include_original) + \
                 ")"
        if self.translation:
            result += "\n[TRANS]:(" + self.translation + ")[" + str(self.getTranslationState()) + "]"
        return result

    def __eq__(self, other):
        valid = (other is not None) and (isinstance(other, RefItem))
        if not valid:
            return False

        is_equal = (self.start == other.start) and \
                   (self.end == other.end) and \
                   (self.text == other.text) and \
                   (self.reftype == other.reftype)
        return is_equal

    def extraItemCount(self):
        return len(self.extra_list)

    def hasExtraItems(self):
        count = self.extraItemCount()
        return (count > 0)

    def isIquivalent(self, other):
        if not other:
            return False

        is_same_type = (self.reftype == other.reftype)
        this_has_text = (self.text and len(self.text) > 0)
        other_has_text = (other.text and len(other.text) > 0)

        text_in_other = this_has_text and \
                        other_has_text and \
                        (self.text in other.text)
        other_text_in_this =  this_has_text and \
                              other_has_text and \
                              (other.text in self.text)
        is_equipvalent = is_same_type and (text_in_other or other_text_in_this)
        return is_equipvalent

    def textContain(self, search_txt):
        if self.text is None:
            return False
        return (search_txt in self.text)

    def getLocation(self):
        return self.start, self.end

    def setLocation(self, s, e):
        self.start = s
        self.end = e

    def setStarterEnder(self, starter: str, ender: str):
        self.starter_txt = starter
        self.ender_txt = ender

    def setStart(self, s):
        self.start = s
        has_text = (self.txt is not None) and (len(self.text) > 0)
        if has_text:
            text_len = len(self.text)
            self.end = self.start + text_len

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text

    def getTranslationState(self):
        return self.translation_state

    def setTranslationState(self, state: TranslationState):
        self.translation_state = state

    def getTranslation(self):
        return self.translation

    def setTranlation(self, tran, is_fuzzy: bool, is_ignore: bool):
        if not tran:
            tran = ""

        self.translation = tran

        st = TranslationState.ACCEPTABLE
        if is_fuzzy:
            st = TranslationState.FUZZY
        elif is_ignore:
            st = TranslationState.IGNORED
        self.setTranslationState(st)

    def getValues(self):
        return self.start, self.end, self.text

    def setValues(self, start, end, txt):
        self.start = start
        self.end = end
        self.text = txt

    def getRefType(self):
        return self.reftype

    def setRefType(self, ref_type: RefType):
        self.reftype = ref_type

    def setIncludeOriginal(self, flag=True):
        self.translation_include_original = flag

    def isIncludeOriginal(self):
        return self.translation_include_original

    def getTextForKeyboard(self):
        item_list = {}
        found_dict = cm.patternMatchAll(cm.KEYBOARD_SEP, self.getText())
        for loc, mm in found_dict.items():
            (s, e), txt = mm.getOriginAsTuple()
            entry = {s: (s, e, txt)}
            item_list.update(entry)
        return item_list

    def getTextForGenericRef(self):
        item_list = {}

        msg = self.getText()
        is_pure_path = (cm.PURE_PATH.search(msg) is not None)
        is_pure_ref = (cm.PURE_REF.search(msg) is not None)
        is_api_ref = (cm.API_REF.search(msg) is not None)
        is_keep = (ig.isKeep(msg))
        is_keep_contain = (ig.isKeepContains(msg))
        is_ignore = (is_pure_path or is_pure_ref or is_api_ref) and (not (is_keep or is_keep_contain))
        if is_ignore:
            return item_list

        has_ref_link = (cm.REF_LINK.search(msg) is not None)
        if has_ref_link:
            found_list = cm.findInvert(cm.REF_LINK, msg)
            for k, v in reversed(list(found_list.items())):
                s, e, orig_txt = v
                entry = {s: (s, e, orig_txt)}
                item_list.update(entry)
        else:
            entry = {0: (0, len(msg), msg)}
            item_list.update(entry)
        return item_list

    def removeBlankFromText(self):
        new_ref_rec_list=[]

        has_blank = (cm.FILLER_CHAR in self.text)
        if not has_blank:
            return new_ref_rec_list

        new_ref_item: RefItem = None
        part_dict = cm.findInvert(cm.FILLER_CHAR_PATTERN, self.text)
        part_list = list(part_dict.items())
        part_list.reverse()

        count=len(part_list)
        for index, entry in enumerate(part_list):

            loc, ntxt = entry
            strip_s, strip_e, strip_txt = cm.stripSpaces(ntxt)
            s, e = loc
            ns = self.start + s + strip_s
            ne = ns + len(strip_txt)

            is_first_item = (index == 0)
            if is_first_item:
                self.setValues(ns, ne, strip_txt)
            else:
                new_ref_item = copy(self)
                new_ref_item.setValues(ns, ne, strip_txt)
                self.extra_list.append(new_ref_item)

    def formatTranslation(self):
        def addExtraChar(self, msg, ref_type=None):
            char_tbl = {
                RefType.SNG_QUOTE: "'",
                RefType.DBL_QUOTE: '"',
                RefType.AST_QUOTE: '*'
            }

            insert_char = char_tbl[ref_type]
            if insert_char:
                msg = f'{insert_char}{msg}{insert_char}'
            return msg

        # from refwithlink
        loc_s, loc_e = location
        left = loc_orig[:loc_s]
        right = loc_orig[loc_e:]
        orig_txt = loc_orig[loc_s:loc_e]
        is_text = (ref_type == RefType.TEXT)
        if not loc_tran:
            mid = f'{orig_txt}'
        else:
            if is_text:
                mid = f'{loc_tran}'
            else:
                mid = f"{loc_tran} ({orig_txt})"
        loc_value = left + mid + right
        return loc_value

        # solving the problem :term:`:abbr:`something (explanation)``
        # tran = self.recomposeAbbrevTranslation(orig_txt, tran)
        is_abbrev = (cm.ABBREV_PATTERN_PARSER.search(translation) is not None)
        if is_abbrev:
            abbrev_orig_rec, abbrev_part, exp_part = cm.extractAbbr(translation)
            tran = formValue(loc, msg, exp_part)
        else:
            tran = formValue(loc, msg, translation)

        # from quoted
        tran_found = (tran is not None)
        if not tran_found:
            return None, False, False

        if is_ignore:
            return None, is_fuzzy, is_ignore

        abbr_str = RefType.ABBR.value
        has_abbr = (abbr_str in tran)
        if has_abbr:
            return tran, is_fuzzy, is_ignore

        orig_msg = str(msg)
        ex_ga_msg = cm.EXCLUDE_GA.findall(msg)
        if (len(ex_ga_msg) > 0):
            msg = ex_ga_msg[0]

        msg = cm.replaceArchedQuote(msg)
        msg = self.addExtraChar(msg, ref_type=ref_type)
        if tran_found:
            orig_tran = str(tran)
            ex_ga_msg = cm.EXCLUDE_GA.findall(tran)
            if (len(ex_ga_msg) > 0):
                tran = ex_ga_msg[0]

            tran = cm.replaceArchedQuote(tran)
            tran = self.addExtraChar(tran, ref_type=ref_type)
            tran = f"{abbr_str}`{tran} ({msg})`"
        else:
            tran = f"{abbr_str}`{msg} ({msg})`"

    def translate(self):
        try:
            ref_txt = self.getText()
            is_ignore = ig.isIgnored(ref_txt)
            if is_ignore:
                self.setTranlation(None, False, True)
                return

            ref_type = self.reftype
            is_kbd = (ref_type == RefType.KBD)
            is_abbr = (ref_type == RefType.ABBR)
            is_menu = (ref_type == RefType.MENUSELECTION)
            is_ga = (ref_type == RefType.GA)
            is_ref = (ref_type == RefType.REF)
            is_doc = (ref_type == RefType.DOC)
            is_osl_attrib = (ref_type == RefType.OSL_ATTRIB)
            is_term = (ref_type == RefType.TERM)

            # ----------
            is_ast = (ref_type == RefType.AST_QUOTE)
            is_dbl_quote = (ref_type == RefType.DBL_QUOTE)
            is_sng_quote = (ref_type == RefType.SNG_QUOTE)
            is_python_format = (ref_type == RefType.PYTHON_FORMAT)
            is_function = (ref_type == RefType.FUNCTION)

            is_quoted = (is_ast or is_dbl_quote or is_sng_quote)

            converted_to_abbr = False
            if is_kbd:
                dd(f'translateRefItem: is_kbd:{ref_txt}')
                tran, is_fuzzy, is_ignore = self.tf.translateKeyboard(ref_txt)
            elif is_abbr:
                dd(f'translateRefItem: is_abbr:{ref_txt}')
                tran, is_fuzzy, is_ignore = self.tf.translateAbbrev(ref_txt)
            elif is_menu:
                dd(f'translateRefItem: is_menu:{ref_txt}')
                tran, is_fuzzy, is_ignore = self.tf.translateMenuSelection(ref_txt)
            elif is_quoted:
                dd(f'translateRefItem: is_quoted:{ref_txt}')
                tran, is_fuzzy, is_ignore = self.tf.translateQuoted(ref_txt, ref_type=ref_type)
                converted_to_abbr = True
            elif is_osl_attrib or is_python_format or is_function:
                return
            else:
                # is_ignore = cm.isLinkPath(ref_txt)
                # if is_ignore:
                #     ref_item.setTranlation(None, False, True)
                #     return
                #
                dd(f'translateRefItem: anything else: {ref_txt}')
                is_ref_path = (is_ref and cm.REF_PATH.search(ref_txt) is not None)
                is_doc_path = (is_doc and cm.DOC_PATH.search(ref_txt) is not None)
                is_ignore_path = (is_ref_path or is_doc_path)
                if is_ignore_path:
                    return

                tran, is_fuzzy, is_ignore = self.tf.translateRefWithLink(ref_txt, ref_type)

            self.setTranlation(tran, is_fuzzy, is_ignore)
        except Exception as e:
            print(f'ERROR! translateRefItem(), ref_item:{self}, ref_type:{ref_type}, ERROR: {e}')