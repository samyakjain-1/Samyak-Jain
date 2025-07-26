# Makefile for MarketAI

# Ensure pip is used for installation
install:
	pip install -r requirements.txt

# Run backend server
run-backend:
	uvicorn src.adk.main:app --host 0.0.0.0 --port 8080 --reload

# Run streamlit frontend
run-frontend:
	streamlit run src/frontend/streamlit_app.py

# Run tests (placeholder for now)
test:
	@echo "No tests defined yet."

# Linting with ruff (placeholder)
lint:
	@echo "No linter configured yet."
