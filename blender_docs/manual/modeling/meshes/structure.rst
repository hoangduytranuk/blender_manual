
*********
Structure
*********

With meshes, everything is built from three basic structures:
*vertices*, *edges* and *faces*.

.. figure:: /images/modeling_meshes_structure_example.svg
   :width: 600px

   Example of mesh structure.

.. The geometry of the faces performing the model is called topology.


Vertices
========

The most elementary part of a mesh is the vertex which is a single point or position in 3D space.
The vertices (the plural form of vertex) are stored in an array of coordinates.

It is usually invisible in rendering and in *Object Mode*.
Do not mistake the :doc:`Origin Point </editors/3dview/object/origin>` of an object for a vertex.
It looks similar, but it is bigger and you cannot select it.

.. figure:: /images/modeling_meshes_structure_cube-example.png

   The vertex is labeled as "A", and "B" is object origin.


Edges
=====

An edge always connects two vertices by a straight line.
The edges are the "wires" you see when you look at a mesh in wireframe view.
They are usually invisible on the rendered image. They are used to construct faces.


Faces
=====

Faces are used to build the actual surface of the object.
They are what you see when you render the mesh.
If this area does not contain a face,
it will simply be transparent or non-existent in the rendered image.

A face is defined as the area between either three (triangles), four (quadrangles) or more (n-gons) vertices,
with an edge on every side. The faces are often abbreviated to *tris, quads & n-gons*.

Triangles are always flat and therefore easy to calculate. On the other hand,
quadrangles "deform well" and are therefore preferred for animation and subdivision modeling.

While you could build a cube with triangular faces,
it would just look more confusing in *Edit Mode*.


Loops
=====

.. _fig-mesh-topo-loop:

.. figure:: /images/modeling_meshes_structure_edge-face-loops.png

   Edge and face loops.

*Edge* and *face* loops are sets of faces or edges that form continuous "loops" as shown in
Fig. :ref:`fig-mesh-topo-loop`.

.. note::

   Note that loops (2 and 4) do not go around the whole model.
   Loops stop at so-called poles because there is no unique way to continue a loop from a pole.
   Poles are vertices that are connected to either three, five, or more edges. Accordingly,
   vertices connected to exactly one, two or four edges are not poles.

In the image above, loops that do not end in poles are cyclic (1 and 3).
They start and end at the same vertex and divide the model into two partitions.
Loops can be a quick and powerful tool to work with specific,
continuous regions of a mesh and are a prerequisite for organic character animation.
For a detailed description of how to work with loops in Blender, see:
:doc:`Advanced Selection </modeling/meshes/selecting/advanced>`.


.. _modeling-mesh-structure-edge-loops:

Edge Loops
----------

Loops (1 and 2) in Fig. :ref:`fig-mesh-topo-loop` are edge loops.
They connect vertices so that each one on the loop has exactly two neighbors that are not on
the loop and placed on both sides of the loop (except the start and end vertex in case of poles).

Edge loops are an important concept especially in organic (subsurface)
modeling and character animation. When used correctly, they allow you to build models with
relatively few vertices that look very natural when used as subdivision surfaces and
deform very well in animation.

Take Fig. :ref:`fig-mesh-topo-loop` in organic modeling as an example: the edge loops follow the natural
contours and deformation lines of the skin and the underlying muscles and are more dense in
areas that deform more when the character moves, for example at the shoulders or knees.

Further details on working with edge loops can be found in
:ref:`Edge Loop Selection <modeling-meshes-selecting-edge-loops>`.


Face Loops
----------

These are a logical extension of edge loops in that they consist of the faces between
two edge loops, as shown in loops (3 and 4) in Fig. :ref:`fig-mesh-topo-loop`.
Note that for non-circular loops (4)
the faces containing the poles are not included in a face loop.

Further details on working with face loops can be found in
:ref:`Face Loop Selection <modeling-meshes-selecting-face-loops>`.
