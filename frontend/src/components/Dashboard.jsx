import React from 'react'
import Plot from 'react-plotly.js'
import Stats from './Stats'
import './Dashboard.css'

export default function Dashboard({ graphs, stats, loading }) {
  const plotConfig = { responsive: true, displayModeBar: true }

  const renderPlot = (graphObject, extraLayout = {}) => {
    if (!graphObject) return null

    return (
      <Plot
        data={graphObject.data}
        layout={{
          ...graphObject.layout,
          paper_bgcolor: 'rgba(0,0,0,0)',
          plot_bgcolor: 'rgba(255,255,255,0.01)',
          font: {
            color: '#f2fbfb',
            family: 'Space Grotesk, sans-serif'
          },
          ...extraLayout
        }}
        config={plotConfig}
        style={{ width: '100%', height: '100%' }}
      />
    )
  }

  if (loading) {
    return (
      <div className="dashboard">
        <div className="loading">
          <div className="loading-spinner"></div>
          <p>Carregando dados...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="dashboard fade-in">
      <div className="dashboard-content">
        {stats && <Stats stats={stats} />}

        <div className="section-title-group">
          <h3>Visao Executiva</h3>
          <p>Leitura rapida de volume, geografia e comportamento de vendas</p>
        </div>

        <div className="charts-container">
          <div className="chart-wrapper">
            <div className="chart-card">
              {renderPlot(graphs.histogram)}
            </div>

            <div className="chart-card">
              {renderPlot(graphs.forecast)}
            </div>
          </div>

          <div className="chart-wrapper full-width">
            <div className="chart-card">
              {renderPlot(graphs.map)}
            </div>
          </div>

          <div className="section-title-group">
            <h3>Insights Estrategicos</h3>
            <p>Tendencia temporal, ranking de oportunidade e comparativos de mercado</p>
          </div>

          <div className="chart-wrapper">
            <div className="chart-card">
              {renderPlot(graphs.temporal_trend)}
            </div>
            <div className="chart-card">
              {renderPlot(graphs.ranking)}
            </div>
          </div>

          <div className="ranking-table-card">
            <h4>Top Restaurantes por Oportunidade</h4>
            <div className="ranking-table">
              <div className="ranking-row ranking-header">
                <span>Restaurante</span>
                <span>Ticket Medio</span>
                <span>Crescimento (%)</span>
                <span>Score</span>
              </div>
              {(graphs.ranking_table || []).map((item) => (
                <div key={item.restaurante} className="ranking-row">
                  <span>{item.restaurante}</span>
                  <span>{Number(item.ticket_medio).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</span>
                  <span>{item.crescimento}%</span>
                  <span>{item.score_oportunidade}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="chart-wrapper">
            <div className="chart-card">
              {renderPlot(graphs.comparatives?.ticket_medio)}
            </div>
            <div className="chart-card">
              {renderPlot(graphs.comparatives?.faixa_preco)}
            </div>
          </div>

          <div className="chart-wrapper full-width">
            <div className="chart-card">
              {renderPlot(graphs.comparatives?.sazonalidade)}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
