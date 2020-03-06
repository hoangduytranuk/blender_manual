#!/bin/python3
from pathlib import Path
import glob
import os
import re

import datetime
from time import gmtime, strftime
from pytz import timezone

doc_dir=os.environ.get("DOC_DIR")

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

def getLastUpdatedPOFile():
    files=listDir(doc_dir, ".po")
    sorted_files=sorted(files, key=os.path.getctime, reverse=True)
#    print(sorted_files)
    #length = len(sorted_files)
    #print("the length is " + str(length))
    #latest_file=sorted_files[length-1]
    latest_file=sorted_files[0]
    return latest_file
#    print(latest_file)

def getTimeNow():
    local_time=timezone('Europe/London')
    fmt='%Y-%m-%d %H:%M%z'
    loc_dt=local_time.localize(datetime.datetime.now())
    formatted_dt=loc_dt.strftime(fmt)
    return formatted_dt

def readFile(fileName):
    try:
        with open(fileName) as f:
            read_text = f.read();
            f.close()
            return read_text
    except Exception as e:
        print("Error: " + str(e))
    return None

def replaceText(text, from_pattern, to_pattern):
    p = re.compile(from_pattern)
    #print(p)
    new_text=None
    ntimes=0
    m = p.search(text)
    print(m)
    if (m != None):
        print("Replacing: [" + from_pattern + "] to [" + to_pattern + "]")
        new_text,ntimes = p.subn(to_pattern, text)
        print(new_text)
        print(ntimes)
        return [new_text, ntimes]
    else:
        return [text, 0]

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


#    with open(fileName, "w") as f:
#        f.write()
def insertLanguageVI(text):
    from_pattern="\"MIME-Version"
    to_pattern="\"Language: vi\\\\n\"\n\"MIME-Version"
    replaced_text,ntimes = replaceText(text, from_pattern, to_pattern)
    return [replaced_text,ntimes]

def replaceFIRST_AUTHOR(text):
    from_pattern="FIRST AUTHOR.*>\, \d{4}"
    to_pattern="Hoang Duy Tran <hoangduytran1960@gmail.com>, 2018"
    replaced_text,ntimes = replaceText(text, from_pattern, to_pattern)
    return [replaced_text,ntimes]

def replaceFULL_NAME(text):
    from_pattern="Last-Translator.*>"
    to_pattern="Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>"
    replaced_text,ntimes = replaceText(text, from_pattern, to_pattern)
    return [replaced_text,ntimes]

def replaceLanguage_Team(text):
    from_pattern="Language-Team.*>"
    to_pattern="Language-Team: London, UK <hoangduytran1960@googlemail.com>"
    replaced_text,ntimes = replaceText(text, from_pattern, to_pattern)
    return [replaced_text,ntimes]

def replacePORevisionDate(text):
    time_now=getTimeNow()
    print(time_now)
    date_from1="PO-Revision-Date: \d{4}-\d{2}-\d{2} \d{2}:\d{2}\+\d{4}"
    print(date_from1)
    date_from2="PO-Revision-Date.*ZONE"
    print(date_from2)
    date_to="PO-Revision-Date: " + time_now
    print(date_to)
    replaced_text,ntimes = replaceText(text, date_from1, date_to)
    replaced_text,ntimes = replaceText(text, date_from2, date_to)
    return [replaced_text,ntimes]

def replaceLastModifiedPO():
    last_po_file=getLastUpdatedPOFile()
    print(last_po_file)
    changed=False
    text = readFile(last_po_file)
    if (text != None):
        replaced_text,ntimes = replaceFIRST_AUTHOR(text)
        changed  = (ntimes > 0)
        replaced_text,ntimes = replaceFULL_NAME(replaced_text)
        changed = True if (changed == False and ntimes > 0) else False
        replaced_text,ntimes = replaceLanguage_Team(replaced_text)
        changed = True if (changed == False and ntimes > 0) else False
        replaced_text,ntimes = replacePORevisionDate(replaced_text)
        changed = True if (changed == False and ntimes > 0) else False
        replaced_text,ntimes = insertLanguageVI(replaced_text)
        changed = True if (changed == False and ntimes > 0) else False


    #print("ABOUT to write replaced text to file")
    if (changed == True):
        #print("writing replaced text to file")
        print(replaced_text)
        #NEED to write a backup (and remove backup afterward) before allowing this to be executed
        #writeTextToExistingFile(last_po_file, replaced_text)
        print("wrote changes to [" + last_po_file + "]")



replaceLastModifiedPO()

#files.sorted(key=os.path.getmtime)
#print(files)

#list_of_files=Path(doc_dir).glob('**/*.po')
#my_list=[]
#for one_file in files:
#    my_list.append(one_file)
#print(my_list)

#sorted_list=sorted(list_of_files, key=os.path.getctime, reverse=True)
#print(sorted_list)

#latest_file=$(find . -type f -name "*.po" -printf '%T@ %P\n' | sort -n | awk '{print $2}' | tail -1)
#DATE_FROM="\"PO-Revision-Date.*$"
#DATE_NOW=$(timenow.py)
#DATE_NOW=$(echo $DATE_NOW | sed "s/\+/\\+/g")
#DATE_TO="\"PO-Revision-Date: $DATE_NOW\\n\""
#function replaceTime(){
    #input_file=$1
    #command="sed -e \"s/$DATE_FROM/$DATE_TO/g\" $input_file"
    #echo $command
    #$command
#}
##stat --printf="%y %n\n" $(ls -tr $(find * -type f))
##find PATH -type f -printf "%T@ %p\n"| sort -nr
##OFS="$IFS";IFS=$'\n';stat --printf="%y %n\n" $(ls -tr $(find . -type f));IFS="$OFS"; //filenames with spaces
##find . -type f -name "*.po" -exec stat --format '%Y :%y %n' "{}" \; | sort -nr | cut -d: -f2- | head

#replaceTime $latest_file
