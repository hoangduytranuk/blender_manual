        def preparse():
            parsed_entries = []
            # remain_to_be_parsed = str(self.msg)
            # preparsing, just get location, text, type, pattern parsed
            for index, item in enumerate(pattern_list):
                importance_level = index
                p, ref_type = item
                is_bracket = (ref_type == RefType.ARCH_BRACKET)
                if is_bracket:
                    found_dict = cm.getTextWithinBrackets('(', ')', self.sl_txt, is_include_bracket=False)
                else:
                    found_dict = cm.patternMatchAll(p, self.sl_txt)
                for loc, mm in found_dict.items():
                    m_loc, found_text = mm.getOriginAsTuple()
                    entry = (importance_level, m_loc, found_text, ref_type, p)
                    parsed_entries.append(entry)
            return parsed_entries

        def removeDuplicates(parsed_l):
            def checkSingleEntry(current_entry):
                imp_lev, loc_c, text_c, ref_type_c, pat_c = current_entry
                changed = False
                for parsed_entry in keep_list:
                    imp_lev, loc_p, text_p, ref_type_p, pat_p = parsed_entry
                    is_ignore = (loc_p == loc_c)
                    if is_ignore:
                        continue

                    is_ovrlap = cm.isOverlappedLoc(loc_p, loc_c)
                    if not is_ovrlap:
                        continue

                    A = parsed_entry
                    B = current_entry

                    changed = True
                    del_list.append(parsed_entry)

                    result_dict = cm.subtractText(loc_p, text_p, loc_c, text_c)
                    for loc, txt in result_dict.items():
                        new_entry = (loc, txt, ref_type_p, pat_p)
                        keep_list.append(new_entry)
                return changed

            del_list=[]
            keep_list = copy(parsed_l)
            for entry in parsed_l:
                changed = checkSingleEntry(entry)
                if not changed:
                    keep_list.append(entry)
                else:
                    for del_entry in del_list:
                        del keep_list[del_entry]
                    del_list = []
            return keep_list

        parsed_list = preparse()
        nondup_list = removeDuplicates(parsed_list)
        count_item = len(nondup_list)


    def filteringParsedEntries(self, parsed_list):
        def checkOverlapped(current_entry: RefRecord):
            overlap_list=[]
            old_entry:RefRecord = None
            for old_entry in loc_list:
                is_ovrlap = current_entry.isOverLapped(old_entry)
                if not is_ovrlap:
                    continue
                is_already_in_list = (old_entry in overlap_list)
                if not is_already_in_list:
                    overlap_list.append(old_entry)

                is_already_in_list = (current_entry in overlap_list)
                if not is_already_in_list:
                    overlap_list.append(current_entry)

                has_the_pair = (len(overlap_list) == 2)
                if has_the_pair:
                    break

            return overlap_list

        keep_list=[]
        loc_list=[]
        c_ref_record: RefRecord = None
        for current_entry in parsed_list:
            (c_loc, c_cover_length), c_ref_record = current_entry
            ovrlap_list = checkOverlapped(c_ref_record)
            if not ovrlap_list:
                loc_list.append(c_ref_record)
                continue
            rec_1 = ovrlap_list[0]
            rec_2 = ovrlap_list[2]
            rec_bigger = (rec_1 if rec_1 >= rec_2 else rec_2)
            rec_smaller = (rec_2 if rec_2 <= rec_1 else rec_1)
            result_sub = rec_bigger - rec_smaller
            print(f'result_sub')
        return loc_list
