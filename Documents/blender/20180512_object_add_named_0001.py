import bpy

x = (1.1,2.2,3.3,4.4)
y = (1.1,2.2,3.3,4.4)
z = (1.1,2.2,3.3,4.4)

#requires an object of with the below refereenced name has already been added
for index,val in enumerate(x):
#    bpy.ops.object.add(type='EMPTY', location=(x[index],y[index],z[index]))
    bpy.ops.object.add_named(linked=False, name="Cube")
