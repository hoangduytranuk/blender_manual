#!/usr/bin/python3 -d
from argparse import ArgumentParser
from pathlib import Path
import glob
import os
import re

import datetime
from time import gmtime, strftime
from pytz import timezone
from enum import Enum



class ListPathEvent:
    """
        This is the base body of file listing event handler, based on the java's ActionEvent pattern.
        It only holds mainly the data passing in by the listPath function
            1. dirpath : current path of a file
            2. dirnames : all the directory names under the dirpath
            3. filenames : only the filename part under the dirpath
    """
    def __init__(self):
        """
        Initialise the class, setting all variables to None
        """
        self.dirpath : str = None
        self.dirnames : list = None
        self.filenames : list = None
        self.root_path : str = None

    def setVars(self, root_path, dirpath : str, dirnames : list, filenames : list):
        """
        :param dirpath: see above
        :param dirnames: see above
        :param filenames: see above
        :return: None
        """
        self.dirpath = dirpath
        self.dirnames = dirnames
        self.filenames = filenames
        self.root_path = root_path

    def run(self):
        """
        Any inherited instance must implement this routine
        to extract a desired result out of the data provided in
        provided variables
        :return: None
        """
        pass


class findParentDir(ListPathEvent):
    """
    An instance of implementation of the ListPathEvent
    Search for a directory name and return the parent directory of search_path
    Calling it by x = findParentDir(".svn")
    get result by x.result
    return the part BEFORE the ".svn", ie. <locale_dir> (ROOT_DIR/locale/fr)
    """
    def __init__(self, search_path : str):
        """
        Initialise the class
        :param search_path: The path to be searched in the dirnames provided
        """
        self.search_path : str = search_path
        self.result : str = None
        self.lock_result : bool = False

    def run(self):
        valid : bool = ((self.dirnames != None) and (self.search_path in self.dirnames))
        if (valid and (not self.lock_result)):
            self.result = self.dirpath+os.sep
            self.lock_result = True


class findFileByExtension(ListPathEvent):
    """
    An instance of implementation of the ListPathEvent
    Find all files with matching extenion input
    Calling it by x = findFileByExtension("rst")
    return the list of all files matching the provided extension
    """

    def __init__(self, search_extension : str):
        """
        Initialise the class with the search_extension
        :param search_extension:
        """
        self.search_extension : str = search_extension
        self.result : list = []

    def run(self):
        for filename in self.filenames:
            ext : str = os.path.splitext(filename)[1]
            is_valid : bool = ext.lower().endswith(self.search_extension)
            if (is_valid):
                entry : str =os.path.join(self.dirpath, filename)
                self.result.append(entry)

class findFileByExtensionRelative(ListPathEvent):
    """
    An instance of implementation of the ListPathEvent
    Find all files with matching extenion
    Calling it by x = findFileByExtension("rst")
    return the list of all files matching the provided extension, with relative paths
    """

    def __init__(self, search_extension : str):
        """
        Initialise the class, setting all variables to input parameters

        :param root_dir: The directory where
        :param search_extension:
        """
        self.search_extension : str = search_extension
        self.result : list = []

    def run(self):
        excluded_len : int = len(self.root_path)
        for filename in self.filenames:
            ext : str = os.path.splitext(filename)[1]
            valid : bool = ext.lower().endswith(self.search_extension)
            if (valid):
                entry : str =os.path.join(self.dirpath, filename)
                rel_path : str = entry[excluded_len:]
                if (rel_path.startswith(os.sep)):
                    rel_path = rel_path[1:]
                self.result.append(rel_path)

class findDirRelative(ListPathEvent):
    """
    An instance of implementation of the ListPathEvent
    Find all dỉrectories from a given root
    return the list of all directory under the root with relative paths
    """

    def __init__(self):
        """
        Initialise the class, setting all variables to input parameters
        """
        self.result : list = []

    def run(self):
        excluded_len : int = len(self.root_path)
        for dir_name in self.dirnames:
            full_path = os.path.join(self.dirpath, dir_name)
            rel_path : str = full_path[excluded_len:]
            if (rel_path.startswith(os.sep)):
                rel_path = rel_path[1:]
            self.result.append(rel_path)


class findFileByName(ListPathEvent):
    """
    An instance of implementation of the ListPathEvent
    Find all files with the same name in all subdirectories
    Calling it by x = findFileByName("index.po")
    Get result by x.result
    return the list of all matching the provided name in all subdirectories

    """

    def __init__(self, search_name : str):
        """
        Initialise the class, setting all variables to input parameters

        :param search_name: The filename to be searched
        """
        self.search_name : str = search_name
        self.result : list = []

        # is_found : bool = (filename.lower() == self.search_name.lower())
        self.p: Pattern = re.compile(self.search_name)

    def run(self):
        """
        This part could be improved using regular expression if there is a need, as:

        p : Pattern = re.compile(search_name)
        m : Match = p.match(filename)
        is_found : bool = (m != None)

        :return: None
        """
        for filename in self.filenames:
            m: Match = self.p.match(filename)
            is_found: bool = (m != None)
            if (is_found):
                entry : str = os.path.join(self.dirpath, filename)
                self.result.append(entry)


class UpdateOption(Enum):
    AUTHOR=1,
    REVDATE=2,
    TRANSLATOR=3,
    TEAM=4,
    LANGUAGE=5
    TRUE=6
    FALSE=7
    INVALID_VALUE=100

    def describe(self):
        return self.name, self.value

    def __str__(self):
        return "{0}".format(self.name)

    def toValue(up_option):
        op_list=[UpdateOption.AUTHOR, UpdateOption.REVDATE, UpdateOption.TRANSLATOR, UpdateOption.TEAM, UpdateOption.LANGUAGE]
        for(index, up_op) in enumerate(op_list):
            is_found = (up_option == up_op.name)
            if (is_found):
                return up_op.value
        return UpdateOption.INVALID_VALUE.value

    def validate(up_option):
        op_list=[str(UpdateOption.AUTHOR), str(UpdateOption.REVDATE), str(UpdateOption.TRANSLATOR), str(UpdateOption.TEAM), str(UpdateOption.LANGUAGE)]
        input_oplist = [up_option]
        common = set(op_list).intersection(set(input_oplist))
        print("common:[{0}]".format(common))
        if (len(common) == 0):
            return UpdateOption.INVALID_VALUE
        else:
            return up_option


class ReplacingBlenderDocText:
    zone=timezone('Europe/London')
    fmt='%Y-%m-%d %H:%M%z'
    local_time_now = zone.localize(datetime.datetime.now())
    time_now = local_time_now.strftime(fmt)
    revision_time="PO-Revision-Date: {}".format(time_now)

    comment_msg = [
        ["FIRST AUTHOR.*>", "Hoang Duy Tran <hoangduytran1960@gmail.com>"],
        ["Last-Translator.*>", "Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>"],
        ["Language-Team.*>", "Language-Team: London, UK <hoangduytran1960@googlemail.com>"],
        ["PO-Revision-Date: \d{4}-\d{2}-\d{2} \d{2}:\d{2}\+\d{4}", revision_time],
        ["PO-Revision-Date.*ZONE", revision_time]
    ]
    language_vi_insert = "\"Language: vi\\n\""


    def __init__(self):
        self.list_of_files=[]
        self.last_files=[]
        self.current_file=None
        self.vi_po_changed=False
        self.using_default = False
        self.doc_dir = None
        self.update_option = UpdateOption.INVALID_VALUE
        self.update_option_value = None
        self.file_count = -1

    def setVars(self, doc_dir):
        if (doc_dir == None):
            self.doc_dir = os.getcwd()
        else:
            self.doc_dir = doc_dir

    def sorted_dir(self, folder):
        def getmtime(name):
            path = os.path.join(folder, name)
            return os.path.getmtime(path)

        return sorted(os.listdir(folder), key=getmtime, reverse=True)

    def listDir(self, input_dir, callback):
        list_dir=[]
        #os.chdir(input_dir)
        for (dir, dirs, files) in os.walk(input_dir, topdown = True, onerror = None):
            if dirpath.startswith(DOT):
                continue

            valid_function : bool = ((not callback is None) and (isinstance(callback, ListPathEvent)))
            if (valid_function):
                callback.setVars(path, dirpath, dirnames, filenames)
                callback.run()


    def listDir(self):


        changed_list = os.system("git status | grep 'modified' | awk '{ print $2 }' | grep ".po"")

function findChangedFiles()
{
    #latest_file=$(find . -type f -name "*.po" -newermt $(date +%F) -ls | sort | tail -n 1 | awk '{ print $11 }')
    if [ -d ".git" ]; then
        changed_list=$(git status | grep 'modified' | awk '{ print $2 }' | grep ".po")
    elif [ -d ".svn" ]; then
        changed_list=$(svn status | grep 'M' | awk '{ print $2 }' | grep ".po")
    else
        changed_list=$(find . -type f -name "*.po" -exec ls -al --time-style=+%D\ %H:%M:%S {} \; | grep `/usr/bin/date +%D` | awk '{ print $6,$7,$8 }' | sort | awk '{ print $3 }')
    fi
    #latest_file=$(find . -type f -name "*.po" -exec ls -al --time-style=+%D\ %H:%M:%S {} \; | grep `/usr/bin/date +%D` | awk '{ print $6,$7,$8 }' | sort | tail -1 | awk '{ print $3 }')
}


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
        #print("Matcher: " + str(m))
        if (m != None):
            new_text,ntimes = p.subn(to_pattern, text)
            #print(new_text)
            print("Replaced: [{}] to [{}], #times: {}".format(from_pattern, to_pattern, ntimes))
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
        from_pattern="Language-Team.*>"
        to_pattern="Language-Team: London, UK <hoangduytran1960@googlemail.com>"
        replaced_text,ntimes = self.replaceText(text, from_pattern, to_pattern)
        return [replaced_text,ntimes]

    def replacePORevisionDate(self, text):
        date_from1=self.comment_msg[3][0]
        date_from2=self.comment_msg[4][0]
        date_to=self.comment_msg[4][1]
        #print("date_from1:{}, date_from2:{}, date_to:{}".format(date_from1, date_from2, date_to))
        replaced_text,ntimes = self.replaceText(text, date_from1, date_to)
        replaced_text,ntimes = self.replaceText(text, date_from2, date_to)
        return [replaced_text,ntimes]

    #def replaceGreedyMethod(self, text):
        #date_to="PO-Revision-Date: " + time_now + "\\\\n\""
        #from_pattern="PO-Revision-Date(.+)MIME-Version"
        #to_pattern= date_to + """
    #\"Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>\\\\n\"
    #\"Language-Team: London, UK <hoangduytran1960@googlemail.com>\\\\n\"
    #\"Language: vi\\\\n\"
    #\"MIME-Version"""
        #replaced_text,ntimes = self.replaceText(text, from_pattern, to_pattern, is_multi=True)
        #return [replaced_text,ntimes]

    def replaceAllModifiedPO(self, input_dir):
        self.list_of_files=self.getSortedPOFileList(input_dir)
        for(index, po_file) in enumerate(self.list_of_files):
            changed=False
            text = self.readFile(po_file)
            if (text != None):
                replaced_text = text

                replaced_text,ntimes = self.replaceFIRST_AUTHOR(text)
                changed  = changed | (ntimes > 0)

                replaced_text,ntimes = self.insertLanguageVI(replaced_text)
                changed  = changed | (ntimes > 0)

                replaced_text,ntimes = self.replaceLastTranslator(replaced_text)
                changed  = changed | (ntimes > 0)

                replaced_text,ntimes = self.replaceLanguage_Team(replaced_text)
                changed  = changed | (ntimes > 0)

                replaced_text,ntimes = self.replacePORevisionDate(replaced_text)
                changed  = changed | (ntimes > 0)

            #print("ABOUT to write replaced text to file")
            if (changed != None):
                #print("writing replaced text to file")
                #print(replaced_text)
                #NEED to write a backup (and remove backup afterward) before allowing this to be executed
                #self.writeTextToExistingFile(last_po_file, replaced_text)
                print("wrote changes to [" + po_file + "]")

    def replaceLastModifiedPO(self, input_dir):
        last_po_file=self.getLastUpdatedPOFile(input_dir)
        #print("Last updated PO file: " + last_po_file)
        changed=False
        text = self.readFile(last_po_file)
        if (text != None):
            replaced_text = text

            replaced_text,ntimes = self.replaceFIRST_AUTHOR(text)
            changed  = changed | (ntimes > 0)

            replaced_text,ntimes = self.insertLanguageVI(replaced_text)
            changed  = changed | (ntimes > 0)

            replaced_text,ntimes = self.replaceLastTranslator(replaced_text)
            changed  = changed | (ntimes > 0)

            replaced_text,ntimes = self.replaceLanguage_Team(replaced_text)
            changed  = changed | (ntimes > 0)

            replaced_text,ntimes = self.replacePORevisionDate(replaced_text)
            changed  = changed | (ntimes > 0)

        #print("ABOUT to write replaced text to file")
        if (changed != None):
            #print("writing replaced text to file")
            #print(replaced_text)
            #NEED to write a backup (and remove backup afterward) before allowing this to be executed
            #self.writeTextToExistingFile(last_po_file, replaced_text)
            print("wrote changes to [" + last_po_file + "]")


    def findLatestChangedPOFile(self, input_dir, count):
        self.list_of_files=self.getSortedPOFileList(input_dir)
        for(index, po_file) in enumerate(self.list_of_files):
            is_finish = (index >= int(count))
            if (is_finish):
                return
            else:
                #mod_time_str=strftime("%t%t %a, %Y-%m-%d %H:%M:%S", gmtime(os.path.getmtime(po_file)))
                print("{} {}".format(po_file, mod_time_str))

    def setDefaultValues(self):
        self.using_default = True
        self.doc_dir = os.getcwd()
        self.update_option = UpdateOption.REVDATE
        self.update_option_value = self.revision_time
        self.file_count = -1

    def settingArgumentValues(self, doc_dir, update_option, option_value, file_count, is_default):
        using_default = (is_default == "TRUE")
        if (using_default):
            self.setDefaultValues()
        else:
            self.doc_dir = (os.getcwd() if (doc_dir == None ) else doc_dir)
            self.update_option = UpdateOption.validate(update_option)
            print("Value of self.update_option: {} is {}".format(self.update_option, UpdateOption.toValue(update_option)) )
            self.option_value = ("" if (option_value == None ) else option_value)
            if (not file_count is None):
                self.file_count = int(file_count)
            print("doc_dir:[{}], update_option:[{}], option_value:[{}], file_count:[{}]".format(self.doc_dir, self.update_option, self.option_value, self.file_count))


    def run(self):
        self.replaceAllModifiedPO(self.doc_dir)


parser = ArgumentParser()
parser.add_argument("-d", "--dir", dest="doc_dir", help="Directory to search for PO files")
args = parser.parse_args()

print("args: {}".format(args))

x = ReplacingBlenderDocText()
x.setVars(args.doc_dir)
x.run()
