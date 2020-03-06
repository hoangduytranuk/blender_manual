#!/usr/bin/env python3
import re

QS= re.compile(r"(?P<quote>['\"])(?P<string>.*?)(?<!\\)(?P=quote)")
QUOTED_CHAR_RE = re.compile(r"(?P<quote_char>['\"])")

DQ=re.compile(r"(?P<double_quote>[\"])(?P<string>.*?)(?<!\\)(?P=double_quote)")
SQ=re.compile(r"(?P<single_quote>['])(?P<string>.*?)(?<!\\)(?P=single_quote)")

DC=re.compile(r"(?P<dquote_char>[\"])")
SC=re.compile(r"(?P<squote_char>['])")

#QSS = re.compile(r"(\"([^\"]|\"\")*\")\"


def checkIfWellQuoted(text_line) -> dict:
    dictionary=[]
    counter=[0,0] #single quote index 0, double quote index = 1
    ic_state=[False, False]
    ci = -1
    for index, c in enumerate(text_line):
        is_squote = SC.match(c)
        is_dquote = DC.match(c)
        if (is_squote or is_dquote):
            ci = (0) if (is_squote) else (1)
            ic_state[ci] = not ic_state[ci]
            counter[ci] = (counter[ci] + 1) if (ic_state[ci]) else (counter[ci] - 1)
            key="{}{}".format(counter[0], counter[1])
            if (key == "00"):
                dictionary.clear()
            else:
                dictionary.append( {key:index} )
            print("Quoted:{}".format(counter))

    result = int(counter[0]) * 10 + int(counter[1])
    return [result == 0, dictionary]

class QUOTE_HEAD(Enum):
    FRONT=1
    BACK=2


def parsingQuotedStatus(status : list):
    '''
        Decides which end of string needed to patch with quote and if patching, is it with single or double quote?
    '''
    si = 0 #single quote index
    di = 1 #double quote index
    l = length(status)
    for index, entry in enumerate(status):
        s_status = (entry[si])

#t0="\"well quoted\"some 'thing'\""
#t0="\"'w' q\"e't'\""
#t0="a'b'c\""
t0="a\"'b'c"
#t0="\"a'b'c"
is_well_formed,parse_result = checkIfWellQuoted(t0)
print("{}\n{}".format(is_well_formed, parse_result))
print("len:{}".format(len(t0)))
#print("t0[25]=[{}]".format(t0[25]))
#m=QS.findall(t0)
#print("m={}".format(m))

