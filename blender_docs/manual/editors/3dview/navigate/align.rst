
********
Aligning
********

These options allow you to align and orient the view.


Axes
====

Blender uses a right-angled "Cartesian" coordinate system with the Z axis pointing upwards.

:X axis: Left / Right
:Y axis: Front / Back
:Z axis: Top / Bottom

You can select the viewing direction for a 3D View with the *View* menu entries,
or by pressing the hotkeys.

These operators change the view to be aligned with the specified global axes:

:Top: :kbd:`Numpad7`
:Front: :kbd:`Numpad1`
:Right: :kbd:`Numpad3`

Holding :kbd:`Ctrl` shows the other side of the same axis.

:Bottom: :kbd:`Ctrl-Numpad7`
:Back: :kbd:`Ctrl-Numpad1`
:Left: :kbd:`Ctrl-Numpad3`

Holding :kbd:`Shift` aligns the view relative to the active selection.
So you can for example, view a rotated objects side, or align the view to the active face in mesh Edit Mode.


Align View Menu
===============

Align View to Active
   The options in this menu align your view with specified local axes of the selected active object,
   bone, or, in *Edit Mode* with the normal of the selected face.

   Hold down :kbd:`Shift` while using the numpad to set the view axis.
Align Active Camera to View :kbd:`Ctrl-Alt-Numpad0`
   Gives your active camera the current viewpoint.
Align Active Camera to Selected
   Points the active camera toward the selected object; based on the direction of the current viewpoint.

Center Cursor and View All :kbd:`Shift-C`
   Moves the cursor back to the origin and zooms in/out so that you can see everything in your scene.
Center View to Cursor
   Centers view to 3D cursor.
View Lock to Active
   Centers view to the last selected active object, overriding other view alignment settings.
View Lock Clear
   Returns the view alignment to the view align settings before use of *View Lock to Active*.
