.. _bpy.types.Sculpt.symmetrize_direction:
.. _bpy.ops.sculpt.symmetrize:

********
Symmetry
********

.. admonition:: Reference
   :class: refbox

   :Mode:      Sculpt Mode
   :Tool:      :menuselection:`Toolbar --> Tool --> Symmetry`

Mirror
   See :doc:`/sculpt_paint/brush/symmetry`.
Lock
   These three buttons allow you to block any modification/deformation
   of your model along selected local axes, while you are sculpting it.
Tiling
   Using this option allows you to seamlessly tile your strokes along the given axes.
   This allows to create repeating patterns.
Feather
   Reduces the strength of the stroke where it overlaps the planes of symmetry.
Radial
   See :doc:`/sculpt_paint/brush/symmetry`.
Tile Offset
   The default tile size is set to one unit.
   The offset allows the option to alter the tile size along all three axes.

Direction
   Determines which direction the model will be symmetrized.
Symmetrize
   Uses direction orientation to symmetrize. Since Dyntopo adds
   details dynamically it may happen that the model goes asymmetric,
   so this a good tool for that.
