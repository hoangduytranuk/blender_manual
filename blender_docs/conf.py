import sys, os
sys.path.append(os.path.abspath('sphinxext'))
print("CURRENT sys.path:{}".format(sys.path))

language = 'vi'
locale_dirs = ['locale/']
gettext_compact = True

extensions = ['HDTextname']


#autodoc_default_flags = ['members', 'private-members', 'special-members',
                         ##'undoc-members',
                         #'show-inheritance']

#def autodoc_skip_member(app, what, name, obj, skip, options):
    #exclusions = ('__weakref__',  # special-members
                  #'__doc__', '__module__', '__dict__',  # undoc-members
                  #)
    #print("")
    #exclude = name in exclusions
    #return skip or exclude

#def setup(app):
    #app.connect('autodoc-skip-member', autodoc_skip_member)

#def maybe_skip_member(app, what, name, obj, skip, options):
    #print "app:{}, what:{}, name:{}, obj:{}, skip:{}, options:{}".format(app, what, name, obj, skip, options)
    #return True

#def source_read_function(app, docname, source):
    #print "app:{}, docname:{}, source:{}".format(app, docname, source)

#def setup(app):
    #print("READING SETUP(APP) here!!!!")
    #exit(0)
    ##app.connect('autodoc-skip-member', maybe_skip_member)
    #app.connect('source-read', source_read_function)
