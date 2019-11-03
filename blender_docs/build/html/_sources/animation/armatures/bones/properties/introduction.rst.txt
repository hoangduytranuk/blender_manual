
************
Introduction
************

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode, Edit Mode and Pose Mode
   :Panel:     :menuselection:`Properties editor --> Bone`

When bones are selected (hence in *Edit Mode* and *Pose Mode*), their
properties are shown in the *Bone* tab of the Properties editor.
This shows different panels used to control features of each selected bone;
the panels change depending on which mode you are working in.

.. TODO2.8
   .. figure:: /images/animation_armatures_bones_properties_introduction_properties-editor.png

      The Bone tab.


.. todo Move pose related to new pose > properties folder,
   check other: pose library; edit text above accordingly.

Transform
=========

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode and Pose Mode
   :Panel:     :menuselection:`Bone --> Transform`

.. TODO2.8
   .. list-table::

      * - .. figure:: /images/animation_armatures_bones_properties_introduction_transform-panel-edit.png

             The Transform panel (Edit Mode).

        - .. figure:: /images/animation_armatures_bones_properties_introduction_transform-panel-pose.png

             The Transform panel (Pose Mode).

When in *Edit Mode* you can use this panel to control position and roll of individual bones.
Whereas in *Pose Mode* you can only set location for the main bone, and you can now set rotation and scale.

In addition, in *Pose Mode* it is possible to restrict changes in position,
rotation and scale by axis on each bone in the armature.


Inverse Kinematics
==================

.. admonition:: Reference
   :class: refbox

   :Mode:      Pose Mode
   :Panel:     :menuselection:`Bone --> Inverse Kinematics`

.. TODO2.8
   .. figure:: /images/animation_armatures_bones_properties_introduction_inverse-kinematics-panel.png

      The Inverse Kinematics panel.

This panel controls the way a bone or set of bones behave when linked in
an :doc:`inverse kinematic </animation/armatures/posing/bone_constraints/inverse_kinematics/introduction>` chain.


Custom Properties
=================

.. admonition:: Reference
   :class: refbox

   :Mode:      Pose Mode
   :Panel:     :menuselection:`Bone --> Custom Properties`

See the :ref:`Custom Properties <files-data_blocks-custom-properties>` page for more information.
