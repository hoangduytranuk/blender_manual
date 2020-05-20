import bpy
from bpy.props import BoolVectorProperty, BoolProperty

def flag_all(self, context):
    for i, flag in enumerate(self.flags):
        self.flags[i] = self.flag_all
    return None

bpy.types.Scene.flags = BoolVectorProperty(size=4)
flag_names = []
i = 0
while i < 4:
    flag_names.append("flag%d" % i)
    i += 1

bpy.types.Scene.flag_all = BoolProperty(update=flag_all)

class HelloWorldPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Hello World Panel"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        row = layout.row()
        row.prop(scene, "flag_all", text="SELECT ALL")
        row = layout.row(align=True)
        for i,name in enumerate(flag_names):
            
            row.prop(scene, "flags", index=i, text=name, toggle=True)


def register():
    bpy.utils.register_class(HelloWorldPanel)


def unregister():
    bpy.utils.unregister_class(HelloWorldPanel)


if __name__ == "__main__":
    register()