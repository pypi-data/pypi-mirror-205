#!/usr/bin/env python
import glob
import numpy
from numpy.distutils.core import setup, Extension
import pickle
import get_docstring
from distutils.command.sdist import sdist

# Generate documentation dictionary and save it in "lib/"
docstring = get_docstring.get_docstring()
f = open("lib/docstring_pickle.pkl", "wb")
pickle.dump(docstring, f)
f.close()

ext1 = Extension(name = 'pyslalib.slalib',
                 include_dirs = ['.'],
                 sources = ['slalib.pyf']+\
                           glob.glob("*.f")+\
                           glob.glob("*.F"))

if __name__ == "__main__":
    numpy_version = numpy.__version__
    setup(name = 'pySLALIB',
          description       = "f2py and numpy based wrappers for SLALIB",
          version           = "1.0.7",
          author            = "Scott Ransom",
          author_email      = "sransom@nrao.edu",
          install_requires = ['numpy=={}'.format(numpy_version)],
          tests_require=["unittest-xml-reporting"],
          packages = ['pyslalib'],
          package_dir = {'pyslalib': 'lib'},
          package_data = {'pyslalib': ['docstring_pickle.pkl']},
          ext_modules = [ext1],
          cmdclass={'sdist': sdist},
          )
