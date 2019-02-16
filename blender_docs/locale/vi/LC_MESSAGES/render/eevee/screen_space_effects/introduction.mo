��          T               �   �   �   �       �  �   �  �   D  )   �  �  $  �   �  �  -     �  �   �  �   p  )   &	   Blended surfaces are not considered by these effects. They are not part of the depth prepass and does not appear in the depth buffer. Eevee is not a ray tracing engine and cannot do ray-triangle intersection. Instead of this, Eevee uses the depth buffer as an approximated scene representation. This reduces the complexity of scene scale effects and allows high performances. However, only what is in inside the view can be considered when computing these effects. Also, since it only use one layer of depth, only the frontmost pixel distance is known. Introduction The screen space effects disappear when reaching the screen border. This can be partially fixed by using the *overscan* feature. The screen space effects don't know how deep (or thick) the objects are. This is why most effects have a thickness parameter to control how to consider potential intersected pixels. These limitations creates a few problems: Project-Id-Version: Blender 2.80 Manual 2.80
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-22 15:35+0000
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language: vi
Language-Team: vi <LL@li.org>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 Blended surfaces are not considered by these effects. They are not part of the depth prepass and does not appear in the depth buffer. Eevee is not a ray tracing engine and cannot do ray-triangle intersection. Instead of this, Eevee uses the depth buffer as an approximated scene representation. This reduces the complexity of scene scale effects and allows high performances. However, only what is in inside the view can be considered when computing these effects. Also, since it only use one layer of depth, only the frontmost pixel distance is known. Giới Thiệu -- Introduction The screen space effects disappear when reaching the screen border. This can be partially fixed by using the *overscan* feature. The screen space effects don't know how deep (or thick) the objects are. This is why most effects have a thickness parameter to control how to consider potential intersected pixels. These limitations creates a few problems: 