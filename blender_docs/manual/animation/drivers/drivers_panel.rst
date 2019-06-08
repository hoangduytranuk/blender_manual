
*************
Drivers Panel
*************

.. admonition:: Reference
   :class: refbox

   :Editor:    Graph editor
   :Mode:      Drivers
   :Panel:     :menuselection:`Sidebar region --> Drivers --> Drivers`

.. figure:: /images/animation_drivers_drivers-panel_panel.png
   :align: right

   Drivers panel.

This panel is located in the :doc:`Graph Editor </editors/graph_editor/introduction>` with the mode set to Drivers.

The Drivers panel is for setting up *Driver Variables* or a *Scripted Expression* which
will determine the value of the *Driver Value*.


Settings
========

Update Dependencies
   This will force an update for the Driver Value dependencies.
Remove Driver
   Removes the driver from the property.

Type
   There are two categories of scripts: built-in (average, sum, minimum and maximum) and
   custom scripts (Scripted Expressions).

   Average Value
      Uses the average value of the referenced Driver Variables.
   Sum Values
      Uses the sum of the referenced Driver Variables.
   Scripted Expression
      Uses a Scripted Expression. See `Expression`_.
      You can write a Python expression which performs your own calculations on the Driver Variables.
   Minimum Value
      Uses the lowest value from the referenced Driver Variables.
   Maximum Value
      Uses the highest value from the referenced Driver Variables.

Show Debug Info
   Shows the *Driver Value*.
Driver Value
   The output value of the driver script.


Expression
----------

Expression
   Here you can add variables, real numbers, math operators, math functions, Python properties, driver functions.
   See Driver Expression below for some examples. For performance optimization it is best to use
   the `Simple Expressions`_ subset as much as possible.
Use Self
   This allows for drivers to references their own data using the variable ``self``.
   Useful for objects, bones, to avoid having to create a variable pointing to its self.


Simple Expressions
^^^^^^^^^^^^^^^^^^

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


Driver Variables
----------------

.. list-table::

   * - .. figure:: /images/animation_drivers_drivers-panel_transform-channel2.png

          Transform channel setup.

     - .. figure:: /images/animation_drivers_drivers-panel_distance.png

          Distance setup.

Variable are references to properties or delta transformations which are a reference to two properties.

Add Variable
   Adds a new Driver Variable.
Copy/Paste
   Uses the copy of the current variable stack so it can be pasted onto another object's variable stack.
Name
   Name to use for scripted expressions/functions.
   No spaces or dots are allowed and must start with a letter.

Variable Type
   The type of variable to use.

   Single Property
      Use the value from some RNA property.
      For example, the Ambient shading color from a material.
      (see Fig. :ref:`fig-setup-single-property`)
      First select the type of ID-block, then the ID of the ID-block, then copy and
      paste an RNA property :kbd:`Ctrl-V`.
      See also :doc:`/files/custom_properties`.

      ID Type
         The ID-block type. For example: Key, Image, Object, Material.
      ID
         The ID of the ID-block type. For example: "Material.001".
      RNA Path
         The RNA ID name of the property. For example: 'ambient' from material shading.

   Transform Channel
      Use one of the Transform channels from an object or bone.

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
      Use the rotational difference between two objects or bones.
   Distance
      Use the distance between two objects or bones.

Value
   Shows the value of the variable.


Example
=======

.. _fig-setup-single-property:

.. figure:: /images/animation_drivers_drivers-panel_single-property.png

   Setup of a single property.

.. seealso::

   - :ref:`Extending Blender with Python <scripting-index>`.

   - `Python <https://www.python.org>`__ and its `documentation <https://docs.python.org/>`__.
   - `functions.wolfram.com <http://functions.wolfram.com/>`__.
