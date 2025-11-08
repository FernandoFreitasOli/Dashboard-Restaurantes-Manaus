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
    dbc.Row([
        dbc.Col([controllers], md=3, style={"padding": "25px"}),
        dbc.Col([map, hist], md=9),
    ])
], fluid=True)

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
    hist_fig = px.histogram(df_filtered, x="prato", title="Pratos mais vendidos")
    hist_fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=10, t=30, b=50))

    # Mapa de vendas
    
    map_fig = px.scatter_mapbox(
    df_filtered, lat="LATITUDE", lon="LONGITUDE",
    color="categoria", size="preco", zoom=11,
    hover_name="restaurante", opacity=0.5
    )

    map_fig.update_layout(
        mapbox=dict(
            center=dict(lat=mean_lat, lon=mean_long),
            style="open-street-map"  # <<< aqui está a mudança
        ),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10)
    )


    return hist_fig, map_fig

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8050)

