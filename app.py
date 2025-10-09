import dash
from dash import html, dcc

app = dash.Dash(__name__, use_pages=True)


orden_paginas = ["Inicio", "Página", "Tarea"]

app.layout = html.Div([
    html.H1("Técnicas de Modelamiento Matemático", className='app-header'),

    html.Div([
        html.Div([
            html.Div(
                dcc.Link(
                    f"{page['name']}",
                    href=page["relative_path"],
                    className='nav-link'
                )
            )
            for page in sorted(
                dash.page_registry.values(),
                key=lambda p: orden_paginas.index(p["name"]) if p["name"] in orden_paginas else 999
            )
        ], className='nav-links')
    ], className='navigation'),

    dash.page_container
], className='app-container')

if __name__ == '__main__':
    app.run(debug=True)
