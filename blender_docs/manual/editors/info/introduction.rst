
************
Introduction
************

The Info Editor is found at the top of the Default Screen and has the following components.


Header
======

.. figure:: /images/editors_info_introduction_info-editor.png

   Info Editor header.

   Editor Type Selector (red), Menus (blue), Screen Data-block (green),
   Scene Data-block (orange), Engine Selector (purple), Resource Information (aqua).


Menus
-----

Provides access to the Blender's main menu options.


File
^^^^

See :doc:`/editors/info/file` menu.

Edit
^^^^

Preferences
   Opens the :doc:`Blender Preferences </editors/preferences/introduction>` in a new window.


Render
^^^^^^

Render
   See :doc:`/render/output/render_panel`.
Show/Hide Render View :kbd:`F11`
   Shows (or hides) the editor where the last render was performed.
Play Rendered Animation :kbd:`Ctrl-F11`
   Plays the last rendered animation using the internal :doc:`/render/output/animation_player` or
   an external video player, which has to be defined in the File tab of the Preferences.


Window
^^^^^^

Duplicate Window :kbd:`Ctrl-Alt-W`
   Duplicates the current window so that a new one is created with the same screen layout and size.
   Useful for multiple monitors.
Toggle Window Fullscreen :kbd:`Alt-F11`
   Toggles full screen on or off.
Screenshot, Screencast
   See :doc:`/editors/info/screen_capture`.
Toggle System Console
   Shows or hides the :doc:`System Console </advanced/command_line/introduction>` (on MS-Windows).


Help
^^^^

See :ref:`help-menu`.


Workspaces
----------

Tabs to select :doc:`workspaces </interface/window_system/workspaces>`.


Controls
--------

Back to Previous
   A button shown when an area is maximized to return to tiled areas.
Scene
   :ref:`Data-block menu <ui-data-block>` to select different :doc:`Scenes </scene_layout/scene/introduction>`.
   Having multiple Scenes allows you to work with separate virtual environments,
   with completely separate data, or with object and/or mesh data linked between them.
Engine
   Gives a list of selectable render engines.
Render/Baking progress
   A progress bar and a cancel button are shown while rendering or baking.
   Hovering over them shows a time estimate.
Report Message
   Label for an operator to display results or warnings. It disappears after a short time.
   By clicking with :kbd:`LMB` on the icon on the left side, the full report is copied into a new text data-block,
   which you can be open in the Text Editor.
Blender Icon
   Clicking on the Blender logo opens the :ref:`splash`.
Blender version
   This label displays the Blender version.
Resource Information
   Scene
      Displays information about the current loaded scene dependent on the mode and object type.
      When two numbers are shown, the first one means the selected, and the second one means the total count.
      This can be the number of vertices, faces, triangles or bones, as well as the selected objects and lamps.
   Memory
      The "Mem" label shows the calculated memory consumption by Blender.
      This can help to identify, when you are reaching the limits of your hardware.
   Active Object
      The object type of the current selected object.


.. _info-report-console:

Report Console
==============

When the Info Editor's area is scaled up, it reveals the Report console,
where a scripting trail is displayed.
Whenever an operator has been executed, it leaves a report, creating a log.

.. figure:: /images/editors_info_introduction_report-console.png

   The Report Console after adding a cube.
