import bpy
from bpy.types import Operator
from bpy.props import BoolVectorProperty

class OBJECT_OT_move_to_layer2(Operator):
    """Move to Layer 2"""
    # class properties
    bl_idname = "object.move_to_layer2"
    bl_label = "Move to Layer [TESTING]"
    bl_options = {'REGISTER', 'UNDO'}

    event = None
    objects = []
    prev_sel = []

    # poll is a class method
    @classmethod
    def poll(self, context):
        return True

    def execute(self, context):
        ev = []
        event = self.event
        if event.ctrl:
            ev.append("Ctrl")
        if event.shift:
            ev.append("Shift")
        if event.alt:
            ev.append("Alt")
        if event.oskey:
            ev.append("OS")
        changed = [i for i, (l, s) in
                enumerate(zip(self.layers, self.prev_sel))
                if l != s]

        print("+".join(ev), event.type, event.value, changed)
        # pick only the changed one
        if not (event.ctrl or event.shift) and changed:
            self.layers = [i in changed for i in range(20)]
        self.prev_sel = self.layers[:]

        self.runMove(context)
        return {'FINISHED'}

    def check(self, context):
        return True # thought True updated.. not working

    def invoke(self, context, event):
        self.layers = [any(o.layers[i] for o in context.selected_objects)
                      for i in range(20)]
        self.event = event
        self.objects = [o.name for o in context.selected_objects]
        self.prev_sel = self.layers[:]
        return context.window_manager.invoke_props_popup(self, event)

    # properties

    layers = BoolVectorProperty(
        name="Layers",
        subtype="LAYER",
        description="Object Layers",
        size=20,
        )

    def runMove(self, context):
        for name in self.objects:
            obj = context.scene.objects.get(name)
            obj.layers = self.layers

def register():
    bpy.utils.register_class(OBJECT_OT_move_to_layer2)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_move_to_layer2_name)

if __name__ == "__main__":
    register()
    bpy.ops.object.move_to_layer2('INVOKE_DEFAULT')