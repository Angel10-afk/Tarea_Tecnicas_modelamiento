import dash
from dash import html, dcc, Input, Output, State, callback
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint

# Registro de la página (si usas multipage)
dash.register_page(__name__, path='/Moda_Crocs', name='Ciclo de Vida Moda Crocs')

# ==========================================
# 1. LÓGICA MATEMÁTICA (MODELO SIR)
# ==========================================
def calcular_moda_sir(N, b, k, I0, t_max, num_puntos=200):
    # Definición de las ecuaciones diferenciales
    def deriv(y, t, N, b, k):
        S, I, R = y
        dSdt = -b * S * I
        dIdt = b * S * I - k * I
        dRdt = k * I
        return dSdt, dIdt, dRdt

    # Condiciones iniciales
    S0 = N - I0
    R0 = 0
    y0 = (S0, I0, R0)
    
    # Vector de tiempo
    t = np.linspace(0, t_max, num_puntos)
    
    # Resolver EDO
    ret = odeint(deriv, y0, t, args=(N, b, k))
    S, I, R = ret.T
    
    return t, S, I, R

# ==========================================
# 2. COMPONENTES DE INTERFAZ (ESTILO DEL ARCHIVO ORIGINAL)
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
def crear_figura_moda(t, S, I, R, t_max):
    # --- COLORES CLAROS (ESTILO CIENTÍFICO) ---
    COLOR_FONDO_PAPEL = 'lightblue'  # Fondo exterior
    COLOR_FONDO_GRAFICO = 'white'    # Fondo interior
    COLOR_GRID = 'lightpink'         # Rejilla
    COLOR_TEXTO_PRINCIPAL = 'green'  # Títulos
    COLOR_TEXTO_SECUNDARIO = 'black' # Ejes y leyendas
    COLOR_ZEROLINE = 'red'           # Línea cero
    
    # Colores específicos para las curvas SIR (Azul, Rojo, Verde)
    COLOR_S = "blue"
    COLOR_I = "red"
    COLOR_R = "green"

    fig = go.Figure()

    # Curva S: Susceptibles
    fig.add_trace(go.Scatter(
        x=t, y=S,
        mode='lines',
        name='S: No tiene (Susceptible)',
        line=dict(color=COLOR_S, width=3),
        hovertemplate='Día: %{x:.1f}<br>S: %{y:.0f}<extra></extra>'
    ))
    
    # Curva I: Infectados (Usuarios de Crocs)
    fig.add_trace(go.Scatter(
        x=t, y=I,
        mode='lines',
        name='I: Usa Crocs (Infectado)',
        line=dict(color=COLOR_I, width=3),
        hovertemplate='Día: %{x:.1f}<br>I: %{y:.0f}<extra></extra>'
    ))

    # Curva R: Recuperados (Aburridos)
    fig.add_trace(go.Scatter(
        x=t, y=R,
        mode='lines',
        name='R: Se aburrió (Recuperado)',
        line=dict(color=COLOR_R, width=3),
        hovertemplate='Día: %{x:.1f}<br>R: %{y:.0f}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(
            text='<b>Ciclo de Vida de una Moda (Crocs) en el Campus</b>',
            font=dict(size=20, color=COLOR_TEXTO_PRINCIPAL),
            x=0.5, y=0.95
        ),
        xaxis_title='Días',
        yaxis_title='Estudiantes',
        margin=dict(l=40, r=40, t=70, b=40),
        
        # APLICACIÓN DE COLORES CLAROS (Igual que tu ejemplo)
        paper_bgcolor=COLOR_FONDO_PAPEL,
        plot_bgcolor=COLOR_FONDO_GRAFICO,
        font=dict(family='Outfit, Arial, sans-serif', size=12, color=COLOR_TEXTO_SECUNDARIO),
        
        legend=dict(
            orientation='v',  # Vertical para ver mejor las 3 curvas
            yanchor='top', y=0.9, xanchor='right', x=0.99,
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
    
    # Ajuste dinámico de Y
    y_max = max(max(S), max(I), max(R)) * 1.05
    fig.update_yaxes(**estilo_ejes, range=[0, y_max])
    
    return fig

# ==========================================
# 4. LAYOUT
# ==========================================
layout = html.Div([
    
    html.H1("Simulación: Adopción de Moda SIR", 
            style={'textAlign': 'center', 'color': 'green', 'marginBottom': '30px'}),

    html.Div([
        # --- COLUMNA IZQUIERDA: CONTROLES ---
        html.Div([
            html.H3("Parámetros del Modelo", style={'color': 'green', 'borderBottom': '2px solid lightpink', 'marginBottom': '20px'}),
            html.P("Ajuste las variables del modelo SIR para la tendencia de moda:", style={'fontSize': '14px', 'marginBottom': '20px'}),
            
            crear_grupo_input("Población Total (N):", "input-N-moda", value=1000, step=10),
            crear_grupo_input("Tasa de imitación (b):", "input-b-moda", value=0.0005, step=0.0001, tipo="number"),
            crear_grupo_input("Tasa de aburrimiento (k):", "input-k-moda", value=0.1, step=0.01),
            crear_grupo_input("Usuarios Iniciales (I0):", "input-I0-moda", value=5, step=1),
            crear_grupo_input("Tiempo máximo (Días):", "input-t-moda", value=60, step=5),
            
            html.Button("Actualizar Gráfico", id="btn-generar-moda", 
                        style={'backgroundColor': 'green', 'color': 'white', 'padding': '12px', 'width': '100%', 'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer', 'marginTop': '10px', 'fontSize': '16px'})
        ], style={'flex': '1', 'minWidth': '300px', 'padding': '25px', 'backgroundColor': '#f9f9f9', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
        
        # --- COLUMNA DERECHA: GRÁFICO ---
        html.Div([
            dcc.Graph(
                id='grafica-moda-sir',
                style={'height': '500px', 'width': '100%'}
            )
        ], style={'flex': '2', 'minWidth': '400px', 'padding': '10px'})
        
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '30px', 'maxWidth': '1200px', 'margin': '0 auto'})
    
], style={'padding': '20px', 'fontFamily': 'Outfit, sans-serif'})

# ==========================================
# 5. CALLBACKS
# ==========================================
@callback(
    Output('grafica-moda-sir', 'figure'),
    Input('btn-generar-moda', 'n_clicks'),
    State('input-N-moda', 'value'),
    State('input-b-moda', 'value'),
    State('input-k-moda', 'value'),
    State('input-I0-moda', 'value'),
    State('input-t-moda', 'value'),
    prevent_initial_call=False
)
def actualizar_grafica_moda(n_clicks, N, b, k, I0, t_max):
    # Valores por defecto para evitar errores
    if N is None: N = 1000
    if b is None: b = 0.0005
    if k is None: k = 0.1
    if I0 is None: I0 = 5
    if t_max is None: t_max = 60

    # Validaciones básicas
    if N <= 0 or t_max <= 0:
        fig_empty = go.Figure()
        fig_empty.update_layout(title="Error: Ingrese valores positivos", paper_bgcolor='lightblue')
        return fig_empty
        
    t, S, I, R = calcular_moda_sir(N, b, k, I0, t_max)
    fig = crear_figura_moda(t, S, I, R, t_max)
    return fig