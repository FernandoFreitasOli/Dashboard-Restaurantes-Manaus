from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

app = Flask(__name__)
CORS(app)

# Carregar dados
df_data = pd.read_csv("Dataset/pedidos_manaus_tratado.csv")
df_data["data"] = pd.to_datetime(df_data["data"])

mean_lat = df_data["LATITUDE"].mean()
mean_long = df_data["LONGITUDE"].mean()

@app.route('/api/data', methods=['GET'])
def get_data():
    """Retorna os dados brutos"""
    return jsonify(df_data.to_dict('records'))

@app.route('/api/filters', methods=['GET'])
def get_filters():
    """Retorna as opções dos filtros"""
    return jsonify({
        'restaurantes': sorted(df_data['restaurante'].unique().tolist()),
        'bairros': sorted(df_data['bairro'].unique().tolist()),
        'categorias': sorted(df_data['categoria'].unique().tolist()),
        'date_range': {
            'min': df_data['data'].min().isoformat(),
            'max': df_data['data'].max().isoformat()
        }
    })

@app.route('/api/graphs', methods=['POST'])
def get_graphs():
    """Retorna os dados dos gráficos baseado nos filtros"""
    filters = request.json
    
    df_filtered = df_data.copy()
    
    # Aplicar filtros
    if filters.get('restaurante'):
        df_filtered = df_filtered[df_filtered['restaurante'] == filters['restaurante']]
    if filters.get('bairro'):
        df_filtered = df_filtered[df_filtered['bairro'] == filters['bairro']]
    if filters.get('categoria'):
        df_filtered = df_filtered[df_filtered['categoria'] == filters['categoria']]
    if filters.get('start_date') and filters.get('end_date'):
        start = pd.to_datetime(filters['start_date'])
        end = pd.to_datetime(filters['end_date'])
        df_filtered = df_filtered[(df_filtered['data'] >= start) & (df_filtered['data'] <= end)]
    
    # Histograma
    hist_fig = px.histogram(
        df_filtered, 
        x="prato", 
        title="📈 Pratos Mais Vendidos",
        labels={'prato': 'Prato', 'count': 'Vendas'},
        color_discrete_sequence=['#ff6b6b']
    )
    hist_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis_tickangle=-45,
        height=400
    )
    
    # Mapa
    map_fig = px.scatter_mapbox(
        df_filtered,
        lat="LATITUDE",
        lon="LONGITUDE",
        color="categoria",
        size="preco",
        hover_name="restaurante",
        opacity=0.7,
        zoom=11,
        title="📍 Localização dos Restaurantes"
    )
    
    map_fig.update_layout(
        mapbox=dict(
            center=dict(lat=mean_lat, lon=mean_long),
            style="open-street-map"
        ),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        height=500
    )
    
    return jsonify({
        'histogram': json.loads(hist_fig.to_json()),
        'map': json.loads(map_fig.to_json()),
        'stats': {
            'total_vendas': len(df_filtered),
            'restaurantes': df_filtered['restaurante'].nunique(),
            'preco_medio': float(df_filtered['preco'].mean()),
            'preco_total': float(df_filtered['preco'].sum())
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Verifica se a API está online"""
    return jsonify({'status': 'online'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
