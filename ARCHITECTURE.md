# MarketAI - System Architecture

This document outlines the architecture of the MarketAI system.

## High-Level Design

MarketAI is composed of three main layers:
1.  **Frontend**: A Streamlit web application for user interaction.
2.  **Backend**: A FastAPI server that hosts the agentic workflow.
3.  **Data Layer**: A MongoDB database for persistence and memory.

## System Diagram

```
[USER] -> [Frontend (Streamlit)] -> [Backend (FastAPI)]
                                          |
                                          v
                                [Orchestrator Agent]
                               /          |           \
                              /           |            \
                             v            v             v
        [Hypothesis Agent] [Research Agent] [Contradiction Agent]
                             \            |             /
                              \           |            /
                               v          v           v
                                [Synthesis Agent] -> [MongoDB]
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
- **Technology**: FastAPI, Google ADK, Gemini API
- **Components**:
    - **`main.py`**: The FastAPI application entry point. Defines the `/analyze` endpoint.
    - **`orchestrator.py`**: The core planner/executor. It manages the flow of data between all other agents.
    - **`agents/`**: Contains the specialized agents:
        - `HypothesisAgent`: Structures the user's query.
        - `ResearchAgent`: Gathers supporting evidence.
        - `ContradictionAgent`: Finds counter-arguments and risks.
        - `SynthesisAgent`: Aggregates all data and generates the final confidence score and report.

### 3. Data Layer (`src/database/`)
- **Technology**: MongoDB, PyMongo
- **Responsibilities**:
    - Store the results of each analysis.
    - Log the inputs and outputs of each agent for traceability.
    - Act as the long-term memory for the system.

### 4. Tools (`src/tools/`)
- **Responsibilities**:
    - Provide agents with the ability to interact with the outside world.
    - Examples: A tool for scraping financial news websites, a tool for fetching stock prices from an API.
