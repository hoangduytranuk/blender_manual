
.. |prop-edit-icon| image::
   /images/editors_3dview_object_editing_transform_control_proportional-edit_header.png


*****************
Proportional Edit
*****************

Proportional Edit is a way of transforming selected elements (such as vertices)
while having that transformation affect other nearby elements. For example,
having the movement of a single vertex cause the movement of unselected vertices within a given range.
Unselected vertices that are closer to the selected vertex will move more than those farther from it
(i.e. they will move proportionally relative to the location of the selected element).
Since Proportional Editing affects the nearby geometry,
it is very useful when you need to smoothly deform the surface of a dense mesh.

.. note:: Sculpting

   Blender also has :ref:`painting-sculpting-index`
   that contains brushes and tools for proportionally editing a mesh without seeing the individual vertices.


Object Mode
===========

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      Via the |prop-edit-icon| icon in the header.
   :Hotkey:    :kbd:`O`

Proportional Editing is typically used in *Edit Mode*, however, it can also be used in *Object Mode*.
In *Object Mode* the tool works on entire objects rather than individual mesh components.

In the image below, the right cylinder is scaled along the Z axis.
When the *Proportional Editing* is enabled, the adjacent cylinders are also within the tool's radius of influence.

.. figure:: /images/scene-layout_object_editing_transform_control_proportional-edit_object-mode.png

   Proportional Editing in Object Mode.


.. (Todo move) to modeling section

Edit Mode
=========

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Mesh --> Proportional Editing` and via the |prop-edit-icon| highlighted icon
   :Hotkey:    :kbd:`O`, :kbd:`Alt-O`, :kbd:`Shift-O`

When working with dense geometry, it can become difficult to make subtle adjustments to
the vertices without causing visible lumps and creases in the model's surface.
When you face situations like this the Proportional Editing tool
can be used to smoothly deform the surface of the model.
This is done by the tool's automatic modification of unselected vertices within a given range.

.. figure:: /images/scene-layout_object_editing_transform_control_proportional-edit_edit-mode.png

   Proportional Editing in Edit Mode.


Influence
---------

You can increase or decrease the radius of the tool's influence with
the mouse wheel :kbd:`WheelUp`, :kbd:`WheelDown` or
:kbd:`PageUp`, :kbd:`PageDown` respectively. As you change the radius,
the points surrounding your selection will adjust their positions accordingly.

.. figure:: /images/scene-layout_object_editing_transform_control_proportional-edit_influence.png

   Influence circle.


Options
-------

.. list-table::

   * - .. figure:: /images/scene-layout_object_editing_transform_control_proportional-edit_tool.png
          :width: 250px

          Proportional Editing tool.


The *Proportional Editing* mode menu is on the 3D View header.

Disable :kbd:`O`, :kbd:`Alt-O`
   Proportional Editing is Off, only selected vertices will be affected.
Enable :kbd:`O`, :kbd:`Alt-O`
   Vertices other than the selected vertex are affected, within a defined radius.
Projected from View
   Depth along the view is ignored when applying the radius.

   .. figure:: /images/scene-layout_object_editing_transform_control_proportional-edit_2d-compare.png
      :width: 560px

      The difference between regular and Projected (2D) proportional option (right).

Connected Only
   Rather than using a radius only, the proportional falloff spreads via connected geometry.
   This means that you can proportionally edit the vertices in a finger of a hand
   without affecting the other fingers. While the other vertices are physically close (in 3D space),
   they are far away following the topological edge connections of the mesh.
   The icon will have a gray center when *Connected* is active.
   This mode is only available in *Edit Mode*.

.. _3dview-transform-control-proportional-edit-falloff:

Falloff
   While editing, you can change the curve profile used by either
   using the header icon *Falloff* menu, or by pressing :kbd:`Shift-O` to toggle between the various options.

.. list-table::

   * - .. figure:: /images/scene-layout_object_editing_transform_control_proportional-edit_falloff-constant.png
          :width: 320px

          Constant, No Falloff.

     - .. figure:: /images/scene-layout_object_editing_transform_control_proportional-edit_falloff-random.png
          :width: 320px

          Random Falloff.

   * - .. figure:: /images/scene-layout_object_editing_transform_control_proportional-edit_falloff-linear.png
          :width: 320px

          Linear Falloff.

     - .. figure:: /images/scene-layout_object_editing_transform_control_proportional-edit_falloff-sharp.png
          :width: 320px

          Sharp Falloff.

   * - .. figure:: /images/scene-layout_object_editing_transform_control_proportional-edit_falloff-root.png
          :width: 320px

          Root Falloff.

     - .. figure:: /images/scene-layout_object_editing_transform_control_proportional-edit_falloff-sphere.png
          :width: 320px

          Sphere Falloff.

   * - .. figure:: /images/scene-layout_object_editing_transform_control_proportional-edit_falloff-smooth.png
          :width: 320px

          Smooth Falloff.

     - .. figure:: /images/scene-layout_object_editing_transform_control_proportional-edit_falloff-inverse-square.png
          :width: 320px

          Inverse Square Falloff.


Examples
--------

The image below shows the final render of the low-poly landscape
obtained by moving up the vertices of the triangulated grid
with enabled *Proportional Editing*.

.. figure:: /images/scene-layout_object_editing_transform_control_proportional-edit_landscape.jpg
   :width: 620px

   A landscape obtained via Proportional Editing.
