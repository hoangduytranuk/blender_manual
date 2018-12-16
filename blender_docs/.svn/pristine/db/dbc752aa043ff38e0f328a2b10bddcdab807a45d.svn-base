
********************
Numeric Input Fields
********************

.. figure:: /images/interface_controls_buttons_number_number-button.png
   :align: right

   Numeric input fields.

Numeric input fields store values and units.

First type of numeric input field shows triangles pointing left (◂) and right (▸)
on the sides of the field when mouse pointer is on top of the field.
Second field type sliders have a colored bar in the background
to illustrate value over a range, e.g. percentage values.

The value can be edited in several ways:

Incremental Steps
   To change the value in unit steps, click :kbd:`LMB` on the small triangles
   (only available on first field type).
   You can also use :kbd:`Ctrl-Wheel` while hovering over the field to edit the value.
Dragging
   To change the value with mouse, hold down :kbd:`LMB` and drag to left or right.

   .. TODO, this is not currently working: Hold :kbd:`Ctrl` to snap to the discrete steps
      while dragging or :kbd:`Shift` for precision input.

Keyboard Input
   Press :kbd:`LMB` or :kbd:`Return` to enter value by typing it with keyboard.

   When entering values by keyboard, numeric fields work like text fields:

   - Press :kbd:`Return` or :kbd:`LMB` outside the field to apply the change.
   - Press :kbd:`Esc` or :kbd:`RMB` to cancel.
   - Press :kbd:`Tab` to jump to the next field or :kbd:`Ctrl-Tab` to go to the previous field.
   - Press :kbd:`Minus` while hovering over a numeric field to negate the value.


Multi-Value Editing
===================

.. figure:: /images/interface_controls_buttons_number_multi-value-edit.png
   :align: right

   Multi-value editing.

You can edit multiple numeric fields at once by pressing down
:kbd:`LMB` on the first field, and then drag vertically over
the fields you want to edit. Finally you can either drag left or right to
adjust value with mouse, or release the :kbd:`LMB` and type in a value.


Value Limits
============

Most numerical values are restricted by "soft limit" and "hard limit" value ranges.
Changing value by dragging with mouse is restricted to "soft limit" value range.
Input via keyboard can allow use of wider value range, but never wider than "hard limit".


Expressions
===========

.. Do not use mathjax here

You can enter mathematical expressions into any numerical input field.
For example, enter ``3*2`` or ``10/5+4`` instead of ``6``.
Even constants like ``pi`` (3.142) or functions like ``sqrt(2)`` (square root of 2)
may be used.

.. seealso::

   These expressions are evaluated by Python; for all available math expressions see:
   `Math module reference <https://docs.python.org/3/library/math.html>`__.


Expressions as Drivers
----------------------

You may want your expression to be re-evaluated after it is entered.
Blender supports this using :doc:`Drivers </animation/drivers/index>` (a feature of the animation system).

Expressions beginning with ``#`` have a special use.
Instead of evaluating the value and discarding the expression,
a driver is added to the property with the expression entered.

The expression ``#frame`` is a quick way to access map a value to the current frame,
but more complex expressions are also supported ``#fmod(frame, 24) / 24`` for example.

This is simply a convenient shortcut to add drivers which can also be added via the :kbd:`RMB` menu.


Units
=====

As well as expressions, you can specify numbers and units.
If no unit is given, then a default unit is applied.
The unit system can be changed in :ref:`scene settings <data-scenes-props-units>`.

You can use either the unit abbreviation or the full name after the value.

Examples of valid usage of length units include:

.. hlist::
   :columns: 2

   - ``1cm``
   - ``1m 3mm``
   - ``1m, 3mm``
   - ``2ft``
   - ``3ft/0.5km``
   - ``2.2mm + 5' / 3" - 2yards``

.. note:: Using Units

   - Decimal separator is optional.
   - You can mix units, e.g. metric and imperial even though you can only show one at a time.
   - Plurals of the names are recognized too, so ``meter`` and ``meters`` can both be used.
