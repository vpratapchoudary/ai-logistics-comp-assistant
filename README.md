# AI Logistics Compliance Assistant

## Overview
Greatglobe Logistics manages a portfolio of more than 500 products across 20-30 client organizations and multiple jurisdictions. Every shipment may require international trade compliance checks, including import/export documentation, customs classification, duty calculation, and payment obligations. The manual process of bringing together product data and country-specific trade requirements is slow, inconsistent, and prone to operational risk.

This project automates that workflow with a lightweight AI assistant that:

- looks up product metadata from a local SQLite database,
- classifies the product by HS/HSN code,
- searches for current trade and customs guidance for a route,
- presents a concise compliance brief for logistics teams.

## Business Problem
The current process is fragmented:

- product records live in an internal database,
- customs and compliance details are researched manually online,
- each shipment route may require a different document set and payment process,
- route verification must be repeated across countries and clients.

This makes it difficult for supply chain teams to validate compliance quickly before shipping goods internationally.

## Solution Architecture
The application is a Streamlit-based assistant that combines structured product lookup with LLM-driven research.

### Components
- Frontend: Streamlit UI for shipment input
- Data layer: SQLite database with product catalog
- Agent orchestration: LangChain / LangGraph-style agent workflow
- Search layer: DuckDuckGo web search for current compliance sources
- Model layer: Groq-hosted LLM via LangChain

### Runtime Flow
1. The user selects a product and enters the source and destination countries in the Streamlit form.
2. `get_product_names()` loads the available catalog entries.
3. `get_product_details()` queries the `products` table using the selected product name.
4. A `ShippingDetails` Pydantic model packages the route and product metadata.
5. `search_shipping_requirements()` performs a targeted web search for import/export requirements, duties, and payment obligations.
6. The language model synthesizes the results into a concise compliance brief.

## Technical Stack
- Python 3.12+
- Streamlit
- LangChain
- LangChain Community
- DuckDuckGo Search
- SQLite
- Groq model integration (`groq:openai/gpt-oss-120b`)

## Project Structure

```text
ai-logistics-comp-assistant/
├── README.md
├── pyproject.toml
├── src/
│   └── ai_logistics_comp_assistant/
│       ├── __init__.py
│       ├── streamlit_app.py
│       ├── data/
│       │   └── greatglobe.db
│       └── core/
│           ├── agent.py
│           ├── prompt.py
│           └── tools.py
└── uv.lock
```

## Data Model
The core data source is the `products` table in the SQLite database.

| Column | Type | Description |
| --- | --- | --- |
| Product_ID | TEXT | Unique identifier for each product |
| Category | TEXT | Product category such as Automobile, Textiles, or Pharmaceuticals |
| Product_Name | TEXT | Human-readable product name |
| HS_Code | INTEGER | Harmonized System classification code used for customs processing |

The current dataset contains 500 product records and supports quick retrieval by product name.

## Agent Behavior
The assistant is constrained by a system prompt to:

- retrieve the exact product metadata from the database,
- use the HS code and trade route context,
- avoid generic shipping advice,
- report only relevant import/export requirements,
- recommend independent verification with official customs/trade authorities before shipment.

## Setup
This project uses the Python package manager `uv`.

```bash
uv sync
```

## Environment and Configuration
The app expects a valid LLM provider configuration for the Groq model used by LangChain. In a typical local setup, this is provided through the environment, for example with a `GROQ_API_KEY` variable.

## Run the Application
Start the Streamlit app from the repository root:

```bash
uv run streamlit run src/ai_logistics_comp_assistant/streamlit_app.py
```