from common import Common as cm, dd, pp, LocationObserver
from matcher import MatcherRecord
from definition import Definitions as df
import re
import copy as CP
from reflist import RefList
from collections import OrderedDict
import inspect as INP
from nocasedict import NoCaseDict as NDIC
from ignore import Ignore as ig
import operator as OP
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
                 tran_tl_txt = None,

                 translation_engine=None,
                 processed_dict=None,
                 glob_sr=None
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

        self.sent_sl_rec: MatcherRecord = None
        self.sent_tl_rec: MatcherRecord = None
        self.tf = translation_engine
        self.root_location = root_loc
        self.text_list_to_be_translated = None
        self.processed_list: NDIC = processed_dict
        self.text_list_to_be_translated = None
        self.local_dict = NDIC()
        self.global_sr_list=glob_sr

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
            df.LOG(f'{e}')
            if bool(self.tran_sl_txt):
                self.sent_sl_rec = MatcherRecord(txt=self.tran_sl_txt)
                self.sent_tl_rec = MatcherRecord(txt=self.tran_sl_txt)

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

                for index, from_index in enumerate(dict_sl_any_index_list):
                    to_index = dict_tl_any_index_list[index]
                    df.LOG(f'dict_tl_any_index_list[index]:[{dict_tl_any_index_list}] [index{index}] => to_index:{to_index}')
                    # extract untranslated text out of external sentence where $$$ supposedly occupied
                    # this will give you texts supposedly to be translated:
                    # such as:
                    #           the structure from CONSTRUCTIVE
                    #           DECONSTRUCTIVE
                    df.LOG(f'sent_sl_list_of_txt[from_index]:[{sent_sl_list_of_txt}] [from_index{from_index}] => sent_sl_list_of_txt[from_index]:{sent_sl_list_of_txt[from_index]}')
                    untran_loc, untran_txt = sent_sl_list_of_txt[from_index]
                    dict_tl_pat_txt, dict_tl_smode_item = dict_tl_smode_list[to_index]
                    dict_sl_pat_txt, dict_sl_smode_item = dict_sl_smode_list[from_index]
                    tl_mode_rec:SMODEREC = dict_tl_smode_item[0]
                    sl_mode_rec:SMODEREC = dict_sl_smode_item[0]

                    is_sl_order = (sl_mode_rec.smode == SMODE.ORDERED_GROUP)
                    is_tl_order = (tl_mode_rec.smode == SMODE.ORDERED_GROUP)
                    is_order = (is_sl_order and is_tl_order)
                    if is_order:
                        tl_order = tl_mode_rec.extra_param
                        sl_order = sl_mode_rec.extra_param
                        is_matching = (sl_order == tl_order)
                        if not is_matching:
                            new_entry = {tl_order: untran_txt}
                            order_queue.update(new_entry)
                            continue

                    # new_entry = (untran_loc, (any_tl_pattern_txt, untran_txt))
                    new_entry = (untran_loc, untran_txt)

                    # insert into the correct position, but offsets of next text items will be out of sync
                    # (cloc, ctxt) = sent_tl_list.pop(to_index)
                    # sent_tl_list.insert(to_index, new_entry)
                    any_list.append(new_entry)

                if order_queue:
                    sorted_queue = list(order_queue.items())
                    sorted_queue.sort()

                    new_sent_tl_list = []
                    if any_list:
                        raise ValueError(f'UNHANDLED situation: have ORDER QUEUE [{order_queue}] and ANY LIST: [{any_list}]')
                        # # for current_untran_loc, tl_pat_or_txt in sent_tl_list:
                        # for current_untran_loc, tl_pat_or_txt in any_list:
                        #     is_order = df.REGULAR_VAR_PAT.search(tl_pat_or_txt)
                        #     if is_order:
                        #         ord_group_list = is_order.groups()
                        #         order = int(ord_group_list[1])
                        #         (untran_loc, untran_txt) = order_queue[order]
                        #         entry = (untran_loc, untran_txt)
                        #         new_sent_tl_list.append(entry)
                        #     else:
                        #         entry = (current_untran_loc, tl_pat_or_txt)
                        #         new_sent_tl_list.append(entry)
                        # df.LOG(f'RETURN new_sent_tl_list:{new_sent_tl_list}')
                        # return new_sent_tl_list
                    else:
                        return sorted_queue
                else:
                    # df.LOG(f'RETURN sent_tl_list:{sent_tl_list}')
                    # return sent_tl_list
                    return any_list

            except Exception as e:
                df.LOG(e, error=True)
                raise e

        def moveEndingPunctuationsIfNeeded(to_index):
            fname = INP.currentframe().f_code.co_name
            try:
                new_entry = sent_tl_list[to_index]
                new_loc, new_txt = new_entry

                next_index = to_index+1
                next_entry = sent_tl_list[next_index]

                left, mid, right = cm.getTextWithin(new_txt)
                is_ending_punctual = (df.BEGIN_AND_END_BASIC_PUNCTUAL_IN_MID_SENT.search(right) is not None)
                if not is_ending_punctual:
                    return None, None

                new_entry = (new_loc, left + mid)
                (next_loc, next_txt) = next_entry
                nleft, nmid, nright = cm.getTextWithin(next_txt)
                is_nright_spaces = (not bool(nright.strip()))
                if is_nright_spaces:
                    next_txt = nleft + nmid + right + nright
                else:
                    next_txt += next_txt + right
                next_entry = (next_loc, next_txt)
                return new_entry, next_entry
            except Exception as e:
                df.LOG(e, error=True)
                return None, None

        # def getTranSLFullTextList():
        #     obs = LocationObserver(self.tran_sl_txt)
        #     copy_of_tran_sl_rec = CP.deepcopy(self.sent_sl_rec.getSubEntriesAsList())
        #     temp_dict = OrderedDict(copy_of_tran_sl_rec)
        #     loc_list = temp_dict.keys()
        #     obs.markListAsUsed(loc_list)
        #     remaining_txt_list = obs.getRawUnmarkedPartsAsList()
        #
        #     copy_of_tran_sl_rec.extend(remaining_txt_list)
        #     copy_of_tran_sl_rec.sort()
        #
        #     return copy_of_tran_sl_rec

        def correctTextsOffsets(senttl_list):
            def creatTLTextList():
                any_index_list=[]
                dict_tl_txt = self.dict_tl_rec.txt
                dict_tl_list = cm.patStructToListOfWords(dict_tl_txt, removing_symbols=False)

                sent_tl_index = 0
                new_list = []
                senttl_list_length = len(senttl_list)
                for index, (loc, tl_txt) in enumerate(dict_tl_list):
                    (ls, le) = loc
                    is_pattern = (df.SENT_STRUCT_PAT.search(tl_txt) is not None)
                    if is_pattern:
                        senttl_loc, actual_tl_txt = senttl_list[sent_tl_index]
                        sent_tl_index = max(sent_tl_index + 1, senttl_list_length - 1)
                        any_index_list.append(index)
                    else:
                        actual_tl_txt = tl_txt

                    new_le = ls + len(actual_tl_txt)
                    new_loc = (ls, new_le)
                    new_entry = (new_loc, actual_tl_txt)
                    new_list.append(new_entry)
                df.LOG(f'RETURN new_list:[{new_list}]; any_index_list:[{any_index_list}]')
                return new_list, any_index_list

            def correctIndexOfTLTextList(the_new_list, any_index_list):
                df.LOG(f'the_new_list:[{the_new_list}]; any_index_list:[{any_index_list}]')
                index_corrected=[]
                tran_required_list = []
                ls = le = 0
                for index, (loc, txt) in enumerate(the_new_list):
                    txt_length = len(txt)
                    le = (ls + txt_length)
                    new_loc = (ls, le)
                    new_entry = (new_loc, txt)
                    index_corrected.append(new_entry)
                    is_entry_untranslated = (index in any_index_list)
                    if is_entry_untranslated:
                        tran_required_list.append(new_entry)
                    ls = le
                df.LOG(f'RETURN index_corrected:[{index_corrected}]; tran_required_list:[{tran_required_list}]')
                return index_corrected, tran_required_list

            new_tl_txt_list, any_index_list = creatTLTextList()
            corrected_sent_tl_list, text_to_translate_list  = correctIndexOfTLTextList(new_tl_txt_list, any_index_list)

            temp_dict = OrderedDict(corrected_sent_tl_list)
            txt_list = (temp_dict.values())
            new_sent_tl_txt = "".join(txt_list)

            ns = 0
            ne = len(new_sent_tl_txt)
            # Note, the s, e here is a temporal value, this will have to matched up with the originally parsed location
            n_mm = MatcherRecord(s=ns, e=ne, txt=new_sent_tl_txt)
            n_mm.appendSubRecords(corrected_sent_tl_list)
            self.sent_tl_rec = n_mm
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
            df.LOG(e, error=True)
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

    def setTLTranslationOverride(self, tl_txt):
        self.sent_tl_rec.txt = tl_txt
        self.updateProcessed({self.sent_sl_rec.txt: self.sent_tl_rec.txt})

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
            return self.sent_tl_rec.txt
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
            dict_sl_pat, (dict_sl_txt, dict_sl_word_list, dict_sl_mm, dict_tl_txt, dict_tl_word_list, dict_tl_mm) = self.getDict().getSentStructPattern(txt)
            current_processed_list = self.processed_list.keys()
            is_already_processed = (dict_sl_txt in current_processed_list)
            is_ignore = (not dict_sl_pat) or (is_already_processed)
            if is_already_processed:
                dd(f'makeSRRecord: [{txt}] is already processed')

            if is_ignore:
                return None

            print(f'IS STRUCTURE:[{txt}] => sl:[{dict_sl_txt}] tl:[{dict_tl_txt}] pat:[{dict_sl_pat}]')
            sr = self.reproduce()
            sr.__init__(root_loc=root_location,
                        dict_sl_txt=dict_sl_txt,
                        dict_sl_word_list=dict_sl_word_list,
                        dict_sl_rec=dict_sl_mm,

                        dict_tl_rec=dict_tl_mm,
                        dict_tl_word_list=dict_tl_word_list,
                        dict_tl_txt=dict_tl_txt,

                        tran_sl_txt=txt,
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

                cm.debugging(sr_sub_txt)
                is_ended_punct = df.END_BASIC_PUNCTUAL.search(sr_sub_txt)
                if is_ended_punct:
                    end_punct = is_ended_punct.group(0)
                    (sr_s, sr_e) = sr_loc
                    len_of_punct = len(end_punct)
                    sr_e -= len_of_punct
                    sr_sub_txt = sr_sub_txt[:-len_of_punct]
                    sr_loc = (sr_s, sr_e)

                dd(f'trying to make SR with: [{sr_sub_txt}]')
                sr = self.makeSRRecord(sr_sub_txt, sr_loc)
                if sr:
                    entry = (sr_loc, sr)
                    parsed_list.append(entry)
                    processed(sr_loc, sr_sub_txt, None)
                    count += 1
            print(count)

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
        map = cm.genmap(txt)
        obs = LocationObserver(txt)
        parsed_list=[]
        translated_list=[]

        makeSRStructFirst(map)
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
                self.setTLTranslationOverride(tran)
                return tran

            tran_list=[]
            list_needed_to_translate = self.getListOfTextsNeededToTranslate()
            for loc, txt in list_needed_to_translate:
                is_processed = (txt in self.processed_list)
                if is_processed:
                    tran = self.translateText(txt)
                    addTranEntry(loc, txt, tran)
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
            df.LOG(e, error=True)
            return None

    def translateText(self, txt):
        try:
            ref_list = RefList(msg=txt, keep_orig=False, tf=self.tf)
            ref_list.parseMessage()
            ref_list.translate()
            trans = ref_list.getTranslation()
            return trans
        except Exception as e:
            df.LOG(e)
            return None

