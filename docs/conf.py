# Basic information
project = "Tokki"
copyright = "2019 Hannele Ruiz"
author = "Hannele Ruiz"


# The extensions that are going to be loaded
extensions = [
    "sphinx.ext.autodoc"
]

# Stuff to ignore when we are looking for documentation
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
# Files to be included in the output
html_static_path = ["_static"]


# The Theme to use for the HTTP content
# This is required for Read the Docs
html_theme = "sphinx_rtd_theme"
# Custom CSS files to use
html_css_files = [
    "tokki.css"
]
