# import importlib.util
# spec = importlib.util.spec_from_file_location("bpy", "/Applications/Blender.app/Contents/Resources/2.83/scripts/modules/bpy.py")
# bpy = importlib.util.module_from_spec(spec)
import bpy
import re
from enum import Enum
from bpy.types import Menu

bl_info = {
    "name": "single_quote",
    "author": "Hoang Duy Tran (hoangduytranuk)",
    "version": (0, 1),
    "blender": (2, 82, 0),
    "location": "Text editor > Format panel",
    "description": "Convert translation text to '<tran> -- <orig>'",
    "doc_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/"
        "Scripts/Text_Editor/hastebin",
    "tracker_url": "https://developer.blender.org/maniphest/task/edit/form/2/",
    "category": "Development"}

class InterfaceVars(bpy.types.PropertyGroup):
    op_types = bpy.props.EnumProperty(
        items=[
            ('grave_accent', '', 'Grave Accent', 'GA_BRACKETS', 0),
            ('arch_bracket', '', 'Arched Brackets', 'ARCH_BRACKETS', 1),
        ],
        default='arch_bracket',
    )

class TEXT_OT_single_quoted(bpy.types.Operator):
    """ 
    transform the selected text into single quoted text, 
    remove arched brackets, insert '--' to get it ready for
    abbreviation creation
    """
    bl_idname = "text.single_quoted_for_abbrev"
    bl_label = "Single Quoted"
    bl_description = "Convert selected text into single quoted text, remove all brackets and other symbols depend on option selected"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        # acceptable = TEXT_EDITOR # static const EnumPropertyItem active_theme_area[]
        is_editor_context = (context.area.type == 'TEXT_EDITOR')
        if not is_editor_context:
            return False
        else:
            has_text = (context.space_data.text is not None)
            return has_text

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
    def execute(self, context):
        sd = context.space_data
        # text = sd.text
        # sd.text.l
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

        op_type = context.window_manager.interface_vars
        # is_arched_bracket = (op_type == 'arch_bracket')
        # is_ga_bracket = (op_type == 'grave_accent')
        self.report({'INFO'}, f"op_type: {op_type}")

        # get the selected text
        text = self.getSelectedText(sd.text)
        if text is None:
            return {'CANCELLED'}
        
        # # # example: *bàn giao tiếp Python* (Python Console)
        # if self.getOpType() == OpType.SINGLE_QUOTE_FROM_ARCHED_BRACKETS:
        #     part_list = text.split(' (')
        # elif self.getOpType() == OpType.SINGLE_QUOTE_FROM_GA:
        #     part_list = text.split(' -- ')
        # else:
        #     part_list = text.split()

        # for index, part in enumerate(part_list):
        #     txt = part_list[index]
        #     if self.getOpType() == OpType.SINGLE_QUOTE_FROM_ARCHED_BRACKETS:
        #         txt = txt.replace('*', '')
        #         txt = txt.replace('(', '')
        #         txt = txt.replace(')', '')
        #     elif self.getOpType() == OpType.SINGLE_QUOTE_FROM_GA:
        #         txt = txt.replace('`', '')

        #     part_list[index] = txt

        # tran_part = part_list[0]
        # orig_part = part_list[1]
        # text = f"'{tran_part} -- {orig_part}'"
        # bpy.context.window_manager.clipboard = text
        # bpy.ops.text.paste()

        return {'FINISHED'}   

class TEXT_OT_abbrev_selected_panel(bpy.types.Panel):
    bl_label = "Single Quote Panel"
    bl_idname = "TEXT_OT_abbrev_selected_panel"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Text'

    def draw(self, context):
        lo = self.layout
        # obj = context.object

        # row.label(text='Perform', icon='WORLD_DATA')
        row = lo.row()
        row.prop(context.window_manager.interface_vars, 'grave_accent', expand=True)
        row.prop(context.window_manager.interface_vars, 'arch_bracket', expand=True)
        row.sepator()
        row = lo.row(align=True)
        row.operator("text.single_quoted_for_abbrev")

classes = (
    InterfaceVars,
    TEXT_OT_abbrev_selected_panel,
    TEXT_OT_single_quoted,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.interface_vars = bpy.props.PointerProperty(type=InterfaceVars)

def unregister():
    del bpy.types.WindowManager.interface_vars
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
