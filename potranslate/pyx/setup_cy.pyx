from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import build_ext, cythonize

# ext_modules = [
#     Extension('translation_finder_cy', 'translation_finder_cy.pyx'),
#     Extension('paragraph_cy', 'paragraph_cy.pyx')
# ]
#
# setup(
#     name='TranslationProject',
#     cmdclass={'build_ext': build_ext},
#     ext_modules=ext_modules,
# )

setup(
    name='TranslationProject',
    ext_modules=cythonize(['*.pyx'])
)