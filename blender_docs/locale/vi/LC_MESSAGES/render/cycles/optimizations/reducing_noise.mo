��          �               ,  z   -     �     �  |  �     H  	   X     b  �  �  2  !    T     Y     g     u     �     �  �  �  �  `
  z        �     �  |  �     N     a      |  �  �  2  >    q  ,   v     �  =   �  !   �       �  &   Below is an example render by `The Pixelary <http://blog.thepixelary.com/post/160451378592/denoising-in-cycles-tested>`__. Bounces Caustics and Filter Glossy Caustics are a well-known source of noise, causing fireflies. They happen because the renderer has difficulty finding specular highlights viewed through a soft glossy or diffuse reflection. There is a :ref:`No Caustics <render-cycles-integrator-no-caustics>` option to disable glossy behind a diffuse reflection entirely. Many renderers will typically disable caustics by default. Clamp Fireflies Denoising Glass and Transparent Shadows However, using No Caustics will result in missing light, and it still does not cover the case where a sharp glossy reflection is viewed through a soft glossy reflection. There is a :ref:`Filter Glossy <render-cycles-integrator-filter-glossy>` option to reduce the noise from such cases at the cost of accuracy. This will blur the sharp glossy reflection to make it easier to find, by increasing the shader Roughness. Ideally with all the previous tricks, fireflies would be eliminated, but they could still happen. For that, the *intensity* that any individual light ray sample will contribute to a pixel can be *clamped* to a maximum value with the integrator :ref:`Clamp setting <render-cycles-integrator-clamp-samples>`. In reality light will bounce a huge number of times due to the speed of light being very high. In practice more bounces will introduce more noise, and it might be good to use something like the Limited Global Illumination preset in the :ref:`Light Paths <render-cycles-integrator-light-paths>` Section that uses *fewer* bounces for different shader types. Diffuse surfaces typically can get away with fewer bounces, while glossy surfaces need a few more, and transmission shaders such as glass usually need the most. Light Falloff Light Portals Multiple Importance Sampling Path Tracing Reducing Noise The world background also has a *Multiple Importance* (:ref:`render-cycles-integrator-world-settings`) option. This is mostly useful for environment maps that have small bright spots in them, rather than being smooth. This option will then, in a preprocess, determine the bright spots, and send light rays directly towards them. Again, enabling this option may take samples away from more important light sources if it is not needed. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2020-02-14 16:43+0100
PO-Revision-Date: 2019-04-24 02:16+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 Below is an example render by `The Pixelary <http://blog.thepixelary.com/post/160451378592/denoising-in-cycles-tested>`__. Lượng Bật Nảy -- Bounces -- Caustics and Filter Glossy Caustics are a well-known source of noise, causing fireflies. They happen because the renderer has difficulty finding specular highlights viewed through a soft glossy or diffuse reflection. There is a :ref:`No Caustics <render-cycles-integrator-no-caustics>` option to disable glossy behind a diffuse reflection entirely. Many renderers will typically disable caustics by default. -- Clamp Fireflies Lọc Nhiễu -- Denoising -- Glass and Transparent Shadows However, using No Caustics will result in missing light, and it still does not cover the case where a sharp glossy reflection is viewed through a soft glossy reflection. There is a :ref:`Filter Glossy <render-cycles-integrator-filter-glossy>` option to reduce the noise from such cases at the cost of accuracy. This will blur the sharp glossy reflection to make it easier to find, by increasing the shader Roughness. Ideally with all the previous tricks, fireflies would be eliminated, but they could still happen. For that, the *intensity* that any individual light ray sample will contribute to a pixel can be *clamped* to a maximum value with the integrator :ref:`Clamp setting <render-cycles-integrator-clamp-samples>`. In reality light will bounce a huge number of times due to the speed of light being very high. In practice more bounces will introduce more noise, and it might be good to use something like the Limited Global Illumination preset in the :ref:`Light Paths <render-cycles-integrator-light-paths>` Section that uses *fewer* bounces for different shader types. Diffuse surfaces typically can get away with fewer bounces, while glossy surfaces need a few more, and transmission shaders such as glass usually need the most. Suy Giảm của Ánh Sáng -- Light Falloff -- Light Portals Lấy Mẫu Vật Đa Trọng -- Multiple Importance Sampling Dò Đường Đi -- Path Tracing -- Reducing Noise The world background also has a *Multiple Importance* (:ref:`render-cycles-integrator-world-settings`) option. This is mostly useful for environment maps that have small bright spots in them, rather than being smooth. This option will then, in a preprocess, determine the bright spots, and send light rays directly towards them. Again, enabling this option may take samples away from more important light sources if it is not needed. 