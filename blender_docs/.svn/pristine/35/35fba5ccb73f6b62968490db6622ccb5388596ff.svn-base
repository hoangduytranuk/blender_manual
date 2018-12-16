.. _bpy.types.Object.use_dupli_faces:
.. _bpy.ops.object.make_dupli_face:

**********
DupliFaces
**********

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Panel:     :menuselection:`Object --> Duplication`
   :Menu:      :menuselection:`Object --> Make Dupli-Face`

*Duplication Faces* or *DupliFaces* is the capability to replicate an object on each face of a parent object.
One of the best ways to explain this is through an example illustration.

Scale
   Scales each instances according to the size of its corresponding face.

   Inherit Scale
      Scale the *DupliFaces* objects.

*Make Dupli-Face* tool converts linked objects (that share mesh data) into dupli-face instanced.
This tool creates the parent object (duplicator) with faces where the objects were,
then it uses *Duplication Faces* to put instances at the location of every created face.

You can to go back from *DupliFaces* instancing to multiple linked objects using
:menuselection:`Object --> Apply --> Make Duplicates Real`, :kbd:`Shift-Ctrl-A`.

.. seealso:: Example blend-file

   Download the blend-file used for the examples on this page
   `here <https://wiki.blender.org/wiki/File:Manual-2.5-Duplifaces-Example01.blend>`__.


Basic Usage
===========

In this example we will use a UV sphere with an extruded "north pole" as our base object and
cube as our parent mesh. To parent the sphere to the cube, in *Object Mode*,
first :kbd:`RMB` select the sphere, then :kbd:`Shift-RMB` select the cube
(order is very important here), and finally :kbd:`Ctrl-P` to parent.

.. list-table::

   * - .. figure:: /images/editors_3dview_object_properties_duplication_duplifaces_cube-before.png
          :width: 320px

          A cube and a sphere.

     - .. figure:: /images/editors_3dview_object_properties_duplication_duplifaces_cube-after.png
          :width: 320px

          Duplication Faces applied to the cube.

Next, in the :menuselection:`Object tab --> Duplication panel`,
enable *Faces*. The sphere is duplicated one for each face of the cube.

.. note:: Inherited properties

   The location, orientation, and scale of the duplicated child(ren) matches that of the faces of the parent.
   So, if several objects are parented to the cube, they will all be duplicated once for each face on the cube.
   If the cube is subdivided, every child will be duplicated for each face on the cube.

Both the parent object and original are displayed as editable "templates" in 3D View,
but neither is rendered.


Scale
=====

.. list-table::

   * - .. figure:: /images/editors_3dview_object_properties_duplication_duplifaces_scale-enabled.png
          :width: 320px

          Scale enabled.

     - .. figure:: /images/editors_3dview_object_properties_duplication_duplifaces_scale-changed.png
          :width: 320px

          Top face of cube scaled down.

By enabling *Scale* for the parent object,
the scale of the child objects will be adapted to the size of each face in the parent object.

Thus, by rescaling the face of the parent object,
the size of the duplicated object will change accordingly.


Limitations/Considerations
==========================

The positioning of the duplicated geometry relative to the face is dependent upon the position
of the child objects relative to the duplicator's origin. This can lead to some visual
artifacts in the editor as the geometry of the original objects overlaps or intersects with
the duplicates.
One workaround is to move the origin of the duplicator mesh off of the plane of the faces.

If the geometry of the children is not symmetrical then the orientation of the face
(as determined by the order of its vertices) could matter. As of 2.70 Blender does not have
tools which allow you to adjust the ordering of the vertices on a face.

However, there is a workflow that lets you control for this. Make a single square and
enable the Duplication/Faces so you can see the duplicated geometry in your editor.
If the orientation is not what you want, rotate the face until it is how you want.
Typically you want to do the rotation in Edit Mode, not Object Mode,
but this is not a hard rule.

Once you have the orientation correct,
Duplicate the face and move the duplicate where you want it.
Repeat this process until you have enough faces.
Since it is common for these faces to butt up against one another,
your geometry will have lots of duplicate vertices.
Use the Remove Doubles button in the Tools panel.


.. rubric:: Demo Video

A short video illustrating this workflow:

.. youtube:: diI8xJ9oo_8
