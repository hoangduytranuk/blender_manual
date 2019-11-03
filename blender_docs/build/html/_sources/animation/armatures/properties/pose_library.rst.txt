.. _bpy.ops.poselib:

******************
Pose Library Panel
******************

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Panel:     :menuselection:`Properties editor --> Object --> Pose Library`

.. TODO2.8
   .. figure:: /images/animation_armatures_properties_pose-library_panel.png
      :align: right

      The Pose Library panel.

The *Pose Library* panel is used to save, apply, and manage armature poses.
*Pose Libraries* are saved to :doc:`Actions </animation/actions>`.
They are not generally used as actions, but can be converted to and from.

Action
   A :ref:`ui-data-block` for Actions or Pose Libraries.
Pose Libraries
   A :ref:`List view <ui-list-view>` of poses for the active Pose Library.

   Add ``+``
      If a pose is added, a :ref:`pose marker <marker-pose-add>` is created.
      Keys are only stored for selected bones. If no bones are selected, all bones are keyed.

      Add New
         Adds a new pose to the active Pose Library with the current pose of the armature.
      Add New (Current Frame).
         Will add a pose to the Pose Library based on the current frame selected in the Timeline.
         In contrast to *Add New* and *Replace Existing* which automatically allocate a pose to an action frame.
      Replace Existing
         Replace an existing pose in the active Pose Library with the current pose of the armature.
   Apply Pose (magnifying glass icon)
      Applies the active pose to the selected pose bones.
   Sanitize Action (book icon)
      Makes an action suitable for use as a Pose Library.
      This is used to convert an Action to a Pose Library.
      A pose is added to the Pose Library for each frame with keyframes.
   Move (up/down arrow icon)
      Moves the pose up/down in the list.


.. TODO Move to pose editing.

Menu
====

.. admonition:: Reference
   :class: refbox

   :Mode:      Pose Mode
   :Menu:      :menuselection:`Pose --> Pose Library`

- Browse Poses. :kbd:`Ctrl-L`.
- Add Pose. :kbd:`Shift-L`.
- Rename Pose. :kbd:`Shift-Ctrl-L`.
- Remove Pose. :kbd:`Alt-L`.
