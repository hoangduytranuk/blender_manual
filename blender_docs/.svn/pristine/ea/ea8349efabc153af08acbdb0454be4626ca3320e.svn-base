.. _bpy.types.ObjectSolverConstraint:

************************
Object Solver Constraint
************************

The *Object Solver* constraint gives the owner of this constraint,
the location and rotation of the "solved object motion".

The "solved object motion" is where Blender thinks the physical,
real-world (tracked) object was, relative to the camera that filmed it.

Can be used to add a mesh to video for example.

.. note::

   This constraint only works after you have set up a minimum of eight markers and pressed
   :ref:`Solve object Motion <editors-movie-clip-tracking-clip-solve-motion>`.
   Located at :menuselection:`Movie Clip Editor --> Toolbar --> Solve --> Solve Camera Motion`.

   If it says *Solve Camera Motion* instead of *Solve Object Motion* then go into
   the :menuselection:`Movie Clip Editor --> Sidebar region --> Objects`
   and switch it from the camera, to an object.


Options
=======

.. TODO2.8
   .. figure:: /images/animation_constraints_motion-tracking_object-solver_panel.png

      Object Solver Constraint panel.

Active Clip
   Receive tracking data from the active movie clip in the Movie Clip editor.
   If unchecked, an option appears to choose from the other clips.
Object
   Select a tracked object to receive transform data from.
Camera
   Select the camera to which the motion is parented to (if active empty scene camera is used).
Set Inverse
   Moves the origin of the object to the origin of the camera.
Clear Inverse
   Moves the origin of the object back to the spot set
   in the Movie Clip Editor :menuselection:`Toolbar --> Solve --> Orientation --> Set Origin`.
Constraint to F-Curve
   Applies the constraint, creating keyframes for the transforms.
