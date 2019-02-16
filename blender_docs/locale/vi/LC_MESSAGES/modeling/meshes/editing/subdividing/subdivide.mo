��    L      |              �  g   �  0   E  G   v     �     �  �   �  N   z  j   �     4  �   D  I   �  	   !     +     4     8  �   F  �   �     �	      �	  �   �	  �   �
  �   (  �   �  u   k     �     �     	  
        (     -     F     K     T     c  	   l     v     ~     �     �     �     �     �     �     �     �  	   �     	  &        E  
   c  �   n     �  	             0  �   P  r   .     �  }   �  F  0  G   w  <   �  ]   �     Z     f     j     }     �     �     �  �   �  `   �  �   	  (   �  &   �  �  �  g   �  0     G   2  +   z     �  �   �  N   U  j   �       �   #  I   �  %         &     @     T  �   b  �        �      �  �   �  �   �  �   T  �     u   �                 8   $   L      q      �      �      �   $   �      �   	   �      �      !     !!     9!     H!     b!     v!  +   �!     �!  "   �!     �!     "  &   "     ="     ["  �   u"     #      #     8#     V#  �   v#  r   T$     �$  }   �$  F  V%  G   �&  <   �&  ]   "'     �'     �'     �'     �'     �'     �'  *    (  �   +(  `   )  �   l)  (   �)  &   *   :menuselection:`Mesh --> Edges --> Subdivide`, :menuselection:`Specials --> Subdivide/Subdivide Smooth` :menuselection:`Mesh --> Edges --> Un-Subdivide` :menuselection:`Tool Shelf --> Tools --> Mesh Tools --> Add: Subdivide` Along Normal Along normal set to 1. Below are several examples illustrating the various possibilities of the *Subdivide* and *Subdivide Multi* tools. Note the selection after subdivision. Causes the vertices to move along their normals, instead of random directions. Changes the random seed of the *Fractal* noise function, producing a different result for each seed value. Corner Cut Type Displaces subdivisions to maintain approximate curvature. The effect is similar to the way the Subdivision Surface Modifier might deform the mesh. Displaces the vertices in random directions after the mesh is subdivided. Edit Mode Examples Fan Fan cut type. First an edge is created between the two opposite ends of the selected edges, dividing the quad in two triangles. Then, the same goes for the involved triangle as described above. Forces subdivide to create triangles or quads instead of n-gons (see examples below). This mode doesn't allow the use of *Straight Cut* on quad corners. Fractal How many subdivisions to remove. If the face is a quad, and the edges are neighbors, we have *three* possible behaviors, depending on the setting of *Corner Cut Type* (the select menu next to the *Subdivide* button, in *Mesh Tools* panel). See below for details. If the face is a quad, and the edges are opposite, the quad is just subdivided in two quads by the edge linking the two new vertices. If the face is a quad, first the two opposite edges are subdivided as described above. Then, the "middle" edge is subdivided, affecting its new "sub-quad" as described above for only one edge. If the face is a triangle, a new edge is created between the two new vertices, subdividing the triangle in a triangle and a quad. If the face is a triangle, this means the whole face is selected and it is then subdivided in four smaller triangles. Inner vertices Inner vertices cut type. Innervert cut type. Iterations Menu Mesh before subdividing. Mode Multicut Number of Cuts One Edge One Edge. Options Panel Path Path cut type. Plane before subdivision. Quad with two cuts. Quad/Four Edges Quad/Tri Mode Quad/Tri Mode. Random Seed Reference Regular subdivision. Same mesh with a different seed value. Same mesh with fractal added. Smoothness Specifies the number of cuts per edge to make. By default this is 1, cutting edges in half. A value of 2 will cut it into thirds, and so on. Straight Cut Subdivide Subdivided with no smoothing. Subdivided with smoothing of 1. Subdividing splits selected edges and faces by cutting them in half or more, adding new vertices, and subdividing accordingly the faces involved. It adds resolution to the mesh by divide faces or edges into smaller units. The quad is subdivided in a fan of four triangles, the common vertex being the one opposite to the selected edges. The sample mesh. The selected edges are subdivided, then an edge is created between the two new vertices, creating a small triangle and n-gon. The selected edges are subdivided, then an edge is created between the two new vertices, creating a small triangle. This edge is also subdivided, and the "inner vertex" thus created is linked by another edge to the one opposite to the original selected edges. All this results in a quad subdivided in a triangle and two quads. These options are available in the *Tool Panel* after running the tool; This process follows a few rules, depending on the settings: This select menu controls the way quads with only two adjacent selected edges are subdivided. Three Edges Tri Tri with two cuts. Two Adjacent Quad Edges Two Opposite Quad Edges Two Tri Edges Un-Subdivide Unsubdivide functions as the reverse of subdivide by attempting to remove edges that were the result of a subdivide operation. If additional editing has been done after the subdivide operation, unexpected results may occur. When four edges of a face (a quad) are selected, the face is subdivided into four smaller quads. When only one edge of a face is selected (Triangle mode), triangles are subdivided into two triangles, and quads, into three triangles. When three edges of a face are selected: When two edges of a face are selected: Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-12-07 01:52+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 :menuselection:`Mesh --> Edges --> Subdivide`, :menuselection:`Specials --> Subdivide/Subdivide Smooth` :menuselection:`Mesh --> Edges --> Un-Subdivide` :menuselection:`Tool Shelf --> Tools --> Mesh Tools --> Add: Subdivide` Theo Hướng Pháp Tuyến -- Along Normal Along normal set to 1. Below are several examples illustrating the various possibilities of the *Subdivide* and *Subdivide Multi* tools. Note the selection after subdivision. Causes the vertices to move along their normals, instead of random directions. Changes the random seed of the *Fractal* noise function, producing a different result for each seed value.  -- Corner Cut Type Displaces subdivisions to maintain approximate curvature. The effect is similar to the way the Subdivision Surface Modifier might deform the mesh. Displaces the vertices in random directions after the mesh is subdivided. Chế Độ Biên Soạn -- Edit Mode Các Ví Dụ -- Examples Hình Quạt -- Fan Fan cut type. First an edge is created between the two opposite ends of the selected edges, dividing the quad in two triangles. Then, the same goes for the involved triangle as described above. Forces subdivide to create triangles or quads instead of n-gons (see examples below). This mode doesn't allow the use of *Straight Cut* on quad corners. Phân Dạng -- Fractal How many subdivisions to remove. If the face is a quad, and the edges are neighbors, we have *three* possible behaviors, depending on the setting of *Corner Cut Type* (the select menu next to the *Subdivide* button, in *Mesh Tools* panel). See below for details. If the face is a quad, and the edges are opposite, the quad is just subdivided in two quads by the edge linking the two new vertices. If the face is a quad, first the two opposite edges are subdivided as described above. Then, the "middle" edge is subdivided, affecting its new "sub-quad" as described above for only one edge. If the face is a triangle, a new edge is created between the two new vertices, subdividing the triangle in a triangle and a quad. If the face is a triangle, this means the whole face is selected and it is then subdivided in four smaller triangles. -- Inner vertices Inner vertices cut type. Innervert cut type. Số Lần Lặp Lại -- Iterations Trình Đơn -- Menu Mesh before subdividing. Chế Độ -- Mode -- Multicut Số Phân Đoạn -- Number of Cuts -- One Edge One Edge. Tùy Chọn -- Options Bảng -- Panel Đường Dẫn -- Path Path cut type. Plane before subdivision. Quad with two cuts. -- Quad/Four Edges Chế Độ Tam/Tứ Giác -- Quad/Tri Mode Quad/Tri Mode. Mầm Ngẫu Nhiên -- Random Seed Tham Chiếu -- Reference Regular subdivision. Same mesh with a different seed value. Same mesh with fractal added. Độ Mịn -- Smoothness Specifies the number of cuts per edge to make. By default this is 1, cutting edges in half. A value of 2 will cut it into thirds, and so on. Cắt Thẳng -- Straight Cut Phân Chia -- Subdivide Subdivided with no smoothing. Subdivided with smoothing of 1. Subdividing splits selected edges and faces by cutting them in half or more, adding new vertices, and subdividing accordingly the faces involved. It adds resolution to the mesh by divide faces or edges into smaller units. The quad is subdivided in a fan of four triangles, the common vertex being the one opposite to the selected edges. The sample mesh. The selected edges are subdivided, then an edge is created between the two new vertices, creating a small triangle and n-gon. The selected edges are subdivided, then an edge is created between the two new vertices, creating a small triangle. This edge is also subdivided, and the "inner vertex" thus created is linked by another edge to the one opposite to the original selected edges. All this results in a quad subdivided in a triangle and two quads. These options are available in the *Tool Panel* after running the tool; This process follows a few rules, depending on the settings: This select menu controls the way quads with only two adjacent selected edges are subdivided. -- Three Edges Hình Tam Giác -- Tri Tri with two cuts. -- Two Adjacent Quad Edges -- Two Opposite Quad Edges -- Two Tri Edges Giảm Lượng Phân Chia -- Un-Subdivide Unsubdivide functions as the reverse of subdivide by attempting to remove edges that were the result of a subdivide operation. If additional editing has been done after the subdivide operation, unexpected results may occur. When four edges of a face (a quad) are selected, the face is subdivided into four smaller quads. When only one edge of a face is selected (Triangle mode), triangles are subdivided into two triangles, and quads, into three triangles. When three edges of a face are selected: When two edges of a face are selected: 