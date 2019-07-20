.. _bpy.ops.anim.keying_set:

***********
Keying Sets
***********

.. figure:: /images/editors_timeline_keying-sets.png
   :align: right

   The Active Keying Sets data ID in the Timeline.

.. (alt) Keying Sets are a set of keyframe channels.

Keying Sets are a collection of properties.
They are used to record multiple properties at the same time.

Now when you press :kbd:`I` in the 3D View,
Blender will add keyframes for all the properties in the active keying set.

There are some built-in Keying Sets and,
also custom Keying Sets called *Absolute Keying Sets*.

To select and use a Keying Set, set the *Active Keying Set*
in the :ref:`Keying popover <timeline-keying>` in the Timeline Header,
or the Keying Set panel, or press :kbd:`Shift-Ctrl-Alt-I` in the 3D View.


Keying Set Panel
================

.. admonition:: Reference
   :class: refbox

   :Editor:    Properties editor
   :Panel:     :menuselection:`Scene --> Keying Set`

This panel is used to add, select, manage *Absolute Keying Sets*.

.. figure:: /images/animation_keyframes_keying-sets_scene-keying-set-panel.png

   The Keying Set panel.

Active Keying Set
   The :ref:`List View <ui-list-view>` of Keying Sets in the active Scene.

   Add ``+``
      Adds an empty Keying Set.


Properties
----------

Description
   A short description of the keying set.
Export to File
   Export Keying Set to a Python script ``File.py``.
   To re-add the keying set from the ``File.py``, open then run the ``File.py`` from the Text Editor.

Keyframing Settings (General Override)
   These options control all properties in the Keying Set.
   Note that the same settings in *Preferences* override these settings if enabled.

   Only Needed
      Only insert keyframes where they are needed in the relevant F-curves.
   Visual Keying
      Insert keyframes based on the visual transformation.
   XYZ to RGB
      For new F-curves, set the colors to RGB for the property set, Location XYZ for example.


Active Keying Set Panel
=======================

.. admonition:: Reference
   :class: refbox

   :Editor:    Properties editor
   :Panel:     :menuselection:`Scene --> Active Keying Set`

This panel is used to add properties to the active Keying Set.

.. figure:: /images/animation_keyframes_keying-sets_scene-active-keying-set-panel.png

   The Active Keying Set panel.

Active Keying Set Paths
   A collection of paths in a :ref:`List View <ui-list-view>` each with a *Data Path* to a property
   to add to the active Keying Set.

   Add ``+``
      Adds an empty path.


Properties
----------

Target
   ID-Block
      Set the ID Type and the *Object IDs* Data Path for the property.
   Data Path
      Set the rest of the Data Path for the property.
   Array All Items
      Use *All Items* from the Data Path or select the array index for a specific property.

F-Curve Grouping
   This controls what group to add the channels to.

   Keying Set Name, None, Named Group

Keyframing Settings (Active Set Override)
   These options control individual properties in the Keying Set.

   Only Needed
      Only insert keyframes where they are needed in the relevant F-curves.
   Visual Keying
      Insert keyframes based on the visual transformation.
   XYZ to RGB
      For new F-curves, set the colors to RGB for the property set, Location XYZ for example.


Adding Properties
=================

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Context menu --> Add All/Single to Keying Set`
   :Hotkey:    :kbd:`K`

Some ways to add properties to keying sets.

:kbd:`RMB` the property in the *User Interface*, then select *Add Single to Keying Set* or *Add All to Keying Set*.
This will add the properties to the active keying set, or to a new keying set if none exist.

Hover the mouse over the properties, then press :kbd:`K`, to add *Add All to Keying Set*.
