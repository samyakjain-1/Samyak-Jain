# MarketAI - Design and Reasoning Explanation

This document explains the design choices, agent reasoning processes, and technical implementation details of the MarketAI system.

## 1. Agent Planning Style

MarketAI employs a **hybrid hierarchical and multi-agent planning style**, mirroring the `tradesage-mvp` reference project.

- **Hierarchical Control**: A central **Orchestrator** (`orchestrator.py`) acts as the top-level planner. It follows a predefined, sequential graph of tasks, ensuring a structured and predictable workflow.
- **Multi-Agent Collaboration**: The Orchestrator delegates specific sub-tasks to a team of six specialized agents. Each agent is an expert in its domain, making the system modular and extensible.

The workflow is as follows:
1.  The **Orchestrator** receives the initial hypothesis.
2.  It calls the **`HypothesisAgent`** to structure the input into a clear, testable statement.
3.  It calls the **`ContextAgent`** to enrich the structured hypothesis with broader market context and define key research parameters.
4.  It calls the **`ResearchAgent`** and **`ContradictionAgent`** in parallel to gather supporting and opposing evidence using the data tools.
5.  It passes all collected evidence to the **`SynthesisAgent`** to create a final, balanced report with a confidence score.
6.  Finally, it calls the **`AlertAgent`** to generate actionable alerts based on the report's findings.

## 2. Memory Usage

Memory is implemented through a **PostgreSQL database with SQLAlchemy**, fulfilling the `memory.py` concept in a robust, relational manner.

- **Short-Term Memory**: During a single analysis run, the state (structured hypothesis, context, research findings, etc.) is held in memory by the Orchestrator and passed between agents.
- **Long-Term Memory (PostgreSQL)**:
    - The `src/database/crud.py` module provides functions to interact with the database via SQLAlchemy sessions.
    - Every completed analysis is saved as a new row in the `reports` table.
    - All generated alerts are saved to the `alerts` table, linked to their corresponding report.
    - This provides a structured, long-term memory that can be queried for historical analysis.

## 3. Tool Integration

- **Gemini API**: This is the core tool for all agent reasoning. Each of the six agents uses a specific, detailed prompt (identical to those in `tradesage-mvp`) to leverage the `gemini-2.0-flash` model for its task.
- **External Data Tools (`src/tools/`)**:
    - Agents use a suite of pre-defined tools to interact with the outside world, abstracting away the complexity of direct API calls.
    - **`news_tool`**: Calls the `NewsService` to fetch financial news and sentiment from Alpha Vantage.
    - **`market_data_tool`**: Calls the `MarketDataService` to fetch real-time market data, with a fallback system (Alpha Vantage -> FMP -> Yahoo Finance scraping).

## 4. Known Limitations

- **Static Planning**: The Orchestrator follows a fixed plan. It cannot dynamically alter its course based on early findings.
- **Limited Toolset**: The current toolset is focused on news and basic market data. A production system would benefit from more advanced tools (e.g., for reading SEC filings, technical analysis).
- **No Frontend for Alerts**: The generated alerts are saved to the database but are not yet displayed in the Streamlit UI. This would require a new API endpoint and frontend component.
