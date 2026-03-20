import React from 'react'
import './Header.css'

export default function Header() {
  return (
    <header className="header fade-in">
      <div className="header-content">
        <div className="header-left">
          <div className="logo">📊</div>
          <div className="header-text">
            <h1>Análise de Vendas</h1>
            <h2>Restaurantes Manaus</h2>
          </div>
        </div>
        <p className="header-description">
          Explore as vendas de pequenos e médios restaurantes da cidade de Manaus
        </p>
      </div>
    </header>
  )
}
