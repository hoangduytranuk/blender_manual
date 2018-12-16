
****************
Hiding & Masking
****************

Selection Masking
=================

If you have a complex mesh,
it is sometimes not easy to paint on all vertices in Weight Paint Mode.
Suppose you only want to paint on a small area of the Mesh and keep the rest untouched.
This is where *selection masking* comes into play. When this mode is enabled,
a brush will only paint on the selected vertices or faces.
The option is available from the header of the 3D View
(see icons surrounded by the yellow frame):

.. figure:: /images/sculpt-paint_painting_weight-paint_hide-mask_select.png

   You can choose between *Face Selection masking* (left button)
   and *Vertex selection masking* (right button).

*Select* mode has some advantages over the default *Weight Paint Mode*:

- The original mesh edges are drawn, even when modifiers are active.
- You can select faces to restrict painting to the vertices of the selected faces.
- Selecting tools include:


Details About Selecting
-----------------------

The following standard selection operations are supported:

- :kbd:`RMB` -- Single faces. Use :kbd:`Shift-RMB` to select multiple.
- :kbd:`A` -- All faces, also to de-select.
- :kbd:`B` -- Border selection.
- :kbd:`C` -- Circle select with brush.
- :kbd:`L` -- Pick linked (under the mouse cursor).
- :kbd:`Ctrl-L` -- Select linked.
- :kbd:`Ctrl-I` -- Invert selection *Inverse*.

.. tip:: Selecting Deform Groups

   When you are doing weight painting for deform bones (with an Armature),
   you can select a deform group by selecting the corresponding bone.
   However, this Vertex Group selection mode is disabled when Selection Masking is active!


Vertex Selection Masking
------------------------

.. figure:: /images/sculpt-paint_painting_weight-paint_hide-mask_vertex-select.png

   Vertex Selection masking.

In this mode you can select one or more vertices and then paint only on the selection.
All unselected vertices are protected from unintentional changes.

.. note::

   This option can also be toggled with :kbd:`V`.


Face Selection Masking
----------------------

.. figure:: /images/sculpt-paint_painting_weight-paint_hide-mask_face-select.png

   Face Selection masking.

The *Face Selection masking* allows you to select faces and limit the weight paint
tool to those faces, very similar to Vertex selection masking.


Hide/Unhide Faces
-----------------

.. figure:: /images/sculpt-paint_painting_weight-paint_hide-mask_face-select-hidden.png

   Hidden faces.

You also can hide selected faces as in Edit Mode with the keyboard Shortcut :kbd:`H`,
then paint on the remaining visible faces and finally unhide the hidden faces again by using
:kbd:`Alt-H`.


Hide/Unhide Vertices
--------------------

You cannot directly hide selected faces in vertex mask selection mode.
However, you can use a trick:

#. First go to Face selection mask mode.
#. Select the areas you want to hide and then hide the faces (as explained above).
#. Switch back to Vertex Selection mask mode.

Now the vertices belonging to the hidden Faces will remain hidden.


The Clipping Border
-------------------

To constrain the paint area further you can use the *Clipping Border*.
Press :kbd:`Alt-B` and :kbd:`LMB`\ -drag a rectangular area.
The selected area will be "cut out" as the area of interest.
The rest of the 3D View gets hidden.

.. figure:: /images/sculpt-paint_painting_weight-paint_hide-mask_border-select.png

   The Clipping Border is used to select interesting parts for local painting.

You make the entire mesh visible again by pressing :kbd:`Alt-B` a second time.

All weight paint tools that use the view respect this clipping, including border select,
weight gradient and of course brush strokes.
