import bpy
from bpy.props import StringProperty, EnumProperty

class ImportDataBaseConnection(bpy.types.Operator):
    bl_idname = "importgis.database_connection" 
    bl_description = 'Import Geometry Data'
    bl_label = "Geometry"

    host : StringProperty(options={'HIDDEN'})
    port : StringProperty(options={'HIDDEN'})
    database : StringProperty(options={'HIDDEN'})
    username : StringProperty(options={'HIDDEN'})
    password : StringProperty(options={'HIDDEN'})

    def item_callback(self, context):
        return (
            ('NONE', 'None', "Flat geometry"),
            ('GEOM', 'Geometry', "Use z value from shape geometry if exists"),
            ('FIELD', 'Field', "Extract z elevation value from an attribute field"),
            ('OBJ', 'Object', "Get z elevation value from an existing ground mesh"),
        )

    geo_type : EnumProperty(
        items=item_callback,
        name="Geometry Type",
        description="choose a geometry",
        default=None,
        options={'ANIMATABLE'},
        update=None,
        get=None,
        set=None)

    def execute(self, context):
        message = "Connection"
        self.report({'INFO'}, message)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=500)


def register():
    bpy.utils.register_class(ImportDataBaseConnection)


def unregister():
    bpy.utils.unregister_class(ImportDataBaseConnection)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.importgis.database_connection('INVOKE_DEFAULT')