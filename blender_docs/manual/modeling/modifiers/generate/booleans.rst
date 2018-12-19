.. _bpy.types.BooleanModifier:

****************
Boolean Modifier
****************

The Boolean Modifier performs operations on meshes that are otherwise too complex
to achieve with as few steps by editing meshes manually. The Boolean Modifier
uses one of three Boolean operations that can be used to create a single mesh out of two mesh objects:

.. figure:: /images/modeling_modifiers_generate_booleans_union-intersect-difference-examples.png

   The Union, Intersection and Difference between a Cube and a UV Sphere,
   with the modifier applied to the sphere and using the cube as target.


Usage
=====

To use the *Boolean Modifier* select the desired mesh Object then add a *Boolean Modifier*.
When you add the Boolean Modifier for an object, Blender will need a second object to
be the target of the operation. You can use open or closed meshes,
as long as they have available face normals for the calculations to take effect.
You can add one or more modifiers of this type for an Object but you can only apply one
operation for the Boolean Modifier at a time.

.. tip:: This is a dynamic real-time modifier!

   If you have marked your Objects to show the Edges
   (in :menuselection:`Properties Editor --> Object --> Display`, enable *Wire*),
   you will see the Edge creation process while you are moving your Objects. Depending on your mesh topology,
   you can also enable X-Ray and Transparency and see the topology being created in real-time.


Options
=======

.. figure:: /images/modeling_modifiers_generate_booleans_panel.png

   Boolean Modifier options.


Operations
----------

Operation
   Which boolean operation will be used.

   Difference
      The modified mesh is subtracted from the target mesh.
   Union
      The target mesh is added to the modified mesh.
   Intersect
      The target mesh is subtracted from the modified mesh.

Object
   The name of the target mesh object.

Solver
   Determines what set of algorithms are used to calculate the boolean operation.
   Carve uses the external `Carve Library <https://github.com/VTREEM/Carve>`__
   while BMesh uses Blender's built-in library and should give better results.


Known Limitations
=================

Boolean operates best on *water-tight* meshes, where inside/outside is clearly defined.

The following characteristics are known to give bad output.

- Open volumes.
- Overlapping geometry.
- Self-intersections.
- Zero-area faces.

While they may not fail in all situations, they aren't guaranteed to work properly.
