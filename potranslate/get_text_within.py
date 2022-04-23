
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

    @classmethod
    def getTextWithinBlind(cls, txt: str) -> str:
        gwt = GetTextWithin.reproduce(txt)
        left = gwt.getNoneAlphaPart(is_start=True)
        right = gwt.getNoneAlphaPart(is_start=False)
        len_ref = len(left)
        len_right = len(right)
        has_right = (len_right > 0)
        if has_right:
            mid = gwt.msg[len_ref:-len_right]
        else:
            mid = gwt.msg[len_ref:]
        return (left, mid, right)

    @classmethod
    def getTextMidOnly(cls, txt: str) -> str:
        (left, mid, right) = cls.getTextWithinBlind(txt)
        return mid

    # def isConsider
    def getReducibleLen(self, txt: str):
        def isMirrorOf(c1: str, c2: str):
            s1 = ['<', '[', '{', '(']
            s2 = ['>', ']', '}', ')']
            for i in range(len(s1)):
                is_mirror = (s1[i] == c1) and (s2[i] == c2)
                if is_mirror:
                    return True
            return False

        def isSame(c1: str, c2: str):
            return (c1 == c2) or isMirrorOf(c1, c2)

        reducible_len = 0
        left_non_alpha_list = self.start_pattern.findall(txt)
        right_non_alpha_list = self.end_pattern.findall(txt)
        has_left = len(left_non_alpha_list) > 0
        has_right = len(right_non_alpha_list) > 0
        is_reducible = (has_left and has_right)
        if not is_reducible:
            return reducible_len

        right_non_alpha_list.reverse()
        max_len = min(len(left_non_alpha_list), len(right_non_alpha_list))
        for i in range(max_len):
            left_symb = left_non_alpha_list[i]
            right_symb = right_non_alpha_list[i]
            is_same = isSame(left_symb, right_symb)
            if is_same:
                reducible_len += 1
        return reducible_len

    def getTextWithin(self):
        is_debug = ('{UUID}:{path}:{simple name}' in self.msg)
        if is_debug:
            is_debug = True

        ref_list = PSER(self.msg)
        ref_list.parseMessage(is_ref_only=True, include_brackets=True)
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
            has_left = bool(left_part) and len(left_part) > 0
            has_right = bool(right_part) and len(right_part) > 0

            is_left_all_symbols = has_left and (df.ALL_WORD_SYMBOLS.search(left_part) is not None)
            is_right_all_symbols =has_right and (df.ALL_WORD_SYMBOLS.search(right_part) is not None)
            can_extract_left = (has_left and not is_left_all_symbols)
            can_extract_right = (has_right and not is_right_all_symbols)
            if can_extract_left:
                left = self.getNoneAlphaPartOnMsg(left_part, is_start=True)
            else:
                left = left_part

            if can_extract_right:
                right = self.getNoneAlphaPartOnMsg(right_part, is_start=False)
            else:
                right = right_part

            has_left = bool(left) and len(left) > 0
            has_right = bool(right) and len(right) > 0
            can_reduce_more = not (has_left or has_right)
            if can_reduce_more:
                reducible_len = self.getReducibleLen(self.msg)
                can_reduce = (reducible_len > 0)
                if can_reduce:
                    left = self.msg[reducible_len]
                    right = self.msg[-reducible_len]

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

    @classmethod
    def getTextMarginMidOnly(self, txt: str):
        gt = GetTextWithin.reproduce(txt)
        (left, mid, right) = gt.getTextWithin()
        return mid