
******************
Collection Manager
******************

This add-on adds new functionality for the management of collections via a pop-up in the 3D Viewport.
It also offers a simple display and modification of the relationship of objects with collections.

.. figure:: /images/addons_interface_collection-manager_popup.png
   :align: center


Activation
==========

- Open Blender and go to Preferences then the Add-ons tab.
- Click Interface then Collection Manager to enable the script.


Description
===========

Use :kbd:`M` call up the main Collection Manager pop-up in the 3D View when in Object Mode.

View Layer
   Render
      Enable/disable rendering of this view layer with this checkbox.
   View Layer
      :ref:`ui-data-block` of the current view layer.

Filter (funnel icon)
   Choose which restriction toggles are shown in the interface.
Global Restrictions (checkbox, cursor, eye, screen, camera icons)
   See the Outliner page for information about :ref:`Restrictions <editors-outliner-restriction-columns>`.

   - :kbd:`LMB` -- Enable the restrictions for all collections. Click again to restore the previous state.
   - :kbd:`Shift-LMB` -- Invert the restriction state on all collections.

Tree View
   Shows the collections within the current selected scene.
   The active collection is synced to tree view selection.

   Expansion (small triangle icon)
      - :kbd:`LMB` -- Expand/collapse children.
      - :kbd:`Shift-LMB` -- Expand/collapse children and descendants.
   Name
      Double :kbd:`LMB`-click to rename the collection.

   Set Object (box icon)
      - :kbd:`LMB` -- Move object(s) to collection.
      - :kbd:`Shift-LMB` -- Add/Remove object(s) to/from collection.

   Local Restrictions (checkbox, cursor, eye, screen, camera icons)
      - :kbd:`LMB` -- Toggle collection restriction on/off.
      - :kbd:`Shift-LMB` -- Isolate the collection's restriction, preserving parents if need be.
        Click again to restore the previous state.
      - :kbd:`Ctrl-LMB` -- Toggles the restrictions of the collection and it's children on/off.

   Remove ``X``
      Remove the collection.

   Filtering
      By Name (box icon)
         A text field to filter collections by name.
      Invert (magnifying glass icon)
         Invert filtering (inverts the collections shown in the tree view so that what is shown is hidden
         and what was hidden is shown).
      By Selected (box icon)
         Filter collections by selected objects (show only collections that contain the selected objects).

Add Collection, Add Subcollection
   Self-explanatory.

Phantom Mode
   All visibility changes made in this mode will be discarded when it's disabled.

   Enabling Phantom Mode saves the current state of your restrictions and
   allows you to edit them without fear of losing your current state.
   When finished, disabling Phantom Mode will restore the saved state.

   Note: You will be unable to edit anything other than the collections' restrictions while in Phantom Mode.

.. admonition:: Reference
   :class: refbox

   :Category:  Interface
   :Description: Collection management system.
   :Location: 3D Viewport
   :File: collection_manager folder
   :Author: imaginer (Ryan Inch)
   :Maintainer: imaginer
   :License: GPL
   :Support Level: Community
   :Note: This add-on is bundled with Blender.
