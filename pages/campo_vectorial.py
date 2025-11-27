import dash
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff 

dash.register_page(__name__, path="/Campo_Vectorial", name="Campo Vectorial")

# ==========================================
# 1. ESTILOS Y CONSTANTES
# ==========================================
# Paleta "Cuaderno Científico"
COLOR_FONDO_PAPEL = 'lightblue'
COLOR_FONDO_GRAFICO = 'white'
COLOR_GRID = 'lightpink'
COLOR_TITULO = 'green'
COLOR_TEXTO = 'black'
COLOR_VECTORES = 'navy'  # Azul oscuro para contraste
COLOR_ZEROLINE = 'red'

# Helper para crear inputs estilizados
def crear_input_campo(label, id_input, value, tipo="text", step=None):
    return html.Div([
        html.Label(label, style={'fontWeight': 'bold', 'color': COLOR_TITULO, 'fontSize': '14px'}),
        dcc.Input(
            id=id_input,
            type=tipo,
            value=value,
            step=step,
            className="input-field",
            style={
                'width': '100%', 'padding': '8px', 'borderRadius': '5px',
                'border': '1px solid #ccc', 'marginTop': '5px', 'marginBottom': '15px',
                'boxSizing': 'border-box' # Para que el padding no rompa el ancho
            }
        )
    ])

# ==========================================
# 2. LAYOUT
# ==========================================
layout = html.Div([
    
    html.H1("Visualizador de Campos Vectoriales", 
            style={'textAlign': 'center', 'color': COLOR_TITULO, 'marginBottom': '30px'}),

    html.Div([
        # --- COLUMNA IZQUIERDA: CONTROLES ---
        html.Div([
            html.H3("Definición del Campo", style={'color': COLOR_TITULO, 'borderBottom': '2px solid lightpink', 'marginBottom': '20px'}),
            
            # Inputs de Ecuaciones
            crear_input_campo("Ecuación dx/dt =", "input-fx-c5", "y"),
            crear_input_campo("Ecuación dy/dt =", "input-fy-c5", "-x - 0.1*y"), # Ejemplo un poco más interesante
            
            html.Hr(style={'borderTop': '1px dashed lightpink', 'margin': '20px 0'}),
            
            # Inputs de Configuración
            html.Div([
                html.Div([crear_input_campo("Rango X", "input-xmax-c5", 5, "number")], style={'flex': 1}),
                html.Div([crear_input_campo("Rango Y", "input-ymax-c5", 5, "number")], style={'flex': 1}),
            ], style={'display': 'flex', 'gap': '10px'}),
            
            crear_input_campo("Densidad de Malla (n)", "input-n-c5", 20, "number"),
            
            html.Button("Generar Campo", id="btn-generar-c5", 
                        style={'backgroundColor': 'green', 'color': 'white', 'padding': '12px', 'width': '100%', 
                               'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer', 'fontSize': '16px', 'marginTop': '10px'}),
            
            # Ejemplos rápidos
            html.Div([
                html.H4("Ejemplos:", style={'color': 'black', 'marginTop': '20px'}),
                html.Ul([
                    html.Li("Fuente: x, y"),
                    html.Li("Silla: x, -y"),
                    html.Li("Espiral: y, -x - 0.5*y"),
                    html.Li("No lineal: sin(y), cos(x)"),
                ], style={'fontSize': '13px', 'color': '#555', 'paddingLeft': '20px'})
            ])

        ], style={'flex': '1', 'minWidth': '300px', 'padding': '25px', 'backgroundColor': '#f9f9f9', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}),
        
        # --- COLUMNA DERECHA: GRÁFICO ---
        html.Div([
            dcc.Graph(id="grafica-campo-c5", style={"height":"500px","width":"100%"}),
            html.Div(id="info-campo-c5", style={'marginTop': '10px', 'color': 'gray', 'fontSize': '12px', 'textAlign': 'right'}) 
        ], style={'flex': '2', 'minWidth': '400px', 'padding': '10px'})

    ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '30px', 'maxWidth': '1200px', 'margin': '0 auto'})

], style={'padding': '20px', 'fontFamily': 'Outfit, sans-serif'})


# ==========================================
# 3. LÓGICA (CALLBACK)
# ==========================================
@callback(
    [Output("grafica-campo-c5", "figure"),
     Output("info-campo-c5", "children")],
     Input("btn-generar-c5", "n_clicks"),
     State("input-fx-c5", "value"),
     State("input-fy-c5", "value"),
     State("input-xmax-c5", "value"),
     State("input-ymax-c5", "value"),
     State("input-n-c5", "value"),
     prevent_initial_call=False
)
def generar_campo(n_clicks, fx_str, fy_str, xmax, ymax, n):
    
    # Validaciones básicas
    if not n or n < 5: n = 5
    if n > 50: n = 50 # Límite para rendimiento
    if not xmax: xmax = 5
    if not ymax: ymax = 5

    x = np.linspace(-xmax, xmax, n)
    y = np.linspace(-ymax, ymax, n)
    X, Y = np.meshgrid(x, y)
    
    try:
        # Diccionario seguro para eval
        diccionario = {
            "x": X, "y": Y, "np": np,
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, 'sqrt': np.sqrt, 'pi': np.pi, 'e': np.e 
        }
        
        fx = eval(fx_str, {}, diccionario)
        fy = eval(fy_str, {}, diccionario)
        
        # Normalización para visualización limpia
        mag = np.sqrt(fx**2 + fy**2)
        # Evitar división por cero
        mag_safe = np.where(mag == 0, 1, mag) 
        
        # Vectores unitarios para dirección (opcional, aquí normalizamos un poco)
        fx_norm = fx / mag_safe
        fy_norm = fy / mag_safe
        
        info_mensaje = f"Rango evaluado: [-{xmax}, {xmax}]"
        
    except Exception as error:
        # Retornar gráfico vacío con mensaje de error
        fig_error = go.Figure()
        fig_error.add_annotation(text=f"Error en sintaxis: {str(error)}", x=0.5, y=0.5, showarrow=False, font=dict(color="red", size=14))
        fig_error.update_layout(paper_bgcolor=COLOR_FONDO_PAPEL, plot_bgcolor=COLOR_FONDO_GRAFICO)
        return fig_error, "Error de cálculo"

    # Crear Quiver Plot (Flechas)
    fig = ff.create_quiver(
        X, Y, fx_norm, fy_norm,
        scale=1.0,      # Escala visual de las flechas
        arrow_scale=0.3, 
        line=dict(color=COLOR_VECTORES, width=1.5),
        name='Vector'
    )

    # Añadir un punto rojo en el origen (0,0) como referencia
    fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(color='red', size=8), name='Origen'))

    # Actualizar Layout con Estilo Científico
    fig.update_layout(
        title=dict(
            text=f"<b>Campo: dx/dt={fx_str}, dy/dt={fy_str}</b>",
            x=0.5, y=0.95,
            font=dict(color=COLOR_TITULO, size=18)
        ),
        xaxis_title="x",
        yaxis_title="y",
        paper_bgcolor=COLOR_FONDO_PAPEL,
        plot_bgcolor=COLOR_FONDO_GRAFICO,
        font=dict(color=COLOR_TEXTO, family='Outfit, sans-serif'),
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=False
    )
    
    # Configuración de Ejes (Grid Rosa)
    estilo_ejes = dict(
        showgrid=True, gridwidth=1, gridcolor=COLOR_GRID,
        zeroline=True, zerolinewidth=2, zerolinecolor=COLOR_ZEROLINE,
        showline=True, linecolor=COLOR_TEXTO, linewidth=2, mirror=True,
    )
    
    fig.update_xaxes(**estilo_ejes, range=[-xmax*1.1, xmax*1.1])
    fig.update_yaxes(**estilo_ejes, range=[-ymax*1.1, ymax*1.1])
    
    # Mantener aspecto cuadrado (importante para campos vectoriales)
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    
    return fig, info_mensaje