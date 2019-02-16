
*************
Clear & Apply
*************

.. _bpy.ops.object.*clear:

Clear
=====

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Object --> Clear --> Clear Location / Clear Scale / Clear Rotation / Clear Origin`
   :Hotkey:    :kbd:`Alt-G`, :kbd:`Alt-S`, :kbd:`Alt-R`, :kbd:`Alt-O`

Clearing transforms simply resets the transform values.
The objects location and rotation values return to 0, and the scale returns to 1.

Clear Location :kbd:`Alt-G`
   Clear (reset) the location of the selection.
   This will move the selection back to the coordinates (0, 0, 0).
Clear Scale :kbd:`Alt-S`
   Clear (reset) the scale of the selection.
   This will resize the selection back to the size it was when created.
Clear Rotation :kbd:`Alt-R`
   Clear (reset) the rotation of the selection.
   This will set the rotation of the selection to 0 degrees in each plane.
Clear Origin :kbd:`Alt-O`
   Clears (resets) the offset of the child objects origin.
   This will cause child objects to move to the origin of the parent.


Options
-------

Clear Delta
   Clear the :ref:`delta transform <transform-delta>` in addition to clearing the primary transforms.
   (Appears in the Operator panel.)


Apply
=====

These operations lets you apply several transformations to the selected objects.
The object transformation coordinates are transferred to the object data.
If the objects have hierarchical descendants, it also applies those transformations to their children.


.. _bpy.ops.object.transform_apply:

Apply Object Transformations
----------------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Object --> Apply --> Location / Rotation / Scale / Rotation & Scale`
   :Hotkey:    :kbd:`Ctrl-A`

Applying transform values essentially resets the values of object's location, rotation or scale,
while visually keeping the object data in-place.
The object origin point is moved to the global origin, the rotation is cleared and scale values are set to 1.

For simple cases you won't notice any difference the 3D View or rendered output,
however modifiers and constraints may depend on object transformation.

.. warning:: Armature Objects

   While applying transformations to armatures is supported,
   this does **not** apply to their pose location, animation curves or constraints.
   This tool should be used before rigging and animation.

When running *Apply Transform*, the Operator panel lets you choose the combination of transformations to apply.


Options
^^^^^^^

Location
   Apply (set) the location of the selection.
   This will make Blender consider the current location to be equivalent to 0 in each plane
   i.e. the selection will not move, the current location will be considered to be the "default location".
   The Object origin will be set to actual (0, 0, 0) (where the colored axis lines intersect in each view).
Rotation
   Apply (set) the rotation of the selection.
   This will make Blender consider the current rotation to be equivalent to 0 degrees in each plane
   i.e. the selection will not rotated, the current rotation will be considered to be the "default rotation".
Scale
   Apply (set) the scale of the selection.
   This will make Blender consider the current scale to be equivalent to 0 in each plane
   i.e. the selection will not scaled, the current scale will be considered to be the "default scale".
Rotation and Scale
   Apply (set) the rotation and scale of the selection. Do the above two applications simultaneously.
Apply Properties
   (Todo)


.. _bpy.ops.object.transforms_to_deltas:
.. _bpy.ops.object.anim_transforms_to_deltas:

Transforms to Deltas
--------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Object --> Apply -->`
   :Hotkey:    :kbd:`Shift-Alt-G`, :kbd:`Shift-Alt-R`, and :kbd:`Shift-Alt-S`

Converts primary object transformations to :ref:`delta transforms <transform-delta>`,
any existing delta transforms will be included as well.

- Location to Deltas :kbd:`Shift-Alt-G`
- Rotation to Deltas :kbd:`Shift-Alt-R`
- Scale to Deltas :kbd:`Shift-Alt-S`

All Transforms to Deltas
   Converts all primary transformations to delta transforms.
Animated Transform to Deltas
   Converts the primary transformation animations
   (animations done to the translation, scale, and, rotation values) to delta transforms.


Options
^^^^^^^

Reset Values
   Clear primary transform values after transferring to deltas.


.. _bpy.ops.object.visual_transform_apply:

Visual Transform
----------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Object --> Apply --> Visual Transform`
   :Hotkey:    :kbd:`Ctrl-A`

Apply (set) the result of a constraint and apply this back to the Object's location, rotation and scale.


Visual Geometry as Mesh
-----------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Object --> Apply --> Visual Geometry as Mesh`
   :Hotkey:    :kbd:`Ctrl-A`

Apply the visual state of all selected objects (modifiers, shape keys, hooks, etc.) to object data.
This is a way to freeze all object data into static meshes, as well as converts non-mesh types to mesh.

For details, see the :ref:`object-convert-to` mesh.


.. _bpy.ops.object.duplicates_make_real:

Make Duplicate Real
-------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Object --> Apply --> Make Duplicate Real`
   :Hotkey:    :kbd:`Shift-Ctrl-A`

*Make Duplicates Real* unlinks linked duplicates so each duplicate now has its own data-block.

.. (TODO) Need to explain, here we mean the Dupli Object (Particle, DupliGroup...)


Options
^^^^^^^

Parent
   Parents all the generated objects to the former duplicator when the option is checked;
   otherwise, they will be global objects.
Keep Hierarchy
   If this option is checked, the internal hierarchies (i.e. parent relationships)
   will be preserved in the newly generated objects,
   even if *Parent* is also checked, in which case, only the duplicated objects on top of the hierarchy
   will be parented to the former duplicator.
