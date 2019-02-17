# -*- encoding: utf-8 -*-
#
# Plug-in to make the links absolute in the TOC and
# the extra style/script files on the 404 page.
#
# Adapted form: sphinxcontrib-fulltoc
# https://github.com/sphinx-contrib/fulltoc
#
# Copyright © 2012 New Dream Network, LLC (DreamHost)
#
# Author: Doug Hellmann <doug.hellmann@dreamhost.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


from docutils import nodes
from sphinx import addnodes

ROOT = "https://docs.blender.org/manual/"
LANGUAGE = "en"
VERSION = "dev"


def path_to_abs(uri):
    while True:
        if uri.startswith("../"):
            uri = uri[3:]
        else:
            break

    return ROOT + LANGUAGE + "/" + VERSION + "/" + uri


def html_page_context(app, pagename, templatename, context, doctree):
    """Event handler for the html-page-context signal.

    Modifies the context directly.

     - Replaces the 'toc' value created by the HTML builder with one
       that shows all document titles and the local table of contents.
     - Sets display_toc to True so the table of contents is always
       displayed, even on empty pages.
     - Replaces the 'toctree' function with one that uses the entire
       document structure, ignores the maxdepth argument, and uses
       only prune and collapse.
    """
    if templatename == "404.html":
        global LANGUAGE
        LANGUAGE = context['language']

        # more cannot be replaced because the html builder adds "_static"
        for k in ("css_files", "script_files"):
            res = []
            for ent in context[k]:
                if ent.startswith("_static"):
                    ent = path_to_abs(ent)
                res.append(ent)
            context[k] = res

        # >>>
        rendered_toc = get_rendered_toctree(app.builder, pagename)
        context['toc'] = rendered_toc

        if "toctree" not in context:
            # json builder doesn't use toctree func, so nothing to replace
            return
        def make_toctree(collapse=True, maxdepth=-1, includehidden=True, titles_only=False):
            return get_rendered_toctree(app.builder,
                                        pagename,
                                        prune=False,
                                        collapse=collapse,
                                        )
        context['toctree'] = make_toctree


def get_rendered_toctree(builder, docname, prune=False, collapse=True):
    """Build the toctree relative to the named document,
    with the given parameters, and then return the rendered
    HTML fragment.
    """
    fulltoc = build_full_toctree(builder,
                                 docname,
                                 prune=prune,
                                 collapse=collapse,
                                 )
    rendered_toc = builder.render_partial(fulltoc)['fragment']
    return rendered_toc


def build_full_toctree(builder, docname, prune, collapse):
    """Return a single toctree starting from docname containing all
    sub-document doctrees.
    """
    env = builder.env
    doctree = env.get_doctree(env.config.master_doc)
    toctrees = []
    for toctreenode in doctree.traverse(addnodes.toctree):
        toctree = env.resolve_toctree(docname, builder, toctreenode,
                                      collapse=collapse,
                                      prune=prune,
                                      includehidden=True,
                                      )
        if toctree is not None:
            toctrees.append(toctree)

    if not toctrees:
        return None
    result = toctrees[0]
    for toctree in toctrees[1:]:
        if toctree:
            result.extend(toctree.children)

    # >>>
    for node in result.traverse(nodes.reference):
        node["refuri"] = path_to_abs(node["refuri"])

    return result


def setup(app):
    app.connect('html-page-context', html_page_context)
