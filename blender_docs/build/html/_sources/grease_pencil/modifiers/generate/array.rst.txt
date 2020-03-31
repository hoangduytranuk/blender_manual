.. _bpy.types.ArrayGpencilModifier:

**************
Array Modifier
**************

The *Array* modifier creates an array of copies of the base object, with each copy being offset from
the previous one in any of a number of possible ways.

Useful for creating complex repetitive drawings.

Multiple Array modifiers may be active for an object at the same time
(e.g. to create complex three-dimensional constructs).


Options
=======

.. figure:: /images/grease-pencil_modifiers_generate_array_panel.png
   :align: right

   The Array modifier.

Count
   Total number of copies.


Offset
------

Constant Offset
   Adds a constant translation component to the duplicate object's offset.
   X, Y and Z constant components can be specified.

   X, Y, Z

Relative Offset
   Adds a translation equal to the object's bounding box size along each axis,
   multiplied by a scaling factor, to the offset. X, Y and Z scaling factors can be specified.

   X, Y, Z

Object Offset
   Adds a transformation taken from an object (relative to the current object) to the offset.
   It is good practice to use an empty object centered or near to the initial object.

Random Offset
   Add random offset values to the copies.

   X, Y, Z

Random Rotation
   Add random rotation values to the copies.

   X, Y, Z

Random Scale
   Add random scale values to the copies.

   X, Y, Z

Seed
   Seed used by the pseudo-random number generator.

Material Override
   Index of the material to use on duplicated strokes (0 use strokes original materials).

.. note::

   The *Depth Order* is used in the Grease Pencil object has an influence on
   the strokes visualization when using the Array modifier.
   See :doc:`Depth Order </grease_pencil/properties/strokes>` for more information.


Influence Filters
-----------------

See :ref:`grease-pencil-modifier-influence-filters`.
