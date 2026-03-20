import React, { useState, useEffect } from 'react'
import axios from 'axios'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import Dashboard from './components/Dashboard'
import './App.css'

export default function App() {
  const [filters, setFilters] = useState({
    restaurante: null,
    bairro: null,
    categoria: null,
    start_date: null,
    end_date: null
  })
  
  const [filterOptions, setFilterOptions] = useState({
    restaurantes: [],
    bairros: [],
    categorias: [],
    date_range: {}
  })
  
  const [graphs, setGraphs] = useState({
    histogram: null,
    map: null,
    stats: null
  })
  
  const [loading, setLoading] = useState(false)

  // Carregar opções de filtro
  useEffect(() => {
    const fetchFilters = async () => {
      try {
        const response = await axios.get('/api/filters')
        setFilterOptions(response.data)
        
        // Definir datas padrão
        if (response.data.date_range) {
          setFilters(prev => ({
            ...prev,
            start_date: response.data.date_range.min,
            end_date: response.data.date_range.max
          }))
        }
      } catch (error) {
        console.error('Erro ao carregar filtros:', error)
      }
    }

    fetchFilters()
  }, [])

  // Carregar gráficos quando filtros mudam
  useEffect(() => {
    const fetchGraphs = async () => {
      setLoading(true)
      try {
        const response = await axios.post('/api/graphs', filters)
        setGraphs(response.data)
      } catch (error) {
        console.error('Erro ao carregar gráficos:', error)
      } finally {
        setLoading(false)
      }
    }

    if (filterOptions.restaurantes.length > 0) {
      fetchGraphs()
    }
  }, [filters])

  const handleFilterChange = (filterName, value) => {
    setFilters(prev => ({
      ...prev,
      [filterName]: value
    }))
  }

  return (
    <div className="app-container">
      <Header />
      <div className="app-body">
        <Sidebar 
          filters={filters}
          filterOptions={filterOptions}
          onFilterChange={handleFilterChange}
        />
        <Dashboard 
          graphs={graphs}
          stats={graphs.stats}
          loading={loading}
        />
      </div>
    </div>
  )
}
