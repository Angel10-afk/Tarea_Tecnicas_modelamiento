import dash
from dash import html, dcc, Input, Output, State, callback
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__, path='/Crecimiento_poblacion', name='Crecimiento poblacion logístico')

# ==========================================
# 1. LÓGICA MATEMÁTICA
# ==========================================
def calcular_crecimiento_logistico(P0, r, K, t_max, num_puntos=200):
    t = np.linspace(0, t_max, num_puntos)
    if K == 0:
        return t, np.full(num_puntos, P0)
    denominador = (K - P0) + P0 * np.exp(r * t)
    if np.any(denominador == 0):
        return t, np.zeros(num_puntos)
    numerador = P0 * K * np.exp(r * t)
    P = numerador / denominador
    return t, P

# ==========================================
# 2. COMPONENTES DE INTERFAZ (ESTILO MEJORADO)
# ==========================================
def crear_grupo_input(label_text, input_id, value, min_val=0, step=1, tipo="number"):
    return html.Div([
        html.Label(label_text, style={'fontWeight': 'bold', 'color': 'green', 'fontSize': '14px'}),
        dcc.Input(
            id=input_id,
            type=tipo,
            value=value,
            min=min_val,
            step=step,
            className="input-field",
            style={
                'width': '100%', 
                'padding': '8px', 
                'borderRadius': '5px',
                'border': '1px solid #ccc', 
                'marginTop': '5px', 
                'marginBottom': '15px',
                'boxSizing': 'border-box',
                'backgroundColor': 'white',
                'color': 'black'
            }
        )
    ])

# ==========================================
# 3. GENERACIÓN DE GRÁFICOS (ESTILO CLARO)
# ==========================================
def crear_figura_logistica(t, P, K, t_max):
    # --- COLORES CLAROS (ESTILO CIENTÍFICO) ---
    COLOR_FONDO_PAPEL = 'lightblue'  # Fondo exterior
    COLOR_FONDO_GRAFICO = 'white'    # Fondo interior
    COLOR_GRID = 'lightpink'         # Rejilla
    COLOR_TEXTO_PRINCIPAL = 'green'  # Títulos
    COLOR_TEXTO_SECUNDARIO = 'black' # Ejes y leyendas
    COLOR_ZEROLINE = 'red'           # Línea cero
    
    COLOR_DATOS = "#0000FF"          # Azul fuerte para la curva
    COLOR_LIMITE = "#FF8C00"         # Naranja para la asíntota (K)

    fig = go.Figure()

    # Curva de Población
    fig.add_trace(go.Scatter(
        x=t, y=P,
        mode='lines',
        name='Población P(t)',
        line=dict(color=COLOR_DATOS, width=3),
        hovertemplate='t: %{x:.2f}<br>P(t):%{y:.2f}<extra></extra>'
    ))
    
    # Línea de Capacidad de Carga
    fig.add_trace(go.Scatter(
        x=[0, t_max], y=[K, K],
        mode='lines',
        name='Capacidad de Carga (K)',
        line=dict(color=COLOR_LIMITE, width=2, dash='dash'),
        hovertemplate='K: %{y:.2f}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(
            text='<b>Modelo Logístico de Crecimiento</b>',
            font=dict(size=20, color=COLOR_TEXTO_PRINCIPAL),
            x=0.5, y=0.95
        ),
        xaxis_title='Tiempo (t)',
        yaxis_title='Población P(t)',
        margin=dict(l=40, r=40, t=70, b=40),
        
        # APLICACIÓN DE COLORES CLAROS
        paper_bgcolor=COLOR_FONDO_PAPEL,
        plot_bgcolor=COLOR_FONDO_GRAFICO,
        font=dict(family='Outfit, Arial, sans-serif', size=12, color=COLOR_TEXTO_SECUNDARIO),
        
        legend=dict(
            orientation='h', yanchor='bottom', y=1.02, x=0,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='lightgray', borderwidth=1
        ),
        hovermode="x unified"
    )
    
    # Configuración de Ejes (Grid Rosa)
    estilo_ejes = dict(
        showgrid=True, gridwidth=1, gridcolor=COLOR_GRID,
        zeroline=True, zerolinewidth=2, zerolinecolor=COLOR_ZEROLINE,
        showline=True, linecolor=COLOR_TEXTO_SECUNDARIO, linewidth=2, mirror=True
    )
    
    fig.update_xaxes(**estilo_ejes, range=[0, t_max])
    
    y_max = max(K, np.max(P)) * 1.1 if len(P) > 0 else K * 1.1
    if y_max == 0: y_max = 10
    fig.update_yaxes(**estilo_ejes, range=[0, y_max])
    
    return fig

# ==========================================
# 4. LAYOUT
# ==========================================
layout = html.Div([
    
    html.H1("Simulación de Crecimiento Poblacional", 
            style={'textAlign': 'center', 'color': 'green', 'marginBottom': '30px'}),

    html.Div([
        # --- COLUMNA IZQUIERDA: CONTROLES ---
        html.Div([
            html.H3("Parámetros", style={'color': 'green', 'borderBottom': '2px solid lightpink', 'marginBottom': '20px'}),
            html.P("Ajuste las variables de la ecuación diferencial logística:", style={'fontSize': '14px', 'marginBottom': '20px'}),
            
            crear_grupo_input("Población inicial P(0):", "input-p0", value=20, step=1),
            crear_grupo_input("Tasa de crecimiento (r):", "input-r", value=0.1, step=0.01),
            crear_grupo_input("Capacidad de Carga (K):", "input-k", value=1000, step=10),
            crear_grupo_input("Tiempo máximo (t):", "input-t", value=100, step=5),
            
            html.Button("Actualizar Gráfico", id="btn-generar", 
                        style={'backgroundColor': 'green', 'color': 'white', 'padding': '12px', 'width': '100%', 'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer', 'marginTop': '10px', 'fontSize': '16px'})
        ], style={'flex': '1', 'minWidth': '300px', 'padding': '25px', 'backgroundColor': '#f9f9f9', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
        
        # --- COLUMNA DERECHA: GRÁFICO ---
        html.Div([
            dcc.Graph(
                id='grafica-poblacion_2',
                style={'height': '500px', 'width': '100%'}
            )
        ], style={'flex': '2', 'minWidth': '400px', 'padding': '10px'})
        
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '30px', 'maxWidth': '1200px', 'margin': '0 auto'})
    
], style={'padding': '20px', 'fontFamily': 'Outfit, sans-serif'})

# ==========================================
# 5. CALLBACKS
# ==========================================
@callback(
    Output('grafica-poblacion_2', 'figure'),
    Input('btn-generar', 'n_clicks'),
    State('input-p0', 'value'),
    State('input-r', 'value'),
    State('input-k', 'value'),
    State('input-t', 'value'),
    prevent_initial_call=False
)
def actualizar_grafica(n_clicks, P0, r, K, t_max):
    # Valores por defecto para evitar errores al inicio
    if P0 is None: P0 = 20
    if r is None: r = 0.1
    if K is None: K = 1000
    if t_max is None: t_max = 100

    if K <= 0 or t_max <= 0 or P0 < 0:
        fig_empty = go.Figure()
        fig_empty.update_layout(
            title="Error: Ingrese valores positivos",
            paper_bgcolor='lightblue',
            plot_bgcolor='white',
             font=dict(color='black')
        )
        return fig_empty
        
    t, P = calcular_crecimiento_logistico(P0, r, K, t_max)
    fig = crear_figura_logistica(t, P, K, t_max)
    return fig