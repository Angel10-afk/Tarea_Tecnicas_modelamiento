import dash
from dash import html, dcc

# Inicializamos la app con soporte para múltiples páginas
app = dash.Dash(__name__, use_pages=True)

# Lista exacta del orden solicitado (nombres tal cual aparecen en register_page)
orden_paginas = [
    "Inicio",
    "Página",
    "Tarea",
    "Crecimiento poblacion logístico",
    "Crecimiento Logistico",
    "Campo Vectorial",
    "Modelo SIR",
    "Proyecto Modelo SIR",
    "Modelo SIR Rumor",
    "Ciclo de Vida Moda Crocs",
    "Comparacion Escenarios"
]

# --- ESTILOS CSS MEJORADOS (DISEÑO CON COLOR) ---

# Estilo de la barra lateral (Sidebar) - TEMA OSCURO
ESTILO_SIDEBAR = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "280px",
    "padding": "2rem 1rem",
    "backgroundColor": "#1a233a",  # Azul oscuro elegante
    "color": "white",              # Texto blanco general
    "boxShadow": "4px 0 10px rgba(0,0,0,0.1)", # Sombra para dar profundidad
    "overflowY": "auto",
    "zIndex": 100
}

# Estilo del contenido principal
ESTILO_CONTENIDO = {
    "marginLeft": "300px",
    "marginRight": "2rem",
    "padding": "2rem 1rem",
    "backgroundColor": "#f4f6f9", # Fondo muy suave para el contenido
    "minHeight": "100vh"
}

# Estilo de los enlaces (Botones del menú) - TIPO TARJETA
ESTILO_LINK = {
    "display": "block",
    "padding": "12px 20px",
    "marginBottom": "12px",
    "color": "#1a233a",            # Texto oscuro para contraste
    "textDecoration": "none",
    "fontSize": "15px",
    "fontWeight": "600",           # Texto un poco más grueso
    "backgroundColor": "#ffffff",  # Fondo blanco para los botones
    "borderRadius": "10px",        # Bordes más redondeados
    "borderLeft": "6px solid #00C851", # Borde verde lateral decorativo
    "boxShadow": "0 4px 6px rgba(0,0,0,0.1)",
    "transition": "transform 0.2s ease-in-out",
    "cursor": "pointer"
}

# --- LÓGICA DEL MENÚ ---
rutas_por_nombre = {
    page["name"]: page["relative_path"]
    for page in dash.page_registry.values()
}

# --- LAYOUT PRINCIPAL ---
app.layout = html.Div([

    # 1. Menú Lateral (Sidebar)
    html.Div([
        html.H2("Navegación", style={'textAlign': 'center', 'color': '#ffffff', 'marginBottom': '30px', 'borderBottom': '1px solid rgba(255,255,255,0.2)', 'paddingBottom': '15px'}),
        
        html.Div([
            # Generación de enlaces con el nuevo estilo
            dcc.Link(
                nombre,
                href=rutas_por_nombre[nombre],
                style=ESTILO_LINK
            )
            for nombre in orden_paginas
            if nombre in rutas_por_nombre
        ])

    ], style=ESTILO_SIDEBAR),

    # 2. Área de Contenido
    html.Div([
        html.H1("Técnicas de Modelamiento Matemático", 
                style={'textAlign': 'center', 'color': '#1a233a', 'fontWeight': 'bold', 'marginBottom': '40px'}),

        dash.page_container
    ], style=ESTILO_CONTENIDO)

])

if __name__ == '__main__':
    app.run(debug=True)