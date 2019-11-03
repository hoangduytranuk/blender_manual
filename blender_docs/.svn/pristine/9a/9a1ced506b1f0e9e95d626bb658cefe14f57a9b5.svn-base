.. _bpy.types.BooleanModifier:

****************
Boolean Modifier
****************

The *Boolean* modifier performs operations on meshes that are otherwise too complex
to achieve with as few steps by editing meshes manually. It uses one of
the three available boolean operations to create a single mesh out of two mesh objects:

.. figure:: /images/modeling_modifiers_generate_booleans_union-intersect-difference-examples.png

   The Union, Intersection and Difference between a Cube and a UV Sphere,
   with the modifier applied to the sphere and using the cube as target.

This modifier needs a second object to be the target (the second operand) of the operation.

.. warning::

   Only :term:`manifold` meshes are guaranteed to give proper results,
   other cases (especially "opened" meshes, :term:`non-manifold` but without any self-intersections)
   will usually work well, but might give odd glitches and artifacts in some cases.

   You should also avoid any co-planar faces (or co-linear edges) between both operands,
   those also tend to give issues currently.

.. tip::

   If you have marked your objects to show the edges
   (in :menuselection:`Properties Editor --> Object --> Viewport Display`, enable *Wireframe*),
   you will see the edge creation process while you are moving your objects around. Depending on your mesh topology,
   you can also enable X-Ray and Transparency and see the topology being created in real-time.


Options
=======

.. figure:: /images/modeling_modifiers_generate_booleans_panel.png

   The Boolean modifier.


Operations
----------

Operation
   Which boolean operation will be used.

   Difference
      The target mesh is subtracted from the modified mesh (everything *outside* of the target mesh is kept).
   Union
      The target mesh is added to the modified mesh.
   Intersect
      Opposite of *Difference* (everything *inside* of the target mesh is kept).

Object
   The name of the target mesh object.

Overlap Threshold
   Maximum distance between two faces to consider them as overlapping.
