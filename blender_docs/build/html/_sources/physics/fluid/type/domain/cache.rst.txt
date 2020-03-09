
*****
Cache
*****

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Fluid --> Cache`
   :Type:      Domain

The *Cache* panel is used to :term:`Bake <Baking>` the fluid simulation and stores the outcome of
a simulation so it does not need to be recalculated.

Baking takes a **lot** of compute power (hence time). Depending on the scene, it is recommended
to allocate enough time for the baking process.

If the mesh has modifiers, the rendering settings are used for exporting the mesh to the fluid solver.
Depending on the setting, calculation times and memory use might exponentially increase. For example,
when using a moving mesh with *Subdivision Surface* as an obstacle, it might help to decrease simulation
time by switching it off, or to a low subdivision level. When the setup/rig is correct, you can always
increase settings to yield a more realistic result.

.. note::

   Fluid simulations use their own cache. All other physics simulations make use of
   the :doc:`General Baking </physics/baking>` operators.

.. _bpy.types.FluidDomainSettings.cache_directory:

Cache Directory
   Directory to store baked simulation files in. Inside this directory each simulation type
   (i.e. mesh, particles, noise) will have its own directory containing the simulation data.

.. _bpy.types.FluidDomainSettings.cache_type:

Type
   The type of the cache determines how the cache can be baked.

   Modular
      In this mode the cache is baked step by step. The bake operators for this type can be found in
      the other panels within the domain settings. It is possible to cancel and resume bake jobs when
      using this type.

   Final
      This mode bakes the cache considering all selected settings at once. The bake operator for this
      type can be found in the cache panel.

   Replay
      The cache is baked as the simulation is being played in the viewport.

.. _bpy.types.FluidDomainSettings.cache_frame_start:

Start
   Frame on which to start the simulation.

.. _bpy.types.FluidDomainSettings.cache_frame_end:

End
   Frame on which to stop the simulation.

   .. note::

      The simulation is only calculated for positive frames between the *Start* and *End* frames
      of the *Cache* panel. So if you want a simulation that is longer than the default frame range
      you have to change the *End* frame.

.. _bpy.types.FluidDomainSettings.cache_data_format:

Data File Format
   File format for the data simulation files. Data simulation files store the information of the most basic grids
   that are needed for a fluid simulation (e.g. velocity, density).

   Uni Cache
      Blender's own caching format with some compression.

   Raw Cache
      Blender's own caching format without any compression.

   OpenVDB
      Advanced and efficient storage method developed by
      `DreamWorks Animation <http://www.dreamworksanimation.com/>`__.

      All grids are stored in separate ``.vdb`` files. Thus every file contains just one simulation field or grid.

.. _bpy.types.FluidDomainSettings.cache_particle_format:

Particle File Format :guilabel:`Liquids Only`
   File format for the particle cache files.

   Uni Cache
      Blender's own caching format with some compression.

.. _bpy.types.FluidDomainSettings.cache_mesh_format:

Mesh File Format :guilabel:`Liquids Only`
   File format for the mesh cache files.

   Binary Object
      Mesh data files with some compression.

   Object
      Simple, standard data format for mesh data.

.. _bpy.ops.fluid.bake_all:
.. _bpy.ops.fluid.free_all:

Bake All, Free All
   This option is only available when using the :ref:`Final <bpy.types.FluidDomainSettings.cache_type>` cache type.
   *Bake All* will run the simulation considering all parameters from
   the settings (i.e. it will bake all steps that can be baked individually with
   the :ref:`Modular <bpy.types.FluidDomainSettings.cache_type>` cache type at once).

   The progress will be displayed in the status bar. Pressing :kbd:`Esc` will abort the simulation.

   Once the simulation has been baked, the cache can be deleted by pressing *Free All*.
   It is not possible to pause or resume a *Bake All* process as only the most essential cache files are stored on drive.


.. _bpy.types.FluidDomainSettings.export_manta_script:

Advanced
========

Export Mantaflow Script
   Export the simulation as a standalone Mantaflow script when baking the scene (exported on "Bake Data").
   Usually, only developers and advanced users who know how to use the Mantaflow GUI will
   make use of this functionality. Use a :ref:`Debug Value <bpy.ops.wm.debug_menu>` of ``3001`` to enable.
