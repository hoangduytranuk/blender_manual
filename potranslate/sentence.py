from collections import OrderedDict
from common import Common as cm
from key import Key

class SentStructRecord():
    def __init__(self, struct_dict, dict_pat, dict_index, key, k_loc,  k_left, k_mid, k_right, tran, t_loc, t_left, t_mid, t_right, km_translated):
        self.struct_dict = struct_dict      # struct_dict: the reference to the dictionary where structure pattern is found
        self.dict_pat = dict_pat            # dict_pat: the structure pattern in the dictionary which key (msg) matched, hold here for reference
        self.dict_pat_index = dict_index    # index in the struct_dict, where the dict_pat is found

        self.key = key              # msg: the message contains the structured pattern, and needed to be translated
        self.k_loc = k_loc          # key: location of $$$
        self.kl_txt = k_left        # key: part before $$$
        self.km_txt = k_mid         # key: part where $$$ was, needed to be translated
        self.kr_txt = k_right       # key: part after $$$

        self.tran = tran            # tran: the message contains the structured pattern, with translated left/right
        self.t_loc = t_loc          # tran: location of $$$
        self.tl_txt = t_left        # tran: part before $$$
        self.tm_txt = t_mid         # tran: part where the place-holder ' $$$ ' was
        self.tr_txt = t_right       # tran: part after $$$
        self.km_translated = km_translated      # flag to indicate km has been translated

    def __repr__(self):
        sl = [
            ("struct_dict", self.struct_dict),
            ("dict_pat", self.dict_pat),
            ("dict_pat_index", self.dict_pat_index),
            ("key", self.key),
            ("k_loc", self.k_loc),
            ("kl_txt", self.kl_txt),
            ("km_txt", self.km_txt),
            ("kr_txt", self.kr_txt),
            ("tran", self.tran),
            ("t_loc", self.t_loc),
            ("tl_txt", self.tl_txt),
            ("tm_txt", self.tm_txt),
            ("tr_txt", self.tr_txt),
            ("km_translated", self.km_translated),
        ]
        string =  '; '.join(sl)
        return string

    def get_t_txt(self, is_non_tran=False):
        t_m = (self.km_txt if is_non_tran else self.tm_txt)
        l = []
        if self.tl_txt:
            l.append(self.tl_txt)
        l.append(t_m)
        if self.tr_txt:
            l.append(self.tr_txt)

        t = ' '.join(l)
        return t

    def getNonTranslated(self):
        t = self.get_t_txt(is_non_tran=True)
        return t

    def getTranslated(self):
        t = self.get_t_txt(is_non_tran=False)
        return t

class SenStructRecord():
    def __init__(self, txt, loc, left, mid, right):
        self.txt = txt
        self.loc = loc
        self.left = left
        self.mid = mid
        self.right = right

class SenStructDict(OrderedDict):
    def __init__(self, data=None):
        self.struct_list = {}
        self.k_start_list = []
        self.k_end_list = []

    def parseStruct(self, txt):
        m = cm.SENT_STRUCT_PAT.search(txt)
        s = m.start()
        e = m.end()
        left = txt[:s]
        right = txt[e:]
        mid = txt[s:e]
        loc = (s, e)
        sent_struct = SenStructRecord(txt, loc, left, mid, right)
        return sent_struct

    def __setitem__(self, key, value):
        lkey_key = Key(key)
        super(SenStructDict, self).__setitem__(lkey_key, value)

        k_struct = self.parseStruct(key)
        v_struct = self.parseStruct(value)
        self.struct_list.update({k_struct: v_struct})