��          �               �  l   �  �  �  ]   �     �     �     �             .        B     X     j  Y  q    �  �   �  �   �  �   �     6	     =	     L	  �   ]	  �   -
  �  �
  �   �  �    ]   �                .  "   C     f  .   |  4   �     �     �  Y      b  �   x  �   X  �   3     �     �  +   �  �   #  �   �   :ref:`ui-data-id` used to select the constraints target, and is not functional (red state) when it has none. It also optionally has some raw volumetric features, so the owner can squash down as the target moves closer, or thin out as the target moves farther away. Note however, that it is not the real volume of the owner which is thus preserved, but rather the virtual one defined by its scale values. Hence, this feature works even with non-volumetric objects, like empties, 2D meshes or surfaces, and curves. Limits for the volume preservation to a minimum and maximum scaling each by a *Bulge* factor. Options Plane Reset Rest Length Smooth Smoothness factor to make limits less visible. Stretch To Constraint Stretch To panel. Target The *Stretch To* constraint causes its owner to rotate and scale its Y axis towards its target. So it has the same tracking behavior as the :doc:`Track To constraint </rigging/constraints/tracking/track_to>`. However, it assumes that the Y axis will be the tracking and stretching axis, and does not give you the option of using a different one. These buttons are equivalent to the *Up* ones of the :doc:`Track To constraint </rigging/constraints/tracking/track_to>`: they control which of the X or Z axes should be maintained (as much as possible) aligned with the global Z axis, while tracking the target with the Y axis. These buttons control which of the X and/or Z axes should be affected (scaled up/down) to preserve the virtual volume while stretching along the Y axis. If you enable the *none* button, the volumetric features are disabled. This number button controls the amount of "volume" variation exponentially to the stretching amount. Note that the 0.0 value is not allowed, if you want to disable the volume feature, use the *None* button (see below). This number button sets the rest distance between the owner and its target, i.e. the distance at which there is no deformation (stretching) of the owner. Volume Volume Min/Max Volume Variation When clicked, this small button will recalculate the *Rest Length* value, so that it corresponds to the actual distance between the owner and its target (i.e. the distance before this constraint is applied). With bones, the "volumetric" variation scales them along their own local axes (remember that the local Y axis of a bone is aligned with it, from root to tip). Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-12-07 01:52+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 :ref:`ui-data-id` sử dụng để chọn mục tiêu ràng buộc. Không hoạt động (trạng thái màu đỏ) khi không có gì. It also optionally has some raw volumetric features, so the owner can squash down as the target moves closer, or thin out as the target moves farther away. Note however, that it is not the real volume of the owner which is thus preserved, but rather the virtual one defined by its scale values. Hence, this feature works even with non-volumetric objects, like empties, 2D meshes or surfaces, and curves. Limits for the volume preservation to a minimum and maximum scaling each by a *Bulge* factor. Tùy Chọn -- Options Mặt Phẳng -- Plane Hoàn Lại -- Reset Chiều Dài Nghỉ -- Rest Length Mịn Màng -- Smooth Smoothness factor to make limits less visible. Ràng Buộc Co Giãn Tới -- Stretch To Constraint Stretch To panel. Mục Tiêu -- Target The *Stretch To* constraint causes its owner to rotate and scale its Y axis towards its target. So it has the same tracking behavior as the :doc:`Track To constraint </rigging/constraints/tracking/track_to>`. However, it assumes that the Y axis will be the tracking and stretching axis, and does not give you the option of using a different one. These buttons are equivalent to the *Up* ones of the :doc:`Track To constraint </rigging/constraints/tracking/track_to>`: they control which of the X or Z axes should be maintained (as much as possible) aligned with the global Z axis, while tracking the target with the Y axis. These buttons control which of the X and/or Z axes should be affected (scaled up/down) to preserve the virtual volume while stretching along the Y axis. If you enable the *none* button, the volumetric features are disabled. This number button controls the amount of "volume" variation exponentially to the stretching amount. Note that the 0.0 value is not allowed, if you want to disable the volume feature, use the *None* button (see below). This number button sets the rest distance between the owner and its target, i.e. the distance at which there is no deformation (stretching) of the owner. Âm Lượng -- Volume  -- Volume Min/Max Dao Động Thể Tích -- Volume Variation When clicked, this small button will recalculate the *Rest Length* value, so that it corresponds to the actual distance between the owner and its target (i.e. the distance before this constraint is applied). With bones, the "volumetric" variation scales them along their own local axes (remember that the local Y axis of a bone is aligned with it, from root to tip). 