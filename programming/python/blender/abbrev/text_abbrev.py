import sys
sys.path.append('/Users/hoangduytran/blender_manual/potranslate')

import re
import bpy
from bpy.types import Menu

from pprint import pprint as pp
from enum import Enum

from reflink import RefList, RefRecord, RefItem
from ignore import Ignore as ig
from common import Common as cm
from translate_po import trans_finder


from bpy.props import (
    BoolProperty,
    BoolVectorProperty,
    CollectionProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
    IntProperty,
    IntVectorProperty,
    PointerProperty,
    RemoveProperty,
    StringProperty
)
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )


bl_info = {
    "name": "text_abbreviation",
    "author": "Hoang Duy Tran (hoangduytranuk)",
    "version": (0, 1),
    "blender": (2, 82, 0),
    "location": "Text editor > Format panel",
    "description": "Convert translation text to '<tran> -- <orig>'",
    "doc_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"
    "Scripts/Text_Editor/hastebin",
    "tracker_url": "https://developer.blender.org/maniphest/task/edit/form/2/",
    "category": "Development"}

# def enum_members_from_type(rna_type, prop_str):
#     prop = rna_type.bl_rna.properties[prop_str]
#     return [e.identifier for e in prop.enum_items]

# def enum_members_from_instance(rna_item, prop_str):
#     return enum_members_from_type(type(rna_item), prop_str)

sep_table = (
    ('SP_DBL_HYPH_SP', '" -- "', ' Space Hyphen Space', 0),
    ('SP_ARCH_BRK', '" ("', 'Space Left Bracket', 1),
    ('SP_SPACE', '" "', 'Space',2),
)

rm_sym_list = ["`", "*", "'", "\"", "\\", "(", ")", "<", ">", "-"]
blanking_id = re.compile(r'\:[^\:]+\:')
blanking_hyphen = re.compile(r'[-]+')
dbl_quote_pat = re.compile(r'[\"]+')

case_status_table = (
    ('UPPER', 'Upper', 'Upper case', 1),
    ('LOWER', 'Lower', 'Lower case', 2),
    ('TITLE', 'Titled', 'Title Case', 3),
    ('FIRST', 'Cap First', 'First letter capitalised', 4),
)

find_replace_option_table = [
    ("Regular Expression", 'FREEZE'),
    ("Match Case", 'SYNTAX_OFF'),
    ("Whole Word", 'OUTLINER_OB_FONT'),
    ("Wrap Round", 'DECORATE_OVERRIDE'),
    ("Inselection", 'RESTRICT_INSTANCED_ON'),
    ("HighLight Matches", 'INDIRECT_ONLY_ON'),
]

# :MM:
# :abbr:
# :class:
# :doc:
# :guilabel:
# :kbd:
# :linenos:
# :math:
# :menuselection:
# :minute:
# :mod:
# :ref:
# :sup:
# :term:

ref_table = (
    ('NONE', '', 'None fill prefix', 0),
    ('ABBR', ':abbr:', 'Abbreviations', 1),
    ('CLASS', ':class:', 'Classes', 2),
    ('DOC', ':doc:', 'Documentations', 3),
    ('GUILBL', ':guilabel:', 'GUI labels', 4),
    ('KBD', ':kbd:', 'Keyboards', 5),
    ('LINENOS', ':linenos:', 'Line numbers', 6),
    ('MATH', ':math:', 'Maths', 7),
    ('MNUSEL', ':menuselection:', 'Menu selections', 8),
    ('MIN', ':minute:', 'Minutes', 9),
    ('MOD', ':mod:', 'Modules', 10),
    ('REF', ':ref:', 'References', 11),
    ('SUP', ':sup:', 'Supplements', 12),
    ('TERM', ':term:', 'Terms', 13),
)

# show_enum_values(bpy.context.scene.transform_orientation_slots[0], 'type')
# show_enum_values(bpy.context.object, 'mode')


class MySettings(PropertyGroup):

    is_reversed: BoolProperty(
        name="Reverse",
        description="Reverse Terms or not",
        default=False,
    )

    def ref_type_callback(self, context):
        return ref_table

    ref_type: EnumProperty(
        items=ref_type_callback,
        name='Ref type',
        description='Ref type to prefix',
        default=None,
    )

    def updateAbbrev(self, context):
        is_all_on = (self.is_abbrev) and (self.is_kbd or self.is_term)
        if is_all_on:
            self.is_term = False
            self.is_kbd = False

    is_abbrev: BoolProperty(
        name="Abbrev",
        description="Create Abbrev",
        default=False,
        update=updateAbbrev
    )

    def updateTerm(self, context):
        is_all_on = (self.is_term) and (self.is_kbd or self.is_abbrev)
        if is_all_on:
            self.is_abbrev = False
            self.is_kbd = False

    is_term: BoolProperty(
        name="Term",
        description="Create Term",
        default=False,
        update=updateTerm
    )

    def updateKBD(self, context):
        is_all_on = (self.is_kbd) and (self.is_abbrev or self.is_term)
        if is_all_on:
            self.is_abbrev = False
            self.is_term = False

    is_kbd: BoolProperty(
        name="Kbd",
        description="Create Kbd",
        default=False,
        update=updateKBD
    )

    is_matching_case: BoolProperty(
        name="Matching Case",
        description="Matching the case of translation with the original",
        default=False,
    )

    def updateSeparator(self, context):
        sep_id = self['term_sep']
        entry = sep_table[sep_id]
        id, txt, _, _ = entry
        chosen_separator = txt.strip('"')
        print(f'chosen_separator:[{chosen_separator}]')

    def term_sep_callback(self, context):
        return sep_table

    term_sep: EnumProperty(
        items=term_sep_callback,
        name='Term Separator',
        description='Separator to split terms with',
        default=None,
        update=updateSeparator
    )

    rm_chars: BoolVectorProperty(
        name='Removing Characters',
        description='Table for characters to be removed from selected text',
        size=len(rm_sym_list),
    )

    filler_char: BoolVectorProperty(
        name='Head/Tail Filler',
        description='Table for characters to be filled at head/tail of parts',
        size=len(rm_sym_list),
    )

    filler_count: IntProperty(
        name="Filler Count",
        description="Number of filler character instances",
        default=1,
        min=0,
        soft_min=0,
        soft_max=5
    )

    def updateRmCharSelectAll(self, context):
        for i, _ in enumerate(self.rm_chars):
            # print(f'self.rm_char_select_all:[{self.rm_char_select_all}]')
            self.rm_chars[i] = self.rm_char_select_all

    rm_char_select_all: BoolProperty(
        name="(De)Select All",
        description="Select All Removing Characters",
        default=False,
        update=updateRmCharSelectAll
    )

    rm_redundant_hyphen: BoolProperty(
        name="Remove Hyphens",
        description="Remove redundant hyphens characters after split",
        default=False,
    )

    braket_to_square: BoolProperty(
        name="Square Brackets",
        description="Replacing other brakets to squares, good for abbreviations",
        default=False,
    )

    # cases ====================================
    def case_status_callback(self, context):
        return case_status_table

    case_status: EnumProperty(
        items=case_status_callback,
        name='Type',
        description='Converting selected text to different case types',
    )

    # replace ==================================
    find_string: StringProperty(
        name="Find",
        description="String to find",
        default="",
    )

    replace_string: StringProperty(
        name="Replace",
        description="String to replace",
        default="",
    )

    find_replace_options: BoolVectorProperty(
        name='Options',
        description='Find and replace options',
        size=len(find_replace_option_table),
    )

    find_rep_RE: BoolProperty(
        name="Regular Expression",
        description="Allowing regular expression",
        default=False,
    )

    # ("Regular Expression", 'FREEZE'),
    # ("Match Case", 'SYNTAX_OFF'),
    # ("Whole Word", 'OUTLINER_OB_FONT'),
    # ("Wrap Round", 'DECORATE_OVERRIDE'),
    # ("Inselection", 'RESTRICT_INSTANCED_ON'),
    # ("HighLight Matches", 'INDIRECT_ONLY_ON'),

    find_rep_RE: BoolProperty(
        name="Regular Expression",
        description="Allowing regular expression",
        default=False,
    )
    find_rep_match_case: BoolProperty(
        name="Case Sensitive",
        description="Sensitive to UPPER, lower and mix cases",
        default=False,
    )
    find_rep_whole_word: BoolProperty(
        name="Whole Word",
        description="Whole world matching only.",
        default=False,
    )
    find_rep_wrap_round: BoolProperty(
        name="Wrap Round",
        description="Wrap round when performing find, ie. back to top if reached the bottom.",
        default=False,
    )
    find_rep_in_selection: BoolProperty(
        name="In Selection",
        description="Find and replace within the selected area only.",
        default=False,
    )
    find_rep_highlight_matches: BoolProperty(
        name="Highlight Matches",
        description="Find and replace within the selected area only.",
        default=False,
    )

    removing_marker: BoolProperty(
        name="Remove Marker",
        description="Removing :<something>: in the text.",
        default=False,
    )


class TEXT_OT_single_quoted_base(bpy.types.Operator):
    """
    transform the selected text into single quoted text,
    remove arched brackets, insert '--' to get it ready for
    abbreviation creation
    """
    # bl_idname = "text.single_quoted_for_abbrev_base"
    # bl_label = "Abbreviation"
    bl_description = "Convert selected text into single quoted text, remove all brackets and other symbols depend on option selected"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):
        self.is_reverse = False
        self.is_abbrev = True
        self.previous_text = ""

    # def replaceSelectedText(self, context, new_text):
    #     sd = context.space_data
    #     text = sd.text

        # current_line = text.current_line
        # select_end_line = text.select_end_line

        # current_character = text.current_character
        # select_end_character = text.select_end_character

        # is_selection_on_the_same_line = (current_line == select_end_line)
        # if is_selection_on_the_same_line:
        #     left_part = current_line.body[:start]
        #     right_part = current_line.body[end:]
        #     current_line.body = left_part + text + right_part
        #     sd.text =

    # taken this block from release/scripts/addons_contrib/text_editor_hastebin.py
    def getSelectedText(self, text):
        """"""
        current_line = text.current_line
        select_end_line = text.select_end_line

        current_character = text.current_character
        select_end_character = text.select_end_character

        # if there is no selected text return None
        if current_line == select_end_line:
            if current_character == select_end_character:
                return None
            else:
                start = min(current_character, select_end_character)
                end = max(current_character, select_end_character)
                return current_line.body[start: end]

        text_return = None
        writing = False
        normal_order = True  # selection from top to bottom

        for line in text.lines:
            if not writing:
                if line == current_line:
                    text_return = current_line.body[current_character:] + "\n"
                    writing = True
                    continue
                elif line == select_end_line:
                    text_return = select_end_line.body[select_end_character:] + "\n"
                    writing = True
                    normal_order = False
                    continue
            else:
                if normal_order:
                    if line == select_end_line:
                        text_return += select_end_line.body[:select_end_character]
                        break
                    else:
                        text_return += line.body + "\n"
                        continue
                else:
                    if line == current_line:
                        text_return += current_line.body[:current_character]
                        break
                    else:
                        text_return += line.body + "\n"
                        continue

        return text_return

  # taken this block from /Applications/Blender.app/Contents/Resources/2.83/scripts/addons_contrib/text_editor_hastebin.py
    def setReverse(self, is_reverse):
        self.is_reverse = is_reverse

    def setAbbrev(self, is_abbrev):
        self.is_abbrev = is_abbrev

    def restoreClibboardPreviousCopy(self):
        bpy.context.window_manager.clipboard = self.previous_text

    def pasteText(self, text_to_paste):

        self.previous_text = bpy.context.window_manager.clipboard

        bpy.context.window_manager.clipboard = text_to_paste
        bpy.ops.text.paste()

    def execute(self, context):
        sd = context.space_data

        sc = context.scene
        var = sc.my_tool
        is_reverse = var.is_reversed  # making use of ready made boolean
        is_abbrev = var.is_abbrev  # making use of ready made boolean
        is_term = var.is_term  # making use of ready made boolean
        is_kbd = var.is_kbd
        sep = var.term_sep
        is_matching_case_with_original = var.is_matching_case
        prefix_type = var.ref_type

        # get the selected text
        text = self.getSelectedText(sd.text)
        if text is None:
            return {'CANCELLED'}

        chosen_term_sep_id = var.term_sep
        chosen_sep = None
        for i, sep_entry in enumerate(sep_table):
            id, sep_text, _, _ = sep_entry
            found = (id == chosen_term_sep_id)
            if found:
                chosen_sep = sep_text.strip('"')
                break

        print(f'chosen_sep:[{chosen_sep}]')
        part_list = text.split(chosen_sep)
        print(f'part_list:[{part_list}]')

        has_parts = (len(part_list) > 1)
        if not has_parts:
            self.report({'ERROR'}, f"String did NOT SPLIT: {part_list}")
            return {'CANCELLED'}

        tran_part = part_list[0]
        orig_part = part_list[1]

        rm_char_list = var.rm_chars
        chosen_chars = []
        for i, rm_selected in enumerate(rm_char_list):
            if rm_selected:
                chosen_chars.append(rm_sym_list[i])
        chosen_blanking_chars = "".join(chosen_chars)

        filler_char_list = var.filler_char
        chosen_filler_chars = []
        for i, filler_selected in enumerate(filler_char_list):
            if filler_selected:
                # using the same list a remove symbols
                chosen_filler_chars.append(rm_sym_list[i])
        chosen_filler_chars = "".join(chosen_filler_chars)

        filler_count = var.filler_count
        filler_list = []
        for char in chosen_filler_chars:
            filler_list.append(f'{char * filler_count}')
        filler = "".join(filler_list)

        # updateRmChars(var, context)
        is_blanking_id = var.removing_marker
        print(f'is_blanking_id:{is_blanking_id}')
        if is_blanking_id:
            # clean out any ':something:' groups
            orig_part = blanking_id.sub("", orig_part)
            # clean out any ':something:' groups
            tran_part = blanking_id.sub("", tran_part)

        is_bracket_to_square = var.braket_to_square
        if is_bracket_to_square:
            orig_part = orig_part.replace('(', '[')
            orig_part = orig_part.replace(')', ']')
            tran_part = tran_part.replace('(', '[')
            tran_part = tran_part.replace(')', ']')

        print(f'chosen_blanking_chars:[{chosen_blanking_chars}]')
        is_blanking_char = (chosen_blanking_chars is not None) and (
            len(chosen_blanking_chars) > 0)
        if is_blanking_char:
            for c in chosen_blanking_chars:
                # print(f'character:[{c}], text:[{text}]')
                orig_part = orig_part.replace(c, "")
                tran_part = tran_part.replace(c, "")

        print(f'orig_part:[{orig_part}], tran_part:[{tran_part}]')

        is_blanking_hyphen = var.rm_redundant_hyphen
        if is_blanking_hyphen:
            tran_part = blanking_hyphen.sub("", tran_part)
            orig_part = blanking_hyphen.sub("", orig_part)

        has_filler = (len(filler) > 0)
        if has_filler:
            tran_part = f'{filler}{tran_part}{filler}'
            orig_part = f'{filler}{orig_part}{filler}'

        tran_has_quote = (dbl_quote_pat.search(tran_part) is not None)
        if tran_has_quote:
            tran_part = tran_part.replace('"', '\\"')

        orig_has_quote = (dbl_quote_pat.search(orig_part) is not None)
        if orig_has_quote:
            orig_part = orig_part.replace('"', '\\"')

        print(f'orig_part:[{orig_part}], tran_part:[{tran_part}]')
        # return {'CANCELLED'}

#        text = "Một đường tham chiếu định nghĩa các tọa độ dọc theo một hướng hợp quy trong không gian *đa chiều (n-D) -- (n-Dimensions)*"

#        print(f'before:[{text}]')
#        text = blanking_pat.sub("", text)
        # print(f'done:[{text}]')
        # return {'CANCELLED'}

        # for sep in sep_list:
        #     if sep in text:
        #         part_list = text.split(sep)
        #         break

        # if part_list is None:
        #     return {'CANCELLED'}

        # print(f'just brokup: [{part_list}]')
        # for index, _ in enumerate(part_list):
        #     txt = part_list[index]
        #     txt = blanking_id.sub("", txt)
        #     txt = blanking_pat.sub("", txt)
        #     part_list[index] = txt

        if is_matching_case_with_original:
            # matching cases to original
            if orig_part.isupper():
                tran_part = tran_part.upper()
            elif orig_part.islower():
                tran_part = tran_part.lower()
            elif orig_part.istitle():
                tran_part = tran_part.title()

        prefix_type = self.getPrefixType(context)
        # strip all spaces surrounding text before inserting into the template
        text = self.textPrefix(orig_part, tran_part, prefix_type, is_reverse)
        # return {'CANCELLED'}
        self.pasteText(text)
        return {'FINISHED'}

# ref_table = (
#     ('NONE', '', 'None fill prefix', 0),
#     ('ABBR', ':abbr:', 'Abbreviations', 1),
#     ('CLASS', ':class:', 'Classes', 2),
#     ('DOC', ':doc:', 'Documentations', 3),
#     ('GUILBL', ':guilabel:', 'GUI labels', 4),
#     ('KBD', ':kbd:', 'Keyboards', 5),
#     ('LINENOS', ':linenos:', 'Line numbers', 6),
#     ('MATH', ':math:', 'Maths', 7),
#     ('MNUSEL', ':menuselection:', 'Menu selections', 8),
#     ('MIN', ':minute:', 'Minutes', 9),
#     ('MOD', ':mod:', 'Modules', 10),
#     ('REF', ':ref:', 'References', 11),
#     ('SUP', ':sup:', 'Supplements', 12),
#     ('TERM', ':term:', 'Terms', 13),
# )

    def getPrefixText(self, prefix_type):
        prefix_text = ""
        for index, prefix_entry in enumerate(ref_table):
            type, prefix, _, _ = prefix_entry
            is_found = (prefix_type == type)
            if is_found:
                prefix_text = prefix
                break

        return prefix_text

    def getPrefixType(self, context):
        sc = context.scene
        var = sc.my_tool
        prefix_type = var.ref_type

        return prefix_type

    def textPrefix(self, orig_part, tran_part, prefix_type, is_reverse):

        hyphen = ['DOC', 'GUILBL', 'REF', 'TERM']
        bracket = ['KBD', 'ABBR']

        if prefix_type in hyphen:
            text = self.textHyphen(orig_part, tran_part, is_reverse)
        elif prefix_type in bracket:
            text = self.textBracket(orig_part, tran_part, is_reverse)
        else:
            text = self.textSame(orig_part, tran_part, is_reverse)

        text = text.strip()

        prefix_text = self.getPrefixText(prefix_type)
        print(f'before {prefix_type} => prefix_text:{prefix_text} text:{text}')
        is_none_ref = (prefix_text == "")
        if is_none_ref:
            text = f"{text}"
        else:
            text = f"{prefix_text}`{text}`"

        print(f'after {prefix_type} => prefix_text:{prefix_text} text:{text}')
        return text

    def textHyphen(self, orig_part, tran_part, is_reverse):
        if is_reverse:
            text = f"{orig_part} -- {tran_part}"
        else:
            text = f"{tran_part} -- {orig_part}"
        print(f'hyphen => text:{text}')
        return text

    def textBracket(self, orig_part, tran_part, is_reverse):
        if is_reverse:
            text = f"{orig_part} ({tran_part})"
        else:
            text = f"{tran_part} ({orig_part})"
        print(f'bracket => text:{text}')
        return text

    def textSame(self, orig_part, tran_part, is_reverse):
        if is_reverse:
            text = f"{orig_part} {tran_part}"
        else:
            text = f"{tran_part} {orig_part}"
        print(f'textSame => text:{text}')
        return text

class TEXT_OT_single_quoted_forward(TEXT_OT_single_quoted_base):
    bl_idname = "text.single_quoted_for_abbrev"
    bl_label = "Abbreviation"

    def execute(self, context):
        self.setReverse(False)
        result = super(TEXT_OT_single_quoted_forward, self).execute(context)
        return result

    def invoke(self, context, event):
        result = self.execute(context)
        self.restoreClibboardPreviousCopy()
        return result

class TEXT_OT_find_forward(TEXT_OT_single_quoted_base):
    bl_idname = "text.find_forward"
    bl_label = "Forward"
    bl_description = "Find forward"
    bl_context = 'scene'

    def execute(self, context):
        sd = context.space_data
        text = self.getSelectedText(sd.text)
        if text is None:
            return {'CANCELLED'}
        return {'FINISHED'}

    def invoke(self, context, event):
        result = self.execute(context)
        self.restoreClibboardPreviousCopy()
        return result


class TEXT_OT_find_backward(TEXT_OT_single_quoted_base):
    bl_idname = "text.find_backward"
    bl_label = "Backward"
    bl_description = "Find backward"
    bl_context = 'scene'

    def execute(self, context):
        sd = context.space_data
        text = self.getSelectedText(sd.text)
        if text is None:
            return {'CANCELLED'}
        return {'FINISHED'}

    def invoke(self, context, event):
        result = self.execute(context)
        self.restoreClibboardPreviousCopy()
        return result


class TEXT_OT_find_replace(TEXT_OT_single_quoted_base):
    bl_idname = "text.find_replace"
    bl_label = "Replace"
    bl_description = "Replace with options"
    bl_context = 'scene'

    def execute(self, context):
        sd = context.space_data
        text = self.getSelectedText(sd.text)
        if text is None:
            return {'CANCELLED'}
        return {'FINISHED'}

    def invoke(self, context, event):
        result = self.execute(context)
        self.restoreClibboardPreviousCopy()
        return result


class TEXT_OT_case_conversion(TEXT_OT_single_quoted_base):
    bl_idname = "text.case_conversion"
    bl_label = "Change Case"
    bl_description = "Convert selected text to match case option"
    bl_context = 'scene'

    def execute(self, context):
        sd = context.space_data
        text = self.getSelectedText(sd.text)
        if text is None:
            return {'CANCELLED'}

        scene = context.scene
        my_tool = scene.my_tool

        case = my_tool.case_status
        print(f'case:{case}')
        if case == 'UPPER':
            text = text.upper()
        elif case == 'LOWER':
            text = text.lower()
        elif case == 'TITLE':
            text = text.title()
        elif case == 'FIRST':
            text = text[0].upper() + text[1:].lower()
        else:
            return {'CANCELLED'}

        print(f'converted: [{text}]')
        self.pasteText(text)
        return {'FINISHED'}

class TEXT_OT_parse_sentence(TEXT_OT_single_quoted_base):
    bl_idname = "text.parse_sentence"
    bl_label = "Parse Sentence"
    bl_description = "Capture and parse sentence automatically"
    bl_context = 'scene'

    def execute(self, context):
        sd = context.space_data
        text = self.getSelectedText(sd.text)
        if text is None:
            return {'CANCELLED'}

        part_list = text.split(': "')
        has_parts = (len(part_list) > 0)
        if not has_parts:
            print('Text is not splitting, requiring dictionary like format!')
            return {'CANCELLED'}

        orig_msg = part_list[0]
        orig_msg = orig_msg.strip('"')

        tran_msg = part_list[1]
        tran_msg = tran_msg.strip('"')
        tran_msg = tran_msg.strip('",')

        k = orig_msg
        v = tran_msg

        ref_list = RefList(msg=v)
        new_v = ref_list.quotedToAbbrev(k)

        text = f'"{k}": "{new_v}",'

        print(f'converted text: [{text}]')
        self.pasteText(text)
        return {'FINISHED'}

    def invoke(self, context, event):
        result = self.execute(context)
        self.restoreClibboardPreviousCopy()
        return result

class TEXT_OT_paste_join(TEXT_OT_single_quoted_base):
    bl_idname = "text.paste_join_abbrev"
    bl_label = "Paste Join"
    bl_description = "Paste the previously copied content, and join with currently selected text"
    bl_context = 'scene'

    def execute(self, context):
        sd = context.space_data

        sc = context.scene
        var = sc.my_tool
        is_reverse = var.is_reversed  # making use of ready made boolean

        orig_part = bpy.context.window_manager.clipboard
        has_orig = len(orig_part) > 0
        if not has_orig:
            self.report({'ERROR'}, f"Must select a text for original part and copy to clipboard")
            return {'CANCELLED'}

        tran_part = self.getSelectedText(sd.text)
        if tran_part is None:
            self.report({'ERROR'}, f"Must select a text for translation part")
            return {'CANCELLED'}

        prefix_type = self.getPrefixType(context)
        text = self.textPrefix(orig_part, tran_part, prefix_type, is_reverse)
        self.pasteText(text)
        return {'FINISHED'}

    def invoke(self, context, event):
        result = self.execute(context)
        self.restoreClibboardPreviousCopy()
        return result

class TEXT_OT_paste_with_colon(TEXT_OT_single_quoted_base):
    bl_idname = "text.paste_with_colon"
    bl_label = "Paste With Colon"
    bl_description = "Paste the previously copied content, adding colon at the end 'text:'"
    bl_context = 'scene'

    def execute(self, context):
        sd = context.space_data

        sc = context.scene
        var = sc.my_tool
        is_reverse = var.is_reversed  # making use of ready made boolean
        orig_part = bpy.context.window_manager.clipboard
        has_orig = len(orig_part) > 0
        if not has_orig:
            self.report({'ERROR'}, f"Must select a text for original part and copy to clipboard")
            return {'CANCELLED'}

        text = f"{orig_part}: "
        self.pasteText(text)
        return {'FINISHED'}

    def invoke(self, context, event):
        result = self.execute(context)
        self.restoreClibboardPreviousCopy()
        return result

class TEXT_OT_convert_to_square_bracket(TEXT_OT_single_quoted_base):
    bl_idname = "text.convert_to_square_brackets"
    bl_label = "Square Bracketing"
    bl_description = "Convert arched brackets of selected text to square brackets"
    bl_context = 'scene'

    def execute(self, context):
        sd = context.space_data

        # sc = context.scene
        # var = sc.my_tool
        # is_reverse = var.is_reversed  # making use of ready made boolean
        text = self.getSelectedText(sd.text)
        if not text:
            self.report({'ERROR'}, f"Must select a text with arched brackets to be converted")
            return {'CANCELLED'}

        text = text.replace('(', '[')
        text = text.replace(')', ']')
        self.pasteText(text)
        return {'FINISHED'}

    def invoke(self, context, event):
        result = self.execute(context)
        self.restoreClibboardPreviousCopy()
        return result

class TEXT_PT_abbrev_selected_panel(bpy.types.Panel):
    bl_label = "Abbreviation Panel"
    bl_idname = "TEXT_PT_abbrev_selected_panel"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Text'

    def draw(self, context):
        lo = self.layout

        scene = context.scene
        my_tool = scene.my_tool

        lo.label(text='Options:')
        # col = lo.column(align=True)
        row = lo.row(align=True)

        # making use of ready made boolean
        row.prop(my_tool, "is_reversed", text="Rev.",
                 icon='FILE_REFRESH', toggle=True)
        # making use of ready made boolean
        row = lo.row(align=True)
        row.prop(my_tool, "ref_type")

        # row.prop(my_tool, "is_abbrev", toggle=True)
        # # making use of ready made boolean
        # row.prop(my_tool, "is_term", toggle=True)
        # row.prop(my_tool, "is_kbd", toggle=True)
        row = lo.row(align=True)
        row.prop(my_tool, "is_matching_case")

#        lo.label(text='Separator:')
        row = lo.row(align=True)
        row.label(text='Separator:')
        row.prop(my_tool, "term_sep", expand=True)

        # lo.label(text='Removing Characters:')
        box = lo.box()
        split = box.split(factor=1, align=True)
        col = split.column()
        col.label(text='Removing:')
        for i in range(0, len(rm_sym_list)):
            if i % 3 == 0:
                row = col.row(align=True)
            row.prop(my_tool, "rm_chars", index=i,
                     text=rm_sym_list[i], toggle=True)
        row.prop(my_tool, "removing_marker", text=":aaa:", toggle=True)

        row = col.row(align=True)
        # row = lo.row(align=True)
        row.prop(my_tool, "rm_char_select_all")

        col = split.column()
        box = lo.box()
        split = box.split(factor=1, align=True)
        col = split.column()
        col.label(text='Head/Tail Filler:')
        for i in range(0, len(rm_sym_list)):
            if i % 3 == 0:
                row = col.row(align=True)
            row.prop(my_tool, "filler_char", index=i,
                     text=rm_sym_list[i], toggle=True)
        row = col.row(align=True)
        row.prop(my_tool, "filler_count")

        split = lo.split()
        col = split.column(align=True)
        col.label(text="Extra Options:")
        col.prop(my_tool, "rm_redundant_hyphen")
        col.prop(my_tool, "braket_to_square")

        col = split.column(align=True)
        col.label(text="Case Conversion:")
        row = col.row(align=True)
        row.prop(my_tool, "case_status", expand=True)
        # lo.operator_menu_enum("case_status", "type")
        col.separator()
        col.operator("text.case_conversion", icon='SYNTAX_OFF')
        # row = col.row(align=True)
        # row = lo.row(align=True)

        col = lo.column(align=True)
        row = col.row(align=True)
        row.operator("text.convert_to_square_brackets", icon='TRACKER_DATA')
        row.operator("text.single_quoted_for_abbrev", icon='LOOP_FORWARDS')
        row.operator("text.parse_sentence", icon='MODIFIER_DATA')

        row = col.row(align=True)
        row.operator("text.cut")
        row.operator("text.copy", icon='COPYDOWN')
        row.operator("text.save", icon='FILE_TICK')

        row = col.row(align=True)
        row.operator("text.paste", icon='PASTEDOWN')
        row.operator("text.paste_join_abbrev", icon='PASTEDOWN')
        row.operator("text.paste_with_colon", icon='PASTEDOWN')


'''
        box = lo.box()
        split = box.split(factor=1, align=True)
        col = split.column(align=True)
        col.label(text="Find & Replace:")
        col.prop(my_tool, "find_string")
        col.prop(my_tool, "replace_string")
        col.separator()

#        row.label(text="Options:")
#        box = col.box()
#        row = col.row(align=True)
        row = col.grid_flow(align=True)
        row.prop(my_tool, "find_rep_RE", icon='GHOST_ENABLED', toggle=True, icon_only=True)
        row.prop(my_tool, "find_rep_match_case", icon='SYNTAX_OFF', toggle=True, icon_only=True)
        row.prop(my_tool, "find_rep_whole_word", icon='SHADING_WIRE', toggle=True, icon_only=True)
        row.prop(my_tool, "find_rep_wrap_round", icon='DECORATE_OVERRIDE', toggle=True, icon_only=True)
        row.prop(my_tool, "find_rep_in_selection", icon='OBJECT_DATAMODE', toggle=True, icon_only=True)
        row.prop(my_tool, "find_rep_highlight_matches", icon='SELECT_EXTEND', toggle=True, icon_only=True)

        row = col.row(align=True)
        row.operator("text.find_forward", icon='SORT_ASC')
        row.operator("text.find_backward", icon='SORT_DESC')
        row.operator("text.find_replace", icon='OUTLINER_OB_MESH')

        # for i in range(0, len(find_replace_option_table)):
        #     text_id, icon_id = find_replace_option_table[i]
        #     row.prop(my_tool, "find_replace_options", index=i,
        #              text="", icon=icon_id, expand=True, icon_only=True)
'''


classes = (
    MySettings,
    TEXT_OT_find_forward,
    TEXT_OT_find_backward,
    TEXT_OT_find_replace,
    TEXT_PT_abbrev_selected_panel,
    TEXT_OT_single_quoted_forward,
    TEXT_OT_case_conversion,
    TEXT_OT_parse_sentence,
    TEXT_OT_paste_join,
    TEXT_OT_paste_with_colon,
    TEXT_OT_convert_to_square_bracket,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.my_tool = PointerProperty(type=MySettings)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.my_tool


if __name__ == '__main__':
    register()

# bpy.ops.text. single_quoted_for_abbrev()
