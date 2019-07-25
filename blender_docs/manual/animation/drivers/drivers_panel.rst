
*************
Drivers Panel
*************

.. figure:: /images/animation_drivers_drivers-panel_panel.png
   :align: right

   Edit Driver popover.

.. admonition:: Reference
   :class: refbox

   :Editor:    Graph editor
   :Mode:      Drivers
   :Panel:     :menuselection:`Sidebar region --> Drivers`
   :Hotkey:    :kbd:`N`

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Context menu --> Edit Driver`
   :Hotkey:    :kbd:`Ctrl-D`

This panel is visible in Sidebar of the :doc:`Drivers Editor </editors/drivers_editor>`
or as a popover when adding a driver to a property.

It shows first the property that is being driven and next a series of settings
that determine how the driver works.


Driver Settings
===============

Type
----

There are two categories of drivers:

- **Built-in functions** (*Average*, *Sum*, *Min* and *Max*)

   The driven property will have the value of the average, sum, lowest or highest (respectively)
   of the values of the referenced *Driver Variables*.
   If there is only one driver variable, these functions will yield the same result.

- **Custom** (*Scripted Expression*).

   A mathematical or Python expression that can make use of the *Driver Variables*. See `Expressions`_.


Driver Value
------------

The current result of the driver setup. Useful for debug purposes.


Variables
---------

See  `Driver Variables`_.


Update Dependencies
-------------------

Forces an update for the Driver Value dependencies.


Show in Drivers Editor
----------------------

Opens the fully featured :doc:`Drivers Editor </editors/drivers_editor>`.
This button only shows in the popover version of the Drivers panel.


Driver Variables
================

Variables are references to properties, transformation channels, or the result of a comparison
between transformations of two objects.

Drivers should access object data via *Driver Variables*, rather than direct references in a Python
expression, in order for dependencies to be correctly tracked.

Add Input Variable
   Adds a new Driver Variable.
Copy/Paste
   Copies of the current variable stack so it can be pasted onto another driver's variable stack.

.. list-table::

   * - .. figure:: /images/animation_drivers_drivers-panel_single-property.png

          Single property.

     - .. figure:: /images/animation_drivers_drivers-panel_transform-channel2.png

          Transform channel.

     - .. figure:: /images/animation_drivers_drivers-panel_distance.png

          Distance.

Name
   Name to use in scripted expressions.
   The name must start with a letter and no spaces or dots are allowed.

Variable Type
   The type of variable to use.

   Single Property
      Retrieves the value of a RNA property, specified by a data-block reference and a path string.

      In case of transform properties, this will return the exact value of the UI property,
      while Transform Channel will take parenting and/or constraints into account as needed.

      See also :ref:`files-data_blocks-custom-properties`.

      ID Type
         The ID-block type. For example: Key, Image, Object, Material.
      ID
         The ID of the ID-block type. For example: "Material.001".
      RNA Path
         The RNA name of the property, based on a subset of Python attribute access syntax.
         For example: ``location.x`` or ``location[0]`` for the raw X location value.

         The most convenient way to set the path is to paste the result of *Copy Data Path*
         from the context menu of the desired property.

   Transform Channel
      Retrieves the value of a Transform channel from an object or bone.

      ID
         ID of the object. For example: Cube, Armature, Camera.
      Bone
         ID of the Armature bone. For example: "Bone", "Bone.002", "Arm.r".
         This option is for armatures.
      Type
         For example, X Location, X Rotation, X Scale.

         The *Average Scale* option retrieves the combined scale value,
         computed as the cubic root of the total change in volume.
         Unlike *X/Y/Z Scale*, this value can be negative if the object is flipped by negative scaling.
      Space
         World Space, Transform Space, Local Space.

   Rotational Difference
      Provides the value of the rotational difference between two objects or bones, in radians.
   Distance
      Provides the value of the distance between two objects or bones.

Value
   Shows the value of the variable.


Expressions
===========

Expression
   A text field where to type *Driver Variables* by their name, real numbers, math operators, math functions,
   Python properties and driver functions.

   For a full list of available expressions and how to add custom functions to the set, see
   :ref:`the driver namespace example<driver-namespace>`.

   For performance optimization it is best to use the `Simple Expressions`_ subset as much as possible.
Use Self
   If this option is enabled, the variable ``self`` can be used for drivers to reference their own data.
   Useful for objects and bones to avoid having creating a *Driver Variable* pointing to itself.

   Example: ``self.location.x`` applied to the Y rotation property of the same object
   will make the object tumble when moving.


.. _drivers-simple-expressions:

Simple Expressions
------------------

Blender can evaluate a useful subset of Python driver expressions directly,
which significantly improves performance, especially on multi-core systems.
To take advantage of this, the driver expression must only use the following features:

Variable Names
   Use only ASCII characters.
Literals
   Floating point and decimal integer.
Globals
   ``frame``
Constants
   ``pi``, ``True``, ``False``
Operators
   ``+``, ``-``, ``*``, ``/``,
   ``==``, ``!=``, ``<``, ``<=``, ``>``, ``>=``,
   ``and``, ``or``, ``not``, conditional operator/ ternary if
Functions
   ``min``, ``max``, ``radians``, ``degrees``,
   ``abs``, ``fabs``, ``floor``, ``ceil``, ``trunc``, ``int``,
   ``sin``, ``cos``, ``tan``, ``asin``, ``acos``, ``atan``, ``atan2``,
   ``exp``, ``log``, ``sqrt``, ``pow``, ``fmod``

Simple expressions are evaluated even when Python script execution is disabled.

When an expression outside of this subset is used, Blender displays a "Slow Python expression" warning.

.. seealso::

   - :ref:`Extending Blender with Python <scripting-index>`.

   - `Python <https://www.python.org>`__ and its `documentation <https://docs.python.org/>`__.
   - `functions.wolfram.com <http://functions.wolfram.com/>`__.
