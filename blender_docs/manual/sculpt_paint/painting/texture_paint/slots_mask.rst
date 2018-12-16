
************
Slots & Mask
************

The *Slots* tab in the *Tool Shelf* of the 3D View.


Slots
=====

.. figure:: /images/sculpt-paint_painting_texture-paint_slots-mask_slots-panel.png
   :align: right

   Slots settings.

The combination of images associated with UV maps is called "slots".

Selecting a *Paint Slots* or *Canvas Image*
will also display the corresponding image in *UV/Image Editors*.

Painting Mode
   The slot system includes two painting modes:

   Image
      You can just select an existing image and painting will use the active UV layer for painting.

      Canvas Image
         Allows you to select the image used as a canvas.

         New
            Create a new image.
      UV Map
         Allows you to select the UV layer for painting.
         (Same as the currently active UV map in the mesh's *UV Maps* panel.)

   Material
      This mode tries to detect the slots from the materials of the mesh.

      For the Cycles renderer,
      all texture images (*Image Texture* node) on the material's node tree are added on the slots tab.

      Available Paint Slots
         A :ref:`ui-list-view` of slots.
         To activate a certain slot to use it for paint a just :kbd:`LMB` click on it.

      UV Map
         Allows you to select a UV layer for the slot.
         The UV map selected in the *UV Map* nodes before an *Image Texture* will be used.
         If there is no *UV Map* nodes or it has a blank value,
         the active UV map of the mesh (*UV Maps* panel) will be used.

      .. (TODO 2.8) Blender Internal (START)

      For Blender Internal, texture paint slots are material texture slots that use images and UV mapping.
      The UV map that is used during painting is either the assigned on the UV slot of the material texture UV slot,
      or the active UV layer of the mesh (this is the highlighted UV map under the mesh tab in the properties editor)
      if no UV map has been assigned. There are a few extra controls:

      Add/Remove Texture Paint Slot
         A menu that allows the addition of new slots which are added directly on the material.
      Blend Type
         Same as in the
         :doc:`Texture Blending Modes </editors/uv_image/uv/textures/properties/influence/blending_modes>`.

      .. (TODO 2.8) (END)

Save All Images
   Repack (or save if external file) all edited images.
   Same as in the :doc:`UV/Image Editor </editors/uv_image/image/introduction>`.


Mask
====

.. figure:: /images/sculpt-paint_painting_texture-paint_slots-mask_mask-panel.png
   :align: right

   Mask settings.

The mask can be deactivated by the checkbox in the header.

UV Map
   Allows you to select the UV layer for the mask image.
Stencil Image
   Image used as a mask. See :ref:`ui-data-block`.
Visualization
   Mask color in the viewport. See :ref:`ui-color-picker`.
Invert Stencil (black/white icon)
   Inverts the mask.
