#!/usr/bin/python3
#cython: language_level=3

from argparse import ArgumentParser
from printemty import PrintEmptyLine
from clearpo import ClearPO
from greppo import GrepPO
from translatepo import TranslatePO
from rmabbr import RemoveAbbr
from replace_msgstr import ReplaceMSGSTR
from updatedict import UpdateDict

# -tr -tran /Users/hoangduytran/Dev/tran/blender_ui/3x/vi.po -f /Users/hoangduytran/new_vi_mix_3_1_and_2_79_0001.po
# -f /Users/hoangduytran/retran_283.po -tr -fuz -o /Users/hoangduytran/retran_283_0001.po
# -tr -f /Users/hoangduytran/Dev/tran/blender_ui/3x/vi.po -tran /Users/hoangduytran/Dev/tran/blender_ui/merged.po -ig -cl

parser = ArgumentParser()
parser.add_argument("-f", "--from_file", dest="from_file", help="PO files to process.")
parser.add_argument("-of", "--out_file", dest="output_to_file", help="PO files to output listings to.")
parser.add_argument("-p", "--pattern", dest="pattern", help="Pattern use to search.")
parser.add_argument("-np", "--negate_pattern", dest="negate_pattern", help="Pattern use to negate the first search, ie. perform subtractions from the found set by --pattern option.")
parser.add_argument("-pid", "--pattern_id", dest="pattern_id", help="Pattern use to search in msgid.")
parser.add_argument("-npid", "--negate_pattern_id", dest="negate_pattern_id", help="Pattern use to negate the first search in msgid")
parser.add_argument("-cs", "--case_sense", dest="case_sensitive", help="define if case sensitive is needed", action='store_const', const=True)
parser.add_argument("-mid", "--msgid", dest="msgid", help="Search pattern perform on msgid", action='store_const', const=True)
parser.add_argument("-mstr", "--msgstr", dest="msgstr", help="Search pattern perform on msgstr", action='store_const', const=True)
parser.add_argument("-s", "--search", dest="searching", help="Searching function only", action='store_const', const=True)
parser.add_argument("-did", "--disp_msgid", dest="display_msgid", help="Display msgid along with msgstr. No effect of msgstr is not selected", action='store_const', const=True)
parser.add_argument("-dstr", "--disp_msgstr", dest="display_msgstr", help="Display msgstr along with msgid. No effect of msgid is not selected", action='store_const', const=True)
parser.add_argument("-cl", "--count_line", dest="count_number_of_lines", help="Count number lines and print out the line_count", action='store_const', const=True)
parser.add_argument("-ig", "--ignore", dest="filter_ignored", help="Filtering out ignored items", action='store_const', const=True)
parser.add_argument("-clr", "--clear", dest="clear_po", help="Clearing msgstr entries in the po files, also set no fuzzy", action='store_const', const=True)
parser.add_argument("-clrcmt", "--clear_comment", dest="clear_po_comment", help="Clearing the comments as well when performing clear_po option", action='store_const', const=True)
parser.add_argument("-mend", "--match_ends", dest="match_vipo_ends", help="Clearing msgstr entries in the po files, also set no fuzzy", action='store_const', const=True)
parser.add_argument("-tr", "--translate", dest="translate_po", help="translate given po file", action='store_const', const=True)
parser.add_argument("-tran", "--tran_file", dest="translation_file", help="File to take the translation from.")
parser.add_argument("-vf", "--validate_file", dest="validate_file", help="When printing empty lines, this file can be used to check if EMPTY entries exists in this file or not.")
parser.add_argument("-rmabbr", "--remove_abbr", dest="remove_abbreviations", help="Remove abbreviations from the translations in msgstr", action='store_const', const=True)
parser.add_argument("-rpl", "--replace_msgstr", dest="replace_msgstr", help="Replace MSGSTR", action='store_const', const=True)
parser.add_argument("-ext", "--extensions", dest="search_extensions", help="List of extensions to search for, separated by vertical bar '|', ie. '*.c|*.cpp|*.h'")
parser.add_argument("-fuz", "--set_fuzzy", dest="set_translation_fuzzy", help="Set changed entry of translation to fuzzy, so can check for its accuracy later", action='store_const', const=True)
parser.add_argument("-mcase", "--match_case", dest="apply_case_matching_orig_txt", help="Apply case matching with msgid when obtain translation from dictionary", action='store_const', const=True)
parser.add_argument("-updict", "--update_dict", dest="update_dictionary", help="Update dictionary", action='store_const', const=True)

args = parser.parse_args()

is_grep_po = (True if args.searching else False)
is_clearing=(True if args.clear_po else False)
is_translating=(True if args.translate_po else False)
is_remove_abbr = (True if args.remove_abbreviations else False)
is_replace_msgstr = (True if args.replace_msgstr else False)
is_update_dictionary = (True if args.update_dictionary else False)

# ReplaceMSGSTR
if is_clearing:
        x = ClearPO(
                input_file=args.from_file,
                output_to_file=args.output_to_file,
                clear_po_comment=args.clear_po_comment
        )
elif is_grep_po:
        x = GrepPO(
                input_file=args.from_file,
                output_to_file=args.output_to_file,
                pattern=args.pattern,
                negate_pattern=args.negate_pattern,
                pattern_id=args.pattern_id,
                negate_pattern_id=args.negate_pattern_id,
                is_case_sensitive=args.case_sensitive,
                is_msgid=args.msgid,
                is_msgstr=args.msgstr,
                is_display_msgid=args.display_msgid,
                is_display_msgstr=args.display_msgstr,
                filter_ignored=args.filter_ignored,
                search_extensions=args.search_extensions
        )
elif is_translating:
        x = TranslatePO(
                input_file=args.from_file,
                output_to_file=args.output_to_file,
                translation_file=args.translation_file,
                set_translation_fuzzy=args.set_translation_fuzzy,
                apply_case_matching_orig_txt=args.apply_case_matching_orig_txt
        )
elif is_remove_abbr:
        x = RemoveAbbr(
                input_file=args.from_file,
                output_to_file=args.output_to_file
        )
elif is_replace_msgstr:
        x = ReplaceMSGSTR(
                input_file=args.from_file,
                output_to_file=args.output_to_file
        )
elif is_update_dictionary:
        x = UpdateDict(
                input_file=args.from_file,
                output_to_file=args.output_to_file,
                translation_file=args.translation_file,
                set_translation_fuzzy=args.set_translation_fuzzy,
                apply_case_matching_orig_txt=args.apply_case_matching_orig_txt
        )
else:
        x = PrintEmptyLine(
                input_file=args.from_file,
                output_to_file=args.output_to_file,
                validate_file=args.validate_file,
                is_msgstr=args.display_msgstr
                )

x.count_number_of_lines = (True if args.count_number_of_lines else False)
x.filter_ignored = (True if args.filter_ignored else False)

x.performTask()
# -s -dmid -mstr -p "Delta" -of /Users/hoangduytran/test_0001.po
# -tr -f /Users/hoangduytran/Dev/tran/blender_ui/3x/vi.po -tran /Users/hoangduytran/Dev/tran/blender_ui/merged.po -ig -cl

