from matcher import MatcherRecord
from bracket import RefAndBracketsParser as PSER
from definition import Definitions as df, RefType
from definition import TranslationState
from pattern_utils import PatternUtils as pu
from observer import LocationObserver
from translation_finder import TranslationFinder

class RefBase(list):
    obs: LocationObserver = None

    def __init__(self, txt: str, tf=None, ref_type=None):
        self.txt: str = txt
        self.translation: str = None
        self.handler_list: list = []
        self.type: RefType = (ref_type if (ref_type is not None) else RefType.TEXT)
        self.matcher_record: MatcherRecord = None
        self.tf: TranslationFinder = tf
        self.untranslated=[]
        self.translated=[]

    def statTranslation(self, orig: str = None, tran: str = None, matcher: MatcherRecord = None):

        use_mm = (matcher is not None)
        if use_mm:
            orig = matcher.txt
            tran = matcher.translation

        un_entry = (orig, "")
        self.untranslated.append(un_entry)

        has_tran = (tran and len(tran) > 0)
        if has_tran:
            tran_entry=(orig, tran)
            self.translated.append(tran_entry)

    def unpackAbbr(self, abbr_txt):
        if not abbr_txt:
            return None, None, None

        abbr_dict = pu.patternMatchAll(df.ABBREV_CONTENT_PARSER, abbr_txt)
        if not abbr_dict:
            return None, None, None

        abbrev_orig_rec = abbrev_part = exp_part = None
        mm: MatcherRecord = None

        try:
            abbrev_mm: MatcherRecord = None
            (abbrev_loc, abbrev_mm) = list(abbr_dict.items())[0]
            sub_list = abbrev_mm.getSubEntriesAsList()
            oloc, otxt = sub_list[0]
            ab_loc, abbrev_part = sub_list[1]
            exp_loc, exp_part = sub_list[2]
        except Exception as e:
            msg = f'abbr_txt:{abbr_txt}; exception:{e}'
            df.LOG(msg, error=True)

        return otxt, abbrev_part, exp_part

    def squareBracket(self, txt: str):
        has_bracket_pair = (df.ARCH_BRAKET_MULTI_SIMPLE.search(txt) is not None)
        if not has_bracket_pair:
            return txt

        txt: str = txt.replace('(', '[')
        txt: str = txt.replace(')', ']')
        return txt

    def removeBracket(self, txt: str):
        try:
            txt: str = txt.replace(' (', ': ')
            txt: str = txt.replace(')', '')
        except Exception as e:
            pass
        return txt

    def removeOrig(self, orig: str, txt: str):
        pattern_list = [
            f'[{orig}]',
            f'{orig}:',
            f'({orig})',
            f'{orig}',
        ]
        new_txt = str(txt)
        for pattern in pattern_list:
            new_txt = new_txt.replace(pattern, "")
        return new_txt.strip()

    def extractAbbr(self, txt: str):
        abbr_dict = pu.patternMatchAll(df.ABBREV_PATTERN_PARSER, txt)
        has_abbr = len(abbr_dict) > 0
        if has_abbr:
            abbr_dict_list = list(abbr_dict.items())
            abbr_dict_list.sort(reverse=True)
            new_txt = str(txt)
            for (loc, mm) in abbr_dict_list:
                sub_list = mm.getSubEntriesAsList()
                (sub_loc, txt) = sub_list[1]
                abbrev_orig_rec, abbrev_part, exp_part = self.unpackAbbr(txt)
                abbrev_orig_rec = self.removeBracket(abbrev_orig_rec)
                new_txt = self.jointText(new_txt, abbrev_orig_rec, loc)
            return new_txt
        else:
            return txt

    def jointText(self, orig: str, tran: str, loc: tuple):
        s, e = loc
        left = orig[:s]
        right = orig[e:]
        has_tran = (tran is not None)
        string_list = ([left, tran, right] if has_tran else [left, right])
        new_string = ''.join(string_list)
        return new_string

    def getPattern(self):
        pass

    def parse(self):
        pass

    def getTextForTranslateMultiLevel(self, entry):
        entry_loc = entry[0]
        mm: MatcherRecord = entry[1]

        sub_list = mm.getSubEntriesAsList()
        (oloc, orig) = sub_list[0]
        (sub_loc, sub_txt) = sub_list[1]
        try:
            (txt_loc, txt) = sub_list[2]
        except Exception as e:
            (txt_loc, txt) = sub_list[1]
        return [txt]

    def getTextForTranslate(self, entry):
        entry_loc = entry[0]
        mm: MatcherRecord = entry[1]

        sub_list = mm.getSubEntriesAsList()
        (oloc, orig) = sub_list[0]
        (txt_loc, txt) = sub_list[1]
        return [txt]

    def formatTranslationOutside(self, orig: str, tran: str):
        is_tran = (tran is not None)
        orig = self.squareBracket(orig)
        if is_tran:
            tran = self.squareBracket(tran)

        if is_tran:
            new_txt = f'{orig} (*{tran}*)'
        else:
            new_txt = f'{orig}'
        return new_txt

    def formatTranslationSingle(self, orig: str, tran: str):
        is_tran = (tran is not None)
        orig = self.squareBracket(orig)
        if is_tran:
            tran = self.squareBracket(tran)

        if is_tran:
            new_txt = f'{tran} ({orig})'
        else:
            new_txt = f'({orig})'
        return new_txt

    def translateSingle(self, txt: str):
        try:
            tran = self.tf.isInDict(txt)
            has_tran = (tran is not None) and (len(tran) > 0) and (tran != txt)
            if has_tran:
                tran = self.extractAbbr(tran)
            else:
                return None
        except Exception as e:
            raise e
        formatted_tran = self.formatTranslationSingle(txt, tran)
        return formatted_tran

    def formatTranslation(self, mm: MatcherRecord):
        is_tran = self.isTranslated(mm)
        tran = mm.translation
        orig = mm.txt
        orig = self.squareBracket(orig)
        tran = self.squareBracket(tran)
        if is_tran:
            new_txt = f'{tran} ({orig})'
        else:
            new_txt = f'({orig})'
        mm.translation = new_txt
        return mm

    def translate(self, entry):
        loc = entry[0]
        mm: MatcherRecord = entry[1]
        has_tran = False
        try:
            txt = mm.txt
            tran = self.tf.isInDict(txt)
            has_tran = (tran is not None) and (len(tran) > 0) and (tran != txt)
            if has_tran:
                tran = self.extractAbbr(tran)
            else:
                return None
        except Exception as e:
            raise e
        has_tran = (tran is not None)
        mm.translation = (tran if has_tran else None)
        mm.translation_state = (TranslationState.ACCEPTABLE if has_tran else TranslationState.UNTRANSLATED)
        mm = self.formatTranslation(mm)
        entry = (loc, mm)
        return entry

    def isTranslated(self, mm: MatcherRecord):
        is_translated = (mm.translation_state == TranslationState.ACCEPTABLE) and (mm.translation is not None)
        return is_translated

    def getTextAll(self):
        temp_text_list=list(map(self.getTextForTranslate, self))
        text_list = [txt for text_list in temp_text_list for txt in text_list]
        return text_list

    def translateAll(self):
        mm: MatcherRecord = None
        for (loc, mm) in self:
            entry = (loc, mm)
            self.parse(entry)

    def getText(self):
        return self.translation

