
************
Introduction
************

Drivers are scripts which main purpose is to control properties with other properties.
In example the rotation of one object is controlled with the location of another object.

.. seealso::

   :doc:`Auto run </advanced/scripting/security>`


Adding & Removing
=================

There are some different ways to add drivers in Blender.
After adding drivers they are usually modified in the *Graph Editor* with the mode set to *Drivers*.


Add Driver
----------

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Context menu --> Add Driver`
   :Hotkey:    :kbd:`Ctrl-D`

The common way to add a driver to a property is to :kbd:`RMB` click a property,
then add a driver via the context menu.
Drivers can also be added by pressing :kbd:`Ctrl-D` with the mouse over the property set.
The selected properties will be used as a destination (output) for the driver.

All from Target (properties icon)
   This will add drivers to the set of properties used as a destination.
   It creates a default curve with keyframes at (0, 0) and (1, 1),
   For example, it will add drivers to X, Y, and Z for Location.
Single from Target
   This will add a single driver to the selected property used as a destination.
Match Indices (color wheel icon)
   Use the corresponding index to drive the corresponding property on a similar sized vector/array property.
   This is useful for driving ``ob1.location`` with ``ob2.location``, or ``RGB color`` with ``XYZ location``.
Manually Create Later/(Single) (hand icon)
   It adds a/set of driver(s), each with a single variable (but not filled in). No eyedropper will appear.

The source/target (input) property can then be selected with an :ref:`ui-eye-dropper` (e.g. "Scale Y").

.. note::

   Due to the way that Blender's UI Context works, you'll need *two* Properties editor instances open
   (and to have pinned one of the two to show the properties for the unselected object).
   This is necessary as the UI cannot be manipulated while using eyedroppers to pick data.
   Therefore, you need to be able to see both the source and the destination properties when using the eyedropper.


Copy & Paste
------------

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Context menu --> Copy/Paste Driver`

Drivers can be copied and pasted in the UI, via the context menu.
When adding drivers with the same settings, this can save time modifying settings.


Expression
----------

This is a quick way to add drivers with a scripted expression.
First click the property you want to add a driver to, then add a hash ``#`` and a scripted expression.

Some examples:

- ``#frame``
- ``#frame / 20.0``
- ``#sin(frame)``
- ``#cos(frame)``


Removing Drivers
----------------

.. admonition:: Reference
   :class: refbox

   :Editor:    Graph editor
   :Mode:      Drivers
   :Panel:     :menuselection:`Properties region --> Driver --> Drivers --> Remove Driver`
   :Menu:      :menuselection:`Context menu --> Delete (Single) Driver(s)`
   :Hotkey:    :kbd:`Ctrl-Alt-D`

ToDo add.


Graph View
==========

.. figure:: /images/animation_drivers_introduction_fcurve.png
   :align: right

   Driver example in the Graph editor.

The main area of the :doc:`Graph editor </editors/graph_editor/index>` in Driver Mode
shows an :doc:`F-Curve </editors/graph_editor/fcurves/introduction>` that maps the Driver Value to
the target property. The Driver Value is the output of the driver script.
The X axis represents the Driver Value and the Y axis is the value of the target property.
In the example image, if the Driver Value is 2.0 the property will be 0.5.

The default F-curve is an identity map i.e. the value is not changed.
It can be used to create corrective drivers.
