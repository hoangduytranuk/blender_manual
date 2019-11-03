.. _bpy.ops.mesh.vertices_smooth:
.. _tool-mesh-smooth:

******
Smooth
******

Smooth Vertex
=============

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Panel:     :menuselection:`Toolbar --> Tools --> Mesh Tools --> Deform: Smooth Vertex`
   :Menu:      :menuselection:`Mesh --> Vertices --> Smooth Vertex`

This tool smooths the selected vertices by averaging the angles between the faces.
After using the tool, options appear in the *Toolbar*:

Smoothing
   Smoothing factor.
Repeat
   The number of smoothing iterations.
Axes
   Limit the effect to certain axes.

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_transform_smooth_mesh-before.png
          :width: 200px

          Mesh before smoothing.

     - .. figure:: /images/modeling_meshes_editing_transform_smooth_mesh-one-iteration.png
          :width: 200px

          Mesh after one smoothing iteration.

     - .. figure:: /images/modeling_meshes_editing_transform_smooth_mesh-ten-iterations.png
          :width: 200px

          Mesh after ten smoothing iterations.

.. seealso:: Subdividing

   Adjusting the *smooth* option after using
   the :doc:`Subdivide </modeling/meshes/editing/subdividing/subdivide>` tool
   results in a more organic shape.

.. seealso:: Smooth Modifier

   The :doc:`Smooth Modifier </modeling/modifiers/deform/smooth>`, which can be limited to a *Vertex Group*,
   is a non-destructive alternative to the Smooth tool.


Laplacian Smooth
================

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Specials --> Laplacian Smooth`

See the :doc:`Laplacian Smooth Modifier </modeling/modifiers/deform/laplacian_smooth>` for details.

Laplacian smooth uses an alternative smoothing algorithm that better preserves larger details and
this way the overall shape of the mesh. Laplacian smooth exists as a mesh operation and
as a non-destructive modifier.

.. note:: Real Smoothing versus Shading Smoothing

   Do not mistake this tool with the shading smoothing options described at
   :ref:`this page <modeling-meshes-editing-normals-shading>`, they do not work the same!
   This tool modifies the mesh itself, to reduce its sharpness, whereas *Set Smooth* / *Auto Smooth* and co.
   only control the way the mesh is shaded,
   creating an *illusion* of softness, but without modifying the mesh at all...
