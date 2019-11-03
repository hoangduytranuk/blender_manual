
**************
Vertex Weights
**************

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit and Weight Paint Modes
   :Panel:     :menuselection:`Sidebar region --> Vertex Weights`

.. figure:: /images/modeling_meshes_properties_vertex-groups_vertex-weights_panel-overview.png
   :width: 260px

   Vertex Weights panel.

   \(1) Vertex Group Categories, (2) Weight Table, (3) Tools.

As mentioned before in :doc:`Vertex Groups </modeling/meshes/properties/vertex_groups/index>`
each entry in a Vertex Group also contains a weight value in the range of (0.0 to 1.0).
Blender provides a *Vertex Weights* panel from where you can get (and edit)
information about the weight values of each Vertex of a mesh.
That is: to which Vertex Groups the vertex is assigned with which weight value.

The Vertex Weights panel can be found in the right Sidebar region of the 3D View.
It is available in Edit Mode and in Weight Paint Mode
(when Vertex Selection masking is enabled as well).


Vertex Group Categories
=======================

Actually we do not have any strict categories of Vertex Groups in Blender.
Technically they all behave the same way.
However, we can identify two implicit categories of Vertex Groups:


Deform Groups
-------------

These Vertex Groups are sometimes also named *Weight Groups* or *Weight Maps*.
They are used for defining the weight tables of Armature bones.
All Deform Groups of an Object are strictly related to each other via their weight values.

Strictly speaking, the sum of all deform weights for any vertex of a mesh should be exactly 1.0.
In Blender this constraint is a bit relaxed (see below).
Nevertheless, Deform Groups should always be seen as related to each other.
Hence, we have provided a filter that allows restricting the Vertex Weight panel to
display only the Deform bones of an Object.


Other Groups
------------

All other usages of Vertex Groups are summarized into the *Other* category.
These vertex groups can be found within Shape keys, Modifiers, etc.
There is really no good name for this category,
so we kept it simple and named it *Other*.


Weight Table
============

The Weight Table shows all weights associated to the *active vertex*.
Note that a vertex does not necessarily have to be associated to any vertex groups.
In that case the Vertex Weights Panel is not displayed.

.. tip:: The active Vertex

   That is the most recently selected vertex.
   This vertex is always highlighted so that you can see it easily in the mesh.
   If the active Vertex does not have weights, or there is no active vertex selected at the moment,
   then the Vertex Weights Panel disappears.

Each row in the Weight table contains four active elements:

.. figure:: /images/modeling_meshes_properties_vertex-groups_vertex-weights_editor-name.png
   :width: 260px

   Change Active Group.


Set the Active Group
--------------------

As soon as you select any of the Vertex Group Names in the Weight table,
the referenced Vertex Group becomes the new Active group.

.. figure:: /images/modeling_meshes_properties_vertex-groups_vertex-weights_show.png
   :width: 260px

   Enable display of Weights in Edit Mode.


Display Weights in Edit Mode
----------------------------

When you are in edit mode, you can make the Weights of the active Group visible on the mesh:

Search the *Mesh Display* panel in the Sidebar region.
And there enable the *Show Weights* option.
Now you can see the weights of the active Vertex Group displayed on the mesh surface.

.. figure:: /images/modeling_meshes_properties_vertex-groups_vertex-weights_edit-mode.png
   :width: 260px

   Weights in Edit Mode.


Edit Weights in Edit Mode
-------------------------

It is now very easy to work with Vertex Groups in Edit Mode.
All edit options of the mesh are available and
you have direct visual control over how your Weights change when you edit the weight values.

.. figure:: /images/modeling_meshes_properties_vertex-groups_vertex-weights_editor-weight.png
   :width: 260px

   Change Weight value.


Change a Weight
---------------

You can either enter a new weight value manually (click on the number and edit the value),
or you can change the weight by :kbd:`LMB` and while holding down the mouse button,
drag right or left to increase/decrease the weight value. You also can use the right/left
arrows displayed around the weight value to change the weight in steps.

.. figure:: /images/modeling_meshes_properties_vertex-groups_vertex-weights_editor-paste.png
   :width: 260px

   Paste weights.


Pasting
-------

:kbd:`LMB` the Paste Icon allows you to forward a single weight of the active Vertex to all selected vertices.
But note that weights are only pasted to vertices which already have a weight value in the affected Vertex Group.

.. figure:: /images/modeling_meshes_properties_vertex-groups_vertex-weights_editor-delete.png
   :width: 260px

   Delete weights.


Deleting
--------

:kbd:`LMB` the Delete Icon will instantly remove the weight from the active vertex.
Thus the entire row disappears when you click on the delete icon.


Tools
=====

.. figure:: /images/modeling_meshes_properties_vertex-groups_vertex-weights_editor-functions.png
   :width: 260px

   Vertex Weights panel.

Normalize
   Normalizes the weights of the active Vertex.
   That is all weights of the active vertex are recalculated
   such that their relative weight is maintained and the weight sum is 1.0.
Copy
   Copies all weights defined for the active Vertex to all selected vertices.
   Thus all previously defined weights are overwritten.

.. tip:: The filter setting is respected

   Note that both tools only work on the Vertex Groups currently displayed in the Weights Table.
   So if for example only the *Deform weights* are displayed,
   then Normalize and Copy only affect the Deform bones.


Locking
=======

.. figure:: /images/modeling_meshes_properties_vertex-groups_vertex-weights_editor-locked.png
   :width: 260px

   Locked Vertex Weights panel.

Whenever a Weight Group is locked, all data changing tools get disabled:

- Normalize the vertex Weights.
- Copy the Vertex weights.
- Change the Weight of the active vertices.
- Paste to selected vertices.

.. tip:: The filter setting is respected

   If you have for example all deform weight groups unlocked and all other vertex groups locked,
   then you can safely select *Deform* from the Filter row
   and use all available tools from the Weight table again.
