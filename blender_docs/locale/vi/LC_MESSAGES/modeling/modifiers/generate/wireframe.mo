��    %      D              l  �   m     '     0     =  -   K  T   y  J   �  V        p          �  �   �  o        �  !   �  r   �     !     1     8  I   @     �     �  0   �  v  �  $   V  =   {  	   �  �   �  w   �	     
     
     -
     @
  +   T
  �   �
      {  �  �  �   T       /   &  -   V  -   �  T   �  J     V   R  ,   �     �     �  �     o   �     �  !     r   6  7   �     �     �  I     1   \  *   �  0   �  v  �  $   a  =   �     �  �   �  w   �  %   !     G  5   _     �  +   �  �   �      �   A value between (-1 to 1) to change whether the wireframes are generated inside or outside the original mesh. Set to zero, *Offset* will center the wireframes around the original edges. Boundary Crease Edges Crease Weight Creates wireframes on mesh island boundaries. Cube with enabled *Crease Edges* option. The *Crease Weight* is set to 0, 0.5 and 1. Define how much crease (0 to 1) (no to full) the junctions should receive. Determines the edge thickness by the length of the edge. Longer edges will be thicker. Even Thickness Examples Factor If this option is enabled, the original mesh is replaced by the generated wireframe. If not, the wireframe is generated on top of it. In this example, the wireframes carry a second (dark) material while the displaced plane uses its original one. Invert Inverts the vertex group weights. Maintain thickness by adjusting for sharp corners. Sometimes improves quality but also increases computation time. Material Offset Offset Options Percentage that the vertex has influence over the final wireframe result. Relative Thickness Replace Original Restrict the modifier to only this vertex group. The Wireframe Modifier transforms a mesh into a wireframe by iterating over its faces, collecting all edges and turning those edges into four sided polygons. Be aware of the fact that your mesh needs to have faces to be wireframed. You can define the thickness, the material and several other parameters of the generated wireframe dynamically via the given modifier options. The depth or size of the wireframes. The weights of the vertex group gradually change from 0 to 1. Thickness This option is intended for usage with the :doc:`Subdivision Modifier </modeling/modifiers/generate/subsurf>`. Enable this option to crease edges on their junctions and prevent large curved intersections. Uses the chosen material index as the material for the wireframe; this is applied as an offset from the first material. Vertex Group Vertex Group weighting. Wireframe Modifier Wireframe Modifier. Wireframe and Subdivision Surface modifier. Wireframe thickness is an approximation. While *Even Thickness* should yield good results in many cases, skinny faces can cause ugly spikes. In this case you can either reduce the extreme angles in the geometry or disable the *Even Thickness* option. Wireframes on a displaced plane. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-11-14 21:46+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 A value between (-1 to 1) to change whether the wireframes are generated inside or outside the original mesh. Set to zero, *Offset* will center the wireframes around the original edges. Ranh Giới -- Boundary Miết Nếp Gấp của Cạnh -- Crease Edges Trọng Lượng Nếp Gấp -- Crease Weight Creates wireframes on mesh island boundaries. Cube with enabled *Crease Edges* option. The *Crease Weight* is set to 0, 0.5 and 1. Define how much crease (0 to 1) (no to full) the junctions should receive. Determines the edge thickness by the length of the edge. Longer edges will be thicker. Chiều Dày Đều Đặn -- Even Thickness Các Ví Dụ -- Examples Hệ Số -- Factor If this option is enabled, the original mesh is replaced by the generated wireframe. If not, the wireframe is generated on top of it. In this example, the wireframes carry a second (dark) material while the displaced plane uses its original one. Đảo Nghịch -- Invert Inverts the vertex group weights. Maintain thickness by adjusting for sharp corners. Sometimes improves quality but also increases computation time. Dịch Chuyển của Nguyên Liệu -- Material Offset Dịch Chuyển -- Offset Tùy Chọn -- Options Percentage that the vertex has influence over the final wireframe result. Chiều Dày Tương Đối -- Relative Thickness Thay Thế Bản Gốc -- Replace Original Restrict the modifier to only this vertex group. The Wireframe Modifier transforms a mesh into a wireframe by iterating over its faces, collecting all edges and turning those edges into four sided polygons. Be aware of the fact that your mesh needs to have faces to be wireframed. You can define the thickness, the material and several other parameters of the generated wireframe dynamically via the given modifier options. The depth or size of the wireframes. The weights of the vertex group gradually change from 0 to 1. Độ Dày -- Thickness This option is intended for usage with the :doc:`Subdivision Modifier </modeling/modifiers/generate/subsurf>`. Enable this option to crease edges on their junctions and prevent large curved intersections. Uses the chosen material index as the material for the wireframe; this is applied as an offset from the first material. Nhóm Điểm Đỉnh -- Vertex Group Vertex Group weighting. Bộ Điều Chỉnh Khung Dây -- Wireframe Modifier Wireframe Modifier. Wireframe and Subdivision Surface modifier. Wireframe thickness is an approximation. While *Even Thickness* should yield good results in many cases, skinny faces can cause ugly spikes. In this case you can either reduce the extreme angles in the geometry or disable the *Even Thickness* option. Wireframes on a displaced plane. 