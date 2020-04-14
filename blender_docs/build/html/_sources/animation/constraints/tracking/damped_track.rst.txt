.. _bpy.types.DampedTrackConstraint:

***********************
Damped Track Constraint
***********************

The *Damped Track* constraint constrains one local axis of the owner to always point towards *Target*.
This constraint uses a pure :term:`Swing` rotation, i.e. the shortest possible single axis rotation.
In other 3D software you can find it with the name "Look at" constraint.

Although usually associated with bones, Damped Track can align objects to point to (and follow)
other objects or bones. It is important to note that the constraint aligns the origin's axes to
point to the target's origin point. This is illustrated in the following figure.
In each case the objects are set as Damped Track to +X.

.. figure:: /images/animation_constraints_damped_track_axis.png
   :align: center

   A: Object vertices aligned along axis origin.
   B: Object vertices aligned away from origin.


Options
=======

.. TODO2.8
   .. figure:: /images/animation_constraints_tracking_damped-track_panel.png

      Damped Track panel.

Target
   :ref:`ui-data-id` used to select the constraint's target, and is not functional (red state) when it has none.
To
   Once the owner object has had a Damped Track constraint applied to it,
   you must then choose which axis of the object you want to point at the Target object.
   You can choose between 6 axis directions (-X, -Y, -Z, X, Y, Z).
   The negative axis direction cause the object to point away from
   the Target object along the selected axis direction.

.. vimeo:: 171278084
