.. _bpy.types.ShaderNodeTexWave:

*****************
Wave Texture Node
*****************

.. figure:: /images/render_shader-nodes_textures_wave_node.png
   :align: right

   Wave Texture Node.

The *Wave Texture* node adds procedural bands or rings with noise distortion.


Inputs
======

Vector
   Texture coordinate to sample texture at;
   defaults to Generated texture coordinates if the socket is left unconnected.
Scale
   Overall texture scale.
Distortion
   Amount of distortion of the wave (similar to the Marble texture in Blender Internal).
Detail
   Amount of distortion noise detail.
Detail Scale
   Scale of distortion noise.


Properties
==========

Type
   *Bands* or *Rings* shaped waves.
Wave Profile
   Controls the look of the wave type.

   Saw
      Uses a sawtooth profile.
   Sine
      Uses the standard sine profile.


Outputs
=======

Color
   Texture color output.
Factor
   Texture intensity output.


Examples
========

.. figure:: /images/render_shader-nodes_textures_wave_default.jpg
   :width: 200px

   Default wave texture.
