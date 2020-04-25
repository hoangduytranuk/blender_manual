import bpy
import bmesh

context = bpy.context

distance = 0.0 # remove doubles tolerance.
meshes = [o.data for o in context.selected_objects if o.type == 'MESH']

bm = bmesh.new()

for m in meshes:
    bm.from_mesh(m)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=distance)
    bm.to_mesh(m)
    m.update()
    bm.clear()

77bm.free()