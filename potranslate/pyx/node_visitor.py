class TranslationNodeVisitor(nodes.TreeCopyVisitor):
#class TranslationNodeVisitor(nodes.NodeVisitor):

    """Raise `nodes.NodeFound` if non-simple list item is encountered.

    Here 'simple' means a list item containing only a paragraph with a
    single reference in it.
    """
    def setVars(self, node, msg, trans):
        self.current_node = node
        self.current_msg = msg
        if trans:
            self.current_trans = trans
        else:
            self.current_trans = msg
        self.fuzzy_list = []
        self.is_fuzzy = False
        self.is_title_node = False
        self.tr = None
        self.ref_trans=[]
        self.node_msg = None
        self.raw_source = None
        self.node_trans = None
        self.node_trans_list=[]
        self.is_ref_node = False
        self.ref_uri = None




    def printNode(self, node, extra=None):
        if not DEBUG:
            return

        _('-'*50)
        if extra:
            _(extra)

        # dd("self.current_msg:[{}]".format(self.current_msg))
        _("type:", type(node))
        if hasattr(node, 'children'):
            _("children:", node.children)

        #dd("name:", type(node.name))
        _("pp node:")
        pp(node)
        if hasattr(node, 'astext'):
            msg = node.astext()
            msg = msg.strip()
            _("node text: [{}]".format(msg))

        if hasattr(node, 'rawsource'):
            _("rawsource: [{}]".format(node.rawsource))

        if hasattr(node, 'line'):
            _("line", node.line)

        _("")
        # dd("dir:", dir(node))
        # dd("len:", len(node))



    def getNodeMsg(self, node):
        msg = None
        has_rawsource = hasattr(node, 'rawsource')
        has_rawtext = ('rawtext' in node.attributes)
        if has_rawtext:
            msg = node.attributes['rawtext']
        elif has_rawsource:
            msg = node.rawsource
        else:
            msg = node.astext()
        self.raw_source = msg
        return msg

    # def translate(self, node):
    #     if DEBUG:
    #         dd("translate node input:", node.astext())
    #     msg = self.getNodeMsg(node)
    #     trans = trans_finder.translateText(msg)
    #     return trans

    def putTranslation(self, node):
        replace_translated_fragment = (self.node_msg and self.current_trans and self.node_trans)
        if replace_translated_fragment:
            node_msg = re.escape(self.node_msg)
            p_msg = r'{}'.format(node_msg)
            p = re.compile(p_msg)
            trans = node.rawsource
            for ts, te, m0, m1 in cm.patternMatchAsList(p, trans):
                has_result = (m0 != None)
                if not has_result:
                    continue

                trans = trans[:ts] + self.node_trans + trans[te:]

            self.current_trans = self.current_trans.replace(self.node_msg, trans)

        if self.current_trans and DEBUG:
            _("msgid", self.current_msg)
            _("msgstr", self.current_trans)

    def isRefNode(self, node):
        # class abbreviation(Inline, TextElement): pass
        # class acronym(Inline, TextElement): pass
        # class citation_reference(Inline, Referential, TextElement): pass
        # class emphasis(Inline, TextElement): pass
        # class footnote_reference(Inline, Referential, TextElement): pass
        # class literal(Inline, TextElement): pass
        # class math(Inline, TextElement): pass
        # class reference(General, Inline, Referential, TextElement): pass
        # class strong(Inline, TextElement): pass
        # class subscript(Inline, TextElement): pass
        # class substitution_reference(Inline, TextElement): pass
        # class superscript(Inline, TextElement): pass
        # class title_reference(Inline, TextElement): pass

        is_doc = (cm.DOC in node[cm.CLASS])
        is_menu = (cm.MNU in node[cm.CLASS])
        is_kbd = (cm.KBD in node[cm.CLASS])
        is_std_ref = (cm.STD_REF in node[cm.CLASS])
        is_x_ref = (cm.X_REF in node[cm.CLASS])
        is_gui_lab = (cm.GUI_LAB in node[cm.CLASS])

        is_ref = (is_doc or is_menu or is_kbd or is_std_ref or is_x_ref or is_gui_lab)
        return is_ref


    def setupNodeForTrans(self, node):
        self.raw_source = self.getNodeMsg(node)
        if DEBUG:
            _("RAW", self.raw_source, ":", type(node), node.astext())
        is_duplicated_already = self.isRefNode(node)
        self.is_ref_node = is_duplicated_already
        is_ignore = isIgnored(node.astext())
        self.keep_original = not ( is_ignore or is_duplicated_already)

        if self.is_ref_node:
            has_ref_uri = (cm.REF_URI in node.attributes)
            if has_ref_uri:
                self.ref_uri  = node.attributes[cm.REF_URI]
            else:
                self.ref_uri = None


    def default_departure(self, node):
        pass

    def default_visit(self, node):
        try:
            if DEBUG:
                _("-"*50)
            trans_finder.treatingText(node)
            has_children = hasattr(node, 'children')
            if has_children:
                for child in node.children:
                    is_same_child = (child == node)
                    if not is_same_child:
                        trans_finder.treatingText(child)
        except Exception as e:
            self.node_msg = None
            self.node_trans = None
            self.keep_original = False

            # class 'docutils.nodes.emphasis' ##>
            # class 'docutils.nodes.image'>
            # class 'docutils.nodes.inline' ##>
            # class 'docutils.nodes.literal' ##>
            # class 'docutils.nodes.math'>
            # class 'docutils.nodes.reference' ##>
            # class 'docutils.nodes.strong' ##>
            # class 'docutils.nodes.Text'>

        # is_inline = isinstance(node, nodes.inline)
        # is_emphasis = isinstance(node, nodes.emphasis)
        # is_title = isinstance(node, nodes.title)
        # is_term = isinstance(node, nodes.term)
        # is_rubric = isinstance(node, nodes.rubric)
        # is_field_name = isinstance(node, nodes.field_name)
        # is_reference = isinstance(node, nodes.reference)
        # is_strong = isinstance(node, nodes.strong)

    def visit_title(self, node):
        if DEBUG:
            _("visit_title", node.astext())
        self.setupNodeForTrans(node)
        #self.default_translation(node, keep_orig=True)

    def depart_title(self, node):
        if DEBUG:
            _("depart_title", node.astext())

    def visit_term(self, node):
        if DEBUG:
            _("visit_term", node.astext())
        self.setupNodeForTrans(node)

    def visit_rubric(self, node):
        if DEBUG:
            _("visit_rubric", node.astext())
        self.setupNodeForTrans(node)

    def visit_field_name(self, node):
        if DEBUG:
            _("visit_field_name", node.astext())
        #self.setupNodeForTrans(node)

    def visit_strong(self, node):
        if DEBUG:
            _("visit_strong", node.astext())
        self.setupNodeForTrans(node)

    def visit_emphasis(self, node):
        if DEBUG:
            _("visit_emphasis", node.astext())
        self.setupNodeForTrans(node)

    def visit_strong(self, node):
        if DEBUG:
            _("visit_strong", node.astext())
        self.setupNodeForTrans(node)

    def depart_reference(self, node):
        if DEBUG:
            msg = node.astext()
            _("depart_reference", msg)
        # is_debug = ('Editing' in msg)
        # if is_debug:
        #     dd('DEBUG')
        # has_ref_uri = (cm.REF_URI in node.attributes)
        # if has_ref_uri:
        #     # ref = [#armature-editing-naming-conventions], actual form = :ref:`next page <armature-editing-naming-conventions>`
        #     refuri = node.attributes[cm.REF_URI]
        #     dd('Attaching REFUIR', refuri)

    def visit_reference(self, node):
        if DEBUG:
            _("visit_reference", node.astext())
        self.setupNodeForTrans(node)

    def depart_inline(self, node):
        if DEBUG:
            _("visit_reference", node.astext())

    def visit_inline(self, node):
        if DEBUG:
            _("visit_inline", node.astext())
        self.setupNodeForTrans(node)
        # is_doc = (cm.DOC in node[cm.CLASS])
        # is_menu = (cm.MNU in node[cm.CLASS])
        # is_kbd = (cm.KBD in node[cm.CLASS])
        # is_std_ref = (cm.STD_REF in node[cm.CLASS])
        # is_x_ref = (cm.X_REF in node[cm.CLASS])
        # is_gui_lab = (cm.GUI_LAB in node[cm.CLASS])
        #
        # accounted = (is_doc or is_menu or is_kbd or is_std_ref or is_x_ref or is_gui_lab)
        # if not accounted:
        #     dd("NOT ACCOUNTED")
        # else:
        #     dd("is_doc, is_menu, is_kbd, is_std_ref, is_x_ref, is_gui_lab")
        #     dd(is_doc , is_menu , is_kbd , is_std_ref , is_x_ref , is_gui_lab)
        #     orig_msg = node.astext()
        #     dd("text:", orig_msg)
        #     raw_source = self.getNodeMsg(node)
        #     if raw_source:
        #         dd("raw_source:", raw_source)
        #     else:
        #         dd("NO RAW")
        #     trans = None
        #     must_use_raw_source = (raw_source != orig_msg)
        #     if is_menu and must_use_raw_source:
        #         trans = self.transMenuselection(raw_source)
        #     elif is_kbd and must_use_raw_source:
        #         trans = self.trans_keyboard(raw_source)
        #     elif must_use_raw_source:
        #         trans = self.transRef(raw_source)
        #
        #     if trans:
        #         entry={raw_source:trans}
        #         self.node_trans_list.update(entry)
        #     #self.default_translation(orig_msg, keep_orig=True, raw=(raw_source if must_use_raw_source else None))


    def visit_literal(self, node):
        if DEBUG:
            _("visit_literal", node.astext())
        self.setupNodeForTrans(node)
        # raw_source = self.getNodeMsg(node)
        # if raw_source:
        #     dd("raw_source:", raw_source)
        # else:
        #     dd("NO RAW")

    def depart_paragraph(self, node):
        _("depart_paragraph", node.astext())
        msg = node.astext()
        raw_source = self.getNodeMsg(node)
        _("text:", msg)
        _("raw_source:", raw_source)
        trans = str(raw_source)
        for k,v in self.node_trans_list.items():
            trans = trans.replace(k, v)
        self.node_trans_list.clear()
        entry = {raw_source: trans}
        self.node_trans_list.update(entry)
        _('-'*80)
        pp(self.node_trans_list)
        _('-'*80)
        # #exit(0)

    def visit_paragraph(self, node):
        if DEBUG:
            _("visit_paragraph", node.astext())
        # msg = node.astext()
        # dd("text:", msg)
        # raw_source = self.getNodeMsg(node)
        # if raw_source:
        #     dd("raw_source:", raw_source)
        # else:
        #     dd("NO RAW")

        #self.default_translation(node)

    def visit_abbreviation(self, node):
        #:abbr: `POV(Point Of View)`
        if DEBUG:
            _("visit_abbreviation", node.astext())
        self.setupNodeForTrans(node)
        # raw_source = ":abbr:`{} ({})`".format(node.astext(), node.get('explanation'))
        # expl = node.get('explanation')
        # trans = trans_finder.findTranslation(expl)
        # if trans:
        #     trans = "{} -- {}".format(expl, trans)
        # else:
        #     trans = "-- {}".format(expl)
        # trans = raw_source.replace(expl, trans)
        # entry = {raw_source:trans}
        # self.node_trans_list.update(entry)

    # def default_translation(self, node, keep_orig=False, raw=None):
    #     raw_source = None
    #     if raw:
    #         raw_source = raw
    #     else:
    #         raw_source = self.getNodeMsg(node)
    #
    #     orig = node.astext()
    #     trans = trans_finder.findTranslation(orig)
    #     if keep_orig:
    #         if trans:
    #             trans = "{} -- {}".format(orig, trans)
    #         else:
    #             trans = "-- {}".format(orig)
    #
    #     if trans:
    #         trans = raw_source.replace(orig, trans)
    #         entry = {raw_source:trans}
    #         self.node_trans_list.update(entry)

    def invisible_visit(self, node):
        # type: (nodes.Node) -> None
        """Invisible nodes should be ignored."""
        pass
