.. _bpy.types.Brush:
.. _bpy.ops.brush:
.. _bpy.types.Brush.use_custom_icon:
.. _bpy.types.Brush.icon_filepath:
.. _bpy.types.UnifiedPaintSettings:

*****
Brush
*****

For painting modes each brush type is exposed as a tool,
the brush can be changed from the tool setting.

.. figure:: /images/sculpt-paint_brush_brush_data-block-menu.png
   :align: right

   Brush data-block menu.

Brushes
   The :ref:`ui-data-block` to select a preset brush type or a custom brush.
   They are a combination of a "tool", along with stroke, texture, and options.

   Add Brush
      When you add a brush, the new brush is a clone of the current one.

   Brush Specials
      Enabled Modes
         Todo.
      Tool Selection
         Todo.
      Reset Brush
         Todo.

      Custom Icon
         Allows definition of a custom brush icon.

   .. note::

      In order to save in a blend-user a custom brush, enable Fake User.

Radius
   The size of the brush can be changed by the :kbd:`[` and :kbd:`]` shortcuts.

Autosmooth
   Amount of smoothing to apply to each stroke.

Inverse Autosmooth
   Lighter pressure causes more smoothing to apply.

Height
   Simulated height of brush.


Options
=======

Accumulate
   Accumulate stroke daubs on top of each other.

Radius Unit
   View
      Measure brush size relative to the screen.
   Scene
      Measure brush size relative to the scene.

Original Normal
   Keep using the normal of the initial location where the stroke originated.

Front Faces Only
   Brush only affects vertices that face the viewer.

2D Falloff
   Apply brush influence in 2D circle instead of a sphere.
