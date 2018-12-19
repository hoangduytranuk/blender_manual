
********
Symmetry
********

Snap to Symmetry
================

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Mesh --> Snap to Symmetry`

The Snap to Symmetry tool lets you snap a mesh vertices to their mirrored neighbors.

Useful when dealing with meshes which are mostly symmetrical,
but have vertices which have been moved enough that Blender
does not detect them as mirrored (when X Mirror option is enabled for example).

This can be caused by accident when editing without X Mirror enabled. Sometimes models
imported from other applications are asymmetrical enough that mirror fails too.

Direction
   Specify the axis and direction to snap. Can be any of the three axes,
   and either positive to negative, or negative to positive.
Threshold
   Specify the search radius to use when finding matching vertices.
Factor
   Support for blending mirrored locations from one side to the other (0.5 is an equal mix of both).
Center
   Snap vertices in the center axis to zero.

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_basics_symmetry_snap-to-symmetry-before.png
          :width: 320px

          Before Snap to Symmetry.

     - .. figure:: /images/modeling_meshes_editing_basics_symmetry_snap-to-symmetry-after.png
          :width: 320px

          After Snap to Symmetry.


Symmetrize
==========

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Mesh --> Symmetrize`

The *Symmetrize* tool is a quick way to make a mesh symmetrical.
*Symmetrize* works by cutting the mesh at the pivot point of the object,
and mirroring over the geometry in the specified axis, and merges the two halves together
(if they are connected). Also the mesh data is copied from one side to the other:
e.g. UVs, vertex colors, vertex weights.

Direction
   Specify the axis and direction of the effect. Can be any of the three axes,
   and either positive to negative, or negative to positive.
Threshold
   The vertices in this range will be snapped to the plane of symmetry.

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_basics_symmetry_symmetrize1.png
          :width: 320px

          Mesh before Symmetrize.

     - .. figure:: /images/modeling_meshes_editing_basics_symmetry_symmetrize2.png
          :width: 320px

          Mesh after Symmetrize.

.. seealso::

   See :doc:`Mirror </modeling/meshes/editing/transform/mirror>`
   for information on mirroring, which allows you to flip geometry across an axis.
