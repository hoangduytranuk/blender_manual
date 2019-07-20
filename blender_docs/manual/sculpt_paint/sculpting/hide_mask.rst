
****************
Hiding & Masking
****************

.. admonition:: Reference
   :class: refbox

   :Mode:      Sculpt Mode
   :Menu:      :menuselection:`Hide/Mask`

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

Hide Bounding Box :kbd:`H`
   To hide a part of a mesh inside the selection.
   This works similar to :ref:`Box Select <tool-select-box>` tool.
Hide Bounding Box :kbd:`Shift-H`
   To reveal a hidden part of a mesh inside the selection.
Show All :kbd:`Alt-H`
   Reveal all hidden parts.
Hide Masked
   Hides all masked vertices.


.. _sculpt-mask-menu:

Mask
====

Masking to control which areas of the mesh are influenced by sculpting.

.. figure:: /images/sculpt-paint_sculpting_hide-mask_example.jpg

   Black part is masked.


Brush
-----

In order to edit the mask, select the *Mask Brush* from the Brush panel.


Editing
-------

Masks can be edited across the entire model:

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


Displaying
----------

.. admonition:: Reference
   :class: refbox

   :Mode:      Sculpt Mode
   :Popover:   :menuselection:`Viewport Overlays -- Sculpt --> Mask`
   :Menu:      :menuselection:`Tool Settings --> Sculpt --> Mask`

The mask display can be toggled as a :doc:`viewport overlay </editors/3dview/controls/overlays>`.
In the overlay popover, the opacity of the mask overlay can be adjusted to make it more or less visible on the mesh.


.. _sculpt_mask_clear-data:

Clearing Mask Data
------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Object/Edit Mode
   :Menu:      :menuselection:`Properties --> Object Data --> Geometry Data --> Clear Sculpt-Mask Data`

Completely frees the mask data layer from the mesh, while not a huge benefit,
this can speed-up sculpting if the mask is no longer being used.
