.. _bpy.types.SpaceView3D.cursor_location:

*********
3D Cursor
*********

The 3D Cursor is simply a point in 3D space which can be used for a number of purposes.


Placement
=========

There are a few methods to position the 3D cursor.


Direct Placement with the Mouse
-------------------------------

.. figure:: /images/editors_3dview_3d-cursor_two-view-positioning.png
   :align: center

   Positioning the 3D cursor with two orthogonal views.

Using :kbd:`LMB` in the 3D View will place the 3D cursor directly under your mouse pointer.

For accuracy you should use two perpendicular orthogonal 3D Views, i.e.
any combination of top :kbd:`Numpad7`, front :kbd:`Numpad1` and side :kbd:`Numpad3`.
That way you can control the positioning along two axes in one view and determine depth in the second view.

By default the depth of the geometry under the cursor is used,
this can be disabled using the *Cursor Depth* toggle in the :doc:`Preferences </editors/preferences/interface>`.

.. seealso::

   The :doc:`Snap Menu </scene_layout/object/editing/transform/control/snap>`
   which allows the cursor placement relative to scene objects.


3D Cursor Panel
---------------

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Panel:     :menuselection:`Sidebar region --> 3D Cursor`

.. figure:: /images/editors_3dview_3d-cursor_panel.png

   The 3D Cursor panel of the Sidebar region.

The 3D cursor can also be positioned by editing the location coordinates values in
the *3D cursor* panel of the Sidebar region.


Usage
=====

The 3D Cursor is used as the origin for any added object, can be used and moved with
the :doc:`snap tool </scene_layout/object/editing/transform/control/snap>`, and is an option for
the :doc:`pivot point </scene_layout/object/editing/transform/control/pivot_point/index>`.
