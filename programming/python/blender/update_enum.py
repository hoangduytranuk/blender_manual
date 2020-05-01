import bpy

def update_enum(self, context):
    # self = current scene in an EnumProperty callback!
    print(self.my_enum)
    eval('bpy.ops.%s()' % self.my_enum)


class LayoutDemoPanel(bpy.types.Panel):
    bl_label = "Test"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

        layout.label(text="Enum prop")

        scene = context.scene
        layout.prop(scene, "my_enum", expand=True)


def register():
    bpy.utils.register_class(LayoutDemoPanel)

    bpy.types.Scene.my_enum = bpy.props.EnumProperty(
            name = "My enum",
            description = "My enum description",
            items = [
                ("mesh.primitive_cube_add", "Cube", "Create a cube"),
                ("mesh.primitive_uv_sphere_add", "Sphere", "Create a Sphere"),
            ],
            update=update_enum
        )

def unregister():
    bpy.utils.unregister_class(LayoutDemoPanel)

    bpy.types.Scene.my_enum


if __name__ == "__main__":
    register()