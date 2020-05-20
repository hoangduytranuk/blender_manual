import bpy
import re
from pprint import pprint as pp
from enum import Enum
from bpy.types import Menu
from bpy.props import (
                        StringProperty, 
                        BoolProperty, 
                        IntProperty, 
                        FloatProperty, 
                        EnumProperty,
                        PointerProperty,
                        FloatVectorProperty,
                        )

from bpy.types import (
                        Panel,
                        Menu,
                        Operator,
                        PropertyGroup,
                        WindowManager,
                    )
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

class MyProperties(PropertyGroup):

    my_bool: BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default = False
        )

    my_int: IntProperty(
        name = "Int Value",
        description="A integer property",
        default = 23,
        min = 10,
        max = 100
        )

    my_float: FloatProperty(
        name = "Float Value",
        description = "A float property",
        default = 23.7,
        min = 0.01,
        max = 30.0
        )

    my_float_vector: FloatVectorProperty(
        name = "Float Vector Value",
        description="Something",
        default=(0.0, 0.0, 0.0), 
        min= 0.0, # float
        max = 0.1
    ) 

    my_string: StringProperty(
        name="User Input",
        description=":",
        default="",
        maxlen=1024,
        )

    my_path: StringProperty(
        name = "Directory",
        description="Choose a directory:",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
        )

    my_enum: EnumProperty(
        name="Dropdown:",
        description="Apply Data to attribute.",
        items=[ ('OP1', "Option 1", ""),
                ('OP2', "Option 2", ""),
                ('OP3', "Option 3", ""),
               ]
        )
            
class TEXT_OT_base(Operator):
    """ 
    transform the selected text into single quoted text, 
    remove arched brackets, insert '--' to get it ready for
    abbreviation creation
    """
    bl_idname = "text.TEXT_OT_base"
    bl_label = "Text Transform Base"
    bl_description = "Convert selected text into single quoted text, remove all brackets and other symbols depend on option selected"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        # acceptable = TEXT_EDITOR # static const EnumPropertyItem active_theme_area[]
        return True
        is_editor_context = (context.area.type == 'TEXT_EDITOR')
        if not is_editor_context:
            return False
        else:
            has_text = (context.space_data.text is not None)
            return has_text

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

class TEXT_OT_abbrev(TEXT_OT_base):
    """ 
    transform the selected text into single quoted text, 
    remove arched brackets, insert '--' to get it ready for
    abbreviation creation
    """
    bl_idname = "text.abbrev_for_selected_text"
    bl_label = "Abbreviation Conversion"
    bl_description = "Convert selected text into single quoted text, remove all brackets and other symbols depend on option selected"
    bl_context = "space_data"
    bl_options = {'REGISTER', 'UNDO'}


  # taken this block from /Applications/Blender.app/Contents/Resources/2.83/scripts/addons_contrib/text_editor_hastebin.py
    def execute(self, context):
        st = context.space_data
        
        # get the selected text
        text = self.getSelectedText(sd.text)
        if text is None:
            return {'CANCELLED'}

        # # # example: *bàn giao tiếp Python* (Python Console)
        part_list = text.split(' (')        
        for index, part in enumerate(part_list):
            txt = part_list[index]
            txt = re.sub(r'\*', '', txt)
            txt = re.sub(r'\(', '', txt)
            txt = re.sub(r'\)', '', txt)
            part_list[index] = txt

        tran_part = part_list[0]
        orig_part = part_list[1]
        text = f":abbr:`'{tran_part}' ('{orig_part}')`"
        bpy.context.window_manager.clipboard = text
        bpy.ops.text.paste()

        return {'FINISHED'}   


class TEXT_PT_abbrev_panel(Panel):
    bl_label = "Single Quote Convert Panel"
    bl_idname = "TEXT_PT_abbrev_selected_panel"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Text'
    bl_context = "space_data"
    
    def draw(self, context):
        layout = self.layout
        st = context.space_data
        mytool = st.hoangduytran_tool

        row = layout.row()

        layout.prop(mytool, "my_bool")
        layout.prop(mytool, "my_enum", text="") 
        layout.prop(mytool, "my_int")
        layout.prop(mytool, "my_float")
        layout.prop(mytool, "my_float_vector", text="")
        layout.prop(mytool, "my_string")
        layout.prop(mytool, "my_path")
        
        layout.separator()
        row = layout.row()

        row.operator("text.abbrev_for_selected_text")


classes = (
    MyProperties,
    TEXT_OT_abbrev,
    TEXT_PT_abbrev_panel
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Space.hoangduytran_tool = PointerProperty(type=MyProperties)

def unregister():
    del bpy.types.Space.my_tool
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == '__main__':
    register()

