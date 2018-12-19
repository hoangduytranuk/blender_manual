.. _bpy.types.Object.dupli_frames:

***********
DupliFrames
***********

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Panel:     :menuselection:`Object --> Duplication`

.. figure:: /images/editors_3dview_object_properties_duplication_dupliframes_panel.png
   :align: right

   Object Duplication panel.

*Duplication at Frames* or *DupliFrames* creates instances of an animated object
that correspond to the state of this object (including *Location*, *Rotation* and *Scaling*)
in each frame of the animation.

Start, End
   Specify the start and end frames of the animation for which the instances will be created.
On, Off
   Creates an alternating pattern,
   *"On"* number of frames will be shown, next *"Off"* frames will be skipped and so on.
Speed
   When the object is animated using :ref:`Follow Path <curve-path-animation>` animation,
   this option causes to ignore this path animation, and use only the animation of the object itself.


Examples
========

In Fig. :ref:`fig-object-duplication-dupliframes-driver`
*DupliFrames* is applied to the object that is animated
using the :doc:`Drivers </animation/drivers/index>` with a scripted expression
and moves along the sine wave.

.. _fig-object-duplication-dupliframes-driver:

.. figure:: /images/editors_3dview_object_properties_duplication_dupliframes_example.png
   :width: 480px

   The sphere is animated using the Drivers.

In Fig. :ref:`fig-object-duplication-dupliframes-path` *DupliFrames* is applied to the *Monkey* object
that travel along the Bézier circle during 16 frames,
(see :ref:`Path Animation <curve-path-animation>` example).
Option *Speed* in the *Duplication panel* is disabled.

.. _fig-object-duplication-dupliframes-path:

.. figure:: /images/modeling_curves_properties_data_path-animation-example-2.png
   :width: 480px

   The monkey is animated using the Follow Path animation.

.. tip::

   To transform all monkeys into real objects, first :kbd:`Shift-Ctrl-A`
   to *Make Duplicates Real*. All monkeys are now real objects, but still linked copies.
   To change this, use :kbd:`U` shortcut or :menuselection:`Object --> Make Single User --> Object & Data --> All`.

.. note::

   There are many alternatives to DupliFrames.

   - To arrange objects along a curve, combining an *Array Modifier* and a *Curve Modifier* is often useful.
   - DupliVerts can be used to arrange objects, for example, along a circle or across a subdivided plane.
