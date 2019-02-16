��    (      \              �     �     �     �  	   �     �     �  =   �     2     H     Z  E   h  �   �  ;   1  �   m  	          S     '   o  O   �  K   �     3     <     @  S  H     �  �   �     �  T   �     �     �  4   �     ,	  �  ?	  �  �
    �  �  �  �   i       �      �        �     �  *   �  *        @     _  =   ~     �  ,   �       E     �   Y  ;   �  �        �     �  S   �  '   9  O   a  K   �     �          '  S  ?     �  �   �     �  T   �     �     
  4        R  �  h  �  �    �  �  �  �   �   8   0!  �   i!   2D Stabilization Panel 2D Stabilization panel. Anchor Frame Autoscale Bicubic Bilinear Compensates any scale changes relative to center of rotation. Expected Position X/Y Expected Rotation Expected Zoom Explicitly scale resulting frame to compensate zoom of original shot. Finds smallest scale factor which, when applied to the footage, would eliminate all empty black borders near the image boundaries. Highest quality interpolation, most expensive to calculate. In addition to location, stabilizes detected rotation around the *rotation pivot point*, which is the weighted average of all location tracking points. Influence Interpolate Known relative offset of original shot, will be subtracted, e.g. for panning shots. Limits the amount of automatic scaling. List of tracks to be used to compensate for camera jumps, or location movement. List of tracks to be used to compensate for camera tilts and scale changes. Location Max Nearest No interpolation, uses nearest neighboring pixel. No interpolation, use nearest neighboring pixel. This setting basically retains the original image's sharpness. The downside is we also retain residual movement below the size of one pixel, and compensation movements are done in 1 pixel steps, which might be noticeable as irregular jumps. Options Reference point to anchor stabilization: other frames will be adjusted relative to this frame's position, orientation and scale. You might want to select a frame number where your main subject is featured in an optimal way. Rotation Rotation present on original shot, will be compensated, e.g. for deliberate tilting. Rotation/Scale Scale Simple linear interpolation between adjacent pixels. Stabilization Type The 2D Stabilization panel is used to define the data used for 2D stabilization of the shot. Several options are available in this panel: you may add a list of tracks to determine lateral image shifts and another list of tracks to determine tilting and zooming movements. Based on the average contribution of these tracks, a compensating movement is calculated and applied to each frame. The amount of transformation applied to the footage can be controlled. In some cases it is not necessary to fully compensate camera jumps. The amount of stabilization applied to the footage can be controlled. In some cases you may not want to fully compensate some of the camera's jumps. Please note that these "\* *Influence*" parameters do control only the *compensation movements* calculated by the stabilizer, not the deliberate movements added through the "*Expected* \*"-parameters. The stabilizer calculates compensation movements with sub-pixel accuracy. Consequently, a resulting image pixel needs to be derived from several adjacent source footage pixels. Unfortunately, any interpolation causes some minor degree of softening and loss of image quality. There is one extra panel which is available in reconstruction mode -- 2D Stabilization Panel. The purpose of this feature is to smooth out jerky camera handling on existing real-world footage. To activate the 2D stabilizer, you need to set the toggle in the panel, and additionally you need to enable *Display Stabilization* in the Display panel. Then you'll need to set up some tracking points to detect the image movements. To *activate* the 2D stabilizer, you need to set the toggle in the panel, and additionally you need to enable *Display Stabilization* in the *Display* panel. Tracks For Stabilization When the footage includes panning and traveling movements, the stabilizer tends to push the image out of the visible area. This can be compensated by animating the parameters for the intentional, "expected" camera movement. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-12-10 21:53+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 -- 2D Stabilization Panel 2D Stabilization panel. Khung Hình Đối Chiếu -- Anchor Frame Tự Động Đổi Tỷ Lệ -- Autoscale Song Lập Phương -- Bicubic Song Tuyến Tính -- Bilinear Compensates any scale changes relative to center of rotation. -- Expected Position X/Y Xoay Chiều Dự Tính -- Expected Rotation -- Expected Zoom Explicitly scale resulting frame to compensate zoom of original shot. Finds smallest scale factor which, when applied to the footage, would eliminate all empty black borders near the image boundaries. Highest quality interpolation, most expensive to calculate. In addition to location, stabilizes detected rotation around the *rotation pivot point*, which is the weighted average of all location tracking points. Ảnh Hưởng -- Influence Nội Suy -- Interpolate Known relative offset of original shot, will be subtracted, e.g. for panning shots. Limits the amount of automatic scaling. List of tracks to be used to compensate for camera jumps, or location movement. List of tracks to be used to compensate for camera tilts and scale changes. Vị Trí -- Location Lớn Nhất -- Max Gần Nhất -- Nearest No interpolation, uses nearest neighboring pixel. No interpolation, use nearest neighboring pixel. This setting basically retains the original image's sharpness. The downside is we also retain residual movement below the size of one pixel, and compensation movements are done in 1 pixel steps, which might be noticeable as irregular jumps. Tùy Chọn -- Options Reference point to anchor stabilization: other frames will be adjusted relative to this frame's position, orientation and scale. You might want to select a frame number where your main subject is featured in an optimal way. Xoay Chiều -- Rotation Rotation present on original shot, will be compensated, e.g. for deliberate tilting. -- Rotation/Scale Tỷ Lệ -- Scale Simple linear interpolation between adjacent pixels. -- Stabilization Type The 2D Stabilization panel is used to define the data used for 2D stabilization of the shot. Several options are available in this panel: you may add a list of tracks to determine lateral image shifts and another list of tracks to determine tilting and zooming movements. Based on the average contribution of these tracks, a compensating movement is calculated and applied to each frame. The amount of transformation applied to the footage can be controlled. In some cases it is not necessary to fully compensate camera jumps. The amount of stabilization applied to the footage can be controlled. In some cases you may not want to fully compensate some of the camera's jumps. Please note that these "\* *Influence*" parameters do control only the *compensation movements* calculated by the stabilizer, not the deliberate movements added through the "*Expected* \*"-parameters. The stabilizer calculates compensation movements with sub-pixel accuracy. Consequently, a resulting image pixel needs to be derived from several adjacent source footage pixels. Unfortunately, any interpolation causes some minor degree of softening and loss of image quality. There is one extra panel which is available in reconstruction mode -- 2D Stabilization Panel. The purpose of this feature is to smooth out jerky camera handling on existing real-world footage. To activate the 2D stabilizer, you need to set the toggle in the panel, and additionally you need to enable *Display Stabilization* in the Display panel. Then you'll need to set up some tracking points to detect the image movements. To *activate* the 2D stabilizer, you need to set the toggle in the panel, and additionally you need to enable *Display Stabilization* in the *Display* panel. Giám Sát Ổn Định Hóa -- Tracks For Stabilization When the footage includes panning and traveling movements, the stabilizer tends to push the image out of the visible area. This can be compensated by animating the parameters for the intentional, "expected" camera movement. 