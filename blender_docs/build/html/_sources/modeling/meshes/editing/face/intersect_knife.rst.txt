.. _bpy.ops.mesh.intersect:

*****************
Intersect (Knife)
*****************

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Face --> Intersect (Knife)`

The Intersect tool lets you cut intersections into geometry.
It is a bit like the Boolean tool, but, does not calculate interior/exterior geometry.
Faces are split along the intersections, leaving new edges selected.

Source
   Selected/Unselected
      Operate between the selected and unselected geometry.
   Self Intersect
      Operate on the overlapping geometry of the mesh.
Separate Mode
   All
      Splits the geometry at the new edge.
   Cut
      Keep each side of the intersection separate without splitting the faces in half.
   Merge
      Merge all the geometry from the intersection.
Merge Threshold
   See Intersect (Boolean).
