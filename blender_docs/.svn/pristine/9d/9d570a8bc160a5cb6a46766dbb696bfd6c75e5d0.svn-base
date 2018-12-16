
**********************
Properties & Modifiers
**********************

Properties
==========

Strip properties can be accessed via the NLA Properties region.


Animation Data
--------------

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties region --> Animations --> Animation Data`

.. figure:: /images/editors_nla_properties-modifiers_animation-data-panel.png

   Animation Data panel.

Action
   A :ref:`Data-Block <ui-data-block>` menu that allows you to edit actions shown in the action track.
   See also the Action Editor's :ref:`Action <dopesheet-action-action>`.
Action Extrapolation
   Action to take for gaps past the strip extents.

   Hold
      Affects both sides of the strip.
   Hold Forward
      Affects the region after the clip, only.
   Nothing
      Neither.

Action Blending
   Affects the behavior when two tracks simultaneously have a curve affecting the same property.

   Replace
      Causes the top strip to take precedence according to the parameters
      of the Blend In/Out (see next option, below).
   Multiply, Subtract, Add
      The weighted result of the strip is multiplied, subtracted, or added with the accumulated results.

Action Influence
   Amount the active Action contributes to the result of the NLA stack.


Active Track
------------

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties region --> Animations --> Active Track`

Name
   Name of the track which the strip currently belongs to.


Active Strip
------------

.. figure:: /images/editors_nla_properties-modifiers_active-strip-panel.png

   Active Strip panel.

Options of the strip itself.

Name
   Renames the strips.
Type
   Will either say "Action Clip", "Transition", or "Meta", according to the three types of strips.
Strip Extents
   The boundaries of the strip itself. Note that this will stretch the duration of the Action,
   it will not cause greater or fewer keyframes from the Actions to play (see below for that option).
Extrapolation
   See *Action Extrapolation* above.
Blending
   See *Action Blending* above.
Auto Blend In/Out
   Creates a ramp starting at the overlap of the strips. The first strip has full control,
   and it ramps linearly giving the second strip full control by the end of the overlapping time period.
Blend In
   Set the frame that represents when this strip will have full influence.
Blend Out
   Set the last frame of this strip's full influence.
Muted
   Mute a single strip (like muting the track, above). Causes the track outline to be dashed.
Reversed
   Cause this strip to be played completely backwards.


Action Clip
-----------

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties region --> Animations --> Active Clip`

.. figure:: /images/editors_nla_properties-modifiers_action-clip-panel.png

   Action Clip panel.

This represents the 'object data' of the strip. Much like the transform values of an object.

Action
   A reference to the Action contained within the strip.
   Can be changed to replace the current strip's value with another Action.
Action Extents
   How much of the Action to use.

   Note: If you select values that are above or below the actual keyframe count of the Action,
   then the F-Curve Extrapolation will be consulted.
   Which can be changed in the Graph Editor, under :menuselection:`Channel --> Extrapolation Mode`.
Sync Length
   Causes the "Start" and "End" Frames, above, to be reset to the first and last keyframed frames of the Action.
Sync Action Length "Now"
   Causes the "Start" and "End" Frames, above, to be reset to the first and last keyframed frames of the Action.
Playback Settings
   Scale
      Stretches strip, another way of increasing the *Strip Extents: End Frame*, above.
   Repeat
      Also expands the strip, but by looping from the first keyframe and going forward.


Evaluation
----------

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties region --> Animations --> Evaluation`

.. figure:: /images/editors_nla_properties-modifiers_evaluation-panel.png

   Evaluation panel.

This determines the degree of influence the strip has, and over what time.

Animated Influence
   Enabling alteration of the degree of influence this strip has as a keyframable value.
   If influence isn't animated, the strips will fade linearly, during the overlap.

   These can be found in the Dope Sheet or Graph Editors under the *NLA Control Curves* and
   look like group channels. They appear before all the groups/F-curves for that channel.
Animated Strip
   Same as *Animated Influence*, but with *Strip Time*.
Cyclic Strip Time
   Cycle the animated time within the action start and end.


Modifiers
=========

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties region --> Modifiers --> Modifiers`

Like its counterparts in graph and video editing,
Modifiers can stack different combinations of effects for strips.

See :doc:`F-Curve Modifiers </editors/graph_editor/fcurves/modifiers>`.
