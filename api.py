from flask import Flask, jsonify, request
from flask_cors import CORS
from urllib import parse, request as urlrequest
import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

app = Flask(__name__)
CORS(app)

DATA_PATH = "Dataset/pedidos_manaus_tratado.csv"
MARKET_PATH = "Dataset/restaurantes_mercado.csv"


def load_base_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["preco"] = pd.to_numeric(df["preco"], errors="coerce")

    tipo_map = {
        "Bebida": "Cafe e Bebidas",
        "Sobremesa": "Doceria e Sobremesas",
        "Massa": "Cozinha Italiana e Massas",
        "Frutos do Mar": "Cozinha Especializada",
        "Lanche": "Lanches e Fast Food",
        "Prato Principal": "Refeicao Completa",
    }
    df["tipo_restaurante"] = df["categoria"].map(tipo_map).fillna("Gastronomia Variada")
    return df.dropna(subset=["data", "preco", "LATITUDE", "LONGITUDE"])


df_data = load_base_data()
mean_lat = float(df_data["LATITUDE"].mean())
mean_long = float(df_data["LONGITUDE"].mean())


def to_json_fig(fig):
    return json.loads(fig.to_json())


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    filtered = df.copy()

    if filters.get("restaurante"):
        filtered = filtered[filtered["restaurante"] == filters["restaurante"]]
    if filters.get("bairro"):
        filtered = filtered[filtered["bairro"] == filters["bairro"]]
    if filters.get("categoria"):
        filtered = filtered[filtered["categoria"] == filters["categoria"]]
    if filters.get("start_date") and filters.get("end_date"):
        start = pd.to_datetime(filters["start_date"], errors="coerce")
        end = pd.to_datetime(filters["end_date"], errors="coerce")
        filtered = filtered[(filtered["data"] >= start) & (filtered["data"] <= end)]

    return filtered


def empty_fig(title: str):
    fig = go.Figure()
    fig.update_layout(
        title=title,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        annotations=[
            {
                "text": "Sem dados para os filtros selecionados",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 14},
            }
        ],
    )
    return fig


def build_main_histogram(df: pd.DataFrame):
    if df.empty:
        return empty_fig("Pratos Mais Vendidos")

    top_pratos = (
        df.groupby("prato").size().sort_values(ascending=False).head(12).reset_index(name="pedidos")
    )
    fig = px.bar(
        top_pratos,
        x="prato",
        y="pedidos",
        color="pedidos",
        color_continuous_scale="Teal",
        title="Pratos Mais Vendidos",
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_tickangle=-35,
        height=420,
        margin={"l": 35, "r": 15, "t": 50, "b": 75},
        coloraxis_showscale=False,
    )
    return fig


def build_map(df: pd.DataFrame):
    if df.empty:
        return empty_fig("Mapa de Restaurantes")

    fig = px.scatter_mapbox(
        df,
        lat="LATITUDE",
        lon="LONGITUDE",
        color="categoria",
        size="preco",
        size_max=26,
        hover_name="restaurante",
        hover_data={"bairro": True, "preco": ":.2f", "categoria": True},
        opacity=0.7,
        zoom=11,
        title="Mapa de Restaurantes e Perfil de Preco",
    )
    fig.update_layout(
        mapbox={"center": {"lat": mean_lat, "lon": mean_long}, "style": "open-street-map"},
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        margin={"l": 0, "r": 0, "t": 50, "b": 0},
        height=520,
    )
    return fig


def build_forecast(df: pd.DataFrame):
    title = "Previsao de Demanda por Categoria e Regiao"
    if df.empty:
        return empty_fig(title)

    daily = (
        df.groupby(["data", "categoria", "bairro"]).size().reset_index(name="pedidos").sort_values("data")
    )
    recent_cut = daily["data"].max() - pd.Timedelta(days=35)
    recent = daily[daily["data"] >= recent_cut]
    combos = (
        recent.groupby(["categoria", "bairro"])["pedidos"].sum().sort_values(ascending=False).head(4).index
    )

    fig = go.Figure()
    horizon = 14

    for categoria, bairro in combos:
        series = daily[(daily["categoria"] == categoria) & (daily["bairro"] == bairro)].copy()
        if series.empty:
            continue

        series = (
            series[["data", "pedidos"]]
            .set_index("data")
            .asfreq("D", fill_value=0)
            .reset_index()
        )
        series["smooth"] = series["pedidos"].rolling(7, min_periods=1).mean()

        x_idx = list(range(len(series)))
        y = series["smooth"].tolist()
        if len(y) > 1:
            x_mean = sum(x_idx) / len(x_idx)
            y_mean = sum(y) / len(y)
            numerator = sum((x - x_mean) * (v - y_mean) for x, v in zip(x_idx, y))
            denominator = sum((x - x_mean) ** 2 for x in x_idx) or 1
            slope = numerator / denominator
            intercept = y_mean - slope * x_mean
        else:
            slope = 0
            intercept = y[0] if y else 0

        last_date = series["data"].max()
        forecast_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=horizon, freq="D")
        start_idx = len(series)
        forecast_values = [max(0, intercept + slope * (start_idx + i)) for i in range(horizon)]

        label = f"{categoria} | {bairro}"
        fig.add_trace(
            go.Scatter(
                x=series["data"],
                y=series["pedidos"],
                mode="lines",
                name=f"Historico - {label}",
                line={"width": 2},
                opacity=0.45,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=forecast_dates,
                y=forecast_values,
                mode="lines+markers",
                name=f"Previsao - {label}",
                line={"dash": "dot", "width": 3},
            )
        )

    fig.update_layout(
        title=title,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=430,
        margin={"l": 35, "r": 15, "t": 50, "b": 35},
        yaxis_title="Pedidos por dia",
    )
    return fig


def build_temporal_trend(df: pd.DataFrame):
    title = "Tendencia Temporal por Tipo de Restaurante"
    if df.empty:
        return empty_fig(title)

    trend = (
        df.assign(mes=df["data"].dt.to_period("M").dt.to_timestamp())
        .groupby(["mes", "tipo_restaurante"])
        .size()
        .reset_index(name="pedidos")
        .sort_values("mes")
    )

    fig = px.line(
        trend,
        x="mes",
        y="pedidos",
        color="tipo_restaurante",
        markers=True,
        title=title,
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=410,
        margin={"l": 35, "r": 15, "t": 50, "b": 35},
        legend_title="Tipo",
    )
    return fig


def build_ranking(df: pd.DataFrame):
    title = "Ranking Inteligente: Oportunidade de Crescimento"
    if df.empty:
        return empty_fig(title), []

    last_date = df["data"].max()
    recent_cut = last_date - pd.Timedelta(days=30)
    prev_cut = recent_cut - pd.Timedelta(days=30)

    grouped = df.groupby("restaurante")
    ranking = grouped.agg(total_pedidos=("id", "count"), ticket_medio=("preco", "mean")).reset_index()

    recent = (
        df[df["data"] >= recent_cut].groupby("restaurante").size().rename("pedidos_recentes").reset_index()
    )
    previous = (
        df[(df["data"] >= prev_cut) & (df["data"] < recent_cut)]
        .groupby("restaurante")
        .size()
        .rename("pedidos_previos")
        .reset_index()
    )

    ranking = ranking.merge(recent, on="restaurante", how="left").merge(
        previous, on="restaurante", how="left"
    )
    ranking[["pedidos_recentes", "pedidos_previos"]] = ranking[
        ["pedidos_recentes", "pedidos_previos"]
    ].fillna(0)
    ranking["crescimento"] = (
        (ranking["pedidos_recentes"] - ranking["pedidos_previos"])
        / ranking["pedidos_previos"].replace(0, 1)
    )

    def normalize(series):
        s_min = series.min()
        s_max = series.max()
        if s_max == s_min:
            return series * 0 + 0.5
        return (series - s_min) / (s_max - s_min)

    ranking["score_demanda"] = normalize(ranking["total_pedidos"])
    ranking["score_ticket"] = normalize(ranking["ticket_medio"])
    ranking["score_crescimento"] = normalize(ranking["crescimento"])
    ranking["score_oportunidade"] = (
        0.45 * ranking["score_crescimento"]
        + 0.30 * ranking["score_ticket"]
        + 0.25 * (1 - ranking["score_demanda"])
    )

    ranking = ranking.sort_values("score_oportunidade", ascending=False)
    top = ranking.head(10).copy()

    fig = px.bar(
        top,
        x="score_oportunidade",
        y="restaurante",
        orientation="h",
        color="score_oportunidade",
        color_continuous_scale="Mint",
        title=title,
        hover_data={
            "ticket_medio": ":.2f",
            "total_pedidos": True,
            "crescimento": ":.2%",
            "score_oportunidade": ":.2f",
        },
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=430,
        margin={"l": 35, "r": 15, "t": 50, "b": 35},
        yaxis={"categoryorder": "total ascending"},
        coloraxis_showscale=False,
        xaxis_title="Score de oportunidade (0-1)",
    )

    table = top[["restaurante", "ticket_medio", "crescimento", "score_oportunidade"]].copy()
    table["ticket_medio"] = table["ticket_medio"].round(2)
    table["crescimento"] = (table["crescimento"] * 100).round(1)
    table["score_oportunidade"] = table["score_oportunidade"].round(3)
    return fig, table.to_dict("records")


def build_comparatives(df: pd.DataFrame):
    if df.empty:
        return {
            "ticket_medio": to_json_fig(empty_fig("Ticket Medio por Bairro")),
            "faixa_preco": to_json_fig(empty_fig("Faixa de Preco por Categoria")),
            "sazonalidade": to_json_fig(empty_fig("Sazonalidade de Pedidos")),
        }

    ticket = (
        df.groupby("bairro")["preco"].mean().sort_values(ascending=False).head(10).reset_index()
    )
    fig_ticket = px.bar(
        ticket,
        x="bairro",
        y="preco",
        color="preco",
        color_continuous_scale="IceFire",
        title="Comparativo de Ticket Medio por Bairro",
    )
    fig_ticket.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=380,
        margin={"l": 35, "r": 15, "t": 50, "b": 35},
        coloraxis_showscale=False,
    )

    fig_faixa = px.histogram(
        df,
        x="preco",
        color="categoria",
        nbins=25,
        barmode="overlay",
        opacity=0.65,
        title="Faixa de Preco por Categoria",
    )
    fig_faixa.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=380,
        margin={"l": 35, "r": 15, "t": 50, "b": 35},
        yaxis_title="Pedidos",
        xaxis_title="Preco (R$)",
    )

    seasonality = (
        df.assign(mes=df["data"].dt.month_name(), dia=df["data"].dt.day_name())
        .groupby(["dia", "mes"])
        .size()
        .reset_index(name="pedidos")
    )
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    month_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    seasonality["dia"] = pd.Categorical(seasonality["dia"], categories=day_order, ordered=True)
    seasonality["mes"] = pd.Categorical(seasonality["mes"], categories=month_order, ordered=True)
    seasonality = seasonality.sort_values(["dia", "mes"])

    fig_sazonalidade = px.density_heatmap(
        seasonality,
        x="mes",
        y="dia",
        z="pedidos",
        color_continuous_scale="Blues",
        title="Sazonalidade: Dia da Semana x Mes",
    )
    fig_sazonalidade.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=380,
        margin={"l": 35, "r": 15, "t": 50, "b": 35},
    )

    return {
        "ticket_medio": to_json_fig(fig_ticket),
        "faixa_preco": to_json_fig(fig_faixa),
        "sazonalidade": to_json_fig(fig_sazonalidade),
    }


def build_synthetic_market_dataset(df: pd.DataFrame, target_size: int = 120) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["nome", "categoria", "bairro", "faixa_preco", "fonte"])

    base = (
        df.groupby(["restaurante", "categoria", "bairro"])["preco"]
        .mean()
        .reset_index(name="ticket_medio")
    )
    generated_rows = []
    idx = 1
    while len(generated_rows) < target_size:
        row = base.iloc[(idx - 1) % len(base)]
        faixa = "economico"
        if row["ticket_medio"] >= 65:
            faixa = "premium"
        elif row["ticket_medio"] >= 40:
            faixa = "intermediario"

        generated_rows.append(
            {
                "nome": f"{row['restaurante']} - Unidade {idx}",
                "categoria": row["categoria"],
                "bairro": row["bairro"],
                "faixa_preco": faixa,
                "fonte": "sintetico",
            }
        )
        idx += 1

    return pd.DataFrame(generated_rows)


def scrape_market_data() -> pd.DataFrame:
    # Coleta de dados geograficos de restaurantes via Overpass (OpenStreetMap).
    overpass_query = """
    [out:json][timeout:25];
    area["name"="Manaus"]->.searchArea;
    (
      node["amenity"="restaurant"](area.searchArea);
      way["amenity"="restaurant"](area.searchArea);
      relation["amenity"="restaurant"](area.searchArea);
    );
    out center tags 220;
    """

    url = "https://overpass-api.de/api/interpreter"
    payload = parse.urlencode({"data": overpass_query}).encode("utf-8")

    rows = []
    try:
        req = urlrequest.Request(url, data=payload)
        with urlrequest.urlopen(req, timeout=25) as response:
            data = json.loads(response.read().decode("utf-8"))

        for item in data.get("elements", []):
            tags = item.get("tags", {})
            name = tags.get("name")
            if not name:
                continue

            cuisine = tags.get("cuisine", "variado")
            lat = item.get("lat") or item.get("center", {}).get("lat")
            lon = item.get("lon") or item.get("center", {}).get("lon")
            rows.append(
                {
                    "nome": name,
                    "categoria": cuisine,
                    "bairro": tags.get("addr:suburb") or tags.get("addr:city_district") or "Nao informado",
                    "faixa_preco": tags.get("price_range", "nao_informado"),
                    "latitude": lat,
                    "longitude": lon,
                    "fonte": "web",
                }
            )
    except Exception:
        pass

    df_market = pd.DataFrame(rows)
    synthetic = build_synthetic_market_dataset(df_data)

    if df_market.empty:
        final_df = synthetic
    else:
        merged = pd.concat([df_market, synthetic], ignore_index=True, sort=False)
        final_df = merged.drop_duplicates(subset=["nome"]).reset_index(drop=True)

    final_df.to_csv(MARKET_PATH, index=False)
    return final_df


def read_market_data() -> pd.DataFrame:
    if not os.path.exists(MARKET_PATH):
        return pd.DataFrame(columns=["nome", "categoria", "bairro", "faixa_preco", "fonte"])
    return pd.read_csv(MARKET_PATH)


@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify(df_data.to_dict("records"))


@app.route("/api/filters", methods=["GET"])
def get_filters():
    return jsonify(
        {
            "restaurantes": sorted(df_data["restaurante"].unique().tolist()),
            "bairros": sorted(df_data["bairro"].unique().tolist()),
            "categorias": sorted(df_data["categoria"].unique().tolist()),
            "date_range": {
                "min": df_data["data"].min().isoformat(),
                "max": df_data["data"].max().isoformat(),
            },
        }
    )


@app.route("/api/scraping/run", methods=["POST"])
def run_scraping_pipeline():
    market_df = scrape_market_data()
    return jsonify(
        {
            "status": "ok",
            "rows": int(len(market_df)),
            "source_breakdown": market_df["fonte"].value_counts().to_dict() if not market_df.empty else {},
        }
    )


@app.route("/api/market-data", methods=["GET"])
def market_data():
    market_df = read_market_data()
    return jsonify(
        {
            "total": int(len(market_df)),
            "preview": market_df.head(100).to_dict("records"),
            "sources": market_df["fonte"].value_counts().to_dict() if not market_df.empty else {},
        }
    )


@app.route("/api/graphs", methods=["POST"])
def get_graphs():
    filters = request.json or {}
    df_filtered = apply_filters(df_data, filters)

    hist_fig = build_main_histogram(df_filtered)
    map_fig = build_map(df_filtered)
    forecast_fig = build_forecast(df_filtered)
    trend_fig = build_temporal_trend(df_filtered)
    ranking_fig, ranking_table = build_ranking(df_filtered)
    comparatives = build_comparatives(df_filtered)
    market_df = read_market_data()

    stats = {
        "total_vendas": int(len(df_filtered)),
        "restaurantes": int(df_filtered["restaurante"].nunique()),
        "preco_medio": float(df_filtered["preco"].mean() if not df_filtered.empty else 0),
        "preco_total": float(df_filtered["preco"].sum() if not df_filtered.empty else 0),
        "ticket_medio": float(df_filtered.groupby("id")["preco"].mean().mean() if not df_filtered.empty else 0),
        "market_restaurantes": int(len(market_df)),
    }

    return jsonify(
        {
            "histogram": to_json_fig(hist_fig),
            "map": to_json_fig(map_fig),
            "forecast": to_json_fig(forecast_fig),
            "temporal_trend": to_json_fig(trend_fig),
            "ranking": to_json_fig(ranking_fig),
            "ranking_table": ranking_table,
            "comparatives": comparatives,
            "market": {
                "total": int(len(market_df)),
                "sources": market_df["fonte"].value_counts().to_dict() if not market_df.empty else {},
            },
            "stats": stats,
        }
    )


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "online"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
