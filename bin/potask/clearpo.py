from sphinx_intl import catalog as c
from potask_base import POTaskBase, POResultRecord
from string_utils import StringUtils as su
class ClearPO(POTaskBase):
    def __init__(self,
                 input_file=None,
                 output_to_file=None,
                 clear_po_comment=None,
                 is_clear_dup=None
                 ):
        POTaskBase.__init__(
                self,
                input_file=input_file,
                output_to_file=output_to_file,
                clear_po_comment=clear_po_comment,
                is_clear_dup=is_clear_dup
        )

    def performTask(self):
        self.setFiles()

        changed = False
        msg_data = c.load_po(self.po_path)
        line_count = 0
        for index, m in enumerate(msg_data):
            is_dup = False
            is_first_line = (index == 0)
            if is_first_line:
                continue


            old_str = m.string
            is_blank = not bool(old_str)
            if is_blank:
                continue

            if self.is_clear_dup:
                is_dup = self.isDup(m.id, m.string)
                if is_dup:
                    changed = True
                    is_fuzzy = m.fuzzy
                    m.string = ""
                    if is_fuzzy:
                        m.flags.remove('fuzzy')
            else:
                is_fuzzy = m.fuzzy
                m.string = ""
                if is_fuzzy:
                    m.flags.remove('fuzzy')

                if self.clear_po_comment:
                    m.auto_comments = []
                    m.user_comments = []
                    m.locations = []
                    m.flags = ()

                changed = True

            if is_dup:
                r = POResultRecord(index + 1, m.id, old_str)
                self.append(r)

        is_output = (changed and bool(self.opo_path))
        if is_output:
            c.dump_po(self.opo_path, msg_data)
        else:
            self.showResult()



# -s -dmid -mstr -p "Delta" -of /Users/hoangduytran/test_0001.po

