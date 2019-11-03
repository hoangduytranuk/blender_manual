
*******
Sidebar
*******

Item
====

Shows :doc:`Transform </scene_layout/object/editing/transform/introduction>` settings
of the active objects.


Tool
====

Show settings of the active tool and Workspace.


View
====

View Panel
----------

The *View* panel lets you set other settings regarding the 3D View.
You can show it with the :menuselection:`View --> View Properties...` menu entry.

Focal Length
   Control the focal length of the 3D View camera in millimeters,
   unlike a :doc:`rendering camera </render/cameras>`.

.. _3dview-view-clip:

Clip Start/End
   Adjust the minimum and maximum distances range to limit the visible range to the area
   between two planes that are orthogonal to the viewing direction of the viewport camera.
   Objects outside the range will not be shown.

   .. note::

      The definition of the two planes depends on the kind of view:

      - Perspective view: The planes with distance of start and end from viewport camera.

      - Orthographic view: The planes with distance of negative end and positive end from the focus point,
        in this case the *Start* is ignored.

   .. warning::

      A large clipping range will allow you to see both near and far objects,
      but reduces the depth precision resulting in artifacts.

      See :ref:`Troubleshooting Depth Buffer Glitches <troubleshooting-depth>` for more information.

Use Local Camera
   Use a local camera in this view, rather then the scene's active camera.

Local Camera
   Active camera used in this view to override the (global) scene camera.
   The option is available only when *Use Local Camera* toggle enabled.

Render Region
   Use a Render Region when not looking through a camera.
   Using :kbd:`Ctrl-B` to draw a region will automatically enable this option.


.. _bpy.types.SpaceView3D.lock:

View Lock
^^^^^^^^^

Lock to Object
   Lock to Object lets you define an object in the *Object* Data ID as the center of the view.
   In that case, the view can be rotated around or zoomed towards that central object,
   but not while, unless you move that itself object
   (this option is not available in a camera view).

Lock to 3D Cursor
   Lock the center of the view to the position of the 3D cursor.
   It is only available when *Lock to Object* is not active.

.. _3dview-lock-camera-to-view:

Lock Camera to View
   When in camera view, all changes in the view (pans, rotations, zooms) will affect the active camera,
   which will follow all those changes. The camera frame will be outlined with a red dashed line.


3D Cursor
---------

Location
   The location of the 3D Cursor.

Rotation
   The rotation of the 3D Cursor.

Rotation Mode
   The Rotation mode of the 3D Cursor.


Collections
-----------

This panel shows a list of collections. The visibility of the collection can be changed.


Annotations
-----------

See :doc:`Annotations </interface/annotate_tool>` for more information.
