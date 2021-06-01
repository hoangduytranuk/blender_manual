import time

from common import Common as cm, dd, pp, LocationObserver
from translation_finder import TranslationFinder
from sentence import StructRecogniser as SR
from nocasedict import NoCaseDict as NDIC
from definition import Definitions as df
import inspect as INP

class Paragraph(list):
    def __init__(self, txt, translation_engine=None):
        self.sl_txt = txt
        self.tl_txt = None
        self.tf = translation_engine
        self.parsed_dict = NDIC()
        self.sr_global_dict = NDIC()

    def formatOutput(self):
        try:
            tran = self.tl_txt.replace('"', '\\"')
            orig = self.sl_txt.replace('"', '\\"')
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

    def translate(self):
        fname = INP.currentframe().f_code.co_name

        try:
            input_txt = self.sl_txt
            txt_list = cm.findInvert(df.SPLIT_SENT_PAT, input_txt)
            dd('TRANSLATING LIST OF SEGMENTS:')
            pp(txt_list)
            dd('-' * 80)
            tran_list = []
            for loc, mm in txt_list.items():
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
                    tran_list.append(tran_list_entry)

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
            df.LOG(f'from:[{self.sl_txt}]=>[{self.tl_txt}]')
        except Exception as e:
            df.LOG(f'{e};', error=True)
