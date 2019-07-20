.. _bpy.types.WarpModifier:

*************
Warp Modifier
*************

The *Warp* modifier can be used to warp parts of a mesh to a new location in
a very flexible way, by using two objects to select the "from" and "to" regions,
with options for using a curve falloff, texture and/or vertex group.

.. figure:: /images/modeling_modifiers_deform_warp_example.png
   :align: center

   A Warp modifier applied to a grid mesh.

This modifier is a bit tricky to understand at first.
It requires two points, specified by the two target objects' origins.
The "from" point designates a point in space that is pulled toward the "to" point.
It is akin to using
the :doc:`Proportional Editing </scene_layout/object/editing/transform/control/proportional_edit>` in Edit Mode.


Options
=======

.. figure:: /images/modeling_modifiers_deform_warp_panel.png
   :align: right

   The Warp modifier.

From
   The object defining the origin transformation of the warp.
To
   The object defining the destination transformation of the warp.
Preserve Volume
   Enables volume preservation when rotating one of the transforms.
Strength
   Sets how strong the effect is.
Radius
   Sets the distance from the transforms that can be warped by the transform handles.
Falloff Type
   Sets the way the strength of the warp change as it goes from the center of the transform to the *Radius* value.
   See :doc:`Proportional Editing </scene_layout/object/editing/transform/control/proportional_edit>`
   for descriptions of the falloff types.

You can finely control which vertices are affected by the warp, and to what extent,
using a vertex group and/or a texture.

See :ref:`common masking options <modifiers-common-options-masking>` for a complete reference.


Usage
=====

The *Warp* modifier can be awkward to use sometimes, and its use case is rather small,
But there are a few still. For example, it can be used to have
an interactive :doc:`Proportional Editing </scene_layout/object/editing/transform/control/proportional_edit>`
that can be used for animations.

Another way to use this modifier is similar to
the :doc:`Deform Modifier </modeling/modifiers/deform/mesh_deform>`.
This allows you to deform parts of the mesh without having to make a vertex group.


Examples
========

.. figure:: /images/modeling_modifiers_deform_warp_example-curve-falloff.png
   :align: center

   Warp Modifier with a custom falloff curve.
