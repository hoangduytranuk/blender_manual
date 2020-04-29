��    
      l               �   "   �      �   G  �      B     V     h  �  ~     	     '	  �  0	  S   �
  E   2  G  x  /   �     �  @     �  C  /   �  "      Animating Stabilization Parameters Avoid Problematic Footage Each track contributes to the overall result by the degree controlled through its *Stab Weight* parameter. It is evaluated on a per-frame basis, which enables us to control the influence of a track by *animating* this *Stab Weight*. You may imagine the overall working of the stabilizer as if each tracking point "drags" the image through a flexible spring: When you turn down the *Stab Weight* of a tracking point, you decrease the amount of "drag" it creates. Sometimes the contribution of different tracks has to work partially counter each other. This effect might be used to cancel out spurious movement, e.g. as caused by perspective. But when, in such a situation, one of the involved tracks suddenly goes away, a jump in image position or rotation might be the result. Thus, whenever we notice a jump at the very frame where some partially covered track starts or ends, we need to soften the transition. We do so by animating the *Stab Weight* gradually down, so that it reaches zero at the boundary point. In a similar vein, when we plan a "handover" between several partially covered tracks, we define a *cross-fade* over the duration where the tracks overlap, again by animating the *Stab Weight* parameters accordingly. But even with such cross-fade smoothing, some residual movement might remain, which then needs to be corrected with the *Expected Position* or *Expected rotation* parameters. It is crucial to avoid "overshooting" movements in such a situation -- always strive at setting the animation keyframes onto precisely the same frame number for all the tracks and parameters involved. Elaborate Movements Fine-tuning pass: Irregular Track Setup Prefer higher frame rates. The more *temporal resolution* the stabilizer has to work on, the better the results. If you have the option to choose between progressive and interlaced modes, by all means use interlaced and deinterlace the footage to the *doubled frame rate*. This can be done with the `yadif <https://ffmpeg.org/ffmpeg-filters.html#yadif-1>`__ filter of FFmpeg: use the mode 1 (``send_field``). The Simple Case Workflow Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-07-06 20:15+0100
PO-Revision-Date: 2020-04-10 19:26+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@gmail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@gmail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 Hoạt Hình các Tham Số Ổn Định Hóa -- Animating Stabilization Parameters Tránh các Đoạn Phim Có Vấn Đề -- Avoid Problematic Footage Each track contributes to the overall result by the degree controlled through its *Stab Weight* parameter. It is evaluated on a per-frame basis, which enables us to control the influence of a track by *animating* this *Stab Weight*. You may imagine the overall working of the stabilizer as if each tracking point "drags" the image through a flexible spring: When you turn down the *Stab Weight* of a tracking point, you decrease the amount of "drag" it creates. Sometimes the contribution of different tracks has to work partially counter each other. This effect might be used to cancel out spurious movement, e.g. as caused by perspective. But when, in such a situation, one of the involved tracks suddenly goes away, a jump in image position or rotation might be the result. Thus, whenever we notice a jump at the very frame where some partially covered track starts or ends, we need to soften the transition. We do so by animating the *Stab Weight* gradually down, so that it reaches zero at the boundary point. In a similar vein, when we plan a "handover" between several partially covered tracks, we define a *cross-fade* over the duration where the tracks overlap, again by animating the *Stab Weight* parameters accordingly. But even with such cross-fade smoothing, some residual movement might remain, which then needs to be corrected with the *Expected Position* or *Expected rotation* parameters. It is crucial to avoid "overshooting" movements in such a situation -- always strive at setting the animation keyframes onto precisely the same frame number for all the tracks and parameters involved. Di Chuyển Phức Tạp -- Elaborate Movements Fine-tuning pass: Sắp Đặt Giám Sát Bất Thường -- Irregular Track Setup Prefer higher frame rates. The more *temporal resolution* the stabilizer has to work on, the better the results. If you have the option to choose between progressive and interlaced modes, by all means use interlaced and deinterlace the footage to the *doubled frame rate*. This can be done with the `yadif <https://ffmpeg.org/ffmpeg-filters.html#yadif-1>`__ filter of FFmpeg: use the mode 1 (``send_field``). Trường Hợp Đơn Giản -- The Simple Case Quy Trình Làm Việc -- Workflow 