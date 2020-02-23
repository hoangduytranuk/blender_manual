#!/usr/bin/env python3
"""
Using sphinx catalog to read/write PO file
Transfer msgstr from new_vipo/vi.po to po/blender.pot to create new vi.po file
"""

import sys
#sys.path.append("/home/htran/.local/lib/python3.6/site-packages")
sys.path.append("/home/htran/bin/python/PO")
sys.path.append("/home/htran/bin")
#print("sys.path:", sys.path)
#exit(0)
import re
import os
import io

from sphinx_intl import catalog as c
from common import Common as cm
from babel.messages.catalog import Message
from babel._compat import text_type, cmp

from bisect import bisect_left
from babel.messages import pofile
from pprint import pprint as pp

class Comparator(object):

    def setItem(a):
        self.item=a

    def compare(self, a, b):
        pass

    def __eq__ (self, a, b):
        return (self.compare(a, b) == 0)

    def __lt__ (self, a, b):
        return (self.compare(a, b) < 0)

    def __gt__ (self, a, b):
        return (self.compare(a, b) > 0)

    def getKey(self, a):
        pass

    def setLower(self, value):
        pass

    def setHigher(self, value):
        pass

    def getAtIndex(self, index):
        pass


class POListComparator(Comparator):
    def compare(self, a, b):
        pass

class UpdateVIPO:
    from_vipo_path="/home/htran/blender_documentations/new_po/vi.po"
    to_blender_pot_path="/home/htran/blender_documentations/github/blender_manual/gui/2.79/po/vi.po"

    def __init__(self):
        self.from_po_cat = c.load_po(UpdateVIPO.from_vipo_path)
        self.to_po_cat = c.load_po(UpdateVIPO.to_blender_pot_path)
        self.sorted_from_po_cat = None

    def poCatToList(self, po_cat):
        l=[]
        for index, m in enumerate(po_cat):
            context = m.context
            #print("context:{}".format(context))
            k = m.id
            v = m
            l.append((k, context, v))
        return l

    def binarySearch(self, sorted_list, po_entry, is_lcase=False):
        #found_item = Algo.binarySearch(self.block_list, msgid_entry, cmp=self.compareMSGID)
        is_debug = False
        is_debug_on = False
        ss_list = sorted_list
        lo = 0
        hi = len(ss_list)
        mid = -1
        while (lo < hi):
            mid = (lo + hi) // 2
            k, c, v = ss_list[mid]

            is_debug = (po_entry.id == "Random seed")
            if (not is_lcase):
                ss_list_entry = "{}{}".format(k,c)
                po_entry_msg = "{}{}".format(po_entry.id, po_entry.context)
                ss_list_entry_id = k
                po_entry_msg_id = po_entry.id
            else:
                ss_list_entry = "{}{}".format(k.lower(),c)
                po_entry_msg = "{}{}".format(po_entry.id.lower(), po_entry.context)
                ss_list_entry_id = k.lower()
                po_entry_msg_id = po_entry.id.lower()

            is_equal = (ss_list_entry == po_entry_msg) or (ss_list_entry_id == po_entry_msg_id)
            if (is_debug):
                print("ss_list_entry:", ss_list_entry)
                print("po_entry_msg:", po_entry_msg)
                print("is_equal:", is_equal)

            if (is_equal):
                return v
            elif (ss_list_entry < po_entry_msg):
                #print("lo = mid + 1")
                lo = mid + 1
            else:
                #print("hi = mid")
                hi = mid
        #print("Not found")
        #exit(0)
        return -1

    def dump_po(self, filename, catalog):
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # Because babel automatically encode strings, file should be open as binary mode.
        with io.open(filename, 'wb') as f:
            #pofile.write_po(f, catalog, width=0)
            self.write_po(f, catalog, ignore_obsolete=True)



    def write_po(self, fileobj, catalog, width=76, no_location=False, omit_header=False,
                sort_output=False, sort_by_file=False, ignore_obsolete=False,
                include_previous=False, include_lineno=True):
        r"""Write a ``gettext`` PO (portable object) template file for a given
        message catalog to the provided file-like object.

        >>> catalog = Catalog()
        >>> catalog.add(u'foo %(name)s', locations=[('main.py', 1)],
        ...             flags=('fuzzy',))
        <Message...>
        >>> catalog.add((u'bar', u'baz'), locations=[('main.py', 3)])
        <Message...>
        >>> from babel._compat import BytesIO
        >>> buf = BytesIO()
        >>> write_po(buf, catalog, omit_header=True)
        >>> print(buf.getvalue().decode("utf8"))
        #: main.py:1
        #, fuzzy, python-format
        msgid "foo %(name)s"
        msgstr ""
        <BLANKLINE>
        #: main.py:3
        msgid "bar"
        msgid_plural "baz"
        msgstr[0] ""
        msgstr[1] ""
        <BLANKLINE>
        <BLANKLINE>

        :param fileobj: the file-like object to write to
        :param catalog: the `Catalog` instance
        :param width: the maximum line width for the generated output; use `None`,
                    0, or a negative number to completely disable line wrapping
        :param no_location: do not emit a location comment for every message
        :param omit_header: do not include the ``msgid ""`` entry at the top of the
                            output
        :param sort_output: whether to sort the messages in the output by msgid
        :param sort_by_file: whether to sort the messages in the output by their
                            locations
        :param ignore_obsolete: whether to ignore obsolete messages and not include
                                them in the output; by default they are included as
                                comments
        :param include_previous: include the old msgid as a comment when
                                updating the catalog
        :param include_lineno: include line number in the location comment
        """
        def quoted(text):
            has_many_lines = (text.find(u'\n') >= 0)
            if (has_many_lines):
                old_text_list= text.split( u'\n')
                text_list=[]
                #print("old_text_list:", old_text_list)
                print(repr(text))
                #print("escaped:[{}]".format(pofile.escape(text)))
                max_index=len(old_text_list)
                text_list.append("\"\"")
                for index, line in enumerate(old_text_list):
                    is_last_line = (index >= max_index-1)
                    if (line):
                        if (not is_last_line):
                            esc_text = pofile.escape(line + u'\n')
                        else:
                            esc_text = pofile.escape(line)
                        text_list.append(esc_text)
                esc_text = os.linesep.join(text_list)
                #print("esc_text:\n", esc_text)
                #exit(0)
            else:
                esc_text = pofile.escape(text)
            return "{}".format(esc_text)
            #return normalize(key, prefix=prefix, width=width)

        def _write(text):
            if isinstance(text, text_type):
                text = text.encode(catalog.charset, 'backslashreplace')
            fileobj.write(text)

        def _write_comment(comment, prefix='', is_user_comment=False):
            # xgettext always wraps comments even if --no-wrap is passed;
            # provide the same behaviour
            #print("is_user_comment -----------<")
            #print(repr(comment))
            #print("is_user_comment ----------->")
            if (is_user_comment):
                print("is_user_comment")
                print(repr(comment))
                #exit(0)

            SC = "script"
            SRC= "source"
            is_script = comment.startswith(SC)
            is_source = comment.startswith(SRC)
            is_sc = (is_script or is_source)
            if (is_sc):
                text_list=comment.split(' ')

                #print("is_user_comment -----------<")
                #print(text_list)
                #print("is_user_comment ----------->")
                for sc in text_list:
                    sc_text = '#%s %s\n' % (prefix, sc.strip())
                    #print(sc_text)
                    _write(sc_text)
                ##print(repr(comment))
                ##exit(0)
            else:
                #comment_stripped = comment.strip()
                has_len = (len(comment) > 0)
                if (has_len):
                    _write('#%s %s\n' % (prefix, comment))

        def _write_message(message, prefix=''):
            if isinstance(message.id, (list, tuple)):
                if message.context:
                    _write('%smsgctxt %s\n' % (prefix, quoted(message.context)))
                _write('%smsgid %s\n' % (prefix, quoted(message.id[0])))
                _write('%smsgid_plural %s\n' % (prefix, quoted(message.id[1])))

                for idx in range(catalog.num_plurals):
                    try:
                        string = message.string[idx]
                    except IndexError:
                        string = ''
                    _write('%smsgstr[%d] %s\n' % (prefix, idx, quoted(string)))
            else:
                if message.context:
                    _write('%smsgctxt %s\n' % (prefix, quoted(message.context)))

                _write('%smsgid %s\n' % (prefix, quoted(message.id)))
                _write('%smsgstr %s\n' % (prefix, quoted(message.string or '')))

        sort_by = None
        if sort_output:
            sort_by = "message"
        elif sort_by_file:
            sort_by = "location"

        for message in catalog:
            if not message.id:  # This is the header "message"
                if omit_header:
                    continue
                comment_header = catalog.header_comment
                _write(comment_header + u'\n')

            for comment in message.user_comments:
                _write_comment(comment, is_user_comment=True)
            for comment in message.auto_comments:
                _write_comment(comment, prefix='.')

            if not no_location:
                locs = []

                # Attempt to sort the locations.  If we can't do that, for instance
                # because there are mixed integers and Nones or whatnot (see issue #606)
                # then give up, but also don't just crash.
                try:
                    locations = sorted(message.locations)
                except TypeError:  # e.g. "TypeError: unorderable types: NoneType() < int()"
                    locations = message.locations

                for filename, lineno in locations:
                    if lineno and include_lineno:
                        locs.append(u'%s:%d' % (filename.replace(os.sep, '/'), lineno))
                    else:
                        locs.append(u'%s' % filename.replace(os.sep, '/'))
                _write_comment(' '.join(locs), prefix=':')
            if message.flags:
                _write('#%s\n' % ', '.join([''] + sorted(message.flags)))

            _write_message(message)
            _write('\n')

        if not ignore_obsolete:
            for message in _sort_messages(
                catalog.obsolete.values(),
                sort_by=sort_by
            ):
                for comment in message.user_comments:
                    _write_comment(comment)
                _write_message(message, prefix='#~ ')
                _write('\n')


    def run(self):
        from_po_dic = self.poCatToList(self.from_po_cat)
        self.sorted_from_po_cat = sorted(from_po_dic, key = lambda x: "{}{}".format(x[0], x[1]))
        self.sorted_lower_po_cat = sorted(from_po_dic, key = lambda x: "{}{}".format(x[0].lower(), x[1]))

        #pp(self.sorted_from_po_cat)
        #exit(0)
        changed = False
        for index, po_entry in enumerate(self.to_po_cat):
            is_first_entry = (index == 0)
            if (is_first_entry):
                continue

            #print("id:{}, is_fuzzy:{}".format(po_entry.id, po_entry.fuzzy))

            #if (po_entry.fuzzy):
                #exit(0)
            #else:
                #continue

            k = po_entry.id
            found_entry = self.binarySearch(self.sorted_from_po_cat, po_entry)
            is_in = isinstance(found_entry, Message)

            if (not is_in):
                #print("Not found: {}".format(k))
                #print("Find in lower case list: ", k)
                found_entry = self.binarySearch(self.sorted_lower_po_cat, po_entry, is_lcase=True)
                is_in = isinstance(found_entry, Message)
                if (not is_in):
                    #print("Not Found, NEW: {}".format(k))
                    continue


            old_translation = po_entry.string
            new_translation = found_entry.string
            is_change = (old_translation != new_translation)

            if (not is_change):
                continue

            #print("po_entry:", po_entry.id)
            #print("Found entry:", found_entry.id)

            po_entry.string = found_entry.string
            #changed = False
            changed = True

            print("msgid \"{}\"".format(po_entry.id))
            print("OLD msgstr \"{}\"".format(old_translation))
            print("NEW msgstr \"{}\"".format(po_entry.string))
            print("-" * 20)
            #print("po_entry.id:{}, po_entry.string:{}, po_entry.fuzzy:{}".format(po_entry.id, po_entry.string, po_entry.fuzzy))

        if (changed):
            new_po_file = "/home/htran/new_279_vi.po"
            print("Saving content of new to_po_cat to:{}".format(new_po_file))
            self.dump_po(new_po_file, self.to_po_cat)


x = UpdateVIPO();
x.run()
