��          �                 1     a  O     �  3   �  �   �     �  	   �     �               -  �   E  ^   �  A   :  T   |  �  �  1   �  a  �     	  3   2	  �   f	     _
     o
     �
     �
  5   �
     �
  �     ^   �  A     T   E   :menuselection:`Render --> Subsurface Scattering` For the effect to be efficient, samples needs to be coherent and not random. This can lead to cross shaped pattern when the scattering radius is high. Increasing the Jitter Threshold will rotate the samples below this radius percentage in a random pattern in order to hide the visible pattern. This affects performance if the scattering radius is large. Jitter Threshold Number of samples to compute the scattering effect. Output the albedo of a BSSRDF in a separate buffer in order to not blur it. The *Texture Blur* parameter require this option to be enable to work correctly. This option increases the video memory usage but does not have a big impact on performance. Panel Reference Samples Separate Albedo Subsurface Scattering Subsurface Translucency The Subsurface Translucency option needs to be enabled in order to make the light go through an object (like simulating a human ear lit from behind). This effect mimic real subsurface scattering by blurring the diffuse lighting in screen space. This option does only work if *Subsurface Scattering* is enabled. This option only works with shadowed light and does not work with indirect lighting. Project-Id-Version: Blender 2.80 Manual 2.80
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
 :menuselection:`Render --> Subsurface Scattering` For the effect to be efficient, samples needs to be coherent and not random. This can lead to cross shaped pattern when the scattering radius is high. Increasing the Jitter Threshold will rotate the samples below this radius percentage in a random pattern in order to hide the visible pattern. This affects performance if the scattering radius is large.  -- Jitter Threshold Number of samples to compute the scattering effect. Output the albedo of a BSSRDF in a separate buffer in order to not blur it. The *Texture Blur* parameter require this option to be enable to work correctly. This option increases the video memory usage but does not have a big impact on performance. Bảng -- Panel Tham Chiếu -- Reference Lượng Mẫu Vật -- Samples  -- Separate Albedo Tán Xạ Dưới Bề Mặt -- Subsurface Scattering -- Subsurface Translucency The Subsurface Translucency option needs to be enabled in order to make the light go through an object (like simulating a human ear lit from behind). This effect mimic real subsurface scattering by blurring the diffuse lighting in screen space. This option does only work if *Subsurface Scattering* is enabled. This option only works with shadowed light and does not work with indirect lighting. 