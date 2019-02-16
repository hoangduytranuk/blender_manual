��    J      l              �  �   �  �   N  w     Y   �     �     �  f       j  
   o  ]   z  "  �     �	  	   
     
     )
  �   >
  .   �
  (   �
  1        M     m     z  f   �     �     �     �  %   �     %  w   ,     �     �  �   �  R   y  <   �     	     !  �   (     �     �     �  
     q       �  3   �  @   �  	              7  
   =  U   H  R   �     �     �       
         +     <     N  !   `  �   �     4  �  <  �       �  c   �  �        �     �  ]   �  H   F  %   �      �  "   �  �  �  �   �  �   B  w     Y   |     �  2   �  f  &     �     �  ]   �  "       /      B   8   `      �   �   �   .   7!  (   f!  1   �!     �!     �!     �!  f   "  	   "     �"  "   �"  %   �"     �"  w   �"     d#     {#  �   �#  R   G$  <   �$     �$     �$  �   %     �%  %   �%     &     &  q  4&  +   �'  3   �'  @   (     G(      _(     �(  +   �(  U   �(  R   )     j)  .   �)  '   �)      �)  +   �)  6   &*  >   ]*  !   �*  �   �*     p+  �  �+  �   e-    �-  c   �.  �   Y/     0  =   00  ]   n0  H   �0  %   1      ;1  "   \1   A method that is faster than *Multiple-scattering GGX* but is less physically accurate. Selecting it enables the *Transmission Roughness* input. Amount of anisotropy for specular reflection. Higher values give elongated highlights along the tangent direction; negative values give highlights shaped perpendicular to the tangent direction. Amount of dielectric specular reflection. Specifies facing (along normal) reflectivity in the most common 0 - 8% range. Amount of soft velvet like reflection near edges, for simulating materials such as cloth. Anisotropic Anisotropic Rotation Average distance that light scatters below the surface. Higher radius gives a softer appearance, as light bleeds into shadows and through the object. The scattering distance is specified separately for the RGB channels, to render materials such as skin where red light scatters deeper. The X, Y and Z values are mapped to the R, G and B values, respectively. BSDF Base Color Below are some examples of how all the Principled BSDF's parameters interact with each other. Blends between a non-metallic and metallic material model. A value of 1.0 gives a fully specular reflection tinted with the base color, without diffuse reflection or transmission. At 0.0 the material consists of a diffuse or transmissive base layer, with a specular reflection layer on top. Christensen-Burley Clearcoat Clearcoat Normal Clearcoat Roughness: Compared to the *Anisotropic BSDF* node, the direction of highlight elongation is rotated by 90°. Add 0.25 to the value to correct. Controls the normals of the *Clearcoat* layer. Controls the normals of the base layers. Controls the tangent for the *Anisotropic* layer. Diffuse or metal surface color. Distribution Examples Extra white specular layer on top of others. This is useful for materials like car paint and the like. For example: GGX IOR Index of refraction for transmission. Inputs Is an approximation to physically-based volume scattering. Gives less blurry results than Cubic and Gaussian functions. Metallic Microfacet distribution to use. Mix between diffuse and subsurface scattering. Rather than being a simple mix between Diffuse and Subsurface Scattering, it acts as a multiplier for the Subsurface Radius. Mix between fully opaque surface at zero and fully glass like transmission at one. Mix between white and using base color for sheen reflection. Multiple-scattering GGX Normal Normal dielectrics have colorless reflection, so this parameter is not technically physically correct and is provided for faking the appearance of materials with complex surface structure. Outputs Principled BSDF Principled BSDF. Properties Provides the most accurate results for thin and curved objects. This comes at the cost of increased render time or noise for more dense media like skin, but also better geometry detail preservation. Random Walk uses true volumetric scattering inside the mesh, which means that it works best for closed meshes. Overlapping faces and holes in the mesh can cause problems. Random Walk Rendering method to simulate subsurface scattering. Rotates the direction of anisotropy, with 1.0 going full circle. Roughness Roughness of clearcoat specular. Sheen Sheen Tint Since materials with reflectivity above 8% do exist, the field allows values above 1. Specifies microfacet roughness of the surface for diffuse and specular reflection. Specular Specular Tint Standard shader output. Subsurface Subsurface Color Subsurface Method Subsurface Radius Subsurface scattering base color. Takes multiple bounce (scattering) events between microfacets into account. This gives a more energy conserving results, which would otherwise be visible as excessive darkening. Tangent The *Principled* :abbr:`BSDF (Bidirectional scattering distribution function)` that combines multiple layers into a single easy to use node. It is based on the Disney principled model also known as the "PBR" shader, making it compatible with other software such as Pixar's Renderman\ :sup:`®` and Unreal Engine\ :sup:`®`. Image textures painted or baked from software like Substance Painter\ :sup:`®` may be directly linked to the corresponding parameters in this shader. The emphasis on compatibility with other software means that it interprets certain input parameters differently from older Blender nodes. This "Uber" shader includes multiple layers to create a wide variety of materials. The base layer is a user controlled mix between diffuse, metal, subsurface scattering and transmission. On top of that there is a specular layer, sheen layer and clearcoat layer. Tints the facing specular reflection using the base color, while glancing reflection remains white. To compute this value for a realistic material with a known index of refraction, you may use this special case of the Fresnel formula: :math:`specular = ((ior - 1)/(ior + 1))^2 / 0.08` Transmission Transmission Roughness When converting from the older *Glossy BSDF* node, use the square root of the original value. With **GGX** distribution controls roughness used for transmitted light. diamond: ior = 2.417, specular = 2.15 glass: ior = 1.5, specular = 0.5 water: ior = 1.33, specular = 0.25 Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-17 22:20+0000
PO-Revision-Date: 2018-12-07 01:52+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 A method that is faster than *Multiple-scattering GGX* but is less physically accurate. Selecting it enables the *Transmission Roughness* input. Amount of anisotropy for specular reflection. Higher values give elongated highlights along the tangent direction; negative values give highlights shaped perpendicular to the tangent direction. Amount of dielectric specular reflection. Specifies facing (along normal) reflectivity in the most common 0 - 8% range. Amount of soft velvet like reflection near edges, for simulating materials such as cloth. Dị Hướng -- Anisotropic Xoay Chiều Dị Hướng -- Anisotropic Rotation Average distance that light scatters below the surface. Higher radius gives a softer appearance, as light bleeds into shadows and through the object. The scattering distance is specified separately for the RGB channels, to render materials such as skin where red light scatters deeper. The X, Y and Z values are mapped to the R, G and B values, respectively. BSDF Màu Cơ Sở -- Base Color Below are some examples of how all the Principled BSDF's parameters interact with each other. Blends between a non-metallic and metallic material model. A value of 1.0 gives a fully specular reflection tinted with the base color, without diffuse reflection or transmission. At 0.0 the material consists of a diffuse or transmissive base layer, with a specular reflection layer on top. Christensen-Burley Lớp Sơn Bóng -- Clearcoat Pháp Tuyến của Lớp Sơn Bóng -- Clearcoat Normal  -- Clearcoat Roughness: Compared to the *Anisotropic BSDF* node, the direction of highlight elongation is rotated by 90°. Add 0.25 to the value to correct. Controls the normals of the *Clearcoat* layer. Controls the normals of the base layers. Controls the tangent for the *Anisotropic* layer. Diffuse or metal surface color. Phân Phối -- Distribution Các Ví Dụ -- Examples Extra white specular layer on top of others. This is useful for materials like car paint and the like. Ví dụ: GGX Chỉ Số Khúc Xạ (IOR) -- IOR Index of refraction for transmission. Đầu Vào -- Inputs Is an approximation to physically-based volume scattering. Gives less blurry results than Cubic and Gaussian functions. Kim Loại -- Metallic Microfacet distribution to use. Mix between diffuse and subsurface scattering. Rather than being a simple mix between Diffuse and Subsurface Scattering, it acts as a multiplier for the Subsurface Radius. Mix between fully opaque surface at zero and fully glass like transmission at one. Mix between white and using base color for sheen reflection. -- Multiple-scattering GGX Pháp Tuyến/B.Thg -- Normal Normal dielectrics have colorless reflection, so this parameter is not technically physically correct and is provided for faking the appearance of materials with complex surface structure. Đầu Ra -- Outputs BSDF Nguyên Tắc -- Principled BSDF Principled BSDF. Tính Chất -- Properties Provides the most accurate results for thin and curved objects. This comes at the cost of increased render time or noise for more dense media like skin, but also better geometry detail preservation. Random Walk uses true volumetric scattering inside the mesh, which means that it works best for closed meshes. Overlapping faces and holes in the mesh can cause problems. Tiến Bước Ngẫu Nhiên -- Random Walk Rendering method to simulate subsurface scattering. Rotates the direction of anisotropy, with 1.0 going full circle. Độ Ráp -- Roughness Roughness of clearcoat specular. Bóng Bảy -- Sheen Sắc Thái của Bóng Bảy -- Sheen Tint Since materials with reflectivity above 8% do exist, the field allows values above 1. Specifies microfacet roughness of the surface for diffuse and specular reflection. Lóng Lánh -- Specular Sắc Thái của Lóng Lánh -- Specular Tint Đầu ra chuẩn của bộ tô bóng. Dưới Bề Mặt -- Subsurface Màu Dưới Bề Mặt -- Subsurface Color Phương Pháp Dưới Bề Mặt -- Subsurface Method Bán Kính của Lớp Dưới Bề Mặt -- Subsurface Radius Subsurface scattering base color. Takes multiple bounce (scattering) events between microfacets into account. This gives a more energy conserving results, which would otherwise be visible as excessive darkening. Tiếp Tuyến -- Tangent The *Principled* :abbr:`BSDF (Bidirectional scattering distribution function)` that combines multiple layers into a single easy to use node. It is based on the Disney principled model also known as the "PBR" shader, making it compatible with other software such as Pixar's Renderman\ :sup:`®` and Unreal Engine\ :sup:`®`. Image textures painted or baked from software like Substance Painter\ :sup:`®` may be directly linked to the corresponding parameters in this shader. The emphasis on compatibility with other software means that it interprets certain input parameters differently from older Blender nodes. This "Uber" shader includes multiple layers to create a wide variety of materials. The base layer is a user controlled mix between diffuse, metal, subsurface scattering and transmission. On top of that there is a specular layer, sheen layer and clearcoat layer. Tints the facing specular reflection using the base color, while glancing reflection remains white. To compute this value for a realistic material with a known index of refraction, you may use this special case of the Fresnel formula: :math:`specular = ((ior - 1)/(ior + 1))^2 / 0.08` Truyền Xạ -- Transmission Độ Ráp trong Sự Truyền Xạ -- Transmission Roughness When converting from the older *Glossy BSDF* node, use the square root of the original value. With **GGX** distribution controls roughness used for transmitted light. diamond: ior = 2.417, specular = 2.15 glass: ior = 1.5, specular = 0.5 water: ior = 1.33, specular = 0.25 