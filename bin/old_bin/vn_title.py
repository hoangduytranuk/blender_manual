#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pprint import pprint as pp
from bs4 import BeautifulSoup
import html

#from __future__ import division

import re
from docutils import nodes
from docutils.parsers.rst import directives, Directive
from pprint import pprint as pp

#CONTROL_HEIGHT = 30

#_re_size = re.compile("(\d+)(|%|px)$")
#_re_aspect = re.compile("(\d+):(\d+)")


#def get_size(d, key):
    #if key not in d:
        #return None
    #m = _re_size.match(d[key])
    #if not m:
        #raise ValueError("invalid size %r" % d[key])
    #return int(m.group(1)), m.group(2) or "px"


#def css(d):
    #return "; ".join(sorted("%s: %s" % kv for kv in d.items()))


#class vimeo(nodes.General, nodes.Element):
    #pass


#def visit_vimeo_node(self, node):
    #aspect = node["aspect"]
    #width = node["width"]
    #height = node["height"]

    #if aspect is None:
        #aspect = 16, 9

    #if (height is None) and (width is not None) and (width[1] == "%"):
        #style = {
            #"padding-top": "%dpx" % CONTROL_HEIGHT,
            #"padding-bottom": "%f%%" % (width[0] * aspect[1] / aspect[0]),
            #"width": "%d%s" % width,
            #"position": "relative",
        #}
        #self.body.append(self.starttag(node, "div", style=css(style)))
        #style = {
            #"position": "absolute",
            #"top": "0",
            #"left": "0",
            #"width": "100%",
            #"height": "100%",
            #"border": "0",
        #}
        #attrs = {
            #"src": "https://player.vimeo.com/video/%s" % node["id"],
            #"style": css(style),
        #}
        #self.body.append(self.starttag(node, "iframe", **attrs))
        #self.body.append("</iframe></div>")
    #else:
        #if width is None:
            #if height is None:
                #width = 560, "px"
            #else:
                #width = height[0] * aspect[0] / aspect[1], "px"
        #if height is None:
            #height = width[0] * aspect[1] / aspect[0], "px"
        #style = {
            #"width": "%d%s" % width,
            #"height": "%d%s" % (height[0] + CONTROL_HEIGHT, height[1]),
            #"border": "0",
        #}
        #attrs = {
            #"src": "https://player.vimeo.com/video/%s" % node["id"],
            #"style": css(style),
        #}
        #self.body.append(self.starttag(node, "iframe", **attrs))
        #self.body.append("</iframe>")


#def depart_vimeo_node(self, node):
    #pass


#def nop_node(self, node):
    #pass


##Blender custom for not html builders
#def process_vimeo_node(app, doctree, fromdocname):
    #if app.builder.name != "html" and app.builder.name != "singlehtml":
        #for node in doctree.traverse(vimeo):
            #para = nodes.paragraph()
            #t = "A video can be found at "
            #intex = nodes.Text(t, t)
            #para += intex

            #href = "https://vimeo.com/%s" % node["id"]
            #linknode = nodes.reference('', '', internal=False, refuri=href)
            #innernode = nodes.inline('', href)
            #linknode.append(innernode)
            #para += linknode

            #node.replace_self(para)


#class Vimeo(Directive):
    #has_content = True
    #required_arguments = 1
    #optional_arguments = 0
    #final_argument_whitespace = False
    #option_spec = {
        #"width": directives.unchanged,
        #"height": directives.unchanged,
        #"aspect": directives.unchanged,
    #}

    #def run(self):
        #if "aspect" in self.options:
            #aspect = self.options.get("aspect")
            #m = _re_aspect.match(aspect)
            #if m is None:
                #raise ValueError("invalid aspect ratio %r" % aspect)
            #aspect = tuple(int(x) for x in m.groups())
        #else:
            #aspect = None
        #width = get_size(self.options, "width")
        #height = get_size(self.options, "height")
        #return [
            #vimeo(
                #id=self.arguments[0],
                #aspect=aspect,
                #width=width,
                #height=height,
                #)
             #]

#def process_doctree(app, doctree, docname):
    ##print("-" * 80)
    ##print("process docname = {}".format(docname))
    ##print("process doctree :{}".format(doctree))
    ##print("=" * 80)
    ##pp(doctree)
    ##print("-" * 80)
    ##exit(0)

    ##home = os.environ["HOME"]
    #build_dir="build/rstdoc_0001"
    #output_file="{}.html".format(docname)

    #local_path = os.path.dirname(os.path.abspath( __file__ ))
    #blender_docs_path = os.path.dirname(local_path)

    #rst_output_location = os.path.join(blender_docs_path, build_dir)
    #output_path=os.path.join(rst_output_location, output_file)
    #dir_name = os.path.dirname(output_path)
    ##text = str(doctree).replace("><", ">\n<")
    #text = str(doctree)
    #print("output_path:{}; dir_name:{}; local_path:{}; blender_docs_path:{}".format(output_path, dir_name, local_path, blender_docs_path))
    ##pp(text)
    #try:
        #os.makedirs(dir_name, exist_ok=True)
        #with open(output_path, "w") as f:
            #soup = BeautifulSoup(text, 'html.parser')
            #text = soup.prettify()
            #f.write(text);
    #except Exception as e:
        #print("Exception writeTextFile:{}".format(output_path))
        #raise e
    ##exit(0)


#def setup(app):
    ##event listener: replace node if not html builder
    #listender_id = app.connect('doctree-resolved', process_doctree)

    #return {
        #"parallel_read_safe": True,
    #}

class title(nodes.Element): pass
class field_list(nodes.Element): pass
class field_name(nodes.Element): pass
class field_body(nodes.Element): pass
class term(nodes.Element): pass
class strong(nodes.Element): pass
class rubric(nodes.Element): pass
class paragraph(nodes.Element): pass

def visit_title_html(self, node):
    print("visit_title_html - node [{}]".format(node))
    raise nodes.SkipNode

def depart_title_html(self, node):
    print("depart_title_html - node [{}]".format(node))
    raise nodes.SkipNode

def visit_field_name_html(self, node):
    print("visit_field_name_html - node [{}]".format(node))
    print("node.astext:{}".format(node.astext()) )
    raise nodes.SkipNode

def depart_field_name_html(self, node):
    print("depart_field_name_html - node [{}]".format(node))
    raise nodes.SkipNode

def visit_field_body_html(self, node):
    print("visit_field_body_html - node [{}]".format(node))
    print("node.astext:{}".format(node.astext()))

    print("list_of_nodes:")
    list_of_nodes = list(node.traverse())
    pp(list_of_nodes)

    #print("node.attlist:{}".format(node.attlist()))

    #if (node.hasattr('rawtext')):
    #   print("node.rawtext:{}".format(node.get('rawtext', "")))

    #print("node.astext:{}".format(node.astext()) )
    raise nodes.SkipNode

def depart_field_body_html(self, node):
    print("depart_field_body_html - node [{}]".format(node))
    raise nodes.SkipNode


def visit_paragraph_html(self, node):
    is_parent_field_body = isinstance(node.parent, nodes.field_body)
    if (is_parent_field_body):
        print("visit_paragraph_html - node [{}]".format(node))
        node_text = str(node)
        soup = BeautifulSoup(node_text, "html.parser")
        para = soup.find_all('paragraph')
        men = soup.find_all('inline', {'classes' : 'menuselection'})
        kbd = soup.find_all('literal', {'classes' : 'kbd'})
        txt = soup.text

        #if use raw_text then don't use para.text
        use_para_text = True
        for m in men:
            rawtext = "{}".format(m['rawtext'])
            rawtext = html.unescape(rawtext)
            use_para_text = False
            print("rawtext:{}".format(rawtext))

        for k in kbd:
            k.replaceWith(":kbd:`{}`".format(k.text))

        if (use_para_text):
            for p in para:
                print("para.text:[{}]".format(p.text))
                print("type(para):[{}]".format(type(p)))

        print("men:[{}]".format(men))
        print("kbd:[{}]".format(kbd))

        #never uses this
        print("txt:[{}]".format(txt))
        print("-" * 50)
        #print("visit_paragraph_html - node [{}]".format(node))
        #print("list_of_nodes:")
        #list_of_nodes = list(node.traverse())
        #pp(list_of_nodes)
        #length = len(list_of_nodes)
        #for i, x in enumerate(list_of_nodes):
            #print("i:{}; x=[{}]".format(i, x))



    raise nodes.SkipNode

def depart_paragraph_html(self, node):
    print("depart_paragraph_html - node [{}]".format(node))
    raise nodes.SkipNode



def visit_term_html(self, node):
    print("visit_term_html - node [{}]".format(node))
    raise nodes.SkipNode

def depart_term_html(self, node):
    print("depart_term_html - node [{}]".format(node))
    raise nodes.SkipNode

def visit_strong_html(self, node):
    print("visit_strong_html - node [{}]".format(node))
    raise nodes.SkipNode

def depart_strong_html(self, node):
    print("depart_strong_html - node [{}]".format(node))
    raise nodes.SkipNode

def visit_rubric_html(self, node):
    print("visit_rubric_html - node [{}]".format(node))
    raise nodes.SkipNode

def depart_rubric_html(self, node):
    print("depart_rubric_html - node [{}]".format(node))
    raise nodes.SkipNode

def process_title(app, doctree, docname):
    print("=" * 50)
    print("process_title - docname [{}]".format(docname))
    print("=" * 50)


def setup(app):
    #app.add_node(title, html=(visit_title_html, depart_title_html))

    #app.add_node(field_name, html=(visit_field_name_html, depart_field_name_html))
    app.add_node(paragraph, html=(visit_paragraph_html, depart_paragraph_html))

    #app.add_node(term, html=(visit_term_html, depart_term_html))
    #app.add_node(strong, html=(visit_strong_html, depart_strong_html))
    #app.add_node(rubric, html=(visit_rubric_html, depart_rubric_html))

    ##event listener: replace node if not html builder
    #listender_id = app.connect('doctree-resolved', process_doctree)

    #listender_id = app.connect('doctree-resolved', process_title)
    listender_id = app.connect('doctree-resolved', process_title)

    return {
        "parallel_read_safe": True,
    }
