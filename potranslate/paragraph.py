from common import Common as cm, dd, pp, LocationObserver
from translation_finder import TranslationFinder
from sentence import StructRecogniser as SR

class Paragraph(list):
    def __init__(self, txt, translation_engine=None):
        self.msg = txt
        # self.msg = "To view your changes, build the manual :doc:`as instructed </about/contribute/build/index>`. Keep in mind that you can also build only the chapter you just edited to view it quickly. Open the generated ``.html`` files inside the ``build/html`` folder using your web browser, or refresh the page if you have it open already."
        self.translation = None
        self.tf = translation_engine
        self.dict = None
        if translation_engine:
            self.dict = translation_engine.getDict()

    def makeSRRecord(self, txt, root_location):
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
        else:
            sr = SR(root_loc=root_location, tran_sl_txt=txt, translation_engine=self.tf)
        sr.root_location = root_location
        return sr

    def translate(self):
        def translateUsingSR(txt):
            sr: SR = None
            record_index = 0
            sr_dict={}
            prev_text_list=[]
            local_sub_text_list=[]
            is_finished = False
            sr = self.makeSRRecord(txt, loc)
            # ls, le = loc
            # test_txt = orig_txt[ls: le]
            sr_dict.update({record_index: sr})
            record_index += 1
            prev_text_list.append(txt)
            sub_text_list = sr.getTextListTobeTranslated()
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

            translated_list=[]
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

        msg = self.msg
        map = cm.genmap(msg)
        obs = LocationObserver(msg)

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
                tran = translateUsingSR(orig_txt)
            if tran:
                obs.markLocAsUsed(loc)
                covering_length = len(txt)
                entry = (loc, covering_length, txt, tran)
                translated_entries.append(entry)

        # there shouldn't be any part not translated at this point
        if not translated_entries:
            self.translation = None
        else:
            translation = str(self.msg)
            for loc, covering_length, sl_txt, tl_txt in translated_entries:
                translation = cm.jointText(translation, tl_txt, loc)
            self.translation = translation
        return self.translation