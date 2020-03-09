.. _vertex-merging:

**************
Merge Vertices
**************

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Vertex --> Merge...`,
               :menuselection:`Context Menu --> Merge`
   :Hotkey:    :kbd:`Alt-M`

This tool allows you to merge all selected vertices to a unique one, dissolving all others.
You can choose the location of the surviving vertex in the menu this tool pops up before
executing:

At First
   Only available in *Vertex* select mode,
   it will place the remaining vertex at the location of the first one selected.
At Last
   Only available in *Vertex* select mode,
   it will place the remaining vertex at the location of the last one selected (the active one).
At Center
   Available in all select modes,
   it will place the remaining vertex at the center of the selection.
At Cursor
   Available in all select modes,
   it will place the remaining vertex at the 3D Cursor.
Collapse
   Every island of selected vertices (connected by selected edges) will merge on its own median center,
   leaving one vertex per island.
   It is also available *via* the :menuselection:`Mesh --> Edges --> Collapse` menu option...

Merging vertices of course also deletes some edges and faces. But Blender will do everything
it can to preserve edges and faces only partly involved in the reunion.

.. note::

   *At First* and *At Last* depend on that the selection order is saved:
   the order is lost, for instance, after changing selection mode.

UVs
   If *UVs* is ticked in the :ref:`ui-undo-redo-adjust-last-operation` panel,
   the UV mapping coordinates, if existing, will be corrected to avoid image distortion.


By Distance
-----------

Todo.
