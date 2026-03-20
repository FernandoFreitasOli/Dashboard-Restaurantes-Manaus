# FoodInsight Manaus

Dashboard de inteligencia para restaurantes de Manaus, criado para transformar dados brutos em insights acionaveis para pequenos e medios negocios.

## Visao Geral

O FoodInsight Manaus nasceu para responder perguntas reais de negocio com dados e visualizacao:

- Quais pratos sao mais vendidos em cada bairro?
- Quais categorias tem maior demanda?
- Como os precos variam por regiao?
- Onde estao as melhores oportunidades de crescimento?

## O Que Foi Desenvolvido

- ETL completo com limpeza, tratamento e enriquecimento de dados
- Filtros dinamicos por restaurante, bairro, categoria e periodo
- Mapa interativo de localizacao com contexto de categorias e precos
- Visualizacoes analiticas com histogramas e graficos interativos
- Estrutura reativa para atualizacao em tempo real com base nos filtros

## Melhorias Ja Implementadas

As melhorias prometidas na evolucao visual e de usabilidade foram aplicadas em grande parte:

- Redesign de interface com visual moderno e foco em dashboard premium
- Sidebar com filtros avancados e calendario em campos separados (data inicial/final)
- Correcoes de layout para evitar corte de calendario e melhorar responsividade
- Header com melhor hierarquia tipografica, profundidade visual e efeitos de destaque
- Cartoes de KPI (stats) com novo estilo, hover refinado e leitura mais clara
- Area de graficos com cards mais robustos, melhor espaco e contraste
- Base global de estilo (scrollbar, animacoes, tipografia e background) refinada

## Melhorias Extras Aplicadas Nesta Fase

- Ajuste de consistencia visual entre Sidebar, Header, Dashboard e Stats
- Efeitos de glassmorphism e sombras com melhor equilibrio para leitura
- Animacoes com transicoes mais suaves e coerentes em toda a interface
- Correcao de detalhes de CSS e normalizacao de elementos visuais

## Stack Tecnologica

### Backend
- Python
- Flask
- Pandas
- Plotly

### Frontend
- React
- Vite
- Plotly.js
- CSS customizado

## Estrutura do Projeto

```text
.
|- app.py
|- api.py
|- index_manaus.py
|- data_treatment.py
|- controllers_manaus.py
|- Dataset/
|  |- pedidos_manaus.csv
|  |- pedidos_manaus_tratado.csv
|  \- pedidos_manaus_atualizado.csv
\- frontend/
	|- src/
	|  |- components/
	|  \- ...
	\- ...
```

## Como Rodar

### 1. Backend (Python)

```bash
source .venv/bin/activate
python app.py
```

ou, para API dedicada:

```bash
source .venv/bin/activate
python api.py
```

### 2. Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

## Roadmap (Proximas Entregas)

- Previsao de demanda por categoria e regiao
- Analise de tendencia temporal por tipo de restaurante
- Ranking inteligente de restaurantes por oportunidade de crescimento
- Pipeline de web scraping para ampliar base com dados reais de mercado
- Novas visualizacoes comparativas (ticket medio, faixa de preco, sazonalidade)

## Objetivo de Impacto

A proposta do FoodInsight Manaus e apoiar decisoes de negocio com dados, tornando analise avancada mais acessivel para restaurantes locais.

---

Se quiser ver o projeto em detalhes ou trocar ideia sobre data analytics, dashboards e Python, fique a vontade para chamar.
