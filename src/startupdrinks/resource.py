from fanstatic import Library, Resource, Group

library = Library('sd_buildout', 'static')

#jQuery
jquery = Resource(library, 'assets/js/jquery/jquery-1.8.0.min.js')

#Twitter bootstrap
bootstrap_css = Resource(library, 'bootstrap/css/bootstrap.css')
bootstrap_responsive_css = Resource(library, 'bootstrap/css/bootstrap-responsive.css')
bootstrap_js = Resource(library, 'bootstrap/js/bootstrap.js')
bootstrap = Group(depends=[bootstrap_css, bootstrap_responsive_css, jquery, bootstrap_js])

#These are the specifics of this application
styles_css = Resource(library, 'assets/css/styles.css')
admin_css = Resource(library, 'assets/css/admin.css')
map_init_js = Resource(library, 'assets/js/map_init.js')
