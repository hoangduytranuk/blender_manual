
************
Introduction
************

.. figure:: /images/editors_file-browser_introduction_editor.png

   The File Browser.


Usage
=====

The File Browser is used in all the file-related operations.
It has multiple use cases, while it's often used for save/load.

These include:

- Opening and saving blend-files.
- Importing/exporting other file formats.
- Picking new locations for existing file paths (images, video, fonts...).
- Browsing inside other blend-files, when using :doc:`Linked Libraries </data_system/linked_libraries>`.

You can also keep the File Browser open, as with any other editor type,
to browse through the file system. In this case, confirm/cancel buttons will be absent.

The main purpose of this is to be able to drag media files:

- Images into the :ref:`editors-sequencer-index` (to set background or apply as material textures).
- Media files into the :ref:`editors-sequencer-index`.

On the other hand, if the File Browser is opened for a file action (opening, saving, importing, etc.),
it will appear maximized and waiting for an operation to complete before returning to the former screen layout.


Header
======

Navigation icon buttons
   Tools for navigation of files.

   Left Arrow :kbd:`Backspace`
      Move to previous folder.
   Right Arrow :kbd:`Shift-Backspace`
      Move to next folder.
   Up Arrow :kbd:`P`
      Move up to parent directory.
   Cycle Arrows :kbd:`R`, :kbd:`NumpadPeriod`
      Refresh current folder.

Create Directory
   Prompts you to enter the name of a newly created directory inside the current one :kbd:`I`.
Recursion
   The number of directory levels to show at once in a flat way.

   - None (only the current directory)
   - Blend File (inside blend-files)
   - One level
   - Two Levels
   - Three levels

Display type
   Controls how files are displayed.

   - Short list
   - Detailed list
   - Thumbnails (show :doc:`previews </editors/file_browser/previews>`)
Display size
   The size of thumbnails or the width of columns.

   Tiny, small, normal, large
Sorting
   Sorts files by on of the following methods:

   - Alphabetically
   - By file type
   - By date of last edit
   - By file size
Show hidden
   Shows hidden files (starting with ``.``) :kbd:`H`.
File filtering
   File Type
      Filters files by type.

      - Folders
      - blend-files
      - Backup blend-files
      - Image files
      - Movie files
      - Script files
      - Font files
      - Sound files
      - Text files

   Data-Block Type
      Data-block type filtering inside blend-files.
   Search field
      Filter files by name.


File Region
===========

File Path
   The text field for the current path.
   :kbd:`Tab` will auto-complete an existing path.
   If you type a non existing directory path, you will be prompted to create that new directory.
File Name
   Text field to edit the file name and extension.
   If the background is red, a file with same name already exist in the folder.
   :kbd:`Tab` will auto-complete to existing names in the current directory.
Increment Filename ``+``, ``-``
   Adds/increases or removes/decreases a trailing number to your file name
   (used to make *versions* of a file).
Confirm
   The main button to Open Directory/File or Save (As) :kbd:`Return` or
   double-click with :kbd:`LMB` on the entry confirms with that file or data-block.

   - :kbd:`Shift-LMB` -- Open the file externally (selected in :doc:`/preferences/file`).
   - :kbd:`Alt-LMB` -- Open the directory externally (using the system's file manager).
Cancel
   Cancels the Open or Save file selection and closes the File Browser :kbd:`Esc` or
   by using the *Back to Previous* in the Info editor header.


Tool Shelf
==========

The left region displays different ways to find files and several options.
Clicking with :kbd:`LMB` on one of the entries, the File Browser will navigate to that folder.


System
------

The system panel contains a list of drives that are available
to navigate through to find files.


System Bookmarks
----------------

Bookmarks that are common for a particular operating system.


Bookmarks
---------

A :ref:`List View <ui-list-view>` of shortcuts to folders,
that you want to be able to access often without having to navigate to them in the File Browser.

Add ``+``
   This button adds the current directory to the list.


Recent
------

This is a list of recently accessed folders. You can control how many folders appear in this
list by going to the *File* tab of the :doc:`User Preferences </preferences/file>`,
in the *Recent Files* number button.


Operator Panel
--------------

Link/Append from Library
   See :doc:`Linked libraries </data_system/linked_libraries>`.
Open, Save, Save As Blender File
   See :doc:`/data_system/files/open` or :doc:`/data_system/files/save`.
Open, Replace, Save As Image
   See :doc:`/data_system/files/media/image_formats`.

For the common option:

Relative Path
   See :doc:`Relative paths </data_system/files/relative_paths>`.


Main Region
===========

Navigation
----------

Entering a Directory
   A single :kbd:`LMB` click on a directory enters that directory.
Parent Directory :kbd:`Backspace`, :kbd:`P`
   Takes you up one level of directory.


Arrow Keys
^^^^^^^^^^

Directory navigation is also possible through the arrow keys with :kbd:`Alt` pressed:

- Go to Parent :kbd:`Alt-Up`
- Previous Directory :kbd:`Alt-Left`
- Next Directory :kbd:`Alt-Right`


File Drop
^^^^^^^^^

You now can simply drag & drop files from your local file explorer into the Blender File Browser.
This will relocate the File Browser to the directory of the dropped file and the file will be selected.


Selection
---------

Select
   Both :kbd:`LMB` and :kbd:`RMB` works.
(De)select All :kbd:`A`
   Toggles selecting all files.
Dragging
   Dragging with :kbd:`LMB` starts a :ref:`border selection <bpy.ops.view3d.select_border>`.


Arrow Keys
^^^^^^^^^^

It is also possible to select/deselect files by "walking" through them using the arrow keys:

- Just using an arrow key, the next file in the chosen direction will be selected and all others deselected.
- Holding down :kbd:`Shift` while doing this does not deselect anything so it extends to the selection,
  plus it allows to deselect files by navigating into a block
  of already selected ones (minimum two files in sequence).
- Holding down :kbd:`Shift-Ctrl` further selects/deselects all files in between.

If no file is selected, the arrow key navigation selects the first or last file in the directory,
depending on the arrow direction.

If you select a directory and hit :kbd:`Return`, you will go into that directory
(and highlighting 'parent' entry will bring you up one level).


File Management
---------------

Delete Files :kbd:`Delete`, :kbd:`X`
   Delete the currently selected files.
Rename :kbd:`Ctrl-LMB`
   Can be used on a file or directory to rename it.
