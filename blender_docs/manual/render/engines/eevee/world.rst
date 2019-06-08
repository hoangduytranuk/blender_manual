
*****
World
*****

The world environment can emit light, ranging from a single solid color
to arbitrary textures. It works the same as the :doc:`world material </render/engines/cycles/world>` in Cycles.

In Eevee, the world lighting contribution is first rendered and
stored in smaller resolution textures before being applied to the objects.
This makes the lighting less precise than Cycles.

.. seealso::

   :doc:`Indirect Lighting </render/engines/eevee/indirect_lighting>`.
