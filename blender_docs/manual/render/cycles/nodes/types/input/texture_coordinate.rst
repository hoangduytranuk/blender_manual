.. _bpy.types.ShaderNodeTexCoord:

***********************
Texture Coordinate Node
***********************

.. figure:: /images/render_cycles_nodes_types_input_texture-coordinate_node.png
   :align: right

   Texture Coordinate Node.

The *Texture Coordinate* node is commonly used for the coordinates of textures,
typically used as inputs for the *Vector* input for texture nodes.


Inputs
======

This node has no inputs.


Properties
==========

Object
   Specific object to use for object space coordinates.
   This only affects the *Object* output.

.. _cycles-nodes-input-texture-coordinate-from-dupli:

From Dupli
   If the material is applied to a dupli object, use texture coordinates from the parent object.
   This only affects the *Generated* and *UV* outputs.

   .. figure:: /images/render_cycles_nodes_types_input_texture-coordinate_from-dupli-comparison.png

      From left to right: Sphere with a UV-mapped texture.
      Small spheres duplicated to the faces of the textured sphere using
      :doc:`duplifaces </editors/3dview/object/properties/duplication/duplifaces>`.
      Small spheres with *From Dupli* enabled, using the UV map of the large sphere.

   .. note::

      *From Dupli* only works with the UV output when the dupli object is instanced from faces,
      either with :doc:`particles </physics/particles/introduction>` or
      :doc:`duplifaces </editors/3dview/object/properties/duplication/duplifaces>`.


Outputs
=======

Generated
   Automatically-generated texture coordinates from the vertex positions of the mesh without deformation,
   keeping them sticking to the surface under animation. Range from 0.0 to 1.0
   over the bounding box of the undeformed mesh. See :doc:`Generated UVs </editors/uv_image/uv/generated_uvs>`
   for more information.
Normal
   Object space normal, for texturing objects with the texture staying fixed on the object as it transformed.
   The Normal output can be used on Point and Spot lamps. The coordinates will take
   the rotation of the lamp into account.
UV
   UV texture coordinates from the active render UV map.
   See :ref:`UV Mapping <editors-uv-image-index>` for more information.

   .. note::

      In order to select UV map other than the active map you must use
      the :doc:`UV Map node </render/cycles/nodes/types/input/uv_map>`.
Object
   Uses an object as a source for coordinates. Often used with an *Empty*,
   this is an easy way to place a small image at a given point on the object.
   This object can also be animated, to move a texture around or through a surface.
Camera
   Position coordinate in camera space.
Window
   Location of shading point on the screen, ranging from 0.0 to 1.
   0 from the left to right side and bottom to top of the render.
   This is well suited for blending two objects.
Reflection
   Uses the direction of the reflection vector as coordinates.
   This is useful for adding reflection maps. You will need this input when using environment maps.
