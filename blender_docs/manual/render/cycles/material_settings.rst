.. _bpy.types.CyclesMaterialSettings:

*****************
Material Settings
*****************

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Material --> Settings` and :menuselection:`Shader Editor --> Sidebar --> Settings`


Surface
=======

Multiple Importance Sample
   By default objects with emitting materials use both direct and indirect light sampling methods,
   but in some cases it may lead to less noise overall to disable direct light sampling for some materials.
   This can be done by disabling the *Multiple Importance Sample* option.
   This is especially useful on large objects that emit little light compared to other light sources.

   This option will only have an influence if the material contains an emission node; otherwise it will be disabled.

Transparent Shadows
   Use transparent shadows if it contains a :doc:`Transparent BSDF </render/shader_nodes/shader/transparent>`,
   disabling will render faster but will not give accurate shadows.

.. _bpy.types.CyclesMaterialSettings.displacement:
.. _cycles-materials-settings-displace:

Displacement Method
   Method used to perform :doc:`Displacement </render/materials/components/displacement>` on materials.

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


Volume
======

Similar volume settings as the :ref:`World settings <render-cycles-integrator-world-settings>` per material.
