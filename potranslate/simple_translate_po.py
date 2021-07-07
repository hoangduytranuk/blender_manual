#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import division

import re
from docutils import nodes
from docutils.parsers.rst import directives, Directive

import sys
import os
from pyparsing import *
from sphinx.cmd.build import main
from definition import Definitions as df
from sphinx.util.nodes import extract_messages
from common import Common as cm, dd
from translation_finder import TranslationFinder

tf = TranslationFinder()

def doctree_resolved(app, doctree, docname):
    def isKeepCopyOfOriginal(node):
        is_inline = isinstance(node, nodes.inline)
        is_emphasis = isinstance(node, nodes.emphasis)
        is_title = isinstance(node, nodes.title)
        is_term = isinstance(node, nodes.term)
        is_rubric = isinstance(node, nodes.rubric)
        is_field_name = isinstance(node, nodes.field_name)
        is_reference = isinstance(node, nodes.reference)
        is_strong = isinstance(node, nodes.strong)

        is_keep_original = (is_inline or
                            is_emphasis or
                            is_title or
                            is_term or
                            is_rubric or
                            is_field_name or
                            is_reference or
                            is_strong
                            )
        return is_keep_original

    try:
        for node, msg in extract_messages(doctree):
            is_repeat = isKeepCopyOfOriginal(node)
            if is_repeat:
                msg = msg.strip()
                dd("=" * 80)
                df.LOG(f"msgid:[{msg}]")
                tran = tf.isInDict(msg)
                if not tran:
                    tf.addBackupDictEntry(msg, "")

    except Exception as e:
        df.LOG(f'{e}', error=False)

def build_finished(app, exeption):
    tf.writeChosenDict(is_master=False)

def setup(app):
    # app.connect('builder-inited', builder_inited)
    app.connect('doctree-resolved', doctree_resolved)
    app.connect('build-finished', build_finished)
    # app.connect('env-updated', env_updated)
    # env-updated

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }


if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
