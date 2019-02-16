��    3      �              L  &   M  *   t     �     �     �     �  
   �  
   �  
   �  n   �  	   Y  r  c     �  /   �               -     ?     U    ^     c     u  �   �  `   X     �     �     �  
   �  	   �  '   �  F   	  )   e	  4   �	  l   �	  T   1
  ;   �
     �
  p   �
     ;  .   �     �  U   �  C   T  �   �     L     [     j     |     �  !  �  �  �  &   o  *   �     �     �  /   �            &     G  %   g  n   �     �  r  	     |  /   �  &   �  1   �  *     ?   >     ~    �     �     �  �   �  `   �  ;   �     6     G      W     x  '   �  F   �  )     4   +  l   `  T   �  ;   "     ^  p   t     �  .   e  /   �  U   �  C     �   ^          %     8     N     d  !  {   :menuselection:`Material --> Settings` :term:`Blend modes` for transparent faces. Add Alpha Alpha Anti-Aliasing Alpha Blend Alpha Clip Alpha Sort Blend Mode Both methods can be combined, to do displacement on a coarser mesh, and use bump mapping for the final detail. Bump only By default objects with emitting materials use both direct and indirect light sampling methods, but in some cases it may lead to less noise overall to disable direct light sampling for some materials. This can be done by disabling the *Multiple Importance Sample* option. This is especially useful on large objects that emit little light compared to other light sources. Color Diffuse color of the object in the 3D viewport. Displacement Displacement Method Displacement Only Displacement and Bump Hardness Index number for the *Material Index* :doc:`render pass </render/cycles/settings/scene/render_layers/passes>`. This can be used to give a mask to a material and then be read with the :doc:`ID Mask Node </compositing/types/converter/id_mask>` in the compositor. Material Settings Material Settings. Mesh vertices will be displaced before rendering, modifying the actual mesh. This gives the best quality results, if the mesh is finely subdivided. As a result, this method is also the most memory intensive. Method used to perform :doc:`Displacement </render/cycles/materials/displacement>` on materials. Multiple Importance Sample Opaque Panel Pass Index Reference Render color of textured face as color. Render polygon transparent, depending on alpha channel of the texture. Render transparent and add color of face. Roughness control for the object in the 3D viewport. Similar volume settings as the :ref:`World settings <render-cycles-integrator-world-settings>` per material. Sort faces for correct alpha drawing (slow, use *Alpha Clip* instead when possible). Specular reflection color of the object in the 3D viewport. Surface These Options are only available if :ref:`Experimental Feature Set <cycles-experimental-features>` is turned on. This option will only have an influence if the material contains an emission node; it will be automatically disabled otherwise. Transparency of the object in the 3D viewport. Transparent Shadows Use texture alpha to add an anti-aliasing mask, requires multi-sample OpenGL display. Use the image alpha values clipped with no blending (binary alpha). Use transparent shadows if it contains a :doc:`Transparent BSDF </render/cycles/nodes/types/shaders/transparent>`, disabling will render faster but will not give accurate shadows. Viewport Alpha Viewport Color Viewport Settings Viewport Specular Volume When executing the surface shader, a modified surface normal is used instead of the true normal. This is a less memory intensive alternative to actual displacement, but only an approximation. Surface silhouettes will not be accurate and there will be no self-shadowing of the displacement. Project-Id-Version: Blender 2.79 Manual 2.79
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
 :menuselection:`Material --> Settings` :term:`Blend modes` for transparent faces. Cộng -- Add Alpha Chống Răng Cưa Alpha -- Alpha Anti-Aliasing Hòa Trộn Alpha -- Alpha Blend Cắt Bằng Alpha -- Alpha Clip Sắp Xếp Alpha -- Alpha Sort Chế Độ Hòa Trộn -- Blend Mode Both methods can be combined, to do displacement on a coarser mesh, and use bump mapping for the final detail. -- Bump only By default objects with emitting materials use both direct and indirect light sampling methods, but in some cases it may lead to less noise overall to disable direct light sampling for some materials. This can be done by disabling the *Multiple Importance Sample* option. This is especially useful on large objects that emit little light compared to other light sources. Màu -- Color Diffuse color of the object in the 3D viewport. Phép/Sự/Dời Hình -- Displacement Phương Pháp Dời Hình -- Displacement Method Duy Phép Dời Hình -- Displacement Only Phép Dời Hình và Độ Gồ Ghề -- Displacement and Bump Độ Sắc Nét -- Hardness Index number for the *Material Index* :doc:`render pass </render/cycles/settings/scene/render_layers/passes>`. This can be used to give a mask to a material and then be read with the :doc:`ID Mask Node </compositing/types/converter/id_mask>` in the compositor.  -- Material Settings Material Settings. Mesh vertices will be displaced before rendering, modifying the actual mesh. This gives the best quality results, if the mesh is finely subdivided. As a result, this method is also the most memory intensive. Method used to perform :doc:`Displacement </render/cycles/materials/displacement>` on materials. Lấy Mẫu Vật Đa Trọng -- Multiple Importance Sample Đục -- Opaque Bảng -- Panel Chỉ Số Lượt -- Pass Index Tham Chiếu -- Reference Render color of textured face as color. Render polygon transparent, depending on alpha channel of the texture. Render transparent and add color of face. Roughness control for the object in the 3D viewport. Similar volume settings as the :ref:`World settings <render-cycles-integrator-world-settings>` per material. Sort faces for correct alpha drawing (slow, use *Alpha Clip* instead when possible). Specular reflection color of the object in the 3D viewport. Bề Mặt -- Surface These Options are only available if :ref:`Experimental Feature Set <cycles-experimental-features>` is turned on. This option will only have an influence if the material contains an emission node; it will be automatically disabled otherwise. Transparency of the object in the 3D viewport. Bóng Tối Trong Suốt -- Transparent Shadows Use texture alpha to add an anti-aliasing mask, requires multi-sample OpenGL display. Use the image alpha values clipped with no blending (binary alpha). Use transparent shadows if it contains a :doc:`Transparent BSDF </render/cycles/nodes/types/shaders/transparent>`, disabling will render faster but will not give accurate shadows.  -- Viewport Alpha  -- Viewport Color  -- Viewport Settings  -- Viewport Specular Âm Lượng -- Volume When executing the surface shader, a modified surface normal is used instead of the true normal. This is a less memory intensive alternative to actual displacement, but only an approximation. Surface silhouettes will not be accurate and there will be no self-shadowing of the displacement. 