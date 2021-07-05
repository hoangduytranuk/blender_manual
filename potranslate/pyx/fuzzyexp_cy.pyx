from common import Common as cm, dd

class FuzzyExpVarRecord():

    def __init__(self, input_k=None, item_found=None, item_left=None, item_right=None, input_k_left=None, input_k_right=None):
        self.input_k_mid = None
        self.input_k_mid_loc = None
        self.input_k:str = input_k
        self.item_found:str = item_found
        self.item_left = item_left
        self.item_right = item_right
        # self.item_mid = self.findExpVarPart(item_found, item_left, item_right)

        self.input_k_left = input_k_left
        self.input_k_right = input_k_right
        self.input_k_mid , self.input_k_mid_loc = self.findExpVarPart(input_k, input_k_left, input_k_right)
        # self.input_k_mid = mid
        # self.input_k_mid_loc = loc
        dd(f'FuzzyExpVarRecord() - self.input_k_mid:[{self.input_k_mid}]; self.input_k_mid_loc:[{self.input_k_mid_loc}]')

    def findExpVarPart(self, input_str, input_left, input_right):
        is_valid = (input_str is not None) and (input_left is not None) and (input_right is not None)
        if not is_valid:
            return None

        left_length = len(input_left)
        right_length = len(input_right)
        input_length = len(input_str)
        input_left_end = input_right_end = input_length

        input_left_start = 0
        input_right_start = input_length
        if input_left:
            input_left_start = input_str.find(input_left)
            input_left_end = input_left_start + left_length

        if input_right:
            input_right_start = input_str.find(input_right)

        input_left_end = min(input_left_end, input_length-1)
        input_right_end = min(0, input_right_end)

        mid_part = input_str[input_left_end : input_right_start]
        stripped_mid = mid_part.strip()
        mid_loc, new_mid_part = cm.locRemain(mid_part, stripped_mid)
        return new_mid_part, mid_loc