.. _bpy.types.ShaderNodeTexNoise:

******************
Noise Texture Node
******************

.. figure:: /images/render_shader-nodes_textures_noise_node.png
   :align: right

   Noise Texture Node.

The *Noise Texture* node evaluates a fractal Perlin noise at the input texture coordinates.
The noise can be evaluated in 1D, 2D, 3D, and 4D dimensions.

Inputs
======

The inputs are dynamic. In particular, the *Vector* input is only available in the 2D, 3D, and 4D dimensions,
while the *W* input is only available in the 1D and 4D dimensions.

Vector
   Texture coordinate to evaluate the noise at;
   defaults to *Generated* texture coordinates if the socket is left unconnected.
W  
   Texture coordinate to evaluate the noise at.
Scale
   Scale of the base noise octave.
Detail
   Number of noise octaves.
   The fractional part of the input is multiplied by the magnitude of the last octave.
   Higher number of octaves corresponds to a higher render time.
Distortion
   Amount of distortion.

Properties
==========

Dimensions
   The dimensions of the space to evaluate the noise in.

   1D
      Evaluate the noise in 1D space at the input *W*.
   2D
      Evaluate the noise in 2D space at the input *Vector*. The z component is ignored.
   3D
      Evaluate the noise in 3D space at the input *Vector*.
   4D
      Evaluate the noise in 4D space at the input *Vector* and the input *W* as the fourth dimension.

Higher dimensions corresponds to higher render time, so lower dimensions should be used unless higher dimensions are necessary. 

Outputs
=======

Factor
   Value of fractal noise.  
Color
   Color with different fractal noises in each component.

Examples
========

.. figure:: /images/render_shader-nodes_textures_noise_example.jpg

   Noise Texture with high detail.
