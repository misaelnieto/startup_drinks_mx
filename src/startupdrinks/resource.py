from fanstatic import Library, Resource, Group

library = Library('sd_buildout', 'static')

#jQuery
jquery = Resource(library, 'assets/js/jquery/jquery-1.8.0.min.js')

#Twitter bootstrap
bootstrap_css = Resource(library, 'bootstrap/css/bootstrap.css')
bootstrap_responsive_css = Resource(library, 'bootstrap/css/bootstrap-responsive.css')
bootstrap_js = Resource(library, 'bootstrap/js/bootstrap.js')
bootstrap = Group(depends=[bootstrap_css, bootstrap_responsive_css, jquery, bootstrap_js])

#Bootstrap wysihtml5
wysihtml5_js = Resource(library, 'wysihtml5/wysihtml5-0.3.0_rc2.js')
bootstrap_wysihtml5_js = Resource(
    library, 'bootstrap-wysihtml5/bootstrap-wysihtml5-0.0.2.js', 
    depends=[bootstrap])
bootstrap_wysihtml5_css = Resource(
    library, 'bootstrap-wysihtml5/bootstrap-wysihtml5-0.0.2.css', 
    depends=[bootstrap])
bootstrap_wysihtml5 = Group(
    depends=[wysihtml5_js, bootstrap_wysihtml5_js, bootstrap_wysihtml5_css]
)

#These are the specifics of this application
styles_css = Resource(library, 'assets/css/styles.css', depends=[bootstrap_css])
admin_css = Resource(library, 'assets/css/admin.css', depends=[bootstrap_css])
map_init_js = Resource(library, 'assets/js/map_init.js')
map_edit_js = Resource(library, 'assets/js/map_edit.js')
landing_page_js = Resource(library, 'assets/js/landing_page.js', depends=[bootstrap])
wysihtml5_init = Resource(library, 'assets/js/wysihtml5_init.js', depends=[bootstrap_wysihtml5])