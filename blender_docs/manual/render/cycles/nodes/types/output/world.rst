.. _bpy.types.ShaderNodeOutputWorld:

**********
World Node
**********

.. figure:: /images/render_cycles_nodes_types_output_world_node.png
   :align: right

   World Node.

The *World Output* node is used to output light a color information
to the scene's :doc:`World </render/cycles/world>`.


Inputs
======

Surface
   The appearance of the environment,
   usually preceded by a :doc:`Background </render/cycles/nodes/types/shaders/background>` shader.
Volume
   Used to add volumetric effects to the world.
   See the :doc:`Volume Absorption </render/cycles/nodes/types/shaders/volume_absorption>`
   and :doc:`Volume Scatter </render/cycles/nodes/types/shaders/volume_scatter>` for more information.

   .. note::

      It is not possible to have an HDR and volumetric due to the fact that
      HDR's are assumed to be an infinite distance from the camera.


Properties
==========

This node has no properties.


Outputs
=======

This node has no outputs.
