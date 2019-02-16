��    I      d              �  $   �  2   �                    !  (   0  &   Y  .   �     �     �     �     �     �     �     �  	     -     '   C  )   k  >   �     �  E   �     &     -  B   =  #   �     �     �     �     �     �  ?   �     /  �   A     �  
   �     �     	  �   '	     �	     
     
     
     #
  N   A
     �
     �
     �
     �
     �
     �
  &   �
     �
  [  �
  
   D     O     c  ,   u  3   �  E   �       @   2     s  .   �     "     1     >     S     b  �   p  "   8  �  [  $     2   8     k  "   �  3   �     �  (   �  &     .   <     k  9   �  8   �     �  )     '   @  &   h     �  -   �  '   �  )     >   +     j  E   �     �  4   �  B     #   ^     �  "   �     �  #   �  %   �  ?      &   `  �   �          7     E     ^  �   s     G     \     r     �     �  N   �               2     @     X     l  &   �     �  [  �       2   7     j  ,   |  3   �  E   �     #  @   9     z  .   �  '   )  $   Q     v     �  1   �  �   �  "   �   .... _bpy.types.PointDensityTexture: Adds directed noise to the density at render time. Cache Color Source Constant Constant color Coordinate system to cache particles in. Data to derive the color results from. Density is constant within the look-up radius. Depth Emit Object Location Emit Object Space Falloff Falloff Curve Global Space Global Time Influence Level of detail in the added turbulent noise. Lifetime mapped as 0.0 - 1.0 intensity. Method for driving added turbulent noise. Multiplier to bring particle speed within an acceptable range. Noise Basis Noise patterns will remain unchanged, faster and suitable for stills. Object Object Vertices Object Vertices, Generate point density from an object's vertices. Object to take the point data from. Options Particle Age Particle Color Sources Particle Speed Particle System Particle System, Generate point density from a particle system. Particle Velocity Particle speed (absolute magnitude of velocity) mapped as 0.0 - 1.0 intensity. An additional color ramp can be used to convert intensity to RGB colors. Particle system to use. Point Data Point Density Texture Point Density panel. Point density renders a given point cloud (object vertices or particle system) as a 3D volume, using a user-defined radius for the points. Internally, the system uses a BVH data structure for fast range lookups. Radius Radius of the points. Root Scale Scale of the turbulent noise. See :doc:`Here </editors/uv_image/uv/textures/types/procedural/introduction>`. Size Smooth Soft Softness Standard Static Strength of the added turbulent noise. System The rendered points are spherical by default, with various smooth falloff options, as well as simple Turbulence options for displacing the result with noise, adding fine detail. When using Point Density with a particle system, additional particle info such as particle velocity, age, and speed, can be visualized using a color/alpha ramp gradient. Turbulence Turbulence Strength Turbulence panel. Turbulent noise driven by particle velocity. Turbulent noise driven by the global current frame. Turbulent noise driven by the particle's age between birth and death. Use a custom falloff. Use a vertex color layer for coloring the point density texture. Use a weights from a vertex group as intensity values. An additional color ramp can be used to convert intensity to RGB colors. Use object-space vertex normals as RGB values. Velocity Scale Vertex Color Vertex Color Sources Vertex Normals Vertex Weight Vertex colors are defined per face corner. A single vertex can have as many different colors as faces it is part of. The actual color of the point density texture is averaged from all vertex corners. XYZ velocity mapped to RGB colors. Project-Id-Version: Blender 2.80 Manual 2.80
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-22 15:35+0000
PO-Revision-Date: 2018-12-10 21:57+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 .... _bpy.types.PointDensityTexture: Adds directed noise to the density at render time. Bộ Nhớ Đệm -- Cache Nguồn Màu Sắc -- Color Source Hằng Số/Đồng Đều/Bất Biến -- Constant Constant color Coordinate system to cache particles in. Data to derive the color results from. Density is constant within the look-up radius. Chiều/Độ Sâu -- Depth Vị Trí của Vật Thể Phát -- Emit Object Location Không Gian của Vật Thể Phát -- Emit Object Space Suy Giảm Dần -- Falloff Đồ Thị Giảm Dần -- Falloff Curve Không Gian Toàn Cầu -- Global Space Thời Gian Toàn Cầu -- Global Time Ảnh Hưởng -- Influence Level of detail in the added turbulent noise. Lifetime mapped as 0.0 - 1.0 intensity. Method for driving added turbulent noise. Multiplier to bring particle speed within an acceptable range. Cơ Sở Nhiễu -- Noise Basis Noise patterns will remain unchanged, faster and suitable for stills. Vật Thể -- Object Điểm Đỉnh của Vật Thể -- Object Vertices Object Vertices, Generate point density from an object's vertices. Object to take the point data from. Tùy Chọn -- Options Tuổi Thọ Hạt -- Particle Age -- Particle Color Sources Tốc Độ Hạt -- Particle Speed Hệ Thống Hạt -- Particle System Particle System, Generate point density from a particle system. Vận Tốc Hạt -- Particle Velocity Particle speed (absolute magnitude of velocity) mapped as 0.0 - 1.0 intensity. An additional color ramp can be used to convert intensity to RGB colors. Particle system to use. -- Point Data -- Point Density Texture Point Density panel. Point density renders a given point cloud (object vertices or particle system) as a 3D volume, using a user-defined radius for the points. Internally, the system uses a BVH data structure for fast range lookups. Bán Kính -- Radius Radius of the points. Phép Căn -- Root Tỷ Lệ -- Scale Scale of the turbulent noise. See :doc:`Here </editors/uv_image/uv/textures/types/procedural/introduction>`. Kích Thước -- Size Mịn Màng -- Smooth Mềm -- Soft Độ Xốp -- Softness Chuẩn -- Standard Tĩnh Tại -- Static Strength of the added turbulent noise. Hệ Thống -- System The rendered points are spherical by default, with various smooth falloff options, as well as simple Turbulence options for displacing the result with noise, adding fine detail. When using Point Density with a particle system, additional particle info such as particle velocity, age, and speed, can be visualized using a color/alpha ramp gradient. Hỗn Loạn -- Turbulence Cường độ Hỗn Loạn -- Turbulence Strength Turbulence panel. Turbulent noise driven by particle velocity. Turbulent noise driven by the global current frame. Turbulent noise driven by the particle's age between birth and death. Use a custom falloff. Use a vertex color layer for coloring the point density texture. Use a weights from a vertex group as intensity values. An additional color ramp can be used to convert intensity to RGB colors. Use object-space vertex normals as RGB values. Tỷ Lệ Vận Tốc -- Velocity Scale Màu Điểm Đỉnh -- Vertex Color -- Vertex Color Sources -- Vertex Normals Trọng Lượng Điểm Đỉnh -- Vertex Weight Vertex colors are defined per face corner. A single vertex can have as many different colors as faces it is part of. The actual color of the point density texture is averaged from all vertex corners. XYZ velocity mapped to RGB colors. 