
***********
Duplication
***********

There are two types of object duplication,
being `Duplicate`_ and `Linked Duplicates`_ which instance their Object Data.


.. _bpy.ops.object.duplicate_move:

Duplicate
=========

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit and Object Modes
   :Panel:     :menuselection:`Tool Shelf --> Tools --> Edit --> Duplicate`
   :Menu:      :menuselection:`Object --> Duplicate Objects`
   :Hotkey:    :kbd:`Shift-D`

This will create a visually-identical copy of the selected object(s).
The copy is created at the same position as the original object and
you are automatically placed in *Grab* mode. See the examples below.

This copy is a new object, which shares some data-blocks with the original object
(by default, all the Materials, Textures, and F-Curves), but which has copied others,
like the mesh, for example. This is why this form of duplication is sometimes called "shallow link",
because not all data-blocks are shared; some of them are "hard copied"!

.. tip::

   You can choose which types of data-block will be linked or copied when duplicating:
   in the :ref:`Preferences <prefs-editing-duplicate-data>`.


Examples
--------

.. figure:: /images/editors_3dview_object_editing_duplication_example.png

   The Cube object was duplicated.

The object ``Cube`` was duplicated, using :kbd:`Shift-D`.
Both these cubes has separate meshes with unique names: ``Cube`` and ``Cube.001``.

- The original left cube is being edited, the duplicated right cube remains unchanged.
  The mesh data has been copied, not linked.
- Likewise, if one cube is edited in Object Mode, the other cube remains unchanged.
  The new object's transform properties or data-block is a copy, not linked.
- When the cube was duplicated, it inherited the material of the original cube.
  The material properties were linked, not copied.

See above if you want separate copies of the data-blocks normally linked.


.. _bpy.ops.object.duplicate_move_linked:

Linked Duplicates
=================

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Panel:     :menuselection:`Tool Shelf --> Tools --> Edit --> Duplicate Linked`
   :Menu:      :menuselection:`Object --> Duplicate Linked`
   :Hotkey:    :kbd:`Alt-D`

You also have the choice of creating a *Linked Duplicate* rather than a *Duplicate*;
this is called a deep link.
This will create a new object with **all** of its data linked to the original object.
If you modify one of the linked objects in *Edit Mode*,
all linked copies are modified. Transform properties (object data-blocks) still remain copies,
not links, so you still can rotate, scale, and move freely without affecting the other copies.
Reference Expl. :ref:`Duplicate Example <expl-object-link-duplicate>` for the discussions below.

Linked
   In the *Duplicate Objects* Operator panel the *Linked* checkbox is checked unlike with *Duplicate*.

.. hint::

   If you want to make changes to an object in the new linked duplicate independently of the original object,
   you will have to manually make the object a "single-user" copy by :kbd:`LMB`
   the number in the *Object Data* panel of the Properties editor. (See :ref:`ui-data-block`).

.. seealso::

   :ref:`data-system-datablock-make-single-user` for unlinking data-blocks.


.. _expl-object-link-duplicate:

Examples
--------

.. figure:: /images/editors_3dview_object_editing_duplication_linked-example.png

   The Cube object was linked duplicated.

The object ``Cube`` was linked duplicated, using :kbd:`Alt-D`.
Though both these cubes are separate objects with unique names: ``Cube`` and ``Cube.001``,
the single mesh named ``Cube``, is shared by both.

- As a mesh is edited in *Edit Mode* in one object, the same occurs in the other cube as well.
  The mesh data are links, not copies.
- In contrast, if one of these two cubes is rotated or rescaled in Object Mode, the other remains unchanged.
  The transform properties are copied, not linked.
- As in the previous example, the newly created cube has inherited the material of the original cube.
  The material properties are linked, not copied.

A common table has a top and four legs. Model one leg,
and then make linked duplicates three times for each of the remaining legs.
If you later make a change to the mesh, all the legs will still match.
Linked duplicates also apply to a set of drinking glasses,
wheels on a car... anywhere there is repetition or symmetry.

.. seealso:: Linked Library Duplication

   :doc:`Linked Libraries </files/linked_libraries>` are also a form of duplication.
   Any object or data-block in other blend-files can be reused in the current file.

.. hint::

   If you want transform properties (i.e. object data-blocks) to be "linked",
   see the page on :doc:`parenting </scene_layout/object/properties/relations/parents>`.
