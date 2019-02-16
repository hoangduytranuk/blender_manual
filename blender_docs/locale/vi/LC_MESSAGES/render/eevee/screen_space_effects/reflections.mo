��          �               �  4   �     �  B   �          '  �   =  K  �  �   >  �   �     q  7   }  /   �     �  	   �     �       |     m  �  l   �  .   e  	   �     �  �   �  �  f	  4        S  B   j     �     �  �   �  K  �  �   �  �   s  #     7   /  /   g     �     �     �     �  |   �  m  ]  l   �  .   8     g       �   �   :menuselection:`Render --> Screen Space Reflections` Clamp Clamp the reflected color intensity to remove noise and fireflies. Edge Fading Half Resolution Trace How thick to consider the pixels of the depth buffer during the tracing. Higher values will stretch the reflections and add flickering. Lower values may make the ray miss surfaces. If a *Reflection Plane* is near a reflective surface, it will be used as the source for tracing rays more efficiently and fix the partial visibility problem [TODO 2.8 image]. However, the reflected color will not contain the following effects: Subsurface scattering, volumetrics, screen space reflections, screen space refractions. If this effect is enabled, all Materials will use the depth buffer and the previous frame color to create more accurate reflection than reflection probes. Increase precision of the ray trace but introduce more noise and lower the maximum trace distance. Increased precision also increases performance cost. Limitations Only one glossy BSDF can emit screen space reflections. Only one refraction event is correctly modeled. Panel Reference Reflections Refractions Screen Space Reflections will reflect transparent object but without accurate positioning due to the one layer depth buffer. Screen space refractions work the same way as screen space reflections and use same parameters. But they are not enabled by default on all surfaces. Enabling it will have a small performance cost. You need to enable them in :menuselection:`Material Properties --> Options`. Materials using screen space refractions will not be able to cast screen space reflections. Smoothly fade out the reflected pixels if they are close to a screen edge. The unit is in screen percentage. The chosen BSDF is currently arbitrary chosen. Thickness Trace Precision Use half resolution ray tracing. Only cast a ray for every fourth pixels. Enabling this option reduces drastically video memory usage and increase performances at the cost of quality. Project-Id-Version: Blender 2.80 Manual 2.80
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-24 23:43+0000
PO-Revision-Date: 2018-12-07 01:52+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 :menuselection:`Render --> Screen Space Reflections` Hạn Định -- Clamp Clamp the reflected color intensity to remove noise and fireflies.  -- Edge Fading  -- Half Resolution Trace How thick to consider the pixels of the depth buffer during the tracing. Higher values will stretch the reflections and add flickering. Lower values may make the ray miss surfaces. If a *Reflection Plane* is near a reflective surface, it will be used as the source for tracing rays more efficiently and fix the partial visibility problem [TODO 2.8 image]. However, the reflected color will not contain the following effects: Subsurface scattering, volumetrics, screen space reflections, screen space refractions. If this effect is enabled, all Materials will use the depth buffer and the previous frame color to create more accurate reflection than reflection probes. Increase precision of the ray trace but introduce more noise and lower the maximum trace distance. Increased precision also increases performance cost. Những Giới Hạn -- Limitations Only one glossy BSDF can emit screen space reflections. Only one refraction event is correctly modeled. Bảng -- Panel Tham Chiếu -- Reference -- Reflections  -- Refractions Screen Space Reflections will reflect transparent object but without accurate positioning due to the one layer depth buffer. Screen space refractions work the same way as screen space reflections and use same parameters. But they are not enabled by default on all surfaces. Enabling it will have a small performance cost. You need to enable them in :menuselection:`Material Properties --> Options`. Materials using screen space refractions will not be able to cast screen space reflections. Smoothly fade out the reflected pixels if they are close to a screen edge. The unit is in screen percentage. The chosen BSDF is currently arbitrary chosen. Độ Dày -- Thickness  -- Trace Precision Use half resolution ray tracing. Only cast a ray for every fourth pixels. Enabling this option reduces drastically video memory usage and increase performances at the cost of quality. 