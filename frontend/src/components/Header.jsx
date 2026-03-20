import React from 'react'
import './Header.css'

export default function Header() {
  return (
    <header className="header fade-in">
      <div className="header-content">
        <div className="header-left">
          <div className="logo">FI</div>
          <div className="header-text">
            <h1>FoodInsight Manaus</h1>
            <h2>Growth Intelligence para Restaurantes</h2>
          </div>
        </div>
        <p className="header-description">
          Forecast de demanda, tendencia temporal, ranking de oportunidade e comparativos estrategicos em uma unica visao.
        </p>
      </div>
    </header>
  )
}
