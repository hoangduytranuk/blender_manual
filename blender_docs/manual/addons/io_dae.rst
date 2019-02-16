
*******
Collada
*******

:Name: Collada format
:Location: :menuselection:`File --> Import/Export --> Collada (.dae)`
:Version: OpenCollada 1.6.68
:Blender: 2.80
:Category: Import-Export
:Authors: Gaia Clary


Usage
=====

This format is mainly use for interchanging character animations between applications
and is supported by applications such as Cinema4D, Maya, Autodesk 3ds Max, Wings3D and
engines such as Unity3D, Unreal Engine 3/UDK and Unreal Engine 4.

The exporter can bake mesh modifiers and animation into the Collada export
so the final result looks the same as in Blender.

.. note::

   This module is still in development.


Properties
==========

Import
------

Main
^^^^

Import Units
   Use unit information from the Asset node in the Collada file. Use Blender units if not enabled.


Armatures
^^^^^^^^^

Fix Leaf Bones
   Try to find a reasonable location for the bone tails of leaf nodes.
Find Bone Chains
   Find best matching bone chains and make sure that children are connected to their parent.
Auto Connect
   Connect bones to their parent if they are the only child of their parent.
Minimum Chain Length
   Minimum number of bones in a parent/child hierarchy needed to identify it as a chain.
   Used for auto connect and to find bone chains.
Keep Bind Info
   Add two custom properties to each bone containing:

   - rest_mat: An array of 16 values representing the rest-pose matrix at time of import.
   - bind_mat: An array of 16 values representing the bind-pose matrix at time of import.

   Note that, the ``bind_mat`` is identical to the ``rest_mat`` if the armature is imported with its rest pose.


Export
------

Main
^^^^

Selection Only
   Only export the selected objects. Otherwise export all objects in the scene.
Include Children
   Include children of selected objects even if not selected.
Include Armatures
   Include armatures for rigged objects even if the armature is not selected.
Include Shape Keys
   Export shape key data (caution, this creates very large output files if many shape keys are defined).
Only Selected UV Map
   Export the active UV map when enabled, otherwise export all UV maps.
Copy
   Copy textures to same folder where the dae-file is exported to, otherwise create links to the image files.


Geometry
^^^^^^^^

Apply Modifiers
   When enabled, the mesh will be from the output of the modifiers applied to the mesh.
Triangulate
   Triangulate meshes before exporting (use this option when the target engine supports only tris).


Armature
^^^^^^^^

Deform Bones Only
   Restrict armature to its deform bones.
Export to SL/OpenSim
   Prepare the rig for the :abbr:`SL (Second Life)` target engine (to be specified).


Animation
^^^^^^^^^

Include Animations
   Export Animation data.
Export Format
   - Samples: Create sample frames with the specified *Sample Rate* (see below).
   - Curves: Keep animation curves intact (experimental, does not work with *Shear*).

Transformation Type
   - Matrix: Export transformations as baked matrices.
   - TransRotLoc: Export transformations as separate curves for translation, rotation and scale.

Keep Smooth Curves
   Also export curve handles (only works when the animated object parent-inverse matrix is unity).
Sampling Rate
   Distance between two sample keyframes (1 means every frame is keyed).
Keep Keyframes
   Make sure that the keyframes are always exported even if they are between two sample frames.
All Keyed Curves
   Also export flat curves (with all key values identical or only one key defined).
Include All Actions
   Export all actions compatible with the selected armatures
   start/end times which are derived from the keyframe range of each action.
   When disabled only the currently assigned action is exported.


Extra
^^^^^

Use Object Instances
   Define an object only once and use it as a reference (not supported on all target engines).
Use Blender Profile
   Export extra information to allow a more precise import back into Blender.
Sort by Object Name
   Make sure the exported objects are exported in sort order of their names.
Keep Bind Info
   Each bone can have two custom properties:

   - rest_mat: An array of 16 values representing the rest-pose matrix at time of import.
   - bind_mat: An array of 16 values representing the bind-pose matrix at time of import.

   If the ``bind_mat`` is defined then use that matrix as bind matrix of the bone.
   If the ``rest_mat`` is defined then use that matrix as the rest matrix of the bone.
   This corresponds with the same custom properties from the Collada Importer.
   ``Bind_mat`` and ``rest_mat`` are needed when handling rigs that where originally made
   with a bind pose (which Blender does not support).
Limit Precision
   Take care to use at max five digits after the comma. This is good for debugging when you want to compare values.


Compatibility
=============

Import
------

TODO


Export
------

TODO


Missing
-------

TODO
