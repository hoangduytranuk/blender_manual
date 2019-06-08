
***************
Troubleshooting
***************

Some common problems people may run into when using drivers.


Scripted Expression
===================

.. figure:: /images/animation_drivers_troubleshooting_autorun-graph-editor.png

   An Auto-execution warning in the Drivers panel.

.. figure:: /images/animation_drivers_troubleshooting_autorun-info-header.png

   An Auto-run warning in the Info editor's header.

By default Blender will not autorun Python scripts.

If using a *Scripted Expression* Driver Type, you will have to open the file as *Trusted Source*,
or set *Auto Run Python Scripts* in :menuselection:`Preferences --> File --> Auto Execution`.

.. list-table::
   :widths: 40 60

   * - .. figure:: /images/animation_drivers_troubleshooting_autorun-file-browser.png

          The Trusted Source checkbox in the File Browser.

     - .. figure:: /images/animation_drivers_troubleshooting_autorun-user-preference.png

          The Auto Run Python Scripts checkbox in the Preferences.


Rotational Properties are Radians
=================================

Parts of the User Interface may use different units of measurements for angles, rotation.
In the Graph Editor, while working with Drivers, all angles are Radians.


Intra-armature Bone Drivers can Misbehave
=========================================

There is a `well-known limitation <https://developer.blender.org/T40301>`__
with drivers on bones that refer to another bone in the same armature.
Their values can be incorrectly calculated based on the position of the other bone
as it was *before* you adjust the current frame.
This can lead to obvious shape glitches when the rendering of frames has
a jump in the frame number (either because the blend-file is currently
on a different frame number or because you are skipping already rendered frames).
