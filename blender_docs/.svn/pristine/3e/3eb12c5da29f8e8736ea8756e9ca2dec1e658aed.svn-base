
*********************
Display & View Panels
*********************

Display Panel
=============

This panel lets you configure some visualization parameters of the viewport.

Only Render
   Displays only items that will be rendered.
   This option hides visualizations, overlays, the 3D cursor, and the grid floor.
   The :doc:`3D manipulator widget </editors/3dview/object/editing/transform/control/manipulators>`
   has to be toggled separately.

   This can be useful for a preview and for :doc:`OpenGL </render/opengl>` viewport rendering.

   .. note::

      While the option displays the regular viewport without distracting elements,
      the objects displayed do **not** match the final render output.

      Options such as restrict-render, modifiers render option,
      dupli-parents and render layers are not taken into account.

Outline Selected
   If disabled, the orange outline around your selected objects in
   *Solid*, *Shaded*, *Textured* draw types will no longer be displayed.
World Background
   Creates an estimation of what the world background will look like and uses it to draw the background.
All Object Origins
   Forces the origin dot of objects to always be visible, even for non-selected objects
   (by default, unselected objects' origins might be hidden by geometry in solid/shaded/textured shadings).
Relationship Lines
   Controls whether the dashed parenting, constraining, hooking, etc., lines are drawn.
Grid Floor
   Grid Floor is a finite grid which is shown in views that are not orthographically aligned (top, front, side).
   It lays on the global XY plane. The checkbox lets you show or hide that grid.
   In aligned orthographic views an infinite grid is shown.

   Axis
      Controls which global axes are shown as colored lines (Grid floor only).
      Their length depend on the defined size of that grid.

      X, Y, Z
   Lines
      Controls the total number of lines that make the grid, in both directions
      (odd values will be rounded down).
   Scale
      Controls the distance between the grid lines.

      This is also used for the size of newly added objects.
   Subdivisions
      Controls the number of sub-lines that appear in each cell of the grid.
      In aligned orthographic views the level of subdivision depend on the zoom.
Toggle Quad View
   Toggles the four view 3D View.
   :doc:`Read more about arranging areas </interface/window_system/areas>`.


View Panel
==========

The *View Properties* panel lets you set other settings regarding the 3D View.
You can show it with the :menuselection:`View --> View Properties...` menu entry.

Lens
   Control the focal length of the 3D View camera in millimeters,
   unlike a :doc:`rendering camera </render/cycles/camera>`.
Lock to Object
   Lock to Object lets you define an object in the *Object* Data ID as the center of the view.
   In that case, the view can be rotated around or zoomed towards that central object,
   but not on translation, unless you translate that itself object
   (this option is not available in a camera view).
Lock to Cursor
   Lock the center of the view to the position of the 3D cursor.
   It is only available when *Lock to Object* is not active.

.. _3dview-lock-camera-to-view:

Lock Camera to View
   When in camera view, all changes in the view (pans, rotations, zooms) will affect the active camera,
   which will follow all those changes. The camera frame will be outlined with a red dashed line.

.. _3dview-view-clip:

Clip Start and Clip End
   Adjust the minimum and maximum distances range to be visible for the viewport camera.
   Objects outside the range will not be shown.

   .. note::

      A large clipping range will allow you to see both near and far objects,
      but reduces the depth precision resulting in artifacts.

      See :ref:`Troubleshooting Depth Buffer Glitches <troubleshooting-depth>` for more information.

Local Camera
   Active camera used in this view to override the (global) scene camera.
   The option is available only when *lock local camera and layers* toggle in the header is not enabled.
Render Border
   Use a Render Border when not looking through a camera.
   Using :kbd:`Ctrl-B` to draw a border region will automatically enable this option.
