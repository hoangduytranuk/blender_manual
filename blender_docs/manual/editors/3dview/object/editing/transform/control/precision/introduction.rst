
************
Introduction
************

.. admonition:: Reference
   :class: refbox

   :Mode:      Object and Edit Modes
   :Hotkey:    :kbd:`Ctrl` and/or :kbd:`Shift`

Holding :kbd:`Ctrl` during a transform operation (such as grab, rotate or scale)
will toggle :ref:`Transform Snapping <transform-snap>`.
When the :ref:`Snap Element <transform-snap-element>` is set to *Increment*,
this allows the transformation to be performed in discrete amounts.

Holding :kbd:`Shift` during a transform operation will transform the object at 1/10th the speed,
allowing much finer control.

The magnitude of the transformation can be viewed in the 3D View footer.
Releasing :kbd:`Ctrl` or :kbd:`Shift` during the transformation will cause the movement
to revert back to its normal mode of operation.

Holding both :kbd:`Shift-Ctrl` enables precise snap.
This option will move the object with high precision along with the snapping constraint.

.. note::

   The snapping behaviors described on this page **only** apply when :ref:`Increment Snap <transform-snap-element>`
   is selected.


Usage
=====

With Hotkeys
------------

Press :kbd:`G`, :kbd:`R` or :kbd:`S` and then hold either :kbd:`Ctrl`,
:kbd:`Shift` or :kbd:`Shift-Ctrl`.


With the Transform Manipulator
------------------------------

Hold :kbd:`Ctrl`, :kbd:`Shift` or :kbd:`Shift-Ctrl` and click on the appropriate manipulator handle.
Then move the mouse in the desired direction. The reverse action will also work i.e.
clicking the manipulator handle and then holding the shortcut key for precision control.

.. seealso::

   :doc:`Read more about the Transform Manipulator </editors/3dview/object/editing/transform/control/manipulators>`.

.. tip:: Combining with Other Controls

   All of the precision controls detailed on the page can be combined with
   the :doc:`Axis Locking </editors/3dview/object/editing/transform/control/precision/axis_locking>`
   controls and used with the different
   :doc:`Pivot Points </editors/3dview/object/editing/transform/control/pivot_point/index>`.


Snapping
========

Grab/move
---------

.. figure:: /images/editors_3dview_object_editing_transform_control_precision_introduction_blender-units.png
   :align: right

   One Blender Unit (default zoom level).

For grab/move operations at the default zoom level,
holding :kbd:`Ctrl` will cause your selection to move by increments of 1 Blender Unit (1 BU)
(i.e. between the two light gray lines). Zooming in enough to see the next set of gray
lines will now cause :kbd:`Ctrl` movements to occur by 1/10 of a BU.
Zooming in further until the next set of gray lines becomes visible
will cause movement to happen by 1/100 of a BU and so on until the zoom limit is reached.
Zooming out will have the opposite effect and
cause movement to happen by increments of 10 BU, 100 BU, etc.

.. container:: lead

   .. clear

.. seealso::

   Read more about :doc:`zooming </editors/3dview/navigate/introduction>`.


Rotation
--------

Holding :kbd:`Ctrl` will cause rotations of 5 degrees.


Scale
-----

Holding :kbd:`Ctrl` will cause size changes in increments of 0.1 BU.

.. note:: Snapping modes

   Note that if you have a :ref:`Snap Element <transform-snap-element>` option enabled,
   holding :kbd:`Ctrl` will cause the selection to snap to the nearest element.

   Read more about :doc:`snapping </editors/3dview/object/editing/transform/control/snap>`.


Precision
=========

Holding :kbd:`Shift` during transformations allows for very fine control that does not
rely on fixed increments. Rather, large movements of the mouse across the screen only result
in small transformations of the selection.

In rotation mode the selected element will be rotate in 0.01 degree increments.


Precision Snapping
==================

Grab/move
---------

For grab/move operations at the default zoom level, holding :kbd:`Shift-Ctrl` will cause
your selection to move by increments of 1/10 Blender Units. Holding :kbd:`Shift-Ctrl` at
any zoom level will cause the transformation increments to always be 1/10 of the increment if
you were only holding :kbd:`Ctrl`.


Rotation
--------

Holding :kbd:`Shift-Ctrl` will cause rotations of 1 degree.


Scale Transformations
---------------------

Holding :kbd:`Shift-Ctrl` will cause size changes in 0.01 BU increments.
