
.. _meta-ball-editing:

*******
Editing
*******

Active Element
==============

.. admonition:: Reference
   :class: refbox

   :Mode:      Object or Edit Modes
   :Panel:     :menuselection:`Properties editor --> Active Element`

.. figure:: /images/modeling_metas_properties_active-element-panel.png
   :align: right

   Active Element panel.

When in *Edit* mode, the *Active Element* panel appears.
These settings apply only to the selected meta element.

.. note::

   In addition to having several meta objects in a same family,
   you can also have several meta primitives in a single object (just add some more while in *Edit* mode).
   Each will be an element, with its own shape, editing rings (in the viewport), and settings...


Type
----

The *Type* menu lets you change the shape of the meta object.
See :doc:`Structure</modeling/metas/structure>` for more details.


Stiffness
---------

Together with *Threshold*, *Stiffness* controls the influencing range.
While the threshold is common to all metas in the same :ref:`family<meta-ball-object-families>`,
the stiffness is specific to each meta.

Scaling the inner green circle also changes the *Stiffness* value.

Stiffness defines how much the meta object is filled.
This essentially defines how sensitive a meta is to being affected by other metas.
With a low stiffness, the meta will begin to deform from further away.
A higher value means the meta needs to be close to another one to begin merging.

When a *Meta* object comes within "range" of another meta,
the two will begin to interact with each other. They do not necessarily need to intersect,
and depending on the *Threshold* and *Stiffness* settings,
they most likely will not need to. *Stiffness* is materialized by the *green ring*.

The range is from (0.0 to 10.0). But to be visible,
the *Stiffness* must be slightly larger than the *Threshold* value.
You can also visually adjust the *Stiffness* ring by selecting and :ref:`scaling<bpy.ops.transform.resize>` it.

.. _fig-meta-edit-stiffness:

.. figure:: /images/modeling_metas_editing_stiffness.png
   :width: 450px

   Stiffness.

In Fig. :ref:`fig-meta-edit-stiffness`, the left meta ball,
has a smaller *Stiffness* value than the right one.
As you can see, the radius (green ring) is different for each of them.


.. _meta-ball-editing-negative-influence:

Negative Influence
------------------

.. _fig-meta-intro-positive:

.. figure:: /images/modeling_metas_editing_family.png
   :width: 450px

   Positive influence of three meta balls.

A *positive* influence is defined as an attraction,
meaning that the meshes will stretch towards each other as the *rings of influence* intersect.
Fig. :ref:`fig-meta-intro-positive` shows three meta balls' *rings of influence*
intersecting with a *positive* influence.

.. _fig-meta-ball-negative:

.. figure:: /images/modeling_metas_editing_negative-influence.png
   :width: 450px

   Negative influence of a meta ball.

The opposite effect of a *positive* influence would be a *negative* influence:
the objects repel each other. Fig. :ref:`fig-meta-ball-negative`
shows a meta ball and a meta plane where the first is negative and the second, positive.
Notice how the negative meta is not visible: only the surrounding circles appear.
This is how Blender indicates that the object is negative.

Moving the sphere to the plane causes the plane's mesh to "cave in" or collapse inward.
If you move the plane away from the sphere, the plane's mesh will restore itself.


Hiding Elements
---------------

As in :ref:`object-show-hide` in *Object* mode, you can hide the selected meta(s),
and then reveal what was hidden. This is very handy for cleaning your views up a bit...

.. note::

   Hiding a meta does not *only* hide it, it also disables it from the meta computation,
   which will affect the final geometry...

.. note::

   The two red and green rings always remain visible in *Edit* mode,
   as well as the select circle in *Object* Mode.


Deleting Elements
=================

.. admonition:: Reference
   :class: refbox

   :Hotkey:    :kbd:`X`, :kbd:`Delete`

You can only delete the active element, no fancy options here.


Conversion
==========

To convert the meta to a real mesh, use :ref:`object-convert-to` in *Object* mode.


.. _meta-ball-object-families:

Object Families
===============

A "family" is a way to regroup several meta objects,
producing something very similar to having several metas inside the same object.

It is defined by the left part of an object's name (the one before the first dot). Remember,
an object's name is the one in the *Object Name* field, in most panels,
**not** the *Metaball Name* field, which is the meta data-block's name... For example,
the *family* part of "MetaPlane.001" is ``MetaPlane``.
Each meta object in the same "family" is associated with one another as discussed below.

.. figure:: /images/modeling_metas_editing_family.png
   :width: 450px

   Meta ball family.

Families of metas are controlled by a *base* meta object which is identified by
an object name **without** a dot in it. For example,
if we have three metas called ``MetaThing``, ``MetaThing.001``,
``MetaThing.round``,
the *base* meta object would be ``MetaThing``.

The *base* meta object determines the basis, the resolution, the threshold,
*and* the transformations. It also has the material and texture area.
In a way, the *base* meta is the "owner" of the other metas in the family
(i.e. it is as if the other metas were "included" or joined into the base one).

.. hint::

   When working with multiple scenes,
   take care naming your meta objects so the *base* is always in the same scene as other metas.

   Failing to do so will give confusing behaviors (like invisible meta objects).


Examples
========

.. _fig-meta-ball-base:

.. figure:: /images/modeling_metas_editing_base-example.png
   :width: 450px

   Meta ball base.

Fig. :ref:`fig-meta-ball-base` shows the *base* meta labeled "B".
The other two *Meta* objects are *children*. Children's selection rings are always black,
while the group's mesh is orange. Because the metas are grouped,
they form a unified mesh which can always be selected by selecting the mesh of any meta in the group.

For example, in Fig. :ref:`fig-meta-ball-base`, only the lower sphere (the parent) has been selected,
and you see that both the parent's mesh *and* all of the children's meshes are now highlighted.

.. _fig-meta-ball-scale:

.. figure:: /images/modeling_metas_editing_base-example-scale.png
   :width: 450px

   Scaling the "base".

The *base* meta object controls the *polygonalization* (mesh structure) for the group, and
as such, also controls the polygonalization for the children (non-base) metas.
If we transform the *base* meta, the children's polygonalization changes.
However, if we transform the children, the polygonalization remains unchanged.

.. hint::

   This discussion of "polygonization" does *not* mean that the various meshes do not deform
   towards or away from each other (meta objects always influence one another in the usual way,
   within a same family).
   
   Rather, it means that the underlying mesh structure changes only when the *base* object transforms.
   For example, if you scale the *base*, the children's mesh structure changes.
   
   In Fig. :ref:`fig-meta-ball-scale`, the *base* has been scaled down,
   which has the effect of scaling the mesh structure of each of the children. As you can see,
   the children's mesh resolution has increased, while the *base* decreased.
   The children did *not* change size!
