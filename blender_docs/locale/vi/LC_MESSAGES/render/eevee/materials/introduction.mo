��          �                 �        �  ~   �  m   y  x   �     `     m     y  �   �     &  U   2  b   �  
   �  �  �       �  �  �   G     	  ~   8	  m   �	  x   %
     �
  #   �
     �
  �   �
     �  U   �  b        g  �  �     	   As of now, Bump mapping is supported using OpenGL derivatives which are the same for each block of 2x2 pixels. This means the bump output value will appear pixelated. It is recommended to use Normal mapping instead. Bump Due to realtime constraints, not all Cycles features are available in Eevee. See :doc:`/render/eevee/materials/nodes_support`. Eevee's materials system uses the same node based approach as :doc:`Cycles </render/cycles/materials/index>`. If you absolutely need to render using Bump nodes, render at twice the target resolution and downscale the final output. Introduction Limitations Nodes Support Object volume shaders will affect the whole bounding box of the object. The shape of the volume must be adjusted using procedural texturing inside the shader. Performance Performance is highly dependent on the number of BSDF nodes present in the node tree. Prefer using the Principled BSDF instead of multiple BSDF nodes because Eevee is optimized for it. Refraction Refraction is faked by sampling the same reflection probe used by the Glossy BSDFs, but using the refracted view direction instead of the reflected view direction. Only the first refraction event is modeled correctly. An approximation of the second refraction event can be used for relatively thin objects using Refraction Depth. Using Screen Space refraction will refract what is visible in. Volumes Objects Project-Id-Version: Blender 2.80 Manual 2.80
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-22 15:35+0000
PO-Revision-Date: 2018-12-07 01:52+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 As of now, Bump mapping is supported using OpenGL derivatives which are the same for each block of 2x2 pixels. This means the bump output value will appear pixelated. It is recommended to use Normal mapping instead. Độ Gồ Ghề -- Bump Due to realtime constraints, not all Cycles features are available in Eevee. See :doc:`/render/eevee/materials/nodes_support`. Eevee's materials system uses the same node based approach as :doc:`Cycles </render/cycles/materials/index>`. If you absolutely need to render using Bump nodes, render at twice the target resolution and downscale the final output. Giới Thiệu -- Introduction Những Giới Hạn -- Limitations -- Nodes Support Object volume shaders will affect the whole bounding box of the object. The shape of the volume must be adjusted using procedural texturing inside the shader. Hiệu Suất -- Performance Performance is highly dependent on the number of BSDF nodes present in the node tree. Prefer using the Principled BSDF instead of multiple BSDF nodes because Eevee is optimized for it. Khúc Xạ -- Refraction Refraction is faked by sampling the same reflection probe used by the Glossy BSDFs, but using the refracted view direction instead of the reflected view direction. Only the first refraction event is modeled correctly. An approximation of the second refraction event can be used for relatively thin objects using Refraction Depth. Using Screen Space refraction will refract what is visible in.  -- Volumes Objects 