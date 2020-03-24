#!/bin/python3
from pathlib import Path
import glob
import os
import re

import datetime
from time import gmtime, strftime
from pytz import timezone

class BaseFileIO:
    blender_home=os.environ.get("BLENDER_HOME")
    vi_po_dir=os.path.join(blender_home, "trunk/po")
    vi_po_changed=os.environ.get("VI_PO_CHANGED")
    doc_dir=os.environ.get("DOC_DIR")
    empty_string="\"\""

    def writeListToExistingFile(fileName, text_list):
    try:
        with open(fileName, "w") as f:
            for (index, text) in enumerate(text_list):
                f.write(text+"\n")
            f.close()
    except Exception as e:
        print("Error: " + str(e))

    def writeTextToExistingFile(fileName, text):
        #print("write this:")
        #print(text)
        #print("to file: " + fileName)
        try:
            with open(fileName, "w") as f:
                f.write(text)
                f.close()
        except Exception as e:
            print("Error: " + str(e))

    def readFile(fileName):
        try:
            with open(fileName) as f:
                read_text = f.read();
                f.close()
                return read_text
        except Exception as e:
            print("Error: " + str(e))
        return None

    def getTimeNow():
        local_time=timezone('Europe/London')
        fmt='%Y-%m-%d %H:%M%z'
        loc_dt=local_time.localize(datetime.datetime.now())
        formatted_dt=loc_dt.strftime(fmt)
        return formatted_dt

    def sorted_dir(folder):
        def getmtime(name):
            path = os.path.join(folder, name)
            return os.path.getmtime(path)

        return sorted(os.listdir(folder), key=getmtime, reverse=True)

    def listDir(input_dir, extension):
        list_dir=[]
        os.chdir(input_dir)
        for (dir, dirs, files) in os.walk(".", topdown = True, onerror = None):
            for f in files:
                if (f.endswith(extension)):
                    path=os.path.join(dir,f)
                    list_dir.append(path)
        return list_dir

    def getSortedPOFileList(input_dir):
        files=listDir(input_dir, ".po")
        sorted_files=sorted(files, key=os.path.getctime, reverse=True)
        return sorted_files

    def splitFileIntoBlocks(read_text):
        blocks = read_text.split("\n\n")
        return blocks

    def splitBlockIntoComponents(block):
        lines = block.split("\n")
        comment=[]
        msgctxt=[]
        msgid=[]
        msgstr=[]
        current_list=[]
        for line in lines:
            if (line.startswith("#")):
                current_list=comment
            if (line.startswith("msgctxt")):
                current_list=msgctxt
            if (line.startswith("msgid")):
                current_list=msgid
            if (line.startswith("msgstr")):
                current_list=msgstr
            current_list.append(line.strip())
        return [comment, msgctxt, msgid, msgstr]

class manual(BaseFileIO):
    def replaceTranslationOfOneGroup(msgid, msgstr, search_string, replace_string):
        orig_text = None
        rep_text = None
        has_orig = (len(msgid) > 0)
        has_rep = (len(msgstr) > 0)
        is_orig_match=False
        is_rep_match=False
        if (has_orig):
            orig_text = msgid[0].strip()
            is_orig_match = textContain(orig_text, search_string)
    #        print("orig_text = " + orig_text)
            if (is_orig_match and has_rep):
                rep_text = msgstr[0].strip()
                is_rep_match = textContain(rep_text, replace_string)
    #        print("rep_text = " + rep_text)

        is_rep_differ = (is_orig_match and (is_rep_match == False))
        if (is_rep_differ):
            print("is_rep_differ = " + str(is_rep_differ))
            print("[" + msgstr[0] + "] REPLACED WITH [" + replace_string + "]")
            msgstr[0]=replace_string
            is_file_dirty=True
        else:
            if (is_orig_match):
                print("[" + orig_text + "] TRANSLATED AS [" + msgstr[0] + "]")

    def replaceTextInCommentBlock(comment, search_string, replace_string):
        for (index, s) in enumerate(comment):
            comment[index] = re.sub(search_string, replace_string, s)
    #    print("comment" + str(comment))

    def replaceTextInMsgStrBlock(msgstr, search_string, replace_string):
        for (index, s) in enumerate(msgstr):
            msgstr[index] = re.sub(search_string, replace_string, s)
    #    print("msgstr" + str(msgstr))

    def insertItemIntoList(item_list, search_string, insert_string, is_after=True):
        for (index, s) in enumerate(item_list):
            m = re.search(search_string, s)
            is_change = (not m is None)
    #        print("is_change: " + str(is_change) + " m:" + str(m))
            if (is_change):
                list_len = len(item_list)
                insert_index = ((index + 1) if (is_after) else (index - 1))
                insert_index = max(0, min(insert_index, list_len+1))
                is_append = (insert_index > list_len)
                #print("is_append: " + str(is_append) + " insert_index: " + str(insert_index) + " index: " + str(index))
                if (is_append):
                    item_list.append(insert_string)
                else:
                    item_list.insert(insert_index, insert_string)
                break
                #print("item_list" + str(item_list))


    def textContain(text, find_pattern):
        m = re.search(find_pattern, text)
        is_contain = (not m is None)
        if (is_contain):
            print("textContain - find_pattern: " + find_pattern + " m= " + str(m))
        return is_contain

    def checkOrigAndReplacement(text, orig, rep):
        has_orig = textContain(text, orig)
        has_rep = textContain(text, rep)
        need_to_change=(has_orig and not has_rep)
        no_both=(not (has_orig or has_rep))
        is_needed = (need_to_change and not no_both)
        orig_count=(1 if has_orig else 0)
        rep_count=(1 if has_rep else 0)
        return [is_needed, orig_count, rep_count]

    def isTextNeededToChange(text):
        tot_orig = 0
        tot_rep = 0

        for (index, list_elem) in enumerate(msg_list):
                orig_text, rep_text = list_elem
                is_needed, orig_count, rep_count = checkOrigAndReplacement(text, orig_text, rep_text)
                tot_orig += orig_count
                tot_rep += rep_count
                if (is_needed): return True

        print("tot_orig=" + str(tot_orig) + "; tot_rep=" + str(tot_rep))
        do_not_check_further = (tot_orig == 0) and (tot_rep == 0)
        if (do_not_check_further): return False

        print("NEED CHECKING TO SEE IF HEADER HAS BEEN FILLED OR NOT, ONLY REPLACED HEADER IF IT HASN'T BEEN FILLED")
        has_orig = textContain(text, date_from2)
        has_rep = textContain(text, date_from1)
        need_to_change = (has_orig and not has_rep)
        if (need_to_change):
            return True
        else:
            return False

    def processOneBlock(comment, msgctxt, msgid, msgstr, block_index):
        for (index, list_elem) in enumerate(msg_list):
            orig_text, rep_text = list_elem
            replaceTranslationOfOneGroup(msgid, msgstr, orig_text, rep_text)

        #print("changing COMMENT BLOCK!")
        replaceTextInCommentBlock(comment, first_author_orig, first_author_replacement)
        replaceTextInMsgStrBlock(msgstr, last_translator_orig, last_translator_replacement)
        replaceTextInMsgStrBlock(msgstr, language_team_orig, language_team_replacement)

        replaceTextInMsgStrBlock(msgstr, date_from1, date_to)
        replaceTextInMsgStrBlock(msgstr, date_from2, date_to)
        insertItemIntoList(msgstr, language_team_orig, language_vi_insert, is_after=True)

    def blockToList(list_of_blocks):
        text_list=[]
        for [comment, msgctxt, msgid, msgstr] in list_of_blocks:
            #print("comment="+ str(comment))
            #print("msgctxt="+ str(msgctxt))
            #print("msgid="+ str(msgid))
            #print("msgstr="+ str(msgstr))
            if (len(comment) > 0):
                text_list.extend(blockToText(comment))
            if (len(msgctxt) > 0):
                text_list.extend(blockToText(msgctxt))
            if (len(msgid) > 0):
                text_list.extend(blockToText(msgid))
            if (len(msgstr) > 0):
                text_list.extend(blockToText(msgstr))
            text_list.append("")
        return text_list

    def processOneFile(input_file):
        print("=====================")
        print(input_file)
        print("=====================")
        list_of_blocks=[]
        read_text = readFile(input_file)
        blocks = splitFileIntoBlocks(read_text)
        is_ignore = False
        need_to_change = isTextNeededToChange(read_text)
        if (need_to_change is False):
            print("NO need changing")
            return

        print("need changing")
        for (block_index, block) in enumerate(blocks):
            comment, msgctxt, msgid, msgstr = splitBlockIntoComponents(block)
            #print("comment="+ str(comment))
            #print("msgctxt="+ str(msgctxt))
            #print("msgid="+ str(msgid))
            #print("msgid="+ str(msgstr))
            processOneBlock(comment, msgctxt, msgid, msgstr, block_index)
            is_ignore = (len(comment)==0) and (len(msgctxt)==0) and (len(msgid)==0) and (len(msgstr)==0)
            if (is_ignore == False):
                list_element = [comment, msgctxt, msgid, msgstr]
                list_of_blocks.append(list_element)
        return list_of_blocks

    def processAllFiles(input_dir):
        sorted_files = getSortedPOFileList(input_dir)
        for one_file in sorted_files:
            is_file_dirty=False
            list_of_blocks = processOneFile(one_file)
            #text_list = blockToList(list_of_blocks)
            #print(list_of_blocks)
            #print(text_list)
            #writeListToExistingFile("/home/htran/change.txt", text_list)
            #break

    def getLastUpdatedPOFile(input_dir):
        sorted_files = getSortedPOFileList(input_dir)
    #    print(sorted_files)
        length = len(sorted_files)
        #print("the length is " + str(length))
        #latest_file=sorted_files[length-1]
        latest_file=sorted_files[0]
        return latest_file
    #    print(latest_file)

    def replaceText(text, from_pattern, to_pattern, is_multi=False):
        #print("in replaceText: [" + from_pattern + "] to [" + to_pattern + "]")
        if (is_multi == True):
            p = re.compile(from_pattern, re.MULTILINE | re.DOTALL | re.VERBOSE)
        else:
            p = re.compile(from_pattern)
        print(p)
        new_text=None
        ntimes=0
        print("text=" + str(text))
        m = p.search(text)
        print("Matcher: " + str(m))
        if (m != None):
            new_text,ntimes = p.subn(to_pattern, text)
            #print(new_text)
            print("Replaced: [" + from_pattern + "] to [" + to_pattern + "]")
            print("Number of times replaced: " + str(ntimes))
            return [new_text, ntimes]
        else:
            return [text, 0]

    po_file_block_list=None
    msg_list=[
    ["msgid \"Inputs\"", "msgstr \"Các Đầu Vào -- Inputs\""],
    ["msgid \"Outputs\"", "msgstr \"Các Đầu Ra -- Outputs\""],
    ["msgid \"Properties\"","msgstr \"Các Tính Chất -- Properties\""],
    ["msgid \"This node has no output sockets.\"", "msgstr \"Nút này không có ổ cắm đầu ra.\""],
    ["msgid \"This node has no input sockets.\"", "msgstr \"Nút này không có ổ cắm đầu vào.\""],
    ["msgid \"This add-on does not have any properties.\"", "msgstr \"Trình bổ-sung này không có tính chất nào cả.\""],
    ["msgid \"Example\"", "msgstr \"Ví Dụ -- Example\""],
    ["msgid \"Examples\"", "msgstr \"Các Ví Dụ -- Examples\""],
    ["msgid \"Axis\"", "msgstr \"Trục -- Axis\""],
    ["msgid \"Factor\"", "msgstr \"Hệ Số -- Factor\""],
    ["msgid \"Image\"", "msgstr \"Hình Ảnh -- Image\""],
    ["msgid \"Value\"", "msgstr \"Giá Trị -- Value\""],
    ["msgid \"Offset\"", "msgstr \"Dịch Chuyển -- Offset\""]
    ]

    #comment block
    first_author_orig="FIRST AUTHOR.*>"
    first_author_replacement="Hoang Duy Tran <hoangduytran1960@gmail.com>"
    last_translator_orig="Last-Translator.*>"
    last_translator_replacement="Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>"
    language_team_orig="Language-Team.*>"
    language_team_replacement="Language-Team: London, UK <hoangduytran1960@googlemail.com>"
    date_from1="PO-Revision-Date: \d{4}-\d{2}-\d{2} \d{2}:\d{2}\+\d{4}"
    date_from2="PO-Revision-Date.*ZONE"
    time_now=getTimeNow()
    date_to="PO-Revision-Date: " + time_now
    language_vi_insert="\"Language: vi\\n\""

    #global var
    is_file_dirty=False
    po_file_block_list = loadViPOFile()
    text_list = processAllFiles(doc_dir)

class vipo(BaseFileIO):
    def __init__(self):
        self.block_size=0;
        self.block_index=-1;

    def loadViPOFile():
        input_file=vi_po_dir + "vi.po"
        read_text = readFile(input_file)
        blocks = splitFileIntoBlocks(read_text)
        return blocks
