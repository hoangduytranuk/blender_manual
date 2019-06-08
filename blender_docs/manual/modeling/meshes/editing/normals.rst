
*******
Normals
*******

Introduction
============

In geometry, a normal is a direction or line that is perpendicular to something,
typically a triangle or surface but can also be relative to a line, a tangent line for a point on a curve,
or a tangent plane for a point on a surface.

.. figure:: /images/modeling_meshes_editing_normals_viewport.png
   :width: 350px

   A visualization of the face normals of a torus.

In the figure above, each blue line represents the normal for a face on the torus.
The lines are each perpendicular to the face on which they lie.
The visualization can be activated in the :ref:`Mesh Display panel <mesh-display-normals>`.


.. _modeling-meshes-editing-normals-shading:

Shading
=======

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode
   :Menu:      :menuselection:`Object --> Shade Smooth / Shade Flat`

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Mesh --> Shading`
   :Menu:      :menuselection:`Face --> Shade Smooth / Shade Flat`


.. _bpy.ops.object.shade_flat:

Flat
----

.. list-table:: Example mesh flat (left) and smooth-shaded (right).
   `Sample blend-file <https://wiki.blender.org/wiki/File:25-manual-meshsmooth-example.blend>`__.

   * - .. figure:: /images/modeling_meshes_editing_normals_example-flat.png
          :width: 200px

     - .. figure:: /images/modeling_meshes_editing_normals_example-smooth.png
          :width: 200px

As seen in the previous sections, polygons are central to Blender.
Most objects are represented by polygons and truly curved objects
are often approximated by polygon meshes. When rendering images,
you may notice that these polygons appear as a series of small, flat faces.
Sometimes this is a desirable effect, but usually we want our objects to look nice and smooth.


.. _bpy.ops.object.shade_smooth:

Smooth
------

The easiest way is to set an entire object as smooth or faceted by selecting a mesh object,
and in *Object Mode*, select *Shade Smooth* in the *Object* menu.
This forces the assignment of the "smoothing" attribute to each face in the mesh,
including when you add or delete geometry.

Notice that the outline of the object is still strongly faceted.
Activating the smoothing features does not actually modify the object's geometry;
it changes the way the shading is calculated across the surfaces (normals will be interpolated),
giving the illusion of a smooth surface.

Select the *Shade Flat* item in the *Object* menu
to revert the shading back (normals will be constant)
to that shown in the first image above.


Smoothing Parts of a Mesh
^^^^^^^^^^^^^^^^^^^^^^^^^

Alternatively, you can choose which faces to smooth by entering *Edit Mode*,
then selecting some faces and picking *Shade Smooth* from the *Face Menu*.

When the mesh is in *Edit Mode*,
only the selected faces will receive the "smoothing" attribute. You can set faces as flat
(removing the "smoothing" attribute)
in the same way by selecting edges and picking the *Shade Flat* from the *Face Menu*.

.. seealso::

   The :ref:`Auto Smooth <auto-smooth>` option is a quick and easy way to combine smooth and
   faceted faces in the same object.


.. _modeling_meshes_editing_normals_properties:

Properties
==========

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties editor --> Object Data --> Normals`

.. figure:: /images/modeling_meshes_properties_object-data_normals-panel.png

   Normals panel.

.. _auto-smooth:

Auto Smooth
   Edges where an angle between the faces is smaller than specified in the *Angle* button will be smoothed,
   when shading of these parts of the mesh is set to smooth. This is an easier way to combine smooth and sharp edges.

   Angle
      Angle number button.


Example
-------

.. figure:: /images/modeling_meshes_properties_object-data_example-auto-smooth.png
   :width: 250px

   Example mesh with *Auto Smooth* enabled.

.. seealso:: Edge Split Modifier

   With the :doc:`Edge Split Modifier </modeling/modifiers/generate/edge_split>` a result
   similar to *Auto Smooth* can be achieved with the ability to choose which edges should be split,
   based on angle.


.. _modeling-meshes-editing-normals-editing:

Editing
=======

Flip Direction
--------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Panel:     :menuselection:`Tool Shelf --> Shading/UVs --> Shading --> Normals: Flip Direction`
   :Menu:      :menuselection:`Mesh --> Normals --> Flip` or :menuselection:`Specials --> Flip Normals`

Well, it will just reverse the normals direction of all selected faces.
Note that this allows you to precisely control the direction
(**not** the orientation, which is always perpendicular to the face) of your normals,
as only selected ones are flipped.


Recalculate Normals
-------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Panel:     :menuselection:`Tool Shelf --> Shading/UVs --> Shading --> Normals: Recalculate`
   :Menu:      :menuselection:`Mesh --> Normals --> Recalculate Outside` and
               :menuselection:`Mesh --> Normals --> Recalculate Inside`
   :Hotkey:    :kbd:`Ctrl-N` and :kbd:`Shift-Ctrl-N`

These tools will recalculate the normals of selected faces so that they point outside
(respectively inside) the volume that the face belongs to.
This volume do not need to be closed. In fact, this means that the face of interest must be
adjacent with at least one non-coplanar other face.
For example, with a *Grid* primitive, recalculating normals does not have a meaningful result.


Set from Face
-------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Panel:     :menuselection:`Tool Shelf --> Shading/UVs --> Shading --> Normals: Set from Face`

Sets the custom vertex normals from the selected face's normals.


.. _modeling_meshes_normals_custom:

Custom Split Normals
====================

*Custom Split Normals* is a way to tweak/fake shading by pointing them towards other directions than default,
auto-computed ones. It is mostly used in game development, where it allows to counterbalance some issues generated
by low-poly objects (the most common examples are low-poly trees/bushes/grass/etc., and the 'rounded' corners).

Blender supports custom normals on a 'smooth fan' base, defined as a set of neighbor face corners
sharing the same vertex and 'linked' by smooth edges. This means you can have normals per face corners,
per a set of neighbor face corners, or per vertex.


Enabling Custom Split Normals Support
-------------------------------------

#. Enable custom split normals using :ref:`Add Custom Split Normals Data <modeling_meshes_properties_custom-data>`.
#. Make sure to enable :ref:`Auto Smooth <modeling_meshes_editing_normals_properties>`.

.. note::

   Once you have custom normals, the angle threshold of the *Auto Smooth* behavior is disabled --
   all non-sharp-tagged edges will be considered as smooth, disregarding the angle between their faces.


Creating/Editing Custom Split Normals
-------------------------------------

Currently, editing is only possible by using the :doc:`/modeling/modifiers/modify/normal_edit`.

You can also copy normals from another mesh using Data Transfer
(:doc:`operator </modeling/meshes/editing/data_transfer>`
or :doc:`modifier </modeling/modifiers/modify/data_transfer>`).


Importing Custom Split Normals
------------------------------

Some tools, in particular :abbr:`CAD (Computer-Aided Design)` ones, tends to generate irregular geometry
when tessellating their objects into meshes (very thin and long triangles, etc.).
Auto-computed normals on such geometry often gives bad artifacts,
so it is important to be able to import and use the normals as generated by the CAD tool itself.

.. note::

   Currently, only the FBX importer is capable of importing custom normals.
