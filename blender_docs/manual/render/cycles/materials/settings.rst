.. _bpy.types.CyclesMaterialSettings:

*****************
Material Settings
*****************

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Material --> Settings`

.. figure:: /images/render_cycles_materials_settings_panel.png
   :align: right

   Material Settings.


Surface
=======

Multiple Importance Sample
   By default objects with emitting materials use both direct and indirect light sampling methods,
   but in some cases it may lead to less noise overall to disable direct light sampling for some materials.
   This can be done by disabling the *Multiple Importance Sample* option.
   This is especially useful on large objects that emit little light compared to other light sources.

   This option will only have an influence if the material contains an emission node; 
   otherwise it will be automatically disabled.

Transparent Shadows
   Use transparent shadows if it contains a :doc:`Transparent BSDF </render/cycles/nodes/types/shaders/transparent>`,
   disabling will render faster but will not give accurate shadows.


Volume
======

Similar volume settings as the :ref:`World settings <render-cycles-integrator-world-settings>` per material.


.. _bpy.types.CyclesMaterialSettings.displacement:
.. _cycles-materials-settings-displace:

Displacement
============

.. note::

   These Options are only available if :ref:`Experimental Feature Set <cycles-experimental-features>` is turned on.

Displacement Method
   Method used to perform :doc:`Displacement </render/cycles/materials/displacement>` on materials.

   Displacement Only
      Mesh vertices will be displaced before rendering, modifying the actual mesh.
      This gives the best quality results, if the mesh is finely subdivided.
      As a result, this method is also the most memory intensive.
   Bump only
      When executing the surface shader, a modified surface normal is used instead of the true normal.
      This is a less memory intensive alternative to actual displacement, but only an approximation.
      Surface silhouettes will not be accurate and there will be no self-shadowing of the displacement.
   Displacement and Bump
      Both methods can be combined, to do displacement on a coarser mesh,
      and use bump mapping for the final detail.


Viewport Settings
=================

Viewport Color
--------------

Color
   Diffuse color of the object in the 3D viewport.
Alpha
   Transparency of the object in the 3D viewport.


Viewport Specular
-----------------

Color
   Specular reflection color of the object in the 3D viewport.
Hardness
   Roughness control for the object in the 3D viewport.


Viewport Alpha
--------------

Blend Mode
   :term:`Blend modes` for transparent faces.

   Opaque
      Render color of textured face as color.
   Add
      Render transparent and add color of face.
   Alpha Clip
      Use the image alpha values clipped with no blending (binary alpha).
   Alpha Blend
      Render polygon transparent, depending on alpha channel of the texture.
   Alpha Sort
      Sort faces for correct alpha drawing (slow, use *Alpha Clip* instead when possible).
   Alpha Anti-Aliasing
      Use texture alpha to add an anti-aliasing mask, requires multi-sample OpenGL display.


Pass Index
----------

Pass Index
   Index number for the *Material Index* :doc:`render pass </render/cycles/settings/scene/render_layers/passes>`.
   This can be used to give a mask to a material and then be read with
   the :doc:`ID Mask Node </compositing/types/converter/id_mask>` in the compositor.
