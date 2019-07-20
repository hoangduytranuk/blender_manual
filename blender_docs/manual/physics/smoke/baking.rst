
************************
Baking Smoke Simulations
************************

.. TODO2.8:
   .. figure:: /images/physics_smoke_baking_interface.png
      :align: right

      *Smoke Cache* options.

:term:`Baking` is used to store the outcome of a simulation so it does not need to be recalculated.

Smoke baking settings are in :menuselection:`Properties --> Physics --> Smoke --> Cache`.
Unlike most physics simulations smoke physics has some settings that are specific to smoke.


File Format
===========

File format that the cache data is to be stored.


Point Cache
-----------

Blender's own caching format.


OpenVDB
-------

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

Compression
   Method of data compression.

   Zip
      Efficient but slower compression method.
   Blosc
      Multi-threaded compression with about the same quality and size as ``Zip``.
   None
      Do not compress the data.

Data Depth
   Bit depth for writing all scalar (including vectors), lower values reduce the file size of the cache.

   Float (Half)
      Half float (16 bit data). Gives less data with the benefit of smaller file sizes.
   Float (Full)
      Full float (32 bit data). Gives more data at the cost of larger file sizes.

.. seealso::

   For other options see the :doc:`General Baking </physics/baking>` docs for more information.

.. note::

   Baking can only been done once your blend-file is saved.
   If your blend-file has not been saved, the *Smoke Cache* panel will be disabled.
