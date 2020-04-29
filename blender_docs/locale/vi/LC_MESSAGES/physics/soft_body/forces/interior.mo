��          �                      a      �  �   �  �       �     �  �  �     �     �  �   �     �  �  �  c  j
  �  �  /   |  a  �      �     �   �    a     x  �  �     l      �  �   �     r  �  �  c  "   Bending Stiffness Bending stiffness can also be used if you want to make a subdivided plane more plank like. Without *Bending* the faces can freely rotate against each other like hinges Fig. :ref:`fig-softbody-force-interior-no-bending`. There would be no change in the simulation if you activated *Stiff Quads*, because the faces are not deformed at all in this example. In Blender's case, the ideal length is the original edge length which you designed as a part of your mesh, even before you enable the Soft Body system. Until you add the Soft Body physics, all springs are assumed to be perfectly stiff: no stretch and no squeeze. In Fig. :ref:`fig-softbody-force-interior-bending`, *Bending* is activated with a strength setting of 1. Now both cubes are more rigid. In Fig. :ref:`fig-softbody-force-interior-with`, *Stiff Quads* is activated (for both cubes). Both cubes keep their shape, there is no difference for the red cube, because it has no quads anyway. In Fig. :ref:`fig-softbody-force-interior-without`, the default settings are used (without *Stiff Quads*). The "quad only" cube will collapse completely, the cube composed of tris keeps its shape, though it will deform temporarily because of the forces created during collision. Interior Luckily, Blender allows to define additional *virtual* connections. On one hand you can define virtual connections between the diagonal edges of a quad face (*Stiff Quads* Fig. :ref:`fig-softbody-force-interior-stiff`), on the other hand you can define virtual connections between a vertex and any vertices connected to its neighbors' *Bending Stiffness*. In other words, the amount of bend that is allowed between a vertex and any other vertex that is separated by two edge connections. Settings Stiff Quads The characteristics of edges are set with the *Springs* and *Stiff Quads* properties in the *Soft Body Edges* panel. See the :ref:`Soft Body Edges settings <physics-softbody-settings-edges>` for details. Tips: Preventing Collapse To create a connection between the vertices of a soft body object there have to be forces that hold the vertices together. These forces are effective along the edges in a mesh, the connections between the vertices. The forces act like a spring. Fig. :ref:`fig-softbody-force-interior-connection` illustrates how a 3×3 grid of vertices (a mesh plane in Blender) are connected in a soft body simulation. To show the effect of the different edge settings we will use two cubes (blue: only quads, red: only tris) and let them fall without any goal onto a plane (how to set up collision is shown on the page :doc:`Collisions </physics/soft_body/collision>`). See the `example blend-file <https://wiki.blender.org/wiki/File:Blender3D Quads-BE-Stiffness.blend>`__. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2020-04-10 19:26+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@gmail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@gmail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 Độ Cứng khi Bẻ Cong -- Bending Stiffness Bending stiffness can also be used if you want to make a subdivided plane more plank like. Without *Bending* the faces can freely rotate against each other like hinges Fig. :ref:`fig-softbody-force-interior-no-bending`. There would be no change in the simulation if you activated *Stiff Quads*, because the faces are not deformed at all in this example. In Blender's case, the ideal length is the original edge length which you designed as a part of your mesh, even before you enable the Soft Body system. Until you add the Soft Body physics, all springs are assumed to be perfectly stiff: no stretch and no squeeze. In Fig. :ref:`fig-softbody-force-interior-bending`, *Bending* is activated with a strength setting of 1. Now both cubes are more rigid. In Fig. :ref:`fig-softbody-force-interior-with`, *Stiff Quads* is activated (for both cubes). Both cubes keep their shape, there is no difference for the red cube, because it has no quads anyway. In Fig. :ref:`fig-softbody-force-interior-without`, the default settings are used (without *Stiff Quads*). The "quad only" cube will collapse completely, the cube composed of tris keeps its shape, though it will deform temporarily because of the forces created during collision. -- Interior Luckily, Blender allows to define additional *virtual* connections. On one hand you can define virtual connections between the diagonal edges of a quad face (*Stiff Quads* Fig. :ref:`fig-softbody-force-interior-stiff`), on the other hand you can define virtual connections between a vertex and any vertices connected to its neighbors' *Bending Stiffness*. In other words, the amount of bend that is allowed between a vertex and any other vertex that is separated by two edge connections. Sắp Đặt -- Settings Tứ Giác Cứng -- Stiff Quads The characteristics of edges are set with the *Springs* and *Stiff Quads* properties in the *Soft Body Edges* panel. See the :ref:`Soft Body Edges settings <physics-softbody-settings-edges>` for details. -- Tips: Preventing Collapse To create a connection between the vertices of a soft body object there have to be forces that hold the vertices together. These forces are effective along the edges in a mesh, the connections between the vertices. The forces act like a spring. Fig. :ref:`fig-softbody-force-interior-connection` illustrates how a 3×3 grid of vertices (a mesh plane in Blender) are connected in a soft body simulation. To show the effect of the different edge settings we will use two cubes (blue: only quads, red: only tris) and let them fall without any goal onto a plane (how to set up collision is shown on the page :doc:`Collisions </physics/soft_body/collision>`). See the `example blend-file <https://wiki.blender.org/wiki/File:Blender3D Quads-BE-Stiffness.blend>`__. 