.. _bpy.types.NlaStrip:

******
Strips
******

Types
=====

There are four kinds of strips: Action, Transition, Sound clip and Meta.


Action Strips
-------------

An Action Strip is a container of keyframe data of an action.
Any action used by the NLA first must be turned into an Action strip.
This is done so by clicking the Push Down action button see above.
Alternatively, you can go to :menuselection:`Add --> Action Strip`.


Transition Strips
-----------------

Transitions interpolate between Actions. They must be placed in between other strips.
Select two or more strips on the same track,
and go to :menuselection:`Add --> Transition`.

.. figure:: /images/editors_nla_strips_basics-transition.png

   Transition Strip.


Sound Clip Strips
-----------------

Controls when a speaker plays a sound clip.
:menuselection:`Add --> Sound Clip`.


Meta Strips
-----------

Meta strips group strips together as a whole, so you can move them as one.
If you find yourself moving a lot of strips together, you can group them into a Meta strip.
A Meta strip can be moved and duplicated like a normal strip.

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Add --> Add Meta-Strips`
   :Hotkey:    :kbd:`Shift-G`

.. list-table::

   * - .. figure:: /images/editors_nla_strips_meta1.png
          :width: 320px

          Shift-select two or more strips.

     - .. figure:: /images/editors_nla_strips_meta2.png
          :width: 320px

          Combine them into a meta strip.

A Meta strip still contains the underlying strips. You can ungroup a Meta strip.

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Add --> Remove Meta-Strips`
   :Hotkey:    :kbd:`Alt-G`


Editing
=======

Start Tweaking Strips Action
----------------------------

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Edit --> Start Tweaking Strips Action`
   :Hotkey:    :kbd:`Tab`

The contents of Action strips can be edited, but you must be in *Tweak Mode* to do so.
The keyframes of the action can then be edited in the Dope Sheet.

.. list-table::

   * - .. figure:: /images/editors_nla_strips_nla-mode.png
          :width: 320px

          Strip in NLA mode.

     - .. figure:: /images/editors_nla_strips_edit-mode.png
          :width: 320px

          Strip in Tweak mode.

When you finished editing the strip, simply go to :menuselection:`Edit --> Tweaking Strips Action`
or press :kbd:`Tab`.


Start Editing Stashed Action
----------------------------

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Edit --> Start Editing Stashed Action`
   :Hotkey:    :kbd:`Shift-Tab`

It will enter and exit Tweak Mode as usual, but will also make sure that the action can be edited in isolation
(by flagging the NLA track that the action strip comes from as being "solo").
This is useful for editing stashed actions, without the rest of the NLA Stack interfering.


Duplicate
---------

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Edit --> Duplicate`
   :Hotkey:    :kbd:`Shift-D`

Creates a new instance of the selected strips with a copy of the action.


Linked Duplicate
----------------

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Edit --> Linked Duplicate`
   :Hotkey:    :kbd:`Alt-D`

The contents of one Action strip can be instanced multiple times. To instance another strip,
select a strip, go to :menuselection:`Edit --> Linked Duplicate`.
It will uses the same action as the selected strips.

Now, when any strip is tweaked, the others will change too.
If a strip other than the original is tweaked,
the original will turn to red.

.. figure:: /images/editors_nla_strips_linked-strip-edit.png

   Linked duplicated strip being edited.


Make Single User
----------------

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Edit --> Make Single User`
   :Hotkey:    :kbd:`U`

This tool ensures that none of the selected strips use an action which is also used by any other strips.

.. (dev) NOTE: This does not recursively go inside meta's, so care is still advised in that case.
