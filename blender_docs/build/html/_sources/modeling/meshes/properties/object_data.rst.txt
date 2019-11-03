
***********
Object Data
***********

Meshes
   The mesh :ref:`Data-Block Menu <ui-data-block>` can be used to link the data between objects.


Vertex Groups
=============

Vertex groups can be used to assign a group or weighted group to some operator.
An object can have several weight groups and can be assigned in
:doc:`Weight Paint </modeling/meshes/properties/vertex_groups/vertex_groups>` mode,
or in :doc:`Edit Mode </modeling/meshes/properties/vertex_groups/assigning_vertex_group>` via this panel.

See :doc:`Vertex Groups </modeling/meshes/properties/vertex_groups/index>` for more information.


Shape Keys
==========

Shape Keys can be used to transform one shape into another.
See :doc:`/animation/shape_keys/shape_keys_panel` for more information.


UV Maps
=======

UV Maps are used to map a 3D object onto a 2D plane that determines where a texture appears on the 3D object.
Different UV Maps can be used for different textures. For more information see :ref:`uv-maps-panel`.


Vertex Colors
=============

Color data can be applied directly to an object's vertices rather than using a texture or a material.
Colors can are painted onto vertices in :doc:`Vertex Paint </sculpt_paint/vertex_paint/index>` mode.


.. _bpy.types.FaceMaps:
.. _bpy.ops.object.face_map:

Face Maps
=========

Face Maps create custom gizmos to deform meshes by assigning faces to *Face Maps*.
Face Maps can be used to rig quickly within object mode and without making complicated rigging setups.
Face Maps are currently not fully implemented in Blender and require add-ons to take full advantage of this feature.

.. seealso::

   `Auto Face Map Widgets add-on <https://developer.blender.org/diffusion/BAC/browse/master/object_facemap_auto/>`__


Normals
=======

In geometry, a normal is a direction or line that is perpendicular to something,
typically a triangle or surface but can also be relative to a line, a tangent line for a point on a curve,
or a tangent plane for a point on a surface. Normals help to determine the shading of the mesh among other things.

See :ref:`Normal Properties <modeling_meshes_editing_normals_properties>` for more information.


Texture Space
=============

Each Object can have an automatically generated UV map, these maps can be adjusted here.

See :ref:`Generated UV Properties <properties-texture-space>` for more information.


Geometry Data
=============

Mesh objects can have different types of custom data attached to them.
This data is mostly used internally and can be exported by some :doc:`exporters </files/import_export>`.
See :doc:`/modeling/meshes/properties/custom_data` for more information.
