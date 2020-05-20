bl_info = {
    "name": "tester",
    "description": "",
    "author": "poor",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "UV/Image Editor > Tool Shelf (T)",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Test"
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
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )


# ------------------------------------------------------------------------
#    Store properties in the active scene
# ------------------------------------------------------------------------

class MySettings(PropertyGroup):

    my_bool : BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default = False
        )

    my_int : IntProperty(
        name = "Set a value",
        description="A integer property",
        default = 23,
        min = 10,
        max = 100
        )

    my_float : FloatProperty(
        name = "Set a value",
        description = "A float property",
        default = 23.7,
        min = 0.01,
        max = 30.0
        )

# ------------------------------------------------------------------------
#    My Tool in the image editor
# ------------------------------------------------------------------------

class UV_PT_my_panel(Panel):
    bl_idname = "UV_PT_my_panel"
    bl_label = "My Tool"
    bl_category = "My Category"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        # display the properties
        layout.prop(mytool, "my_bool", text="Bool Property")
        layout.prop(mytool, "my_int", text="Integer Property")
        layout.prop(mytool, "my_float", text="Float Property")

        # check if bool property is enabled
        if (mytool.my_bool == True):
            print ("Property Enabled")
        else:
            print ("Property Disabled")


# ------------------------------------------------------------------------
#     Registration
# ------------------------------------------------------------------------

classes = (
    MySettings,
    UV_PT_my_panel,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.my_tool = PointerProperty(type=MySettings)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()