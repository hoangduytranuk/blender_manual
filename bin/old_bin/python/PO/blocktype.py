import sys
from enum import Enum

class BlockType(Enum):
    COMMENT="#",
    MSGCTXT="msgctxt",
    MSGID="msgid",
    MSGSTR="msgstr"
    INVALID=None

    blk_list=[COMMENT, MSGCTXT, MSGID, MSGSTR]

    def describe(self):
        return self.name, self.value

    def __str__(self):
        return "{0}".format(self.name)
