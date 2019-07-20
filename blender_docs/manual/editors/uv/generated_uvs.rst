
*************
Generated UVs
*************

.. _properties-texture-space:
.. _bpy.types.*texspace:
.. _bpy.types.Mesh.texture_mesh:
.. _bpy.types.Curve.use_uv_as_generated:
.. _bpy.ops.curve.match_texture_space:

Properties
==========

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Panel:     :menuselection:`Properties editor --> Object Data --> Texture Space`

These are settings of the :term:`texture space` used by generated texture mapping.
The visualization of the texture space can be activated in the :doc:`/scene_layout/object/properties/display`.

Auto Texture Space
   Adjusts the active object's texture space automatically when transforming the object.

   Location, Size
      If the texture space is not calculated automatically then you can define
      the location and size of the texture space relative to the base object.
      These can also be adjusted from the 3D View, see `Editing`_ for more information.

------------------------

Texture Mesh
   Use another mesh for texture indices, the vertex of the two objects must be perfectly aligned.
   otherwise the UV map will be distorted. Note that, this is only for mesh objects.
Use UV for Mapping
   Use UV values as generated texture coordinates. Note that, this is only for curve objects.
Match Texture Space
   Modifies the *Location* and *Size* to match the objects bounding box.
   This disables Auto Texture Space. Note that, this is only for curve objects.

   .. is Match Texture Space the same thing as Auto Texture Space?


.. _properties-texture-space-editing:

Editing
=======

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode and Edit Mode
   :Menu:      :menuselection:`Object --> Transform --> Scale/Move Texture Space`

To modify the texture space from the 3D View, enable
:ref:`Edit Texture Space <modeling_transform_edit-texture-space>`
while :doc:`transforming </scene_layout/object/editing/transform/basics>` an object.


Accessing
=========

The automatically calculated UV map can be accessed by an object's material through
the *Generated* output of the :doc:`/render/shader_nodes/input/texture_coordinate`.
This output can then be used to map any texture onto an object.

.. tip::

   Generated texture spaces do not have rotation support, to overcome this,
   a :doc:`/render/shader_nodes/vector/mapping` can be used to rotate the UV map.
