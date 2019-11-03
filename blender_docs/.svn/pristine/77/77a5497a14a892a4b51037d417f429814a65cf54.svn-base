
************
Mesh Options
************

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Panel:     :menuselection:`Sidebar --> Tool tab --> Options panel`


.. _bpy.types.Mesh.use_mirror_x:

X Mirror
========

The *X Mirror* option of the *Mesh Options* panel allows you to edit symmetrical vertices on the other side
of the mesh in a single action. When you transform an element (vertex, edge or face),
if there is its exact X-mirrored counterpart (in local space),
it will be transformed accordingly, through a symmetry along the local X axis.

.. note::

   The conditions for *X Mirror* to work are quite strict, which can make it difficult to use.
   To have an exact mirrored version of a (half) mesh,
   it's easier and simpler to use the :doc:`Mirror Modifier </modeling/modifiers/generate/mirror>`.


.. _modeling_meshes_editing_topology-mirror:
.. _bpy.types.Mesh.use_mirror_topology:

Topology Mirror
===============

.. note::

   For *Topology Mirror* to work the *X Mirror* option must be enabled.

When using the *X Mirror* option to work on mirrored Mesh Geometry, the vertices that
are mirrored must be perfectly placed. If they are not exactly positioned in their mirror
locations then *X Mirror* will not treat those vertices as mirrored.

*Topology Mirror* tries to address this problem by determining which vertices are mirrored vertices not only by
using their positions but also by looking at how those vertices are related to others in the Mesh Geometry.
It looks at the overall topology to determine if particular vertices will be treated as mirrored.
The effect of this is that mirrored vertices can be non-symmetrical and yet still be treated as mirrored when
*X Mirror* and *Topology Mirror* are both active.

.. note::

   The *Topology Mirror* functionality will work more reliably on mesh geometry
   which is more detailed. If you use very simple geometry, for example
   a *Cube* or *UV Sphere*, the *Topology Mirror* option will often not work.


Example
-------

For an example of how to use *Topology Mirror* open up a new Blender scene,
then delete the default cube and add a Monkey object to the 3D View.

#. Press :kbd:`Tab` to put the Monkey object into *Edit Mode*.
#. With the *X Mirror* option disabled move one of the Monkey object's vertices slightly.
#. Then Turn *X Mirror* option on again but leave *Topology Mirror* disabled.
#. If you now move that vertex again *X Mirror* will not work and the mirrored
   vertices will not be altered.
#. If you then enable *Topology Mirror* and move the same vertices again,
   then *X Mirror* should still mirror the other vertex,
   even though they are not perfectly positioned.


Auto Merge
==========

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Sidebar --> Tool --> Options --> Auto Merge`

When the *Auto Merge* option is enabled, as soon as a vertex moves closer to another one
than the *Threshold* setting, they are automatically merged.
This option affects interactive operations only
(tweaks made in the :ref:`ui-undo-redo-adjust-last-operation` panel are considered interactive too).
If the exact spot where a vertex is moved contains more than one vertex,
then the merge will be performed between the moved vertex and one of those.

Auto Merge
   Enables the Auto Merge feature.

   Double Threshold
      Defines the maximum distance between vertices that are merged by the *Auto Merge*.
