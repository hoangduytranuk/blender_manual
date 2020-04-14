
***********
In-Betweens
***********

.. figure:: /images/animation_armatures_posing_editing_inbetweens-tools.png
   :align: right

   In-Betweens Tools.

There are several tools for editing poses in an animation.

There are also in *Pose Mode* a bunch of armature-specific editing options/tools,
like :ref:`auto-bones naming <armature-editing-naming-bones>`,
:ref:`properties switching/enabling/disabling <armature-bone-properties>`, etc.,
that were already described in the armature editing pages. See the links above...


Push Pose from Breakdown
========================

.. admonition:: Reference
   :class: refbox

   :Mode:      Pose Mode
   :Tool:      :menuselection:`Toolbar --> In-Betweens Tools --> Push`
   :Menu:      :menuselection:`Pose --> In-Betweens --> Push Pose from Breakdown`
   :Hotkey:    :kbd:`Ctrl-E`

*Push Pose* interpolates the current pose by making it closer to the next keyframed position.


Push Pose from Rest
===================

.. admonition:: Reference
   :class: refbox

   :Mode:      Pose Mode
   :Menu:      :menuselection:`Pose --> In-Betweens --> Push Pose from Rest`

Similar to *Push Pose from Breakdown* but interpolates the pose to the rest position instead.
Only one keyframe is needed for this tool unlike two for the other.


Relax Pose to Breakdown
=======================

.. admonition:: Reference
   :class: refbox

   :Mode:      Pose Mode
   :Tool:      :menuselection:`Toolbar --> In-Betweens Tools --> Relax`
   :Menu:      :menuselection:`Pose --> In-Betweens --> Relax Pose to Breakdown`
   :Hotkey:    :kbd:`Alt-E`

Relax pose is somewhat related to the above topic, but it is only useful with keyframed bones.
When you edit such a bone (and hence take it "away" from its "keyed position"),
using this tool will progressively "bring it back" to its "keyed position",
with smaller and smaller steps as it comes near it.


Relax Pose to Rest
==================

.. admonition:: Reference
   :class: refbox

   :Mode:      Pose Mode
   :Menu:      :menuselection:`Pose --> In-Betweens --> Relax Pose to Rest`

Similar to *Relax Pose to Breakdown* but works to bring the pose back to the rest position instead.
Only one keyframe is needed for this tool unlike two for the other.


Breakdowner
===========

.. admonition:: Reference
   :class: refbox

   :Mode:      Pose Mode
   :Tool:      :menuselection:`Toolbar region --> In-Betweens Tools --> Breakdowner`
   :Menu:      :menuselection:`Pose --> In-Betweens --> Pose Breakdowner`
   :Hotkey:    :kbd:`LMB`-drag

Creates a suitable breakdown pose on the current frame.

The Breakdowner tool can be constrained to work on specific transforms and axes,
by pressing the following keys while the tool is active:

- :kbd:`G`, :kbd:`R`, :kbd:`S`: move, rotate, scale
- :kbd:`B`: Bendy bones
- :kbd:`C`: custom properties
- :kbd:`X`, :kbd:`Y`, :kbd:`Z`: to the corresponding axes
