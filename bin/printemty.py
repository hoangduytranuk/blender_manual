from potask_base import POTaskBase, POResultRecord
import os
from sphinx_intl import catalog as c
from ignore import Ignore as ig

class PrintEmptyLine(POTaskBase):
    def __init__(self,
                 input_file=None,
                 output_to_file=None,
                 validate_file=None
                 ):
        POTaskBase.__init__(
                self,
                input_file=input_file,
                output_to_file=output_to_file,
                validate_file=validate_file)

    def performTask(self):

        self.setFiles()

        val_data = None
        has_validate = bool(self.validate_file) and os.path.isfile(self.validate_file)
        if has_validate:
            val_data = c.load_po(self.validate_file)
            has_validate = bool(val_data) and (len(val_data) > 0)

        msg_data = c.load_po(self.po_path)
        line_count = 0
        for index, m in enumerate(msg_data):
            is_fuzzy = m.fuzzy
            is_translated = bool(m.string)
            is_ignore = (is_translated and not is_fuzzy)
            is_in_validate_data = False

            if is_ignore:
                continue

            msgid = m.id
            if has_validate:
                is_in_validate_data = (msgid in val_data)

            if self.filter_ignored:
                is_ignored = (ig.isIgnored(msgid, is_debug=False))
                if is_ignored:
                    continue

            if is_in_validate_data:
                continue

            if self.count_number_of_lines:
                self.line_count += 1

            r = POResultRecord(index+1, msgid, "")
            self.append(r)
        self.showResult()



# -s -dmid -mstr -p "Delta" -of /Users/hoangduytran/test_0001.po

