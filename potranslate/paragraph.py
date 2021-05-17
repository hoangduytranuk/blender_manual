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
            df.LOG(e)
            return None

    def getTranslation(self):
        # return self.formatOutput()
        return self.tl_txt

    def getTextAndTranslation(self):
        return self.formatOutput()

    def translate(self):
        fname = INP.currentframe().f_code.co_name

        try:
            tran = self.tf.isInDict(self.sl_txt)
            if not tran:
                sr = SR(translation_engine=self.tf, processed_dict=self.parsed_dict, glob_sr=self.sr_global_dict)
                loc = (0, len(self.sl_txt))
                tran = sr.parseAndTranslateText(loc, self.sl_txt)
                if tran:
                    # tran = cm.removeTheWord(tran)
                    cache_entry = {self.sl_txt: tran}
                    self.tf.getDict().addCacheEntry(cache_entry)
            self.tl_txt = tran
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
            df.LOG(f'{e};')
