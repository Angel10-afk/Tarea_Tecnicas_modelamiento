import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__, path='/inicio', name='Inicio')

# ==========================================
# 1. MODELOS MATEMÁTICOS (Gráficos Interactivos)
# ==========================================

# --- Modelo A: Espiral (Tu código original mejorado) ---
t = np.linspace(0, 10 * np.pi, 500)
x = np.sin(t) * np.exp(-0.05 * t)
y = np.cos(t) * np.exp(-0.05 * t)

fig_spiral = go.Figure()
fig_spiral.add_trace(go.Scatter(
    x=x, y=y, mode='lines', 
    line=dict(width=4, color='#6200ea'), # Color violeta intenso
    name='Trayectoria'
))
fig_spiral.update_layout(
    title='<b>Espiral Paramétrica</b>',
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=20, r=20, t=40, b=20), height=300
)

# --- Modelo B: Superficie 3D (Optimización) ---
x_3d = np.linspace(-3, 3, 50)
y_3d = np.linspace(-3, 3, 50)
X, Y = np.meshgrid(x_3d, y_3d)
Z = np.sin(np.sqrt(X**2 + Y**2))

fig_3d = go.Figure(data=[go.Surface(z=Z, colorscale='Viridis')])
fig_3d.update_layout(
    title='<b>Optimización 3D</b>',
    margin=dict(l=0, r=0, t=40, b=0),
    paper_bgcolor='rgba(0,0,0,0)', height=300,
    scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z')
)

# --- Modelo C: Predador-Presa (Simulación Temporal) ---
time = np.linspace(0, 15, 100)
prey = 10 + 5 * np.sin(time)
predator = 5 + 4 * np.sin(time - 1.5)

fig_bio = go.Figure()
fig_bio.add_trace(go.Scatter(x=time, y=prey, name='Presas', line=dict(color='#00c853')))
fig_bio.add_trace(go.Scatter(x=time, y=predator, name='Depredadores', line=dict(color='#d50000', dash='dot')))
fig_bio.update_layout(
    title='<b>Dinámica de Poblaciones</b>',
    plot_bgcolor='rgba(240,240,240,0.5)', paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=20, r=20, t=40, b=20), height=300
)

# ==========================================
# 2. ESTILOS CSS
# ==========================================
style_card = {
    'backgroundColor': 'white', 'borderRadius': '15px', 'padding': '25px',
    'boxShadow': '0 4px 15px rgba(0,0,0,0.1)', 'flex': '1', 'minWidth': '300px',
    'textAlign': 'center', 'transition': 'transform 0.3s'
}

style_img_container = {
    'width': '45%', 'minWidth': '300px', 'backgroundColor': 'white',
    'padding': '15px', 'borderRadius': '10px', 'boxShadow': '0 2px 5px rgba(0,0,0,0.05)',
    'textAlign': 'center'
}

# ==========================================
# 3. LAYOUT DE LA PÁGINA
# ==========================================
layout = html.Div([
    
    # --- HERO HEADER (Encabezado) ---
    html.Div([
        # Logo o Icono Principal
        html.Img(src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg", 
                 style={'width': '80px', 'marginBottom': '10px'}),
        html.H1("Portafolio de Modelamiento", style={'color': 'white', 'margin': '0'}),
        html.H3("Angel Meza | Computación Científica", style={'color': '#d1c4e9', 'fontWeight': '300'}),
    ], style={
        'background': 'linear-gradient(135deg, #4a148c 0%, #7c43bd 100%)', # Degradado morado
        'padding': '60px 20px 80px 20px', 'textAlign': 'center', 'borderRadius': '0 0 50px 50px'
    }),

    # --- CONTENEDOR PRINCIPAL ---
    html.Div([
        
        # --- SECCIÓN: INFORMACIÓN (Tarjetas Superpuestas) ---
        html.Div([
            # Tarjeta 1: Sobre Mí
            html.Div([
                # IMAGEN 1: Icono de Estudiante
                html.Img(src="https://cdn-icons-png.flaticon.com/512/5775/5775807.png", style={'width': '90px', 'marginBottom': '15px'}),
                html.H2("Sobre Mí", style={'color': '#4a148c', 'fontSize': '24px'}),
                html.P("Soy Angel Meza, estudiante de Computación Científica. En este curso de Técnicas de Modelamiento, aprendo a traducir el mundo real al lenguaje de las matemáticas.", 
                       style={'textAlign': 'justify', 'color': '#555', 'lineHeight': '1.6'})
            ], style=style_card),

            # Tarjeta 2: Objetivos
            html.Div([
                # IMAGEN 2: Icono de Análisis
                html.Img(src="https://cdn-icons-png.flaticon.com/512/3202/3202926.png", style={'width': '90px', 'marginBottom': '15px'}),
                html.H2("Objetivos del Curso", style={'color': '#004aad', 'fontSize': '24px'}),
                html.Ul([
                    html.Li("Simulación de sistemas complejos."),
                    html.Li("Optimización y cálculo numérico."),
                    html.Li("Visualización de datos científicos."),
                ], style={'textAlign': 'left', 'color': '#555', 'lineHeight': '1.8'})
            ], style=style_card),
        ], style={'display': 'flex', 'gap': '30px', 'flexWrap': 'wrap', 'marginTop': '-50px', 'padding': '0 20px'}),

        # --- SECCIÓN: GALERÍA DE MODELOS INTERACTIVOS ---
        html.H2("Mis Modelos Interactivos", style={'textAlign': 'center', 'color': '#333', 'marginTop': '60px'}),
        html.Div([
            html.Div([dcc.Graph(figure=fig_spiral, config={'displayModeBar': False})], style=style_card),
            html.Div([dcc.Graph(figure=fig_3d, config={'displayModeBar': False})], style=style_card),
            html.Div([dcc.Graph(figure=fig_bio, config={'displayModeBar': False})], style=style_card),
        ], style={'display': 'flex', 'gap': '20px', 'flexWrap': 'wrap', 'padding': '20px'}),

        # --- SECCIÓN: CONCEPTOS TEÓRICOS (Imágenes Estáticas) ---
       
    ], style={'maxWidth': '1200px', 'margin': '0 auto', 'fontFamily': 'Segoe UI, Roboto, Helvetica, Arial, sans-serif'}),

    # --- FOOTER ---
    html.Footer("© 2024 Angel Meza | Facultad de Ciencias", 
                style={'textAlign': 'center', 'padding': '30px', 'color': '#888', 'fontSize': '14px', 'marginTop': '20px'})
])