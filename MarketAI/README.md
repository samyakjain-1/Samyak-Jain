# MarketAI - Agentic Financial Analysis

MarketAI is an AI-powered system that automates the research process behind trading hypotheses. It treats market predictions as testable scientific statements, using a multi-agent system to provide evidence-based confidence scores.

This project is a submission for the Agentic AI App Hackathon.

## 📋 Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Repository Structure](#-repository-structure)
- [Setup and Installation](#-setup-and-installation)
- [Running the Application](#-running-the-application)

## 🏗️ Architecture Overview

MarketAI uses a multi-agent architecture orchestrated by a central controller. The system is built with Python, FastAPI, and the Google Gemini API.

- **Backend**: A FastAPI server that exposes an API for analyzing financial hypotheses.
- **Agents**: A team of six specialized AI agents, each responsible for a specific part of the analysis (structuring, context, research, contradiction, synthesis, and alerts).
- **Database**: PostgreSQL with SQLAlchemy for storing analysis reports and alerts.
- **Frontend**: A Streamlit application for interacting with the system.

(A more detailed diagram is in `ARCHITECTURE.md`)

## 📁 Repository Structure

```
MarketAI/
├── Dockerfile              # Container configuration for the backend
├── docker-compose.yml      # Defines the PostgreSQL service
├── Makefile                # Development commands
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── src/
│   ├── adk/
│   │   ├── main.py         # FastAPI app entry point
│   │   ├── orchestrator.py # Core agent workflow planner/executor
│   │   └── agents/         # All 6 specialized agent definitions
│   ├── database/
│   │   ├── database.py     # SQLAlchemy connection
│   │   ├── models.py       # SQLAlchemy table models
│   │   └── crud.py         # Database operations
│   ├── services/           # Handles external API calls
│   ├── tools/              # Simple interfaces for agents to use services
│   └── frontend/
│       └── streamlit_app.py # Streamlit UI
├── ARCHITECTURE.md         # System architecture details
├── EXPLANATION.md          # Agent reasoning and design choices
└── DEMO.md                 # Link to the video demo
```

## ⚙️ Setup and Installation

Follow these steps to get the project running locally.

### 1. Prerequisites
- **Docker Desktop**: Make sure Docker is installed and running on your system.
- **Python 3.11+**: Ensure you have a compatible Python version.
- **Virtual Environment**: It is highly recommended to use a Python virtual environment.

### 2. Clone the Repository
```bash
git clone <your-repo-url>
cd MarketAI
```

### 3. Configure Environment Variables
Create a `.env` file by copying the example file:
```bash
cp .env.example .env
```
Now, open the `.env` file and add your secret keys:
- `GEMINI_API_KEY`: **Required.** Your API key from Google AI Studio.
- `ALPHA_VANTAGE_API_KEY`: **Required.** Your API key from Alpha Vantage for market data and news.
- `FMP_API_KEY`: **Optional.** A backup API key from Financial Modeling Prep.

The database credentials in `.env.example` are pre-configured to work with the Docker setup. You can leave them as they are.

### 4. Install Dependencies
Install all the required Python packages using the `Makefile`:
```bash
make install
```

## 🚀 Running the Application

The application requires three separate processes to be running: the database, the backend, and the frontend.

### 1. Start the Database
In your first terminal, from the `MarketAI` directory, start the PostgreSQL database using Docker:
```bash
docker-compose up
```
You can add the `-d` flag to run it in the background.

### 2. Start the Backend
In a second terminal, from the `MarketAI` directory, start the FastAPI backend server:
```bash
make run-backend
```
The backend will be available at `http://localhost:8080`.

### 3. Start the Frontend
In a third terminal, from the `MarketAI` directory, start the Streamlit frontend:
```bash
make run-frontend
```
This will automatically open the application in your web browser at `http://localhost:8501`. You are now ready to use MarketAI!
