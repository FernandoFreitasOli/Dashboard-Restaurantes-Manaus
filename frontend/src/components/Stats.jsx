import React from 'react'
import './Stats.css'

export default function Stats({ stats }) {
  if (!stats) return null

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value)
  }

  return (
    <div className="stats-grid">
      <div className="stat-card">
        <div className="stat-icon">📊</div>
        <div className="stat-content">
          <p className="stat-label">Total de Vendas</p>
          <p className="stat-value">{stats.total_vendas.toLocaleString('pt-BR')}</p>
        </div>
      </div>

      <div className="stat-card">
        <div className="stat-icon">🏪</div>
        <div className="stat-content">
          <p className="stat-label">Restaurantes</p>
          <p className="stat-value">{stats.restaurantes}</p>
        </div>
      </div>

      <div className="stat-card">
        <div className="stat-icon">💰</div>
        <div className="stat-content">
          <p className="stat-label">Preço Médio</p>
          <p className="stat-value">{formatCurrency(stats.preco_medio)}</p>
        </div>
      </div>

      <div className="stat-card">
        <div className="stat-icon">💵</div>
        <div className="stat-content">
          <p className="stat-label">Total em Vendas</p>
          <p className="stat-value">{formatCurrency(stats.preco_total)}</p>
        </div>
      </div>

      <div className="stat-card">
        <div className="stat-icon">🎫</div>
        <div className="stat-content">
          <p className="stat-label">Ticket Medio</p>
          <p className="stat-value">{formatCurrency(stats.ticket_medio)}</p>
        </div>
      </div>

      <div className="stat-card">
        <div className="stat-icon">🌐</div>
        <div className="stat-content">
          <p className="stat-label">Restaurantes no Mercado</p>
          <p className="stat-value">{(stats.market_restaurantes || 0).toLocaleString('pt-BR')}</p>
        </div>
      </div>
    </div>
  )
}
