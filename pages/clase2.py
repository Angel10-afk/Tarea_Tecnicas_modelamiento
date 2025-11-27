import dash
from dash import html, dcc, Input, Output, State, callback
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__, path='/Crecimiento_Logistico', name='Crecimiento Logístico')

# ==========================================
# ESTILOS (DEFINICIÓN EN LÍNEA PARA GARANTIZAR TEMA CLARO)
# ==========================================
ESTILO_CONTENEDOR_INPUT = {
    'backgroundColor': '#f9f9f9',
    'padding': '20px',
    'borderRadius': '10px',
    'border': '1px solid #ddd',
    'marginBottom': '20px',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
}

ESTILO_INPUT = {
    'width': '100%',
    'padding': '8px',
    'borderRadius': '5px',
    'border': '1px solid #ccc',
    'marginTop': '5px',
    'marginBottom': '15px',
    'boxSizing': 'border-box'
}

ESTILO_LABEL = {
    'fontWeight': 'bold',
    'color': 'green',
    'display': 'block'
}

ESTILO_BTN = {
    'backgroundColor': 'green',
    'color': 'white',
    'padding': '10px 20px',
    'border': 'none',
    'borderRadius': '5px',
    'cursor': 'pointer',
    'width': '100%',
    'fontSize': '16px'
}

# ==========================================
# LAYOUT DE LA PÁGINA
# ==========================================
layout = html.Div([
    html.H1("Modelo Logístico de Crecimiento", 
            style={'textAlign': 'center', 'color': 'green', 'fontFamily': 'Arial', 'marginBottom': '30px'}),

    html.Div([
        # --- COLUMNA IZQUIERDA: PARÁMETROS ---
        html.Div([
            html.H3("Parámetros del modelo", style={'color': 'green', 'borderBottom': '2px solid lightpink', 'marginBottom': '15px'}),
            
            html.Div([
                html.Label("Población inicial P(0):", style=ESTILO_LABEL),
                dcc.Input(id="input-p0", type="number", value=20, style=ESTILO_INPUT)
            ]),
            
            html.Div([
                html.Label("Tasa de crecimiento (r):", style=ESTILO_LABEL),
                dcc.Input(id="input-r", type="number", value=0.1, style=ESTILO_INPUT)
            ]),
            
            html.Div([
                html.Label("Capacidad de Carga (K):", style=ESTILO_LABEL),
                dcc.Input(id="input-k", type="number", value=1000, style=ESTILO_INPUT)
            ]),
            
            html.Div([
                html.Label("Tiempo máximo (t):", style=ESTILO_LABEL),
                dcc.Input(id="input-t", type="number", value=100, style=ESTILO_INPUT)
            ]),
            
            html.Button("Generar gráfico", id="btn-generar", style=ESTILO_BTN)
            
        ], style={'flex': '1', 'minWidth': '300px', **ESTILO_CONTENEDOR_INPUT}),
        
        # --- COLUMNA DERECHA: GRÁFICA ---
        html.Div([
            html.Div([
                dcc.Graph(
                    id='grafica-poblacion',
                    style={'height': '500px', 'width': '100%'}
                )
            ], style={'backgroundColor': 'white', 'padding': '10px', 'borderRadius': '10px', 'border': '1px solid #ddd'})
        ], style={'flex': '2', 'minWidth': '400px'})
        
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '30px', 'maxWidth': '1200px', 'margin': '0 auto'})

], style={'padding': '20px', 'backgroundColor': '#f9f9f9', 'minHeight': '100vh', 'fontFamily': 'Arial, sans-serif'})


# ==========================================
# CALLBACKS
# ==========================================
@callback(
    Output('grafica-poblacion', 'figure'),
    Input('btn-generar', 'n_clicks'),
    State('input-p0', 'value'),
    State('input-r', 'value'),
    State('input-k', 'value'),
    State('input-t', 'value'),
    prevent_initial_call=False
)
def actualizar_grafica(n_clicks, P0, r, K, t_max):
    # --- COLORES CLAROS ---
    COLOR_FONDO_PAPEL = 'lightblue'   # Fondo externo del gráfico
    COLOR_FONDO_GRAFICO = 'white'     # Fondo interno (donde van las líneas)
    COLOR_TEXTO = 'black'             # Color de ejes y números
    COLOR_TITULO = 'green'            # Título del gráfico
    COLOR_GRID = 'lightpink'          # Rejilla
    COLOR_DATOS = "#0000FF"           # Azul (Curva)
    COLOR_LIMITE = "#FF8C00"          # Naranja (K)

    # Valores por defecto para evitar errores al cargar
    if P0 is None: P0 = 20
    if r is None: r = 0.1
    if K is None: K = 1000
    if t_max is None: t_max = 100

    # Validación
    if K <= 0 or t_max <= 0 or P0 < 0:
        fig_empty = go.Figure()
        fig_empty.update_layout(
            title="Error: Ingrese valores positivos",
            paper_bgcolor=COLOR_FONDO_PAPEL,
            plot_bgcolor=COLOR_FONDO_GRAFICO,
            font=dict(color=COLOR_TEXTO)
        )
        return fig_empty

    # Cálculo matemático
    t = np.linspace(0, t_max, 200)
    if K == 0:
        P = np.full(200, P0)
    else:
        denominador = (K - P0) + P0 * np.exp(r * t)
        # Evitar división por cero
        with np.errstate(divide='ignore', invalid='ignore'):
             numerador = P0 * K * np.exp(r * t)
             P = np.where(denominador == 0, 0, numerador / denominador)

    # Crear trazos
    trace_poblacion = go.Scatter(
        x=t, y=P,
        mode='lines',
        name='Población P(t)',
        line=dict(color=COLOR_DATOS, width=3),
        hovertemplate='t: %{x:.2f}<br>P(t):%{y:.2f}<extra></extra>'
    )
    
    trace_capacidad = go.Scatter(
        x=[0, t_max], y=[K, K],
        mode='lines',
        name='Capacidad de Carga (K)',
        line=dict(color=COLOR_LIMITE, width=2, dash='dash'),
        hovertemplate='K: %{y:.2f}<extra></extra>'
    )

    fig = go.Figure(data=[trace_poblacion, trace_capacidad])
    
    # Configuración del diseño (Layout)
    fig.update_layout(
        title=dict(
            text='<b>Dinámica Poblacional</b>',
            font=dict(size=20, color=COLOR_TITULO),
            x=0.5, y=0.95
        ),
        xaxis_title='Tiempo (t)',
        yaxis_title='Población',
        margin=dict(l=40, r=40, t=70, b=40),
        
        # APLICACIÓN DE COLORES CLAROS
        paper_bgcolor=COLOR_FONDO_PAPEL,
        plot_bgcolor=COLOR_FONDO_GRAFICO,
        font=dict(color=COLOR_TEXTO),
        
        legend=dict(
            orientation='h',
            yanchor='bottom', y=1.02, xanchor='right', x=1,
            bgcolor='rgba(255,255,255,0.6)'
        )
    )

    # Configuración de Ejes
    estilo_ejes = dict(
        showgrid=True, gridwidth=1, gridcolor=COLOR_GRID,
        zeroline=True, zerolinewidth=1, zerolinecolor='red',
        showline=True, linecolor=COLOR_TEXTO, linewidth=1, mirror=True
    )

    fig.update_xaxes(**estilo_ejes, range=[0, t_max])
    
    y_max = max(K, np.max(P)) * 1.1 if len(P) > 0 else K * 1.1
    if y_max == 0: y_max = 10
    fig.update_yaxes(**estilo_ejes, range=[0, y_max])

    return fig