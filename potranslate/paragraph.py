from common import Common as cm, dd, pp, LocationObserver
from translation_finder import TranslationFinder
from sentence import StructRecogniser as SR

class Paragraph():
    def __init__(self, txt, translation_engine=None):
        self.msg = txt
        # self.msg = "To view your changes, build the manual :doc:`as instructed </about/contribute/build/index>`. Keep in mind that you can also build only the chapter you just edited to view it quickly. Open the generated ``.html`` files inside the ``build/html`` folder using your web browser, or refresh the page if you have it open already."
        self.translation = None
        self.tf = translation_engine
        self.dict = None
        if translation_engine:
            self.dict = translation_engine.getDict()

    def translate(self):
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
                dict_sl_pat, (dict_sltxt, dict_tltxt, dict_tl_mm_record, dict_tl_list) = self.dict.getSentStructPattern(orig_txt)
                if dict_sl_pat:
                    print(f'IS STRUCTURE:{orig_txt} => {dict_tltxt}')
                    sr = SR(dict_sl_txt=dict_sltxt,
                            dict_tl_txt=dict_tltxt,
                            tran_sl_txt=orig_txt,
                            recog_pattern=dict_sl_pat,
                            dict_tl_rec=dict_tl_mm_record,

                            translation_engine=self.tf)
                else:
                    sr = SR(tran_sl_txt=orig_txt, translation_engine=self.tf)
                sr.translate()
                tran = sr.getTranslation()
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