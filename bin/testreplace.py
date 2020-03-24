#!/usr/bin/python3 -d

import os
import re
import datetime
from time import gmtime, strftime
from pytz import timezone

zone=timezone('Europe/London') #example, replace this with your zone
fmt='%Y-%m-%d %H:%M%z'
local_time_now = zone.localize(datetime.datetime.now())
time_now = local_time_now.strftime(fmt)
revision_time="PO-Revision-Date: {}".format(time_now)

comment_msg = [
    ["FIRST AUTHOR.*>,", "Your Full Name <your_email_address@server>,"],
    ["Last-Translator.*>", "Last-Translator: Your Full Name <your_email_address@server"],
    ["Language-Team.*>", "Language-Team: name_of_your_team_or_town, <your_email_address@server"],
    ["PO-Revision-Date: \d{4}-\d{2}-\d{2} \d{2}:\d{2}\+\d{4}", revision_time],
    ["PO-Revision-Date.*ZONE", revision_time],
    ["\"MIME-Version", "Language: vi\\\\n\"\n\"MIME-Version"]
]
language_insert = "\"Language: vi\\n\""

def readFile(fileName):
    try:
        with open(fileName) as f:
            read_text = f.read();
            f.close()
            return read_text
    except Exception as e:
        print("Error: " + str(e))
    return None

def writeFile(fileName, text):
    try:
        with open(fileName, "w") as f:
            f.write(text)
            f.close()
    except Exception as e:
        print("Error: " + str(e))

def replaceText(text, pattern, replace, is_multi=False):
    new_text=None
    ntimes=0
    if (is_multi == True):
        #print("is_multi")
        p = re.compile(pattern, re.MULTILINE | re.DOTALL | re.VERBOSE)
    else:
        #print("is_single")
        p = re.compile(pattern)
    m = p.search(text)
    is_found = (m != None)
    if (is_found):
        #new_text = text.replace(pattern, replace)
        new_text =p.sub(pattern, replace)
        print("pattern=[{}]; replace=[{}]; m=[{}]".format(pattern, replace, str(m)))
        print("new_text=\n[{}]\n".format(new_text))
        return [new_text, 1]
    else:
        return [text, 0]


def ReplaceTextInFile(po_file):
    changed = False
    text = readFile(po_file)
    replaced_text = text
    if (len([text]) > 0):
        for(index, comment_msg_entry) in enumerate(comment_msg):
            is_multi = (index == 5)
            pattern, value = comment_msg_entry
            replaced_text,ntimes = re.replaceText(text, pattern, value, is_multi)
            print("ntimes={}".format(ntimes))
            if (ntimes > 0):
                changed = True

    if (changed):
        print(replaced_text)
        #writeFile(po_file, replaced_text)

po_file = "/home/htran/testfile.po"
ReplaceTextInFile(po_file)

