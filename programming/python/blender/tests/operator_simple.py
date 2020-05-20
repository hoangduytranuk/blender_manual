import bpy


#def main(context):
#    for ob in context.scene.objects:
#        print(ob)


class TextTransformABC(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.transform_abc"
    bl_label = "Tranform ABC"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(TextTransformABC)


def unregister():
    bpy.utils.unregister_class(TextTransformABC)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.TextTransformABC()
