from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app import app

# Componentes
from _map import *
from controllers_manaus import *
from _histogram import *

# =======================================
# Data Ingestion
df_data = pd.read_csv("Dataset/pedidos_manaus_tratado.csv")
df_data["data"] = pd.to_datetime(df_data["data"])

mean_lat = df_data["LATITUDE"].mean()
mean_long = df_data["LONGITUDE"].mean()

# ================================
# Layout do app
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1(
                    "📊 Dashboard Restaurantes",
                    style={
                        'color': '#fff',
                        'font-weight': '800',
                        'margin-bottom': '5px',
                        'font-size': '36px'
                    }
                ),
                html.P(
                    "Manaus",
                    style={
                        'color': '#ff6b6b',
                        'font-size': '18px',
                        'font-weight': '600',
                        'margin-bottom': '0'
                    }
                ),
            ])
        ], width=12)
    ], style={
        'background': 'linear-gradient(135deg, #0f3460 0%, #16213e 100%)',
        'padding': '40px',
        'margin-bottom': '30px',
        'border-radius': '12px',
        'box-shadow': '0 8px 32px rgba(0,0,0,0.3)'
    }),

    # Main Content
    dbc.Row([
        dbc.Col([controllers], md=3),
        dbc.Col([
            dbc.Row([
                dbc.Col([map], width=12)
            ]),
            dbc.Row([
                dbc.Col([hist], width=12, style={'margin-top': '20px'})
            ])
        ], md=9),
    ], style={'gap': '20px'}),

], fluid=True, style={
    'background-color': '#0a0e27',
    'min-height': '100vh',
    'padding': '20px',
    'font-family': 'Arial, sans-serif'
})

# ========================================================
# Callbacks 
@app.callback(
    [Output('hist-graph', 'figure'), Output('map-graph', 'figure')],
    [
        Input('dropdown-restaurante', 'value'),
        Input('dropdown-bairro', 'value'),
        Input('dropdown-categoria', 'value'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date')
    ]
)
def update_graphs(restaurante, bairro, categoria, start_date, end_date):
    df_filtered = df_data.copy()

    if restaurante:
        df_filtered = df_filtered[df_filtered['restaurante'] == restaurante]
    if bairro:
        df_filtered = df_filtered[df_filtered['bairro'] == bairro]
    if categoria:
        df_filtered = df_filtered[df_filtered['categoria'] == categoria]
    if start_date and end_date:
        df_filtered = df_filtered[(df_filtered['data'] >= start_date) & (df_filtered['data'] <= end_date)]

    # Histograma de pratos
    hist_fig = px.histogram(df_filtered, x="prato", title="📈 Pratos mais vendidos")
    hist_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.1)",
        font=dict(family="Arial, sans-serif", size=12, color="#fff"),
        margin=dict(l=10, r=10, t=40, b=60),
        title_font_size=16,
        title_font_color="#fff",
        hovermode='x unified',
        xaxis_tickangle=-45
    )
    hist_fig.update_traces(marker_color='#ff6b6b')

    # Mapa de vendas
    
    map_fig = px.scatter_mapbox(
        df_filtered, lat="LATITUDE", lon="LONGITUDE",
        color="categoria", size="preco", zoom=11,
        hover_name="restaurante", opacity=0.7,
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    map_fig.update_layout(
        mapbox=dict(
            center=dict(lat=mean_lat, lon=mean_long),
            style="open-street-map"
        ),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.1)",
        font=dict(family="Arial, sans-serif", size=11, color="#fff"),
        margin=dict(l=10, r=10, t=30, b=10),
        title_text="📍 Localização dos Restaurantes",
        title_font_size=16,
        title_font_color="#fff",
        hovermode='closest'
    )

    return hist_fig, map_fig

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8050)

