import dash
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import odeint

dash.register_page(__name__, path="/SIR", name="Modelo SIR")

# ==========================================
# 1. ESTILOS Y COLORES (TEMA CLARO)
# ==========================================
# Paleta consistente con el resto del portafolio
COLOR_SUCEPTIBLES = '#00BFFF'  # Deep Sky Blue (Azul brillante)
COLOR_INFECTADOS = '#FF1493'   # Deep Pink (Rosa intenso)
COLOR_RECUPERADOS = '#9400D3'  # Dark Violet (Violeta oscuro)

COLOR_FONDO_PAPEL = 'lightblue'
COLOR_FONDO_GRAFICO = 'white'
COLOR_GRID = 'lightpink'
COLOR_TITULO = 'green'
COLOR_TEXTO = 'black'
COLOR_ZEROLINE = 'red'

# Helper para crear inputs estilizados (Reutilizable)
def crear_input_sir(label, id_input, value, step=1, min_val=0):
    return html.Div([
        html.Label(label, style={'fontWeight': 'bold', 'color': COLOR_TITULO, 'fontSize': '14px'}),
        dcc.Input(
            id=id_input,
            type="number",
            value=value,
            step=step,
            min=min_val,
            className="input-field",
            style={
                'width': '100%', 
                'padding': '8px', 
                'borderRadius': '5px',
                'border': '1px solid #ccc', 
                'marginTop': '5px', 
                'marginBottom': '15px',
                'backgroundColor': 'white', 
                'color': 'black',
                'boxSizing': 'border-box'
            }
        )
    ])

# ==========================================
# 2. LÓGICA MATEMÁTICA
# ==========================================
def modelo_sir(y, t, b, g, N):
    S, I, R = y
    # Asegurar no negatividad
    S = max(0, S)
    I = max(0, I)
    
    dS_dt = -b * S * I / N
    dI_dt = b * S * I / N - g * I
    dR_dt = g * I
    return [dS_dt, dI_dt, dR_dt]


# ==========================================
# 3. LAYOUT
# ==========================================
layout = html.Div([
    
    html.H1("Modelo SIR - Epidemiología", 
            style={'textAlign': 'center', 'color': COLOR_TITULO, 'marginBottom': '30px'}),

    html.Div([
        # --- COLUMNA IZQUIERDA: CONTROLES ---
        html.Div([
            html.H3("Parámetros de Infección", style={'color': COLOR_TITULO, 'borderBottom': '2px solid lightpink', 'marginBottom': '20px'}),
            html.P("Ajuste las tasas para simular la epidemia:", style={'fontSize': '14px', 'marginBottom': '20px'}),
            
            crear_input_sir("Población Total (N):", "input-n-sir", 1000, 10),
            crear_input_sir("Tasa de transmisión (β):", "input-b-sir", 0.3, 0.01),
            crear_input_sir("Tasa de recuperación (γ):", "input-g-sir", 0.1, 0.01),
            crear_input_sir("Infectados iniciales (I₀):", "input-I0-sir", 1, 1),
            crear_input_sir("Días a simular:", "input-tiempo-sir", 100, 10),
            
            html.Button("Generar Simulación", id="btn-generar-sir", 
                        style={'backgroundColor': 'green', 'color': 'white', 'padding': '12px', 'width': '100%', 
                               'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer', 'fontSize': '16px', 'marginTop': '10px'})

        ], style={'flex': '1', 'minWidth': '300px', 'padding': '25px', 'backgroundColor': '#f9f9f9', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
        
        # --- COLUMNA DERECHA: GRÁFICO ---
        html.Div([
            dcc.Graph(id="grafica-sir", style={"height":"500px","width":"100%"})
        ], style={'flex': '2', 'minWidth': '400px', 'padding': '10px'})

    ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '30px', 'maxWidth': '1200px', 'margin': '0 auto'})

], style={'padding': '20px', 'fontFamily': 'Outfit, sans-serif'})


# ==========================================
# 4. CALLBACKS
# ==========================================
@callback(
    Output("grafica-sir", "figure"),
    Input("btn-generar-sir", "n_clicks"),
    State("input-n-sir", "value"),
    State("input-b-sir", "value"),
    State("input-g-sir", "value"),
    State("input-I0-sir", "value"),
    State("input-tiempo-sir", "value"),
    prevent_initial_call=False
)
def simular_sir(n_clicks, n, beta, gamma, I0, tiempo_max):
    
    # Validaciones y valores por defecto para evitar errores
    if not n: n = 1000
    if not beta: beta = 0.3
    if not gamma: gamma = 0.1
    if not I0: I0 = 1
    if not tiempo_max: tiempo_max = 100
        
    S0 = n - I0 
    R0_inicial = 0
    y0 = [S0, I0, R0_inicial]
    t = np.linspace(0, tiempo_max, 200) 
    
    try:
        solucion = odeint(modelo_sir, y0, t, args=(beta, gamma, n))
        S, I, R = solucion.T
    except Exception as e:
        fig_error = go.Figure()
        fig_error.add_annotation(text="Error de cálculo", showarrow=False)
        fig_error.update_layout(paper_bgcolor=COLOR_FONDO_PAPEL, plot_bgcolor=COLOR_FONDO_GRAFICO)
        return fig_error

    # Construcción del gráfico claro
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=S, mode='lines', name='Susceptibles',
        line=dict(color=COLOR_SUCEPTIBLES, width=3),
        hovertemplate="Día %{x:.0f}: %{y:.0f} Susceptibles<extra></extra>"
    ))
    
    fig.add_trace(go.Scatter(
        x=t, y=I, mode='lines', name='Infectados',
        line=dict(color=COLOR_INFECTADOS, width=3),
        fill='tozeroy', fillcolor='rgba(255, 20, 147, 0.1)', # Relleno suave rosa
        hovertemplate="Día %{x:.0f}: %{y:.0f} Infectados<extra></extra>"
    ))
    
    fig.add_trace(go.Scatter(
        x=t, y=R, mode='lines', name='Recuperados',
        line=dict(color=COLOR_RECUPERADOS, width=3),
        hovertemplate="Día %{x:.0f}: %{y:.0f} Recuperados<extra></extra>"
    ))

    # Cálculo del número reproductivo básico
    r0_val = beta / gamma if gamma != 0 else 0

    fig.update_layout(
        title=dict(
            text=f"<b>Evolución del Modelo SIR (R₀ ≈ {r0_val:.2f})</b>",
            font=dict(color=COLOR_TITULO, size=20),
            x=0.5, y=0.95
        ),
        xaxis_title="Tiempo (días)",
        yaxis_title="Número de personas",
        paper_bgcolor=COLOR_FONDO_PAPEL,
        plot_bgcolor=COLOR_FONDO_GRAFICO,
        font=dict(color=COLOR_TEXTO, family='Outfit, sans-serif'),
        legend=dict(
            orientation='h', y=1.02, x=0.5, xanchor='center', 
            bgcolor='rgba(255,255,255,0.8)', bordercolor='#ddd', borderwidth=1
        ),
        margin=dict(l=40, r=40, t=60, b=40),
        hovermode="x unified"
    )

    # Configuración de ejes (Grid Rosa)
    estilo_ejes = dict(
        showgrid=True, gridwidth=1, gridcolor=COLOR_GRID,
        zeroline=True, zerolinewidth=2, zerolinecolor=COLOR_ZEROLINE,
        showline=True, linecolor=COLOR_TEXTO, linewidth=2, mirror=True,
    )
    
    fig.update_xaxes(**estilo_ejes)
    fig.update_yaxes(**estilo_ejes)

    return fig