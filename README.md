# MarketAI - Agentic Financial Analysis

MarketAI is an AI-powered system that automates the research process behind trading hypotheses. It treats market predictions as testable scientific statements, using a multi-agent system to provide evidence-based confidence scores.

This project is a submission for the Agentic AI App Hackathon.

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Architecture Overview](#-architecture-overview)
- [Repository Structure](#-repository-structure)
- [Local Development](#-local-development)
- [Cloud Deployment](#-cloud-deployment)

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** installed
- **Docker** (for containerized deployment)
- **MongoDB** instance (local or cloud-based)
- **Google Gemini API Key**

### Environment Setup

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd MarketAI

# 2. Set up environment variables
cp .env.example .env

# 3. Edit the .env file with your credentials:
# MONGO_URI="your-mongodb-connection-string"
# GEMINI_API_KEY="your-gemini-api-key"

# 4. Install dependencies
make install
```

## 🏗️ Architecture Overview

MarketAI uses a multi-agent architecture orchestrated by a central controller. The system is built with Python, FastAPI, and the Google Agent Development Kit (ADK).

- **Backend**: A FastAPI server that exposes an API for analyzing financial hypotheses.
- **Agents**: A team of specialized AI agents built with the Gemini API, each responsible for a specific part of the analysis (structuring, research, contradiction, synthesis).
- **Database**: MongoDB is used for storing analysis results, agent logs, and other persistent data.
- **Frontend**: A simple Streamlit application for interacting with the system.

(A more detailed diagram will be in `ARCHITECTURE.md`)

## 📁 Repository Structure

```
MarketAI/
├── Dockerfile              # Container configuration
├── Makefile                # Development commands
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── src/
│   ├── adk/
│   │   ├── main.py         # FastAPI app entry point
│   │   ├── orchestrator.py # Core agent workflow planner/executor
│   │   └── agents/         # Specialized agent definitions
│   ├── database/
│   │   ├── database.py     # MongoDB connection
│   │   └── crud.py         # Database operations
│   ├── tools/              # Tools for agents (e.g., web scraper)
│   └── frontend/
│       └── streamlit_app.py # Streamlit UI
├── ARCHITECTURE.md         # System architecture details
├── EXPLANATION.md          # Agent reasoning and design choices
└── DEMO.md                 # Link to the video demo
```

## 💻 Local Development

### Start the Backend Server

```bash
make run-backend
```
The backend will be available at `http://localhost:8080`.

### Start the Frontend Application

```bash
make run-frontend
```
The frontend will be available at `http://localhost:8501`.

## ☁️ Cloud Deployment

The application is designed to be deployed as a containerized service on platforms like Google Cloud Run.

### Build the Docker Image

```bash
docker build -t marketai-app .
```

### Run the Docker Container

```bash
docker run -p 8080:8080 -v $(pwd)/.env:/app/.env marketai-app
```
This command runs the container and makes the application available on `http://localhost:8080`.
