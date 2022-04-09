from matcher import MatcherRecord
from bracket import RefAndBracketsParser as PSER
from definition import Definitions as df, RefType
from definition import TranslationState
from pattern_utils import PatternUtils as pu
from observer import LocationObserver

from translation_finder import TranslationFinder

class RefBase(list):
    obs: LocationObserver = None

    def __init__(self, txt: str, tf=None):
        self.txt: str = txt
        self.translation: str = None
        self.handler_list: list = []
        self.type: RefType = None
        self.matcher_record: MatcherRecord = None
        self.tf: TranslationFinder = tf

        self.need_tran_list=[]

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
        try:
            txt: str = txt.replace('(', '[')
            txt: str = txt.replace(')', ']')
        except Exception as e:
            pass
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
            has_tran = (tran is not None)
            if has_tran:
                tran = self.extractAbbr(tran)
            else:
                self.need_tran_list.append(txt)
        except Exception as e:
            raise e
        formatted_tran = self.formatTranslationSingle(txt, tran)
        return formatted_tran

    def formatTranslation(self, mm: MatcherRecord):
        is_tran = self.isTranslated()
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
            has_tran = (tran is not None)
            if has_tran:
                tran = self.extractAbbr(tran)
            else:
                self.need_tran_list.append(txt)
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

    def translateAll(self):
        mm: MatcherRecord = None
        for (loc, mm) in self:
            entry = (loc, mm)
            self.parse(entry)

    def getText(self):
        return self.translation

