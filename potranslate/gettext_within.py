from matcher import MatcherRecord
from definition import Definitions as df
from observer import LocationObserver
from collections import deque, OrderedDict
from definition import RefType
from enum import Enum
import re

class SymbParseState(Enum):
    UNKNOWN = 0
    IGNORE = 1
    CONSUME = 2
    REMOVE = 3

class SymbolState:
    def __init__(self, symb:str, loc:tuple, state:SymbParseState):
        self.symb = symb
        self.loc = loc
        self.state = state

class SymbolStateList(list):
    def __init__(self, msg:str):
        self.msg = msg
        self.left = None
        self.right = None
        self.mid = None

    @classmethod
    def reproduce(cls, msg):
        return cls(msg)

    def getNoneAlphaPart(self, is_start=True):
        if not self.msg:
            return ""

        non_alnum_part = ""
        if is_start:
            non_alpha = df.START_WORD_SYMBOLS.search(self.msg)
        else:
            non_alpha = df.END_WORD_SYMBOLS.search(self.msg)

        if non_alpha:
            non_alnum_part = non_alpha.group(0)
        return non_alnum_part

    def makeSymbolStateRecords(self, from_loc: int, to_loc:int):
        def makeRecord(c: str, s: int, e: int):
            loc = (s, e)
            record = (loc, SymbolState(c, loc, SymbParseState.UNKNOWN))
            self.append(record)

        try:
            for i in range(from_loc, to_loc-1):
                c = self.msg[i]
                is_symbol = (c in df.varifying_brk_pattern_txt)
                if not is_symbol:
                    continue

                s = i
                e = min(to_loc-1, i+1)
                makeRecord(c, s, e)
        except Exception as e:
            df.LOG(f'{e}: txt:{self.msg}; loc:{from_loc}, {to_loc}')

    def maskOffMatchingSymbol(self, from_symb_record, other):
        state_queue = deque()
        try:
            other.sort()
            # for loc, symb_record in other:
            #
            from_loc: tuple = None
            from_symb: SymbolState = None
            to_symb: SymbolState = None
            # for from_loc, from_symb in self:

        except Exception as e:
            df.LOG(f'{e}: other:{other}')


class StateMachine:

    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []

    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = name.upper()

    def run(self, cargo):
        try:
            handler = self.handlers[self.startState]
        except:
            raise RuntimeError("must call .set_start() before .run()")
        if not self.endStates:
            raise RuntimeError("at least one state must be an end_state")

        while True:
            (newState, cargo) = handler(cargo)
            if newState.upper() in self.endStates:
                print("reached ", newState)
                break
            else:
                handler = self.handlers[newState.upper()]


class TestStateMachine:
    def __init__(self):
        self.positive_adjectives = ["great", "super", "fun", "entertaining", "easy"]
        self.negative_adjectives = ["boring", "difficult", "ugly", "bad"]

    def start_transitions(self, txt):
        splitted_txt = txt.split(None, 1)
        word, txt = splitted_txt if len(splitted_txt) > 1 else (txt, "")
        if word == "Python":
            newState = "Python_state"
        else:
            newState = "error_state"
        return (newState, txt)

    def python_state_transitions(self, txt):
        splitted_txt = txt.split(None, 1)
        word, txt = splitted_txt if len(splitted_txt) > 1 else (txt, "")
        if word == "is":
            newState = "is_state"
        else:
            newState = "error_state"
        return (newState, txt)

    def is_state_transitions(self, txt):
        splitted_txt = txt.split(None, 1)
        word, txt = splitted_txt if len(splitted_txt) > 1 else (txt, "")
        if word == "not":
            newState = "not_state"
        elif word in self.positive_adjectives:
            newState = "pos_state"
        elif word in self.negative_adjectives:
            newState = "neg_state"
        else:
            newState = "error_state"
        return (newState, txt)

    def not_state_transitions(self, txt):
        splitted_txt = txt.split(None, 1)
        word, txt = splitted_txt if len(splitted_txt) > 1 else (txt, "")
        if word in self.positive_adjectives:
            newState = "neg_state"
        elif word in self.negative_adjectives:
            newState = "pos_state"
        else:
            newState = "error_state"
        return (newState, txt)

    def neg_state(self, txt):
        print("Hallo")
        return ("neg_state", "")

    # m = StateMachine()
    # m.add_state("Start", start_transitions)
    # m.add_state("Python_state", python_state_transitions)
    # m.add_state("is_state", is_state_transitions)
    # m.add_state("not_state", not_state_transitions)
    # m.add_state("neg_state", None, end_state=1)
    # m.add_state("pos_state", None, end_state=1)
    # m.add_state("error_state", None, end_state=1)
    # m.set_start("Start")
    # m.run("Python is great")
    # m.run("Python is difficult")
    # m.run("Perl is ugly")

class GetTextWithin:
    # get list of brackets in the text line, with location, state = UNKOWN
    # mask off pairs that are (CONSUME)
    #   - (SLINE)(BRK) .. (BRK)(space) (exlcude space)
    #   - (space)(BRK) .. (BRK)(space) (exlcude space)
    #   - (space)(BRK) .. (BRK)(ELINE) (exlcude space)
    #
    # remove if pairs are (REMOVE)
    #   - (SLINE)(BRK) .. (BRK)(ELINE)
    #   - (SLINE|NON-ALPHA+)(BRK) .. (BRK)(ELINE)
    #   - (SLINE)(BRK) .. (BRK)(NON-ALPHA+|ELINE)
    #   - (SLINE, NON-ALPHA+)(ALPHA) (exclude the alpha)
    #   - (ALPHA)(NON-ALPHA+, ELINE) (exclude the alpha)

    def patternMatchAll(pat, text):
        return_dict = {}
        try:
            for m in pat.finditer(text):
                match_record = MatcherRecord(matcher_record=m)
                match_record.pattern = pat
                loc = match_record.getMainLoc()
                dict_entry = {loc: match_record}
                return_dict.update(dict_entry)
        except Exception as e:
            pass
            # df.LOG(e)
        return return_dict

    def getMatches(pat: re.Pattern, find_txt: str, ref: RefType):
        local_found_dict = {}
        try:
            is_bracket = (ref == RefType.ARCH_BRACKET)
            if is_bracket:
                local_found_dict = GetTextWithin.getTextWithinBrackets('<|(|{|[', '>|)|}|]', find_txt, is_include_bracket=False)
            else:
                local_found_dict = GetTextWithin.patternMatchAll(pat, find_txt)
        except Exception as e:
            df.LOG(f'{e}; pat:[{pat}]; find_txt:[{find_txt}]; ref:[{ref}]; local_found_dict:[{local_found_dict}];',
                   error=True)
            raise e
        return local_found_dict

    def findOnePattern(msg: str, pattern: re.Pattern, reftype: RefType):
        result_dict={}
        found_dict = OrderedDict()

        valid_msg = (msg is not None) and (len(msg) > 0)
        valid_pattern = (pattern is not None)
        valid = valid_msg and valid_pattern
        if not valid:
            return

        try:
            found_dict = GetTextWithin.getMatches(pattern, msg, reftype)
            if found_dict:
                result_dict.update(found_dict)
        except Exception as e:
            df.LOG(f'{e} msg:[{msg}]; found_dict:[{found_dict}]', error=True)
            raise e
        return result_dict

    def findPattern(pattern_list: list, txt: str):
        result_dict={}
        pattern_list.reverse()
        for index, item in enumerate(pattern_list):
            p, ref_type = item
            found_dict = GetTextWithin.findOnePattern(txt, p, ref_type)
            result_dict.update(found_dict)

        GetTextWithin.cleanupBrackets(result_dict, txt)
        return result_dict

    def cleanupBrackets(input_dict, msg):
        mm: MatcherRecord = None
        remove_list = []
        obs = LocationObserver(msg)

        # marking NON-arched bracket places
        for loc, mm in input_dict.items():
            ref_type = mm.type
            is_bracket = (ref_type == RefType.ARCH_BRACKET)
            if is_bracket:
                continue

            obs.markLocAsUsed(loc)

        # ignore if Non-bracket,
        for loc, mm in input_dict.items():
            ref_type = mm.type
            is_bracket = (ref_type == RefType.ARCH_BRACKET)
            if not is_bracket:
                continue

            txt = mm.txt
            is_fully_used = obs.isLocFullyUsed(loc)
            if is_fully_used:
                df.LOG(f'REMOVING: [{mm}]')
                remove_list.append(loc)

        for loc in remove_list:
            del input_dict[loc]
        return input_dict

    def removeStartEndBrackets(input_txt, start_bracket=None, end_bracket=None):
        try:
            str_len = len(input_txt)
            start_loc = 0
            end_loc = str_len

            s_brk = (start_bracket if start_bracket else '(')
            e_brk = (end_bracket if end_bracket else ')')

            bracket_pattern_txt = r'([\%s\%s])' % (s_brk, e_brk)
            bracket_pattern = re.compile(bracket_pattern_txt)
            found_dict = GetTextWithin.patternMatchAll(bracket_pattern, input_txt)
            found_list = list(found_dict.items())
            if not found_list:
                orig_loc = (start_loc, end_loc)
                orig_entry = (orig_loc, input_txt)
                return orig_entry

            q = deque()
            for loc, mm in found_dict.items():
                brk = mm.txt
                is_open = (brk == s_brk)
                is_close = (brk == e_brk)
                current_entry = (loc, brk)
                if is_open:
                    q.append(current_entry)
                if is_close:
                    if not q:
                        continue

                    q_entry = q.pop()
                    (cs, ce), cbrk = current_entry
                    (qs, qe), qbrk = q_entry
                    is_start_string_bracket = (qs == 0)
                    is_end_string_bracket = (ce == str_len)
                    is_remove_start_and_end = (is_start_string_bracket and is_end_string_bracket)
                    if is_remove_start_and_end:
                        start_loc = qs + len(start_bracket)
                        end_loc = ce - len(end_bracket)
                        break
            new_txt = input_txt[start_loc: end_loc]
            new_loc = (start_loc, end_loc)
            return (new_loc, new_txt)

        except Exception as e:
            df.LOG(f'{e} [{input_txt}]', error=True)
            raise e


    def getTextWithinBrackets(
            start_bracket: str,
            end_bracket: str,
            input_txt:str,
            is_include_bracket:bool =False,
            replace_internal_start_bracket:str = None,
            replace_internal_end_bracket:str = None
    ) -> list:

        def pop_q(pop_s, pop_e) -> bool:
            last_s = q.pop()
            ss = last_s
            ee = pop_e

            # for 'function()', do not store as a bracketed text
            txt_line = input_txt[ss:ee]
            if not txt_line:
                return False

            is_ignore = (len(txt_line) < 3)
            if not is_ignore:
                loc = (ss, ee)
                entry = (loc, txt_line)
                sentence_list.append(entry)
            return True

        def getBracketList(start_brk, end_brk):
            # split at the boundary of start and end brackets
            try:
                # 1. find positions of start bracket
                if is_same_brakets:
                    p_txt = r'\%s' % start_brk
                else:
                    p_txt = r'[\%s\%s]' % (start_brk, end_brk)

                p = re.compile(p_txt)
                brk_list = GetTextWithin.patternMatchAll(p, input_txt)
                return brk_list, p
            except Exception as e:
                df.LOG(f'{e} [{input_txt}]', error=True)
                raise e
            return brk_list

        def getSentenceList(start_brk, end_brk):
            bracket_list, pattern = getBracketList(start_brk, end_brk)
            if not bracket_list:
                return sentence_list, pattern

            # detecting where start/end and take the locations
            mm: MatcherRecord = None
            if is_same_brakets:
                for loc, mm in bracket_list.items():
                    s, e = loc
                    bracket = mm.txt
                    is_bracket = (bracket == start_brk)
                    if is_bracket:
                        if not q:
                            q.append(s)
                        else:
                            pop_q(s, e)
            else:
                for loc, mm in bracket_list.items():
                    s, e = loc
                    bracket = mm.txt
                    is_open = (bracket == start_brk)
                    is_close = (bracket == end_brk)
                    if is_open:
                        q.append(s)
                    if is_close:
                        if not q:
                            continue
                        else:
                            pop_q(s, e)
            return sentence_list, pattern

        def sortSentencesFunction(item):
            (loc, txt) = item
            sort_key = (len(txt), loc)
            return sort_key

        def findUsingBracketSet(start_brk, end_brk):
            output_dict = OrderedDict()
            txt_len = len(input_txt)

            if is_same_brakets:
                df.LOG(f'getTextWithinBracket() - WARNING: start_bracket and end_braket is THE SAME {start_bracket}. '
                   f'ERRORS might occurs!')

            sentence_list, pattern = getSentenceList(start_brk, end_brk)
            if not sentence_list:
                return output_dict

            loc_list = []
            obs = LocationObserver(input_txt)
            sentence_list.sort(key=sortSentencesFunction, reverse=True)
            for loc, txt in sentence_list:
                is_finished = obs.isCompletelyUsed()
                if is_finished:
                    break

                is_used = obs.isLocUsed(loc)
                if is_used:
                    continue

                if not is_include_bracket:
                    (sub_loc, actual_txt) = GetTextWithin.removeStartEndBrackets(txt, start_bracket=start_brk,
                                                                          end_bracket=end_brk)
                    (cs, ce) = loc
                    (ss, se) = sub_loc
                    actual_loc = (cs + ss, cs + se)
                else:
                    actual_loc = loc
                    actual_txt = txt

                obs.markLocAsUsed(loc)
                (ss, ee) = actual_loc
                mm = MatcherRecord(s=ss, e=ee, txt=actual_txt)
                mm.pattern = pattern
                mm.type = RefType.ARCH_BRACKET
                dict_entry = {actual_loc: mm}
                output_dict.update(dict_entry)

            return output_dict

        result={}
        is_same_brakets = False
        q = None
        sentence_list = None
        start_bracket_list = start_bracket.split('|')
        end_bracket_list = end_bracket.split('|')
        for index in range(0, len(start_bracket_list)):
            q = deque()
            sentence_list = []

            start_brk = start_bracket_list[index]
            end_brk = end_bracket_list[index]
            is_same_brakets = (start_brk == end_brk)
            result_set = findUsingBracketSet(start_brk, end_brk)
            if result_set:
                result.update(result_set)

        return result

    def getNoneAlphaPart(msg, is_start=True):
        if not msg:
            return ""

        non_alnum_part = ""
        if is_start:
            non_alpha = df.START_WORD_SYMBOLS.search(msg)
        else:
            non_alpha = df.END_WORD_SYMBOLS.search(msg)

        if non_alpha:
            non_alnum_part = non_alpha.group(0)
        return non_alnum_part

    def getTextWithinWithDiffLoc(msg, to_matcher_record=False):
        # should really taking bracket pairs into account () '' ** "" [] <> etc.. before capture
        left_part = GetTextWithin.getNoneAlphaPart(msg, is_start=True)
        right_part = GetTextWithin.getNoneAlphaPart(msg, is_start=False)

        ss = len(left_part)
        ee = (-len(right_part) if right_part else len(msg))
        mid_part = msg[ss:ee]
        length_ee = len(right_part)
        diff_loc = (ss, length_ee)

        main_record: MatcherRecord = None
        if to_matcher_record:
            ls = 0
            le = ss
            ms = le
            me = ms + len(mid_part)
            rs = me
            re = rs + len(right_part)

            main_record = MatcherRecord(s=0, e=len(msg), txt=msg)
            if left_part:
                main_record.addSubMatch(ls, le, left_part)
                test_txt = left_part[ls: le]
            else:
                main_record.addSubMatch(-1, -1, None)
            if mid_part:
                main_record.addSubMatch(ms, me, mid_part)
                test_txt = left_part[ms: me]
            else:
                main_record.addSubMatch(ls, re, msg)
            if right_part:
                main_record.addSubMatch(rs, re, right_part)
                test_txt = left_part[rs: re]
            else:
                main_record.addSubMatch(-1, -1, None)

        return diff_loc, left_part, mid_part, right_part, main_record

    def getTextWithin(msg):
        diff_loc, left_part, mid_part, right_part, main_record = GetTextWithin.getTextWithinWithDiffLoc(msg)
        return left_part, mid_part, right_part

        # # states,
        # # bbegining
        # def maskingOffBrkPairs(part, is_backward=True):
        #     if is_backward:
        #         from_loc = len(part)
        #         to_loc = len(msg)-1
        #         remain_part = msg[from_loc:]
        #     else:
        #         from_loc = len(msg) - len(part)
        #         to_loc = -1
        #         remain_part = msg[:from_loc]
        #
        #
        # brk = df.varifying_brk_pattern.search(msg)
        # has_brk = (brk is not None)
        # if has_brk:
        #     msg_len = len(msg)
        #     left_part = GetTextWithin.getNoneAlphaPart(msg, is_start=True)
        #     left_len = len(left_part)
        #
        #     right_part = GetTextWithin.getNoneAlphaPart(msg, is_start=False)
        #     right_len = len(right_part)
        #
        #     has_left = (left_len > 0)
        #     has_right = (right_len > 0)
        #
        #
        #     found_dict = GetTextWithin.findPattern(df.pattern_list, msg)
        #     found_list = list(found_dict)
        #     found_list.sort()
        #     list_len = len(found_list)
        #     has_only_one = (list_len == 1)
        #     if has_only_one:
        #         pass
        #     else:
        #         left_side = found_list[0]
        #         right_side = found_list[list_len-1]
        #
        #     # obs = LocationObserver(msg)
        #     # start = 0
        #     # end = len(msg)-1
        #     # for loc, mm in found_list.items():
        #     #     obs.markLocAsUsed(loc)
        #     #
        #     # process_txt = obs.blank
        # else:
        #     process_txt = msg
        #
        # diff_loc, left, mid, right, _ = GetTextWithin.getTextWithinWithDiffLoc(process_txt)
        # return left, mid, right

