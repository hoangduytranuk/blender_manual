��    K      t              �      �     �  
                  6  2   I  	   |  �  �  p     0   �  ?   �  Z   �  =   S     �     �  M   �  <   	  �  W	     	       &     �  D     �     �     �  �   
     �  )   �     �  B     |   C     �     �  �   �  o   �  n     Y   t  |   �  3   K  O     g   �     7     >     K     `     m     |  )   �  b   �  �        �     �       g        �     �     �     �  	   �     �  �  �  ?   �     �     �     �     �  �    b   �  o       t    w  �   �  �   R  �  (       �!     "  
   "  @   ""     c"  ,   {"  2   �"  !   �"  �  �"  p   �$  0   �$  ?   /%  Z   o%  =   �%     &     '&  M   C&  <   �&  �  �&     �(  ,   �(  &   �(  �  �(     �*     �*     �*  �   �*     o+  -   �+     �+  B  �+  |   -     �-     �-  �   �-  o   v.  n   �.  Y   U/  |   �/  3   ,0  O   `0  g   �0     1     '1     41  )   I1     s1     �1  )   �1  b   �1  �   +2      3     3  '   ,3  g   T3     �3     �3  '   �3     4     "4     <4  �  M4  ?   6     Y6     n6     �6     �6  �  �6  b   99  o  �9     ;    ;  �   =  �   �=   :menuselection:`Render --> Bake` Additional Options Advantages Ambient Occlusion Ambient Occlusion Pass. Ambient Occlusion. Axis to bake into the red, green and blue channel. Bake Mode Bake shading on the surface of selected objects to the active object. The rays are cast from the low-poly object inwards towards the high-poly object. If the high-poly object is not entirely involved by the low-poly object, you can tweak the rays start point with *Ray Distance* or *Cage Extrusion* (depending on whether or not you are using cage). For even more control you can use a *Cage Object*. Baked result is extended this many pixels beyond the border of each UV "island", to soften seams in the texture. Bakes Emission, or the Glow color of a material. Bakes all materials, textures, and lighting except specularity. Bakes ambient occlusion as specified in the World panels. Ignores all lights in the scene. Bakes colors of materials and textures only, without shading. Bakes normals to an RGB image. Bakes shadows and lighting. Bakes the diffuse, glossiness, transmission of subsurface pass of a material. Bakes the environment as seen from the center of the object. Baking, in general, is the act of pre-computing something in order to speed up some other process later down the line. Rendering from scratch takes a lot of time depending on the options you choose. Therefore, Blender allows you to "bake" some parts of the render ahead of time, for select objects. Then, when you press Render, the entire scene is rendered much faster, since the colors of those objects do not have to be recomputed. Cage Cage Extrusion Can significantly reduce render times. Cast rays to active object from a cage. A cage is a ballooned-out version of the low-poly mesh created either automatically (by adjusting the ray distance) or manually (by specifying an object to use). When not using a cage the rays will conform to the mesh normals. This produces glitches on the edges, but it is a preferable method when baking into planes to avoid the need of adding extra loops around the edges. Clear Combined Combined Pass options. Cycles uses the render settings (samples, bounces, ...) for baking. This way the quality of the baked textures should match the result you get from the rendered scene. Diffuse Pass options. Diffuse, Glossy, Transmission, Subsurface Disadvantages Distance to use for the inward ray cast when using *Selected to Active* and *Cage*. The inward rays are casted from a version of the active object with disabled Edge Split Modifiers. Hard splits (e.g. when the Edge Split Modifier is applied) should be avoided because they will lead to non-smooth normals around the edges. Distance to use for the inward ray cast when using selected to active. Ray distance is only available when not using *Cage*. Emit Environment For materials the same spaces can be chosen in the image texture options next to the existing *Normal Map* setting. For correct results, the setting here should match the setting used for baking. Human (labor) time must be spent unwrapping and baking and saving files and applying the textures to a channel. If color and either direct or indirect are selected, you get the direct and/or indirect contributions colored. If color is not selected, you get the direct and/or indirect contributions in gray-scale. If only color is selected you get the pass color, which is a property of the surface and independent of sampling refinement. If selected, clears the image before baking render. If shadows are baked, lights and object cannot move with respect to each other. Large textures (e.g. 4096×4096) can be memory intensive, and be just as slow as the rendered solution. Margin Memory Usage Normal Pass options. Normal Space Normal Swizzle Normals Normals can be baked in different spaces: Normals in object coordinates, independent of object transformation, but dependent on deformation. Normals in tangent space coordinates, independent of object transformation and deformation. This is the default, and the right choice in most cases, since then the normal map can be used for animated objects too. Normals. Object must be UV-unwrapped. Object space Object to use as cage instead of calculating the cage from the active object with the *Cage Extrusion*. Options Panel Ray Distance Reduced polygon count. Reference Render Baking Render baking creates 2D bitmap images of a mesh object's rendered surface. These images can be re-mapped onto the object using the object's UV coordinates. Baking is done for each individual mesh, and can only be done if that mesh has been UV-unwrapped. While it takes time to set up and perform, it saves render time. If you are rendering a long animation, the time spent baking can be much less than time spent rendering out each frame of a long animation. Repeated renders are made faster, multiplying the time savings. Select to Active Shadow Tangent space Texture painting made easier. The baking happens into the respective active textures of the object materials. The active texture is the last selected Image Texture node of the material node tree. That means the active object (or the selected objects, when not baking 'Selected to Active') needs a material, and that material needs at least an Image Texture node, with the image to be used for the baking. Note, the node does not need to be connected to any other node. The active texture is what projection painting and the viewport use as a criteria to which image to use. This way after the baking is done you can automatically preview the baked result in the Texture mode. The passes that contribute to the combined pass can be toggled individually to form the final map. There is a CPU fixed memory footprint for every object used to bake from. In order to avoid crashes due to lack of memory, the high-poly objects can be joined before the baking process. The render tiles parameter also influence the memory usage, so the bigger the tile the less overhead you have, but the more memory it will take during baking (either in GPU or CPU). UV Use *Full Render* or *Textures* to create an image texture; baked procedural textures can be used as a starting point for further texture painting. Use *Normals* to make a low resolution mesh look like a high resolution mesh. To do that, UV unwrap a high resolution, finely sculpted mesh and bake its normals. Save that normal map, and *Mapping* (texture settings) the UV of a similarly unwrapped low resolution mesh. The low resolution mesh will look just like the high resolution, but will have much fewer faces/polygons. Use Render Bake in intensive light/shadow solutions, such as AO or soft shadows from area lights. If you bake AO for the main objects, you will not have to enable it for the full render, saving render time. When the base mesh extruded does not give good results, you can create a copy of the base mesh and modify it to use as a *Cage*. Both meshes need to have the same :term:`topology` (number of faces and face order). Project-Id-Version: Blender 2.79 Manual 2.79
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
 :menuselection:`Render --> Bake` -- Additional Options Advantages Tính Hấp Thụ Quang Xạ Môi Trường -- Ambient Occlusion Ambient Occlusion Pass. Tính Hấp Thụ Quang Xạ Môi Trường. Axis to bake into the red, green and blue channel. Chế Độ Nướng -- Bake Mode Bake shading on the surface of selected objects to the active object. The rays are cast from the low-poly object inwards towards the high-poly object. If the high-poly object is not entirely involved by the low-poly object, you can tweak the rays start point with *Ray Distance* or *Cage Extrusion* (depending on whether or not you are using cage). For even more control you can use a *Cage Object*. Baked result is extended this many pixels beyond the border of each UV "island", to soften seams in the texture. Bakes Emission, or the Glow color of a material. Bakes all materials, textures, and lighting except specularity. Bakes ambient occlusion as specified in the World panels. Ignores all lights in the scene. Bakes colors of materials and textures only, without shading. Bakes normals to an RGB image. Bakes shadows and lighting. Bakes the diffuse, glossiness, transmission of subsurface pass of a material. Bakes the environment as seen from the center of the object. Baking, in general, is the act of pre-computing something in order to speed up some other process later down the line. Rendering from scratch takes a lot of time depending on the options you choose. Therefore, Blender allows you to "bake" some parts of the render ahead of time, for select objects. Then, when you press Render, the entire scene is rendered much faster, since the colors of those objects do not have to be recomputed. Khung Lồng -- Cage Đẩy Trồi Khung Lồng -- Cage Extrusion Can significantly reduce render times. Cast rays to active object from a cage. A cage is a ballooned-out version of the low-poly mesh created either automatically (by adjusting the ray distance) or manually (by specifying an object to use). When not using a cage the rays will conform to the mesh normals. This produces glitches on the edges, but it is a preferable method when baking into planes to avoid the need of adding extra loops around the edges. Xóa -- Clear Tổng Hợp -- Combined Combined Pass options. Cycles uses the render settings (samples, bounces, ...) for baking. This way the quality of the baked textures should match the result you get from the rendered scene. Diffuse Pass options.  -- Diffuse, Glossy, Transmission, Subsurface Disadvantages Distance to use for the inward ray cast when using *Selected to Active* and *Cage*. The inward rays are casted from a version of the active object with disabled Edge Split Modifiers. Hard splits (e.g. when the Edge Split Modifier is applied) should be avoided because they will lead to non-smooth normals around the edges. Distance to use for the inward ray cast when using selected to active. Ray distance is only available when not using *Cage*. Phát Xạ -- Emit Môi Trường -- Environment For materials the same spaces can be chosen in the image texture options next to the existing *Normal Map* setting. For correct results, the setting here should match the setting used for baking. Human (labor) time must be spent unwrapping and baking and saving files and applying the textures to a channel. If color and either direct or indirect are selected, you get the direct and/or indirect contributions colored. If color is not selected, you get the direct and/or indirect contributions in gray-scale. If only color is selected you get the pass color, which is a property of the surface and independent of sampling refinement. If selected, clears the image before baking render. If shadows are baked, lights and object cannot move with respect to each other. Large textures (e.g. 4096×4096) can be memory intensive, and be just as slow as the rendered solution. Lề -- Margin Memory Usage Normal Pass options. Không Gian Pháp Tuyến -- Normal Space -- Normal Swizzle Pháp Tuyến -- Normals Normals can be baked in different spaces: Normals in object coordinates, independent of object transformation, but dependent on deformation. Normals in tangent space coordinates, independent of object transformation and deformation. This is the default, and the right choice in most cases, since then the normal map can be used for animated objects too. Pháp Tuyến. Object must be UV-unwrapped. Không gian vật thể -- Object space Object to use as cage instead of calculating the cage from the active object with the *Cage Extrusion*. Tùy Chọn -- Options Bảng -- Panel Khoảng Cách Tia Xạ -- Ray Distance Reduced polygon count. Tham Chiếu -- Reference -- Render Baking Render baking creates 2D bitmap images of a mesh object's rendered surface. These images can be re-mapped onto the object using the object's UV coordinates. Baking is done for each individual mesh, and can only be done if that mesh has been UV-unwrapped. While it takes time to set up and perform, it saves render time. If you are rendering a long animation, the time spent baking can be much less than time spent rendering out each frame of a long animation. Repeated renders are made faster, multiplying the time savings.  -- Select to Active Bóng Tối -- Shadow -- Tangent space Texture painting made easier. The baking happens into the respective active textures of the object materials. The active texture is the last selected Image Texture node of the material node tree. That means the active object (or the selected objects, when not baking 'Selected to Active') needs a material, and that material needs at least an Image Texture node, with the image to be used for the baking. Note, the node does not need to be connected to any other node. The active texture is what projection painting and the viewport use as a criteria to which image to use. This way after the baking is done you can automatically preview the baked result in the Texture mode. The passes that contribute to the combined pass can be toggled individually to form the final map. There is a CPU fixed memory footprint for every object used to bake from. In order to avoid crashes due to lack of memory, the high-poly objects can be joined before the baking process. The render tiles parameter also influence the memory usage, so the bigger the tile the less overhead you have, but the more memory it will take during baking (either in GPU or CPU). UV Use *Full Render* or *Textures* to create an image texture; baked procedural textures can be used as a starting point for further texture painting. Use *Normals* to make a low resolution mesh look like a high resolution mesh. To do that, UV unwrap a high resolution, finely sculpted mesh and bake its normals. Save that normal map, and *Mapping* (texture settings) the UV of a similarly unwrapped low resolution mesh. The low resolution mesh will look just like the high resolution, but will have much fewer faces/polygons. Use Render Bake in intensive light/shadow solutions, such as AO or soft shadows from area lights. If you bake AO for the main objects, you will not have to enable it for the full render, saving render time. When the base mesh extruded does not give good results, you can create a copy of the base mesh and modify it to use as a *Cage*. Both meshes need to have the same :term:`topology` (number of faces and face order). 