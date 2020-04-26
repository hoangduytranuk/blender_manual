# import importlib.util
# spec = importlib.util.spec_from_file_location("bpy", "/Applications/Blender.app/Contents/Resources/2.83/scripts/modules/bpy.py")
# bpy = importlib.util.module_from_spec(spec)
import bpy
import re
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

class TEXT_OT_abbrev_selected(bpy.types.Operator):
    """ 
    transform the selected text into single quoted text, 
    remove brackets, insert '--' to get it ready for
    abbreviation creation
    """
    bl_idname = "text.single_quoted_for_abbrev"
    bl_label = "Single Quoted"
    bl_description = "Convert selected text into single quoted text, remove all brackets, and 'filler' entries"
    
    @classmethod
    def poll(cls, context):
#        acceptable = TEXT_EDITOR # static const EnumPropertyItem active_theme_area[]
        is_editor_context = (context.area.type == 'TEXT_EDITOR')
        if not is_editor_context:
            return False
        else:
            has_text = (context.space_data.text is not None)
            return has_text

#    def execute(self, context):
#        obj = context.selected
#        print(f'selected [{obj}]')
#        current_context_type  = context.area.type 
#        print(f'My area is: {current_context_type}')        
#        return {'FINISHED'} 
    
# Cảnh Cáo: Selected text is: <bpy_collection[149], Text.lines>
# Cảnh Cáo: current_line: <bpy_struct, TextLine at 0x7f9e5a2aa178>
# Cảnh Cáo: current_line_index: 49
# Cảnh Cáo: select_end_line: <bpy_struct, TextLine at 0x7f9e5a2aa1a8>
# Cảnh Cáo: current_character: 21
# Cảnh Cáo: select_end_line_index: 50
# Cảnh Cáo: select_end_character: 19

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


        # get the selected text
        text = self.getSelectedText(sd.text)
        if text is None:
            return {'CANCELLED'}
        
        # # example: *bàn giao tiếp Python* (Python Console)
        part_list = text.split(' (')
        for index, part in enumerate(part_list):
            txt = part_list[index]
            txt = txt.replace('*', '')
            txt = txt.replace('(', '')
            txt = txt.replace(')', '')
            part_list[index] = txt

        tran_part = part_list[0]
        orig_part = part_list[1]
        text = f"'{tran_part} -- {orig_part}'"
        bpy.context.window_manager.clipboard = text
        bpy.ops.text.paste()

        # self.report({'WARNING'}, "Selected text is: %s." % (text))

        # new_text = self.get_set_text(text, is_replace=False)
        # self.report({'WARNING'}, "Selected text is: %s." % (new_text))
        # # bpy.context.window_manager.clipboard = text
        return {'FINISHED'}
    
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

class TEXT_OT_abbrev_selected_panel(bpy.types.Panel):
    bl_label = "Single Quote Panel"
    bl_idname = "TEXT_OT_abbrev_selected_panel"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Text'

    def draw(self, context):
        lo = self.layout
        # obj = context.object

        row = lo.row()
        # row.label(text='Perform', icon='WORLD_DATA')
        row.operator("text.single_quoted_for_abbrev")

classes = (
    TEXT_OT_abbrev_selected_panel,
    TEXT_OT_abbrev_selected,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == '__main__':
    register()
