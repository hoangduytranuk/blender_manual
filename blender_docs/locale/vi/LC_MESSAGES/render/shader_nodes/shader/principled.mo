��    $      <              \  w   ]  
   �  	   �     �     �               &     3     7     >     G     _     f     n  
   ~     �  	   �     �  
   �  U   �                 
   5     @     Q     c     u  �  }  �   X       %         D  "   e  �  �  w   6	     �	     �	  8   �	     !
     9
     V
  	   k
  "   u
     �
     �
     �
     �
     �
  %        3  +   N     z     �  +   �  U   �     )  .   A  '   p      �  +   �  6   �  >        [  �  u  �   P     	  %   '      M  "   n   Amount of dielectric specular reflection. Specifies facing (along normal) reflectivity in the most common 0 - 8% range. Base Color Clearcoat Clearcoat Normal Clearcoat Roughness: Distribution Examples For example: IOR Inputs Metallic Multiple-scattering GGX Normal Outputs Principled BSDF Properties Random Walk Roughness Sheen Sheen Tint Since materials with reflectivity above 8% do exist, the field allows values above 1. Specular Specular Tint Standard shader output. Subsurface Subsurface Color Subsurface Method Subsurface Radius Tangent The *Principled* :abbr:`BSDF (Bidirectional scattering distribution function)` that combines multiple layers into a single easy to use node. It is based on the Disney principled model also known as the "PBR" shader, making it compatible with other software such as Pixar's Renderman\ :sup:`®` and Unreal Engine\ :sup:`®`. Image textures painted or baked from software like Substance Painter\ :sup:`®` may be directly linked to the corresponding parameters in this shader. To compute this value for a realistic material with a known index of refraction, you may use this special case of the Fresnel formula: :math:`specular = ((ior - 1)/(ior + 1))^2 / 0.08` Transmission diamond: ior = 2.417, specular = 2.15 glass: ior = 1.5, specular = 0.5 water: ior = 1.33, specular = 0.25 Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-06-21 14:24+1000
PO-Revision-Date: 2020-02-26 21:13+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@gmail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@gmail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 Amount of dielectric specular reflection. Specifies facing (along normal) reflectivity in the most common 0 - 8% range. Màu Cơ Sở -- Base Color Lớp Sơn Bóng -- Clearcoat Pháp Tuyến của Lớp Sơn Bóng -- Clearcoat Normal -- Clearcoat Roughness: Phân Phối -- Distribution Ví Dụ -- Examples Ví dụ: Chỉ Số Khúc Xạ (IOR) -- IOR Đầu Vào -- Inputs Kim Loại -- Metallic -- Multiple-scattering GGX Pháp Tuyến -- Normal Đầu Ra -- Outputs BSDF Nguyên Tắc -- Principled BSDF Tính Chất -- Properties Tiến Bước Ngẫu Nhiên -- Random Walk Độ Ráp -- Roughness Bóng Bảy -- Sheen Sắc Thái của Bóng Bảy -- Sheen Tint Since materials with reflectivity above 8% do exist, the field allows values above 1. Lóng Lánh -- Specular Sắc Thái của Lóng Lánh -- Specular Tint Đầu ra chuẩn của bộ tô bóng. Dưới Bề Mặt -- Subsurface Màu Dưới Bề Mặt -- Subsurface Color Phương Pháp Dưới Bề Mặt -- Subsurface Method Bán Kính của Lớp Dưới Bề Mặt -- Subsurface Radius Tiếp Tuyến -- Tangent The *Principled* :abbr:`BSDF (Bidirectional scattering distribution function)` that combines multiple layers into a single easy to use node. It is based on the Disney principled model also known as the "PBR" shader, making it compatible with other software such as Pixar's Renderman\ :sup:`®` and Unreal Engine\ :sup:`®`. Image textures painted or baked from software like Substance Painter\ :sup:`®` may be directly linked to the corresponding parameters in this shader. To compute this value for a realistic material with a known index of refraction, you may use this special case of the Fresnel formula: :math:`specular = ((ior - 1)/(ior + 1))^2 / 0.08` Truyền Xạ -- Transmission diamond: ior = 2.417, specular = 2.15 glass: ior = 1.5, specular = 0.5 water: ior = 1.33, specular = 0.25 