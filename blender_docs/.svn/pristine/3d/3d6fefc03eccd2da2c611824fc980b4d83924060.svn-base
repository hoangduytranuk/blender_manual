.. _bpy.types.UserPreferencesView:

*********
Interface
*********

Interface configuration lets you change how UI elements are displayed and how they react.

.. figure:: /images/preferences_interface_tab.png


Display
=======

Scale
   Adjusts the size of fonts and buttons relative to the automatically detected DPI.
   During typical usage, you may prefer to use zoom which is available in many parts of Blender interface.
Line Width
   Scale of lines and points in the interface e.g. button outlines, edges and vertex points in the 3D View.

   Thin, Auto, Thick
Tooltips
   When enabled, a tooltip will appear when your mouse pointer is over a control.
   This tip explains the function of what is under the pointer,
   gives the associated hotkey (if any) and the Python function that refers to it.
Python Tooltips
   Displays a property's Python information below the tooltip.
Object Info
   Display the active Object name and frame number at the bottom left of the 3D View.
Large Cursors
   Use large mouse cursors when available.
View Name
   Display the name and type of the current view in the top left corner of the 3D View.
   For example: *User Perspective* or *Top Orthographic*.
Playback FPS
   Show the frames per second screen refresh rate while an animation is played back.
   It appears in the viewport corner, displaying red if the frame rate set cannot be reached.
Global Scene
   Forces the current scene to be displayed in all screens (a project can consist of more than one scene).
Object Origin Size
   Diameter of 3D Object centers in the viewport (value in pixels from 4 to 10).

Display Mini Axis
   Show the mini axis at the bottom left of the viewport.
Size
   Size of the mini axis.
Brightness
   Adjust brightness of the mini axis.


Warnings
========

Prompt Quit
   When exiting Blender, a pop-up will ask you whether or not you really want to quit
   (currently only available on MS-Windows).


View Manipulation
=================

Cursor Depth
   Use the depth under the mouse when placing the cursor.

.. _prefs-auto-depth:

Auto Depth
   Use the depth under the mouse to improve view pan, rotate, zoom functionality.
   Useful in combination with *Zoom To Mouse Position*.

.. _prefs-zoom-mouse-pos:

Zoom to Mouse Position
   When enabled, the mouse pointer position becomes the focus point of zooming instead of the 2D window center.
   Helpful to avoid panning if you are frequently zooming in and out.
Rotate Around Selection
   The selected object (bounding box center) becomes the rotation center of the viewport.
   When there is no selection the last selection will be used.

   .. hint::

      This may seem ideal behavior.
      However, it can become problematic with larger objects such as a terrain-mesh,
      where the center is not necessarily your point of interest.

Global Pivot
   Lock the same rotation/scaling pivot in all 3D Views.
Camera Parent Lock
   When the camera is locked to the view and in fly mode, transform the parent rather than the camera.

.. _prefs-interface-auto-perspective:

Auto Perspective
   Automatically to perspective Top/Side/Front view after using User Orthographic.
   When disabled, Top/Side/Front views will retain Orthographic or Perspective view
   (whichever was active at the time of switching to that view).
Smooth View
   Length of time the animation takes when changing the view with the numpad
   (Top/Side/Front/Camera...). Reduce to zero to remove the animation.
Rotation Angle
   Rotation step size in degrees, when :kbd:`Numpad4`, :kbd:`Numpad6`, :kbd:`Numpad8`,
   or :kbd:`Numpad2` are used to rotate the 3D View.


2D Viewports
============

Minimum Grid Spacing
   The minimum number of pixels between grid lines in a 2D (i.e. top orthographic) viewport.
Time Code Style
   Format of Time Codes displayed when not displaying timing in terms of frames.
   The format uses '+' as separator for sub-second frame numbers,
   with left and right truncation of the timecode as necessary.
Zoom To Frame Type
   Defines what time range (around the cursor) will be displayed
   when the *View Frame* :kbd:`Numpad0` is performed.

   Keep Range
      The currently displayed time range is preserved.
   Seconds
      The number of seconds specified in the *Zoom Seconds* field will be shown around the cursor.
   Keyframes
      The number of animation keyframes defined in the *Zoom Keyframes* field will be shown around the cursor.

.. _prefs-interface-manipulator:

Manipulator
   Turns manipulator on and off.
Size
   Diameter of the manipulator.
Handle Size
   Size of manipulator handles, as a percentage of the manipulator radius (*size*/ 2).
Hotspot
   Hotspot size (in pixels) for clicking the manipulator handles.


Menus
=====

Open on Mouse Over
   Select this to have the menu open by placing the mouse pointer over the entry instead of clicking on it.
Menu Open Delay
   Time for the menu to open.
Top Level
   Time delay in 1/10 second before a menu opens (*Open on Mouse Over* needs to be enabled).
Sub Level
   Same as above for sub menus (for example: :menuselection:`File --> Open Recent`).


.. _prefs-pie-menu:

Pie Menus
=========

Animation Timeout
   Length of animation when opening Pie Menus.
Recenter Timeout
   The window system tries to keep the pie menu within the window borders.
   Pie menus will use the initial mouse position as center for this amount of time, measured in 1/100ths of a second.
   This allows for fast dragged selections.
Radius
   The size of the Pie Menu set with the distance (in pixels) of the menu items from the center of the pie menu.
Threshold
   Distance from center before a selection can be made.
Confirm Threshold
   Distance threshold after which selection is made (zero disables).


Splash
======

Show Splash
   Display the :ref:`splash` when starting Blender.
