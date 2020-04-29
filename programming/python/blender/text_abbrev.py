import bpy
import re
from enum import Enum
from bpy.types import Menu

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

def enum_members_from_type(rna_type, prop_str):
    prop = rna_type.bl_rna.properties[prop_str]
    return [e.identifier for e in prop.enum_items]

def enum_members_from_instance(rna_item, prop_str):
    return enum_members_from_type(type(rna_item), prop_str)

sep_table = (
        ('SP_DBL_HYPH_SP', '" -- "', 'Desc',0),
        ('SP_ARCH_BRK', '" ("', 'Desc',1),
        ('RESERVED', 'Reserved', 'Reserved Item',2),
    )

rm_sym_list = ["`", "*", "'", "\"", "\\", "(", ")", "<", ">", "-"]

# show_enum_values(bpy.context.scene.transform_orientation_slots[0], 'type')
# show_enum_values(bpy.context.object, 'mode')

class MySettings(PropertyGroup):

    is_reversed : BoolProperty(
        name="Reverse",
        description="Reverse Terms or not",
        default = False
        )

    is_abbrev : BoolProperty(
        name="Abbrev",
        description="Create Abbrev",
        default = False
        )

    is_term : BoolProperty(
        name="Term",
        description="Create Term",
        default = False
        )

    is_reserved : BoolProperty(
        name="Reserved",
        description="A reserved instance",
        default = False
        )


    def term_sep_callback(self, context):
        return sep_table
        # return (
        #     ('SP_DBL_HYPH_SP', '" -- "', 'Desc',0),
        #     ('SP_ARCH_BRK', '" ("', 'Desc',1),
        #     ('RESERVED', 'Reserved', 'Reserved Item',2),
        # )
    
    term_sep : EnumProperty(
        items=term_sep_callback,
        name='Term Separator',
        description='Separator to split terms with',
        default=None
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
                start = min(current_character,select_end_character)
                end = max(current_character,select_end_character)
                return current_line.body[start: end]

        text_return = None
        writing = False
        normal_order = True # selection from top to bottom

        for line in text.lines:
            if not writing:
                if line == current_line:
                    text_return = current_line.body[current_character:] + "\n"
                    writing = True
                    continue
                elif line == select_end_line:
                    text_return =  select_end_line.body[select_end_character:] + "\n"
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

  # taken this block from /Applications/Blender.app/Contents/Resources/2.83/scripts/addons_contrib/text_editor_hastebin.py
    def setReverse(self, is_reverse):
        self.is_reverse = is_reverse

    def setAbbrev(self, is_abbrev):
        self.is_abbrev = is_abbrev

    def execute(self, context):
        sd = context.space_data

        sc = context.scene
        var = sc.my_tool
        is_reverse = var.is_reversed # making use of ready made boolean
        is_abbrev = var.is_abbrev # making use of ready made boolean
        is_term = var.is_term # making use of ready made boolean
        sep = var.term_sep

        print(f'is_reverse: [{is_reverse}]')
        print(f'is_abbrev: [{is_abbrev}]')
        print(f'is_term: [{is_term}]')
        print(f'sep: [{sep}]')
        # sep_tbl = [
        #     ('SP_DBL_HYPH_SP', ' -- '),
        #     ('SP_ARCH_BRK', ' (')
        # ]
        
        # text = 'one -- two, and three (four)'
        # for sp_item, pat in sep_tbl:
        #     if sep == sp_item:
        #         print(f'found the [{sp_item}] [{pat}]')
        #         found_list = pat.findall(text)
        #         print(f'found_list:{found_list}')
        # return {'CANCELLED'}
        # is_reverse = sc.tag # making use of ready made boolean
        # is_abbrev = sc.show_subframe # making use of ready made boolean
        # is_term = sc.use_audio # making use of ready made boolean

        # text = sd.text
        # sd.text -- something and (something else)
        # self.report({'WARNING'}, f"Selected text is: {text.lines}")
        # self.report({'WARNING'}, f"current_line: {text.current_line}")
        # self.report({'WARNING'}, f"current_line_index: {text.current_line_index}")

        # self.report({'WARNING'}, f"select_end_line: {text.select_end_line}")
        # self.report({'WARNING'}, f"current_character: {text.current_character}")
        # self.report({'WARNING'}, f"select_end_line_index: {text.select_end_line_index}")
        # self.report({'WARNING'}, f"select_end_character: {text.select_end_character}")
        # print('my name is Hoang Duy Tran')
        # for index, line in enumerate(text.lines):
        #     line_length = len(line)
        #     print(f'index:[{index}], len:[{line_length}], text:[{line}]')

        # get the selected text
        text = self.getSelectedText(sd.text)
        if text is None:
            return {'CANCELLED'}
        
        # sep_list = [
        #     " -- ",
        #     " (",
        # ]

        # sample: "Một đường tham chiếu định nghĩa các tọa độ dọc theo một hướng hợp quy trong không gian *đa chiều (n-D) -- (n-Dimensions)*",

        blanking_pat = re.compile(r'[\`\*\'\"\\\(\)\-\<\>]+')
        blanking_id = re.compile(r'\:[^\:]+\:')

        part_list=None
        # ('SP_DBL_HYPH_SP', '" -- "', 'Desc',0),
        for index, item in enumerate(sep_table):
            id, sp, _, _ = item

            print(f'id: [{id}], sp:[{sp}]')
            if sep == id:
                sp = sp.strip('"')
                print(f'found sp: [{sp}]')
                part_list = text.split(sp)
                break

        print(f'part_list: [{part_list}]')
        return {'CANCELLED'}
        # for sep in sep_list:
        #     if sep in text:
        #         part_list = text.split(sep)
        #         break
        
        if part_list is None:
            return {'CANCELLED'}
        
        print(f'just brokup: [{part_list}]')
        for index, _ in enumerate(part_list):
            txt = part_list[index]
            txt = blanking_id.sub("", txt)
            txt = blanking_pat.sub("", txt)
            part_list[index] = txt
            
        print(f'replaced symbols: [{part_list}]')
        
        tran_part = part_list[0]
        orig_part = part_list[1]
        
        # matching cases to original
        if orig_part.isupper():
            tran_part = tran_part.upper()
        elif orig_part.islower():
            tran_part = tran_part.lower()
        elif orig_part.istitle():
            tran_part = tran_part.title()

        if is_term:
            if is_reverse:
                text = f"{orig_part} -- {tran_part}"
            else:
                text = f"{tran_part} -- {orig_part}"
        else:
            if is_reverse:
                text = f"{orig_part} ({tran_part})"
            else:
                text = f"{tran_part} ({orig_part})"
        
        # strip all spaces surrounding text before inserting into the template
        text = text.strip()
        if is_term:
            text = f":term:`{text}`"
        elif is_abbrev:
            text = f":abbr:`{text}`"

        bpy.context.window_manager.clipboard = text
        bpy.ops.text.paste()
        return {'FINISHED'}   

class TEXT_OT_single_quoted_forward(TEXT_OT_single_quoted_base):
    bl_idname = "text.single_quoted_for_abbrev"
    bl_label = "Abbreviation"
    def execute(self, context):        
        self.setReverse(False)
        result = super(TEXT_OT_single_quoted_forward, self).execute(context)
        return result

class TEXT_OT_single_quoted_reverse(TEXT_OT_single_quoted_base):
    bl_idname = "text.single_quoted_for_abbrev_reverse"
    bl_label = "Abbreviation Reverse Terms"

    def execute(self, context):        
        self.setReverse(True)
        result = super(TEXT_OT_single_quoted_reverse, self).execute(context)
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
        row.prop(my_tool, "is_reversed", text="Rev.", icon='FILE_REFRESH', toggle=True) # making use of ready made boolean
        row.prop(my_tool, "is_abbrev", toggle=True) # making use of ready made boolean
        row.prop(my_tool, "is_term", toggle=True) # making use of ready made boolean

        lo.label(text='Separator:')
        row = lo.row(align=True)        
        row.prop(my_tool, "term_sep", expand=True)
        
        # row = lo.row(align=True)
        col = lo.column(align=True)
        col.operator("text.single_quoted_for_abbrev", icon='LOOP_FORWARDS')
        # col.operator("text.single_quoted_for_abbrev_reverse", icon='LOOP_BACK')

classes = (
    MySettings,
    TEXT_PT_abbrev_selected_panel,
    TEXT_OT_single_quoted_forward,
    # TEXT_OT_single_quoted_reverse
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