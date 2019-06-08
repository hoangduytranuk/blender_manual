.. _bpy.types.Brush:
.. _bpy.ops.brush:

*****
Brush
*****

.. figure:: /images/sculpt-paint_brush_data-block-menu.png
   :align: right

   Brush data-block menu.

Brushes
   The :ref:`ui-data-block` to select a preset brush type or a custom brush.
   They are a combination of a "tool", along with stroke, texture, and options.

   The brush can be selected by numbers:
   :kbd:`0` to :kbd:`9` and :kbd:`Shift-0` to :kbd:`Shift-9`.

   Add ``+``
      When you add a brush, the new brush is a clone of the current one.

.. note::

   In order to save in a blend-user a custom brush, set a Fake User.

- Increase/decrease brush size :kbd:`[` and :kbd:`]`


Radial Control
==============

- Set brush size :kbd:`F`
- Set brush strength :kbd:`Shift-F`
- Rotate brush texture :kbd:`Ctrl-F`

You can then either adjust the value interactively or by typing in numbers.
After pressing the hotkey move the mouse to increase/reduce the value
(additionally with precision and/or snapping activated).
Finally confirm (:kbd:`LMB`, :kbd:`Return`) or cancel (:kbd:`RMB`, :kbd:`Esc`).


.. TODO: Move to own page (manual/sculpt_paint/options.rst), add refboxes
.. _sculpt-paint-brush-appearance:

Options
=======

Overlay
-------

.. figure:: /images/sculpt-paint_brush_appearance-panel.png
   :align: right

   Brush appearance options.

.. Tool Shelf --> Options --> Overlay panel

Allows you to customize the display in the viewport of the *Curve* and *Texture* that is applied to the brush.

View
   The eye icon is used as a toggle to show or hide the given brush texture.
Alpha
   You can change the amount of transparency used when showing the texture using the *Alpha* slider.
Stroke Overlay
   The brush icon allows you to turn off the viewport overlay during strokes.


Appearance
----------

.. figure:: /images/sculpt-paint_sculpting_introduction_brush-circle.png
   :align: right

   Brush cursor.

.. Tool Shelf --> Options --> Appearance panel

Allows you to customize the color of the brush radius outline and to specify a custom icon.

Show Brush
   Shows the brush shape in the viewport.
Color
   Set the color of the brush ring.
Custom Icon
   Allows definition of a custom brush icon.
