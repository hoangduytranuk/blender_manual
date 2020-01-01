��    (      \              �  *   �  /   �  &   �  +     (   K  8   t     �  �  �  \   A     �     �     �  9   �       T  !     v     �     �  	   �  p   �  {        �     �  >   �  \   �  �   U	    �	  g   �
  �   b  :        A     T     e          �     �  z   �  e   0  �   �  �  ?  *   �  /   "  &   R  +   y  (   �  8   �  7     �  ?  \   �  3         T  G   p  9   �     �  T    2   g  1   �     �     �  p     {   v  0   �  ;   #  >   _  \   �  �   �    �  g   �  �     :   �  /   �  +     C   C  '   �  >   �  <   �  z   +  e   �  �      :class:`blender_api:bpy.types.KeyMapItem`. :class:`blender_api:bpy.types.KeyMapItems.new`, :class:`blender_api:bpy.types.KeyMap`, :class:`blender_api:bpy.types.KeyMaps.new`, :mod:`blender_api:bpy.props.IntProperty` Add the following script to the Text editor in Blender:: Add-on Tutorial An add-on will typically register operators, panels, menu items, etc, but it's worth noting that *any* script can do this, when executed from the Text editor or even the interactive console -- there is nothing inherently different about an add-on that allows it to integrate with Blender, such functionality is just provided by the :mod:`blender_api:bpy` module for any script to access. As before, first we will start with a script, develop it, then convert it into an add-on. :: Bringing It All Together Conclusions Documentation Links For API documentation on the functions listed above, see: Further Reading If you are interested in this area, read into :class:`blender_api:mathutils.Vector` -- there are many handy utility functions such as getting the angle between vectors, cross product, dot products as well as more advanced functions in :mod:`blender_api:mathutils.geometry` such as Bézier spline interpolation and ray-triangle intersection. Install the Add-on Intended Audience Keymap Menu Item Next, we're going to do this in a loop, to make an array of objects between the active object and the cursor. :: Notice this add-on does not do anything related to Blender (the :mod:`blender_api:bpy` module is not imported for example). Operator Property Prerequisites The first step is to convert the script as-is into an add-on:: The method used for adding a menu item is to append a draw function into an existing class:: There are a variety of property types that are used for tool settings, common property types include: int, float, vector, color, boolean and string. These properties from :mod:`blender_api:bpy.props` are handled specially by Blender when the class is registered so they display as buttons in the user interface. There are many arguments you can pass to properties to set limits, change the default and display a tooltip. This add-on takes the body of the script above, and adds it to an operator's ``execute()`` function. :: To get rid of the literal 10 for ``total``, we'll use an operator property. Operator properties are defined via bpy.props module, this is added to the class body:: To give an example, here is the simplest possible add-on:: What is an Add-on? Write the Add-on Write the Add-on (Simple) Write the Script Your First Add-on Your Second Add-on `Blender Development (Wiki) <https://wiki.blender.org>`__ -- *Blender Development, general information and helpful links.* `Dive Into Python <http://getpython3.com/diveintopython3/index.html>`__ sections (1, 2, 3, 4, and 7). `How to Think Like a Computer Scientist <http://interactivepython.org/courselib/static/thinkcspy/index.html>`__ -- *Great info for those who are still learning Python.* Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-12-27 20:49-0600
PO-Revision-Date: 2019-04-24 02:16+0100
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.7.0
 :class:`blender_api:bpy.types.KeyMapItem`. :class:`blender_api:bpy.types.KeyMapItems.new`, :class:`blender_api:bpy.types.KeyMap`, :class:`blender_api:bpy.types.KeyMaps.new`, :mod:`blender_api:bpy.props.IntProperty` Add the following script to the Text editor in Blender:: Hướng Dẫn về Trình Bổ Sung -- Add-on Tutorial An add-on will typically register operators, panels, menu items, etc, but it's worth noting that *any* script can do this, when executed from the Text editor or even the interactive console -- there is nothing inherently different about an add-on that allows it to integrate with Blender, such functionality is just provided by the :mod:`blender_api:bpy` module for any script to access. As before, first we will start with a script, develop it, then convert it into an add-on. :: Tổng Hợp Toàn Bộ -- Bringing It All Together Kết Luận -- Conclusions Những Đường Kết Nối đến Tài Liệu -- Documentation Links For API documentation on the functions listed above, see: Đọc Thêm -- Further Reading If you are interested in this area, read into :class:`blender_api:mathutils.Vector` -- there are many handy utility functions such as getting the angle between vectors, cross product, dot products as well as more advanced functions in :mod:`blender_api:mathutils.geometry` such as Bézier spline interpolation and ray-triangle intersection. Cài Đặt Trình Bổ Sung -- Install the Add-on Đối Tượng Dự Định -- Intended Audience Bố Trí Bàn Phím -- Keymap Trình Mục -- Menu Item Next, we're going to do this in a loop, to make an array of objects between the active object and the cursor. :: Notice this add-on does not do anything related to Blender (the :mod:`blender_api:bpy` module is not imported for example). Tính Chất của Operator -- Operator Property Điều Kiện Tiên Quyết (Đòi Hỏi) -- Prerequisites The first step is to convert the script as-is into an add-on:: The method used for adding a menu item is to append a draw function into an existing class:: There are a variety of property types that are used for tool settings, common property types include: int, float, vector, color, boolean and string. These properties from :mod:`blender_api:bpy.props` are handled specially by Blender when the class is registered so they display as buttons in the user interface. There are many arguments you can pass to properties to set limits, change the default and display a tooltip. This add-on takes the body of the script above, and adds it to an operator's ``execute()`` function. :: To get rid of the literal 10 for ``total``, we'll use an operator property. Operator properties are defined via bpy.props module, this is added to the class body:: To give an example, here is the simplest possible add-on:: Trình Bổ Sung là gì? -- What is an Add-on? Viết Trình Bổ Sung -- Write the Add-on Viết Trình Bổ Sung (Đơn Giản) -- Write the Add-on (Simple) Viết Tập Lệnh -- Write the Script Trình Bổ Sung Đầu Tiên của Bạn -- Your First Add-on Trình Bổ Sung Thứ Hai của Bạn -- Your Second Add-on `Blender Development (Wiki) <https://wiki.blender.org>`__ -- *Blender Development, general information and helpful links.* `Dive Into Python <http://getpython3.com/diveintopython3/index.html>`__ sections (1, 2, 3, 4, and 7). `How to Think Like a Computer Scientist <http://interactivepython.org/courselib/static/thinkcspy/index.html>`__ -- *Great info for those who are still learning Python.* 