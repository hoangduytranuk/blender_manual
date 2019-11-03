
******
Rename
******

.. _tools_rename-active:

Rename Active Item
==================

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Edit --> Rename Active Item`
   :Hotkey:    :kbd:`F2`

The *Rename Active Item* operator renames the active :doc:`Object </scene_layout/object/index>`
or :doc:`Node </interface/controls/nodes/index>`.
When the operator is executed, a pop-up menu appears.
The text field shows the name of the current item and can be overwritten to rename the item.
:kbd:`Return` confirms the name while :kbd:`Esc` cancels the operator.


.. _bpy.ops.wm.batch_rename:

Batch Rename
============

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Edit --> Batch Rename`
   :Hotkey:    :kbd:`Alt-F2`

The *Batch Rename* operator can rename many data-block names at once.
When the operator is executed, a popup menu appears with some options and operations to modify the name.

Data Type
   The :ref:`data-block type <data-system-datablock-types>` to perform the batch rename operations on.
Data Source
   Where to look for the data-blocks that are intended to be renamed.
   *Selected* looks within the currently selected objects.
   While, *All* looks within the entire :doc:`View Layer </scene_layout/view_layers/index>`.
   To the left of this option gives a readout on how many data-blocks are able to be renamed.


Operations
----------

The *Batch Rename* has several sub Operations that to modify the data names.
The default operation is *Find/Replace* however, other operations can be added
to modify the data names farther.


Find/Replace
^^^^^^^^^^^^

*Find/Replace* searches for a particular string in the names and optionally replaces it with a new string.

Find
   The string of text to look for in names.
Replace
   The string of text to replace for in matching names found from the *Find* string.
Regular Expressions
   Enables the use of `Regular Expressions <https://en.wikipedia.org/wiki/Regular_expression>`__
   which are a powerful way to tailor the *Find*/*Replace* strings.
Case Sensitive
   Search results must match the *Find* string's case exactly.


Set Name
^^^^^^^^

*Set Name* works the most similar to `Rename Active Item`_
by renaming the current data-block without having to do a find and replace operation.

Method
   New
      Disregards the current name replacing it with the "new" name.
   Prefix
      Adds text to the beginning of the current name.
      This is useful for tools that look for special text in the prefix of a data-block name.
   Suffix
      Adds text to the end of the current name.
      This is useful for tools that look for special text in the Suffix of a data-block name.
Name
   Defines the new name or the text to add as a prefix/suffix,


Strip Characters
^^^^^^^^^^^^^^^^

*Strip Characters* cleans up names by removing certain
character types from either the beginning or the end of the name.

Spaces
   Strips any space characters from the name, e.g. ``Living Room   `` becomes ``Living Room``.
Digits
   Strips any numerical characters from the name, e.g. ``cube.001`` becomes ``cube.``.
Punctuation
   Strips any punctuation characters (``,.?!:; etc...``) from the name, e.g. ``cube.`` becomes ``cube``.

.. tip::

   Multiple character types can be removed at once by :kbd:`Shift-LMB` on the types.

Start
   Strips and any leading characters in the name.
End
   Strips and any trailing characters in the name.


Change Case
^^^^^^^^^^^

*Change Case* modifies the case of names to be on of the following:

Upper Case
   Changes all text to be in upper case, e.g. ``cube.001`` becomes ``CUBE.001``.
Lower Case
   Changes all text to be in lower case, e.g. ``CUBE.001`` becomes ``cube.001``.
Title Caps
   Changes all text to be in title case, e.g. ``living room`` becomes ``Living Room``.
