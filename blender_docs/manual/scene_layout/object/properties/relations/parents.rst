.. _bpy.types.Object.parent:

*****************
Parenting Objects
*****************

.. _bpy.ops.object.parent_set:

Make Parent
===========

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Object --> Parent`
   :Hotkey:    :kbd:`Ctrl-P`

When modeling a complex object, such as a watch,
you may choose to model the different parts as separate objects. However,
all of the parts may be attached to each other. In these cases,
you want to designate one object as the parent of all the children. Movement,
rotation or scaling of the parent also affects the children.

To parent objects, select at least two objects (select the *Child Objects* first,
and select the *Parent Object* last), and press :kbd:`Ctrl-P`.
The *Set Parent To* menu will pop up allowing you to select from one of several
possible different parenting types.
Selecting one of the entries in *Set Parent To* confirms,
and the child/children to parent relationship is created.

The last object selected will be the *Active Object* (outlined in light orange),
and will also be the *Parent Object*.
If you selected multiple objects before selecting the parent,
they will all be children of the parent and will be at the same level of the hierarchy
(they are "siblings").

The *Set Parent To* pop-up menu is context-sensitive, which means
the number of entries it displays can change depending on what objects are selected
when the :kbd:`Ctrl-P` shortcut is used.

For parenting without `Parent Inverse`_, use the :kbd:`Shift-Ctrl-P` shortcut instead.

Moving, rotating or scaling the parent will also usually move/rotate/scale the child/children.
However, moving/rotating/scaling the child/children of the parent will not result in the parent
moving/rotating/scaling. In other words,
the direction of influence is from parent to child and not child to parent.

In general when using :kbd:`Ctrl-P` or :menuselection:`3D View Header --> Object --> Parent`
to parent objects, the *Child Objects* can only have one *Parent Object*.
If a *Child Object* already has a *Parent Object* and you give it another parent then
Blender will remove the previous parent relationship.


Parent Inverse
--------------

When objects are parented with :kbd:`Ctrl-P`, the current transformation of the parent
is stored in a hidden *Parent Inverse* matrix. By using that, the location, rotation and
scale properties of the child can continue to be effectively interpreted in world space,
as long as the parent doesn't move.

For parenting without assigning the matrix, use the :kbd:`Shift-Ctrl-P` shortcut instead.
This creates an alternative parent-child-relationship where child object's properties are
evaluated in the parent's coordinate system. This is the better choice for CAD purposes,
for example.

The matrix can also be cleared after parenting by using :ref:`Clear Parent Inverse <bpy.ops.object.parent_clear>`.


Parent Types
------------

Blender supports many different types of parenting, listed below:

- Object
- Bone
- Vertex
- Vertex (Triangle)


.. rubric:: Setups

Besides parenting the selected objects,
it adds a Modifier or Constraint to the child objects, with the parent as target object
or activates a parent property i.e. *Follow Path*.

- :doc:`Armature Deform </animation/armatures/skinning/parenting>`
- :doc:`Curve Deform </modeling/modifiers/deform/curve>`
- :ref:`Follow Path <curve-path-animation>`
- :doc:`Path Constraint </animation/constraints/relationship/follow_path>`
- :doc:`Lattice Deform </modeling/modifiers/deform/lattice>`


.. _object-parenting:

Object Parent
=============

*Object Parent* is the most general form of parenting that Blender supports.
If will take selected objects and make the last selected object the *Parent Object*,
while all other selected objects will be *Child Objects*.
The child objects will inherit the transformations of the parent. The parent object can be of any type.


Object (Keep Transform) Parent
------------------------------

*Object (Keep Transform) Parent* works in a very similar way to *Object Parent*. The major difference is in whether
the *Child Objects* will remember any previous transformations applied to them from the previous *Parent Object*.

Since explaining this in an easy to understand technical way is hard,
let's instead use an example to demonstrate.

Assume that we have a scene consisting of three objects,
those being two Empty Objects named "EmptyA" and "EmptyB", and a Monkey object.
Fig. :ref:`fig-view3d-parent-scene-no` shows the three objects with no parenting relationships active on them.

.. _fig-view3d-parent-scene-no:

.. figure:: /images/scene-layout_object_properties_relations_parents_keep-transform-a.png

   Scene with no parenting.

If you select the Monkey object by :kbd:`RMB` click and then :kbd:`Shift-RMB`
click "EmptyA" object and press :kbd:`Ctrl-P` and finally select *Object*
from the *Set Parent To* pop-up menu.
This will result in "EmptyA" object being the *Parent Object* of the Monkey object.
With only "EmptyA" selected rotating/scaling/moving it will result in
the Monkey object being altered respectively.

Scale the "EmptyA" object, so that the Monkey becomes smaller and moves to the left a little.

.. figure:: /images/scene-layout_object_properties_relations_parents_keep-transform-b.png

   The monkey is the child object of "EmptyA".

If you select only the Monkey object by :kbd:`RMB` click and then :kbd:`Shift-RMB`
click "EmptyB" object and press :kbd:`Ctrl-P` and select *Object* from
the *Set Parent To* pop-up menu.
This will result in "EmptyB" object being the *Parent Object* of the Monkey object.
Notice that when you change the parent of the Monkey the scale of the Monkey changed.

.. figure:: /images/scene-layout_object_properties_relations_parents_keep-transform-c.png

   The monkey is the child object of "EmptyB".

This happens because the Monkey object never had its scale altered directly,
the change came about because it was the child of "EmptyA" which had its scale altered.
Changing the Monkey's parent to "EmptyB" resulted in those indirect changes in scale being
removed, because "EmptyB" has not had its scale altered.

This is often the required behavior, but it is also sometimes useful that if you change your
*Parent Object* that the *Child Object* keep any previous transformations
it got from the old *Parent Object*; If instead when changing the *Parent Object* of the Monkey
from "EmptyA" to "EmptyB" we had chosen parenting type *Object (Keep Transform)*,
the Monkey would keep its scale information it obtained from the old parent "EmptyA"
when it is assigned to the new parent "EmptyB";

.. figure:: /images/scene-layout_object_properties_relations_parents_keep-transform-d.png

   The Object (Keep Transform) parent method.


If you want to follow along with the above description here is the blend-file used to describe
*Object (Keep Transform)* parenting method:

`File:Parent_-_Object_(Keep_Transform)_(Demo_File).blend
<https://wiki.blender.org/wiki/File:Parent_-_Object_(Keep_Transform)_(Demo_File).blend>`__.


Bone Parent
===========

Bone parenting allows you to make a certain bone in an armature the Parent Object of another object.
This means that when transforming an armature the Child Object will only move
if the specific bone is the Child Object of moves.

.. _fig-view3d-parent-bone-parent:

.. figure:: /images/scene-layout_object_properties_relations_parents_bone1.png

   Three pictures of armatures with four bones.

In Fig. :ref:`fig-view3d-parent-bone-parent` with the 2nd bone being the Bone Parent of the Child Object Cube.
The Cube is only transformed if the 1st or 2nd bones are.
Notice altering the 3rd and 4th bones has no effect on the Cone.

To use Bone Parenting, you must first select all the Child Objects you wish to parent to a specific Armature Bone,
then :kbd:`Shift-RMB` select the Armature Object and switch it into Pose Mode and
then select the specific bone you wish to be the Parent Bone by :kbd:`RMB` selecting it.
Once done press :kbd:`Ctrl-P` and select Bone from the Set Parent To pop-up menu.

Now transforming that bone in Pose Mode will result in the Child Objects also transforming.


Relative Parenting
------------------

Bone Relative parenting is an option you can toggle for each bone.
This works in the same way as Bone parenting with one difference.

With Bone parenting if you have parented a bone to some Child Objects and
you select that bone and switch it into Edit Mode and then move that bone;
When you switch back into Pose Mode on that bone,
the Child Object which is parented to that bone will snap back to the location of the bone in Pose Mode.

.. _fig-view3d-parent-bone-parent-child:

.. figure:: /images/scene-layout_object_properties_relations_parents_bone2.png

   Single armature bone which has a child object cube parented to it using bone parenting.

In Fig. :ref:`fig-view3d-parent-bone-parent-child` the 1st picture shows the position of the cube and
armature before the bone is moved in Edit Mode.
2nd picture shows the position of the cube and armature after the bone was selected in Edit Mode,
moved and switched back into Pose Mode. Notice that the Child Object moves to the new location of the Pose Bone.

Bone Relative parenting works differently;
If you move a Parent Bone in Edit Mode, when you switch back to Pose Mode,
the Child Objects will not move to the new location of the Pose Bone.

.. _fig-view3d-parent-bone-parent-relative:

.. figure:: /images/scene-layout_object_properties_relations_parents_bone3.png

   Single bone with bone relative parent to a cube.

In Fig. :ref:`fig-view3d-parent-bone-parent-relative` the 1st picture
shows the position of the cube and armature before the bone is moved in Edit Mode.
2nd picture shows the position of the cube and armature after the bone was selected in Edit Mode,
moved and switched back into Pose Mode.
Notice that the Child Object does not move to the new location of the Pose Bone.


Vertex Parent
=============

For objects of type curve, surface, mesh and lattice,
there is the possibility to use one of its vertices or points as the parent of other objects.
You can parent an object to a single vertex or a group of three vertices as well;
that way the child/children will move when the parent mesh is deformed.


Vertex Parent from Edit Mode
----------------------------

In *Object Mode*, select the child/children and then the parent object.
:kbd:`Tab` into *Edit Mode* and on the parent object select either one vertex
that defines a single point, or select three vertices that define an area
(the three vertices do not have to form a complete face;
they can be any three vertices of the parent object),
and then press :kbd:`Ctrl-P` and confirm.

At this point, if a single vertex was selected,
a relationship/parenting line will be drawn from the vertex to the child/children. If three
vertices were selected then a relationship/parenting line is drawn from the averaged center of
the three points (of the parent object) to the child/children. Now,
as the parent mesh deforms and the chosen parent vertex/vertices move,
the child/children will move as well.


Vertex Parent from Object Mode
------------------------------

Vertex parenting can be performed from object mode,
this is done like regular object parenting,
press :kbd:`Ctrl-P` in object mode and select *Vertex* or *Vertex (Triangle)*.

The nearest vertices will be used from each object which is typically what you would want.

.. list-table:: Vertex Parent example.

   * - .. figure:: /images/scene-layout_object_properties_relations_parents_object-mode-example-1.png
          :width: 320px

          The small cubes can each be automatically parented to a triad of nearby vertices on the icosphere using
          the "Vertex (Triangle)" in the set parent context menu.

     - .. figure:: /images/scene-layout_object_properties_relations_parents_object-mode-example-2.png
          :width: 320px

          Reshaping the object in edit mode then means each of the cubes follows their vertex parent separately.

     - .. figure:: /images/scene-layout_object_properties_relations_parents_object-mode-example-3.png
          :width: 320px

          Re-scaling the parent icosphere in object mode means the child cubes are also rescaled as expected.

The parent context menu item means users can rapidly set up a large number of vertex parent
relationships,
and avoid the tedious effort of establishing each parent-child vertex relationship separately.

.. note::

   It is in fact a sort of "reversed" :doc:`hook </modeling/modifiers/deform/hooks>`.


Options
=======

Move Child
----------

You can *move* a child object to its parent by clearing its origin.
The relationship between the parent and child is not affected.
Select the child object and press :kbd:`Alt-O`.
By confirming the child object will snap to the parent's location.
Use the *Outliner* view to verify that the child object is still parented.


.. _bpy.ops.object.parent_clear:

Clear Parent
------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Object --> Parent`
   :Hotkey:    :kbd:`Alt-P`

You can *remove* a parent-child relationship via :kbd:`Alt-P`.

Clear Parent
   If the parent in the group is selected, nothing is done.
   If a child or children are selected, they are disassociated from the parent,
   or freed, and they return to their *original* location, rotation, and size.
Clear and Keep Transformation
   Frees the children from the parent, and *keeps* the location, rotation, and size given to them by the parent.

   See `Non-Uniform Scale`_ which may apply here.
Clear Parent Inverse
   Instead of removing the hierarchical parent-child relationship, this clears
   the `Parent Inverse`_ matrix from the selected objects. With an empty matrix,
   the location, rotation and scale properties of the children are interpreted
   in the coordinate space of the parent.


.. hint:: **Use the Outliner**

   There is another way to see the parent-child relationship in groups and that is to use the *Outliner* view
   of the :doc:`Outliner editor </editors/outliner>`.


Known Limitations
=================

Non-Uniform Scale
-----------------

A parent with non-uniform scale and rotation in relation to its child may cause a *shear* effect.

While this is supported by parenting, the shear will be lost when the parent is cleared since it
can't be represented by location, scale and rotation.

If *Clear and Keep Transformation* moves the object, non-uniform scale is the most likely cause.
