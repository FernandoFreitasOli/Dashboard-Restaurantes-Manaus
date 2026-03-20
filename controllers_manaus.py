from dash import html, dcc
import dash_bootstrap_components as dbc
from app import app
import pandas as pd

# Carregar os dados tratados para alimentar os filtros
df_data = pd.read_csv("Dataset/pedidos_manaus_tratado.csv")

controllers = dbc.Col([
    dcc.Store(id='store-global'),
    
    # Header com Logo
    html.Div([
        html.Img(
            id="logo", 
            src=app.get_asset_url("logo_dark.png"), 
            style={'width': '80px', 'margin-bottom': '20px'}
        ),
    ], style={'text-align': 'center', 'padding-bottom': '20px', 'border-bottom': '2px solid #ff6b6b'}),
    
    # Título
    html.Div([
        html.H2(
            "Análise de Vendas",
            style={
                'color': '#fff',
                'font-weight': '700',
                'margin-top': '20px',
                'margin-bottom': '5px',
                'font-size': '28px'
            }
        ),
        html.P(
            "Restaurantes Manaus",
            style={
                'color': '#ff6b6b',
                'font-size': '16px',
                'font-weight': '600',
                'margin-bottom': '10px'
            }
        ),
        html.P(
            "Explore as vendas de pequenos e médios restaurantes da cidade de Manaus.",
            style={
                'color': '#adb5bd',
                'font-size': '13px',
                'line-height': '1.6',
                'margin-bottom': '20px'
            }
        ),
    ], style={'margin-bottom': '30px'}),

    # Filtros em Cards
    html.Div([
        html.H5(
            "🎯 Filtros",
            style={
                'color': '#fff',
                'font-weight': '700',
                'margin-bottom': '20px',
                'font-size': '16px'
            }
        ),
    ]),

    # Restaurante
    dbc.Card([
        dbc.CardBody([
            html.Label(
                "🏪 Restaurante",
                style={'color': '#fff', 'font-weight': '600', 'margin-bottom': '10px', 'display': 'block'}
            ),
            dcc.Dropdown(
                id="dropdown-restaurante",
                options=[{"label": r, "value": r} for r in sorted(df_data["restaurante"].unique())],
                value=None,
                placeholder="Selecione um restaurante",
                style={'width': '100%'},
                clearable=True
            ),
        ])
    ], style={'margin-bottom': '12px', 'background-color': '#1a1a2e', 'border': '1px solid #16213e'}),

    # Bairro
    dbc.Card([
        dbc.CardBody([
            html.Label(
                "📍 Bairro",
                style={'color': '#fff', 'font-weight': '600', 'margin-bottom': '10px', 'display': 'block'}
            ),
            dcc.Dropdown(
                id="dropdown-bairro",
                options=[{"label": b, "value": b} for b in sorted(df_data["bairro"].unique())],
                value=None,
                placeholder="Selecione um bairro",
                style={'width': '100%'},
                clearable=True
            ),
        ])
    ], style={'margin-bottom': '12px', 'background-color': '#1a1a2e', 'border': '1px solid #16213e'}),

    # Categoria
    dbc.Card([
        dbc.CardBody([
            html.Label(
                "🍽️ Categoria",
                style={'color': '#fff', 'font-weight': '600', 'margin-bottom': '10px', 'display': 'block'}
            ),
            dcc.Dropdown(
                id="dropdown-categoria",
                options=[{"label": c, "value": c} for c in sorted(df_data["categoria"].unique())],
                value=None,
                placeholder="Selecione uma categoria",
                style={'width': '100%'},
                clearable=True
            ),
        ])
    ], style={'margin-bottom': '12px', 'background-color': '#1a1a2e', 'border': '1px solid #16213e'}),

    # Período
    dbc.Card([
        dbc.CardBody([
            html.Label(
                "📅 Período",
                style={'color': '#fff', 'font-weight': '600', 'margin-bottom': '10px', 'display': 'block'}
            ),
            dcc.DatePickerRange(
                id='date-picker-range',
                min_date_allowed=df_data["data"].min(),
                max_date_allowed=df_data["data"].max(),
                start_date=df_data["data"].min(),
                end_date=df_data["data"].max(),
                display_format='DD/MM/YYYY',
                style={'width': '100%'}
            ),
        ])
    ], style={'background-color': '#1a1a2e', 'border': '1px solid #16213e'}),

], md=3, style={
    'background': 'linear-gradient(135deg, #0f3460 0%, #16213e 100%)',
    'padding': '30px',
    'border-radius': '12px',
    'height': '100%',
    'box-shadow': '0 8px 32px rgba(0,0,0,0.3)'
})