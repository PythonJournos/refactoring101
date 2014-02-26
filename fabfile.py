import os

from fabric.api import *


#def readme_to_rst():
#    """
#    Convert README.md to _docs/index.rst for Sphinx.
#    Convert the GitHub-friendly README.md to a Sphinx-friendly reStructured text file.
#    """
#
#    print "Converting markdown to reStructured text."
#
#    # Try to run the pandoc command to convert our file.
#    test_pandoc = os.system('pandoc -s README.md -o _docs/index.rst')
#
#    # If this fails to run for any reason, assume it's not installed and send a nice message.
#    if test_pandoc != 0:
#        print "You don't have pandoc installed! Go get it!\nhttp://johnmacfarlane.net/pandoc/installing.html"
#
#        return False
#
#    return True


def build_sphinx_html():
    """
    Build HTML with Sphinx for our readme.
    Converts _docs/index.rst into a fancy HTML page with search and everything.
    """
    os.system('rm -rf html')
    os.system('cd _docs && make html')

def serve_sphinx():
    """
    Serve Sphinx HTML for Web browsers.
    Runs the Python SimpleHTTPServer on port 8000.
    """
    print "Open a Web browser to http://127.0.0.1:8000/\n"
    os.system('cd html && python -m SimpleHTTPServer')

def bootstrap_docs():
    """
    Setup docs.
    """
    build_sphinx_html()
    serve_sphinx()
