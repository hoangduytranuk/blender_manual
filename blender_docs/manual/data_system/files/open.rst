
*************
Opening Files
*************

.. figure:: /images/data-system_files_open_file-browser-open.png

   The File Browser.


Usage
=====

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Info Editor --> File --> Open`
   :Hotkey:    :kbd:`Ctrl-O` or :kbd:`F1`

The upper text field displays the current directory path,
and the lower text field contains the selected filename.

.. warning:: For Linux and macOS Users

   When exiting you are **not** asked to save unsaved changes to the scene you were previously working on.
   So take care to save your work.

   On MS-Windows, there is a :ref:`prefs-save-load` option to warn on exit.


Options
=======

.. _file-load-ui:

Load UI
   When *Load UI* is checked, it loads the screen layout saved inside each blend-file,
   replacing the current layout. Otherwise the file screen layout is ignored.

   .. tip::

      If you want to work on the blend-file using your own defaults, start a fresh Blender,
      then open the File Browser and turn off the *Load UI* button, and then open the file.

Trusted Source
   When enabled, Python scripts and drivers that may be included in the file will be run automatically.
   Enable this only if you created the file yourself,
   or you trust that the person who gave it to you did not include any malicious code with it.
   See :doc:`Python Security </advanced/scripting/security>` to configure default trust options.


.. _other-file-open-options:

Other File Open Options
=======================

From the *File* menu, you can also open files with the following tools:

Open Recent
   Lists recently used files. Click on one to load it in.
Recover Last Session
   This will load the ``quit.blend`` file Blender automatically saved just before exiting.
   This option enables you to recover your last work session if, for example, you closed Blender by accident.
Recover Auto Save
   This will allow you to open an automatically saved file to recover it.

.. seealso::

   :ref:`Auto Saves <troubleshooting-file-recovery>`
