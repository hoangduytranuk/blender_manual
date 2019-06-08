
*****
Ghost
*****

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Panel:     :menuselection:`Armature --> Ghost`

Ghosts are black outlines (more or less opaque) of the bones as they are positioned at certain frames.
This visualization is only shown in *Pose Mode*.

In traditional cartoon creation, animators use tracing paper,
to see several frames preceding the one they are working on.
This allows them to visualize the overall movement of their character,
without having to play it back.
Blender features something very similar for armatures: the "ghosts".

.. list-table:: Ghosts examples.

   * - .. figure:: /images/rigging_armatures_properties_ghost_example1.png
          :width: 240px

     - .. figure:: /images/rigging_armatures_properties_ghost_example2.png
          :width: 240px


Options
=======

.. figure:: /images/rigging_armatures_properties_ghost_panel.png

   The Ghost panel.

The ghosts settings are found in the *Armature* tab.

Type
   Around Current Frame
      This will display a given number of ghosts before and after the current frame.
      The ghosts are shaded from opaque at the current frame, to transparent at the most distant frames.
   In Range
      This will display the ghosts of the armature's bones inside a given range of frames.
      The ghosts are shaded from transparent for the first frame, to opaque at the last frame. It has four options:
   On Keyframes
      This is very similar to the *In Range* option,
      but there are ghosts only for keyframes in the armature animation
      (i.e. frames at which you keyed one or more of the bones).
      So it has the same options as above, except for the *Step* one (as only keyframes generate ghosts).
      Oddly, the shading of ghosts is reversed compared to *In Range* -- from opaque for the first keyframe,
      to transparent for the last keyframe.

Range
   This number button specifies how many ghosts you will have on both "sides"
   (i.e. a value of 5 will give you ten ghosts, five before the current frame, and five after).
Start, End
   This number button specifies the start/end frame of the range (exclusive).
   Note that unfortunately it cannot take a null or negative value,
   which means you can only see ghosts starting from frame 2 included...
Step
   This number button specifies whether you have a ghost for every frame
   (the default value of 1), or one each two frames, each three frames, etc.


Display
-------

Selected Only
   When enabled, you will only see the ghosts of selected bones
   (otherwise, every bone in the armatures has ghosts...).

Finally, these ghosts are also active when playing the animation :kbd:`Alt-A`
-- this is only useful with the *Around Current Frame* option, of course...

.. note::

   There is no "global switch" to disable this display feature.
   To do so, you have to either set *Ghost* to 0
   (for *Around Current Frame* option),
   or the same frame number in both *Start* and *End*
   (for the two other ghosts types).
