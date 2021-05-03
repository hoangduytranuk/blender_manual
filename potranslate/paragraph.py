from common import Common as cm, dd, pp, LocationObserver
from translation_finder import TranslationFinder
from sentence import StructRecogniser as SR

class Paragraph(list):
    def __init__(self, txt, translation_engine=None):
        self.sl_txt = txt
        # self.msg = "To view your changes, build the manual :doc:`as instructed </about/contribute/build/index>`. Keep in mind that you can also build only the chapter you just edited to view it quickly. Open the generated ``.html`` files inside the ``build/html`` folder using your web browser, or refresh the page if you have it open already."
        self.tl_txt = None
        self.tf = translation_engine
        self.parsed_dict = {}

    def formatOutput(self):
        try:
            tran = self.tl_txt.replace('"', '\\"')
            orig = self.sl_txt.replace('"', '\\"')
            output = f'"{orig}": "{tran}",'
            return output
        except Exception as e:
            print(e)
            return None

    def getTranslation(self):
        return self.formatOutput()

    def translate(self):
        try:
            tran = self.tf.isInDict(self.sl_txt)
            if not tran:
                sr = SR(translation_engine=self.tf, processed_dict=self.parsed_dict)
                tran = sr.parseAndTranslateText(self.sl_txt)
            self.tl_txt = tran
        except Exception as e:
            print(e)
