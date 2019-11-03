
.. |atilde| unicode:: U+000E3
.. |aacute| unicode:: U+000E1
.. |agrave| unicode:: U+000E0
.. |acircumflex| unicode:: U+000E2
.. |aring|  unicode:: U+000E5
.. |ash|  unicode:: U+000E6
.. |aordinal|  unicode:: U+000AA
.. |euml|   unicode:: U+000EB
.. |oslash| unicode:: U+000F8
.. |ccedilla| unicode:: U+000E7
.. |cent| unicode:: U+000A2
.. |dagger| unicode:: U+02020
.. |doubledagger| unicode:: U+02021
.. |section| unicode:: U+000A7
.. |copyright| unicode:: U+000A9
.. |registered| unicode:: U+000AE
.. |trademark| unicode:: U+02122
.. |half| unicode:: U+000BD
.. |division| unicode:: U+000F7
.. |plusminus| unicode:: U+000B1

*******************
Selecting & Editing
*******************

Editing text is quite different from other object types in Blender, and happens mainly in two areas.
First, the 3D View, where you type your text, and have a few shortcuts, e.g. for applying
styles (see :ref:`modeling-text-character`) -- note however, that most Blender hotkeys you know
in Edit Mode do not exist for texts. The second place is the Properties editor, especially the *Font* tab.


Selecting & Cursor
==================

.. figure:: /images/modeling_texts_selecting-editing_cursor.png
   :width: 340px

   Text in Edit mode.

In Edit Mode, your text has a white cursor, and as in any text editor,
it determines where new chars will be inserted.

Next/Previous Character :kbd:`Left`/ :kbd:`Right`
   You can move the cursor with the arrow keys.
Next/Previous Word :kbd:`Ctrl-Left`/ :kbd:`Ctrl-Right`
   To move the cursor on a word's boundary.
Line Begin/End :kbd:`Home`/ :kbd:`End`
    Move the cursor to the beginning and end of a line respectively.
Next/Previous Line :kbd:`Up`/ :kbd:`Down`
   To jump between lines.
Next/Previous Page :kbd:`PageUp`/ :kbd:`PageDown`
   To jump back/forward ten lines at a time.

Hold :kbd:`Shift` while using the arrow keys to select a part of the text.
You can use it to specify different materials, the normal/bold/italic style...


Editing
=======

The menu of the 3D View header offers few options. You have no transform nor mirror tools, and so on.


Basic
-----

Editing *Text* is similar to using a standard text editor but is not as
full-featured and has some differences:

Exit Edit Mode
   :kbd:`Tab` does not insert a tab character in the text,
   but rather enters and exits Edit Mode, as with other object types.
Copy :kbd:`Ctrl-C`
   To copy text to the buffer, use the shortcut or the matching entry in the *Edit* menu.
Cut and Copy :kbd:`Ctrl-X`
   To cut and copy text to the buffer, use the shortcut or the matching entry in the *Edit* menu.
Paste :kbd:`Ctrl-V`
   To paste text from the buffer, use the shortcut or the matching entry in the *Edit* menu.
Delete all text :kbd:`Ctrl-Backspace`
   Completely erase or delete all text.

The text buffer is in sync with the desktop clipboard.
But if it is used within Blender the text formatting will be copied as well.
For other ways of inserting a text, see `Inserting Text`_ below.


Special Characters
------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Edit --> Special Characters`

This is a limited character map to insert characters which aren't available from the keyboard.
Many other special characters can be "composed", see `Accent Characters`_ below.
If you need others, you will have to copy-paste them from an external editor or charmap tool.


Accent Characters
-----------------

Many special characters (such as accented chars, which are not directly available on your keyboard)
can be "composed" using a combination of two other characters. To do so,
type the main char, press :kbd:`Alt-Backspace`,
and then press the desired "modifier" to produce the special character.
Some examples are given below:

.. hlist::
   :columns: 2

   - |atilde|: :kbd:`A`, :kbd:`Alt-Backspace`, :kbd:`~`
   - |aacute|: :kbd:`A`, :kbd:`Alt-Backspace`, :kbd:`'`
   - |agrave|: :kbd:`A`, :kbd:`Alt-Backspace`, :kbd:`Backslash`
   - |acircumflex|: :kbd:`A`, :kbd:`Alt-Backspace`, :kbd:`^`
   - |aring|: :kbd:`A`, :kbd:`Alt-Backspace`, :kbd:`O`
   - |ash|: :kbd:`A`, :kbd:`Alt-Backspace`, :kbd:`E`
   - |aordinal|: :kbd:`A`, :kbd:`Alt-Backspace`, :kbd:`Minus`
   - |euml|: :kbd:`E`, :kbd:`Alt-Backspace`, :kbd:`"`
   - |ccedilla|: :kbd:`C`, :kbd:`Alt-Backspace`, :kbd:`Comma`
   - |cent|: :kbd:`C`, :kbd:`Alt-Backspace`, :kbd:`|`
   - |oslash|: :kbd:`O`, :kbd:`Alt-Backspace`, :kbd:`Slash`

   - |section|: :kbd:`S`, :kbd:`Alt-Backspace`, :kbd:`S`
   - |dagger|: :kbd:`|`, :kbd:`Alt-Backspace`, :kbd:`Minus`
   - |doubledagger|: :kbd:`|`, :kbd:`Alt-Backspace`, :kbd:`=`
   - |copyright|: :kbd:`O`, :kbd:`Alt-Backspace`, :kbd:`C`
   - |registered|: :kbd:`O`, :kbd:`Alt-Backspace`, :kbd:`R`
   - |trademark|: :kbd:`T`, :kbd:`Alt-Backspace`, :kbd:`M`

   - |half|: :kbd:`1`, :kbd:`Alt-Backspace`, :kbd:`2`
   - |division|: :kbd:`Minus`, :kbd:`Alt-Backspace`, :kbd:`:`
   - |plusminus|: :kbd:`Minus`, :kbd:`Alt-Backspace`, :kbd:`Plus`


.. _bpy.ops.font.text_paste_from_file:

Inserting Text
--------------

You can insert text in two ways: from the internal text buffer
(as described above), or from a text file.

To load text from a text file, use the :menuselection:`Text --> Paste File` tool.
This will bring up a :doc:`File Browser </editors/file_browser>` for navigating to a valid UTF-8 file.
As usual, be careful that the file does not have too many characters,
as interactive response will slow down.


Setting Case
------------

You can change the text case by selecting it then clicking the *To Upper* or
*To Lower* in the Toolbar.


Font Style
----------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`3D View --> Font`
   :Panel:     :menuselection:`Properties --> Text --> Font`

To apply the *Bold* / *Italics* / *Underline* / *Small Caps* attribute to a set of characters,
you either turn on the related setting prior to typing characters,
or highlight (select) some existing text, and then toggle desired style from the menu.

.. warning::

   Blender's *Bold* and *Italic* buttons do not work the same way as in other applications,
   as they also serve as placeholders for you to load up other fonts manually,
   see `Loading and Changing Fonts`_ below.


Loading and Changing Fonts
--------------------------

Blender comes with a *built-in* font by default that is displayed in
each of the four font style data-block menus.
The *built-in* font is always present and shows in this list as "Bfont".
The data-block menu contains a list displaying the currently loaded fonts.
Select one for each font style.

To load a different *Font*, click one of the *Load* buttons
in the *Font* panel and navigate to a font file.
The :doc:`File Browser </editors/file_browser>` will give all valid fonts a capital "F" icon.

If you select a font that is unsupported by Blender, you will get the error ``Not a valid font``.

.. note:: Location of Fonts on Unix

   Fonts are typically located under ``/usr/lib/fonts``, or some variant like ``/usr/lib/X11/fonts``,
   but not always. They may be in other locations as well,
   such as ``/usr/share/local`` or ``/usr/local/share``, and possibly related sub-trees.

Remember that the same font will be applied to all chars with same style in a text,
but that a separate font is required for each style.
For example, you will need to load an *Italics* font in order to make characters or words italic.
Once the font is loaded you can apply that font "Style" to the selected characters or the whole object.
In all, you would need to load a minimum of four different types of fonts to represent each style
(Normal, Italics, Bold, Bold & Italics).

It is important to understand, that Blender does not care what font
you load for "normal", "bold", etc., styles.
This is how you can have up to four different fonts in use in the same text,
but you have to choose between different styles of a same font, or different fonts.
Blender has a number of typographic controls for changing the style and layout of text,
found in the *Font* panel.

.. seealso::

   The :ref:`Font panel <modeling-text-character>` description.


Converting Text Objects
-----------------------

Converting to Text Object
^^^^^^^^^^^^^^^^^^^^^^^^^

Using an existing text data-block, you can convert it to an object from the *Text* editor's header,
select :menuselection:`Edit --> Text to 3D Object`,
*One Object* or *One Object per Line* depending on your needs.

It is also possible to paste from the clipboard or a file from the *Edit* menu, while editing 3D Text.


Converting to a Mesh or Curve
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In Object Mode, it is possible to convert a text object to a mesh or curve one, see :ref:`object-convert-to`.

.. tip::

   The topology of the result is usually a bit messy,
   so it may be useful to use a *Limited Dissolve* deletion,
   or apply a :doc:`Remesh modifier </modeling/modifiers/generate/remesh>` at a low threshold, to clean up your mesh.


Assigning Materials
-------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit
   :Panel:     :menuselection:`Properties editor --> Materials`

Each character can have a different *Material index* in order to have different materials
on different characters.

You can assign indices either as you type, or after by selecting blocks of text and
clicking on the *Assign* button in the *Materials* panel.

.. figure:: /images/modeling_texts_selecting-editing_material-index-example.png

   Red Green Blue text example.
