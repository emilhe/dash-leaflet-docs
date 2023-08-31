from dash_extensions.enrich import DashProxy, page_registry
from utils.markdown import register_pages
from utils.patches import unique_map
from utils.ui import create_app_shell, fix_page_load_anchor_issue

js = ["https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"]
css = ["https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.Default.css",
       "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"]
app = DashProxy(__name__, use_pages=True, update_title=None, suppress_callback_exceptions=True,
                external_stylesheets=css, external_scripts=js, prevent_initial_callbacks=True)
# Apply patches.
unique_map()
# Register markdown pages.
register_pages(app, "docs")
register_pages(app, "components")
for sub_dir in ["ui_layers", "raster_layers", "vector_layers", "controls", "misc"]:
    register_pages(app, f"components/{sub_dir}")
# Bind layout.
app.layout = create_app_shell(page_registry.values(), fix_page_load_anchor_issue(app, delay=500))
# Make server available for gunicorn.
server = app.server

if __name__ == '__main__':
    app.run_server(port=7879)
