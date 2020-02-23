#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

#cài BeautifulSoup bằng cách 'sudo pip3 install bs4'
from bs4 import BeautifulSoup as BS

def process_doctree(app, doctree, docname):

    #đường dẫn thư mục để viết ra, dùng thư mục xây dựng làm phụ huynh
    build_dir="build/rstdoc"

    #tên văn bản sẽ viết ra, để là html để các phần mềm xem bài đánh dấu các mã đánh dấu bằng màu sắc, dễ nhìn hơn
    output_file="{}.html".format(docname)

    #thư mục nơi bản mã thi hành. Bản mã này phải năm trong thư mục 'blender_docs/exts, (Extensions)
    local_path = os.path.dirname(os.path.abspath( __file__ ))
    #lùi lại một nhánh để quay về gốc
    blender_docs_path = os.path.dirname(local_path)

    #gắn gốc vào build_dir
    rst_output_location = os.path.join(blender_docs_path, build_dir)
    #gắn đường dẫn và tên tập tin
    output_path=os.path.join(rst_output_location, output_file)
    element_file=os.path.join(output_file, ".elem.txt")
    element_path=os.path.join(rst_output_location, output_file)

    #lấy ra đường dẫn toàn phần, trước tên của tập tin
    dir_name = os.path.dirname(output_path)
    #biến nội dung của doctree thành một dòng văn bản
    text = str(doctree)
    soup = None
    html_text = None

    #Đề phòng có gì xảy ra thì in ra đường dẫn để biết khi xử lý có lỗi và nó nằm ở thời điểm xử lý tập tin nào
    try:
        #nếu đường dẫn chưa có thì tạo nó trước đã
        os.makedirs(dir_name, exist_ok=True)
        #viết nội dung ra, không cần phải đóng (close(f)) vì 'with' đã làm điều này cho mình
        with open(output_path, "w") as f:
            #dùng BeautifulSoup để nó phân tích các mã và làm đẹp nội dung của bản tài liệu, dễ xem
            #cái này nên được viết ra một thư mục riêng vì khi lùng tìm, các ký tự cho thêm của BeautifulSoup
            #gây ảnh hưởng đến kết quả so sánh. Kèm đây để chỉ điểm thi hành trong mã nguồn mà thôi.
            soup = BS(text, 'html.parser')

            html_text = soup.prettify()
            #Viết ra nội dung bản đã được 'làm đẹp'
            f.write(html_text);
    except Exception as e:
        print("Exception process_doctree:{}".format(output_path))
        raise e

    #Dòng này để thoát sau khi chạy 'make gettext' và xử lý một bản đầu tiên trong khi thử nghiệm
    #exit(0)

#bất cứ trình lắng nghe sự kiện nào cũng phải có dòng định nghĩa hàm này
def setup(app):
    #event listener: replace node if not html builder
    #tuy không dùng gì đến listender_id, nhưng viết ra đây để nhớ rằng mình có thể sử dụng nó nữa.
    listender_id = app.connect('doctree-resolved', process_doctree)

    return {
        "parallel_read_safe": True,
    }
'''
-------------------------
     <title>
      Single Image
     </title>
-------------------
ignore instance from Tables
eg:
<table classes="colwidths-given valign" ids="id2 tab-view3d-modes" names="tab-view3d-modes">
    <title>
     Blender’s Modes
    </title>
-----------------
     <thead>
      <row>
       <entry><paragraph>Icon</paragraph></entry>
       <entry><paragraph>Name</paragraph></entry>
       <entry><paragraph>Details</paragraph></entry>
      </row>
     </thead>
-------------------------
     <term>
      Image
     </term>

        <term>
         New
         <literal>
          +
         </literal>
        </term>
        msgid "New ``+``"

<term>
    <reference name="Sphinx RST Primer" refuri="http://www.sphinx-doc.org/en/stable/rest.html">
     Sphinx RST Primer
    </reference>
   </term>
   msgid "`Sphinx RST Primer <http://www.sphinx-doc.org/en/stable/rest.html>`__"

#ignore if followed by <literal>
    <definition_list_item>
     <term>
      <literal>
       ./autosave/ ...
      </literal>
     </term>
     <definition>
      <paragraph>
       Autosave blend-file location. (Windows only, temp directory used for other systems.)
      </paragraph>
      <paragraph>
       Search order:
       <literal>
        LOCAL, USER
       </literal>
       .
      </paragraph>
     </definition>
    </definition_list_item>

#accept
        <definition_list_item>
         <term>
          Average
         </term>
         <definition>
          <paragraph>
           Inherits a uniform scaling factor that represents the total change in the volume of the parent.
          </paragraph>
          <paragraph>
           This effectively keeps the uniform part of the scaling of the parent, while removing squash
and stretch effects. Uniform scaling never causes shear.
          </paragraph>
         </definition>
        </definition_list_item>

-------------------------
   <bullet_list bullet="-">

    <list_item>
     <paragraph>
      <reference internal="True" refuri="">
       <inline classes="doc">
        Toggles the Projection
       </inline>
      </reference>
     </paragraph>
    </list_item>
    msgid ":doc:`Toggles the Projection </editors/3dview/navigate/projections>`"

    <list_item>
     <paragraph>
      <reference internal="True" refuri="">
       <inline classes="doc">
        Toggles the Camera View
       </inline>
      </reference>
     </paragraph>
    </list_item>
    msgid ":doc:`Toggles the Camera View </editors/3dview/navigate/camera_view>`"

    <list_item>
     <paragraph>
      <reference name="Pans the 3D Viewport" refuri="Panning">
       Pans the 3D Viewport
      </reference>
      <target ids="['pans-the-3d-viewport']" names="['pans the 3d viewport']" refuri="Panning">
      </target>
     </paragraph>
    </list_item>

    <list_item>
     <paragraph>
      <reference name="Zooms the 3D Viewport" refuri="Zooming">
       Zooms the 3D Viewport
      </reference>
      <target ids="['zooms-the-3d-viewport']" names="['zooms the 3d viewport']" refuri="Zooming">
      </target>
     </paragraph>
    </list_item>
    msgid "`Zooms the 3D Viewport <Zooming>`_"

   </bullet_list>
-------------------------

  <admonition classes="refbox">
    <title>
     Reference
    </title>
-------------------------

    <field_list>

     <field>
      <field_name>Mode</field_name>
      <field_body>
       <paragraph>All modes</paragraph>
      </field_body>
     </field>

     <field>
      <field_name>Menu</field_name>
      <field_body>
      msgid "Menu"

       <paragraph>
        <inline classes="menuselection" rawtext=":menuselection:`View --&gt; Navigation --&gt; Orbit`">
         View ‣ Navigation ‣ Orbit
        </inline>
       </paragraph>
      </field_body>
     </field>
    msgid ":menuselection:`View --> Navigation --> Orbit`"

     <field>
      <field_name>
       Hotkey
      </field_name>
      msgid "Hotkey"

      <field_body>
       <paragraph>
        <literal classes="kbd">
         MMB
        </literal>
        ,
        <literal classes="kbd">
         Numpad2
        </literal>
        ,
        <literal classes="kbd">
         Numpad4
        </literal>
        ,
        <literal classes="kbd">
         Numpad6
        </literal>
        ,
        <literal classes="kbd">
         Numpad8
        </literal>
        ,
        <literal classes="kbd">
         Ctrl-Alt-Wheel
        </literal>
        ,
        <literal classes="kbd">
         Shift-Alt-Wheel
        </literal>
       </paragraph>
      </field_body>
     </field>
    msgid ""
    ":kbd:`MMB`, :kbd:`Numpad2`, :kbd:`Numpad4`, :kbd:`Numpad6`, "
    ":kbd:`Numpad8`, :kbd:`Ctrl-Alt-Wheel`, :kbd:`Shift-Alt-Wheel`"

    </field_list>
   </admonition>

-------------------------------------
   <note>
    <paragraph>
     Hotkeys
    </paragraph>
    <paragraph>
     Remember that most hotkeys affect the
     <strong>
      active
     </strong>
     area (the one that has focus),
so check that the mouse cursor is in the area you want to work in before you use the hotkeys.
    </paragraph>
   </note>

#the first instance of paragraph is THE TITLE??? - if there are one or more instances of paragraph belows
msgid "Hotkeys"

-------------------------------------

   <seealso>
    <bullet_list bullet="-">
     <list_item>
      <paragraph>
       <reference internal="True" refuri="#prefs-input-orbit-style">
        <inline classes="std std-ref">Orbit Style Preference</inline>
       </reference>
      </paragraph>
     </list_item>

     <list_item>
      <paragraph>
       <reference internal="True" refuri="#prefs-interface-auto-perspective">
        <inline classes="std std-ref">
         Auto-Perspective Preference
        </inline>
       </reference>
      </paragraph>
     </list_item>

    </bullet_list>
   </seealso>

msgid ":ref:`Orbit Style Preference <prefs-input-orbit-style>`"
msgid ":ref:`Auto-Perspective Preference <prefs-interface-auto-perspective>`"
-------------------------------------

<hint>
    <paragraph>
     If You Get Lost
    </paragraph>
    <paragraph>
     If you get lost in 3D space, which is not uncommon, two hotkeys will help you:
     <literal classes="kbd">
      Home
     </literal>
     changes the view so that you can see all objects
     <inline classes="menuselection" rawtext=":menuselection:`View --&gt; Frame All`">
      View ‣ Frame All
     </inline>
     ,
while
     <literal classes="kbd">
      NumpadPeriod
     </literal>
     zooms the view to the currently selected objects
when in perspective mode
     <inline classes="menuselection" rawtext=":menuselection:`View --&gt; Frame Selected`">
      View ‣ Frame Selected
     </inline>
     .
    </paragraph>

msgid ""
"If you get lost in 3D space, which is not uncommon, two hotkeys will help"
" you: :kbd:`Home` changes the view so that you can see all objects "
":menuselection:`View --> Frame All`, while :kbd:`NumpadPeriod` zooms the "
"view to the currently selected objects when in perspective mode "
":menuselection:`View --> Frame Selected`."

   </hint>
-------------------------------------
<rubric ids="bpy-types-cyclesrendersettings-texture-limit bpy-types-rendersettings-simplify-subdivision" names="bpy.types.cyclesrendersettings.texture_limit bpy.types.rendersettings.simplify_subdivision">
   Common Settings
  </rubric>
  msgid "Common Settings"


-------------------------------------
'''
