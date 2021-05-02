from common import Common as cm, LocationObserver
from matcher import MatcherRecord
from definition import Definitions as df
import re
import copy as CP
from reflist import RefList
from collections import OrderedDict
from reftype import TranslationState as TS

class StructRecogniser():
    '''
        paragraph.StructRecogniser
        ~~~~~~~~~~~~~~~~~~~~~~~~~~
        This class recognise an entry of dictionary as a sentence structure which will be in the form:
            dict_sl = "chang\\w+ $$$ to $$$"
            dict_tl = "chuyển đổi từ $$$ sang thành $$$",

        This structure will help to recognise and translate commonly know structures, such as:
            src_sl_txt = "changes the structure from CONSTRUCTIVE to DECONSTRUCTIVE"

        - the class will set flag 'is_sent_struct' to True if the 'dict_sl' containing '$$$' to help identifying
        a dictionary entry is a sentence structure or not
        - the structure 'something $$$...' will be converted to a pattern (dict_sl) to recognise the
        sentences like 'src_sl_txt'. This pattern can be used to store in the 'sent_struct_dictionary' to help
        parsing text parts during translation.
        - once found, and parsed, the class can automatically generate the correct MatchRecord structure,
            self.sent_tl_rec
        ready to be used, translated. It also output the text that needed to be further translated, parsed etc,
        like reflist, for instance.
    '''
    def __init__(self, root_loc=None,
                 dict_sl_txt=None,
                 dict_tl_txt=None,
                 tran_sl_txt=None,
                 recog_pattern=None,
                 dict_tl_rec=None,
                 translation_engine=None,
                 processed_dict=None):
        self.is_sent_struct=False
        # key in dictionary, in the form 'chang\\w+ $$$ to $$$'
        self.dict_sl_txt: str = dict_sl_txt

        # translation of key in dictionary, in the form 'đổi  $$$ sang thành $$$'
        self.dict_tl_txt: str = None
        if dict_tl_txt:
            self.dict_tl_txt: str = u'%s' % (dict_tl_txt)

        # text in found in source language which matched the sentence structure pattern
        self.tran_sl_txt: str = None
        if tran_sl_txt:
            self.tran_sl_txt = tran_sl_txt

        # text that is the result of structure translation
        self.tran_tl_txt: str = None

        # pattern to recognise the sentence structure in the source language text, which will use
        # the preset translation
        self.recog_pattern: re.Pattern = recog_pattern

        self.dict_sl_rec: MatcherRecord = None
        self.dict_tl_rec: MatcherRecord = dict_tl_rec
        self.sent_sl_rec: MatcherRecord = None
        self.sent_tl_rec: MatcherRecord = None
        self.tf = translation_engine
        self.root_location = root_loc
        self.text_list_to_be_translated = None
        self.processed_list: dict = processed_dict
        self.text_list_to_be_translated = None

    def __repr__(self):
        string = "\n{!r}".format(self.__dict__)
        return string

    def getDict(self):
        return self.tf.getDict()

    def isSentenceStructure(self):
        return self.is_sent_struct

    def addBooleanToListItem(self, list_entry):
        (loc, txt) = list_entry
        return (loc, (txt, False))

    def setupRecords(self):
        dict_tl_list = None
        try:
            self.dict_sl_rec, dict_sl_list = cm.createSentRecogniserRecord(self.dict_sl_txt)

            if not self.recog_pattern:
                self.recog_pattern = self.formPattern(dict_sl_list)

            if not self.dict_tl_rec:
                self.dict_tl_rec, dict_tl_list = cm.createSentRecogniserRecord(self.dict_tl_txt)

            if not dict_tl_list:
                dict_tl_list = self.dict_tl_rec.getSubEntriesAsList()

            sent_tl_list = CP.deepcopy(dict_tl_list)

            self.sent_tl_rec = CP.copy(self.dict_tl_rec)

            self.sent_tl_rec.clear()
            self.sent_tl_rec.update(sent_tl_list)
        except Exception as e:
            # print(f'setupDictRecord() [{self}] ERROR:{e}')
            self.is_sent_struct = False
        self.is_sent_struct = bool(self.recog_pattern)
        self.setupSentSLRecord()

    def setupSentSLRecord(self):
        sl_rec: MatcherRecord = None
        try:
            sl_rec = cm.patternMatch(self.recog_pattern, self.tran_sl_txt)
            list_of_words = sl_rec.getSubEntriesAsList()
            interested_part = list_of_words[1:]
            sl_rec.clear()
            sl_rec.update(interested_part)
            self.sent_sl_rec = sl_rec
        except Exception as e:
            if bool(self.tran_sl_txt):
                self.sent_sl_rec = MatcherRecord(txt=self.tran_sl_txt)
                self.sent_tl_rec = MatcherRecord(txt=self.tran_sl_txt)

    def getListOfTextsNeededToTranslate(self):
        '''
            using the index for $$$ in the 'sent_sl_rec' to identify the text
            required (unknown) to be translated
            tran_list hold the tuple (loc, txt), this will be held in the 'sent_tl_rec'
            eventually
        '''

        def getListOfAnythingPosition(mm_record: MatcherRecord):
            '''
                Find list of indexes where $$$ is mentioned in the parsed external text
            '''
            post=[]
            try:
                mm_record_word_list = mm_record.getSubEntriesAsList()
                for index, entry in enumerate(mm_record_word_list):
                    (loc, txt) = entry
                    is_filler = (df.SENT_STRUCT_PAT.search(txt) is not None)
                    if not is_filler:
                        continue

                    post.append(index)
            except Exception as e:
                pass
                # print(f'getListOfTextNeededToTranslate(); mm_record:[{mm_record}]; ERROR:[{e}]')
            return post

        def getInitialListOfTextsToBeTranslated():
            # run through the dictionary's source language indexes, where $$$ was
            # note: we are not in the loop where location and length of strings for each element is relevant
            # these should be dealt with later
            for index, from_index in enumerate(dict_sl_any_index_list):
                # to target index of $$$ in the dictionary target language, where $$$ was
                to_index = dict_tl_any_index_list[index]

                # extract untranslated text out of external sentence where $$$ supposedly occupied
                # this will give you texts supposedly to be translated:
                # such as:
                #           the structure from CONSTRUCTIVE
                #           DECONSTRUCTIVE
                untran_loc, untran_txt = sent_sl_list_of_txt[from_index]
                new_entry = (untran_loc, untran_txt)

                # insert into the correct position, but offsets of next text items will be out of sync
                (cloc, ctxt) = sent_tl_list.pop(to_index)
                sent_tl_list.insert(to_index, new_entry)


        def correctTextsOffsets():
            # now correct offsets for subsequent texts
            corrected_sent_tl_list=[]
            correct_sent_tl_txt_list=[]
            ls = le = 0
            test_dict = OrderedDict(sent_tl_list)
            txt_list = test_dict.values()
            test_full_txt = ''.join(txt_list)
            for index, (loc, txt) in enumerate(sent_tl_list):
                ts, te = loc
                txt_length = len(txt)
                le = (ls + txt_length)
                new_loc = (ls, le)
                new_entry = (new_loc, txt)
                test_txt = test_full_txt[ls: le]
                corrected_sent_tl_list.append(new_entry)

                is_entry_untranslated = (index in dict_tl_any_index_list)
                if is_entry_untranslated:
                    text_to_translate_list.append(new_entry)
                correct_sent_tl_txt_list.append(txt)
                ls = le

            ntxt = "".join(correct_sent_tl_txt_list)
            ns = 0
            ne = len(ntxt)
            # Note, the s, e here is a temporal value, this will have to matched up with the originally parsed location
            n_mm = MatcherRecord(s=ns, e=ne, txt=ntxt)
            n_mm.appendSubRecords(corrected_sent_tl_list)
            self.sent_tl_rec = n_mm

        if bool(self.text_list_to_be_translated):
            return self.text_list_to_be_translated

        text_to_translate_list=[]
        dict_sl_any_index_list = None
        dict_tl_any_index_list = None
        sent_sl_list_of_txt = None
        sent_tl_list = None
        try:
            dict_sl_any_index_list = getListOfAnythingPosition(self.dict_sl_rec)
            # indexes of $$$ in the dictionary's target language entry in the form of [int, int...]
            dict_tl_any_index_list = getListOfAnythingPosition(self.dict_tl_rec)

            # list of text in the external source language sentence, with untranslated text
            sent_sl_list_of_txt = self.sent_sl_rec.getSubEntriesAsList()
            # list of texts in external source language sentence, with untranslated text, but will be
            # replaced with translated parts from the dictionary target language ie. text on both sides of $$$
            sent_tl_list = self.sent_tl_rec.getSubEntriesAsList()

            getInitialListOfTextsToBeTranslated()
            correctTextsOffsets()

            if not text_to_translate_list:
                raise ValueError('List empty for SOME REASONS! Move to next section.')
            print('')
        except Exception as e:
            try:
                main_loc = self.sent_sl_rec.getMainLoc()
                main_txt = self.sent_sl_rec.getMainText()
                # loc = (self.root_location if bool(self.root_location) else main_loc)
                entry=(main_loc, main_txt)
                text_to_translate_list.append(entry)
            except Exception as ee:
                pass
        return text_to_translate_list

    def setTlTranslation(self, trans_list: list):
        tl_txt = self.sent_tl_rec.txt
        trans_list.sort(reverse=True)
        for loc, tran_txt in trans_list:
            tl_txt = cm.jointText(tl_txt, tran_txt, loc)
        self.sent_tl_rec.txt = tl_txt

    def getTranslation(self):
        try:
            return self.sent_tl_rec.txt
        except Exception as e:
            return ""

    # @classmethod
    # def reproduce(cls):
    #     return cls()

    def reproduce(self):
        return self.__class__()

    def getTextListTobeTranslated(self):
        if self.text_list_to_be_translated:
            return self.text_list_to_be_translated
        else:
            if self.is_sent_struct:
                list_of_text_to_be_translated = self.getListOfTextsNeededToTranslate()
            else:
                main_entry = self.sent_sl_rec.getMainEntry()
                list_of_text_to_be_translated=[main_entry]
            self.text_list_to_be_translated = list_of_text_to_be_translated
            return self.text_list_to_be_translated

    def usePrevTran(self, prev_tran_list):
        try:
            tran_list=[]
            translated_count=0
            for orig_loc, sl_txt, tl_txt in prev_tran_list:
                for un_tran_loc, un_tran_txt in self.text_list_to_be_translated:
                    can_use_tran = (sl_txt == un_tran_txt)
                    if not can_use_tran:
                        continue
                    entry=(un_tran_loc, tl_txt)
                    tran_list.append(entry)
                    translated_count += 1
            if tran_list:
                self.setTlTranslation(tran_list)
            return translated_count
        except Exception as e:
            return 0

    def makeNonSRRecord(self, txt, root_location):
        sr = self.reproduce()
        sr.__init__(root_loc=root_location,
                         tran_sl_txt=txt,
                         translation_engine=self.tf,
                         processed_dict=self.processed_list)
        sr.setupRecords()
        sr.getTextListTobeTranslated()
        return sr

    def makeSRRecord(self, txt, root_location):
        dict_sl_pat, (dict_sltxt, dict_tltxt, dict_tl_mm_record, dict_tl_list) = self.getDict().getSentStructPattern(txt)
        if dict_sl_pat:
            print(f'IS STRUCTURE:{txt} => {dict_tltxt}')
            sr = self.reproduce()
            sr.__init__(root_loc=root_location,
                        dict_sl_txt=dict_sltxt,
                        dict_tl_txt=dict_tltxt,
                        tran_sl_txt=txt,
                        recog_pattern=dict_sl_pat,
                        dict_tl_rec=dict_tl_mm_record,
                        translation_engine=self.tf,
                        processed_dict=self.processed_list
                        )
            sr.setupRecords()
            sr.getTextListTobeTranslated()
            return sr
        else:
            return None

    def parseAndTranslateText(self, txt):
        map = cm.genmap(txt)
        obs = LocationObserver(txt)
        parsed_list=[]
        for loc, sub_txt in map:
            is_finish = obs.isCompletelyUsed()
            if is_finish:
                break

            is_used = obs.isLocUsed(loc)
            if is_used:
                continue

            sr = self.makeSRRecord(sub_txt, loc)
            if sr:
                entry = (loc, sr)
                parsed_list.append(entry)
                obs.markLocAsUsed(loc)
                self.processed_list.update({loc: sub_txt})

        un_tran = obs.getUnmarkedPartsAsDict()
        mm_record: MatcherRecord = None
        for loc, mm_record in un_tran.items():
            sub_txt = mm_record.txt
            sr = self.makeNonSRRecord(sub_txt, loc)
            entry = (loc, sr)
            parsed_list.append(entry)
            obs.markLocAsUsed(loc)
            self.processed_list.update({loc: sub_txt})

        parsed_list.sort(reverse=True)
        translation = str(txt)
        for loc, sr in parsed_list:
            tran = sr.translate()
            if tran:
                translation = cm.jointText(translation, tran, loc)
        return translation

    def translate(self):
        def addTranEntry(txt_loc, txt_sl, txt_tl):
            is_valid = (bool(txt_tl) and (txt_tl != txt_sl))
            if is_valid:
                entry=(txt_loc, tran)
                tran_list.append(entry)

        try:
            tran_list=[]
            list_needed_to_translate = self.getListOfTextsNeededToTranslate()
            for loc, txt in list_needed_to_translate:
                is_already_parsed = (txt in self.processed_list.values())
                if is_already_parsed:
                    tran = self.translateText(txt)
                    addTranEntry(loc, txt, tran)
                    continue
                else:
                    tran = self.parseAndTranslateText(txt)
                    addTranEntry(loc, txt, tran)

            if tran_list:
                self.setTlTranslation(tran_list)
                return self.getTranslation()
            else:
                return None
        except Exception as e:
            return None

    def translateText(self, txt):
        try:
            ref_list = RefList(msg=txt, keep_orig=False, tf=self.tf)
            ref_list.parseMessage()
            ref_list.translate()
            trans = ref_list.getTranslation()
            return trans
        except Exception as e:
            print(f'translateText(): {e}')
            return None

