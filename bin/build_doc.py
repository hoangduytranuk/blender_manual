import sys
sys.path.append('/usr/local/lib/python3.8/site-packages')
# sys.path.append('/Users/hoangduytran/blender_manual/potranslate')
# print(f'translation_finder sys.path: {sys.path}')

import os
import re

def build_command(target, build_dir, lang=None):
    lang_opt = []
    if lang:
        lang_opt = ["-D", "language='" + lang + "'"]
        build_dir += "/" + lang
    else:
        build_dir += "/default"

    return ["sphinx-build", "-b", target, "-aE"] + lang_opt + ["source", "build/" + build_dir]

target = 'html'
home_dir = os.environ['HOME']
blender_docs = os.path.join(home_dir, 'blender_docs')

os.chdir(blender_docs)

subprocess.call(build_command(target, build_dir, lang))

subprocess.call(build_command(target, "gettext", "locale"))