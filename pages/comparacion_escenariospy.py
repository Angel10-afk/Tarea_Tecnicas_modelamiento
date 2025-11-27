import dash
from dash import html, dcc, Input, Output, State, callback
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy.integrate import odeint

# Configuración de la app (ajustar según tu estructura de proyecto)
dash.register_page(__name__, path='/comparacion_escenarios', name='Comparacion Escenarios')

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
# 2. COMPONENTES DE INTERFAZ
# ==========================================
def crear_grupo_input(label_text, input_id, value, min_val=0, step=0.0001, tipo="number"):
    return html.Div([
        html.Label(label_text, style={'fontWeight': 'bold', 'color': '#333', 'fontSize': '14px'}),
        dcc.Input(
            id=input_id,
            type=tipo,
            value=value,
            min=min_val,
            step=step,
            style={
                'width': '100%', 'padding': '8px', 'borderRadius': '5px',
                'border': '1px solid #ccc', 'marginTop': '5px', 'marginBottom': '15px'
            }
        )
    ])

# ==========================================
# 3. GENERACIÓN DE GRÁFICOS (REPLICA EXACTA)
# ==========================================
def crear_figura_replica(t, res_a, res_b, k1, k2):
    S1, I1, R1 = res_a
    S2, I2, R2 = res_b

    # Colores exactos de la imagen
    c_potenciales = "#636EFA"  # Azul similar a la imagen (Plotly default blue es cercano)
    c_activos = "red"          # Rojo brillante
    c_aburridos = "#66AA66"    # Verde suave similar a la imagen

    # Nombres de leyenda
    l_s = "Potenciales (S)"
    l_i = "Usuarios Activos (I)"
    l_r = "Aburridos (R)"

    # Crear Subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Escenario A: Tendencia Viral", "Escenario B: Tendencia Fallida"),
        horizontal_spacing=0.1
    )

    # --- ESCENARIO A (Izquierda - Líneas Sólidas) ---
    fig.add_trace(go.Scatter(x=t, y=S1, mode='lines', name=l_s, line=dict(color=c_potenciales, width=2.5)), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=I1, mode='lines', name=l_i, line=dict(color=c_activos, width=2.5)), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=R1, mode='lines', name=l_r, line=dict(color=c_aburridos, width=2.5)), row=1, col=1)

    # Anotación Pico Escenario A
    peak_idx_a = np.argmax(I1)
    peak_val_a = I1[peak_idx_a]
    peak_day_a = t[peak_idx_a]
    
    fig.add_annotation(
        x=peak_day_a + 10, y=peak_val_a + 50, # Ajuste de posición visual
        text=f"Pico: {int(peak_val_a)} usuarios",
        showarrow=False,
        font=dict(color="red", size=12),
        row=1, col=1
    )

    # --- ESCENARIO B (Derecha - Líneas Discontinuas) ---
    fig.add_trace(go.Scatter(x=t, y=S2, mode='lines', name=l_s, line=dict(color=c_potenciales, width=2, dash='dash'), showlegend=True), row=1, col=2)
    fig.add_trace(go.Scatter(x=t, y=I2, mode='lines', name=l_i, line=dict(color=c_activos, width=2, dash='dash'), showlegend=True), row=1, col=2)
    fig.add_trace(go.Scatter(x=t, y=R2, mode='lines', name=l_r, line=dict(color=c_aburridos, width=2, dash='dash'), showlegend=True), row=1, col=2)

    # Anotación Pico Escenario B
    peak_idx_b = np.argmax(I2)
    peak_val_b = I2[peak_idx_b]
    
    fig.add_annotation(
        x=35, y=peak_val_b + 100, # Posición arbitraria centrada como en la imagen
        text=f"Pico: {int(peak_val_b)} usuarios",
        showarrow=False,
        font=dict(color="red", size=12),
        row=1, col=2
    )

    # Configuración de Layout para igualar imagen
    fig.update_layout(
        template='simple_white', # Fondo blanco limpio
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(
            orientation="v", 
            yanchor="top", y=0.6, 
            xanchor="right", x=0.95,
            bgcolor='rgba(255,255,255,0.5)'
        ),
        font=dict(family='Arial', size=12)
    )

    # Grid ligero (como en la imagen ggplot/seaborn style)
    grid_style = dict(showgrid=True, gridwidth=1, gridcolor='#EEEEEE')
    
    fig.update_xaxes(**grid_style, title_text="Días")
    fig.update_yaxes(**grid_style, title_text="Estudiantes", row=1, col=1)
    fig.update_yaxes(**grid_style, row=1, col=2)

    return fig

# ==========================================
# 4. LAYOUT PRINCIPAL
# ==========================================
layout = html.Div([
    html.H2("Simulación: Propagación de un Rumor", style={'textAlign': 'center', 'marginBottom': '30px'}),

    html.Div([
        # Panel de Control
        html.Div([
            html.H4("Parámetros", style={'borderBottom': '2px solid #eee', 'paddingBottom': '10px'}),
            
            # Valores ajustados para replicar la imagen por defecto
            crear_grupo_input("Población Total (N):", "input-N", value=1000, step=10),
            crear_grupo_input("Tasa Transmisión (b):", "input-b", value=0.001, step=0.0001),
            crear_grupo_input("Días:", "input-days", value=60, step=1),
            
            html.Hr(),
            html.Label("Nivel de 'Aburrimiento/Racionalidad' (k)", style={'fontWeight': 'bold'}),
            crear_grupo_input("Escenario A (Viral) - k1:", "input-k1", value=0.2, step=0.01),
            crear_grupo_input("Escenario B (Fallido) - k2:", "input-k2", value=1.5, step=0.01),

            html.Hr(),
            crear_grupo_input("Propagadores Iniciales (I0):", "input-I0", value=10, step=1),
            
            html.Button("Actualizar Gráfica", id="btn-simular", 
                        style={'backgroundColor': '#444', 'color': 'white', 'padding': '10px', 'width': '100%', 'marginTop': '10px'})

        ], style={'flex': '1', 'minWidth': '250px', 'padding': '20px', 'backgroundColor': '#f5f5f5', 'borderRadius': '8px'}),

        # Panel de Gráfica
        html.Div([
            dcc.Graph(id='grafica-replica', style={'height': '500px'})
        ], style={'flex': '4', 'minWidth': '500px'})

    ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px'})
], style={'padding': '20px', 'fontFamily': 'Arial, sans-serif'})

# ==========================================
# 5. CALLBACKS
# ==========================================
@callback(
    Output('grafica-replica', 'figure'),
    Input('btn-simular', 'n_clicks'),
    State('input-N', 'value'),
    State('input-b', 'value'),
    State('input-k1', 'value'),
    State('input-k2', 'value'),
    State('input-I0', 'value'),
    State('input-days', 'value'),
)
def actualizar_grafica(n_clicks, N, b, k1, k2, I0, days):
    # Valores por defecto para la primera carga si son None
    N = N or 1000
    b = b or 0.001
    k1 = k1 or 0.2
    k2 = k2 or 1.5
    I0 = I0 or 10
    days = days or 60
    
    # Asumimos R0 inicial = 0
    R_init = 0
    S0 = N - I0 - R_init

    # Simular
    t, S1, I1, R1 = resolver_sir_rumor(N, b, k1, S0, I0, R_init, days)
    _, S2, I2, R2 = resolver_sir_rumor(N, b, k2, S0, I0, R_init, days)

    # Crear Figura
    return crear_figura_replica(t, (S1, I1, R1), (S2, I2, R2), k1, k2)