from dash_extensions.enrich import DashProxy, page_registry
from dash_extensions.snippets import fix_page_load_anchor_issue
from utils.markdown import register_pages
from utils.ui import create_app_shell

css = ["https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.Default.css",
       "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"]
app = DashProxy(__name__, use_pages=True, update_title=None, suppress_callback_exceptions=True, external_stylesheets=css)
# Register component blueprints.
register_pages(app, "content", order=0)
register_pages(app, "ui_layers", order=10)
register_pages(app, "raster_layers", order=20)
register_pages(app, "vector_layers", order=30)
register_pages(app, "controls", order=40)
register_pages(app, "components", order=50)
register_pages(app, "misc", order=50)
# register_pages(app, "tutorials", order=30)
# Bind layout.
app.layout = create_app_shell(page_registry.values(), [])
# Make server available for gunicorn.
server = app.server

if __name__ == '__main__':
    app.run_server(port=7879)
