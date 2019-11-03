��    3      �              L  	   M     W     g     x     �     �     �     �     �     �     �     �     �                &  p   5     �     �  K   �               )     <     M     \     b     h     z       �   �     ,     A     R     X     a     p  $   �     �     �     �  q   �  V   [     �     �     �     �  .  �  [   *	  D   �	  �  �	     �  2   �  *   �  (   �     $  )   =     g     {     �  .   �     �     �     �  -   
  3   8  &   l  p   �       !     K   7  $   �  &   �     �     �  4   �     .     E     `     u     �  �   �  8   @  7   y  ~   �     0  "   F  I   i  $   �     �  ,   �     #  q   6  V   �  /   �     /  3   M  G   �  .  �  [   �  D   T   Animation Apply Modifiers Armature Options Auto Connect Camera Collada Exporter Collada Importer Collada Options Copy Deform Bones Only Export Export & Import Export Data Options Export to SL/OpenSim Find Bone Chains Fix Leaf Bones Fully rigified Armature animations (referring to the Rigify add-on). For export of rigified Armature animations: Import Import Units Import and export of animations for the following parameters are supported: Include Armatures Include Children Include Shape keys Include Textures Keep Bind Info Light Lines Material & Effect Mesh Nodes On import parent transformations for ``<instance_node>``\ s is properly propagated to child node instances. Blender materials are exported with the following mapping: Only Selected UV Map Operator Presets Phong Polygons Selection Only Sort by Object Name Special Notes for Second Life users: Supported geometry types are: Technical Details Texture Options The Collada importer is mostly driven by the imported data. There is one option for controlling the import units: There are two operator presets (see top of Operator panel) for Second Life (SL) users: Transformation Type Triangulate Use Blender Profile Use Object Instances When a rig is imported to Blender, then the rig's bind pose will be used as Blender's rest pose. So all Matrix information of the original rest pose is lost. But in some cases you may want to preserve the original rig information. The new option *Keep Bind Info* checks each bone for having two arrays: When this option is enabled, then the importer creates two custom properties for each bone: `Demonstration video <http://www.youtube.com/watch?v=GTlmmd13J1w>`__ Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-07-06 20:15+0100
PO-Revision-Date: 2019-04-24 02:16+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.7.0
 Hoạt Họa -- Animation Áp Dụng Bộ Điều Chỉnh -- Apply Modifiers Tùy Chọn về Cốt -- Armature Options Tự Động Kết Nối -- Auto Connect Máy Quay Phim -- Camera Trình Xuất Collada -- Collada Exporter -- Collada Importer -- Collada Options Sao Chép -- Copy Duy Biến Dạng Xương -- Deform Bones Only Xuất -- Export -- Export & Import -- Export Data Options Xuất cho Sl/OpenSim -- Export to SL/OpenSim Tìm các Dây Chuyền Xương -- Find Bone Chains Sửa Xương Ngọn -- Fix Leaf Bones Fully rigified Armature animations (referring to the Rigify add-on). For export of rigified Armature animations: Nhập -- Import Nhập Đơn Vị -- Import Units Import and export of animations for the following parameters are supported: Bao Gồm Cốt -- Include Armatures Bao Gồm Con Cái -- Include Children -- Include Shape keys -- Include Textures Lưu Giữ Thông Tin Kết Buộc -- Keep Bind Info Nguồn Sáng -- Light Đường Thẳng -- Lines -- Material & Effect Khung Lưới -- Mesh Nút -- Nodes On import parent transformations for ``<instance_node>``\ s is properly propagated to child node instances. Blender materials are exported with the following mapping: Duy Ánh Xạ UV Được Chọn -- Only Selected UV Map Sắp Đặt Sẵn của Toán Tử -- Operator Presets `Phương pháp tô bóng Phong <https://vi.wikipedia.org/wiki/Ph%C6%B0%C6%A1ng_ph%C3%A1p_t%C3%B4_b%C3%B3ng_Phong>`__ -- Phong Đa Giác -- Polygons Duy Lựa Chọn -- Selection Only Sắp Xếp Thứ Tự theo Tên của Vật Thể -- Sort by Object Name Special Notes for Second Life users: Supported geometry types are: Chi Tiết Kỹ Thuật -- Technical Details -- Texture Options The Collada importer is mostly driven by the imported data. There is one option for controlling the import units: There are two operator presets (see top of Operator panel) for Second Life (SL) users: Thể Loại Biến Hóa -- Transformation Type Tam Giác Hóa -- Triangulate Dùng Hồ Sơ của Blender -- Use Blender Profile Sử Dụng các Thực Thể của Vật Thể -- Use Object Instances When a rig is imported to Blender, then the rig's bind pose will be used as Blender's rest pose. So all Matrix information of the original rest pose is lost. But in some cases you may want to preserve the original rig information. The new option *Keep Bind Info* checks each bone for having two arrays: When this option is enabled, then the importer creates two custom properties for each bone: `Demonstration video <http://www.youtube.com/watch?v=GTlmmd13J1w>`__ 