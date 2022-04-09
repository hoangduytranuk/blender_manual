#!/usr/bin/env python3
"""
Using sphinx catalog to read/write PO file
Transfer msgstr from new_vipo/vi.po to po/blender.pot to create new vi.po file
"""
import pprint

import sys
sys.path.append('/usr/local/lib/python3.9/site-packages')

import os
import io
from argparse import ArgumentParser
from sphinx_intl import catalog as c
from babel.messages import pofile, Catalog, Message
from collections import OrderedDict
from datetime import datetime, date
from enum import Enum

class Action(Enum):
    DO_NOTHING = 0
    ADD_NEW_USING_FROM_SOURCE = 1
    TAKE_DATA_OF_FROM_SOURCE = 2

class MergePO:

    def __init__(self, from_file, to_file, out_file, add_from_source, sort_file):
        self.from_path = from_file
        self.to_path = to_file
        self.out_path = out_file
        self.message_field_list = None
        self.is_add_from_source = (True if bool(add_from_source) else False)
        self.is_sort_message = (True if bool(sort_file) else False)
        self.modi_from_dict = OrderedDict()
        self.modi_to_dict = OrderedDict()


    def run(self):
        def getAction(from_obj, to_obj):
            has_to = bool(to_obj) and len(to_obj) > 0
            has_from = bool(from_obj) and len(from_obj) > 0
            is_diff = (from_obj != to_obj)

            is_new = (has_from and not has_to)
            if is_new:
                return Action.ADD_NEW_USING_FROM_SOURCE

            if is_diff:
                return Action.TAKE_DATA_OF_FROM_SOURCE
            else:
                return Action.DO_NOTHING

        def performAction(field_name):
            fr: Message = performAction.fr
            tr: Message = performAction.tr
            from_data_value = getattr(fr, field_name, None)
            to_data_value = getattr(tr, field_name, None)
            is_degbug = ('Separate an atom' in fr.id) and (field_name == 'flags')
            if is_degbug:
                is_degbug = True
            action_required = getAction(from_data_value, to_data_value)
            is_ignore = (action_required == Action.DO_NOTHING)
            is_add_new = (action_required == Action.ADD_NEW_USING_FROM_SOURCE)
            is_taking_from_data = (action_required == Action.TAKE_DATA_OF_FROM_SOURCE)

            if is_ignore:
                return False
            elif is_add_new or is_taking_from_data:
                msg = f'performAction(): to_data_value:[{to_data_value}] => from_data_value:[{from_data_value}]'
                print(msg)
                has_forbbid_data = ('None (None)' in from_data_value)
                if not has_forbbid_data:
                    setattr(tr, field_name, from_data_value)
                return True
            else:
                msg = f'performAction(): ERROR: last ELSE, return FALSE: {fr} => {tr}'
                print(msg)
                return False

        def actionOnDataFields(data_fields):
            result_list=[]
            fr = actionOnDataFields.from_record
            tr = actionOnDataFields.to_record
            performAction.fr = fr
            performAction.tr = tr
            changed_field_list = list(filter(performAction, self.message_field_list))
            changed = (True in changed_field_list)
            if changed:
                from_record_msg = f'{fr.id}\n{fr.context}'
                to_record_msg = f'{tr.id}\n{tr.context}'
                print(f'actionOnDataFields(): from_msg:{from_record_msg}\nto_msg:{to_record_msg}')
            return changed_field_list

        def pairingRecords(to_message: Message):
            m: Message = None

            valid = bool(to_message) and bool(to_message.id)
            if not valid:
                return (None, None)


            from_catalog: Catalog = pairingRecords.from_data_set
            from_message: Message = from_catalog[to_message.id]
            valid = bool(from_message) and bool(from_message.id)
            if not valid:
                return (None, None)

            print(f'pairingRecords(): {from_message} => {to_message}')
            return (from_message, to_message)

        def mergingPair(message_pair):
            from_message: Message = None
            to_message: Message = None
            (from_message, to_message) = message_pair
            has_from = bool(from_message)
            has_to = bool(to_message)
            is_add_new = (has_from and not has_to)
            is_merge = (has_from and has_to)
            # this part doesnt have any effects at the moment, but leave it here
            # just in case changing mind to include from-Messages
            if is_add_new:
                self.modi_from_dict.update({from_message.id: from_message})
                self.modi_to_dict.update({to_message.id: to_message})
                to_data_set: Catalog = mergingPair.to_data_set
                del to_data_set[from_message.id]
                to_data_set[from_message.id] = from_message
                print(f'mergingPair(): ADD NEW: {from_message}')
                return from_message # indicate this message is processed
            elif is_merge:
                actionOnDataFields.from_record: Message = from_message
                actionOnDataFields.to_record: Message = to_message
                result_list = actionOnDataFields(self.message_field_list)
                if len(result_list) > 0:
                    self.modi_from_dict.update({from_message.id: from_message})
                    self.modi_to_dict.update({to_message.id: to_message})
                    print(f'mergingPair(): actionOnDataFields: {from_message.id} => {to_message.id}')
                    print('-' * 80)
                return from_message # indicate this message is processed
            else:
                return to_message # indicate this message is NOT processed

        def removeProcessedRecords(done_msg: Message):
            from_data_set = removeProcessedRecords.from_data_set
            del from_data_set[done_msg.id]

        def addNoneProcessed(add_message: Message):
            valid = bool(add_message) and bool(add_message.id) and (len(add_message.id) > 0)
            if not valid:
                return (False, add_message)

            to_data_set = addNoneProcessed.to_data_set
            to_data_set[add_message.id] = add_message
            print(f'addNoneProcessed(): added: {add_message}')
            return (True, add_message)


        from_data: Catalog = None
        to_data: Catalog = None

        if not bool(self.from_path):
            parser.print_help(sys.stdout)

        if os.path.isfile(self.from_path):
            from_data = c.load_po(self.from_path)
        else:
            msg = f'Must specify a file to load from!'
            raise RuntimeError(msg)

        now = datetime.now()
        now_str = now.strftime("%d/%m/%Y %H:%M:%S")
        msg = f'from_file:[{self.from_path}]\nto_file:[{self.to_path}]\ntime:[{now_str}]'
        print(msg)

        if os.path.isfile(self.to_path):
            to_data = c.load_po(self.to_path)
        else:
            to_data = None

        m: Message = None
        add_list=[]
        changed = False
        write_changes = False

        pairingRecords.from_data_set = from_data
        mergingPair.from_data_set = from_data
        mergingPair.to_data_set = to_data
        removeProcessedRecords.from_data_set = from_data
        addNoneProcessed.to_data_set = to_data

        # (first_id, first_message) = list(from_data._messages.items())[0]
        # moa_list = dir(first_message)  # message original attributes/properties list
        # field_list = [x for x in moa_list if not (x.startswith('__') or x[0].isupper())]  # message concerned attributes list
        # field_list.sort()
        # self.message_field_list = field_list
        # self.message_field_list = ['id', 'string', 'context', 'locations', 'flags']
        self.message_field_list = ['string', 'flags']

        record_pairs = list(map(pairingRecords, to_data))
        record_pairs = [(x, y) for (x, y) in record_pairs if bool(x) and bool(y)]

        # intenteded to output changes in modi_from_dict, modi_to_dic to separate PO files so can compare diff between them
        # noted that record in the format {key id: message record} dictionary to avoid duplications.
        processed_list = list(map(mergingPair, record_pairs))
        id_list = [x.id for x in processed_list]

        if self.is_add_from_source:
            del_result = list(map(from_data.delete, id_list))
            added_records = list(map(addNoneProcessed, from_data))

        changed = (len(processed_list) > 0) or (len(added_records) > 0)
        write_changes = (changed and bool(self.out_path))
        if write_changes:
            msg = f'Output changes to: [{self.out_path}]'
            c.dump_po(self.out_path, to_data, line_width=4069, sort_output=self.is_sort_message)

parser = ArgumentParser()
parser.add_argument("-f", "--from_file", dest="from_file", help="FROM PO files to merge.")
parser.add_argument("-t", "--to_file", dest="to_file", help="TO PO files to merge. Data from to po file takes priority.")
parser.add_argument("-o", "--out_file", dest="out_file", help="PO file path to write output to.")
parser.add_argument("-af", "--add_unexisted_from_sort", dest="add_unexisted_records_from_sort", help="Add records that are no longer existed in the new file from the FromSource.", action='store_const', const=True)
parser.add_argument("-s", "--sort_file", dest="sort_out_file", help="sort output PO file in ascending order.", action='store_const', const=True)

args = parser.parse_args()

x = MergePO(args.from_file, args.to_file, args.out_file, args.add_unexisted_records_from_sort, args.sort_out_file)
x.run()