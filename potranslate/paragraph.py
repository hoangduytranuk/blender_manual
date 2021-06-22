import time
from common import Common as cm, dd, pp, LocationObserver
from sentence import StructRecogniser as SR
from definition import Definitions as df
from reflist import RefList

class Paragraph(list):
    def __init__(self, txt, translation_engine=None):
        self.sl_txt = txt
        self.tl_txt = None
        self.tf = translation_engine
        # self.parsed_dict = NDIC()
        # self.sr_global_dict = NDIC()

    def formatOutput(self):
        try:
            tran = self.tl_txt
            if tran:
                tran = tran.replace('\\', '\\\\')
                tran = tran.replace('"', '\\"')
            else:
                tran = ""

            orig = self.sl_txt
            orig = orig.replace('\\', '\\\\')
            orig = orig.replace('"', '\\"')
            output = f'"{orig}": "{tran}",'
            return output
        except Exception as e:
            df.LOG(e, error=True)
            return None

    def getTranslation(self):
        # return self.formatOutput()
        return self.tl_txt

    def getTextAndTranslation(self):
        return self.formatOutput()

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

    def translateAsIs(self):
        try:
            orig_txt = self.sl_txt
            tran = self.tf.isInDict(orig_txt)
            if not tran:
                tran = self.translateText(orig_txt)
            if tran:
                tran = cm.removeTheWord(tran)
                self.tl_txt = tran
                df.LOG(f'from:[{self.sl_txt}]=>[{self.tl_txt}]')
        except Exception as e:
            df.LOG(f'{e};', error=True)

    def translateSplitUp(self):
        def translateOneRecord(item):
            (loc, mm) = item
            orig_txt = mm.txt
            tran = self.tf.isInDict(orig_txt)
            if not tran:
                sr = SR(translation_engine=self.tf, processed_dict=self.parsed_dict, glob_sr=self.sr_global_dict)
                tran = sr.parseAndTranslateText(loc, orig_txt)

            if tran:
                tran = cm.removeTheWord(tran)
                cache_entry = {self.sl_txt: tran}
                self.tf.getDict().addCacheEntry(cache_entry)
                tran_list_entry = (loc, orig_txt, tran)
                return tran_list_entry
            else:
                return None

        try:
            input_txt = self.sl_txt
            txt_list = cm.findInvert(df.SPLIT_SENT_PAT, input_txt)
            dd('TRANSLATING LIST OF SEGMENTS:')
            pp(txt_list)
            dd('-' * 80)
            tran_list = []

            temp_tran_list = map(translateOneRecord, txt_list.items())
            tran_list = [x for x in temp_tran_list if bool(x)]

            translation = str(input_txt)
            if tran_list:
                tran_list.sort(reverse=True)
                for loc, orig_txt, tran in tran_list:
                    translation = cm.jointText(translation, tran, loc)

                self.tl_txt = translation

            sr: SR = None
            # for txt, sr in self.sr_global_dict.items():
            #     dd('-' * 80)
            #     dd(f'{fname}()')
            #     dd(f'pattern:{sr.recog_pattern.pattern}; [{sr.dict_sl_rec.txt} => {sr.dict_tl_rec.txt}]')
            #     dd(f'dict_sl_rec:{sr.sent_sl_rec.txt};')
            #     dd(f'sent_tl_rec:{sr.sent_tl_rec.txt};')
            #     dd(f':{sr.getTextListTobeTranslated()};')
            # df.LOG(f'from:[{self.sl_txt}]=>[{self.tl_txt}]')
        except Exception as e:
            df.LOG(f'{e};', error=True)
