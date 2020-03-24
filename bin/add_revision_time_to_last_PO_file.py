#!/usr/bin/python3
from pathlib import Path
import glob
import os
import re

import datetime
from time import gmtime, strftime
from pytz import timezone

class ReplacingBlenderDocText:
    def __init__(self):
        self.list_of_files=[]
        self.last_files=[]
        self.current_file=None
        self.vi_po_changed=False
        
    def sorted_dir(self, folder):
        def getmtime(name):
            path = os.path.join(folder, name)
            return os.path.getmtime(path)

        return sorted(os.listdir(folder), key=getmtime, reverse=True)

    def listDir(self, input_dir, extension):
        list_dir=[]
        os.chdir(input_dir)
        for (dir, dirs, files) in os.walk(".", topdown = True, onerror = None):
            for f in files:
                if (f.endswith(extension)):
                    path=os.path.join(dir,f)
                    list_dir.append(path)
        return list_dir

    def getSortedPOFileList(self, input_dir):
        files=self.listDir(input_dir, ".po")
        sorted_files=sorted(files, key=os.path.getctime, reverse=True)
        return sorted_files

    def getLastUpdatedPOFile(self, input_dir):
        self.list_of_files = self.getSortedPOFileList(input_dir)
    #    print(sorted_files)
        length = len(self.list_of_files)
        #print("the length is " + str(length))
        #latest_file=sorted_files[length-1]
        latest_file=self.list_of_files[0]
        return latest_file
    #    print(latest_file)

    def getTimeNow(self):
        local_time=timezone('Europe/London')
        fmt='%Y-%m-%d %H:%M%z'
        loc_dt=local_time.localize(datetime.datetime.now())
        formatted_dt=loc_dt.strftime(fmt)
        return formatted_dt

    def readFile(self, fileName):
        try:
            with open(fileName) as f:
                read_text = f.read();
                f.close()
                return read_text
        except Exception as e:
            print("Error: " + str(e))
        return None

    def replaceText(self, text, from_pattern, to_pattern, is_multi=False):
        #print("in replaceText: [" + from_pattern + "] to [" + to_pattern + "]")
        if (is_multi == True):
            p = re.compile(from_pattern, re.MULTILINE | re.DOTALL | re.VERBOSE)
        else:
            p = re.compile(from_pattern)
        print(p)
        new_text=None
        ntimes=0
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

    def writeTextToExistingFile(self, fileName, text):
        #print("write this:")
        #print(text)
        #print("to file: " + fileName)
        try:
            with open(fileName, "w") as f:
                f.write(text)
                f.close()
        except Exception as e:
            print("Error: " + str(e))


    #    with open(fileName, "w") as f:
    #        f.write()
    def insertLanguageVI(self, text):
        from_pattern="\"MIME-Version"
        to_pattern="\"Language: vi\\\\n\"\n\"MIME-Version"
        replaced_text,ntimes = self.replaceText(text, from_pattern, to_pattern)
        return [replaced_text,ntimes]

    def replaceFIRST_AUTHOR(self, text):
        from_pattern="FIRST AUTHOR <EMAIL@ADDRESS>"
        to_pattern="Hoang Duy Tran <hoangduytran1960@gmail.com>"
        replaced_text,ntimes = self.replaceText(text, from_pattern, to_pattern)
        return [replaced_text,ntimes]

    def replaceLastTranslator(self, text):
        from_pattern="Last-Translator.*>"
        to_pattern="Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>"
        replaced_text,ntimes = self.replaceText(text, from_pattern, to_pattern)
        #print("Replaced [{}] => []{}] #times:{}".format(text, replaced_text, ntimes))
        return [replaced_text,ntimes]

    def replaceLanguage_Team(self, text):
        from_pattern="Language-Team (.+)MIME-Version"
        to_pattern="Language-Team: London, UK <hoangduytran1960@googlemail.com>\\\\n\"\n\"Language: vi\\\\n\"\n\"MIME-Version"
        replaced_text,ntimes = self.replaceText(text, from_pattern, to_pattern)
        return [replaced_text,ntimes]

    def replacePORevisionDate(self, text):
        time_now=getTimeNow()
        print(time_now)
        date_from1="PO-Revision-Date: \d{4}-\d{2}-\d{2} \d{2}:\d{2}\+\d{4}"
        print(date_from1)
        date_from2="PO-Revision-Date.*ZONE"
        print(date_from2)
        date_to="PO-Revision-Date: " + time_now
        print(date_to)
        replaced_text,ntimes = self.replaceText(text, date_from1, date_to)
        replaced_text,ntimes = self.replaceText(text, date_from2, date_to)
        return [replaced_text,ntimes]

    def replaceGreedyMethod(self, text):
        time_now=getTimeNow()
        date_to="PO-Revision-Date: " + time_now + "\\\\n\""
        from_pattern="PO-Revision-Date(.+)MIME-Version"
        to_pattern= date_to + """
    \"Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>\\\\n\"
    \"Language-Team: London, UK <hoangduytran1960@googlemail.com>\\\\n\"
    \"Language: vi\\\\n\"
    \"MIME-Version"""
        replaced_text,ntimes = self.replaceText(text, from_pattern, to_pattern, is_multi=True)
        return [replaced_text,ntimes]

    def replaceAllModifiedPO(self, input_dir):
        self.list_of_files=self.getSortedPOFileList(input_dir)
        for(index, po_file) in enumerate(self.list_of_files):
            changed=False
            text = self.readFile(po_file)
            if (text != None):
                #replaced_text,ntimes = self.replaceFIRST_AUTHOR(text)
                #changed  = (ntimes > 0)
                replaced_text,ntimes = self.insertLanguageVI(text)
                changed  = (ntimes > 0)                
                if (changed):
                    print("Replacing file: [{}]".format(po_file))
                    #print(replaced_text)
                    self.writeTextToExistingFile(po_file, replaced_text)
            

    def replaceLastModifiedPO(self, input_dir):
        last_po_file=self.getLastUpdatedPOFile(input_dir)
        print("Last updated PO file: " + last_po_file)
        changed=False
        text = self.readFile(last_po_file)
        if (text != None):
            replaced_text,ntimes = self.replaceFIRST_AUTHOR(text)
            changed  = (ntimes > 0)
            #replaced_text,ntimes = self.insertLanguageVI(text)
            #changed  = (ntimes > 0)
            #replaced_text,ntimes = replaceLastTranslator(replaced_text)
            #changed = True if (changed == False and ntimes > 0) else False
            #replaced_text,ntimes = replaceLanguage_Team(replaced_text)
            #changed = True if (changed == False and ntimes > 0) else False
            #replaced_text,ntimes = replacePORevisionDate(replaced_text)
            #changed = True if (changed == False and ntimes > 0) else False
            #replaced_text,ntimes = insertLanguageVI(replaced_text)
            #changed = True if (changed == False and ntimes > 0) else False
            #replaced_text,ntimes = replaceGreedyMethod(replaced_text)
            #changed = True if (changed == False and ntimes > 0) else False


        #print("ABOUT to write replaced text to file")
        if (replaced_text != None):
            #print("writing replaced text to file")
            #print(replaced_text)
            #NEED to write a backup (and remove backup afterward) before allowing this to be executed
            self.writeTextToExistingFile(last_po_file, replaced_text)
            print("wrote changes to [" + last_po_file + "]")



doc_dir=os.path.join(os.environ.get("BLENDER_MAN"), "locales/vi/LC_MESSAGES")
blender_home=os.environ.get("BLENDER_GUI")
vi_po_dir=os.path.join(blender_home, "trunk/po")
vi_po_changed=os.environ.get("VI_PO_CHANGED")
x = ReplacingBlenderDocText()
x.replaceAllModifiedPO(doc_dir)
#msg="\nRemember to set environment variable\n\nexport VI_PO_CHANGED=1\n\nif you want to update vi.po's PO-Revision-Date"
#print(msg)
#if (self.vi_po_changed != None and self.vi_po_changed=="1"):
#    x.replaceLastModifiedPO(vi_po_dir)

