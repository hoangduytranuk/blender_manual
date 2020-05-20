bl_info = {
    "name": "Add-on Template",
    "description": "",
    "author": "p2or",
    "version": (0, 0, 3),
    "blender": (2, 80, 0),
    "location": "3D View > Tools",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}


import bpy

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )


# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

class WM_OT_HelloWorld(Operator):
    bl_label = "Print Values Operator"
    bl_idname = "wm.hello_world"

    
    def execute(self, context):
        scene = context.scene
        rm_sep = scene.rm_sep
        rm_ga = scene.rm_ga
        rm_apos = scene.rm_ga
        rm_quote_mark = scene.rm_ga
        rm_left_paren = scene.rm_ga
        rm_right_paren = scene.rm_ga

        rm_dict={
            '\`':rm_ga,
            '\'':rm_apos,
            '\"':rm_quote_mark,
            '\(':rm_left_paren,
            '\)':rm_right_paren
        }

        print(f'rm_sep', rm_sep)
        for k, v in rm_dict.items():
            print(k, v)

        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Menus
# ------------------------------------------------------------------------

class OBJECT_MT_CustomMenu(bpy.types.Menu):
    bl_label = "Select"
    bl_idname = "OBJECT_MT_custom_menu"


    def draw(self, context):
        layout = self.layout

        # Built-in operators
        layout.operator("object.select_all", text="Select/Deselect All").action = 'TOGGLE'
        layout.operator("object.select_all", text="Inverse").action = 'INVERT'
        layout.operator("object.select_random", text="Random")

# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class OBJECT_PT_CustomPanel(Panel):
    bl_label = "My Panel"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = "TEXT_EDITOR"   
    bl_region_type = "UI"
    bl_category = "Text"
    bl_context = "space_data"   


    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Separator:")
        row = layout.row()
        row = layout.row(align=True)
        row.prop(context.scene, 'rm_sep', expand=True)

        layout.separator()
        row = layout.row()
        row.label(text="Removing Characters:")
        row = layout.row(align=True)
        row.prop(context.scene, 'rm_ga', toggle=True)
        row.prop(context.scene, 'rm_apos', toggle=True)
        row.prop(context.scene, 'rm_quote_mark', toggle=True)
        row.prop(context.scene, 'rm_left_paren', toggle=True)
        row.prop(context.scene, 'rm_right_paren', toggle=True)
        layout.operator("wm.hello_world")
        # layout.menu(OBJECT_MT_CustomMenu.bl_idname, text="Presets", icon="SCENE")
        # layout.separator()

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    WM_OT_HelloWorld,
    OBJECT_MT_CustomMenu,
    OBJECT_PT_CustomPanel
)


def register():
    def boolUpdate(self, context):
        pass
        # bpy.types.Scene.rm_ga = self.rm_ga
        # bpy.types.Scene.rm_apos = self.rm_apos
        # bpy.types.Scene.rm_quote_mark = self.rm_quote_mark
        # bpy.types.Scene.rm_left_paren = self.rm_left_paren
        # bpy.types.Scene.rm_right_paren = self.rm_right_paren
    
    
    
    bpy.types.Scene.rm_sep = EnumProperty(
        name='Separator',
        description='Separator to use to split abbreviation text and full explanation',
        items=[
           ('DBL_HYPHEN', "' -- '", ""),
           ('SPL_BRACKET', "' ('", ""),
           ]
    )

    bpy.types.Scene.rm_ga = BoolProperty(name = '`', description = 'Grave Accent', default = False, update=boolUpdate)
    bpy.types.Scene.rm_apos = BoolProperty(name = '\'', description = 'Apostrophe', default = False, update=boolUpdate)
    bpy.types.Scene.rm_quote_mark = BoolProperty(name = '"', description = 'Quotattion Mark', default = False, update=boolUpdate)
    bpy.types.Scene.rm_left_paren = BoolProperty(name = '(', description = 'Left Parenthesis', default = False, update=boolUpdate)
    bpy.types.Scene.rm_right_paren = BoolProperty(name = ')', description = 'Right Parenthesis', default = False, update=boolUpdate)

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    del bpy.types.Sene.rm_sep
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()