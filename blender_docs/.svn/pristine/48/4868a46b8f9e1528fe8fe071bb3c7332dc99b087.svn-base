
************
Introduction
************

Drivers are small scripts with the purpose of controlling properties with other properties.
For example, the rotation of one object can be controlled by the location of another object.

Effectively, drivers are animation :doc:`F-Curves </editors/graph_editor/fcurves/introduction>`
that use a custom expression as the X axis input instead of the current frame.

.. seealso::

   :doc:`Auto run </advanced/scripting/security>`


Adding & Removing
=================

There are some different ways to add drivers in Blender.
After adding drivers they are usually modified in the *Graph Editor* with the mode set to *Drivers*,
or via a simplified *Edit Driver* popover invoked from the property context menu.


Add Driver
----------

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Context menu --> Add Driver`
   :Hotkey:    :kbd:`Ctrl-D`

The common way to add a driver to a property is to :kbd:`RMB` click a property,
then add a driver via the context menu.
Drivers can also be added by pressing :kbd:`Ctrl-D` with the mouse over the property set.

This operation adds a driver with a single variable (but not filled in), and displays the *Edit Driver* popover.


Edit Driver
-----------

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Context menu --> Edit Driver`

Displays a popover window that allows editing the custom expression and input variables
of the driver without opening the full *Graph Editor*.

Most drivers don't use their :doc:`F-Curve </editors/graph_editor/fcurves/introduction>`
component, so this reduced interface is sufficient.


Open Drivers Editor
-------------------

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Context menu --> Open Drivers Editor`

Opens a new window with the *Graph Editor* in the *Drivers* mode, and
selects the driver associated with the property.


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

   :Menu:      :menuselection:`Context menu --> Delete (Single) Driver(s)`
   :Hotkey:    :kbd:`Ctrl-Alt-D`

Removes driver(s) associated with the property, either for the single selected sub-channel or all of them.


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
