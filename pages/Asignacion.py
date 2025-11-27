import dash 
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint

dash.register_page(__name__, path="/Proyecto/Proyecto", name="Proyecto Modelo SIR")

# ==========================================
# 1. ESTILOS Y COLORES (TEMA CLARO)
# ==========================================
COLOR_FONDO_PAPEL = 'lightblue'
COLOR_FONDO_GRAFICO = 'white'
COLOR_GRID = 'lightpink'
COLOR_TITULO = 'green'
COLOR_TEXTO = 'black'
COLOR_ZEROLINE = 'red'

# Colores de las curvas (Optimizados para fondo blanco)
COLOR_SUCEPTIBLES = '#00BFFF'  # Azul brillante
COLOR_INFECTADOS = '#FF1493'   # Rosa fuerte
COLOR_RECUPERADOS = '#9400D3'  # Violeta oscuro

# ==========================================
# 2. MODELO MATEMÁTICO
# ==========================================
def modelo_sir(y, t, b, g):
    S, I, R = y 
    # Protección contra valores negativos numéricos
    S = max(0, S)
    I = max(0, I)
    
    # Ecuaciones: dS/dt = -beta*S*I
    # Nota: Aquí beta ya incluye el factor 1/N si se definió así en los parámetros
    dS_dt = -b * S * I
    dI_dt = b * S * I - g * I
    dR_dt = g * I
    return [dS_dt, dI_dt, dR_dt]

# --- PARAMETROS DEL PROYECTO ---
N_total = 7138.0             # Población de la facultad
beta = 1.0 / 7138.0          # Tasa de transmisión (1 contacto efectivo / N)
gamma = 0.40                 # Tasa de recuperación (1/2.5 días)
S0 = 7137.0
I0 = 1.0
R0_inicial = 0.0
y0 = [S0, I0, R0_inicial]

# --- SIMULACIÓN ---
t = np.linspace(0, 40, 400) 
solucion = odeint(modelo_sir, y0, t, args=(beta, gamma))
S, I, R = solucion.T

# --- ANÁLISIS DE RESULTADOS ---
# 1. Valor al día 6
t_6 = np.linspace(0, 6, 100)
sol_6 = odeint(modelo_sir, y0, t_6, args=(beta, gamma))
I_6 = sol_6.T[1][-1]

# 2. Pico de infección
idx_pico = np.argmax(I)
dia_pico = t[idx_pico]
max_infectados = I[idx_pico]

# 3. Número Reproductivo Básico (R0)
# R0 = (beta * S0) / gamma. Como S0 ~ N, y beta en este código es (beta_std/N),
# entonces beta_code * N = beta_std.
R0_calc = (beta * N_total) / gamma

# ==========================================
# 3. CREACIÓN DEL GRÁFICO
# ==========================================
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=t, y=S, mode='lines', name='Susceptibles S(t)', 
    line=dict(color=COLOR_SUCEPTIBLES, width=2.5)
))

fig.add_trace(go.Scatter(
    x=t, y=I, mode='lines', name='Infectados I(t)', 
    line=dict(color=COLOR_INFECTADOS, width=3), 
    fill='tozeroy', 
    fillcolor='rgba(255, 20, 147, 0.1)' # Rosa muy suave transparente
))

fig.add_trace(go.Scatter(
    x=t, y=R, mode='lines', name='Recuperados R(t)', 
    line=dict(color=COLOR_RECUPERADOS, width=2.5)
))

# Marcadores para puntos importantes
fig.add_trace(go.Scatter(
    x=[6], y=[I_6], mode='markers+text', name='Día 6',
    marker=dict(color='red', size=10, symbol='x'),
    text=[f"{int(I_6)}"], textposition="top center", showlegend=False
))

fig.add_trace(go.Scatter(
    x=[dia_pico], y=[max_infectados], mode='markers', name='Pico',
    marker=dict(color='black', size=8), showlegend=False
))

fig.update_layout(
    title=dict(
        text="<b>Dinámica de Infección - Facultad de Ciencias</b>", 
        x=0.5, y=0.95,
        font=dict(size=18, color=COLOR_TITULO)
    ),
    xaxis_title="Tiempo (días)",
    yaxis_title="Estudiantes",
    paper_bgcolor=COLOR_FONDO_PAPEL,
    plot_bgcolor=COLOR_FONDO_GRAFICO,
    font=dict(color=COLOR_TEXTO, family='Outfit, sans-serif'),
    legend=dict(
        orientation='h', y=1.02, x=0.5, xanchor='center',
        bgcolor='rgba(255,255,255,0.9)', bordercolor='#ddd', borderwidth=1
    ),
    margin=dict(l=40, r=40, t=60, b=40),
    hovermode="x unified"
)

# Estilo de Ejes (Grid Rosa)
estilo_ejes = dict(
    showgrid=True, gridwidth=1, gridcolor=COLOR_GRID,
    zeroline=True, zerolinewidth=2, zerolinecolor=COLOR_ZEROLINE,
    showline=True, linecolor=COLOR_TEXTO, linewidth=2, mirror=True
)
fig.update_xaxes(**estilo_ejes, range=[0, 40])
fig.update_yaxes(**estilo_ejes, range=[0, N_total * 1.05])

# ==========================================
# 4. TEXTOS DE ANÁLISIS (DETALLADOS)
# ==========================================
texto_intro = r"""
### 1. Marco Teórico
El modelo SIR divide a la población universitaria en tres compartimentos:

* **Susceptibles ($S$):** Estudiantes sanos que pueden contraer el virus.
* **Infectados ($I$):** Estudiantes portadores capaces de transmitir la enfermedad.
* **Recuperados ($R$):** Estudiantes que han superado la enfermedad y adquieren inmunidad.

El sistema de ecuaciones diferenciales ordinarias (EDO) es:
$$ \frac{dS}{dt} = -\beta S I, \quad \frac{dI}{dt} = \beta S I - \gamma I, \quad \frac{dR}{dt} = \gamma I $$
"""

texto_parametros = f"""
### 2. Parámetros del Escenario
Se simula un brote en una población cerrada (sin nacimientos ni muertes) bajo las siguientes condiciones:

* **Población Total ($N$):** {int(N_total)} estudiantes.
* **Paciente Cero ($I_0$):** {int(I0)} estudiante infectado al día 0.
* **Coef. Transmisión ($\\beta$):** $1/{int(1/beta)}$ (Probabilidad de contagio por contacto).
* **Tasa Recuperación ($\\gamma$):** ${gamma}$ (Tiempo medio de infección $\\approx {1/gamma:.1f}$ días).
* **Número Reproductivo ($R_0$):** ${R0_calc:.2f}$ (Cada infectado contagia a 2.5 personas al inicio).
"""

texto_analisis = f"""
### 3. Análisis de Resultados
La simulación numérica arroja los siguientes indicadores críticos para la toma de decisiones:

* **Estado al Día 6:** Se estima que habrá **{int(I_6)}** estudiantes infectados activos.
* **Pico de la Epidemia:** Ocurrirá aproximadamente el día **{dia_pico:.1f}**.
* **Máximo Contagio:** En el pico, **{int(max_infectados)}** estudiantes estarán infectados simultáneamente (aprox. el {max_infectados/N_total*100:.1f}% de la facultad).
"""

# ==========================================
# 5. LAYOUT
# ==========================================
layout = html.Div([
    
    html.H1("Proyecto Final: Modelamiento de Epidemia", 
            style={'textAlign': 'center', 'color': COLOR_TITULO, 'marginBottom': '30px'}),

    html.Div([
        
        # --- COLUMNA IZQUIERDA: GRÁFICO ---
        html.Div([
            html.Div([
                dcc.Graph(figure=fig, style={"height": "600px", "width": "100%"})
            ], style={'padding': '15px', 'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 4px 10px rgba(0,0,0,0.05)'})
        ], style={'flex': '3', 'minWidth': '600px'}),
        
        # --- COLUMNA DERECHA: REPORTE ---
        html.Div([
            html.H3("Informe Técnico", style={'color': COLOR_TITULO, 'borderBottom': '2px solid lightpink', 'marginBottom': '15px'}),
            
            # Bloque 1: Teoría
            dcc.Markdown(texto_intro, mathjax=True, style={'fontSize': '14px', 'textAlign': 'justify'}),
            html.Hr(style={'borderTop': '1px dashed lightpink'}),
            
            # Bloque 2: Parámetros
            dcc.Markdown(texto_parametros, mathjax=True, style={'fontSize': '14px'}),
            html.Hr(style={'borderTop': '1px dashed lightpink'}),

            # Bloque 3: Resultados Destacados (Caja Verde)
            html.Div([
                dcc.Markdown(texto_analisis, mathjax=True, style={'color': 'white'})
            ], style={
                'backgroundColor': 'green', 
                'borderRadius': '8px', 
                'padding': '15px', 
                'marginTop': '10px',
                'boxShadow': '0 2px 5px rgba(0,0,0,0.2)'
            })
            
        ], style={
            'flex': '2', 
            'minWidth': '350px', 
            'padding': '30px', 
            'backgroundColor': '#f9f9f9', 
            'borderRadius': '10px', 
            'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
            'maxHeight': '800px',
            'overflowY': 'auto' # Scroll si el texto es muy largo
        })
        
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '30px', 'maxWidth': '1600px', 'margin': '0 auto'})

], style={'padding': '20px', 'fontFamily': 'Outfit, sans-serif'})