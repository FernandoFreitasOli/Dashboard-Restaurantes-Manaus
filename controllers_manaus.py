from dash import html, dcc
import dash_bootstrap_components as dbc
from app import app
import pandas as pd

# Carregar os dados tratados para alimentar os filtros
df_data = pd.read_csv("Dataset/pedidos_manaus_tratado.csv")

controllers = dbc.Row([
    dcc.Store(id='store-global'),
    html.Img(id="logo", src=app.get_asset_url("logo_dark.png"), style={'width': '50%'}),
    html.H3("Análise de Vendas - Restaurantes Manaus", style={"margin-top": "30px"}),
    html.P("""Este painel interativo permite explorar as vendas de pequenos e médios restaurantes da cidade de Manaus."""),

    html.H4("Filtros", style={"margin-top": "30px"}),

    html.P("Restaurante"),
    dcc.Dropdown(
        id="dropdown-restaurante",
        options=[{"label": r, "value": r} for r in sorted(df_data["restaurante"].unique())],
        value=None,
        placeholder="Selecione um restaurante"
    ),

    html.P("Bairro"),
    dcc.Dropdown(
        id="dropdown-bairro",
        options=[{"label": b, "value": b} for b in sorted(df_data["bairro"].unique())],
        value=None,
        placeholder="Selecione um bairro"
    ),

    html.P("Categoria"),
    dcc.Dropdown(
        id="dropdown-categoria",
        options=[{"label": c, "value": c} for c in sorted(df_data["categoria"].unique())],
        value=None,
        placeholder="Selecione uma categoria"
    ),

    html.P("Período"),
    dcc.DatePickerRange(
        id='date-picker-range',
        min_date_allowed=df_data["data"].min(),
        max_date_allowed=df_data["data"].max(),
        start_date=df_data["data"].min(),
        end_date=df_data["data"].max(),
        display_format='DD/MM/YYYY'
    )
])