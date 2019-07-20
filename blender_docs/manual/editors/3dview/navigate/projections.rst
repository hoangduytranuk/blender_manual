
***********
Projections
***********

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Menu:      :menuselection:`View --> Perspective/Orthographic`
   :Hotkey:    :kbd:`Numpad5`

These operators change the projection of the viewport camera.
Each 3D View supports two different types of projection.
These are demonstrated in the Fig. below.

.. list-table::

   * - .. figure:: /images/editors_3dview_navigate_projections_view-orthographic.png
          :width: 320px

          Orthographic projections.

     - .. figure:: /images/editors_3dview_navigate_projections_view-perspective.png
          :width: 320px

          Perspective projections.

Our eye is used to perspective viewing because distant objects appear smaller.
Orthographic projection often seems a bit odd at first,
because objects stay the same size regardless of their distance.
It is like viewing the scene from an infinitely distant point.
Nevertheless, orthographic viewing is very useful
(it is the default in Blender and most other 3D applications),
because it provides a more "technical" insight into the scene,
making it easier to model and judge proportions.


Options
=======

To change the projection for a 3D View, choose the :menuselection:`View --> Orthographic`
or the :menuselection:`View --> Perspective` menu entry.
The :kbd:`Numpad5` shortcut toggles between the two modes.
Changing the projection for a 3D View does not affect the way the scene will be rendered.
Rendering is in perspective by default. If you need to create an orthographic rendering,
select the camera, go to the Camera tab and
press the *Orthographic* button in the *Lens* panel.

.. seealso::

   - :ref:`Render perspectives <camera-lens-type>`
   - :term:`Camera Projections <projection>`
