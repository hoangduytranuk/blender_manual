
****************
Laplacian Smooth
****************

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Context Menu --> Laplacian Smooth`

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
