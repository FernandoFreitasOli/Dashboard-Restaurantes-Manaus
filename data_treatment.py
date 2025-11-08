# data_treatment.py corrigido para evitar warnings
import pandas as pd
import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')

# Carregar os dados
path = "Dataset/pedidos_manaus.csv"
df_data = pd.read_csv(path)

# Corrigir tipos de dados com formato específico para evitar warnings
df_data["data"] = pd.to_datetime(df_data["data"], format='%Y-%m-%d', errors='coerce')
df_data["preco"] = pd.to_numeric(df_data["preco"], errors='coerce')

# Mapear coordenadas simples por bairro (exemplo base)
bairro_coords = {
    "Vieiralves": (-3.101, -60.015),
    "Adrianópolis": (-3.096, -60.008),
    "Centro": (-3.132, -59.982),
    "Dom Pedro": (-3.097, -60.032),
    "Aleixo": (-3.083, -59.986),
    "Flores": (-3.085, -60.030),
    "Ponta Negra": (-3.102, -60.088),
    "Cidade Nova": (-2.995, -60.010),
    "Compensa": (-3.101, -60.051),
    "São Jorge": (-3.098, -60.045)
}

# Mapear latitude e longitude
df_data["LATITUDE"] = df_data["bairro"].map(lambda x: bairro_coords.get(x, (None, None))[0])
df_data["LONGITUDE"] = df_data["bairro"].map(lambda x: bairro_coords.get(x, (None, None))[1])

# Remover linhas com dados inválidos
df_data = df_data.dropna(subset=['data', 'LATITUDE', 'LONGITUDE'])

# Salvar dados tratados
cleaned_path = "Dataset/pedidos_manaus_tratado.csv"
df_data.to_csv(cleaned_path, index=False)
print("Dados tratados salvos em:", cleaned_path)
print(f"Total de registros: {len(df_data)}")
print("Primeiras linhas:")
print(df_data.head())