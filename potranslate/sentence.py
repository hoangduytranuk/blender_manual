import time

from common import Common as cm, dd, pp, LocationObserver
from matcher import MatcherRecord
import re
import copy as CP
from collections import OrderedDict
import inspect as INP
from nocasedict import NoCaseDict as NDIC
from ignore import Ignore as ig
from definition import Definitions as df, SentStructMode as SMODE, SentStructModeRecord as SMODEREC

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
                 recog_pattern=None,

                 dict_sl_txt=None,
                 dict_sl_word_list=None,
                 dict_sl_rec=None,

                 dict_tl_txt=None,
                 dict_tl_word_list=None,
                 dict_tl_rec=None,

                 tran_sl_txt = None,
                 tran_sl_rec = None,
                 tran_tl_txt = None,

                 translation_engine=None,
                 processed_dict=None,
                 glob_sr=None,

                 ref_list=None,
                 ):
        self.is_sent_struct=False
        # key in dictionary, in the form 'chang\\w+ $$$ to $$$'
        self.dict_sl_txt: str = dict_sl_txt
        self.dict_sl_rec: MatcherRecord = dict_sl_rec
        self.dict_sl_wordlist = dict_sl_word_list

        self.dict_tl_rec: MatcherRecord = dict_tl_rec
        self.dict_tl_wordlist = dict_tl_word_list

        # translation of key in dictionary, in the form 'đổi  $$$ sang thành $$$'
        self.dict_tl_txt: str = None
        if dict_tl_txt:
            self.dict_tl_txt = u'%s' % (dict_tl_txt)

        # text in found in source language which matched the sentence structure pattern
        self.tran_sl_txt: str = tran_sl_txt
        # text that is the result of structure translation
        self.tran_tl_txt: str = tran_tl_txt

        # pattern to recognise the sentence structure in the source language text, which will use
        # the preset translation
        self.recog_pattern: str = recog_pattern

        self.sent_sl_rec: MatcherRecord = tran_sl_rec
        self.sent_tl_rec: MatcherRecord = None
        self.tf = translation_engine
        self.root_location = root_loc
        self.text_list_to_be_translated = None
        self.processed_list: NDIC = processed_dict
        self.text_list_to_be_translated = None
        self.local_dict = NDIC()
        self.global_sr_list=glob_sr
        self.ignore_list = []
        self.fuzzy_list = []
        self.ref_list = ref_list

    def __repr__(self):
        string = "\n{!r}".format(self.__dict__)
        return string

    def setAddIgnore(self, value):
        self.ignore_list.append(value)

    def setAddFuzzy(self, value):
        self.fuzzy_list.append(value)

    def isIgnore(self):
        is_ignore = bool(self.ignore_list) and (False not in self.ignore_list)
        return is_ignore

    def isFuzzy(self):
        is_fuzzy = bool(self.fuzzy_list) and (True in self.fuzzy_list)
        return is_fuzzy

    def getDict(self):
        return self.tf.getDict()

    def isSentenceStructure(self):
        return self.is_sent_struct

    def addBooleanToListItem(self, list_entry):
        (loc, txt) = list_entry
        return (loc, (txt, False))

    def makeSentTLRecord(self, loc: tuple, sl_txt: str, tl_txt:str):
        (ss, se) = loc
        mm_record = MatcherRecord(s=ss, e=se, txt=sl_txt)
        mm_record.translation = tl_txt
        mm_record.setTranslated()
        self.sent_tl_rec = mm_record

    def setupRecords(self):
        fname = INP.currentframe().f_code.co_name
        dict_tl_list = None
        try:
            if not self.dict_sl_rec:
                self.dict_sl_rec, self.dict_sl_wordlist = cm.createSentRecogniserRecord(self.dict_sl_txt)

            if not self.recog_pattern:
                self.recog_pattern = re.compile(cm.formPattern(self.dict_sl_wordlist), flags=re.I)

            if not self.dict_tl_rec:
                self.dict_tl_rec, dict_tl_list = cm.createSentRecogniserRecord(self.dict_tl_txt)

            if not self.dict_tl_wordlist:
                self.dict_tl_wordlist = self.dict_tl_rec.getSubEntriesAsList()

            sent_tl_list = CP.deepcopy(self.dict_tl_wordlist)
            self.sent_tl_rec = CP.copy(self.dict_tl_rec)

            self.sent_tl_rec.clear()
            self.sent_tl_rec.update(sent_tl_list)
        except Exception as e:
            # df.LOG(f'{e}', error=True)
            self.is_sent_struct = False
        self.is_sent_struct = bool(self.recog_pattern)

        self.setupSentSLRecord()

    def setupSentSLRecord(self):
        sl_rec: MatcherRecord = None
        if self.sent_sl_rec:
            return

        try:
            match_dict = cm.patternMatchAll(self.recog_pattern, self.tran_sl_txt)

            match_dict_list = list(match_dict.items())
            sl_loc, sl_rec = match_dict_list[0]
            list_of_words = sl_rec.getSubEntriesAsList()
            interested_part = list_of_words[1:]
            unique_interested_part = cm.removeDuplicationFromlistLocText(interested_part)
            sl_rec.clear()
            sl_rec.update(unique_interested_part)
            self.sent_sl_rec = sl_rec
        except Exception as e:
            # df.LOG(f'{e}')
            tran_sl_txt = self.tran_sl_txt
            if bool(tran_sl_txt):
                self.sent_sl_rec = MatcherRecord(txt=tran_sl_txt)
                self.sent_tl_rec = MatcherRecord(txt=tran_sl_txt)

    def getListOfTextsNeededToTranslate(self):
        fname = INP.currentframe().f_code.co_name
        '''
            using the index for $$$ in the 'sent_sl_rec' to identify the text
            required (unknown) to be translated
            tran_list hold the tuple (loc, txt), this will be held in the 'sent_tl_rec'
            eventually
        '''

        def getListOfAnythingPosition(word_list):
            '''
                Find list of indexes where $$$ is mentioned in the parsed external text
            '''
            index_list=[]
            try:
                for index, (txt_loc, txt) in enumerate(word_list):
                    is_filler = (txt.startswith(df.SENT_STRUCT_START_SYMB))
                    if not is_filler:
                        continue

                    index_list.append(index)
            except Exception as e:
                df.LOG(e, error=True)

            return index_list

        def getInitialListOfTextsToBeTranslated():
            try:
                # to target index of $$$ in the dictionary target language, where $$$ was
                dict_sl_smode_list = list(self.dict_sl_rec.smode.values())
                dict_tl_smode_list = list(self.dict_tl_rec.smode.values())
                order_queue = {}
                any_list=[]
                if not dict_tl_any_index_list:
                    return any_list

                dd('-' * 20)
                dd(f'dict_sl_any_index_list:')
                pp(dict_sl_any_index_list)
                dd('-' * 20)
                dd(f'dict_tl_any_index_list:')
                pp(dict_tl_any_index_list)
                dd('-' * 20)
                if sent_sl_list_of_txt:
                    dd(f'sent_sl_list_of_txt:')
                    pp(sent_sl_list_of_txt)
                else:
                    dd(f'sent_sl_list_of_txt: IS EMPTY')
                dd('*' * 20)
                for index, from_index in enumerate(dict_sl_any_index_list):
                    to_index = dict_tl_any_index_list[index]
                    untran_loc, untran_txt = sent_sl_list_of_txt[from_index]
                    dict_tl_pat_txt, dict_tl_smode_item = dict_tl_smode_list[to_index]
                    dict_sl_pat_txt, dict_sl_smode_item = dict_sl_smode_list[from_index]
                    tl_mode_rec:SMODEREC = dict_tl_smode_item[0]
                    sl_mode_rec:SMODEREC = dict_sl_smode_item[0]

                    is_sl_order = (sl_mode_rec.smode == SMODE.ORDERED_GROUP)
                    is_tl_order = (tl_mode_rec.smode == SMODE.ORDERED_GROUP)
                    is_order = (is_sl_order and is_tl_order)
                    if is_order:
                        sl_order = sl_mode_rec.extra_param
                        new_entry = {sl_order: untran_txt}
                        order_queue.update(new_entry)
                    else:
                        new_entry = (untran_loc, untran_txt)
                        any_list.append(new_entry)

                if order_queue:
                    dict_tl_list = self.dict_tl_rec.getSubEntriesAsList()
                    for loc, txt in dict_tl_list:
                        sent_struct = df.SENT_STRUCT_PAT.search(txt)
                        is_sent_struct_entry = (sent_struct is not None)
                        if not is_sent_struct_entry:
                            continue
                        grp = sent_struct.groups()
                        order = int(grp[1])
                        txt = order_queue[order]
                        any_list.append((loc, txt.strip()))
                    df.LOG('SWAPPING any_list:')
                    pp(any_list)
                return any_list
            except Exception as e:
                df.LOG(e, error=True)
                dd('-' * 80)
                dd(f'dict_sl_any_index_list:')
                pp(dict_sl_any_index_list)
                dd('-' * 80)
                dd(f'dict_tl_any_index_list:')
                pp(dict_tl_any_index_list)
                dd('-' * 80)
                dd(f'dict_sl_smode_list:')
                pp(dict_sl_smode_list)
                dd('-' * 30)
                dd(f'sent_sl_list_of_txt:')
                pp(sent_sl_list_of_txt)
                dd('-' * 30)
                dd(f'dict_tl_smode_list:')
                pp(dict_tl_smode_list)
                dd('-' * 80)
                raise e

        def correctTextsOffsets(senttl_list):
            def creatTLTextList():
                any_index_list=[]
                sent_tl_index = 0
                new_list = []
                senttl_list_length = len(senttl_list)
                for index, (loc, tl_txt) in enumerate(dict_tl_list):
                    (ls, le) = loc
                    is_pattern = (df.SENT_STRUCT_PAT.search(tl_txt) is not None)
                    if is_pattern:
                        senttl_loc, actual_tl_txt = senttl_list[sent_tl_index]
                        sent_tl_index = min(sent_tl_index + 1, senttl_list_length - 1)
                        any_index_list.append(index)
                    else:
                        actual_tl_txt = tl_txt

                    new_entry = (loc, actual_tl_txt)
                    new_list.append(new_entry)
                df.LOG(f'RETURN new_list:; any_index_list:')
                dd('new_list:')
                pp(new_list, width=200)
                dd('-' * 20)
                dd('any_index_list list:')
                pp(any_index_list, width=200)
                dd('-' * 20)

                return new_list, any_index_list

            def correctIndexOfTLTextList(the_new_list, any_index_list):
                # df.LOG(f'the_new_list; any_index_list')
                tran_required_list = []
                the_new_tl_txt = dict_tl_txt
                corrected_list = []
                try:
                    dict_tl_txt_len = len(dict_tl_txt)
                    blank_str = (df.FILLER_CHAR * dict_tl_txt_len)

                    the_new_list_reversed = sorted(the_new_list, reverse=True)
                    for loc, txt in the_new_list_reversed:
                        left, mid, right = cm.getTextWinthinSpaces(txt)
                        (ls, le) = loc
                        ls += len(left)
                        le -= len(right)
                        valid = (ls < le)
                        if not valid:
                            continue

                        new_loc = (ls, le)
                        blank_str = cm.jointText(blank_str, mid, new_loc)

                    temp_list = cm.findInvert(df.FILLER_CHAR_PATTERN, blank_str)
                    for loc, mm in temp_list.items():
                        entry = (loc, mm.txt)
                        corrected_list.append(entry)

                    for index, entry in enumerate(corrected_list):
                        is_entry_untranslated = (index in any_index_list)
                        if is_entry_untranslated:
                            tran_required_list.append(entry)

                    the_new_tl_txt = blank_str.replace(df.FILLER_CHAR, ' ')
                except Exception as e:
                    df.LOG(e)
                df.LOG('corrected_list for translation:')
                pp('-' * 45)
                pp(corrected_list, width=200)
                dd('required to translate:')
                pp(tran_required_list, width=200)
                dd('the_new_tl_txt')
                pp(the_new_tl_txt, width=200)
                pp('-' * 45)
                return corrected_list, tran_required_list, the_new_tl_txt

            dict_tl_txt = self.dict_tl_rec.txt
            dict_tl_list = self.dict_tl_rec.getSubEntriesAsList()

            new_tl_txt_list, any_index_list = creatTLTextList()
            corrected_sent_tl_list, text_to_translate_list, new_sent_tl_txt = correctIndexOfTLTextList(new_tl_txt_list, any_index_list)

            temp_dict = OrderedDict(corrected_sent_tl_list)
            n_mm = MatcherRecord(s=0, e=len(new_sent_tl_txt), txt=new_sent_tl_txt)
            n_mm.appendSubRecords(corrected_sent_tl_list)
            self.sent_tl_rec = n_mm
            # df.LOG(f'return n_mm:[{n_mm}]')
            return text_to_translate_list

        if bool(self.text_list_to_be_translated):
            return self.text_list_to_be_translated

        text_to_translate_list=None
        dict_sl_any_index_list = None
        dict_tl_any_index_list = None
        sent_sl_list_of_txt = None
        sent_tl_list = None
        try:
            dict_sl_any_index_list = getListOfAnythingPosition(self.dict_sl_wordlist)
            # indexes of $$$ in the dictionary's target language entry in the form of [int, int...]
            dict_tl_any_index_list = getListOfAnythingPosition(self.dict_tl_wordlist)

            # list of text in the external source language sentence, with untranslated text
            sent_sl_list_of_txt = self.sent_sl_rec.getSubEntriesAsList()
            # list of texts in external source language sentence, with untranslated text, but will be
            # replaced with translated parts from the dictionary target language ie. text on both sides of $$$
            sent_tl_list = self.sent_tl_rec.getSubEntriesAsList()

            any_list = getInitialListOfTextsToBeTranslated()
            if any_list:
                text_to_translate_list = correctTextsOffsets(any_list)
            else:
                self.sent_tl_rec.setTranslated()
                text_to_translate_list = []
        except Exception as e:
            # df.LOG(e, error=True)
            # if self.is_sent_struct:
            #     exit(0)
            try:
                main_loc = self.sent_sl_rec.getMainLoc()
                main_txt = self.sent_sl_rec.getMainText()
                # loc = (self.root_location if bool(self.root_location) else main_loc)
                entry=(main_loc, main_txt)
                text_to_translate_list.append(entry)
            except Exception as ee:
                df.LOG(ee, error=True)
        return text_to_translate_list

    def setTLTranslationOverride(self, sl_txt, tl_txt):
        self.sent_tl_rec.txt = tl_txt
        self.updateProcessed({sl_txt: tl_txt})

    def setTlTranslation(self, trans_list: list):
        tl_txt = self.sent_tl_rec.txt
        tl_txt_len = len(tl_txt)
        trans_list.sort(reverse=True)
        for loc, tran_txt in trans_list:
            tl_txt = cm.jointText(tl_txt, tran_txt, loc)
        self.sent_tl_rec.txt = tl_txt
        self.sent_tl_rec.e = len(self.sent_tl_rec.txt)
        self.updateProcessed({self.sent_sl_rec.txt: self.sent_tl_rec.txt})

    def getTranFromProcessed(self, txt):
        try:
            tran = self.processed_list[txt]
            if tran:
                return tran

            left, mid, right = cm.getTextWithin(txt)
            is_valid = ((left or right) and (left != right))
            if not is_valid:
                return None

            tran = self.processed_list[mid]
            if not tran:
                return None

            tran = left + tran + right
            return tran
        except Exception as e:
            df.LOG(e, error=True)
            return None

    def updateProcessed(self, entry):
        self.processed_list.update(entry)
        self.tf.getDict().addCacheEntry(entry)

    def getTranslation(self):
        try:
            current_tran = self.sent_tl_rec.txt
            return current_tran
        except Exception as e:
            df.LOG(e, error=True)
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
            df.LOG(e, error=True)
            return 0

    def makeNonSRRecord(self, txt, root_location):
        sr = self.reproduce()
        print(f'IS TEXT:[{txt}]')
        current_processed_list = self.processed_list.keys()
        is_ignore = (txt in current_processed_list)
        if is_ignore:
            dd(f'makeNonSRRecord: [{txt}] is already processed')
            return None

        sr.__init__(
            root_loc=root_location,
            tran_sl_txt=txt,
            translation_engine=self.tf,
            processed_dict=self.processed_list,
            glob_sr=self.global_sr_list
        )
        sr.setupRecords()
        sr.getTextListTobeTranslated()
        self.global_sr_list.update({sr.tran_sl_txt: sr})
        return sr

    def makeSRRecord(self, txt, root_location):
        try:
            # st_time = time.perf_counter()
            # (dict_sl_pat, (dict_sl_txt, dict_sl_word_list, dict_sl_mm, dict_tl_txt, dict_tl_word_list, dict_tl_mm, sent_sl_mm))
            (dict_sl_pat, extra_value) = self.getDict().getSentStructPattern(txt)
            (dict_sl_txt, dict_sl_word_list, dict_sl_mm, dict_tl_txt, dict_tl_word_list, dict_tl_mm, sent_sl_mm) = extra_value

            # ed_time = time.perf_counter()
            # p_time = (ed_time - st_time)

            current_processed_list = self.processed_list.keys()
            is_already_processed = (dict_sl_txt in current_processed_list)
            is_ignore = (not dict_sl_pat) or (is_already_processed)
            if is_already_processed:
                dd(f'makeSRRecord: [{txt}] is already processed')

            if is_ignore:
                return None

            # print(f'IS STRUCTURE:[txt:{txt}] => sl:[{dict_sl_txt}] tl:[{dict_tl_txt}] pat:[{dict_sl_pat}]')
            sr = self.reproduce()
            sr.__init__(root_loc=root_location,
                        dict_sl_txt=dict_sl_txt,
                        dict_sl_word_list=dict_sl_word_list,
                        dict_sl_rec=dict_sl_mm,

                        dict_tl_rec=dict_tl_mm,
                        dict_tl_word_list=dict_tl_word_list,
                        dict_tl_txt=dict_tl_txt,

                        tran_sl_txt=txt,
                        tran_sl_rec=sent_sl_mm,
                        recog_pattern=dict_sl_pat,
                        translation_engine=self.tf,
                        processed_dict=self.processed_list,
                        glob_sr=self.global_sr_list
                        )
            sr.setupRecords()
            need_tran = sr.getTextListTobeTranslated()
            if need_tran:
                df.LOG(f'needed tran:{need_tran}')
                self.global_sr_list.update({sr.tran_sl_txt: sr})
            else:
                df.LOG(f'NO need translations, PROVIDED or LEAVE AS IS!')
            return sr
        except Exception as e:
            df.LOG(e, error=True)

    def makeTranslatedSR(self, loc: tuple, txt: str, tran: str):
        sr = self.reproduce()
        sr.__init__(
            root_loc=loc,
            tran_sl_txt=txt,
            tran_tl_txt=tran,
            translation_engine=self.tf,
            processed_dict=self.processed_list,
            glob_sr=self.global_sr_list,
        )
        sr.makeSentTLRecord(loc, txt, tran)
        self.global_sr_list.update({txt: sr})
        return sr

    def parseAndTranslateText(self, orig_loc: int, txt: str):
        def processed(loc, txt, tran):
            obs.markLocAsUsed(loc)
            entry={txt: tran}
            self.updateProcessed(entry)

        def collectTranslation(loc, txt, tran):
            entry=(loc, txt, tran)
            translated_list.append(entry)
            processed(loc, txt, tran)

        def preTranslate(current_unproc_map):
            for loc, sub_txt in current_unproc_map:
                # cm.debugging(sub_txt)
                tran = self.tf.isInDict(sub_txt)
                if not tran:
                    continue

                entry = {sub_txt: tran}
                self.local_dict.update(entry)

                sub_left, sub_mid, sub_right = cm.getTextWithin(sub_txt)
                is_add_mid = (sub_left or sub_right)
                if not is_add_mid:
                    continue

                tran_left, tran_mid, tran_right = cm.getTextWithin(tran)
                entry = {sub_mid: tran_mid}
                self.local_dict.update(entry)

        def makeSRStructFirst(current_unproc_map):
            count = 0
            for sr_loc, sr_sub_txt in current_unproc_map:
                is_finish = obs.isCompletelyUsed()
                if is_finish:
                    break

                is_used = obs.isLocUsed(sr_loc)
                if is_used:
                    continue

                wc = len(sr_sub_txt.split())
                is_single_word = (wc == 1)
                if is_single_word:
                    continue

                # tran = self.tf.isInDict(sr_sub_txt)
                # is_translated = (tran is not None)
                # if is_translated:
                #     sr = self.makeTranslatedSR(sr_loc, sr_sub_txt, tran)
                #     entry = (sr_loc, sr)
                #     parsed_list.append(entry)
                #     collectTranslation(sr_loc, sr_sub_txt, tran)
                #     continue

                # cm.debugging(sr_sub_txt)
                # removing the end punctuations
                is_ended_punct = df.END_BASIC_PUNCTUAL.search(sr_sub_txt)
                if is_ended_punct:
                    end_punct = is_ended_punct.group(0)
                    (sr_s, sr_e) = sr_loc
                    len_of_punct = len(end_punct)
                    sr_e -= len_of_punct
                    sr_sub_txt = sr_sub_txt[:-len_of_punct]
                    sr_loc = (sr_s, sr_e)

                # dd(f'trying to make SR with: [{sr_sub_txt}]')
                sr = self.makeSRRecord(sr_sub_txt, sr_loc)
                if sr:
                    entry = (sr_loc, sr)
                    parsed_list.append(entry)
                    processed(sr_loc, sr_sub_txt, None)
                    count += 1
            # print(count)

        def makeNonSR():
            un_tran = obs.getUnmarkedPartsAsDict()
            mm_record: MatcherRecord = None

            for non_sr_loc, mm_record in un_tran.items():
                sub_txt = mm_record.txt

                is_ignore = ig.isIgnored(sub_txt)
                if is_ignore:
                    continue

                sr = self.makeNonSRRecord(sub_txt, non_sr_loc)
                if not sr:
                    continue

                list_of_txt_to_be_tran = sr.getTextListTobeTranslated()
                for tran_loc, txt in list_of_txt_to_be_tran:
                    (non_sr_s, non_sr_e) = non_sr_loc
                    (tran_loc_s, tran_loc_e) = tran_loc
                    diff_length = (tran_loc_e - tran_loc_s)
                    actual_loc_s = non_sr_s + tran_loc_s
                    actual_loc_e = actual_loc_s + diff_length
                    actual_loc = (actual_loc_s, actual_loc_e)
                    entry = (actual_loc, sr)
                    parsed_list.append(entry)
                processed(non_sr_loc, sub_txt, None)

        translation = str(txt)
        origin = str(txt)
        sr: StructRecogniser = None

        obs = LocationObserver(txt)
        map = cm.genmap(txt)
        parsed_list=[]
        translated_list=[]

        wc = len(txt.split())
        is_single_word = (wc == 1)
        if not is_single_word:
            st_time = time.perf_counter()
            makeSRStructFirst(map)
            ed_time = time.perf_counter()
            p_time = (ed_time - st_time)

        makeNonSR()

        parsed_list.sort(reverse=True)
        for sr_parsed_loc, sr in parsed_list:
            is_translated = (sr.sent_tl_rec.isTranslated())
            if is_translated:
                tran = (sr.sent_tl_rec.txt)
            else:
                tran = sr.translate()
            if tran:
                txt = sr.tran_sl_txt
                collectTranslation(sr_parsed_loc, txt, tran)

        for sr_parsed_loc, sr in parsed_list:
            tran = sr.getTranslation()
            translation = cm.jointText(translation, tran, sr_parsed_loc)

        is_valid = (translation and translation != origin)
        if not is_valid:
            return None
        else:
            df.LOG(f'OBTAIN TRANSLATION: origin:[{origin}] translation:[{translation}]')
            processed(orig_loc, origin, translation)
            return translation

    def translate(self):
        def addTranEntry(txt_loc, txt_sl, txt_tl):
            is_valid = (bool(txt_tl) and (txt_tl != txt_sl))
            if is_valid:
                entry=(txt_loc, tran)
                tran_list.append(entry)
                entry = {txt_sl: txt_tl}
                self.updateProcessed(entry)

        try:
            txt = self.tran_sl_txt
            tran = self.tf.isInDict(txt)
            if tran:
                self.setTLTranslationOverride(txt, tran)
                return tran

            tran_list=[]
            list_needed_to_translate = self.getListOfTextsNeededToTranslate()
            for loc, txt in list_needed_to_translate:
                is_processed = (txt in self.processed_list)
                if is_processed:
                    tran = self.translateText(txt)
                else:
                    tran = self.parseAndTranslateText(loc, txt)

                addTranEntry(loc, txt, tran)
                if tran:
                    tran = cm.matchCase(txt, tran)

            if tran_list:
                self.setTlTranslation(tran_list)
                return self.getTranslation()
            else:
                return None
        except Exception as e:
            df.LOG(f'{e}: txt:[{txt}]', error=True)
            return None

    def translateText(self, txt):
        try:
            trans, is_fuzzy, is_ignore = self.tf.translate(txt)
            self.setAddFuzzy(is_fuzzy)
            self.setAddIgnore(is_ignore)
            return trans
        except Exception as e:
            df.LOG(e)
            return None

