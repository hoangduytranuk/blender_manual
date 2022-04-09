
from definition import Definitions as df
from bracket import RefAndBracketsParser as PSER

class GetTextWithin:
    def __init__(self, msg: str, start_pattern=df.START_WORD_SYMBOLS, end_pattern=df.END_WORD_SYMBOLS):
        self.msg = msg
        self.start_pattern = start_pattern
        self.end_pattern = end_pattern

    @classmethod
    def reproduce(cls, msg, start_pattern=df.START_WORD_SYMBOLS, end_pattern=df.END_WORD_SYMBOLS):
        return cls(msg, start_pattern=start_pattern, end_pattern=end_pattern)

    def getNoneAlphaPartOnMsg(self, msg: str, is_start=True):
        if not msg:
            return ""

        non_alnum_part = ""
        if is_start:
            non_alpha = self.start_pattern.search(self.msg)
        else:
            non_alpha = self.end_pattern.search(self.msg)

        if non_alpha:
            non_alnum_part = non_alpha.group(0)
        return non_alnum_part

    def getNoneAlphaPart(self, is_start=True):
        non_alnum_part = self.getNoneAlphaPartOnMsg(self.msg, is_start=is_start)
        return non_alnum_part

    def getTextWithin(self):
        ref_list = PSER(self.msg)
        ref_list.parseMessage(is_ref_only=True, pattern_list=df.pattern_list_with_reserved)
        has_ref = len(ref_list) > 0
        if not has_ref:
            left = self.getNoneAlphaPart(is_start=True)
            right = self.getNoneAlphaPart(is_start=False)
            len_ref = len(left)
            len_right = len(right)
            has_right = (len_right > 0)
            if has_right:
                mid = self.msg[len_ref:-len_right]
            else:
                mid = self.msg[len_ref:]
        else:
            obs = ref_list.local_obs
            left_part = obs.getLeft()
            right_part = obs.getRight()
            left = self.getNoneAlphaPartOnMsg(left_part, is_start=True)
            right = self.getNoneAlphaPartOnMsg(right_part, is_start=False)
            len_ref = len(left)
            len_right = len(right)
            has_right = (len_right > 0)
            if has_right:
                mid = self.msg[len_ref:-len_right]
            else:
                mid = self.msg[len_ref:]
        return left, mid, right

    @classmethod
    def getTextMargin(self, txt: str):
        gt = GetTextWithin.reproduce(txt)
        left, mid, right = gt.getTextWithin()
        return left, mid, right