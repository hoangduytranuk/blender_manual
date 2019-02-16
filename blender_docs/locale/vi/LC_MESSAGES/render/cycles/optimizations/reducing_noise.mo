��    :      �              �  �   �  �  t  z   r     �     �  |       �     �  �  �     w
     �
  	   �
  d  �
           +      L  �   m     $     9     W  �  e  2      9  �  O    �      �     �       �            $     =     U     c     o     �     �     �     �  R   �       �  5  �    
   �  �  �  O  q    �  �   �     �   $   �      �   <  �"  �  <$     �%     �%  �  &  �  �'  �  �)  �   Q+  �  ,  z   .     �.     �.  |  �.     =0     P0  �  d0     +2     >2     P2  d  k2     �3      �3      4  �   24     �4  !   �4      5  �  .5  2  �6    8  �  9    �:      �<  ,   �<     �<  �  �<      �>     ?     -?     E?     S?     _?     w?  !   �?     �?     �?  R   �?     %@  �  >@  �  B  
   �C  �  �C  O  zE    �F  �   �G     �H  $   �H     I  <  K  �  EL     �M     �M  �  N  �  �O   Above we can see the node setup used for the glass transparency trick; on the left the render has too much shadow due to missing caustics, and on the right the render with the trick. Also important is to use shader colors that do **not** have components of value 1.0 or values near that; try to keep the maximum value to 0.8 or less and make your lights brighter. In reality, surfaces are rarely perfectly reflecting all light, but there are of course exceptions; usually glass will let most light through, which is why we need more bounces there. High values for the color components tend to introduce noise because light intensity then does not decrease much as it bounces off each surface. Below is an example render by `The Pixelary <http://blog.thepixelary.com/post/160451378592/denoising-in-cycles-tested>`__. Bounces Caustics and Filter Glossy Caustics are a well-known source of noise, causing fireflies. They happen because the renderer has difficulty finding specular highlights viewed through a soft glossy or diffuse reflection. There is a :ref:`No Caustics <render-cycles-integrator-no-caustics>` option to disable glossy behind a diffuse reflection entirely. Many renderers will typically disable caustics by default. Caustics disabled. Clamp Fireflies Cycles uses path tracing with next event estimation, which is not good at rendering all types of light effects, like caustics, but has the advantage of being able to render more detailed and larger scenes compared to some other rendering algorithms. This is because we do not need to store, for example, a photon map in memory, and because we can keep rays relatively coherent to use an on-demand image cache, compared to e.g. bidirectional path tracing. Default Glas BSDF. Default settings. Denoising Even with all the settings described above there will always end up being some render noise no matter how many samples you use. To fix this there is a post-processing technique to cleanup the final bit of noise. To use this enable :doc:`Denoising </render/cycles/settings/scene/render_layers/denoising>` in the *Render Layers* tab of the Properties editor. Example render after denoising. Example render before denoising. Filter Glossy greater than zero. For more details, see the :doc:`Light Paths </render/cycles/settings/scene/render/light_paths>` and :doc:`Integrator </render/cycles/settings/scene/render/integrator>` documentation. Four bounces at max. Glass and Transparent Shadows Hard Falloff. However, using No Caustics will result in missing light, and it still does not cover the case where a sharp glossy reflection is viewed through a soft glossy reflection. There is a :ref:`Filter Glossy <render-cycles-integrator-filter-glossy>` option to reduce the noise from such cases at the cost of accuracy. This will blur the sharp glossy reflection to make it easier to find, by increasing the shader Roughness. Ideally with all the previous tricks, fireflies would be eliminated, but they could still happen. For that, the *intensity* that any individual light ray sample will contribute to a pixel can be *clamped* to a maximum value with the integrator :ref:`Clamp setting <render-cycles-integrator-clamp-samples>`. If set too low this can cause missing highlights in the image, which might be useful to preserve for camera effects such as bloom or glare. To mitigate this conundrum it's often useful to clamp only indirect bounces, leaving highlights directly visible to the camera untouched. In reality light in a vacuum will always fall off at a rate of 1/(distance^2). However, as distance goes to zero, this value goes to infinity and we can get very bright spots in the image. These are mostly a problem for indirect lighting, where the probability of hitting such a small but extremely bright spot is low and so happens only rarely. This is a typical recipe for fireflies. In reality light will bounce a huge number of times due to the speed of light being very high. In practice more bounces will introduce more noise, and it might be good to use something like the Limited Global Illumination preset in the :ref:`Light Paths <render-cycles-integrator-light-paths>` Section that uses *fewer* bounces for different shader types. Diffuse surfaces typically can get away with fewer bounces, while glossy surfaces need a few more, and transmission shaders such as glass usually need the most. Irradiance at the shading point. Light Falloff Light Portals Materials with emission shaders can be configured to use Multiple Importance Sampling (:doc:`/render/cycles/materials/settings`). This means that they will get rays sent directly towards them, rather than ending up there based on rays randomly bouncing around. For very bright mesh light sources, this can reduce noise significantly. However, when the emission is not particularly bright, this will take samples away from other brighter light sources for which it is important to find them this way. Multiple Importance Sampling Multiple Importance off. Multiple Importance on. No Clamp (0). No bounces. Optimized Glass Shader. Optimized glass shader. Path Tracing Reducing Noise Soft Falloff. The above images show default settings, no caustics, and filter glossy set to 1.0. The detected highlights. The lamp is a known light source, so its location is already known, but the glossy highlight(s) that it causes are a different matter. The best we can do with path tracing is to distribute light rays randomly over the hemisphere, hoping to find all the important bright spots. If for some pixels we miss some bright spot, but we do find it for another, that results in noise. The more samples we take, the higher the probability that we cover all the important sources of light. The optimal setting here is difficult to guess; it may be a matter of trial and error, but often it is clear that a somewhat glowing object may be only contributing light locally, while a mesh light used as a lamp would need this option enabled. Here is an example where the emissive spheres contribute little to the lighting, and the image renders with slightly less noise by disabling Multiple Importance on them. The scene. The world background also has a *Multiple Importance* (:ref:`render-cycles-integrator-world-settings`) option. This is mostly useful for environment maps that have small bright spots in them, rather than being smooth. This option will then, in a preprocess, determine the bright spots, and send light rays directly towards them. Again, enabling this option may take samples away from more important light sources if it is not needed. To find the light that is reflected from this surface, we need to find the average color from all these pixels. Note the glossy highlight on the sphere, and the bright spot the lamp casts on the nearby wall. These hotspots are 100x brighter than other parts of the image and will contribute significantly to the lighting of this pixel. To reduce this problem, the :doc:`Light Falloff </render/cycles/nodes/types/color/light_falloff>` node has a *Smooth factor*, that can be used to reduce the maximum intensity a light can contribute to nearby surfaces. The images above show default falloff and smooth value 1.0. To understand where noise can come from, take for example the scene below. When we trace a light ray into the location marked by the white circle on a red dot, the second image below gives an impression of what the diffuse shader "sees". Two bounces at max. Using Glossy Filter & Light Falloff. We do the inverse of what reality does, tracing light rays from the camera into the scene and onto lights, rather than from the light sources into the scene and then into the camera. This has the advantage that we do not waste light rays that will not end up in the camera, but also means that it is difficult to find some light paths that may contribute a lot. Light rays will be sent either according to the surface BRDF, or in the direction of known light sources (lamps, emitting meshes with Sample as Lamp). When performing a final render, it is important to reduce noise as much as possible. Here we will discuss a number of tricks that, while breaking the laws of physics, are particularly important when rendering animations within a reasonable time. Click to enlarge the example images to see the noise differences well. When rendering a daylight indoor scene where most of the light is coming in through a window or door opening, it is difficult for the integrator to find its way to them. To fix this, use :ref:`Light Portals <render-cycles-lamps-area-portals>`, these work by adding an :ref:`Area Lamp <render-cycles-lamps-area>`. You then will need to modify its shape to match that of the opening that you are trying to fill. Where Noise Comes From With Clamp set to 4. With caustics disabled, glass will miss shadows, and with filter glossy they might be too soft. We can make a glass shader that will use a Glass BSDF when viewed *directly*, and a Transparent BSDF when viewed *indirectly*. The Transparent BSDF can be used for transparent shadows to find light sources straight through surfaces, and will give properly-colored shadows, but without the caustics. The Light Path node is used to determine when to use which of the two shaders. With some tricks we can reduce this noise. If we blur the bright spots, they become bigger and less intense, making them easier to find and less noisy. This will not give the same exact result, but often it's close enough when viewed through a diffuse or soft glossy reflection. Below is an example of using :ref:`Glossy Filter <render-cycles-integrator-filter-glossy>` and :doc:`Light Falloff </render/cycles/nodes/types/color/light_falloff>`. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-12-07 02:04+0000
PO-Revision-Date: 2018-12-07 02:06+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 Above we can see the node setup used for the glass transparency trick; on the left the render has too much shadow due to missing caustics, and on the right the render with the trick. Also important is to use shader colors that do **not** have components of value 1.0 or values near that; try to keep the maximum value to 0.8 or less and make your lights brighter. In reality, surfaces are rarely perfectly reflecting all light, but there are of course exceptions; usually glass will let most light through, which is why we need more bounces there. High values for the color components tend to introduce noise because light intensity then does not decrease much as it bounces off each surface. Below is an example render by `The Pixelary <http://blog.thepixelary.com/post/160451378592/denoising-in-cycles-tested>`__. Lượng Bật Nảy -- Bounces  -- Caustics and Filter Glossy Caustics are a well-known source of noise, causing fireflies. They happen because the renderer has difficulty finding specular highlights viewed through a soft glossy or diffuse reflection. There is a :ref:`No Caustics <render-cycles-integrator-no-caustics>` option to disable glossy behind a diffuse reflection entirely. Many renderers will typically disable caustics by default. Caustics disabled.  -- Clamp Fireflies Cycles uses path tracing with next event estimation, which is not good at rendering all types of light effects, like caustics, but has the advantage of being able to render more detailed and larger scenes compared to some other rendering algorithms. This is because we do not need to store, for example, a photon map in memory, and because we can keep rays relatively coherent to use an on-demand image cache, compared to e.g. bidirectional path tracing. Default Glas BSDF. Default settings. Lọc Nhiễu -- Denoising Even with all the settings described above there will always end up being some render noise no matter how many samples you use. To fix this there is a post-processing technique to cleanup the final bit of noise. To use this enable :doc:`Denoising </render/cycles/settings/scene/render_layers/denoising>` in the *Render Layers* tab of the Properties editor. Example render after denoising. Example render before denoising. Filter Glossy greater than zero. For more details, see the :doc:`Light Paths </render/cycles/settings/scene/render/light_paths>` and :doc:`Integrator </render/cycles/settings/scene/render/integrator>` documentation. Four bounces at max.  -- Glass and Transparent Shadows Hard Falloff. However, using No Caustics will result in missing light, and it still does not cover the case where a sharp glossy reflection is viewed through a soft glossy reflection. There is a :ref:`Filter Glossy <render-cycles-integrator-filter-glossy>` option to reduce the noise from such cases at the cost of accuracy. This will blur the sharp glossy reflection to make it easier to find, by increasing the shader Roughness. Ideally with all the previous tricks, fireflies would be eliminated, but they could still happen. For that, the *intensity* that any individual light ray sample will contribute to a pixel can be *clamped* to a maximum value with the integrator :ref:`Clamp setting <render-cycles-integrator-clamp-samples>`. If set too low this can cause missing highlights in the image, which might be useful to preserve for camera effects such as bloom or glare. To mitigate this conundrum it's often useful to clamp only indirect bounces, leaving highlights directly visible to the camera untouched. In reality light in a vacuum will always fall off at a rate of 1/(distance^2). However, as distance goes to zero, this value goes to infinity and we can get very bright spots in the image. These are mostly a problem for indirect lighting, where the probability of hitting such a small but extremely bright spot is low and so happens only rarely. This is a typical recipe for fireflies. In reality light will bounce a huge number of times due to the speed of light being very high. In practice more bounces will introduce more noise, and it might be good to use something like the Limited Global Illumination preset in the :ref:`Light Paths <render-cycles-integrator-light-paths>` Section that uses *fewer* bounces for different shader types. Diffuse surfaces typically can get away with fewer bounces, while glossy surfaces need a few more, and transmission shaders such as glass usually need the most. Irradiance at the shading point. Suy Giảm của Ánh Sáng -- Light Falloff  -- Light Portals Materials with emission shaders can be configured to use Multiple Importance Sampling (:doc:`/render/cycles/materials/settings`). This means that they will get rays sent directly towards them, rather than ending up there based on rays randomly bouncing around. For very bright mesh light sources, this can reduce noise significantly. However, when the emission is not particularly bright, this will take samples away from other brighter light sources for which it is important to find them this way.  -- Multiple Importance Sampling Multiple Importance off. Multiple Importance on. No Clamp (0). No bounces. Optimized Glass Shader. Optimized glass shader. Dò Đường Đi -- Path Tracing  -- Reducing Noise Soft Falloff. The above images show default settings, no caustics, and filter glossy set to 1.0. The detected highlights. The lamp is a known light source, so its location is already known, but the glossy highlight(s) that it causes are a different matter. The best we can do with path tracing is to distribute light rays randomly over the hemisphere, hoping to find all the important bright spots. If for some pixels we miss some bright spot, but we do find it for another, that results in noise. The more samples we take, the higher the probability that we cover all the important sources of light. The optimal setting here is difficult to guess; it may be a matter of trial and error, but often it is clear that a somewhat glowing object may be only contributing light locally, while a mesh light used as a lamp would need this option enabled. Here is an example where the emissive spheres contribute little to the lighting, and the image renders with slightly less noise by disabling Multiple Importance on them. The scene. The world background also has a *Multiple Importance* (:ref:`render-cycles-integrator-world-settings`) option. This is mostly useful for environment maps that have small bright spots in them, rather than being smooth. This option will then, in a preprocess, determine the bright spots, and send light rays directly towards them. Again, enabling this option may take samples away from more important light sources if it is not needed. To find the light that is reflected from this surface, we need to find the average color from all these pixels. Note the glossy highlight on the sphere, and the bright spot the lamp casts on the nearby wall. These hotspots are 100x brighter than other parts of the image and will contribute significantly to the lighting of this pixel. To reduce this problem, the :doc:`Light Falloff </render/cycles/nodes/types/color/light_falloff>` node has a *Smooth factor*, that can be used to reduce the maximum intensity a light can contribute to nearby surfaces. The images above show default falloff and smooth value 1.0. To understand where noise can come from, take for example the scene below. When we trace a light ray into the location marked by the white circle on a red dot, the second image below gives an impression of what the diffuse shader "sees". Two bounces at max. Using Glossy Filter & Light Falloff. We do the inverse of what reality does, tracing light rays from the camera into the scene and onto lights, rather than from the light sources into the scene and then into the camera. This has the advantage that we do not waste light rays that will not end up in the camera, but also means that it is difficult to find some light paths that may contribute a lot. Light rays will be sent either according to the surface BRDF, or in the direction of known light sources (lamps, emitting meshes with Sample as Lamp). When performing a final render, it is important to reduce noise as much as possible. Here we will discuss a number of tricks that, while breaking the laws of physics, are particularly important when rendering animations within a reasonable time. Click to enlarge the example images to see the noise differences well. When rendering a daylight indoor scene where most of the light is coming in through a window or door opening, it is difficult for the integrator to find its way to them. To fix this, use :ref:`Light Portals <render-cycles-lamps-area-portals>`, these work by adding an :ref:`Area Lamp <render-cycles-lamps-area>`. You then will need to modify its shape to match that of the opening that you are trying to fill.  -- Where Noise Comes From With Clamp set to 4. With caustics disabled, glass will miss shadows, and with filter glossy they might be too soft. We can make a glass shader that will use a Glass BSDF when viewed *directly*, and a Transparent BSDF when viewed *indirectly*. The Transparent BSDF can be used for transparent shadows to find light sources straight through surfaces, and will give properly-colored shadows, but without the caustics. The Light Path node is used to determine when to use which of the two shaders. With some tricks we can reduce this noise. If we blur the bright spots, they become bigger and less intense, making them easier to find and less noisy. This will not give the same exact result, but often it's close enough when viewed through a diffuse or soft glossy reflection. Below is an example of using :ref:`Glossy Filter <render-cycles-integrator-filter-glossy>` and :doc:`Light Falloff </render/cycles/nodes/types/color/light_falloff>`. 