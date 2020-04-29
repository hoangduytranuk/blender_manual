import bpy
import math
 
class InterfaceVars(bpy.types.PropertyGroup):
    angles = bpy.props.EnumProperty(
        items=[
            ('15', '15', '15', '', 0),
            ('30', '30', '30', '', 1),
            ('60', '60', '60', '', 2),
            ('90', '90', '90', '', 3),
            ('120', '120', '120', '', 4),
        ],
        default='15'
    )
    direction = bpy.props.EnumProperty(
        items=[
            ('cw', '', 'CW', 'LOOP_FORWARDS', 0),
            ('ccw', '', 'CCW', 'LOOP_BACK', 1)
        ],
        default='cw'
    )
    
class Rotation(bpy.types.Operator):
    bl_idname = "object.rotation"
    bl_label = "Rotate"
 
    def execute(self, context):
        rotationvalue = int(context.window_manager.interface_vars.angles)
        if context.window_manager.interface_vars.direction == 'ccw':
            rotationvalue = -rotationvalue
        bpy.ops.transform.rotate(value=rotationvalue*math.pi/180, axis=(0, 0, 1)) 
        return {'FINISHED'}
 
class RotationPanel(bpy.types.Panel):
    bl_idname = "object.rotationpanel"
    bl_label = "RotationPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "RotationPanel"
 
    def draw(self, context):
        row = self.layout.row()
        row.prop(context.window_manager.interface_vars, 'angles', expand=True)
        row.prop(context.window_manager.interface_vars, 'direction', expand=True)
        self.layout.operator("object.rotation", text="Rotate")
    
def register():
    bpy.utils.register_class(Rotation)
    bpy.utils.register_class(RotationPanel)
    bpy.utils.register_class(InterfaceVars)
    bpy.types.WindowManager.interface_vars = bpy.props.PointerProperty(type=InterfaceVars)
    
def unregister():
    del bpy.types.WindowManager.interface_vars
    bpy.utils.unregister_class(InterfaceVars)
    bpy.utils.unregister_class(RotationPanel)
    bpy.utils.unregister_class(Rotation)
    
if __name__ == "__main__":
    register()