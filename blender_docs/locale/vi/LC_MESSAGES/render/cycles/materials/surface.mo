��          �               <  �  =     �     �  �   �  >   r  N   �  �     f   �  �    
   �  
   �  	   �  x   �     [     d  �   p     ^	  �  k	  �  #     �     �  �   �  >   \  N   �  �  �  f   �  �  �     �     �     �  x   �     q     �  �   �     �   A major difference from non-physically-based renderers is that direct light reflection from lamps and indirect light reflection of other surfaces are not decoupled, but rather handled using a single :abbr:`BSDF (Bidirectional scattering distribution function)`. This limits the possibilities a bit, but we believe overall it is helpful in creating consistent-looking renders with fewer parameters to tune. BSDF BSDF Parameters BSDFs are a type of *Transmission*, transmitting an incoming ray and changing its direction as it exits on the other side of the surface. BSDFs reflect an incoming ray on the same side of the surface. BSDFs transmit an incoming ray through the surface, leaving on the other side. Currently Blender is coded to use an unsquared model. So if you are using a :term:`Roughness Map` chances are that the result will not be accurate. To fix this, you can square the texture by connecting the texture to a :doc:`Math node </render/cycles/nodes/types/converter/math>` and either setting it to *Multiply* and inputing the texture in both input sockets, or using the *Power* function and setting the second input to 2. Emission defines how light is emitted from the surface, allowing any surface to become a light source. For the glossy :abbr:`BSDF (Bidirectional scattering distribution function)`\ s, the *roughness* parameter controls the sharpness of the reflection, from 0.0 (perfectly sharp) to 1.0 (very soft). Compared to *hardness* or *exponent* parameters, it has the advantage of being in the range 0.0 to 1.0, and as a result gives more linear control and is more easily textureable. The relation is roughly: *roughness* = 1 - 1/*hardness* Reflection Refraction Roughness Stands for Bidirectional Scattering Distribution Function. It defines how light is reflected and refracted at a surface. Surfaces Terminology The surface shader defines the light interaction at the surface of the mesh. One or more :abbr:`BSDF (Bidirectional scattering distribution function)`\ 's specify if incoming light is reflected back, refracted into the mesh, or absorbed. Transmission Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-12-04 21:09+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 A major difference from non-physically-based renderers is that direct light reflection from lamps and indirect light reflection of other surfaces are not decoupled, but rather handled using a single :abbr:`BSDF (Bidirectional scattering distribution function)`. This limits the possibilities a bit, but we believe overall it is helpful in creating consistent-looking renders with fewer parameters to tune. BSDF  -- BSDF Parameters BSDFs are a type of *Transmission*, transmitting an incoming ray and changing its direction as it exits on the other side of the surface. BSDFs reflect an incoming ray on the same side of the surface. BSDFs transmit an incoming ray through the surface, leaving on the other side. Currently Blender is coded to use an unsquared model. So if you are using a :term:`Roughness Map` chances are that the result will not be accurate. To fix this, you can square the texture by connecting the texture to a :doc:`Math node </render/cycles/nodes/types/converter/math>` and either setting it to *Multiply* and inputing the texture in both input sockets, or using the *Power* function and setting the second input to 2. Emission defines how light is emitted from the surface, allowing any surface to become a light source. For the glossy :abbr:`BSDF (Bidirectional scattering distribution function)`\ s, the *roughness* parameter controls the sharpness of the reflection, from 0.0 (perfectly sharp) to 1.0 (very soft). Compared to *hardness* or *exponent* parameters, it has the advantage of being in the range 0.0 to 1.0, and as a result gives more linear control and is more easily textureable. The relation is roughly: *roughness* = 1 - 1/*hardness* Phản Quang -- Reflection Khúc Xạ -- Refraction Độ Ráp -- Roughness Stands for Bidirectional Scattering Distribution Function. It defines how light is reflected and refracted at a surface. Bề Mặt -- Surfaces  -- Terminology The surface shader defines the light interaction at the surface of the mesh. One or more :abbr:`BSDF (Bidirectional scattering distribution function)`\ 's specify if incoming light is reflected back, refracted into the mesh, or absorbed. Truyền Xạ -- Transmission 