# MarketAI - System Architecture

This document outlines the architecture of the MarketAI system, which is designed to be a close reflection of the `tradesage-mvp` reference project.

## High-Level Design

MarketAI is composed of three main layers:
1.  **Frontend**: A Streamlit web application for user interaction.
2.  **Backend**: A FastAPI server that hosts the agentic workflow.
3.  **Data Layer**: A PostgreSQL database with SQLAlchemy for persistence and memory.

## System Diagram

```
[USER] -> [Frontend (Streamlit)] -> [Backend (FastAPI)]
                                          |
                                          v
                                   [Orchestrator]
                                          |
                         +----------------+----------------+
                         |                |                |
                         v                v                v
            [HypothesisAgent] -> [ContextAgent] -> [ResearchAgent]
                                          |      [ContradictionAgent]
                                          |                |
                                          v                v
                                [SynthesisAgent] -> [AlertAgent]
                                          |                |
                                          v                v
                                     [Database (PostgreSQL)]
                                          |
                                          v
                                 [Final Report] -> [Frontend]
```

## Components

### 1. Frontend (`src/frontend/streamlit_app.py`)
- **Technology**: Streamlit
- **Responsibilities**:
    - Capture the user's natural language hypothesis.
    - Send the hypothesis to the backend API.
    - Display the final analysis report in a user-friendly format.

### 2. Backend (`src/adk/`)
- **Technology**: FastAPI, Google Gemini API
- **Components**:
    - **`main.py`**: The FastAPI application entry point. Defines the `/process` endpoint and handles database sessions.
    - **`orchestrator.py`**: The core planner/executor. It manages the sequential flow of data between all agents.
    - **`agents/`**: Contains the six specialized agents:
        - `HypothesisAgent`: Structures the user's query.
        - `ContextAgent`: Enriches the hypothesis with market context.
        - `ResearchAgent`: Gathers supporting evidence.
        - `ContradictionAgent`: Finds counter-arguments and risks.
        - `SynthesisAgent`: Aggregates all data and generates the final report.
        - `AlertAgent`: Creates actionable alerts from the report.

### 3. Data Layer (`src/database/`)
- **Technology**: PostgreSQL, SQLAlchemy
- **Responsibilities**:
    - Store the results of each analysis in a `reports` table.
    - Store the generated alerts in an `alerts` table.
    - Provide a structured, relational long-term memory for the system.

### 4. Services and Tools (`src/services/`, `src/tools/`)
- **Responsibilities**:
    - Provide agents with the ability to interact with the outside world.
    - **Services** contain the complex logic for calling external APIs (e.g., Alpha Vantage, FMP) and handling fallbacks.
    - **Tools** provide simple, clean interfaces for the agents to use the services.
