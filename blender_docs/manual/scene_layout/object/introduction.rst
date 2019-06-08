
************
Introduction
************

The geometry of a scene is constructed from one or more Objects. These objects
can range from lamps to light your scene, basic 2D and 3D shapes to fill it with models, armatures
to animate those models, to cameras to take pictures or video of it all.


Instancing
==========

Each Blender object type (mesh, lamp, curve, camera, etc.) is composed from two parts:
an *Object* and *Object Data* (sometimes abbreviated to *ObData*):

Object
   Holds information about the position, rotation and size of a particular element.
Object Data
   Holds everything else. For example:

   :Meshes: Store geometry, material list, vertex groups, etc.
   :Cameras: Store focal length, depth of field, sensor size, etc.

   Each object has a link to its associated :ref:`object-data <properties-data-tabs>`,
   and a single object-data may be shared by many objects.
