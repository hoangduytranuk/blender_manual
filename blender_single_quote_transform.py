import bpy

class TEXT_OT_abbrev_selected(bpy.types.Operator):
    """ 
    transform the selected text into single quoted text, 
    remove brackets, insert '--' to get it ready for
    abbreviation creation
    """
    bl_idname = "text.single_quoted_for_abbrev"
    bl_label = "Single Quoted"
    
    def execute(self, context):
        
        return {'FINISHED'}
    
    @classmethod
    def poll(cls, context):
        current_context_type  = context.area.type 
        print(f'My area is: {current_context_type}')
        return True

def register():
    bpy.utils.register_class(TEXT_OT_abbrev_selected)

def unregister():
    bpy.utils.unregister_class(TEXT_OT_abbrev_selected)
    

if __name__ == '__main__':
    register()
