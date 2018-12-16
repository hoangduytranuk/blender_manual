.. _bpy.types.DisplaceModifier:

*****************
Displace Modifier
*****************

The Displace Modifier displaces vertices in a mesh based on the intensity of a texture.
Either procedural or image textures can be used.
The displacement can be along a particular local axis, along the vertex normal,
or the separate RGB components of the texture can be used to displace vertices in the local X,
Y and Z directions simultaneously (sometimes referred to as *Vector Displacement*).


Options
=======

.. figure:: /images/modeling_modifiers_deform_displace_panel.png

   Displace Modifier.

Texture
   The name of the texture from which the displacement for each vertex is derived.
   If this field is empty, the modifier defaults to 1.0 (white).

Direction
   The direction along which to displace the vertices.
   Can be one of the following:

   X, Y, Z
      Displace along an axis.
   Normal
      Displace along the vertex normal.
   Custom Normal
      Displace along (averaged) :ref:`custom normals <modeling_meshes_normals_custom>`, instead of vertex normals.
   RGB to XYZ
      Displace along local XYZ axes individually using the RGB components of the texture
      (Red values displaced along the X axis, Green along the Y, Blue along the Z).
      This is sometimes referred to as *Vector Displacement*.
Space
   With a direction set to X, Y, Z, or XYZ the modifier can either displace along local or global axes.

Texture Coordinates
   The texture coordinate system to use when retrieving values from the texture for each vertex.
   Can be one of the following:

   UV
      Take texture coordinates from face UV coordinates.

      UV Map
         The UV map from which to take texture coordinates.
         If the object has no UV coordinates, it uses the *Local* coordinate system.
         If this field is blank, but there is a UV map available
         (e.g. just after adding the first UV map to the mesh),
         it will be overwritten with the currently active UV map.

      .. note::

         Since UV coordinates are specified per face, the UV texture coordinate system currently determines the UV
         coordinate for each vertex from the first face encountered which uses that vertex;
         any other faces using that vertex are ignored.
         This may lead to artifacts if the mesh has non-contiguous UV coordinates.

   Object
      Take the texture coordinates from another object's coordinate system (specified by the *Object* field).

      Object
         The object from which to take texture coordinates.
         Moving the object will therefore alter the coordinates of the texture mapping.

         Take note that moving the original object will **also** result in a texture coordinate update.
         As such, if you need to maintain a displacement coordinate system while moving the modified object,
         consider parenting the coordinate object to the modified object.

         If this field is blank, the *Local* coordinate system is used.

   Global
      Take the texture coordinates from the global coordinate system.
   Local
      Take the texture coordinates from the object's local coordinate system.

Vertex Group
   The name of a vertex group which is used to control the influence of the modifier.
   If left empty, the modifier affects all vertices equally.

Midlevel
   The texture value which will be treated as no displacement by the modifier.
   Texture values below this value will result in negative displacement along the selected direction,
   while texture values above this value will result in positive displacement.

   *displacement* = *texture_value* - *Midlevel*

   Recall that color/luminosity values are typically between (0.0 to 1.0) in Blender,
   and not between (0 to 255).

Strength
   The strength of the displacement. After offsetting by the *Midlevel* value,
   the displacement will be multiplied by the *Strength* value to give the final vertex offset.

   *vertex_offset* = *displacement* × *Strength*.

   A negative strength can be used to invert the effect of the modifier.


Example
=======

.. figure:: /images/modeling_modifiers_deform_displace_example-1.jpg
   :width: 680px

   Three different objects created with the Displace modifier.
   `Sample blend-file <https://en.blender.org/uploads/9/9e/Manual-Modifier-Displace-Example01.blend>`__.

.. figure:: /images/modeling_modifiers_deform_displace_example-2.jpg
   :width: 540px

   A slime animation created with the Displace modifier.
   `Sample blend-file <https://en.blender.org/uploads/6/62/Manual-Modifier-Displace-Slime01.blend>`__.
