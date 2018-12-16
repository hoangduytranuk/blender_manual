.. rename to numeric input?

**************
Number Buttons
**************

.. figure:: /images/interface_controls_buttons_number_number-button.png
   :align: right

   Number buttons.

   (grouped or single).

Number buttons hold numeric values.

Number buttons can be identified by the triangles pointing left (◂) and right (▸) on the sides of the button.
The second type number sliders have a bar in the background and are used for values in a range,
e.g. percentage values. Both types have round corners.
In most cases they contain a name and a colon followed by the number.
The value can be edited in several ways:

In/Decremental Steps
   To change the value in steps, click :kbd:`LMB` on the small triangles (number button only).
Dragging
   To change the value in a wider range, hold down :kbd:`LMB` and drag the mouse to the left or right.
   Hold :kbd:`Ctrl` to snap to the discrete steps while dragging or :kbd:`Shift` for precision input.
Text Input
   Press :kbd:`LMB` or :kbd:`Return` to edit the value as a text field.

   When entering values by hand, this button works like any other text field:

   - Press :kbd:`Return` or :kbd:`LMB` outside the field to apply the change.
   - Press :kbd:`Esc` or :kbd:`RMB` will cancel the value.
   - Press :kbd:`Tab` to jump to the next number button or :kbd:`Ctrl-Tab` for the previous.
   - Press :kbd:`Minus` while hovering over the button to negate the value.


Multi-Value Editing
===================

.. figure:: /images/interface_controls_buttons_number_multi-value-edit.png
   :align: right

   Multi-value editing.

Number buttons can edit multiple values at once (object scale or render resolution for example).
This can be done by clicking on the button and dragging vertically to include buttons above/below.
After the vertical motion you can drag from side to side, or release the :kbd:`LMB` to type in a value.


Limits
======

Most *Number Buttons* have two types of "limits" imposed on them. The first of these is a "soft limit",
this means that the property cannot surpass the value of the "soft limit" without having to :kbd:`LMB`
and input the value with the numpad. The second is the "hard limit",
this is the value that cannot be surpassed even by :kbd:`LMB` and inputing a value.


Expressions
===========

.. Do not use mathjax here

You can also enter expressions such as ``3*2`` instead of ``6``. or ``5/10+3``.
Even constants like ``pi`` (3.142) or functions like ``sqrt(2)`` (square root of 2)
may be used.

.. seealso::

   These expressions are evaluated by Python; for all available math expressions see:
   `Math module reference <https://docs.python.org/3/library/math.html>`__.


Expressions as Drivers
----------------------

You may want your expression to be re-evaluated after it is entered.
Blender supports this using :doc:`Drivers </animation/drivers/index>` (a feature of the animation system).

Expression beginning with ``#``, have a special use.
Instead of evaluating the value and discarding the expression,
a driver is added to the property with the expression entered.

The expression ``#frame`` is a quick way to access map a value to the current frame,
but more complex expressions are also supported ``#fmod(frame, 24) / 24`` for example.

This is simply a convenient shortcut to add drivers which can also be added via the :kbd:`RMB` menu.


Units
=====

As well as expressions, you can mix units with numbers; for this to work,
units need to be set in the :ref:`scene settings <data-scenes-props-units>`.

To use units simply write either the unit abbreviation or the full name after the value.

Examples of valid units include:

.. hlist::
   :columns: 2

   - ``1cm``
   - ``1m 3mm``
   - ``1m, 3mm``
   - ``2ft``
   - ``3ft/0.5km``
   - ``2.2mm + 5' / 3" - 2yards``

.. note:: Using Units

   - Commas are optional.
   - You can mix between metric and imperial even though you can only show one at a time.
   - Plurals of the names are recognized too, so ``meter`` and ``meters`` can both be used.
