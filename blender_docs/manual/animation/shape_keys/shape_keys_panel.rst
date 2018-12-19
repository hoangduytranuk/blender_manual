.. _bpy.ops.object.join_shapes:

****************
Shape Keys Panel
****************

.. admonition:: Reference
   :class: refbox

   :Editor:    Properties editor
   :Mode:      All modes
   :Panel:     :menuselection:`Object Data --> Shape Keys`

.. figure:: /images/animation_shape-keys_shape-keys-panel_basis.png

   Shape Keys panel.


Settings
========

Active Shape Key Index
   A :ref:`ui-list-view`.

   Value
      Current Value of the Shape Key (0.0 to 1.0).
   Mute (eye icon)
      This visually disables the shape key in the 3D View.

   Specials
      Transfer Shape Key
         Transfer the active *Shape Key* from a different object.
         Select two objects, the active Shape Key is copied to the active object.
      Join as Shapes
         Transfer the *Current Shape* from a different object.
         Select two objects, the Shape is copied to the active object.
      Mirror Shape Key
         If your mesh is nice and symmetrical, in *Object Mode*, you can mirror the shape keys on the X axis.
         This will not work unless the mesh vertices are perfectly symmetrical.
         Use the :menuselection:`Mesh --> Symmetrize` tool in *Edit Mode*.
      Mirror Shape Key (Topology)
         This is the same as *Mirror Shape Key* though it detects
         the mirrored vertices based on the topology of the mesh.
         The mesh vertices do not have to be perfectly symmetrical for this one to work.
      New Shape From Mix
         Add a new shape key with the current deformed shape of the object.
      Delete All Shapes
         Delete all shape keys.

Relative
   Set the shape keys to *Relative* or *Absolute*.

Show Only (pin icon)
   Show the shape of the active shape key without interpolation in the 3D View.
   *Show Only* is enabled while the object is in *Edit Mode*, unless the setting below is enabled.
Edit Mode
   Modify the shape key while the object is in *Edit Mode*.


Relative Shape Keys
-------------------

Relative shape keys deform from a selected shape key.
By default, all relative shape keys deform from the first shape key called the Basis shape key.

.. figure:: /images/animation_shape-keys_shape-keys-panel_relative.png

   Relative Shape Keys options.

Clear Weights ``X``
   Set all values to zero.

.. _animation-shapekey-relative-value:

Value
   The value of the active shape key.
Range
   Min and Max range of the active shape key value.
Blend
   Vertex Group
      Limit the active shape key deformation to a vertex group.
   Relative
      Select the shape key to deform from.


Absolute Shape Keys
-------------------

Absolute shape keys deform from the previous and to the next shape key.
They are mainly used to deform the object into different shapes over time.

.. figure:: /images/animation_shape-keys_shape-keys-panel_absolute.png

   Absolute Shape Keys options.

Reset Timing (clock icon)
   Reset the timing for absolute shape keys.
Interpolation
   This controls the interpolation between shape keys.

   Linear, Cardinal, Catmull-Rom, B-Spline

   .. _fig-interpolation-type:

   .. figure:: /images/animation_shape-keys_shape-keys-panel_interpolation-types.png

      Different types of interpolation.

      The red line represents interpolated values between keys (black dots).

Evaluation Time
   This is used to control the shape key influence.


Examples
========

Reset Timing
------------

For example, if you have the shape keys, Basis, Key_1, Key_2, in that order.

Reset Timing will loop the shape keys, and set the shape keyframes to +0.1:

- Basis 0.1
- Key_1 0.2
- Key_2 0.3

Evaluation Time will show this as frame 100:

- Basis 10.0
- Key_1 20.0
- Key_2 30.0


Evaluation Time
---------------

For example, if you have the shape keys, Basis, Key_1, Key_2, in that order, and you reset timing:

- Basis 10.0
- Key_1 20.0
- Key_2 30.0
