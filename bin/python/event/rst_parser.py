import os
from common import Common
import re

class RSTParser:
    def __init__(self, my_line_list):
        self.my_line_list  = my_line_list
        self.previous_line_index  = 0
        self.current_text_block  =[]
        self.current_block  = None
        self.document  = None
        self.text_line  = None
        self.line_index  = -1

    def setArgs(self, my_line_list):
        self.my_line_list = my_line_list

    def setTextLine(self, text_line):
        self.text_line = text_line

    def setDocument(self, document:object):
        self.document = document

    def setLineIndex(self, line_index):
        self.line_index = line_index

    def setPreviousLineIndex(self, prev_line_index):
        self.previous_line_index = prev_line_index

    def run(self):
        pass

    def addBlock(self, header_line):
        new_block = TextBlock(self.document)
        new_block.init()
        new_block.setMSGID(header_line)
        new_block.setMSGSTR("")
        return new_block

    def __repr__(self):
        content_list=[]

class RSTUnderlinedHeader(RSTParser):
    def __init__(self, my_line_list):
        super().__init__(my_line_list)
        self.is_underlined_p = re.compile(Common.RE_RST_UNDERLINED)
        self.is_alpha_p = re.compile(Common.RE_IS_ALPHA)

    def run(self):

        total_size = len(self.my_line_list)
        has_next_line = (self.line_index + 1 < total_size)
        if (not has_next_line):
            return None

        m4 = self.is_alpha_p.match(self.text_line)
        is_alpha = (m4 != None)

        next_line_index = self.line_index + 1
        next_line = self.my_line_list[next_line_index]

        m2 = self.is_underlined_p.match(next_line)
        is_next_line_underlined = (m2 != None)

        is_title_line = (is_alpha and is_next_line_underlined)
        if (is_title_line):
            #print("tabbed header_line:{}".format(self.text_line))
            return self.addBlock(self.text_line)
        else:
            return None

        # #print("text_line:{}".format(self.text_line))
        # m = self.underlined_p.match(self.text_line)
        # is_potential_header = (self.previous_line_index > 0) and (m != None)
        # #print("first_char: {} is_potential_header:{}".format(first_char, is_potential_header))
        # if (not is_potential_header):
        #     self.previous_line_index = self.line_index
        #     return None
        #
        # header_line  = None
        # is_title_line = (self.previous_line_index >= 0) and (self.previous_line_index == self.line_index-1)
        # if (is_title_line):
        #     header_line = self.my_line_list[self.previous_line_index]
        #     #print("header_line:{}".format(header_line))
        #     return self.addBlock(header_line)
        # else:
        #     return None
        # #print("header_line:{} text_line:{}".format(header_line, self.text_line))


class RSTTabbedHeader(RSTParser):
    def __init__(self, my_line_list):
        super().__init__(my_line_list)
        self.tabbed_p = re.compile(Common.RE_LEADING_SPACES)
        self.is_underlined_p = re.compile(Common.RE_RST_UNDERLINED)
        self.rst_special_p = re.compile(Common.RE_RST_SPECIAL)
        self.is_alpha_p = re.compile(Common.RE_IS_ALPHA)
        self.dup_list={}

    def countLeadingSpace(self, text_line):
        trimmed = str(text_line).strip()
        count = len(text_line) - len(trimmed)
        return count

    def run(self):

        """
        Checking to see if

        current_line and below line has a difference in leading tabbulation (indentation)

        need to check if the line below is not for code

        :return:
        """

        total_size = len(self.my_line_list)
        has_next_line = (self.line_index + 1 < total_size)
        if (not has_next_line):
            return None

        next_line_index = self.line_index + 1
        line_below = self.my_line_list[next_line_index]

        leading_space_count_this_line = self.countLeadingSpace(self.text_line)
        leading_space_count_next_line = self.countLeadingSpace(line_below)

        is_next_line_underlined = Common.isUnderlined(line_below)
        is_ended_full_stop = Common.isEndedFullStop(self.text_line)

        is_ignored = Common.isIgnored(self.text_line)
        is_ignore_start = Common.isIgnoredIfStartsWith(self.text_line)
        is_ignore = (is_ignored or is_ignore_start)

        is_possible_title_line = (leading_space_count_this_line < leading_space_count_next_line) or \
                                    (is_next_line_underlined) and \
                                    (not is_ended_full_stop) and \
                                    (not is_ignore)

        is_title_line = False
        tile_text_line = self.text_line

        if (is_possible_title_line):

            trim_copy = tile_text_line.strip()

            is_keyboard = Common.isMustIncludedKeyboardPart(trim_copy)
            is_alpha = Common.isLeadingAlpha(trim_copy)
            is_in_ignore_startswith = Common.isIgnoredIfStartsWith(trim_copy)
            is_in_ignore_list = Common.isIgnored(trim_copy)
            is_in_duplist = (self.dup_list.get(trim_copy) != None)
            is_ended_with_fullstop = (trim_copy.endswith(Common.DOT))

            is_title_line = (is_keyboard or is_alpha) and \
                            (not is_in_ignore_startswith) and \
                            (not is_in_ignore_list) and \
                            (not is_in_duplist) and \
                            (not is_ended_with_fullstop)

#            is_debug = trim_copy.startswith("Min X/Y and Max X/Y")
#            if (is_debug):
#                 self.document.printTitleOnce()
#                 print("RSTTabbedHeader:[{}], is_title_line:{}".format(trim_copy, is_title_line))
#                 #exit(1)

            if (is_title_line):

                self.dup_list.update({trim_copy:trim_copy})
                #self.document.printTitleOnce()
                #print("title_line:{}".format(trim_copy))
                return self.addBlock(trim_copy)

        return None
        #print("header_line:{} text_line:{}".format(header_line, self.text_line))

