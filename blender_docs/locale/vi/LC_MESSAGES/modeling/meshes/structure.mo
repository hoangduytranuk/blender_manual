��          �                 {     
   �     �  
   �     �  }   �  }   )     �     �  	   �    �  	  �     �  ^   �  �  G  {   �     {     �  %   �     �  }   �  }   c	  !   �	     
           	  :     D  ^   `   *Edge* and *face* loops are sets of faces or edges that form continuous "loops" as shown in Fig. :ref:`fig-mesh-topo-loop`. Edge Loops Edges Face Loops Faces Further details on working with edge loops can be found in :ref:`Edge Loop Selection <modeling-meshes-selecting-edge-loops>`. Further details on working with face loops can be found in :ref:`Face Loop Selection <modeling-meshes-selecting-face-loops>`. Loops Loops (1 and 2) in Fig. :ref:`fig-mesh-topo-loop` are edge loops. They connect vertices so that each one on the loop has exactly two neighbors that are not on the loop and placed on both sides of the loop (except the start and end vertex in case of poles). Structure Take Fig. :ref:`fig-mesh-topo-loop` in organic modeling as an example: the edge loops follow the natural contours and deformation lines of the skin and the underlying muscles and are more dense in areas that deform more when the character moves, for example at the shoulders or knees. These are a logical extension of edge loops in that they consist of the faces between two edge loops, as shown in loops (3 and 4) in Fig. :ref:`fig-mesh-topo-loop`. Note that for non-circular loops (4) the faces containing the poles are not included in a face loop. Vertices With meshes, everything is built from three basic structures: *vertices*, *edges* and *faces*. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-11-04 02:53+0000
PO-Revision-Date: 2019-03-23 14:46+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 *Edge* and *face* loops are sets of faces or edges that form continuous "loops" as shown in Fig. :ref:`fig-mesh-topo-loop`. Theo Vòng Mạch -- Edge Loops Cạnh -- Edges Vòng Mạch Bề Mặt -- Face Loops Bề Mặt -- Faces Further details on working with edge loops can be found in :ref:`Edge Loop Selection <modeling-meshes-selecting-edge-loops>`. Further details on working with face loops can be found in :ref:`Face Loop Selection <modeling-meshes-selecting-face-loops>`. Vòng Lặp/Tuần Hoàn -- Loops Loops (1 and 2) in Fig. :ref:`fig-mesh-topo-loop` are edge loops. They connect vertices so that each one on the loop has exactly two neighbors that are not on the loop and placed on both sides of the loop (except the start and end vertex in case of poles). Cấu Trúc -- Structure Take Fig. :ref:`fig-mesh-topo-loop` in organic modeling as an example: the edge loops follow the natural contours and deformation lines of the skin and the underlying muscles and are more dense in areas that deform more when the character moves, for example at the shoulders or knees. These are a logical extension of edge loops in that they consist of the faces between two edge loops, as shown in loops (3 and 4) in Fig. :ref:`fig-mesh-topo-loop`. Note that for non-circular loops (4) the faces containing the poles are not included in a face loop. Điểm Đỉnh -- Vertices With meshes, everything is built from three basic structures: *vertices*, *edges* and *faces*. 