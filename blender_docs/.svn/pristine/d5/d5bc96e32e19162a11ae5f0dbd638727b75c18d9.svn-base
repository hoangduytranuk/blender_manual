
****************
Hiding & Masking
****************

.. admonition:: Reference
   :class: refbox

   :Mode:      Sculpt Mode
   :Menu:      :menuselection:`Sculpt`

While sculpting, areas might be hidden behind parts of the mesh or they might be too close to other parts.
To work through these, it is useful to isolate parts of a mesh to sculpt on.
This can be done by either completely hiding parts of the mesh
or by masking areas that can not be sculpted on.


Hide
====

Portions of the mesh can be hidden in Sculpt Mode to improve the viewport performance and
to access parts of the mesh that would otherwise be difficult to access,
because they are occluded by other parts.

The hidden faces cannot be sculpted on.
Hiding is shared between Edit Mode and Sculpt Mode
(i.e. hiding/unhiding in one mode affects the other mode too).

Show All :kbd:`Alt-H`
   Reveal all hidden parts.
Show Bounding Box :kbd:`Shift-H`
   To reveal a hidden part of a mesh inside the selection.
Hide Bounding Box :kbd:`H`
   To hide a part of a mesh inside the selection.
   This works similar to the :ref:`Box Select <tool-select-box>` tool.
Hide Masked
   Hides all masked vertices.


.. _sculpt-mask-menu:
.. _bpy.ops.paint.mask:

Mask
====

Masking to control which areas of the mesh are influenced by sculpting.

.. figure:: /images/sculpt-paint_sculpting_hide-mask_example.jpg

   Black part is masked.


Brush
-----

To edit the mask, select the *Mask Brush* from the Brush panel.


.. _bpy.ops.paint.mask_flood_fill:
.. _bpy.ops.paint.mask_lasso_gesture:
.. _bpy.ops.sculpt.mask_filter:
.. _bpy.ops.sculpt.mask_expand:
.. _bpy.ops.mesh.paint_mask_slice:
.. _bpy.ops.sculpt.dirty_mask:

Editing
-------

Masks can be edited across the entire model.
Using :kbd:`A` opens a pie menu to choose different operations.

Invert Mask :kbd:`Ctrl-I`
   Inverts an existing mask.
Fill Mask
   Fills the whole mask with a value of 1.
Clear Mask :kbd:`Alt-M`
   Fills the mask with a value of 0. To completely remove the mask data see `Clearing Mask Data`_.
Box Mask :kbd:`B`
   Works like the *Box Select* tool, it creates a rectangular mask region.
   Hold :kbd:`Shift` to clear the mask of the selected region.
Lasso Mask :kbd:`Shift-Ctrl-LMB`
   Can be used to create a free-form mask, similar to the *Lasso Select* tool.

   .. tip::

      To clear the mask of areas with the *Lasso Mask* tool, first invert the mask,
      apply the *Lasso Mask*, and then invert the mask back.

Mask Filters
   Mask filters are operations that are applied to the whole paint mask.

   Type
      Smooth/Sharpen Mask
         Changes the crispness of the mask edge.
      Grow/Shrink Mask
         Changes the size of the mask.
      Increase/Decrease Contrast
         Changes the contrast of the mask.
   Iterations
      The number of times that the filter is going to be applied.
   Auto Iteration Count
      Use a automatic number of iterations based on the number of vertices of the sculpt.

Expand Mask by Topology :kbd:`Shift-A`
   Creates a mask radiating outwards from the active vertex in a uniform manner.

Expand Mask by Curvature :kbd:`Shift-Alt-A`
   Creates a mask radiating outwards from the active vertex while following the curvature of the mesh.

Mask Extract
   Creates a duplicate mesh object based on masked geometry.

   Threshold
      Minimum mask value to consider the vertex valid to extract a face from the original mesh.
   Add Boundary Loop
      Creates and extra boundary loop on the edges of the geometry,
      making it ready for adding a Subdivision Surface modifier later.
   Smooth Iterations
      Smooth iterations applied to the extracted mesh.
   Project to Sculpt
      Project the extracted mesh on to the original sculpt object.
   Extract as Solid
      Adds a :doc:`Solidify Modifier </modeling/modifiers/generate/solidify>` to the newly created mesh object.

Mask Slice
   Removes the masked vertices from the mesh.

   Threshold
      Minimum mask value to consider the vertex valid to extract a face from the original mesh
   Fill Holes
      Fills concave holes with geometry that might have resulted from the *Mask Slice* operation.
   Slice to New Object
      Create a new object from the masked geometry.

Dirty Mask
   Generates a mask based on the geometry cavity and pointiness.


.. _bpy.types.Sculpt.show_mask:
.. _bpy.types.View3DOverlay.sculpt_mode_mask_opacity:

Displaying
----------

.. admonition:: Reference
   :class: refbox

   :Mode:      Sculpt Mode
   :Popover:   :menuselection:`Viewport Overlays -- Sculpt --> Mask`

The mask display can be toggled as a :doc:`viewport overlay </editors/3dview/display/overlays>`.
In the overlay popover, the opacity of the mask overlay can be adjusted to make it more or less visible on the mesh.


.. _bpy.ops.mesh.customdata_mask_clear:
.. _sculpt_mask_clear-data:

Clearing Mask Data
------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Object/Edit Mode
   :Menu:      :menuselection:`Properties --> Object Data --> Geometry Data --> Clear Sculpt-Mask Data`

Completely frees the mask data layer from the mesh, while not a huge benefit,
this can speed-up sculpting if the mask is no longer being used.
