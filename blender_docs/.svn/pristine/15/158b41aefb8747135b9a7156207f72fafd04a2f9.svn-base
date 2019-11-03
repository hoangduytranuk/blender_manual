
******
Passes
******

Passes can be used to split rendered images into colors, direct and indirect light to edit them individually,
and also to extract data such as depth or normals.


.. _render-cycles-passes:

Cycles
======

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Scene --> View Layers --> Passes`

Passes can be used to split rendered images into colors, direct and indirect light to edit them individually,
and also to extract data such as depth or normals.


Lighting Passes
---------------

Combined
   The final combination of render passes with everything included.
Noisy Image
   If denoising is enabled, the original combined pass before denoising.

Diffuse Direct
   Direct lighting from diffuse BSDFs. We define direct lighting as coming from lights, emitting surfaces,
   the background, or ambient occlusion after a single reflection or transmission off a surface.
   BSDF color is not included in this pass.
Diffuse Indirect
   Indirect lighting from diffuse BSDFs. We define indirect lighting as coming from lights,
   emitting surfaces or the background after more than one reflection or transmission off a surface.
   BSDF color is not included in this pass.
Diffuse Color
   Color weights of diffuse BSDFs. These weights are the color input socket for BSDF nodes,
   modified by any Mix and Add Shader nodes.
Glossy Direct, Indirect, Color
   Same as above, but for glossy BSDFs.
Transmission Direct, Indirect, Color
   Same as above, but for transmission BSDFs.
Subsurface Direct, Indirect, Color
   Same as above, but for subsurface BSDFs.
Emission
   Emission from directly visible surfaces.
Environment
   Emission from the directly visible background. When the film is set to transparent,
   this can be used to get the environment color and composite it back in.
Shadow
   Shadows from light objects. Mostly useful for compositing objects with shadow into existing footage.
Ambient Occlusion
   Ambient occlusion from directly visible surfaces. BSDF color or AO factor is not included; i.e.
   it gives a 'normalized' value between 0 and 1.

.. note::

   :doc:`Transparent BSDFs are given special treatment </render/cycles/render_settings/light_paths>`.
   A fully transparent surface is treated as if there is no surface there at all;
   a partially transparent surface is treated as if only part of the light rays can pass through.
   This means it is not included in the Transmission passes;
   for that a glass BSDF with index of refraction 1.0 can be used.


Combining
^^^^^^^^^

All these lighting passes can be combined to produce the final image as follows:

.. figure:: /images/render_layers_passes_combine.svg


Data Passes
-----------

Z
   Distance to any visible surfaces.

   .. note::

      The Z pass only uses one sample.
      When depth values need to be blended in case of motion blur or :term:`Depth of Field`, use the mist pass.

Mist
   Distance to visible surfaces, mapped to the 0.0-1.0 range.
   When enabled, settings are in :ref:`World tab <render-cycles-integrator-world-mist>`.
   This pass can be used in compositing to fade out objects that are farther away.

Normal
   Surface normal used for shading.
Vector
   Motion vectors for the vector blur node. The four components consist of 2D vectors
   giving the motion towards the next and previous frame position in pixel space.
UV
   Default render UV coordinates.
Object Index
   Creates a mask of the object that can be later read by
   the :doc:`ID Mask Node </compositing/types/converter/id_mask>` in the compositor.
Material Index
   Creates a mask of the material that can be later read by
   the :doc:`ID Mask Node </compositing/types/converter/id_mask>` in the compositor.
Denoising Data
   Passes needed by the denoiser, for performing animation denoising in a second pass
   after rendering the entire animation. For still image denoising as part of
   the render process these are not needed.

.. note:: The Z, Object Index and Material Index passes are not anti-aliased.

Alpha Threshold
   Z, Index, normal, UV and vector passes are
   only affected by surfaces with alpha transparency equal to or higher than this threshold.
   With value 0.0 the first surface hit will always write to these passes, regardless of transparency.
   With higher values surfaces that are mostly transparent can be skipped until an opaque surface is encountered.


Cryptomatte
-----------

Cryptomatte is a standard to efficiently create mattes for compositing.
Cycles outputs the required render passes, which can then be used in the Blender compositor
or another compositor with Cryptomatte support to create masks for specified objects.

Unlike the Material and Object Index passes, the objects to isolate are selected in compositing,
and mattes will be anti-aliased and take into account effects like motion blur and transparency.

Object
   Render cryptomatte object pass, for isolating objects in compositing.
Material
   Render cryptomatte material pass, for isolating materials in compositing.
Asset
   Render cryptomatte material pass, for isolating materials in compositing.

Levels
   Sets how many unique objects can be distinguished per pixel.
Accurate Mode
   Generate a more accurate Cryptomatte pass. CPU only, may render slower and use more memory.


Typical Workflow
^^^^^^^^^^^^^^^^

#. Enable Cryptomatte Object render pass in the Passes panel, and render.
#. In the compositing nodes, create a Cryptomatte node and
   link the Render Layer matching Image and Cryptomatte passes to it.
#. Attach a Viewer node to the Pick output of the Cryptomatte node.
#. Use the Cryptomatte Add/Remove button to sample objects in the Pick Viewer node.
#. Use the Matte output of the Cryptomatte node to get the alpha mask.

.. seealso::

   :doc:`Cryptomatte Node </compositing/types/matte/cryptomatte>`.


.. _render-eevee-passes:

Eevee
=====

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Scene --> View Layers --> Passes`


Lighting Passes
---------------

Combined
   The final combination of render passes with everything included.
Subsurface Direct
   Direct lighting from subsurface BSDFs. We define direct lighting as coming from lights, emitting surfaces,
   the background, or ambient occlusion after a single reflection or transmission off a surface.
   BSDF color is not included in this pass.
Subsurface Color
   Color weights of subsurface BSDFs. These weights are the color input socket for BSDF nodes,
   modified by any Mix and Add Shader nodes.
Ambient Occlusion
   Ambient occlusion from directly visible surfaces. BSDF color or AO factor is not included; i.e.
   it gives a 'normalized' value between 0 and 1.


Data Passes
-----------

Z
   Distance to any visible surfaces.

Mist
   Distance to visible surfaces, mapped to the 0.0 - 1.0 range.

Normal
   Surface normal used for shading.
