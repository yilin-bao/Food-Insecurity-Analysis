# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import sphinx_rtd_theme   
package_path = os.path.abspath("../../")
sys.path.insert(0, package_path)   

# -- Project information -----------------------------------------------------

project = 'Food-Insecurity-Analysis'
copyright = '2022, ECE229 Group 3'
author = 'ECE229 Group 3'

# The full version, including alpha/beta/rc tags
release = 'v4'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

extensions = [    'sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'sphinx.ext.todo',
    'sphinx.ext.ifconfig', 'sphinx.ext.extlinks', 'sphinx.ext.imgmath',
    'sphinx.ext.graphviz', 'sphinx.ext.autosectionlabel']     
   # 'sphinx.ext.autodoc',
    #'sphinx.ext.viewcode',
    #'sphinx.ext.todo',
    # 'sphinx.ext.coverage', 
    # 'sphinx.ext.napoleon',
   #  'sphinx.ext.intersphinx',
   #  'sphinx.ext.mathjax',
   #  'sphinx.ext.ifconfig',
    # 'sphinx.ext.githubpages',
    # 'sphinx.ext.doctest',
    ## 'nbsphinx'    ]
      
import recommonmark
from recommonmark.transform import AutoStructify
source_parsers = {
   '.md': 'recommonmark.parser.CommonMarkParser',
}
source_suffix = ['.rst', '.md']

# Add any paths that contain templates here, relative to this directory.
# html_theme = 'alabaster'		
html_theme = "sphinx_rtd_theme"	 
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]	
html_sidebars = {
        '**': [
            'about.html',
            'navigation.html',
            'relations.html',
            'searchbox.html',
            'donate.html',
            'sidebartoc'

    'recommonmark',
        ]
    }	#

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

#source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'
# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

