#!/usr/bin/python3 -d
from argparse import ArgumentParser
from pathlib import Path
import glob
import os
import re
import copy
import pathlib

from datetime import datetime, timedelta, date

from time import gmtime, strftime
from pytz import timezone
from enum import Enum
from math import ceil, floor

#from configparser import ConfigParser

class BaseFileIO():
    empty_string="\"\""

    def writeListToExistingFile(self, file_name, text_list):
        try:
            with open(file_name, "w") as f:
                for (index, text) in enumerate(text_list):
                    f.write(text+"\n")
                f.close()
        except Exception as e:
            print("Error: " + str(e))

    def writeTextToFile(self, file_name, text):
        #print("write this:")
        #print(text)
        #print("to file: " + file_name)
        try:
            with open(file_name, "w+") as f:
                f.write(text)
                f.close()
        except Exception as e:
            print("Error: " + str(e))

    def readFile(self, file_name):
        try:
            with open(file_name) as f:
                read_text = f.read();
                f.close()
                return read_text
        except Exception as e:
            print("Error: " + str(e))
        return None

    def getTimeNow(self):
        local_time=timezone('Europe/London')
        fmt='%Y-%m-%d %H:%M%z'
        loc_dt=local_time.localize(datetime.now())
        formatted_dt=loc_dt.strftime(fmt)
        return formatted_dt

    def prior_week_end(self):
        return datetime.now() - timedelta(days=((datetime.now().isoweekday()) % 7))

    def prior_week_start(self):
        return self.prior_week_end() - timedelta(days=7)

    def getInividualTimeNow(self):
        local_time=timezone('Europe/London')
        fmt='%Y-%m-%d %H:%M%z'
        date_now_fmt='%d'
        month_now_fmt='%m'
        year_now_fmt='%Y'

        #today = date.today()
        today  = datetime.now()
        loc_dt=local_time.localize(today)
        #today = date(2019, 10, 2)
        w_day = today.isoweekday()

        if (w_day >= ceil(7.0/2.0) ):
            w_day = (7-w_day)
        else:
            w_day *= -1

        #offset = (w_day) % 7
        #print("w_day", w_day)
        #print("offset", offset)

        loc_dt = today + timedelta(days=w_day)
        #print("Sunday:", loc_dt)
        #today = datetime.now()
        #loc_dt=local_time.localize(today)
        #w_day = today.weekday()

        #report = 'Last Sunday was {:%d/%m/%Y} and last Saturday was {:%d/%m/%Y}'.format(self.prior_week_start(), self.prior_week_end())
        #print(report)

        #onDay = lambda date, day: date + datetime.timedelta(days=(day-date.weekday())%7)
        #print("onDay:",onDay(today, -1))

        #prev_sunday = today + datetime.timedelta(days=-(w_day), weeks=0)
        #next_sunday = today + datetime.timedelta(days=+(w_day), weeks=0)

        #print(today, w_day)
        #print("next_sunday:", next_sunday)
        #print("prev_sunday:", prev_sunday)
        #exit(0)

        date_now=loc_dt.strftime(date_now_fmt)
        month_now=loc_dt.strftime(month_now_fmt)
        year_now=loc_dt.strftime(year_now_fmt)
        year_now_two_digit="{}".format(year_now[2:])
        return [date_now, month_now, year_now_two_digit]

    def getInividualTimeNowFourDigits(self):
        local_time=timezone('Europe/London')
        fmt='%Y-%m-%d %H:%M%z'
        date_now_fmt='%d'
        month_now_fmt='%m'
        year_now_fmt='%Y'

        loc_dt=local_time.localize(datetime.now())
        date_now=loc_dt.strftime(date_now_fmt)
        month_now=loc_dt.strftime(month_now_fmt)
        year_now=loc_dt.strftime(year_now_fmt)
        year_now_two_digit="{}".format(year_now[2:])
        return [date_now, month_now, year_now]

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


class FillTravelForm(BaseFileIO):
    max_count = 3
    max_count_per_page = 8
    config_file = "/Users/hoangduytran/Documents/jobs/orridge/2018/expenses.ini"

    def __init__(self):
        self.from_doc = None
        self.to_doc = None


    def replaceText(self, text, from_pattern, to_pattern, is_multi=False):
        #print("in replaceText: [" + from_pattern + "] to [" + to_pattern + "]")
        if (is_multi == True):
            p = re.compile(from_pattern, re.MULTILINE | re.DOTALL | re.VERBOSE)
        else:
            p = re.compile(from_pattern)
        #print(p)
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


    def setFromDocument(self, from_doc):
        self.from_doc = from_doc

    def setToDocument(self, to_doc):
        self.to_doc = to_doc

    def setDocument(self, from_doc, to_doc):
        self.from_doc = from_doc
        self.to_doc = to_doc

    def reverseDate(self, orig_date):
        fd_list = orig_date.split("/")
        fd_str = "{}{}{}".format(fd_list[2],fd_list[1],fd_list[0])
        return fd_str


    def fillTravelForm(self):
        text0 = None
        text1 = None

        #config = ConfigParser()
        #config.read(config_file)

        from_doc_text = self.readFile(self.from_doc)

        date_now,month_now,year_now = x.getInividualTimeNow()
        claim_date_value="{}  {}   {}   {}   {}  {}".format(date_now[0], date_now[1], month_now[0], month_now[1], year_now[0], year_now[1])

        #print("from_doc_text:\n{}\n".format(from_doc_text))
        #print("claim_date_value:", claim_date_value)
        #exit(0)
        total_sundry = 0
        for (index, expense_row) in enumerate(expenses):
            is_at_end = (len(expense_row[0]) == 0)
            if (is_at_end):
                break
            else:
                max_count = index+1

        #print("max_count = {}".format(max_count))
        #return

        max_count = (self.max_count_per_page if (max_count > self.max_count_per_page) else max_count)

        text0, ntime = self.replaceText(from_doc_text, "CLAIM_DATE", claim_date_value)
        for index in range(0, max_count):
            expense_entry = expenses[index]
            job_number = expense_entry[0]
            job_date = expense_entry[1]
            from_loc = expense_entry[2]
            to_loc = expense_entry[3]
            amount = "{:05.2f}".format(expense_entry[4])

            pattern_number_string = "{:04d}".format(index+1)
            job_number_pattern = "JOB_{}".format(pattern_number_string)
            date_pattern = "DATE_{}".format(pattern_number_string)
            from_pattern = "FROM_{}".format(pattern_number_string)
            to_pattern = "TO_{}".format(pattern_number_string)
            amount_pattern = "AMOUNT_{}".format(pattern_number_string)
            sundry_pattern = "SUNDRY_{}".format(pattern_number_string)

            text1, ntime = self.replaceText(text0, job_number_pattern, job_number)
            text0, ntime  = self.replaceText(text1, date_pattern, job_date)
            text1, ntime  = self.replaceText(text0, from_pattern, from_loc)
            text0, ntime  = self.replaceText(text1, to_pattern, to_loc)
            text1, ntime  = self.replaceText(text0, amount_pattern, amount)
            sundry_amount = "{}   {}   {}  {}".format(amount[0], amount[1], amount[3], amount[4])
            text0, ntime  = self.replaceText(text1, sundry_pattern, sundry_amount)

            total_sundry += float(amount)

        total_sundry_str = "{:5.2f}".format(total_sundry)
        sundry_total="{}   {}   {}  {}".format(total_sundry_str[0], total_sundry_str[1], total_sundry_str[3], total_sundry_str[4])
        text1, ntime  = self.replaceText(text0, "TOTAL_AMOUNT", sundry_total)
        text0, ntime  = self.replaceText(text1, "GRAND_TOTAL_AB", sundry_total)
        #print(text0)

        for index in range(max_count, self.max_count_per_page):
            expense_entry = ""
            job_number = ""
            job_date = ""
            from_loc = ""
            to_loc = ""
            amount = ""
            sundry_amount = ""

            pattern_number_string = "{:04d}".format(index+1)
            job_number_pattern = "JOB_{}".format(pattern_number_string)
            date_pattern = "DATE_{}".format(pattern_number_string)
            from_pattern = "FROM_{}".format(pattern_number_string)
            to_pattern = "TO_{}".format(pattern_number_string)
            amount_pattern = "AMOUNT_{}".format(pattern_number_string)
            sundry_pattern = "SUNDRY_{}".format(pattern_number_string)

            text1, ntime = self.replaceText(text0, job_number_pattern, job_number)
            text0, ntime  = self.replaceText(text1, date_pattern, job_date)
            text1, ntime  = self.replaceText(text0, from_pattern, from_loc)
            text0, ntime  = self.replaceText(text1, to_pattern, to_loc)
            text1, ntime  = self.replaceText(text0, amount_pattern, amount)
            text0, ntime  = self.replaceText(text1, sundry_pattern, sundry_amount)

        #print(text0)
        first_date = expenses[0][1]
        fd_str = self.reverseDate(first_date)

        last_date=expenses[max_count-1][1]
        ld_str = self.reverseDate(last_date)

        date_range = "{}-{}".format(fd_str, ld_str)
        print("date_range: {}".format(date_range))

        date_now, month_now, year_now = self.getInividualTimeNowFourDigits()

        base_path="/Users/hoangduytran//Documents/jobs/orridge/{}".format(year_now)
        is_there = (os.path.isdir(base_path))
        if (not is_there):
            os.mkdir(base_path)

        entry_path = os.path.join(base_path, os.path.join("expenses", date_range))
        is_there = (os.path.isdir(entry_path))
        if (not is_there):
            pathlib.Path(entry_path).mkdir(parents=True, exist_ok=True)

        file_without_extension = "{}_travel_expenses_claim_form".format(date_range)
        file_path = "{}.{}".format(file_without_extension, "svg")
        image_path = "{}.{}".format(file_without_extension, "png")

        #inkscape:export-filename=
        full_path = os.path.join(entry_path, file_path)
        full_image_path = os.path.join(entry_path, image_path)

        #keyword="inkscape:export-filename"
        export_pattern = r"(inkscape\:export\-filename=\")(.*)(\")"
        found = re.findall(export_pattern, text0)
        current_export_file=found[0][1]
        #print(found[0][1])
        #replace_pattern = r"inkscape:export-filename=\"{}\"".format(full_image_path)
        text1, ntime = self.replaceText(text0, current_export_file, full_image_path)
        #print("export_pattern:{}, replace_pattern:{}, replaced:{}".format(current_export_file, full_image_path, ntime))
        #print(text1)
        #exit(0)
        text0 = text1
        is_there = (os.path.isfile(full_path))
        if (is_there):
            print("overwrite file: {}".format(full_path))
        else:
            print("writing new file to full path: {}".format(full_path))

        self.writeTextToFile(full_path, text0)


#job_number, date, amount, final_amount
expenses=[
#    ["531424", "05/11/2018", "SW11 2BX", "W1J 9LE",3],
#    ["539711", "07/11/2018", "SW11 2BX", "KT6 7HT",5.6],
#    ["510563", "17/10/2018", "SW11 2BX", "SW15 2SR",3.0],
#   ["548354", "31/10/2018", "SW11 2BX", "SW3 3NR",3.0],
#    ["518252", "02/11/2018", "SW11 2BX", "KT12 1DH",15.30],
#    ["539676", "12/11/2018", "SW11 2BX", "W6 0PZ",3.0],
#    ["539703", "19/11/2018", "SW11 2BX", "CR0 1RZ",7.5],
#    ["551505", "21/11/2018", "SW11 2BX", "HA4 0AJ",8.4],
#    ["552879", "08/02/2019", "SW11 2BX", "SW4 9NF",3.0],
#    ["539791", "14/02/2019", "SW11 2BX", "SE18 6HZ",3.9],
#    ["552891", "19/02/2019", "SW11 2BX", "NW11 2JN",3.0],
#    ["552869", "21/02/2019", "SW11 2BX", "SW11 3BA",3.0],
#    ["554875", "22/02/2019", "SW11 2BX", "UB10 9PG",6.0],
#    ["550195", "27/02/2019", "SW11 2BX", "UB7 0LB",11.7],
#    ["554821", "28/02/2019", "SW11 2BX", "N19 5QT",7.0],
#    ["539815", "04/03/2019", "SW11 2BX", "SW16 1DF",8.0],
#    ["558456", "06/03/2019", "SW11 2BX", "UB1 1JR",3.0],
    #["521127", "11/03/2019", "SW11 2BX", "EC2M 4NR",3.0],
    #["553302", "13/03/2019", "SW11 2BX", "KT7 0JW",11.80],
    #["556969", "15/03/2019", "SW11 2BX", "W4 3HD",4.5],
    #["575425", "18/03/2019", "SW11 2BX", "W5 2NH",3.0],
    #["531511", "20/03/2019", "SW11 2BX", "WC2N 5EJ",3.0],
    #["553361", "22/03/2019", "SW11 2BX", "SW19 6DA",3.0],
    #["539802", "25/03/2019", "SW11 2BX", "SW9 7AE",3.0],
    #["553267", "27/03/2019", "SW11 2BX", "SW16 5SQ",4.5],
    #["553195", "29/03/2019", "SW11 2BX", "SW20 0AX",3.0],
    #["521246", "01/04/2019", "SW11 2BX", "SE1 7LY",3.0],
    #["559783", "08/04/2019", "SW11 2BX", "KT1 1BP",3.0],
    #["520936", "10/04/2019", "SW11 2BX", "W8 5SF",3.0],
    #["558603", "12/04/2019", "SW11 2BX", "SW16 3LU",5.3],
    #["558460", "17/04/2019", "SW11 2BX", "SW14 7JE",3.0],
    #["555004", "01/05/2019", "SW11 2BX", "SW2 4RU",3.0],
    #["568841", "08/05/2019", "SW11 2BX", "W12 7GF",3.0],
    #["553169", "10/05/2019", "SW11 2BX", "SW6 4HU",0.0],
    #["553369", "05/06/2019", "SW11 2BX", "",3.0],
    #["553375", "07/06/2019", "SW11 2BX", "",9.7],
    #["566023", "10/06/2019", "SW11 2BX", "RH6 0PJ",18.9],
    #["568186", "12/06/2019", "SW11 2BX", "SE6 3BT",8.1],
    #["578387", "14/06/2019", "SW11 2BX", "W12 7GE",1.5],
    #["568191", "17/06/2019", "SW11 2BX", "KT4 8DR",8.0],
    #["571055", "19/06/2019", "SW11 2BX", "SW18 4TF",0.0],
    #["552972", "21/06/2019", "SW11 2BX", "SW6 6BT",3.0],
    #["548916", "26/06/2019", "SW11 2BX", "W12 7HT",3.0],
    #["566008", "27/06/2019", "SW11 2BX", "EC2M 7QA",5.4],
    #["521241", "01/07/2019", "SW11 2BX", "TW9 1HF",5.0],
    #["571071", "03/07/2019", "SW11 2BX", "SW15 1TW",3.0],
    #["568215", "04/07/2019", "SW11 2BX", "SW15 1RB",0.0],
    #["580964", "05/07/2019", "SW11 2BX", "KT12 1DH",8.2],
    #["559379", "08/07/2019", "SW11 2BX", "SW11 1PW",0.0],
    #["568274", "10/07/2019", "SW11 2BX", "KT19 8AJ",10.0],
    #["559375", "12/07/2019", "SW11 2BX", "SW4 7UB",3.0],
    #["580694", "15/07/2019", "SW11 2BX", "KT1 1QP",6.0],
    #["580695", "16/07/2019", "SW11 2BX", "KT19 8BA",4.5],
    #["520758", "22/07/2019", "SW11 2BX", "SW19 2TY",3.0],
    #["520963", "24/07/2019", "SW11 2BX", "DA9 9SJ",6.9],
    #["571594", "26/07/2019", "SW11 2BX", "RH10 9AN",24.2], //
    #["568244", "29/07/2019", "SW11 2BX", "ME4 4BA",4.5],
    #["582332", "31/07/2019", "SW11 2BX", "SE5 8RW",4.5],
    #["555942", "02/08/2019", "SW11 2BX", "KT15 2TX",15.6],
    #["568315", "05/08/2019", "SW11 2BX", "SW18 4TE",0.0],
    #["559257", "07/08/2019", "SW11 2BX", "UB1 1JR",4.7],
    #["571595", "09/08/2019", "SW11 2BX", "ME20 7NA",8.5], //
    #["582481", "12/08/2019", "SW11 2BX", "EN8 7BX",11.0],
    #["571087", "14/08/2019", "SW11 2BX", "KT12 1BZ",7.0],
    #["568284", "19/08/2019", "SW11 2BX", "UB1 1QB",5.5],
    #["578308", "23/08/2019", "SW11 2BX", "W12 7GF",4.7],
    #["553855", "28/08/2019", "SW11 2BX", "SW16 5PY",5.7],
    #["582373", "01/09/2019", "SW11 2BX", "SW9 8ED",5.1],
    #["571205", "02/09/2019", "SW11 2BX", "W1J 9LE ",3.0],
    #["571219", "04/09/2019", "SW11 2BX", "WC2N 5EJ",3.0],
    #["553082", "06/09/2019", "SW11 2BX", "NW5 2AB",3.0],
    #["559834", "09/09/2019", "SW11 2BX", "SM1 1AX",8.6],
    #["553280", "23/09/2019", "SW11 2BX", "KT18 5NX",20.9],
    #["571220", "25/09/2019", "SW11 2BX", "SW1Y 6WW",3.0],
    #["553280", "23/09/2019", "SW11 2BX", "KT18 5NX",5.8],
    #["574073", "30/09/2019", "SW11 2BX", "SW1P 4RG",0.0],
    #["573767", "02/10/2019", "SW11 2BX", "NW6 4HJ",3.0],
    #["573769", "03/10/2019", "SW11 2BX", "UB8 1LN",5.8],
    #["100410", "07/10/2019", "SW11 2BX", "SW16 1EX",3.0],
    #["100401", "09/10/2019", "SW11 2BX", "SE5 8RZ",3.0],
    #["553532", "11/10/2019", "SW11 2BX", "SW11 1NG",0.0],
    #["571182", "14/10/2019", "SW11 2BX", "W5 5JY",8.2],
    #["586223", "15/10/2019", "SW11 2BX", "SW1W 8AQ",0.0],
    #["587053", "15/10/2019", "SW11 2BX", "TW11 8QZ",12.8],
    #["573769", "17/10/2019", "SW11 2BX", "HA9 7BS",4.5],
    #["559354", "20/10/2019", "SW11 2BX", "SW1V 1JT",3.0],
    #["559350", "22/10/2019", "SW11 2BX", "SW6 1NN",3.0],
    #["553240", "24/10/2019", "SW11 2BX", "W12 9RA",4.5],
    #["560736", "29/10/2019", "SW11 2BX", "SW18 4TG",3.0],
    #["574096", "01/11/2019", "SW11 2BX", "TW16 5DB",15.5],
    #["574100", "02/11/2019", "SW11 2BX", "TW16 5DB",8.6],
    #["000000", "03/11/2019", "SW11 2BX", "TFL Refunds",-9.8],
    #["", "/11/2019", "SW11 2BX", "",0.0],
    #["586772", "05/11/2019", "SW11 2BX", "KT1 1TR",6.0],
    #["582004", "06/11/2019", "SW11 2BX", "TW6 2GA",19.4],
    #["582004", "07/11/2019", "SW11 2BX", "TW6 2GA - TFL refund: 0008255502",-2.6],
    #["581997", "11/11/2019", "SW11 2BX", "TW6 1QG",4.5],
    #["582379", "14/11/2019", "SW11 2BX", "W12 7GE",4.5],
    #["581994", "18/11/2019", "SW11 2BX", "TW6 1LN",6.0],
    #["553150", "21/11/2019", "SW11 2BX", "SW6 4LX",3.0],
    #["553084", "28/11/2019", "SW11 2BX", "",6.8],
    #["553084", "28/11/2019", "SW11 2BX", "TFL refund ref:1431 1251",-1.5],
    #["552900", "03/12/2019", "SW11 2BX", "NW2 3HD",3.0],
    #["573787", "07/01/2020", "SW11 2BX", "RG12 1BE",4.5],
    #["595362", "08/01/2020", "SW11 2BX", "NW9 0AS",1.5],
    #["595362", "09/01/2020", "SW11 2BX", "NW9 0AS",4.5],
    #["570951", "14/01/2020", "SW11 2BX", "NW3 6JP",7.2],
    #["573798", "21/01/2020", "SW11 2BX", "CT1 2TJ",3.0],
    #["573798", "22/01/2020", "CT1 2TJ", "SW11 2BX",1.5],
    #["573803", "23/01/2020", "SW11 2BX", "CT10 2BF",3.9],
    #["573803", "24/01/2020", "CT10 2BF", "SW11 2BX",1.5],
    # ["571725", "28/01/2020", "SW11 2BX", "EC1N 2TD",3.0],
    # ["589568", "30/01/2020", "SW11 2BX", "SE19 1BG",3.0],
    # ["584936", "12/02/2020", "SW11 2BX", "ME20 6SQ",7.20],
    # ["584940", "13/02/2020", "SW11 2BX", "ME20 6SQ",5.40],
    # ["589541", "18/02/2020", "SW11 2BX", "SW11 3BA",3.0],
    # ["589703", "28/02/2020", "SW11 2BX", "CR3 5UG",6.10],
    # ["589703", "28/02/2020", "SW11 2BX", "CR3 5UG TFL Refund: 1473726 (12:30, 02/03/2020)",-1.70],
    # ["589703", "28/02/2020", "SW11 2BX", "CR3 5UG Taking different route, circumstantial",-2.90],
    # ["589703", "28/02/2020", "SW11 2BX", "CR3 5UG Train return to Upper Wallingham",10.00],
    # ["589703", "28/02/2020", "SW11 2BX", "CR3 5UG Bus 409)",2.60],
    # ["589703", "28/02/2020", "CR3 5UG", "SW11 2BX Bus 357)",3.00],
    # ["613614", "02/03/2020", "SW11 2BX", "HA9 7AE",5.8],
    # ["589756", "04/03/2020", "SW11 2BX", "SE22 8HJ",3.0],
    # ["615870", "16/03/2020", "SW11 2BX", "TW6 1QB",6.0],
    # ["576294", "18/03/2020", "SW11 2BX", "W12 7GF",3.0],
    ["614082", "30/10/2020", "SW11 2BX", "TW16 5DB", 14.0],
    ["646257", "31/10/2020", "SW11 2BX", "TW16 5DB",7.8],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
    ["", "", "SW11 2BX", "",0.0],
]

from_doc = "/Users/hoangduytran/Documents/jobs/orridge/travel_expenses_claim_form_base.svg"
x = FillTravelForm()
x.setFromDocument(from_doc)
x.fillTravelForm()

