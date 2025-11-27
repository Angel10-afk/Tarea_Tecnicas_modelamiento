import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np


P0 = 10        
r = 0.25      
K = 150      
t = np.linspace(0, 60, 300) 

A = (K - P0) / P0
P = K / (1 + A * np.exp(-r * t))


trace_logistica = go.Scatter(
    x=t,
    y=P,
    mode='lines',
    line=dict(color='#f57c00', width=3),  # naranja cálido
    name='Crecimiento proyectado'
)

trace_capacidad = go.Scatter(
    x=t,
    y=[K]*len(t),
    mode='lines',
    line=dict(color='#388e3c', width=3, dash='dot'),  # verde fuerte
    name='Límite sostenible (K)'
)

fig = go.Figure(data=[trace_logistica, trace_capacidad])

fig.update_layout(
    title=dict(
        text='<b>Modelo Logístico de Crecimiento Sostenible</b>',
        font=dict(size=20, color='#1b4332'),
        x=0.5
    ),
    xaxis_title='Tiempo (t)',
    yaxis_title='Nivel de crecimiento (P)',
    paper_bgcolor='rgb(255,255,245)',
    plot_bgcolor='rgb(255,255,245)',
    font=dict(family='Outfit', size=13, color='#2c3e50'),
    margin=dict(l=40, r=40, t=60, b=40),
    legend=dict(
        x=0.02, y=0.95,
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='#a5d6a7',
        borderwidth=1
    )
)

fig.update_xaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor='rgba(200,220,200,0.5)',
    zeroline=True,
    zerolinewidth=2,
    zerolinecolor='#388e3c',
    linecolor='#2e7d32',
    linewidth=2
)

fig.update_yaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor='rgba(200,220,200,0.5)',
    zeroline=True,
    zerolinewidth=2,
    zerolinecolor='#388e3c',
    linecolor='#2e7d32',
    linewidth=2
)


dash.register_page(__name__, path='/Tarea', name='Tarea')


layout = html.Div(children=[

    html.Div(children=[
        html.H2("📈 Modelo Logístico de Crecimiento Sostenible", className="title"),

        dcc.Markdown("""
        En muchas áreas desde la ecología hasta la economía los sistemas crecen rápidamente al inicio,
        pero su expansión se modera cuando alcanzan su capacidad de equilibrio o límite sostenible (K).

        Este modelo describe esa dinámica mediante la función logística, representando cómo
        los recursos, las empresas o incluso los ecosistemas tienden a estabilizarse con el tiempo.

        $$ 
        P(t) = \\frac{K}{1 + A e^{-r t}} 
        $$

        donde:
        - $P_0$: valor inicial del sistema  
        - $r$: ritmo de crecimiento  
        - $K$: límite o capacidad máxima sostenible  
        """, mathjax=True, style={'fontSize': '17px'})
    ], className="content left"),

    html.Div(children=[
        html.H2(" Evolución del Crecimiento", className="title"),
        dcc.Graph(
            figure=fig,
            style={'height': '420px', 'width': '100%'}
        ),
        html.P("El modelo refleja un equilibrio entre expansión y estabilidad, "
               "destacando cómo un sistema sostenible debe respetar sus límites naturales.",
               style={'fontSize': '16px', 'textAlign': 'center', 'color': '#2c3e50', 'marginTop': '10px'})
    ], className="content right")
], className="page-container")
