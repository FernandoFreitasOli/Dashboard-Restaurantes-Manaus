import React from 'react'
import Plot from 'react-plotly.js'
import Stats from './Stats'
import './Dashboard.css'

export default function Dashboard({ graphs, stats, loading }) {
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
        {/* Stats */}
        {stats && <Stats stats={stats} />}

        {/* Gráficos */}
        <div className="charts-container">
          {/* Histograma */}
          <div className="chart-wrapper">
            <div className="chart-card">
              {graphs.histogram && (
                <Plot
                  data={graphs.histogram.data}
                  layout={{
                    ...graphs.histogram.layout,
                    paper_bgcolor: 'rgba(0,0,0,0)',
                    plot_bgcolor: 'rgba(255, 107, 107, 0.05)',
                  }}
                  config={{ responsive: true, displayModeBar: true }}
                  style={{ width: '100%', height: '100%' }}
                />
              )}
            </div>
          </div>

          {/* Mapa */}
          <div className="chart-wrapper full-width">
            <div className="chart-card">
              {graphs.map && (
                <Plot
                  data={graphs.map.data}
                  layout={{
                    ...graphs.map.layout,
                    paper_bgcolor: 'rgba(0,0,0,0)',
                  }}
                  config={{ responsive: true, displayModeBar: true }}
                  style={{ width: '100%', height: '100%' }}
                />
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
