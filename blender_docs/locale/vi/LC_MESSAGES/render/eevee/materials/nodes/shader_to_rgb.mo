��          �               <  "   =     `     f  c   l  �   �  �   �  [   �     �     �  
             (     /     =  �   S     (  	   E  �  O  "        *     0  c   D  �   �  �   �  [   r	     �	     �	     �	     
     ,
     E
  5   W
  �   �
  "   b  "   �   (TODO 2.8 Example of Toon shading) Alpha Color Eevee supports the conversion of BSDF outputs into color inputs to make any kind of custom shading. For instance if you quantize the result of the ambient occlusion you will not get a fully quantized output but an accumulation of a noisy quantized output which may or may not converge to a smooth result. (TODO 2.8 Image) Here unpredictable means that it will not have the desired result. This might be the case if you use effects that need temporal accumulation to converge. Namely ambient occlusion, contact shadows, soft shadows, screen space refraction. If a Shader to RGB node is used, any upstream BSDF will invisible to the following effects: Inputs Outputs Properties Screen Space Reflection Shader Shader To RGB Subsurface Scattering This is supported using the Shader to RGB node. While this is supported, this is breaking the :abbr:`PBR (Physically Based Rendering)` pipeline and thus makes the result unpredictable when other effects are used. This node has no properties. Todo 2.8. Project-Id-Version: Blender 2.80 Manual 2.80
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-23 23:09-0500
PO-Revision-Date: 2018-12-04 21:09+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 (TODO 2.8 Example of Toon shading) Alpha Màu Sắc -- Color Eevee supports the conversion of BSDF outputs into color inputs to make any kind of custom shading. For instance if you quantize the result of the ambient occlusion you will not get a fully quantized output but an accumulation of a noisy quantized output which may or may not converge to a smooth result. (TODO 2.8 Image) Here unpredictable means that it will not have the desired result. This might be the case if you use effects that need temporal accumulation to converge. Namely ambient occlusion, contact shadows, soft shadows, screen space refraction. If a Shader to RGB node is used, any upstream BSDF will invisible to the following effects: Đầu Vào -- Inputs Đầu Ra -- Outputs Tính Chất -- Properties Screen Space Reflection Bộ Tô Bóng -- Shader  -- Shader To RGB Tán Xạ Dưới Bề Mặt -- Subsurface Scattering This is supported using the Shader to RGB node. While this is supported, this is breaking the :abbr:`PBR (Physically Based Rendering)` pipeline and thus makes the result unpredictable when other effects are used. Nút này không có tính chất. Nội dung cần viết thêm 2.8. 