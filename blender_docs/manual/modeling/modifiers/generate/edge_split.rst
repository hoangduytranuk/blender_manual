.. _bpy.types.EdgeSplitModifier:

*******************
Edge Split Modifier
*******************

The Edge Split Modifier splits edges within a mesh.
The edges to split can be determined from the edge angle (i.e. angle between faces forming this edge),
and/or edges marked as sharp.

Splitting an edge affects vertex normal generation at that edge, making the edge appear sharp.
Hence, this modifier can be used to achieve the same effect as :ref:`Auto Smooth <auto-smooth>`,
making edges appear sharp when their angle is above a certain threshold.
It can also be used for manual control of the smoothing process,
where the user defines which edges should appear smooth or sharp
(see :ref:`Mesh Smoothing <modeling-meshes-editing-normals-shading>` for other ways to do this).
If desired, both modes can be active at once.

The output of the Edge Split Modifier is available to export scripts,
making it quite useful for creators of game content.


Options
=======

.. figure:: /images/modeling_modifiers_generate_edge-split_panel.png

   Edge Split Modifier.

Edge Angle
   When enabled, edges will be split if the angle between its
   two adjacent faces is greater than the *Split Angle*.

   Split Angle
      On 0: all edges are split. On 180: no edges are split.

Sharp Edges
   When enabled, edges will be split if they were marked as sharp using :menuselection:`Edge Specials --> Mark Sharp`
   (Menu shortcut: :kbd:`Ctrl-E` in Edit Mode).

.. note::

   :term:`Non-manifold` edges (edges shared by more than two faces) will always be split.


Examples
========

.. list-table::

   * - .. figure:: /images/modeling_modifiers_generate_edge-split_example-1.png

          Flat shading.

     - .. figure:: /images/modeling_modifiers_generate_edge-split_example-2.png

          Smooth shading.

   * - .. figure:: /images/modeling_modifiers_generate_edge-split_example-3.png

          Smooth shading with Edge Split.

     - .. figure:: /images/modeling_modifiers_generate_edge-split_example-4.png

          Smooth shading with Edge Split and Subdivision Surface.

.. note::

   Splitting edges can also be performed manually in Edit Mode using:
   :menuselection:`Edge Specials --> Edge Split` (Menu shortcut: :kbd:`Ctrl-E`).
