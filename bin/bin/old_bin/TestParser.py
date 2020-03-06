import os
import docutils
from docutils import nodes
from sphinx import addnodes, roles
from pprint import pprint as PP
from six import text_type
from sphinx.util.nodes import extract_messages, traverse_translatable_index
# class FieldBodyVisitor(GenericNodeVisitor):
#
#     def setResult(self, result):
#         self.result = result
#
#     def default_visit(self, node):
#         pass
#
#     def default_departure(self, node):
#         pass
#
#     def visit_literal(self, node):
#         attrib_class = getattr(node, 'classes')
#         is_keyboard =(attrib_class == 'kbd')
#         is_menu_selection = (attrib_class == 'menuselection')
#         print(node.astext())
#         print("is_keyboard:", is_keyboard)
#         print("is_menu_selection:", is_menu_selection)

def process_field_name(node, result):
    obj = node.next_node(nodes.field_name)
    if not obj:
        return

    result.update({obj.astext():'field_name='})

def process_field_body(node, result):
    obj = node.next_node(nodes.field_body)
    if not obj:
        return

    #traverse
    # for i in range(0, len(obj)):
    #     print("node[{}]={}".format(i, node[i].astext()))

    r = obj._all_traverse()
    print("traverse result:")
    for n in r:
        print("type:{}, text:{}".format(type(n), n))

    #PP(r)
    # for n in enumerate(result):
    #     print("node:{}".format(n))

    result.update({obj.astext():'field_body='})

def process_object_with_classes(node, result):
    literal = node.next_node(nodes.literal)
    inline = node.next_node(nodes.inline)

    valid = (literal or inline)
    if not valid:
        return

    kbd = 'kbd'
    menusel = 'menuselection'
    menu_sep = '‣'
    doc = 'doc'
    std = 'std'
    std_ref = 'std-ref'
    xref = 'xref'
    std_term = 'std-term'


    obj = (literal if literal else inline)
    obj_parent = (obj.parent)
    parent_text = obj_parent.astext()

    #obj.hasattr('classes')
    classes = obj.get('classes')
    is_menu_selection = (classes) and (menusel in classes)
    # print("TEXT:", obj.astext())
    # print("classes:", classes)
    # if (is_menu_selection):
    #     print("is_menu_selection")
    # else:
    #     print("NOT is_menu_selection")
    '''
        msgid ":menuselection:`Add`"
        ------------------------------
        <inline classes="menuselection" rawtext=":menuselection:`Cộng Thêm (Add)`">
         Cộng Thêm (Add)
        </inline>    
    '''

    is_keyboard = (classes) and (kbd in classes)
    # if (is_keyboard):
    #     print("is_keyboard")
    # else:
    #     print("NOT keyboard")
    '''
        msgid ":kbd:`Shift-A`"
        ------------------------------
       <paragraph>
        <literal classes="kbd">
         Shift-A
        </literal>
       </paragraph>        
    '''
    #<reference internal="True" refuri=
    #<inline classes="xref std std-term">
    #:ref:`easings <editors-graph-fcurves-settings-easing>`
    #:doc:`keyframe </animation/keyframes/index>`

    '''
        :term:`Color Blend Modes`
        ---------------------------
        <reference internal="True" refuri="../../../../glossary/index.html#term-color-blend-modes">
        <inline classes="xref std std-term">
         Color Blend Modes
        </inline>
       </reference>

    '''
    # is_doc = (classes) and (doc in classes)
    # is_ref = (classes) and (std in classes) and (std_ref in classes)
    # is_xref_term = (classes) and (xref in classes) and (std in classes) and (std_term in classes)

    # if (classes):
    #     print("classes:", classes)
    keyword = (kbd if is_keyboard else menusel if is_menu_selection else None)
    orig_text = obj.astext()
    if (keyword):
        if (is_menu_selection):
            menu_item_list = orig_text.split(menu_sep)
            PP(menu_item_list)
            orig_text = "-->".join(menu_item_list)

        if (parent_text):
            print("parent_node:", obj_parent.starttag)
            print("parent_text:", parent_text)
        txt = ":{}:`{}`".format(keyword, orig_text)
        tail = "{}".format(obj.tagname)
        result.update({txt:tail})


def process_title(node, result):
    title = node.next_node(nodes.Titular)
    if not title:
        return

    result.update({title.astext():'title='})

def process_term(node, result):
    term = node.next_node(nodes.term)
    if not term:
        return

    #term.traverse(nodes.literal)
    result.update({term.astext():'term='})

def process_rubric(node, result):
    rubric = node.next_node(nodes.rubric)
    if not rubric:
        return

    result.update({rubric.astext():'rubric='})

# def process_field_list(node, result):
#     field_list = node.next_node(nodes.rubric)
#     if not field_list:
#         return
#
#     result.update({field_list.astext():'field_list='})

def process_node_with_title(node, result):
    hint = node.next_node(nodes.hint)
    tip = node.next_node(nodes.tip)
    note = node.next_node(nodes.note)
    valid = (hint or tip or note)
    if not valid:
        return

    obj = (hint if hint else tip if tip else note)
    desc = ('hint' if hint else 'tip' if tip else 'note')

    text_list = obj.astext().split("\n")
    has_title = (len(text_list) > 1)
    if (not has_title):
        return

    first_line = text_list[0]
    second_line = text_list[1]
    has_title = (len(first_line) > 1) and (len(second_line) == 0)
    if (not has_title):
        return

    title = first_line
    result.update({title:"{}'s title".format(obj.tagname)})


def process_list_item(node, result):

    list_item = node.next_node(nodes.list_item)
    if not list_item:
        return

    result.update({list_item.astext():'list_item='})

def process_table_head(node, result):
    thead = node.next_node(nodes.thead)
    if not thead:
        return

    result.update({thead.astext():'thead='})

def print_separator(output_path):
    print("docname:", output_path)
    print("-" * 30)

def print_result_list(result):
    PP(result)

def doctree_resolved(app, doctree, docname):
    build_dir = "build/rstdoc"
    po_vi_dir = "locale/vi/LC_MESSAGES"

    html_file="{}.html".format(docname)
    local_path = os.path.dirname(os.path.abspath( __file__ ))
    blender_docs_path = os.path.dirname(local_path)

    rst_output_location = os.path.join(blender_docs_path, build_dir)
    output_path = os.path.join(rst_output_location, html_file)

    result={}

    for node, msg in extract_messages(doctree):
        is_title = (isinstance(node, nodes.title))
        is_term = (isinstance(node, nodes.term))
        is_rubric = (isinstance(node, nodes.rubric))
        is_field_name = (isinstance(node, nodes.field_name))
        #is_paragraph = (isinstance(node, nodes.paragraph))

        # orig_msg = None
        # if isinstance(node, addnodes.translatable):
        #     orig_msg = node.extract_original_messages()
        # print("node:{}".format(node))
        # if (orig_msg):
        #     print("original message:".format(orig_msg))
        # print("msgid \"{}\"".format(msg))
        # print("")

    # #exit(0)
    # for node in doctree.traverse():
    #
    #     process_title(node, result)
    #     process_term(node, result)
    #     process_rubric(node, result)
    #     process_field_name(node, result)
    #     process_field_body(node, result)
    #     #process_object_with_classes(node, result)
    #     process_node_with_title(node, result)
    #
    #     # seealso = node.next_node(nodes.seealso)
    #     # if seealso:
    #     #     print ("seealso:", seealso.astext())
    #
    #     #process_note(node, result)
    #     # process_list_item(node, result)
    #     process_table_head(node, result)

    print_result_list(result)
    print_separator(output_path)

# def source_read(app, docname, source):
#     #load corresponding po file from locale/vi/LC_MESSAGE
#     #references are placed in app
#     #print("source_read docname:", docname)
#     regis = app.registry
#     print("regis:", regis.get_transforms())
#
#
# def builder_inited(app):
#     app.registry.add_transform(LocalVar)
#     print("builder_inited")
#
#     #read vipo translated file
#     #form normal sorted list
#     #form lower case sorted list
#     #pass


def setup(app):
    # app.connect('builder-inited', builder_inited)
    # app.connect('source-read', source_read)
    app.connect('doctree-resolved', doctree_resolved)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
