.. _bpy.types.SubsurfModifier:

****************************
Subdivision Surface Modifier
****************************

The Subdivision Surface Modifier is used to split the faces of a mesh into smaller faces giving a smooth appearance.
Using this modifier, enables you to model complex smooth surfaces with simple, low-vertex meshes.
This allows modeling of high resolution meshes without the need to save and
maintain huge amounts of data and it gives a smooth *organic* look to the object.

This process creates virtual geometry that is generated non-destructively without modifying the original mesh,
but it can be converted to real geometry that you could edit with the *Apply* button.

Also, like the rest of the Modifiers, order of execution has an important bearing on the results.
For this, see the documentation on the :ref:`modifier stack <modifier-stack>`.

Keep in mind that this is a different operation than its companion,
:ref:`Smooth Shading <modeling-meshes-editing-normals-shading>`.
You can see the difference between the two in the grid image below.

.. figure:: /images/modeling_modifiers_generate_subsurf_grid.png

   Subdivisions levels 0 to 3, without and with Smooth Shading.

.. tip::

   The Subdivision Surface Modifier does not allow you to edit the new subdivided geometry without applying it,
   but the :doc:`Multiresolution Modifier </modeling/modifiers/generate/multiresolution>` does (in sculpt mode).


Options
=======

.. figure:: /images/modeling_modifiers_generate_subsurf_panel.png

   Modifier's panel.

Type
   This toggle button allows you to choose the subdivision algorithm:

   Catmull-Clark
      The default option, subdivides and smooths the surfaces.
      According to its `Wikipedia page <https://en.wikipedia.org/wiki/Catmull%E2%80%93Clark_subdivision_surface>`__,
      the "arbitrary-looking formula was chosen by Catmull and Clark based on the aesthetic appearance of
      the resulting surfaces rather than on a mathematical derivation."
   Simple
      Only subdivides the surfaces, without any smoothing
      (the same as :menuselection:`Specials --> Subdivide`, in Edit Mode).
      Can be used, for example, to increase base mesh resolution when using displacement maps.

Subdivisions
   Recursively adds more geometry. For details on polygon counts, see the `Performance Considerations`_ section.

   The right combination of these settings will allow you to keep a fast and lightweight approximation of your model
   when interacting with it in 3D, but use a higher quality version when rendering.

   Viewport
      The number of subdivision levels shown in the 3D View.
   Render
      The number of subdivision levels shown in renders.
   Quality
      TODO 2.8.

   .. tip::

      Be careful not to set the *Viewport* subdivisions higher than the *Render* subdivisions,
      this would mean the 3D View will be higher quality than the render.

Options
   Subdivide UVs
      When enabled, the UV maps will also be subdivided
      (i.e. Blender will add "virtual" coordinates for all sub-faces created by this modifier).

   .. list-table::

      * - .. figure:: /images/modeling_modifiers_generate_subsurf_subdivide-uvs-no.png
             :width: 320px

             No Subsurf.

        - .. figure:: /images/modeling_modifiers_generate_subsurf_subdivide-uvs-off.png
             :width: 320px

             Subdivide UVs off.

        - .. figure:: /images/modeling_modifiers_generate_subsurf_subdivide-uvs-on.png
             :width: 320px

             Subdivide UVs on.

   Optimal Display
      When drawing the wireframe of this object, the wires of the new subdivided edges will be skipped
      (only draws the edges of the original geometry).


Control
=======

Catmull-Clark subdivision rounds off edges, and often this is not what you want.
There are several solutions that allow you to control the subdivision.


.. _modifiers-generate-subsurf-creases:

Weighted Edge Creases
---------------------

Weighted edge creases for subdivision surfaces allows you to change the way
the Subdivision Surface modifier subdivides the geometry to give the edges a smooth or sharp appearance.

.. figure:: /images/modeling_modifiers_generate_subsurf_withcrease.png

   A subdivided cube with creased edges.

The crease weight of selected edges can be changed in the *Transform* panel of the Sidebar region
:kbd:`N`, or by using the shortcut :kbd:`Shift-E` and moving the mouse closer
or further from the selected edges to adjust the crease weight.
A higher value makes the edge "stronger" and more resistant to the smoothing effect of subdivision surfaces.


Edge Loops
----------

.. figure:: /images/modeling_modifiers_generate_subsurf_cube-with-edge-loops.png

   Subdivision Level 2 cube, the same with an extra Edge Loop, and the same with six extra Edge Loops.

The Subdivision Surface Modifier demonstrates why good, clean topology is so important.
As you can see in the figure, the Subdivision Surface Modifier has a drastic effect on a default Cube.
Until you add in additional Loops (with :kbd:`Ctrl-R`), the shape is almost unrecognizable as a cube.

A mesh with deliberate topology has good placement of Edge Loops,
which allow the placement of more Loops
(or removal of Loops, with :kbd:`X` :menuselection:`--> Edge Loop`)
to control the sharpness/smoothness of the resultant mesh.


Performance Considerations
==========================

Higher levels of subdivisions mean more vertices, and more vertices means more memory will be used
(both video memory for display (VRAM), and system RAM for rendering).
Blender could potentially crash or hang if you do not have enough memory.

When using high levels of subdivision with a graphics card that has a low total amount
of VRAM, some parts of the geometry will disappear visually. Your mesh will actually be intact,
because the render is generated using your Object Data,
(even though it cannot be shown by your graphics card).


Keyboard Shortcuts
==================

To quickly add a Subdivision Surface Modifier to one or more objects, select it/them and press :kbd:`Ctrl-1`.
That will add a Subdivision Surface Modifier with *View Subdivisions* on 1.

You can use other numbers too, such as :kbd:`Ctrl-2`, :kbd:`Ctrl-3`, etc,
to add a Subdivision Surface Modifier with that number of subdivisions.
The *Render Subdivisions* will always be on 2 when added like this.

If an object already has a Subdivision Surface Modifier,
doing this will simply change its subdivision level instead of adding another modifier.


Known Limitations
=================

Non-Contiguous Normals
----------------------

Blender's subdivision system produces nice smooth subdivided meshes, but any subdivided face
(that is, any small face created by the algorithm from a single face of the original mesh),
shares the overall normal orientation of that original face.

.. list-table::

   * - .. figure:: /images/modeling_modifiers_generate_subsurf_normal-orientation-1.png
          :width: 320px

          Comparison of good normals and bad normals.

     - .. figure:: /images/modeling_modifiers_generate_subsurf_normal-orientation-2.png
          :width: 320px

          Side view of image on left.

Abrupt normal changes can produce ugly black gouges even though
these flipped normals are not an issue for the shape itself.

A quick way to fix this is to use Blender's
:doc:`Recalculate Normals </modeling/meshes/editing/normals>` operation in Edit Mode.

If you still have some ugly black gouges you will have to
:doc:`Manually Flip the Normals </modeling/meshes/editing/normals>`.


Concave N-Gons
--------------

While n-gons are supported,
concave n-gons may give ugly overlapping results.

.. figure:: /images/modeling_modifiers_generate_subsurf_ngon-concave.png
   :width: 300px

   The n-gons on the right show overlapping results.
