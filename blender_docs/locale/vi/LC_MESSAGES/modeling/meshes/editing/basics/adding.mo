��          �               �  5   �  C   �               '     C     R     d  	   �  |  �  '  
     2  C  9  �   }  H   w	  N   �	     
  4   
  	   I
  ;  S
  �  �  g    �  x  5   0  C   f     �     �     �     �     �  P     %   c  |  �  '       .  C  D  �   �  H   �  N   �       4   .     c  ;  }  �  �  g  :   :doc:`/modeling/meshes/editing/basics/make_face_edge` :doc:`Duplicate tools </modeling/meshes/editing/duplicating/index>` :kbd:`Ctrl-LMB` Adding Geometry Adding vertices one by one. Creating Faces Creating Vertices Duplicate or Extrude to Cursor Edit Mode For :kbd:`Ctrl-LMB`, Blender will automatically rotate the last selected Edge (the source) for the subsequent operations if you have at least one face created, dividing the angles created between the newly created edge and the last two edges, creating a smooth angle between them. Blender will calculate this angle using the last positive and negative position of the last X and Y coordinates and the last connected unselected edge. If this angle exceeds a negative limit (following a quadrant rule) between the recently created edge and the last two, Blender will wrap the faces. But if you do not want Blender to rotate and smooth edges automatically when extruding from :kbd:`Ctrl-LMB`, you can also inhibit Blender from rotating sources using the shortcut :kbd:`Shift-Ctrl-LMB`. In this case, Blender will not rotate the source dividing the angle between those edges when creating a face. For both cases, Blender will inform the user about the source rotation during the creation process. If you look at the Operator Panel and press :kbd:`Ctrl-LMB`, you will see that the Rotate Source is automatically checked and if :kbd:`Shift-Ctrl-LMB` is used, it will be automatically unchecked. Hotkey If you have three or more vertices selected, and :kbd:`Ctrl-LMB` click, you will also create planar faces, but along the vertices selected, following the direction of the cursor. This operation is similar to an extrude operation, which is explained in the :doc:`Extrude </modeling/meshes/editing/duplicating/extrude>` page. If you have two vertices selected and already connected with an edge, :kbd:`Ctrl-LMB` click will create a planar face, also known as a quad. Blender will follow your mouse cursor and will use the planar view from your viewport to create those quads. In Blender, for modeling, you have several ways of adding mesh elements. Interactively places new vertices with :kbd:`Ctrl-LMB` at the cursor position. Mode Quad from an Edge with source automatically rotated. Reference The most basic element, a vertex, can be added with a :kbd:`Ctrl-LMB` click when no other vertices are selected. Because the camera space (computer screen) is two-dimensional, Blender cannot determine all three vertex coordinates from a single mouse click, so the new vertex is placed at the depth of the 3D cursor. To create interconnected vertices, you can add a vertex and continuously make subsequent :kbd:`Ctrl-LMB` operations with the last vertex selected. This will link the last selected vertex with the vertex created at the mouse position with an edge (See Fig. :ref:`fig-mesh-basics-add-one`), and will continuously create and connect new vertices if you continue repeating this operation. When adding Objects with :kbd:`Ctrl-LMB`, the extrusions of the selected elements, being vertices, edges and faces with the :kbd:`Ctrl-LMB`, are viewport dependent. This means, once you change your viewport, for example, from top to left, bottom or right, the extrusion direction will also follow your viewport and align your extrusions with your planar view. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-12-04 21:09+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 :doc:`/modeling/meshes/editing/basics/make_face_edge` :doc:`Duplicate tools </modeling/meshes/editing/duplicating/index>` :kbd:`Ctrl-LMB` -- Adding Geometry Adding vertices one by one.  -- Creating Faces  -- Creating Vertices Sao Chép hoặc Đẩy Trồi tới Con Trỏ -- Duplicate or Extrude to Cursor Chế Độ Biên Soạn -- Edit Mode For :kbd:`Ctrl-LMB`, Blender will automatically rotate the last selected Edge (the source) for the subsequent operations if you have at least one face created, dividing the angles created between the newly created edge and the last two edges, creating a smooth angle between them. Blender will calculate this angle using the last positive and negative position of the last X and Y coordinates and the last connected unselected edge. If this angle exceeds a negative limit (following a quadrant rule) between the recently created edge and the last two, Blender will wrap the faces. But if you do not want Blender to rotate and smooth edges automatically when extruding from :kbd:`Ctrl-LMB`, you can also inhibit Blender from rotating sources using the shortcut :kbd:`Shift-Ctrl-LMB`. In this case, Blender will not rotate the source dividing the angle between those edges when creating a face. For both cases, Blender will inform the user about the source rotation during the creation process. If you look at the Operator Panel and press :kbd:`Ctrl-LMB`, you will see that the Rotate Source is automatically checked and if :kbd:`Shift-Ctrl-LMB` is used, it will be automatically unchecked. Phím Tắt -- Hotkey If you have three or more vertices selected, and :kbd:`Ctrl-LMB` click, you will also create planar faces, but along the vertices selected, following the direction of the cursor. This operation is similar to an extrude operation, which is explained in the :doc:`Extrude </modeling/meshes/editing/duplicating/extrude>` page. If you have two vertices selected and already connected with an edge, :kbd:`Ctrl-LMB` click will create a planar face, also known as a quad. Blender will follow your mouse cursor and will use the planar view from your viewport to create those quads. In Blender, for modeling, you have several ways of adding mesh elements. Interactively places new vertices with :kbd:`Ctrl-LMB` at the cursor position. Chế Độ -- Mode Quad from an Edge with source automatically rotated. Tham Chiếu -- Reference The most basic element, a vertex, can be added with a :kbd:`Ctrl-LMB` click when no other vertices are selected. Because the camera space (computer screen) is two-dimensional, Blender cannot determine all three vertex coordinates from a single mouse click, so the new vertex is placed at the depth of the 3D cursor. To create interconnected vertices, you can add a vertex and continuously make subsequent :kbd:`Ctrl-LMB` operations with the last vertex selected. This will link the last selected vertex with the vertex created at the mouse position with an edge (See Fig. :ref:`fig-mesh-basics-add-one`), and will continuously create and connect new vertices if you continue repeating this operation. When adding Objects with :kbd:`Ctrl-LMB`, the extrusions of the selected elements, being vertices, edges and faces with the :kbd:`Ctrl-LMB`, are viewport dependent. This means, once you change your viewport, for example, from top to left, bottom or right, the extrusion direction will also follow your viewport and align your extrusions with your planar view. 