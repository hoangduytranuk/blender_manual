��    #      4              L     M  ;   T  <   �  ;   �  ?   	  ;   I  =   �  A   �       B        V     c     j     x     �     �     �     �     �     �     �  h   �     c  y   k  
   �  	   �  
   �  �     :   �  *  �          +     H     [  �  m     %
  ;   C
  <   
  ;   �
  ?   �
  ;   8  =   t  A   �  /   �  B   $  1   g     �  #   �  #   �      �  $         =  !   ^  '   �  6   �     �  h   �     Y  y   n     �  !     )   %  �   O  :   �  *  1  !   \  ,   ~  -   �  1   �   (Todo) 1.0 if shading is executed for a camera ray, 0.0 otherwise. 1.0 if shading is executed for a diffuse ray, 0.0 otherwise. 1.0 if shading is executed for a glossy ray, 0.0 otherwise. 1.0 if shading is executed for a reflection ray, 0.0 otherwise. 1.0 if shading is executed for a shadow ray, 0.0 otherwise. 1.0 if shading is executed for a singular ray, 0.0 otherwise. 1.0 if shading is executed for a transmission ray, 0.0 otherwise. Diffuse Depth Distance traveled by the light ray from the last bounce or camera. Glossy Depth Inputs Is Camera Ray Is Diffuse Ray Is Glossy Ray Is Reflection Ray Is Shadow Ray Is Singular Ray Is Transmission Ray Light Path Node Light Path Node. Number of times the ray has "bounced", i.e. been reflected or transmitted on interaction with a surface. Outputs Passing through a transparent shader :ref:`does not count as a normal "bounce" <render-cycles-light-paths-transparency>`. Properties Ray Depth Ray Length Replace a Transmission light path after X bounces with another shader, e.g. a Diffuse one. This can be used to avoid black surfaces, due to low amount of max bounces. Returns the number of transparent surfaces passed through. The *Light Path* node is used to find out for which kind of incoming ray the shader is being executed; particularly useful for non-physically-based tricks. More information about the meaning of each type is in the :doc:`Light Paths </render/cycles/settings/scene/render/light_paths>` documentation. This node has no inputs. This node has no properties. Transmission Depth Transparent Depth Project-Id-Version: Blender 2.79 Manual 2.79
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
 Nội dung cần viết thêm 1.0 if shading is executed for a camera ray, 0.0 otherwise. 1.0 if shading is executed for a diffuse ray, 0.0 otherwise. 1.0 if shading is executed for a glossy ray, 0.0 otherwise. 1.0 if shading is executed for a reflection ray, 0.0 otherwise. 1.0 if shading is executed for a shadow ray, 0.0 otherwise. 1.0 if shading is executed for a singular ray, 0.0 otherwise. 1.0 if shading is executed for a transmission ray, 0.0 otherwise. Độ Sâu của Khuếch Tán -- Diffuse Depth Distance traveled by the light ray from the last bounce or camera. Độ Sâu của Ánh Bóng Bẩy -- Glossy Depth Đầu Vào -- Inputs Tia Máy Quay Phim -- Is Camera Ray Tia Khuếch Tán -- Is Diffuse Ray Tia Bóng Bẩy -- Is Glossy Ray Tia Phản Xạ -- Is Reflection Ray Tia Bóng Tối -- Is Shadow Ray Tia Lập Dị -- Is Singular Ray Tia Lan Truyền -- Is Transmission Ray Nút Đường Đi của Ánh Sáng -- Light Path Node Light Path Node. Number of times the ray has "bounced", i.e. been reflected or transmitted on interaction with a surface. Đầu Ra -- Outputs Passing through a transparent shader :ref:`does not count as a normal "bounce" <render-cycles-light-paths-transparency>`. Tính Chất -- Properties Độ Sâu của Tia -- Ray Depth Chiều Dài của Tia Xạ -- Ray Length Replace a Transmission light path after X bounces with another shader, e.g. a Diffuse one. This can be used to avoid black surfaces, due to low amount of max bounces. Returns the number of transparent surfaces passed through. The *Light Path* node is used to find out for which kind of incoming ray the shader is being executed; particularly useful for non-physically-based tricks. More information about the meaning of each type is in the :doc:`Light Paths </render/cycles/settings/scene/render/light_paths>` documentation. Nút này không có đầu vào. Nút này không có tính chất nào cả. Độ Sâu Lan Truyền -- Transmission Depth Độ Sâu của Độ Trong -- Transparent Depth 