.. _bpy.types.SpaceTextEditor:
.. _bpy.ops.text:

***********
Text Editor
***********

Blender has a *Text Editor* among its editor types,
accessible via the *Editor type* menu, or the shortcut :kbd:`Shift-F11`.


Header
======

The newly opened Text editor is empty, with a very simple header.
More options become available when a text file is created or opened.

.. _fig-text-header-plain:

.. figure:: /images/editors_text-editor_header.png

   Text header.

.. _fig-text-header-full:

.. figure:: /images/editors_text-editor_header-loaded.png

   Text header with a text loaded.

Editor type
   The standard editor selection button.
Menus
   Editors `Menus`_.
Text
   A :ref:`data-block menu <ui-data-block>` to select a text or to create a new one.
   After that the header will change.
Show
   The following three buttons toggle display options:
   line numbers, word-wrap text and syntax highlighting.

.. _editors-text-run-script:

Run Script / Script Node Update
   Executes the text as a Python script :kbd:`Alt-P`. See `Script and Templates`_.
Register
   Registers the current text data-block as a module on loading (the text name must end with ``.py``).
   Read more about the registration of Python modules in
   `API documentation <https://docs.blender.org/api/2.80/info_overview.html#registration>`__.


Menus
-----

View
   Bottom of File
      Moves the view and cursor to the end of the text.
   Top of File
      Moves the view and cursor to the start of the text.
Text
   Create Text Block
      Creates a new internal text.
   Open Text Block
      Loads a text, a :doc:`File Browser </editors/file_browser>` appears :kbd:`Alt-O`.
   Reload
      Reopens (reloads) the current buffer (all non-saved modifications are lost) :kbd:`Alt-R`.
   Save
      Saves an already open file :kbd:`Alt-S`.
   Save As
      Saves unsaved text as a text file,
      a :doc:`File Browser </editors/file_browser>` appears :kbd:`Shift-Ctrl-Alt-S`.
   Make Internal
      Stores the text inside the blend-file.
   Run Script
      Executes the text as a Python script :kbd:`Alt-P`.
      See `Script and Templates`_.
Edit
   Cut :kbd:`Ctrl-X`
      Cuts out the marked text into the text clipboard.
   Copy :kbd:`Ctrl-C`
      Copies the marked text into the text clipboard.
   Paste :kbd:`Ctrl-V`
      Pastes the text from the clipboard at the cursor location in the Text editor.
   Duplicate Line :kbd:`Ctrl-D`
      Duplicates the current line.
   Move line(s) up :kbd:`Shift-Ctrl-Up`
      Swaps the current/selected line(s) with the above.
   Move line(s) down :kbd:`Shift-Ctrl-Down`
      Swaps the current/selected line(s) with the below.
   Select
      Select Line, Select All.
   Jump
      Shows the Jump pop-up, which lets you select a line number where to jump to.
   Find...
      Shows the Find panel in the Sidebar region.
   Text Auto Complete :kbd:`Ctrl-Spacebar`
      Shows a selectable list of words already used in the text.
   Text To 3D Object
      One Object, One Object per line.
Format
   Indent
      Indents the selection :kbd:`Tab`.
   Unindent
      Un-indents the selection :kbd:`Shift-Tab`.
   Comment
      Turns the selected lines into a Python comment.
   Uncomment
      Uncomments the selected lines.
   Convert Whitespace
      Converts between tab or space indentation.
Template
   See `Script and Templates`_.

   Python, OpenShading Language


Script and Templates
--------------------

The most notable keystroke is :kbd:`Alt-P` which makes the content of the buffer
being parsed by the internal Python interpreter built into Blender.
Before going on it is worth noticing that Blender comes with a fully functional Python interpreter built-in,
and with a lots of Blender-specific modules,
as described in the :doc:`/advanced/scripting/index` section.

The *Text Editor* has now also some dedicated Python scripts,
which add some useful writing tools, like a class/function/variable browser, completion...
You can access them through the Template menu in the header.


Footer
======

The Text editor is special in the fact that it contains a footer UI region.
This footer displays if the text is saved internal or external and
if there are unsaved changes to an external file.
For external files, this region also displays the file path to the text file.


Main View
=========

Typing on the keyboard produces text in the text buffer.
As usual, pressing, dragging and releasing :kbd:`LMB` selects text.

.. tip:: Usages for the Text editor

   The Text editor is handy also when you want to share your blend-files with others.
   The Text editor can be used to write in a ``README`` text explaining the contents of your blend-file.
   Be sure to keep it visible when saving!
