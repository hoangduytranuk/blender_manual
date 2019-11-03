
***************
Add Camera Rigs
***************

Introduction
============

This script was designed to add some extended functionality to a camera by creating control rig
with custom shapes and UI to easily access the cameras settings from the 3D View.


Activation
==========

- Open Blender and go to Preferences then the Add-ons tab.
- Click Camera then Add Camera Rigs to enable the script.


Description
===========

After activating the add-on, it will place two menu items in the :menuselection:`Add --> Camera` menu.
They are Dolly Rig and Crane Rig.

Both rigs are very similar except the "Crane Rig" has two extra adjustable bones (Arm Height and Arm Length)
to make it easier to achieve a cinematic crane shot.


Usage
=====

Add a :menuselection:`Add --> Armature --> Dolly Rig or Crane Rig`.
This will build the rig at the cursor location, add a new camera, making it the new active scene camera.

The camera object will not be selectable by default
but this can be toggled from the UI in the 3D View Sidebar.

When the Rig is selected, the camera properties will be displayed in the Sidebar.


Rigs
====

Root bone
   This is the parent of the entire rig.
Control bone
   This is the bone (named ``CTRL``) that will translate the camera around. By default it will track to the aim bone.
Aim bone
   The camera will point at this bone (named ``AIM``).
   You can also tilt the camera by rotating the aim on the Y axis.


UI
==

The UI will display most of the useful camera settings.
I will only explain the added features here, for more information check out the :doc:`/render/cameras`.

Add DOF Empty
   The *Add DOF Empty* button will automatically add an Empty at the location of the aim bone and
   make it the depth of field (DOF) object.

   The empty is a child of the aim bone but will give the user the ability to animate this object.
X-Ray
   Will make the rig object visible through all other geometry.
   (Useful if you have a fly through scene or if other meshes are in the way.)

Lock Camera Select
   The *Lock Camera Select* is a toggle button to make the camera unselectable
   (so you can't accidentally delete it).
Tracking (Aim Lock)
   This slider controls the Track To constraint on the control bone.
   Turn it off and the bone will not point to the aim bone anymore.

Crane Rig Height, Arm Length
   The *Arm Height* and *Arm Length* sliders at the bottom of the UI show the Y axis scale of the relevant bone.
   By default, both the height and the arm length are at 1 unit in size.
   These values can be set to the users preferences and also animated if need be.


Multiple Cameras
================

It is possible to add as many rigs as your scene needs.
The *Make Camera Active* will appear if the camera attached to the selected rig is **not** the active camera.
By pressing this, it will make this camera the active one.
If you wish to switch active cameras during an animation, check out the `Camera Switching`_ section below.


Camera Switching
================

If you wish to switch cameras during an animation you can do this with the *Add Marker and Bind* button.
This uses Blender's built-in camera binding tool to a Timeline marker.
When pressed, it will add a marker to the Timeline and bind it to the camera controlled by the selected rig.
Go to another frame, select a different Camera Rig and press it again.
Now you have two markers and when you scrub the time line you will see the active camera switch accordingly.
(repeat this process as many times as needed)
This markers can then also be dragged around in the time to change the frame in which they will switch.


Troubleshooting
===============

If the Aim tracking is not functioning check that you have "Auto Run Python Scripts" enabled in the Preferences
:menuselection:`Preferences --> Save & Load --> Auto Run Python Scripts`.

If the UI stops working, perhaps you have parented an object to the rig?
At the moment If you parent an object to the rig with a name
that precedes the camera name alphabetically, the UI can't load.
E.g. The Default camera name for the Dolly is "Dolly Camera". If you parent an object called "E" it will work.
But an object called "A" will fail.


.. admonition:: Reference
   :class: refbox

   :Category:  Camera
   :Description: Adds a camera rig with a UI.
   :Location: :menuselection:`3D View --> Add --> Camera`
   :File: camera_dolly_crane_rigs.py
   :Author: Wayne Dixon, Kris Wittig
   :License: GPL
   :Note: This add-on is bundled with Blender.
