.. (TODO) it was updated in 2.79.5
   https://wiki.blender.org/wiki/Reference/Release_Notes/2.80/Cycles#Ambient_Occlusion_Shader

.. _bpy.types.ShaderNodeAmbientOcclusion:

*****************
Ambient Occlusion
*****************

.. figure:: /images/render_cycles_nodes_types_shaders_ao_node.png
   :align: right

   Ambient Occlusion.

The *Ambient Occlusion* shader node gives per-material control for the amount of AO.
When AO is enabled in the world, it affects all diffuse BSDFs in the scene.
With this option it is possible to let only some materials be affected by AO,
or to let it influence some materials more or less than others.


Inputs
======

Color
   Surface reflection color.


Properties
==========

This node has no properties.


Outputs
=======

AO
   Standard shader output.


Example
=======

.. figure:: /images/render_cycles_nodes_types_shaders_ao_example.jpg

   White AO shader.
