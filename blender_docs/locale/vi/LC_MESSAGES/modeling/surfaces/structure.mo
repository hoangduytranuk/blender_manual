��          t               �   �  �      Q  T  o  �   �  �  �    ?     G  	   V  G  `     �  �  �  �  g
      �  T    �   a  �  ?    �     �     �  G       W   A "row" is a set of control points forming one "line" in one interpolation direction (a bit similar to :ref:`edge loops <modeling-mesh-structure-edge-loops>` for meshes). So you have "U rows" and "V rows" in a NURBS surface. The key point is that *all* rows of a given type (U or V) have the *same* number of control points. Each control point belongs to exactly one U row and one V row. Control Points, Rows and Grid However, you can have "2D" surfaces made of curves (using the :doc:`extrusion tools </modeling/curves/properties/geometry>`, or, to a lesser extent, the filling of closed 2D curves). And you can have "1D" curves made of surfaces, like a NURBS surface with only one row (either in U or V direction) of control points produces only a curve... In Fig. :ref:`fig-surface-intro-weight` a single control point, labeled "C", has had its *Weight* set to 5.0 while all others are at their default of 1.0. As you can see, that control point *pulls* the surface towards it. It is very important to understand the difference between NURBS curves and NURBS surfaces: the first one has one dimension, the latter has two. Blender internally treats NURBS surfaces and NURBS curves completely differently. There are several attributes that separate them but the most important is that a NURBS curve has a single interpolation axis (U) and a NURBS surface has two interpolation axes (U and V). Many of the concepts from :doc:`curves </modeling/curves/introduction>`, especially :ref:`NURBS <curve-nurbs>` ones, carry directly over to NURBS surfaces, such as control points, *Order*, *Weight*, *Resolution*, etc. Here we will just talk about the differences. Preset Weights Structure Visually you can tell which is which by entering *Edit Mode* and looking at the 3D View header: either the header shows *Surface* or *Curve* as one of the menu choices. Also, you can :doc:`extrude </modeling/curves/properties/geometry>` a whole NURBS surface curve to create a surface, but you cannot with a simple NURBS curve. Weight Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2020-01-12 16:43-0500
PO-Revision-Date: 2019-04-24 02:16+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 A "row" is a set of control points forming one "line" in one interpolation direction (a bit similar to :ref:`edge loops <modeling-mesh-structure-edge-loops>` for meshes). So you have "U rows" and "V rows" in a NURBS surface. The key point is that *all* rows of a given type (U or V) have the *same* number of control points. Each control point belongs to exactly one U row and one V row. -- Control Points, Rows and Grid However, you can have "2D" surfaces made of curves (using the :doc:`extrusion tools </modeling/curves/properties/geometry>`, or, to a lesser extent, the filling of closed 2D curves). And you can have "1D" curves made of surfaces, like a NURBS surface with only one row (either in U or V direction) of control points produces only a curve... In Fig. :ref:`fig-surface-intro-weight` a single control point, labeled "C", has had its *Weight* set to 5.0 while all others are at their default of 1.0. As you can see, that control point *pulls* the surface towards it. It is very important to understand the difference between NURBS curves and NURBS surfaces: the first one has one dimension, the latter has two. Blender internally treats NURBS surfaces and NURBS curves completely differently. There are several attributes that separate them but the most important is that a NURBS curve has a single interpolation axis (U) and a NURBS surface has two interpolation axes (U and V). Many of the concepts from :doc:`curves </modeling/curves/introduction>`, especially :ref:`NURBS <curve-nurbs>` ones, carry directly over to NURBS surfaces, such as control points, *Order*, *Weight*, *Resolution*, etc. Here we will just talk about the differences. -- Preset Weights Cấu Trúc -- Structure Visually you can tell which is which by entering *Edit Mode* and looking at the 3D View header: either the header shows *Surface* or *Curve* as one of the menu choices. Also, you can :doc:`extrude </modeling/curves/properties/geometry>` a whole NURBS surface curve to create a surface, but you cannot with a simple NURBS curve. Trọng Lượng -- Weight 