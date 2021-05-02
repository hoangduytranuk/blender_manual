from common import Common as cm, dd, pp, LocationObserver
from translation_finder import TranslationFinder
from sentence import StructRecogniser as SR

class Paragraph(list):
    def __init__(self, txt, translation_engine=None):
        self.sl_txt = txt
        # self.msg = "To view your changes, build the manual :doc:`as instructed </about/contribute/build/index>`. Keep in mind that you can also build only the chapter you just edited to view it quickly. Open the generated ``.html`` files inside the ``build/html`` folder using your web browser, or refresh the page if you have it open already."
        self.tl_txt = None
        self.tf = translation_engine

        self.dict = None
        if translation_engine:
            self.dict = translation_engine.getDict()

        self.part_list = []

    def makeSRRecord(self, txt, root_location):
        sr = self.makeSRRecordOnly(txt, root_location)
        if not sr:
            sr = self.makeNonSRRecord(txt, root_location)
        return sr

    def makeNonSRRecord(self, txt, root_location):
        sr = SR(root_loc=root_location, tran_sl_txt=txt, translation_engine=self.tf)
        return sr

    def makeSRRecordOnly(self, txt, root_location):
        dict_sl_pat, (dict_sltxt, dict_tltxt, dict_tl_mm_record, dict_tl_list) = self.dict.getSentStructPattern(txt)
        if dict_sl_pat:
            print(f'IS STRUCTURE:{txt} => {dict_tltxt}')
            sr = SR(root_loc=root_location,
                    dict_sl_txt=dict_sltxt,
                    dict_tl_txt=dict_tltxt,
                    tran_sl_txt=txt,
                    recog_pattern=dict_sl_pat,
                    dict_tl_rec=dict_tl_mm_record,
                    translation_engine=self.tf)
            return sr
        return None

    def translateMasterSR(self, master_sr_record: SR, master_translated_entries: list):
        '''
            Dealing with sub-SR records within the text if any
        '''
        sr: SR = None
        record_index = 0
        sr_dict={}
        prev_text_list=[]
        local_sub_text_list=[]
        is_finished = False
        sr_dict.update({record_index: master_sr_record})
        record_index += 1
        prev_text_list.append(master_sr_record.tran_sl_txt)
        sub_text_list = master_sr_record.getTextListTobeTranslated()
        local_sub_text_list.extend(sub_text_list)
        while not is_finished:
            sub_txt_list=[]
            for sub_loc, sub_txt in local_sub_text_list:
                if sub_txt in prev_text_list:
                    continue
                sr = self.makeSRRecord(sub_txt, sub_loc)
                prev_text_list.append(sub_txt)
                sr_dict.update({record_index: sr})
                record_index += 1
                sr_txt_list = sr.getTextListTobeTranslated()
                sub_txt_list.extend(sr_txt_list)

            local_sub_text_list.clear()
            local_sub_text_list.extend(sub_txt_list)
            is_finished = not bool(local_sub_text_list)

        translated_list=master_translated_entries
        sr_list = list(sr_dict.items())
        sr_list.reverse()
        for index, sr in sr_list:
            used_count = sr.usePrevTran(translated_list)
            if not used_count:
                sr.translate()

            tran = sr.getTranslation()
            sr_loc = sr.root_location
            entry = (sr_loc, sr.tran_sl_txt, tran)
            translated_list.append(entry)

        if translated_list:
            tran_count = len(translated_list)
            sr_loc, sl_txt, tran = translated_list[tran_count-1]
        else:
            tran = None
        return tran

    def parseText(self):
        msg = self.sl_txt
        map = cm.genmap(msg, is_reverse=True)
        obs = LocationObserver(msg)
        sr_list = []
        translated_entries = []

        for loc, txt in map:
            is_fully_translated = obs.isCompletelyUsed()
            if is_fully_translated:
                break

            is_used = obs.isLocUsed(loc)
            if is_used:
                continue

            orig_txt = obs.getTextAtLoc(loc)
            tran = self.tf.isInDict(orig_txt)
            if not tran:
                sr_record = self.makeSRRecordOnly(orig_txt, loc)
                if sr_record:
                    entry=(loc, sr_record)
                    sr_list.append(entry)
                    obs.markLocAsUsed(loc)
            else:
                entry = (loc, orig_txt, tran)
                translated_entries.append(entry)

        un_tran_dict = obs.getUnmarkedPartsAsDict()
        for loc, mm_record in un_tran_dict.items():
            txt = mm_record.txt
            sr_record = self.makeNonSRRecord(txt, loc)
            entry=(loc, sr_record)
            sr_list.append(entry)

        sr_list.reverse()
        for loc, sr_record in sr_list:
            tran = self.translateMasterSR(sr_record, translated_entries)
            if tran:
                sl_txt = sr_record.tran_sl_txt
                entry = (loc, sl_txt, tran)
                translated_entries.append(entry)

        # there shouldn't be any part not translated at this point
        if not translated_entries:
            self.tl_txt = None
        else:
            translation = str(self.sl_txt)
            for loc, sl_txt, tl_txt in translated_entries:
                translation = cm.jointText(translation, tl_txt, loc)
            self.tl_txt = translation
        return self.tl_txt

    # def translate(self):
    #     def translateUsingSR(txt):
    #         sr: SR = None
    #         record_index = 0
    #         sr_dict={}
    #         prev_text_list=[]
    #         local_sub_text_list=[]
    #         is_finished = False
    #         sr = self.makeSRRecord(txt, loc)
    #         # ls, le = loc
    #         # test_txt = orig_txt[ls: le]
    #         sr_dict.update({record_index: sr})
    #         record_index += 1
    #         prev_text_list.append(txt)
    #         sub_text_list = sr.getTextListTobeTranslated()
    #         local_sub_text_list.extend(sub_text_list)
    #         while not is_finished:
    #             sub_txt_list=[]
    #             for sub_loc, sub_txt in local_sub_text_list:
    #                 if sub_txt in prev_text_list:
    #                     continue
    #                 sr = self.makeSRRecord(sub_txt, sub_loc)
    #                 prev_text_list.append(sub_txt)
    #                 sr_dict.update({record_index: sr})
    #                 record_index += 1
    #                 sr_txt_list = sr.getTextListTobeTranslated()
    #                 sub_txt_list.extend(sr_txt_list)
    #
    #             local_sub_text_list.clear()
    #             local_sub_text_list.extend(sub_txt_list)
    #             is_finished = not bool(local_sub_text_list)
    #
    #         translated_list=[]
    #         sr_list = list(sr_dict.items())
    #         sr_list.reverse()
    #         for index, sr in sr_list:
    #             used_count = sr.usePrevTran(translated_list)
    #             if not used_count:
    #                 sr.translate()
    #
    #             tran = sr.getTranslation()
    #             sr_loc = sr.root_location
    #             entry = (sr_loc, sr.tran_sl_txt, tran)
    #             translated_list.append(entry)
    #
    #         if translated_list:
    #             tran_count = len(translated_list)
    #             sr_loc, sl_txt, tran = translated_list[tran_count-1]
    #         else:
    #             tran = None
    #         return tran
    #
    #     msg = self.msg
    #     map = cm.genmap(msg)
    #     obs = LocationObserver(msg)
    #
    #     translated_entries = []
    #     for loc, txt in map:
    #         is_fully_translated = obs.isCompletelyUsed()
    #         if is_fully_translated:
    #             break
    #
    #         is_used = obs.isLocUsed(loc)
    #         if is_used:
    #             continue
    #
    #         orig_txt = obs.getTextAtLoc(loc)
    #         tran = self.tf.isInDict(orig_txt)
    #         if not tran:
    #             tran = translateUsingSR(orig_txt)
    #         if tran:
    #             obs.markLocAsUsed(loc)
    #             covering_length = len(txt)
    #             entry = (loc, covering_length, txt, tran)
    #             translated_entries.append(entry)
    #
    #     # there shouldn't be any part not translated at this point
    #     if not translated_entries:
    #         self.translation = None
    #     else:
    #         translation = str(self.msg)
    #         for loc, covering_length, sl_txt, tl_txt in translated_entries:
    #             translation = cm.jointText(translation, tl_txt, loc)
    #         self.translation = translation
    #     return self.translation