.. _fluid-baking:

******
Baking
******

.. TODO2.8:
   .. figure:: /images/physics_fluid_types_domain_panels.png

      The fluid simulation options with Domain selected.


Bake Button
===========

Perform the actual fluid simulation. Blender will continue to work normally,
except the progress will be displayed in the statusbar.
Pressing :kbd:`Esc` or the "X" button next to the statusbar will abort the simulation.
Afterwards two ``.bobj.gz`` (one for the *Final* quality, one for the *Preview* quality),
plus one ``.bvel.gz`` (for the *Final* quality)
will be in the selected output directory for each frame.


Bake Directory
==============

Directory and file prefix to store baked surface meshes.

This is similar to the animation output settings, only selecting a file is a bit special:
when you select any of the previously generated surface meshes
(e.g. ``test1_fluidsurface_final_0132.bobj.gz``),
the prefix will be automatically set (``test1_`` in this example).
This way the simulation can be done several times with different settings,
and allows quick changes between the different sets of surface data.


Notes
=====

Unique domain
   Because of the possibility of spanning and linking between scenes,
   there can only be one domain in an entire blend-file.

Selecting a Baked Domain
   After a domain has been baked, it changes to the fluid mesh.
   To re-select the domain so that you can bake it again after you have made changes,
   go to any frame and select :kbd:`RMB` the fluid mesh.
   Then you can click the *bake* button again to recompute the fluid flows inside that domain.

Baking always starts at Frame #1
   The fluid simulator disregards the *Start* setting in the *Animation* panel,
   it will always bake from frame 1. If you wish the simulation to start later than frame 1,
   you must key the fluid objects in your domain to be inactive until the frame you desire to start the simulation.

Baking always ends at the *End* Frame set in the *Animation* panel
   If the frame rate is set to 25 frames per second,
   and ending time is 4.0 seconds, then you should (if your start time is 0)
   set your animation to end at frame ``4.0 × 25 = 100``.

Freeing the previous baked solutions
   Deleting the content of the "Bake" directory is a destructive way to achieve this.
   Be careful if more than one simulation uses the same bake directory
   (be sure they use different filenames, or they will overwrite one another)!

Reusing Bakes
   Manually entering (or searching for) a previously saved (baked)
   computational directory and filename mask will switch the fluid
   flow and mesh deformation to use that which existed during the old bake.
   Thus, you can reuse baked flows by simply pointing to them in this field.

Baking processing time
   Baking takes a **lot** of compute power (hence time).
   Depending on the scene, it might be preferable to bake overnight.

   If the mesh has modifiers, the rendering settings are used for exporting the mesh to the fluid solver.
   Depending on the setting, calculation times and memory use might exponentially increase.
   For example, when using a moving mesh with *Subdivision Surface* as an obstacle,
   it might help to decrease simulation time by switching it off, or to a low subdivision level.
   When the setup/rig is correct, you can always increase settings to yield a more realistic result.


.. ===="St"/"Ad"/"Bn"/"Par" Buttons====
   Till now, we were in the |Standard buttons.
   Clicking another one of these buttons will show other "panels"
   (groups of controls: Advanced, ``Bn`` for boundary, and Particle)
   of more advanced options, that often are fine set at the defaults.

   Standard
      The settings in this set are already been described above...

   Advanced
      Gravity vector
         Strength and direction of the gravity acceleration and any lateral (X, Y plane) force.
         The main component should be along the negative Z axis (in ``m.s<sup>-2</sup>``).

   .. note::

      All of the X, Y, Z values should not be zero, or the fluid will not flow!
      Imagine a droplet floating in the nothingness of deep space...
      It must be some small number in at least one direction.
