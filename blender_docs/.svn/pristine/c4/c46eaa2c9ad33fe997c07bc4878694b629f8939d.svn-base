.. _bpy.types.SimplifyGpencilModifier:

*****************
Simplify Modifier
*****************

The *Simplify* modifier allows you to reduce the amount of points in the strokes.
The goal of this modifier is reduce points while maintaining the lines shape.

Apply the modifier can help to obtain a better performance (more FPS) while animating.


Options
=======

.. figure:: /images/grease-pencil_modifiers_generate_simplify_panel.png
   :align: right

   The Simplify modifier.

Mode
   Determines how to reduce points in the strokes.

   Fixed
      Deletes alternated points in the strokes, except the start and end points.

      Iterations
         Number of times to repeat the procedure.

   Adaptive
      Uses the RDP algorithm (Ramer-Douglas-Peucker algorithm) for points deletion.
      The algorithm try to obtain a similar line shape with fewer points.

      Factor
         Controls the amount of recursively simplifications applied by the algorithm.


Influence Filters
-----------------

See :ref:`grease-pencil-modifier-influence-filters`.


Example
=======

.. list-table:: Fixed Mode sample.

   * - .. figure:: /images/grease-pencil_modifiers_generate_simplify_fixed-iterations-0.png
          :width: 130px

          Original Model.

     - .. figure:: /images/grease-pencil_modifiers_generate_simplify_fixed-iterations-1.png
          :width: 130px

          Iteration: 1.

     - .. figure:: /images/grease-pencil_modifiers_generate_simplify_fixed-iterations-2.png
          :width: 130px

          Iteration: 2.

     - .. figure:: /images/grease-pencil_modifiers_generate_simplify_fixed-iterations-3.png
          :width: 130px

          Iteration: 3.

.. list-table:: Adaptive Mode sample.

   * - .. figure:: /images/grease-pencil_modifiers_generate_simplify_adaptive-factor-0.png
          :width: 130px

          Original Model.

     - .. figure:: /images/grease-pencil_modifiers_generate_simplify_adaptive-factor-01.png
          :width: 130px

          Factor: 0.1.

     - .. figure:: /images/grease-pencil_modifiers_generate_simplify_adaptive-factor-02.png
          :width: 130px

          Factor: 0.5.

     - .. figure:: /images/grease-pencil_modifiers_generate_simplify_adaptive-factor-05.png
          :width: 130px

          Factor: 1.
