��    Y      �              �     �     �     �     �     �     �     �     �       2   
  !   =  .   _  .   �  1   �  $   �  *     *   ?  -   j  &   �  �   �  w   [     �  6   �  !   	     3	     G	     [	     n	  �   �	  �   L
    �
     �  k        n     v  	   }  $   �  �   �     m  	   �  >  �    �     �  �   �     �     �  �   �     �     �     �     �  %   �     �     �       
   	  +       @  	   P     Z     h     x     �     �     �     �     �  .   �  "    ]  $  ]   �  k   �  A   L  �   �  �   :  �   �  �   i  V   :  ,   �     �     �     �     �  �     e   �  )   .  	  X  G   b  �  �     b     k     t     }     �     �     �     �     �  2   �  !   �  .      .   C   1   r   $   �   *   �   *   �   -   !  &   M!  �   t!  w   "     �"  6   �"  O   �"  6   %#  5   \#  +   �#     �#  �   �#  �   �$    +%  A   2&  k   t&     �&     �&     '  O   /'  �   '  =   @(  #   ~(  >  �(    �)     �*  �   +  A   �+     ,  �   6,     �,     -  5   -     L-  ^   b-  E   �-     .     #.  '   3.  +  [.  %   �/     �/  &   �/  *   �/  5   0  8   O0  $   �0  P   �0  ,   �0  &   +1  .   R1  "  �1  ]  �2  ]   4  k   `4  A   �4  �   5  �   �5  �   E6  �   �6  V   �7  ,   8     >8  O   R8     �8  !   �8  �   �8  e   �9  )   :  	  .:  G   8;   :kbd:`C` :kbd:`E` :kbd:`G` :kbd:`K` :kbd:`R` :kbd:`S` :kbd:`Shift-K` :kbd:`Shift-S` :kbd:`Y` :menuselection:`Properties Region --> Strip Input` :menuselection:`Strip --> Change` :menuselection:`Strip --> Cut (hard) at Frame` :menuselection:`Strip --> Cut (soft) at Frame` :menuselection:`Strip --> Grab/Extend from Frame` :menuselection:`Strip --> Grab/Move` :menuselection:`Strip --> Reassign Inputs` :menuselection:`Strip --> Separate Images` :menuselection:`Strip --> Slip Strip Content` :menuselection:`Strip --> Snap Strips` All selected strip handles to the "mouse side" of the current frame indicator will transform together, so you can change the duration of the current frame. Although you can adjust the :ref:`duration (hard) <sequencer-duration-hard>` number buttons in the *Strip Input* panel. Change Changes the source file contained in a selected strip. Clear Strips Offsets :kbd:`Alt-O` Cut (hard) at Frame Cut (soft) at Frame Deinterlace Movies Delete the selected strip(s). Dragging the left arrow left will create a lead-in (copies) of the first frame for as many frames as you drag it. Use this when you want some frames for a transition at the start of the clip. Dragging the right arrow to the left shortens the clip; any original images at the tail are ignored. Use this to quickly clip off a roll-down. Dragging the right arrow to the right extends the clip. For movies and images sequences, more of the animation is used until exhausted. Extending a clip beyond its end results in Blender making a copy of the last image. Use this for transitions out of this clip. Duplicate Strips :kbd:`Shift-D` Duplicate a strip to make an unlinked copy; drag it to a time and channel, and drop it by :kbd:`LMB` click. Editing Effect End Frame Erase Strips :kbd:`X`, :kbd:`Delete` For images sequence only -- Converts the strip into multiple strips, one strip for each frame. Useful for slide shows and other cases where you want to bring in a set on non-continuous images. Grab/Extend from Frame Grab/Move Holding down :kbd:`Ctrl` while dragging snaps to the start and endpoints of other strips. The position of the mouse relative to the selection influences where the strips are snapped. If it is closer to the start of the selection, then the start frame of the selection gets snapped, else the end frame will get snapped. Holding down :kbd:`RMB` and then moving the mouse drags the active strip in time or in channels. Pressing :kbd:`G` moves the all selected strip(s). Move your mouse horizontally (left/right) to change the strip's position in time. Move vertically (up/down) to change channels. Hotkey If you have a 20-image sequence strip, and drag the left arrow to the right by 10 frames, the strip will start at image 11 (images 1 to 10 will be skipped). Use this to clip off a roll-up or undesired lead-in. Insert/Remove Gap Length Like *Cut (soft) at Frame*, it cuts a strip in two distinct strips; however you will not be able to drag the endpoints to show the frames past the cut of each resulting strip. Lock Strips Menu Multiple selection Mute Mute Deselected Strips :kbd:`Shift-H` Mute Strips :kbd:`H` Mute the selected strip(s). Panel Path/Files Position your cursor (vertical green line) to the time you want. Snap to current frame to start a strip exactly at the beginning of the frame. If your Time display is in seconds, you can get to fractional parts of a second by zooming the display; you can get all the way down to an individual frame. Reassign Inputs Reference Reload Strips Separate Images Set Render Size Slip Strip Content Snap Strips Start Frame Offset Swap Inputs Swap Strips Switch the effects on a selected Effect strip. The *end frame* of the strip could be selected by clicking :kbd:`RMB` on the right arrow of the strip; holding it down (or pressing :kbd:`G` grab) and then moving the mouse changes the ending frame within the strip. The frame number label over the strip displays the end frame of the strip. The *start frame offset* for that strip could be selected by clicking :kbd:`RMB` on the left arrow of the strip; holding it down (or pressing :kbd:`G` grab and then moving the mouse left/right) changes the start frame within the strip by the number of frames you move it. The frame number label under the strip displays the start frame of the strip. The Change sequence operator modifies the file path or effect inputs/type on selected strips. The Slip tool allows you to change the position of the contents of a strip without moving the strip itself. The Strip Menu contains additional tools for working with strips: This can be thought of as a quick way to duplicate the current strip, adjusting the start/end frames to form two non-overlapping strips showing the same content as before. This can be thought of as a way to simulate splitting the video file in two parts at the cut-point, replacing the current strip with each. This cuts the selected strip in two at the current frame. This will result in two strips which use the same source, fitting the original strip's timing and length. This tool can be used to assign (reconnect) effect strips in a different way. Just select three arbitrary strips and press :kbd:`R`. If you don't create a cycle, those will be connected to a new effect chain. To "ripple edit" (Make room for strips you drag) hold :kbd:`Alt` when placing a strip. To reset the (soft) start/end frame handles. Tools Un-Mute Strips :kbd:`Alt-H` Un-Mutes all strips. UnLock Strips With a number of strips selected, pressing :kbd:`E` lets you interactively extend the strips. This is similar to grabbing but is useful for extending (or shortening) time around the current frame. You can also lock the direction to time with :kbd:`X` or to change the strip's channel with :kbd:`Y`. You can mute all strips but the selected. You can select several (handles of) strips by :kbd:`Shift-RMB` clicking: when you press :kbd:`G`, everything that is selected will move with your mouse- this means that, for example, you can at the same time move a strip, shorten two others, and extend a forth one. You have to specify the duration you want the resulting strips will be. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2019-01-21 01:47+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 :kbd:`C` :kbd:`E` :kbd:`G` :kbd:`K` :kbd:`R` :kbd:`S` :kbd:`Shift-K` :kbd:`Shift-S` :kbd:`Y` :menuselection:`Properties Region --> Strip Input` :menuselection:`Strip --> Change` :menuselection:`Strip --> Cut (hard) at Frame` :menuselection:`Strip --> Cut (soft) at Frame` :menuselection:`Strip --> Grab/Extend from Frame` :menuselection:`Strip --> Grab/Move` :menuselection:`Strip --> Reassign Inputs` :menuselection:`Strip --> Separate Images` :menuselection:`Strip --> Slip Strip Content` :menuselection:`Strip --> Snap Strips` All selected strip handles to the "mouse side" of the current frame indicator will transform together, so you can change the duration of the current frame. Although you can adjust the :ref:`duration (hard) <sequencer-duration-hard>` number buttons in the *Strip Input* panel. Thay Đổi -- Change Changes the source file contained in a selected strip. Xóa sự Dịch Chuyển của các Dải -- Clear Strips Offsets :kbd:`Alt-O` Cắt (hẳn) tại Khung Hình -- Cut (hard) at Frame Cắt (hờ) tại Khung Hình -- Cut (soft) at Frame Tuần Tự Hóa Phim -- Deinterlace Movies Delete the selected strip(s). Dragging the left arrow left will create a lead-in (copies) of the first frame for as many frames as you drag it. Use this when you want some frames for a transition at the start of the clip. Dragging the right arrow to the left shortens the clip; any original images at the tail are ignored. Use this to quickly clip off a roll-down. Dragging the right arrow to the right extends the clip. For movies and images sequences, more of the animation is used until exhausted. Extending a clip beyond its end results in Blender making a copy of the last image. Use this for transitions out of this clip. Sao Chép Dải :kbd:`Shift-D` -- Duplicate Strips :kbd:`Shift-D` Duplicate a strip to make an unlinked copy; drag it to a time and channel, and drop it by :kbd:`LMB` click. Biên Soạn -- Editing Hiệu Ứng -- Effect Khung Hình Cuối -- End Frame Xóa các Dải :kbd:`X`, :kbd:`Delete` -- Erase Strips :kbd:`X`, :kbd:`Delete` For images sequence only -- Converts the strip into multiple strips, one strip for each frame. Useful for slide shows and other cases where you want to bring in a set on non-continuous images. Tóm Bắt/Co Kéo từ Khung Hình -- Grab/Extend from Frame Túm Nắm/Di Chuyển -- Grab/Move Holding down :kbd:`Ctrl` while dragging snaps to the start and endpoints of other strips. The position of the mouse relative to the selection influences where the strips are snapped. If it is closer to the start of the selection, then the start frame of the selection gets snapped, else the end frame will get snapped. Holding down :kbd:`RMB` and then moving the mouse drags the active strip in time or in channels. Pressing :kbd:`G` moves the all selected strip(s). Move your mouse horizontally (left/right) to change the strip's position in time. Move vertically (up/down) to change channels. Phím Tắt -- Hotkey If you have a 20-image sequence strip, and drag the left arrow to the right by 10 frames, the strip will start at image 11 (images 1 to 10 will be skipped). Use this to clip off a roll-up or undesired lead-in. Chèn Thêm/Xóa Bỏ Khoảng Cách Trống -- Insert/Remove Gap Chiều Dài -- Length Like *Cut (soft) at Frame*, it cuts a strip in two distinct strips; however you will not be able to drag the endpoints to show the frames past the cut of each resulting strip. Khóa Dải -- Lock Strips Trình Đơn -- Menu Chọn nhiều cùng một lúc -- Multiple selection Giải Hoạt -- Mute Giải Hoạt các Dải Không Chọn :kbd:`Shift-H` -- Mute Deselected Strips :kbd:`Shift-H` Giải Hoạt Tính Của Các Dải :kbd:`H` -- Mute Strips :kbd:`H` Mute the selected strip(s). Bảng -- Panel Đường Dẫn/Tập Tin -- Path/Files Position your cursor (vertical green line) to the time you want. Snap to current frame to start a strip exactly at the beginning of the frame. If your Time display is in seconds, you can get to fractional parts of a second by zooming the display; you can get all the way down to an individual frame. Đổi Đầu Vào -- Reassign Inputs Tham Chiếu -- Reference Tái Nạp các Dải -- Reload Strips Phân Tách Hình Ảnh -- Separate Images Đặt Kích Thước Kết Xuất -- Set Render Size Xê Dịch Nội Dung Đoạn Phim -- Slip Strip Content Bám Dính các Dải -- Snap Strips Dịch Chuyển (Vị Trí) của Khung Hình Đầu Tiên -- Start Frame Offset Tráo Đổi các Đầu Vào -- Swap Inputs Tráo Đổi các Dải -- Swap Strips Switch the effects on a selected Effect strip. The *end frame* of the strip could be selected by clicking :kbd:`RMB` on the right arrow of the strip; holding it down (or pressing :kbd:`G` grab) and then moving the mouse changes the ending frame within the strip. The frame number label over the strip displays the end frame of the strip. The *start frame offset* for that strip could be selected by clicking :kbd:`RMB` on the left arrow of the strip; holding it down (or pressing :kbd:`G` grab and then moving the mouse left/right) changes the start frame within the strip by the number of frames you move it. The frame number label under the strip displays the start frame of the strip. The Change sequence operator modifies the file path or effect inputs/type on selected strips. The Slip tool allows you to change the position of the contents of a strip without moving the strip itself. The Strip Menu contains additional tools for working with strips: This can be thought of as a quick way to duplicate the current strip, adjusting the start/end frames to form two non-overlapping strips showing the same content as before. This can be thought of as a way to simulate splitting the video file in two parts at the cut-point, replacing the current strip with each. This cuts the selected strip in two at the current frame. This will result in two strips which use the same source, fitting the original strip's timing and length. This tool can be used to assign (reconnect) effect strips in a different way. Just select three arbitrary strips and press :kbd:`R`. If you don't create a cycle, those will be connected to a new effect chain. To "ripple edit" (Make room for strips you drag) hold :kbd:`Alt` when placing a strip. To reset the (soft) start/end frame handles. Công Cụ -- Tools Bật Hoạt Tính của các Dải :kbd:`Alt-H` -- Un-Mute Strips :kbd:`Alt-H` Un-Mutes all strips. Mở Khóa Dải -- UnLock Strips With a number of strips selected, pressing :kbd:`E` lets you interactively extend the strips. This is similar to grabbing but is useful for extending (or shortening) time around the current frame. You can also lock the direction to time with :kbd:`X` or to change the strip's channel with :kbd:`Y`. You can mute all strips but the selected. You can select several (handles of) strips by :kbd:`Shift-RMB` clicking: when you press :kbd:`G`, everything that is selected will move with your mouse- this means that, for example, you can at the same time move a strip, shorten two others, and extend a forth one. You have to specify the duration you want the resulting strips will be. 