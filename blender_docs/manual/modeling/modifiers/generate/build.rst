.. _bpy.types.BuildModifier:

**************
Build Modifier
**************

The *Build* modifier causes the faces of the mesh object to appear or disappear one after the other over time.

By default, faces appear in the order in which they are stored in memory (by default, the order of creation).
The face/vertex order can be altered in Edit Mode by using :ref:`Sort Mesh Elements <mesh-edit-sort-elements>`.


Options
=======

.. figure:: /images/modeling_modifiers_generate_build_panel.png
   :align: right

   The Build modifier.

Start
   The start frame of the building process.
Length
   The number of frames over which to rebuild the object.

Randomize
   Randomizes the order in which the faces are built.
Seed
   The random seed.
   Changing this value gives a different "random" order when *Randomize* is checked.
   This order is always the same for a given seed/mesh set.
Reversed
   The modifier will operate in reverse, essentially allowing it to be used as a "deconstruction" effect.
   This is useful for making a set of dupli-objects gradually disappear.


Example
=======

The *Build* modifier is often useful when needing a way to get a large number of items to progressively appear,
without resorting to animating the visibility of each one by one.
Examples of this include a mesh containing vertices only,
which is used as an :doc:`Instance Verts emitter </scene_layout/object/properties/instancing/verts>`,
and has the build modifier on it. Such a setup is a workaround/technique for being able to
art-direct some semi-random layout of a collection of objects (i.e. leaves/balls forming a carpet of sorts)
when doing so with particles is not desirable
(e.g. due to undesirable distribution of items leaving random gaps and overlapping in other places).

.. youtube:: -7SqfX5vt_8
