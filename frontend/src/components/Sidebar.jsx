import React from 'react'
import './Sidebar.css'

export default function Sidebar({ filters, filterOptions, onFilterChange }) {
  return (
    <aside className="sidebar slide-in">
      <div className="sidebar-content">
        <h3 className="filters-title">🔍 Filtros Avançados</h3>

        {/* Filtro Restaurante */}
        <div className="filter-group">
          <label className="filter-label">
            <span className="filter-icon">🏪</span>
            Restaurante
          </label>
          <select
            className="filter-select"
            value={filters.restaurante || ''}
            onChange={(e) => onFilterChange('restaurante', e.target.value || null)}
          >
            <option value="">Todos os restaurantes</option>
            {filterOptions.restaurantes?.map((rest) => (
              <option key={rest} value={rest}>{rest}</option>
            ))}
          </select>
        </div>

        {/* Filtro Bairro */}
        <div className="filter-group">
          <label className="filter-label">
            <span className="filter-icon">📍</span>
            Bairro
          </label>
          <select
            className="filter-select"
            value={filters.bairro || ''}
            onChange={(e) => onFilterChange('bairro', e.target.value || null)}
          >
            <option value="">Todos os bairros</option>
            {filterOptions.bairros?.map((bairro) => (
              <option key={bairro} value={bairro}>{bairro}</option>
            ))}
          </select>
        </div>

        {/* Filtro Categoria */}
        <div className="filter-group">
          <label className="filter-label">
            <span className="filter-icon">🍽️</span>
            Categoria
          </label>
          <select
            className="filter-select"
            value={filters.categoria || ''}
            onChange={(e) => onFilterChange('categoria', e.target.value || null)}
          >
            <option value="">Todas as categorias</option>
            {filterOptions.categorias?.map((cat) => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>

        {/* Filtro Data */}
        <div className="filter-group">
          <label className="filter-label">
            <span className="filter-icon">📅</span>
            Data Inicial
          </label>
          <input
            type="date"
            className="filter-date"
            value={filters.start_date ? filters.start_date.split('T')[0] : ''}
            onChange={(e) => onFilterChange('start_date', e.target.value ? new Date(e.target.value).toISOString() : null)}
          />
        </div>

        <div className="filter-group">
          <label className="filter-label">
            <span className="filter-icon">📅</span>
            Data Final
          </label>
          <input
            type="date"
            className="filter-date"
            value={filters.end_date ? filters.end_date.split('T')[0] : ''}
            onChange={(e) => onFilterChange('end_date', e.target.value ? new Date(e.target.value).toISOString() : null)}
          />
        </div>

        {/* Botão Limpar Filtros */}
        <button
          className="btn-clear-filters"
          onClick={() => {
            onFilterChange('restaurante', null)
            onFilterChange('bairro', null)
            onFilterChange('categoria', null)
          }}
        >
          ✨ Resetar Filtros
        </button>

        {/* Informações adicionais */}
        <div className="sidebar-info">
          <p className="info-title">💡 Dica:</p>
          <p className="info-text">Use os filtros para explorar padrões de vendas por região, categoria e período.</p>
        </div>
      </div>
    </aside>
  )
}
