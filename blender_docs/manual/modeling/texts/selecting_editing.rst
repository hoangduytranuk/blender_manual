
.. |atilde| unicode:: U+000E3
.. |aacute| unicode:: U+000E1
.. |agrave| unicode:: U+000E0
.. |aring|  unicode:: U+000E5
.. |euml|   unicode:: U+000EB
.. |oslash| unicode:: U+000F8

*******************
Selecting & Editing
*******************

Editing text is quite different from other object types in Blender, and happens mainly in two areas.
First, the 3D View, where you type your text, and have a few shortcuts, e.g. for applying
styles (see :ref:`modeling-text-character`) -- note however, that most Blender hotkeys you know
in *Edit Mode* do not exist for texts. The second place is the Properties Editor, especially the *Font* tab.


Selecting & Cursor
==================

.. figure:: /images/modeling_texts_selecting-editing_cursor.png
   :width: 340px

   Text in Edit Mode.

In *Edit Mode*, your text has a white cursor, and as in any text editor,
it determines where new chars will be inserted.

Next/Previous Character
   You can move the cursor with the arrow keys :kbd:`Left` or :kbd:`Right`.
Next/Previous Word
   To move the cursor on a word's boundary, use :kbd:`Ctrl-Left` or :kbd:`Ctrl-Right`.
Line Begin/End
   :kbd:`Home` and :kbd:`End` move the cursor to the beginning and end of a line respectively.
Next/Previous Line
   To jump between lines, use :kbd:`Up` or :kbd:`Down`.
Next/Previous Page
   To jump back/forward ten lines at a time, use :kbd:`PageUp` or :kbd:`PageDown`.

Hold :kbd:`Shift` while using the arrow keys to select a part of the text.
You can use it to specify different materials, the normal/bold/italic style,
and not much more.


Editing
=======

The menu of the 3D View header offers few options,
and there is no *Specials* menu. You have no transform nor mirror tools, and so on.
However, you can apply to texts the same modifiers as for curves.


Basic
-----

Editing *Text* is similar to using a standard text editor but is not as
full-featured and has some differences:

Exit *Edit Mode*
   :kbd:`Tab` does not insert a tab character in the text,
   but rather enters and exits *Edit Mode*, as with other object types.
Copy
   To copy text to the buffer, use :kbd:`Ctrl-C` or the *Copy* button in the Tool Shelf.
Cut and Copy
   To cut and copy text to the buffer, use :kbd:`Ctrl-X` or the *Cut* button in the Tool Shelf.
Paste
   To paste text from the buffer, use :kbd:`Ctrl-V` or the *Paste* button in the Tool Shelf.
Delete all text
   To completely erase or delete all text, use :kbd:`Ctrl-Backspace`.

The text buffer is in sync with the desktop clipboard.
But if it is used within Blender the text formatting will be copied as well.
For other ways of inserting a text, see `Inserting Text`_ below.


Special Characters
------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Text --> Special Characters`

If you need special characters (such as accented chars, which are not on your keyboard)
you can produce many of them using a combination of two other characters. To do so,
type the main char, press :kbd:`Alt-Backspace`,
and then press the desired "modifier" to produce the special character.
Some examples are given below:

.. list-table::
   :widths: 20 80

   * - |atilde|

     - :kbd:`A`, :kbd:`Alt-Backspace`, :kbd:`~`

   * - |aacute|

     - :kbd:`A`, :kbd:`Alt-Backspace`, :kbd:`'`

   * - |agrave|

     - :kbd:`A`, :kbd:`Alt-Backspace`, :kbd:`\\`

   * - |aring|

     - :kbd:`A`, :kbd:`Alt-Backspace`, :kbd:`O`

   * - |euml|

     - :kbd:`E`, :kbd:`Alt-Backspace`, :kbd:`"`

   * - |oslash|

     - :kbd:`O`, :kbd:`Alt-Backspace`, :kbd:`/`


Inserting Text
--------------

You can insert text in two ways: from the internal text buffer
(as described above), or from a text file.

To load text from a text file, use the :menuselection:`Text --> Paste File` tool.
This will bring up a :doc:`File Browser </editors/file_browser/index>` for navigating to a valid UTF-8 file.
As usual, be careful that the file does not have too many characters,
as interactive response will slow down.


Converting Text Objects
-----------------------

Converting to Text Object
^^^^^^^^^^^^^^^^^^^^^^^^^

Using an existing text data-block, you can convert it to an object from the Text editor's header,
select :menuselection:`Edit --> Text to 3D Object`,
*One Object* or *One Object per Line* depending on your needs.

It is also possible to paste from the clipboard or a file from the *Edit* menu, while editing 3D Text.


Converting to 3D Mesh
^^^^^^^^^^^^^^^^^^^^^

It is possible to convert a Text Object to a 3D Mesh object.
This can be useful so that you may edit the vertices in *Edit Mode*,
but you will lose the ability to edit the text itself.

This can be done, using :ref:`object-convert-to` in *Object Mode*.
Now you can return to *Edit Mode* and manually edit the vertices.

.. tip::

   The result is usually a bit messy, so it may be useful to use a *Limited Dissolve* deletion or *Remesh* Object
   :doc:`Modifier </modeling/modifiers/index>` at a low threshold to clean up your mesh.


Assigning Materials
-------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Panel:     :menuselection:`Properties editor --> Materials`

Each character can have a different *Material index* in order to have different
materials on different characters.

You can assign indices either as you type, or after by selecting blocks of text and
clicking on the *Assign* button in the Materials panel.

.. _fig-texts-edit-rgb:

.. figure:: /images/modeling_texts_selecting-editing_material-index-example.png

   Red Green Blue.

For example, to create Fig. :ref:`fig-texts-edit-rgb`
you would need to create three separate materials and three separate material indices.
Each word would be assigned a *Material index* by selecting the characters for each word
and clicking the *Assign* button. Fig. :ref:`fig-texts-edit-rgb` is still one single *Text* object.
