.. _bpy.types.ShaderNodeLightPath:

***************
Light Path Node
***************

.. figure:: /images/render_shader-nodes_input_light-path_node.png
   :align: right

   Light Path Node.

The *Light Path* node is used to find out for which kind of incoming ray the shader is being executed;
particularly useful for non-physically-based tricks. More information about the meaning of each type
is in the :doc:`Light Paths </render/cycles/render_settings/light_paths>` documentation.


Inputs
======

This node has no inputs.


Properties
==========

This node has no properties.


Outputs
=======

Is Camera Ray
   1.0 if shading is executed for a camera ray, 0.0 otherwise.
Is Shadow Ray
   1.0 if shading is executed for a shadow ray, 0.0 otherwise.
Is Diffuse Ray
   1.0 if shading is executed for a diffuse ray, 0.0 otherwise.
Is Glossy Ray
   1.0 if shading is executed for a glossy ray, 0.0 otherwise.
Is Singular Ray :guilabel:`Cycles Only`
   1.0 if shading is executed for a singular ray, 0.0 otherwise.
Is Reflection Ray :guilabel:`Cycles Only`
   1.0 if shading is executed for a reflection ray, 0.0 otherwise.
Is Transmission Ray :guilabel:`Cycles Only`
   1.0 if shading is executed for a transmission ray, 0.0 otherwise.
Ray Length :guilabel:`Cycles Only`
   Distance traveled by the light ray from the last bounce or camera.
Ray Depth
   Number of times the ray been reflected or transmitted on interaction with a surface.

   .. note::

      Passing through a transparent shader
      :ref:`does not count as a normal "bounce" <render-cycles-light-paths-transparency>`.

Diffuse Depth :guilabel:`Cycles Only`
   Number of times of times the ray has gone through diffuse reflection or transmission.
Glossy Depth :guilabel:`Cycles Only`
   Number of times of times the ray has gone through glossy reflection or transmission.
Transparent Depth :guilabel:`Cycles Only`
   Returns the number of transparent surfaces passed through.
Transmission Depth :guilabel:`Cycles Only`
   Replace a Transmission light path after X bounces with another shader, e.g. a Diffuse one.
   This can be used to avoid black surfaces, due to low amount of max bounces.
