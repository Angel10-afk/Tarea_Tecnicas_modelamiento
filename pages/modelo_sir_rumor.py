import dash
from dash import html, dcc, Input, Output, State, callback
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy.integrate import odeint

# Si usas multipage, mantén esta línea. Si es app única, usa app = dash.Dash(__name__)
dash.register_page(__name__, path='/Modelo_Rumor', name='Modelo SIR Rumor')

# ==========================================
# 1. LÓGICA MATEMÁTICA (MODELO SIR RUMOR)
# ==========================================
def resolver_sir_rumor(N, b, k, S0, I0, R0, t_max, num_puntos=200):
    # Ecuaciones Diferenciales
    def deriv(y, t, N, b, k):
        S, I, R = y
        dSdt = -b * S * I
        dIdt = b * S * I - k * I
        dRdt = k * I
        return dSdt, dIdt, dRdt

    # Vector de tiempo
    t = np.linspace(0, t_max, num_puntos)
    y0 = (S0, I0, R0)
    
    # Resolver EDO
    ret = odeint(deriv, y0, t, args=(N, b, k))
    S, I, R = ret.T
    return t, S, I, R

# ==========================================
# 2. COMPONENTES DE INTERFAZ (ESTILO REUTILIZADO)
# ==========================================
def crear_grupo_input(label_text, input_id, value, min_val=0, step=0.001, tipo="number"):
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
# 3. GENERACIÓN DE GRÁFICOS (COMPARATIVO)
# ==========================================
def crear_figura_comparativa(t, res_a, res_b, k1, k2):
    S1, I1, R1 = res_a
    S2, I2, R2 = res_b

    # --- COLORES Y ESTILO ---
    COLOR_FONDO_PAPEL = 'lightblue'
    COLOR_FONDO_GRAFICO = 'white'
    COLOR_GRID = 'lightpink'
    COLOR_TEXTO_PRINCIPAL = 'green'
    COLOR_TEXTO_SECUNDARIO = 'black'
    
    # Colores de las líneas (Según tu imagen: Azul, Rojo, Verde)
    COLOR_S = "blue"
    COLOR_I = "red"
    COLOR_R = "green"

    # Crear Subplots (1 fila, 2 columnas)
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(f"Escenario A: k={k1} (Baja Racionalidad)", f"Escenario B: k={k2} (Alta Racionalidad)"),
        horizontal_spacing=0.1
    )

    # --- GRÁFICO IZQUIERDO (ESCENARIO A) ---
    fig.add_trace(go.Scatter(x=t, y=S1, mode='lines', name='Ignoran (S)', line=dict(color=COLOR_S, width=2), legendgroup='1'), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=I1, mode='lines', name='Propagan (I)', line=dict(color=COLOR_I, width=2), legendgroup='1'), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=R1, mode='lines', name='Racionales (R)', line=dict(color=COLOR_R, width=2), legendgroup='1'), row=1, col=1)

    # --- GRÁFICO DERECHO (ESCENARIO B) ---
    # Usamos dash='dash' para diferenciar o mantener sólido según preferencia (en tu imagen B es dashed)
    fig.add_trace(go.Scatter(x=t, y=S2, mode='lines', name='Ignoran (S)', line=dict(color=COLOR_S, width=2, dash='dash'), showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=t, y=I2, mode='lines', name='Propagan (I)', line=dict(color=COLOR_I, width=2, dash='dash'), showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x=t, y=R2, mode='lines', name='Racionales (R)', line=dict(color=COLOR_R, width=2, dash='dash'), showlegend=False), row=1, col=2)

    # Configuración del Layout
    fig.update_layout(
        title=dict(
            text='<b>Comparación de Propagación del Rumor</b>',
            font=dict(size=20, color=COLOR_TEXTO_PRINCIPAL),
            x=0.5, y=0.95
        ),
        margin=dict(l=40, r=40, t=80, b=40),
        paper_bgcolor=COLOR_FONDO_PAPEL,
        plot_bgcolor=COLOR_FONDO_GRAFICO,
        font=dict(family='Outfit, Arial, sans-serif', size=12, color=COLOR_TEXTO_SECUNDARIO),
        legend=dict(orientation='h', yanchor='bottom', y=-0.2, x=0.5, xanchor='center'),
        hovermode="x unified"
    )

    # Estilo de los ejes
    estilo_ejes = dict(
        showgrid=True, gridwidth=1, gridcolor=COLOR_GRID,
        zeroline=True, zerolinewidth=1, zerolinecolor='gray',
        showline=True, linecolor=COLOR_TEXTO_SECUNDARIO, linewidth=1, mirror=True
    )

    fig.update_xaxes(**estilo_ejes, title_text="Días")
    fig.update_yaxes(**estilo_ejes, title_text="Personas", row=1, col=1)
    fig.update_yaxes(**estilo_ejes, row=1, col=2)

    return fig

# ==========================================
# 4. LAYOUT
# ==========================================
layout = html.Div([
    
    html.H1("Simulación: Modelo SIR para un Rumor", 
            style={'textAlign': 'center', 'color': 'green', 'marginBottom': '30px'}),

    html.Div([
        # --- COLUMNA IZQUIERDA: CONTROLES ---
        html.Div([
            html.H3("Parámetros Generales", style={'color': 'green', 'borderBottom': '2px solid lightpink', 'marginBottom': '15px'}),
            
            crear_grupo_input("Población Total (N):", "input-N", value=275, step=1),
            crear_grupo_input("Tasa de Transmisión (b):", "input-b", value=0.004, step=0.0001),
            crear_grupo_input("Días a simular:", "input-days", value=15, step=1),

            html.H4("Comparación de Racionalidad (k)", style={'color': 'green', 'marginTop': '20px'}),
            crear_grupo_input("Escenario A - k1:", "input-k1", value=0.01, step=0.01),
            crear_grupo_input("Escenario B - k2:", "input-k2", value=0.02, step=0.01),

            html.H4("Condiciones Iniciales", style={'color': 'green', 'marginTop': '20px'}),
            crear_grupo_input("Propagadores Iniciales (I0):", "input-I0", value=1, step=1),
            crear_grupo_input("Racionales Iniciales (R0):", "input-R0", value=8, step=1),
            
            html.Button("Simular Rumor", id="btn-simular-rumor", 
                        style={'backgroundColor': 'green', 'color': 'white', 'padding': '12px', 'width': '100%', 'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer', 'marginTop': '15px', 'fontSize': '16px'})
        ], style={'flex': '1', 'minWidth': '300px', 'padding': '25px', 'backgroundColor': '#f9f9f9', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
        
        # --- COLUMNA DERECHA: GRÁFICO ---
        html.Div([
            dcc.Graph(
                id='grafica-rumor',
                style={'height': '600px', 'width': '100%'}
            ),
            html.Div(id='stats-output', style={'marginTop': '20px', 'padding': '10px', 'backgroundColor': 'white', 'borderRadius': '5px'})
        ], style={'flex': '3', 'minWidth': '500px', 'padding': '10px'})
        
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '30px', 'maxWidth': '1400px', 'margin': '0 auto'})
    
], style={'padding': '20px', 'fontFamily': 'Outfit, sans-serif'})

# ==========================================
# 5. CALLBACKS
# ==========================================
@callback(
    [Output('grafica-rumor', 'figure'),
     Output('stats-output', 'children')],
    Input('btn-simular-rumor', 'n_clicks'),
    State('input-N', 'value'),
    State('input-b', 'value'),
    State('input-k1', 'value'),
    State('input-k2', 'value'),
    State('input-I0', 'value'),
    State('input-R0', 'value'),
    State('input-days', 'value'),
    prevent_initial_call=False
)
def actualizar_grafica_rumor(n_clicks, N, b, k1, k2, I0, R0, days):
    # Valores por defecto
    if N is None: N = 275
    if b is None: b = 0.004
    if k1 is None: k1 = 0.01
    if k2 is None: k2 = 0.02
    if I0 is None: I0 = 1
    if R0 is None: R0 = 8
    if days is None: days = 15

    # Calcular Susceptibles Iniciales
    S0 = N - I0 - R0

    # Simular Escenario A
    t, S1, I1, R1 = resolver_sir_rumor(N, b, k1, S0, I0, R0, days)
    # Simular Escenario B
    _, S2, I2, R2 = resolver_sir_rumor(N, b, k2, S0, I0, R0, days)

    # Crear Figura
    fig = crear_figura_comparativa(t, (S1, I1, R1), (S2, I2, R2), k1, k2)

    # Estadísticas básicas
    max_I1 = max(I1)
    dia_max_I1 = t[np.argmax(I1)]
    max_I2 = max(I2)
    dia_max_I2 = t[np.argmax(I2)]

    stats = html.Div([
        html.H4("Análisis Rápido:", style={'color': 'green'}),
        html.P(f"Escenario A (k={k1}): Pico de propagadores ({max_I1:.0f}) en el día {dia_max_I1:.1f}."),
        html.P(f"Escenario B (k={k2}): Pico de propagadores ({max_I2:.0f}) en el día {dia_max_I2:.1f}.")
    ])

    return fig, stats