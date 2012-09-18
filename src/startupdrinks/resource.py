from fanstatic import Library, Resource, Group
from js.jquery import jquery

library = Library('sd_buildout', 'static')

#Twitter bootstrap
bootstrap_css = Resource(library, 'bootstrap/css/bootstrap.css')
bootstrap_js = Resource(library, 'bootstrap/js/bootstrap.js')
bootstrap = Group(depends=[bootstrap_css, jquery,bootstrap_js])

styles_css = Resource(library, 'styles.css')
