��          �               �  J  �     �       A     4   P  6   �  8   �  q   �     g  	   o     y     �     �     �     �     �  �   �     �     �     �  	   �     �  $  �  �     �  �  J  n	     �
     �
  �   �
  t   a  s   �  �   J  q   �     B  %   X     ~  "   �  -   �  )   �  >        W  �   m     d     y     �     �     �  $  �  �   �   *Extrude Individual* allows you to extrude a selection of multiple faces as individuals, instead of as a region. The faces are extruded along their own normals, rather than their average. This has several consequences: first, "internal" edges (i.e. edges between two selected faces) are no longer deleted (the original faces are). :kbd:`Alt-E` :kbd:`E` :menuselection:`Mesh --> Extrude --> Extrude Edges/Vertices Only` :menuselection:`Mesh --> Extrude --> Extrude Region` :menuselection:`Mesh --> Extrude --> Individual Faces` :menuselection:`Operator Search --> Extrude Repeat Mesh` Although the process is quite intuitive, the principles behind *Extrude* are fairly elaborate as discussed below: Details Edit Mode Extrude Extrude Edges and Vertices Only Extrude Individual Extrude Region Extrude Repeat Mesh Hotkey If vertices are selected while doing an extrude, but they do not form an edge or face, they will extrude as expected, forming a :term:`non-manifold` edge. Similarly, if edges are selected that do not form a face, they will extrude to form a face. Menu Mode Offset Reference Steps This tool has to be called from :doc:`/interface/controls/templates/operator_search`. If the selection is not manifold it's extruded the specified number of times, else it behaves similar to the :doc:`/modeling/modifiers/generate/array`. The extrusion is aligned along the Z axis of the view. To force a vertex or edge selection to extrude as a vertex or edge, respectively, use :kbd:`Alt-E` to access the Extrude *Edges Only* and *Vertices Only*. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2020-02-14 15:11+0100
PO-Revision-Date: 2019-04-24 02:16+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 *Extrude Individual* allows you to extrude a selection of multiple faces as individuals, instead of as a region. The faces are extruded along their own normals, rather than their average. This has several consequences: first, "internal" edges (i.e. edges between two selected faces) are no longer deleted (the original faces are). :kbd:`Alt-E` :kbd:`E` :menuselection:`Khung Lưới (Mesh) --> Đẩy Trồi/Nới (Extrude) --> Đẩy Trồi/Nới Edges/Vertices Only (Extrude Edges/Vertices Only)` :menuselection:`Khung Lưới (Mesh) --> Đẩy Trồi/Nới (Extrude) --> Đẩy Trồi Khu Vực (Extrude Region)` :menuselection:`Khung Lưới (Mesh) --> Đẩy Trồi/Nới (Extrude) --> Cá Nhân Bề Mặt (Individual Faces)` :menuselection:`Tìm Kiếm Thao Tác/Toán Tử (Operator Search) --> Lặp Lại Đẩy Trồi Khung Lưới (Extrude Repeat Mesh)` Although the process is quite intuitive, the principles behind *Extrude* are fairly elaborate as discussed below: Chi Tiết -- Details Chế Độ Biên Soạn -- Edit Mode Đẩy Trồi/Nới -- Extrude -- Extrude Edges and Vertices Only Đẩy Trồi Cá Nhân -- Extrude Individual Đẩy Trồi Khu Vực -- Extrude Region Lặp Lại Đẩy Trồi Khung Lưới -- Extrude Repeat Mesh Phím Tắt -- Hotkey If vertices are selected while doing an extrude, but they do not form an edge or face, they will extrude as expected, forming a :term:`non-manifold` edge. Similarly, if edges are selected that do not form a face, they will extrude to form a face. Trình Đơn -- Menu Chế Độ -- Mode Dịch Chuyển -- Offset Tham Chiếu -- Reference Số Bước -- Steps This tool has to be called from :doc:`/interface/controls/templates/operator_search`. If the selection is not manifold it's extruded the specified number of times, else it behaves similar to the :doc:`/modeling/modifiers/generate/array`. The extrusion is aligned along the Z axis of the view. To force a vertex or edge selection to extrude as a vertex or edge, respectively, use :kbd:`Alt-E` to access the Extrude *Edges Only* and *Vertices Only*. 