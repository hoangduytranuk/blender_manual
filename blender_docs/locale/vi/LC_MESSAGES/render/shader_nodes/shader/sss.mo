��          �               l  Y   m     �     �  j   �     ?     E     N  }  W     �  \   �     9     @  T   G     �  
   �     �     �  	   �     �     �  �  �  Y   �  
   �       �        �     �     �  }  �     `	  \   v	     �	     �	  �   
     �
     �
     �
     �
     �
  5     (   I   :abbr:`BSSRDF (Bidirectional subsurface scattering distribution function)` shader output. BSSRDF Color Color of the surface, or physically speaking, the probability that light is reflected for each wavelength. Cubic Examples Gaussian Gives a smoother falloff following a normal distribution, which is particularly useful for more advanced materials that use measured data that was fitted to one or more such Gaussian functions. The function is :math:`e^{-8x^2/ radius^2}`, such that the radius roughly matches the maximum falloff distance. To match a given measured variance *v*, set :math:`radius = sqrt(16 × v)`. Inputs Is a sharp falloff useful for many simple materials. The function is :math:`(radius - x)^3`. Method Normal Normal used for shading; if nothing is connected the default shading normal is used. Outputs Properties Radius Scale Sharpness Subsurface Scattering Texture Blur Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-06-12 16:58+0200
PO-Revision-Date: 2019-04-24 02:16+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 :abbr:`BSSRDF (Bidirectional subsurface scattering distribution function)` shader output.  -- BSSRDF Màu Sắc -- Color Về màu sắc của bề mặt, hoặc về thể chất mà nói, xác suất ánh sáng được phản xạ cho mỗi bước sóng. Lập Phương -- Cubic Ví Dụ -- Examples Gaus -- Gaussian Gives a smoother falloff following a normal distribution, which is particularly useful for more advanced materials that use measured data that was fitted to one or more such Gaussian functions. The function is :math:`e^{-8x^2/ radius^2}`, such that the radius roughly matches the maximum falloff distance. To match a given measured variance *v*, set :math:`radius = sqrt(16 × v)`. Đầu Vào -- Inputs Is a sharp falloff useful for many simple materials. The function is :math:`(radius - x)^3`. Phương Pháp -- Method Pháp Tuyến -- Normal Pháp tuyến sử dụng cho việc tô bóng; nếu không có gì kết nối thì pháp tuyến tô bóng mặc định sẽ được sử dụng. Đầu Ra -- Outputs Tính Chất -- Properties Bán Kính -- Radius Tỷ Lệ -- Scale Độ Sắc/Nhọn -- Sharpness Tán Xạ Dưới Bề Mặt -- Subsurface Scattering Làm Nhòe Chất Liệu -- Texture Blur 