
*****
Usage
*****

Drivers can be added to properties via their context menu, a shortcut, copy-pasted,
or by typing directly into the property's value.

After adding drivers, they are usually modified in the :doc:`Drivers editor </editors/drivers_editor>`,
or via a simplified *Edit Driver* popover invoked from the property context menu.


Add Driver
==========

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Context menu --> Add Driver`
   :Hotkey:    :kbd:`Ctrl-D`

The common way to add a driver to a property is to :kbd:`RMB` click a property,
then add a driver via the context menu.
Drivers can also be added by pressing :kbd:`Ctrl-D` with the mouse over the property set.

This operation adds a driver with a single variable (which needs to be filled in),
and displays the *Edit Driver* popover.


Edit Driver
===========

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Context menu --> Edit Driver`

Displays a popover window that allows editing the custom expression and input variables
of the driver without opening the full *Drivers Editor*.

Many drivers don't use their :doc:`F-Curve </editors/graph_editor/fcurves/introduction>`
component, so this reduced interface is sufficient.


Open Drivers Editor
===================

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Context menu --> Open Drivers Editor`

Opens a new window with the *Drivers Editor* and
selects the driver associated with the property.


Copy & Paste
============

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Context menu --> Copy Driver`
   :Menu:      :menuselection:`Context menu --> Paste Driver`

Drivers can be copied and pasted via the context menu.
When adding drivers with the same settings, this can save time modifying settings.


Expression
==========

This is a quick way to add drivers with a scripted expression.
First click the property you want to add a driver to, then add a hash ``#`` and a scripted expression.

Some examples:

- ``#frame``
- ``#frame / 20.0``
- ``#sin(frame)``
- ``#cos(frame)``


Removing Drivers
================

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Context menu --> Delete Driver(s)`
   :Menu:      :menuselection:`Context menu --> Delete Single Driver`
   :Hotkey:    :kbd:`Ctrl-Alt-D`

Removes driver(s) associated with the property, either for the single selected property
or sub-channel or all components of a vector.
