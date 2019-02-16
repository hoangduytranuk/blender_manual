��          �               �  �   �  '   k  u   �     	  d        z  �   �    b     s     x     �     �     �  	   �  Z   �       
     7   "  )   Z  +   �  g   �      �   %  �  �  �   �
  A   e  u   �  )     d   G     �  �   �    �     �     �  &   �          #     3  Z   M     �  7   �  7   �  )   -  +   W  g   �    �  �   �   *Duplication at Frames* or *DupliFrames* creates instances of an animated object that correspond to the state of this object (including *Location*, *Rotation* and *Scaling*) in each frame of the animation. :menuselection:`Object --> Duplication` Creates an alternating pattern, *"On"* number of frames will be shown, next *"Off"* frames will be skipped and so on. DupliFrames DupliVerts can be used to arrange objects, for example, along a circle or across a subdivided plane. Examples In Fig. :ref:`fig-object-duplication-dupliframes-driver` *DupliFrames* is applied to the object that is animated using the :doc:`Drivers </animation/drivers/index>` with a scripted expression and moves along the sine wave. In Fig. :ref:`fig-object-duplication-dupliframes-path` *DupliFrames* is applied to the *Monkey* object that travel along the Bézier circle during 16 frames, (see :ref:`Path Animation <curve-path-animation>` example). Option *Speed* in the *Duplication panel* is disabled. Mode Object Duplication panel. Object Mode On, Off Panel Reference Specify the start and end frames of the animation for which the instances will be created. Speed Start, End The monkey is animated using the Follow Path animation. The sphere is animated using the Drivers. There are many alternatives to DupliFrames. To arrange objects along a curve, combining an *Array Modifier* and a *Curve Modifier* is often useful. To transform all monkeys into real objects, first :kbd:`Shift-Ctrl-A` to *Make Duplicates Real*. All monkeys are now real objects, but still linked copies. To change this, use :kbd:`U` shortcut or :menuselection:`Object --> Make Single User --> Object & Data --> All`. When the object is animated using :ref:`Follow Path <curve-path-animation>` animation, this option causes to ignore this path animation, and use only the animation of the object itself. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-12-08 16:54+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 *Duplication at Frames* or *DupliFrames* creates instances of an animated object that correspond to the state of this object (including *Location*, *Rotation* and *Scaling*) in each frame of the animation. :menuselection:`Vật Thể (Object) --> Sao Chép (Duplication)` Creates an alternating pattern, *"On"* number of frames will be shown, next *"Off"* frames will be skipped and so on. Sao Chép theo Khung Hình -- DupliFrames DupliVerts can be used to arrange objects, for example, along a circle or across a subdivided plane. Các Ví Dụ -- Examples In Fig. :ref:`fig-object-duplication-dupliframes-driver` *DupliFrames* is applied to the object that is animated using the :doc:`Drivers </animation/drivers/index>` with a scripted expression and moves along the sine wave. In Fig. :ref:`fig-object-duplication-dupliframes-path` *DupliFrames* is applied to the *Monkey* object that travel along the Bézier circle during 16 frames, (see :ref:`Path Animation <curve-path-animation>` example). Option *Speed* in the *Duplication panel* is disabled. Chế Độ -- Mode Object Duplication panel. Chế Độ Vật Thể -- Object Mode Bật, Tắt -- On, Off Bảng -- Panel Tham Chiếu -- Reference Specify the start and end frames of the animation for which the instances will be created. Tốc Độ -- Speed Bắt Đầu, Kết Thúc (Đầu,Cuối) -- Start, End The monkey is animated using the Follow Path animation. The sphere is animated using the Drivers. There are many alternatives to DupliFrames. To arrange objects along a curve, combining an *Array Modifier* and a *Curve Modifier* is often useful. To transform all monkeys into real objects, first :kbd:`Shift-Ctrl-A` to *Make Duplicates Real*. All monkeys are now real objects, but still linked copies. To change this, use :kbd:`U` shortcut or :menuselection:`Object --> Make Single User --> Object & Data --> All`. When the object is animated using :ref:`Follow Path <curve-path-animation>` animation, this option causes to ignore this path animation, and use only the animation of the object itself. 