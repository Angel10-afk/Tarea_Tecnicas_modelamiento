import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__, path='/inicio', name='Inicio')


t = np.linspace(0, 8 * np.pi, 400)
x = np.sin(t) * np.exp(-0.05 * t)
y = np.cos(t) * np.exp(-0.05 * t)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x, y=y,
    mode='lines',
    line=dict(width=4, color='violet'),
    name='Trayectoria matemática'
))

fig.update_layout(
    title=dict(
        text='<b>Representación paramétrica de una espiral decreciente</b>',
        x=0.5,
        font=dict(size=18, color='#5a00b2')
    ),
    xaxis_title='Eje X',
    yaxis_title='Eje Y',
    plot_bgcolor='rgb(255,250,255)',
    paper_bgcolor='rgb(255,250,255)',
    font=dict(family='Outfit', size=13, color='#3b0078'),
    margin=dict(l=40, r=40, t=60, b=40),
)


layout = html.Div([
   
    html.H1(" Bienvenido  ",
            style={
                'textAlign': 'center',
                'color': '#5a00b2',
                'marginTop': '25px',
                'fontWeight': 'bold'
            }),

    


    html.Div([
        html.Div([
            html.Img(
                src="https://cdn-icons-png.flaticon.com/512/5775/5775807.png",
                style={'width': '130px', 'marginBottom': '10px'}
            ),
            html.H2(" El poder de modelar",
                    style={'color': '#5a00b2'}),
            html.P(
                "El modelamiento matemático es una herramienta que nos permite representar "
                "situaciones reales con ecuaciones, funciones y gráficos. "
                "Desde el crecimiento de poblaciones hasta el análisis de redes, "
                "todo puede expresarse con un modelo.",
                style={'fontSize': '18px', 'textAlign': 'justify', 'maxWidth': '500px'}
            ),
        ], style={'width': '45%', 'textAlign': 'center', 'padding': '20px'}),

        html.Div([
            html.Img(
                src="https://cdn-icons-png.flaticon.com/512/3202/3202926.png",
                style={'width': '130px', 'marginBottom': '10px'}
            ),
            html.H2(" En este curso aprenderás a:",
                    style={'color': '#004aad'}),
            html.Ul([
                html.Li(" Interpretar comportamientos usando funciones y ecuaciones."),
                html.Li(" Traducir fenómenos reales a modelos matemáticos."),
                html.Li(" Resolver problemas aplicando simulación y optimización."),
                html.Li(" Visualizar resultados y comprender patrones."),
            ], style={'textAlign': 'left', 'fontSize': '17px', 'lineHeight': '1.6', 'maxWidth': '500px', 'margin': 'auto'})
        ], style={'width': '45%', 'textAlign': 'center', 'padding': '20px'}),
    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'flex-start',
        'gap': '30px',
        'flexWrap': 'wrap',
        'marginTop': '30px'
    }),

    
    

   
    
])
