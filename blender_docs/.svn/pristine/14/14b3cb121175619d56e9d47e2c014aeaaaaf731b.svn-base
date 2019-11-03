.. _bpy.types.ShaderNodeMapping:

************
Mapping Node
************

The *Mapping Node* is used to transform an image or procedural texture.
For example, you can use it to move, rotate, or scale textures.
If you have ever done any UV editing in the past, then you will likely know
that these can also be accomplished by modifying an object's UVs
in the :doc:`UV editor </editors/uv/index>`. However,
it is sometimes useful to have easy access to these functions through
nodes rather than having to modify the UVs. One example of this might be
when you have several textures, each of which needs to be transformed
individually e.g. decals on an object.

.. figure:: /images/render_shader-nodes_vector_mapping_node.png

   Mapping node.


Inputs
======

Vector
   Vector to be transformed, usually this is input from
   a :doc:`Texture Coordinate node </render/shader_nodes/input/texture_coordinate>`.


Properties
==========

Vector type
   Allows the user to choose which vector type to use.

   Texture
      This is the most common option that you will use and will be sufficient for most cases.
   Point
      This works similar to *Texture* but the way the math works
      the *Scale* values are divided rather than multiplied.
   Vector
      Behaves the same as *Point* mode but changes in *Location*
      are ignored -- that is, the texture does not move.
   Normal
      Transforms a normal vector with unit length.

Location
   Vector translation.
Rotation
   Rotation of the vector along the XYZ axes.
Scale
   Scale of the vector, in *Point* and *Vector* modes, a value of 2.0 will halve the texture size,
   while in *Texture* mode the size is double.

Min/Max
   Normalizes the *Location*, *Rotation*,
   and *Scale* values to fit within the specified XYZ values.


Outputs
=======

Vector
   Transformed vector, usually gets connected to some sort of
   :doc:`Texture node </render/shader_nodes/textures/index>`.


Examples
========

Todo <2.8 add.
