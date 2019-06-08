
************
Startup File
************

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`File --> Save Startup File`
   :Hotkey:    :kbd:`Ctrl-U`

Saves the current file as the default Blender file ``startup.blend``.
This file is loaded every time Blender is opened or a new file is generated (:menuselection:`File --> New`).
It contains the default :doc:`startup scene </editors/3dview/startup_scene>` included with Blender.
This startup scene can be replaced by your own customized setup.

To change the startup scene, make all of the desired changes to the current scene or
current file and :menuselection:`File --> Save Startup File`.
Saving the ``startup.blend`` still stores Preferences in the file.
Only if a ``userpref.blend`` exists, it will use the preferences from that file.

If you want to go back to the original startup file
you can reset Blender to its :ref:`factory settings <factory-settings>`.
