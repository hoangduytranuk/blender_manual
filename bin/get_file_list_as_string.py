#!/usr/bin/env python3
# import sys
# import os
# import re
# blend_man_path = os.environ['BLENDER_GITHUB']
# bin_path = os.path.join(blend_man_path, '/bin')
# sys.path.append(bin_path)

from argparse import ArgumentParser

try:
    parser = ArgumentParser()
    parser.add_argument("-f", "--from_file", dest="from_file", help="Files to process.")
    args = parser.parse_args()
    file_name = args.from_file
    with open(file_name, 'r') as f:
        line_list = f.readlines()

    if not line_list:
        print("")
        exit(0)

    uniq_list = list(sorted(set(line_list)))
    result_list=[]
    for line in uniq_list:
        if not line:
            continue
        result_list.append(line)

    total_lines = len(result_list)
    is_one_line = (total_lines == 1)
    is_two_line = (total_lines == 2)
    is_greater_than_two = (total_lines > 2)
    result_string=""

    is_two_or_greater = (is_two_line or is_greater_than_two)
    index_item_before_end = None
    index_item_end = (total_lines - 1)
    if is_two_or_greater:
        index_item_before_end = (total_lines-2)
    elif is_two_line:
        index_item_before_end = 0
    elif is_one_line:
        pass
    else:
        index_item_end = None

    for index, line in enumerate(result_list):
        line = line.strip()
        is_last_two_line = (index_item_before_end is not None) and (index >= index_item_before_end)
        if is_last_two_line:
            item_before_end = result_list[index_item_before_end].strip()
            item_end = result_list[index_item_end].strip()
            result_string += f"{item_before_end} and {item_end}"
            break
        elif is_one_line:
            result_string += f"{line}"
        else:
            result_string += f"{line}, "

    # this code works but is too complicated
    # for index, line in enumerate(result_list):
    #     line = line.strip()
    #     is_last_line = (index + 1 >= total_lines )
    #     if is_last_line:
    #         if is_one_line:
    #             result_string += line
    #         else:
    #             has_comma_ending = (result_string.endswith(", "))
    #             if has_comma_ending:
    #                 result_string = result_string[:-2]
    #                 result_string += " "
    #             result_string += f"and {line}"
    #     else:
    #         result_string += f"{line}"
    #         if is_greater_than_two:
    #             result_string += ", "
    #         else:
    #             result_string += " "
    print(result_string)
except Exception as e:
    pass