.. _bpy.types.ShaderNodeOutputMaterial:

*************
Material Node
*************

.. figure:: /images/render_cycles_nodes_types_output_material_node.png
   :align: right

   Material Node.

The *Material Output* node is used to output surface material information to a surface object.


Inputs
======

Surface
   The surface output of the material.
Volume
   Used to output of the different volume shaders.

   .. seealso::

      The types of volume shaders are:

      - :doc:`Emission </render/shaders/nodes/types/shaders/emission>` shader.
      - :doc:`Volume Absorption </render/shaders/nodes/types/shaders/volume_absorption>` shader.
      - :doc:`Volume Scatter </render/shaders/nodes/types/shaders/volume_scatter>` shader.

Displacement
   Used to create bump mapping or actual subdivided :doc:`Displacement </render/engines/cycles/materials/displacement>`.


Properties
==========

This node has no properties.


Outputs
=======

This node has no outputs.
