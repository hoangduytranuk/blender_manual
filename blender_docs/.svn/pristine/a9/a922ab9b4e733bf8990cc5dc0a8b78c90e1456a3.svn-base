.. _bpy.types.FluidDomainSettings.cache:

*****
Cache
*****

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Fluid --> Cache`
   :Type:      Domain

The *Cache* panel is used to :term:`Bake <Baking>` the fluid simulation
and stores the outcome of a simulation so it does not need to be recalculated.

Baking takes a **lot** of compute power (hence time).
Depending on the scene, it might be preferable to bake overnight.

If the mesh has modifiers, the rendering settings are used for exporting the mesh to the fluid solver.
Depending on the setting, calculation times and memory use might exponentially increase.
For example, when using a moving mesh with *Subdivision Surface* as an obstacle,
it might help to decrease simulation time by switching it off, or to a low subdivision level.
When the setup/rig is correct, you can always increase settings to yield a more realistic result.

.. seealso::

   For other options see the :doc:`General Baking </physics/baking>` docs for more information.

Type
   Todo.

Cache Directory
   Directory and file prefix to store baked surface meshes.

Start
   Frame on which to start the simulation.
End
   Frame on which to stop the simulation.

   .. note::

      The simulation is only calculated for positive frames
      between the *Start* and *End* frames of the *Cache* panel, whether you bake or not.
      So if you want a simulation that is longer than the default frame range you have to change the *End* frame.

Data File Format
   File format that the cache data is to be stored.

   Uni Cache
      Blender's own caching format.
   OpenVDB
      Advanced and efficient storage method developed by
      `DreamWorks Animation <http://www.dreamworksanimation.com/>`__.

      The simulation fields can be found in the ``.vdb`` files under the following names:

      - "color"
      - "density"
      - "heat"
      - "heat old" (the temperature at the previous frame)
      - "flame"
      - "fuel"
      - "react" (reaction coordinates, used for fire)
      - "velocity"
      - "shadow" (the shadows of the volume computed for viewport rendering)
      - "texture coordinates" (used for turbulence)

      .. Compression
      ..    Method of data compression.
      ..
      ..    Zip
      ..       Efficient but slower compression method.
      ..    Blosc
      ..       Multi-threaded compression with about the same quality and size as ``Zip``.
      ..    None
      ..       Do not compress the data.
      ..
      .. Data Depth
      ..    Bit depth for writing all scalar (including vectors), lower values reduce the file size of the cache.
      ..
      ..    Float (Half)
      ..       Half float (16 bit data). Gives less data with the benefit of smaller file sizes.
      ..    Float (Full)
      ..       Full float (32 bit data). Gives more data at the cost of larger file sizes.

Particle File Format :guilabel:`Liquids Only`
   File format that the cache data is to be stored.
Mesh File Format :guilabel:`Liquids Only`
   File format that the cache data is to be stored.

Bake All, Free All
   Perform the actual fluid simulation. Blender will continue to work normally,
   except the progress will be displayed in the status bar.
   Pressing :kbd:`Esc` or the "X" button next to the status bar will abort the simulation.

   Once the simulation has been baked, the cache can be deleted by pressing *Free All*.


.. _bpy.types.FluidDomainSettings.export_manta_script:

Advanced
========

Export Mantaflow Script
   Todo.
