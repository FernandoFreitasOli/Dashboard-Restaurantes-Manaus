from dash import html, dcc
import dash_bootstrap_components as dbc
from app import app
import plotly.graph_objects as go

fig = go.Figure()
fig.update_layout(
    template='plotly_dark',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    font=dict(family="Arial, sans-serif", size=12, color="#fff"),
    margin=dict(l=10, r=10, t=10, b=10)
)

map = dbc.Card([
    dbc.CardBody([
        dcc.Graph(id='map-graph', figure=fig, style={'height': '65vh'})
    ], style={'padding': '0'})
], style={
    'background-color': '#16213e',
    'border': '1px solid #0f3460',
    'border-radius': '12px',
    'margin-bottom': '15px',
    'box-shadow': '0 8px 32px rgba(0,0,0,0.3)'
})
