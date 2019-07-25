..    TODO/Review: {{review|im=old screenshot: Need to update}}.

******
Layout
******

After unwrap, you will likely need to arrange the UV maps into something
that can be logically textured or painted. Your goals for editing are:

- Stitch some pieces (UV maps) back together.
- Minimize wasted space in the image.
- Enlarge the faces where you want more detail.
- Re-size/enlarge the faces that are stretched.
- Shrink the faces that are too grainy and have too much detail.

With a minimum of dead space,
the most pixels can be dedicated to giving the maximum detail and fineness to the UV texture.
A UV face can be as small as a pixel (the little dots that make up an image)
or as large as an entire image. You probably want to make some major adjustments first,
and then tweak the layout.


Transforms
==========

.. admonition:: Reference
   :class: refbox

   :Mode:      View Mode and Mask Mode
   :Panel:     :menuselection:`Toolbar --> Tools --> Transform`
   :Menu:      :menuselection:`UVs --> Transform`

- Move :kbd:`G`
- Rotate :kbd:`R`
- Scale :kbd:`S`
- Shear :kbd:`Shift-Ctrl-Alt-S`


Axis Locking
------------

Transformations can be locked to an axis by pressing :kbd:`X` or :kbd:`Y` after one of the transform tools.
Also, holding the :kbd:`MMB` will constrain movement to the X or Y axis.


.. _bpy.types.SpaceUVEditor.use_live_unwrap:
.. _bpy.types.SpaceUVEditor.pixel_snap_mode:
.. _bpy.types.SpaceUVEditor.lock_bounds:

UV Options
==========

.. admonition:: Reference
   :class: refbox

   :Mode:      View Mode and Mask Mode
   :Menu:      :menuselection:`UVs`

Live Unwrap
   Continuously unwraps the selected UV islands while transforming pinned vertices.
Snap to Pixels
   Disabled
      UVs will not be snapped.
   Corner
      Will force the UVs to snap to the corners of the nearest pixels of an image if loaded.
   Center
      Will force the UVs to snap to the center of the nearest pixels of an image if loaded.
Constraining to Image Bounds
   Turning on *Constrain to Image Bounds* will prevent UVs from being moved outside the 0 to 1 UV range.


.. _bpy.ops.uv.pin:

Pin and Unpin
=============

.. admonition:: Reference
   :class: refbox

   :Mode:      View mode
   :Panel:     :menuselection:`Toolbar --> Tools --> UV Tools --> UV Unwrap: Pin/Unpin`
   :Menu:      :menuselection:`UVs --> Pin/Unpin`
   :Hotkey:    :kbd:`P`, :kbd:`Alt-P`

You can pin UVs so they do not move between multiple unwrap operations.
When Unwrapping a model it is sometimes useful to "Lock" certain UVs,
so that parts of a UV layout stay the same shape, and/or in the same place.
Pinning is done by selecting a UV, then selecting *Pin* from the *UVs* menu,
or the shortcut :kbd:`P`. You can *Unpin a UV* with the shortcut :kbd:`Alt-P`.

Pinning is most effective when using the Unwrap method of UV mapping, for organic objects.
An example is when you are modeling a symmetrical object using
the :doc:`Mirror Modifier </modeling/modifiers/generate/mirror>`.
Some of the UVs on the mirror axis may be shared across the mirrored counterparts.
You could pin the UVs that correspond to the midline, then align them on the X axis,
and they will stay in that location.

Pinning also work great with the Live Unwrap tool. If you pin two or more UVs,
with Live Unwrap on, dragging pinned UVs will interactively unwrap the model.
This helps with fitting a UV island to a certain shape or region.


Seams
=====

.. admonition:: Reference
   :class: refbox

   :Mode:      View mode
   :Panel:     :menuselection:`Toolbar --> Tools --> UV Tools --> UV Unwrap: Mark/Clear Seam`
   :Menu:      :menuselection:`UVs --> Mark/Clear Seam`

See :doc:`/modeling/meshes/editing/uv/unwrapping/seams`.


.. _bpy.ops.uv.pack_islands:
.. _editors-uv-editing-layout-pack_islands:

Pack Islands
============

.. admonition:: Reference
   :class: refbox

   :Mode:      View mode
   :Panel:     :menuselection:`Toolbar --> Tools --> UV Tools --> Pack Islands`
   :Menu:      :menuselection:`UVs --> Pack Islands`
   :Hotkey:    :kbd:`Ctrl-P`

The *Pack Islands* tool generates an optimized UV layout with non-overlapping islands
that tries to efficiently fill the :term:`texture space`.

First it will uniformly scale the selected island,
then individually transform each island so that they fill up the UV space as much as possible.


.. _bpy.ops.uv.average_islands_scale:

Average Island Scale
====================

.. admonition:: Reference
   :class: refbox

   :Mode:      View mode
   :Panel:     :menuselection:`Toolbar --> Tools --> UV Tools --> Average Island Scale`
   :Menu:      :menuselection:`UVs --> Average Island Scale`
   :Hotkey:    :kbd:`Ctrl-A`

Using the *Average Island Scale* tool, will scale each
UV island so that they are all approximately the same scale.


.. _bpy.ops.uv.minimize_stretch:

Minimize Stretch
================

.. admonition:: Reference
   :class: refbox

   :Mode:      View mode
   :Panel:     :menuselection:`Toolbar --> Tools --> UV Tools --> Minimize Stretch`
   :Menu:      :menuselection:`UVs --> Minimize Stretch`
   :Hotkey:    :kbd:`Ctrl-V`

The *Minimize Stretch* tool, reduces UV stretch by minimizing angles. This essentially relaxes the UVs.


.. _bpy.ops.uv.stitch:

Stitch
======

.. admonition:: Reference
   :class: refbox

   :Mode:      View mode
   :Panel:     :menuselection:`Toolbar --> Tools --> UV Tools --> Stitch`
   :Menu:      :menuselection:`UVs --> Stitch`
   :Hotkey:    :kbd:`V`

The *Stitch* tool, will join selected UVs that share vertices.
you set the tool to limit stitching by distance in the :ref:`ui-undo-redo-adjust-last-operation` panel,
by activating *use limit* and adjusting the *limit distance*


Copy Mirrored UV Coordinates
============================

.. admonition:: Reference
   :class: refbox

   :Mode:      View mode
   :Panel:     :menuselection:`Toolbar --> Tools --> UV Tools --> Copy Mirrored UV Coordinates`
   :Menu:      :menuselection:`UVs --> Copy Mirrored UV Coordinates`

Copies UVs from one side of the mirrored mesh to the other.
Affects only selected vertices (on both sides).

Axis Direction
   Positive/Negative
Precision
   Tolerance for finding vertex duplicates.


Mirror
======

.. admonition:: Reference
   :class: refbox

   :Mode:      View mode
   :Panel:     :menuselection:`Toolbar --> Tools --> UV Align --> Mirror X/Y`
   :Menu:      :menuselection:`UVs --> Mirror`
   :Hotkey:    :kbd:`Ctrl-M`

UVs can be mirrored on the Y axis or the X axis:

- Mirror X
- Mirror Y

You can also use the hotkey :kbd:`Ctrl-M`, then enter :kbd:`X` or :kbd:`Y`,
or hold the :kbd:`MMB` and drag in the mirror direction.


Snap
====

.. admonition:: Reference
   :class: refbox

   :Mode:      View mode
   :Menu:      :menuselection:`UVs --> Snap`
   :Hotkey:    :kbd:`Shift-S`

Snapping in the UV Editor is similar to
:doc:`Snapping in 3D </scene_layout/object/editing/transform/control/snap>`.
For the snap to pixel options to work an image has to be loaded.

Selected to Pixels
   Moves selection to nearest pixel. See also *Snap to pixel* above.
Selected to Cursor
   Moves selection to 2D cursor location.
Selected to Cursor (Offset)
   Moves selection center to 2D cursor location, while preserving the offset of the vertices from the center.
Selected to Adjacent Unselected
   Moves selection to adjacent unselected element.

Cursor to Pixels
   Snaps the cursor to the nearest pixels.
Cursor to Selected
   Moves the Cursor to the center of the selection.


.. _bpy.ops.uv.weld:

Weld
====

.. admonition:: Reference
   :class: refbox

   :Mode:      View mode
   :Panel:     :menuselection:`Toolbar --> Tools --> UV Tools --> Weld`
   :Menu:      :menuselection:`UVs --> Weld/Align --> Weld`,
               :menuselection:`Specials --> Weld`
   :Hotkey:    :kbd:`W`

The *Weld* tool will move selected UVs to their average position.


.. _bpy.ops.uv.remove_doubles:

Merge UVs by Distance
=====================

.. admonition:: Reference
   :class: refbox

   :Mode:      View mode
   :Panel:     :menuselection:`Toolbar --> Tools --> UV Tools --> Merge UVs by Distance`
   :Menu:      :menuselection:`UVs --> Weld/Align --> Merge UVs by Distance`,
               :menuselection:`Specials --> Merge UVs by Distance`

The *Merge UVs by Distance* tool will merge selected UVs within the specified *Margin*.


.. _bpy.ops.uv.align:

Straighten/Align
================

.. admonition:: Reference
   :class: refbox

   :Mode:      View mode
   :Panel:     :menuselection:`Toolbar --> Tools --> UV Tools --> UV Align --> Straighten/Align`
   :Menu:      :menuselection:`UVs --> Weld/Align --> Straighten/Align`,
               :menuselection:`Specials --> Straighten/Align`
   :Hotkey:    :kbd:`W`

Straighten
   Auto, X, Y
Align
   Will line up the selected UVs on the X axis, Y axis, or automatically chosen axis.

   Auto, X, Y


Proportional Editing
====================

.. admonition:: Reference
   :class: refbox

   :Mode:      View mode
   :Header:    :menuselection:`Proportional Editing`
   :Menu:      :menuselection:`UVs --> Proportional Editing`
   :Hotkey:    :kbd:`O`

Proportional Editing is available in UV editing. The controls are the same as in the 3D View.
See :doc:`Proportional Editing in 3D </scene_layout/object/editing/transform/control/proportional_edit>`
for a full reference.


Show/Hide Faces
===============

.. admonition:: Reference
   :class: refbox

   :Mode:      View mode
   :Menu:      :menuselection:`UVs --> Show/Hide Faces`

- Reveal Hidden :kbd:`Alt-H`
- Hide Select :kbd:`H`
- Hide Unselect :kbd:`Shift-H`


Export UV Layout
================

.. admonition:: Reference
   :class: refbox

   :Mode:      View mode
   :Menu:      :menuselection:`UVs --> Export UV Layout`

This is an :doc:`add-on </addons/io_mesh_uv_layout>` activated by default.


Header
======

Pivot Point
-----------

.. admonition:: Reference
   :class: refbox

   :Mode:      View mode
   :Header:    :menuselection:`Pivot Point`

The UV Editor has a 2D cursor. Its position can be changed by :kbd:`LMB`
clicking in the UV editor. You can also manually adjust its position in the Sidebar region.
The range by default is from 0 to 256 starting from the lower left corner.
By enabling *Normalized* under *Coordinates*, the range changes from 0 to 1.

The Pivot Point can be changed to:

- Bounding Box Center
- Median Point
- 2D Cursor Location


3D View
=======

.. _uv-image-rotate-reverse-uvs:

Face Mirror and Rotate UVs
--------------------------

.. admonition:: Reference
   :class: refbox

   :Editor:    3D View
   :Mode:      Edit mode
   :Menu:      :menuselection:`Mesh --> Face --> Rotate UVs/Reverse UVs`

The orientation of the UV texture is defined by each face.
If the image is, for example, upside down or laying on its side,
use the :menuselection:`Face --> Rotate UVs` (in the 3D View in Face Select mode)
menu to rotate the UVs per face in 90-degree turns.

The :menuselection:`Face --> Reverse UVs` tool mirrors the UVs per face,
which flips the image over, showing you the image reversed.
