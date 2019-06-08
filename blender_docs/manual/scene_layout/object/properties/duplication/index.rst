.. _bpy.types.Object.dupli_type:

###############
  Duplication
###############

There are currently four ways in Blender to procedurally duplicate objects.
These options are located in the :menuselection:`Object --> Duplication` panel.

Vertices
   This creates an instance of all children of this object on each vertex (for mesh objects only).
Faces
   This creates an instance of all children of this object on each face (for mesh objects only).
Group
   This creates an instance of the group with the transformation of the object.
   Group duplicators can be animated using actions,
   or can get a :ref:`Proxy <object-proxy>`.

.. toctree::
   :maxdepth: 2

   dupliverts.rst
   duplifaces.rst
   dupligroup.rst
