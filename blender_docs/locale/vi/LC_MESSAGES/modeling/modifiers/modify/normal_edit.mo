��    $      <              \     ]  �   d     �  M   �     B  �   J  M   �  ?   B  9   �  #   �  t   �  	   U  
   _     j     s  �   x     )     >  h   T     �  $   �  v   �  :   `     �     �     �  �   �     {  �   �  �   z	  p   Z
  �   �
     r  E   x     �  �  �     �  �   �     %  M   E     �  �   �  M   Q  ?   �  9   �  '     t   A     �  "   �  "   �       �   /  :   �       h   1     �  $   �  v   �  :   P     �  +   �     �  �   �  (   �  �   �  �   �  p   �  �        �  E   �  %      (Todo) Allows per-item fine control of the mix factor. Vertex group influence can be reverted using the small "arrow" button to the right. Directional Directional makes all normals point (converge) towards a given target object. Example Examples of edit custom normals to point towards a given direction, see `example blend-file <http://download.blender.org/ftp/mont29/persistent_data/sapling_CN.blend>`__. Gives modified object's center an offset before using it to generate normals. How much of the generated normals get mixed into existing ones. How to affect existing normals with newly generated ones. Lock Polygon Normals (padlock icon) Makes all normals parallel to the line between both objects' centers, instead of converging towards target's center. Max Angle Mix Factor Mix Mode Mode More complex normal manipulations can be achieved by copying normals from one mesh to another, see the :doc:`Data Transfer Modifier </modeling/modifiers/modify/data_transfer>`. Normal Edit Modifier Normal Edit Modifier. Note the *Multiply* option is **not** a cross product, but a mere component-by-component multiplication. Offset Only relevant in *Directional* mode. Only relevant in *Radial* mode if no *Target Object* is set, and in *Directional* mode when *Parallel Normals* is set. Optional in *Radial* mode, mandatory in *Directional* one. Options Parallel Normals Radial Radial aligns normals with the (origin, vertex coordinates) vector, in other words all normals seems to radiate from the given center point, as if they were emitted from an ellipsoid surface. Target Object The Normal Edit Modifier affects (or generates) custom normals. It uses a few simple parametric methods to compute normals (quite useful in game development and architecture areas), and mixes back those generated normals with existing ones. The left tree mesh has unmodified normals, while on the right one a *Normal Edit* modifier is used to bend them towards the camera. This shading trick is often used in games to fake scattering in trees and other vegetation. The only mandatory prerequisite to use it is to enable *Auto Smooth* option in Mesh properties, *Normals* panel. This modifier can be used to quickly generate radial normals for low-poly tree foliage or "fix" shading of toon-like rendering by partially bending default normals... Usage Uses this object's center as reference point when generating normals. Vertex Group Project-Id-Version: Blender 2.79 Manual 2.79
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
 Nội dung cần viết thêm Allows per-item fine control of the mix factor. Vertex group influence can be reverted using the small "arrow" button to the right. Định Hướng -- Directional Directional makes all normals point (converge) towards a given target object. Ví Dụ -- Example Examples of edit custom normals to point towards a given direction, see `example blend-file <http://download.blender.org/ftp/mont29/persistent_data/sapling_CN.blend>`__. Gives modified object's center an offset before using it to generate normals. How much of the generated normals get mixed into existing ones. How to affect existing normals with newly generated ones.  -- Lock Polygon Normals (padlock icon) Makes all normals parallel to the line between both objects' centers, instead of converging towards target's center. Góc Lớn Nhất -- Max Angle Hệ Số Pha Trộn -- Mix Factor Chế Độ Pha Trộn -- Mix Mode Chế Độ -- Mode More complex normal manipulations can be achieved by copying normals from one mesh to another, see the :doc:`Data Transfer Modifier </modeling/modifiers/modify/data_transfer>`. Bộ Điều Chỉnh Pháp Tuyến -- Normal Edit Modifier Normal Edit Modifier. Note the *Multiply* option is **not** a cross product, but a mere component-by-component multiplication. Dịch Chuyển -- Offset Only relevant in *Directional* mode. Only relevant in *Radial* mode if no *Target Object* is set, and in *Directional* mode when *Parallel Normals* is set. Optional in *Radial* mode, mandatory in *Directional* one. Tùy Chọn -- Options Pháp Tuyến Song Song -- Parallel Normals Tỏa Tròn -- Radial Radial aligns normals with the (origin, vertex coordinates) vector, in other words all normals seems to radiate from the given center point, as if they were emitted from an ellipsoid surface. Vật Thể Mục Tiêu -- Target Object The Normal Edit Modifier affects (or generates) custom normals. It uses a few simple parametric methods to compute normals (quite useful in game development and architecture areas), and mixes back those generated normals with existing ones. The left tree mesh has unmodified normals, while on the right one a *Normal Edit* modifier is used to bend them towards the camera. This shading trick is often used in games to fake scattering in trees and other vegetation. The only mandatory prerequisite to use it is to enable *Auto Smooth* option in Mesh properties, *Normals* panel. This modifier can be used to quickly generate radial normals for low-poly tree foliage or "fix" shading of toon-like rendering by partially bending default normals... Sử Dụng -- Usage Uses this object's center as reference point when generating normals. Nhóm Điểm Đỉnh -- Vertex Group 