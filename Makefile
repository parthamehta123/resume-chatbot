.PHONY: venv install run clean docker-build docker-run test

# Create a virtual environment and install dependencies
venv:
	python -m venv venv
	source venv/bin/activate && pip install -r requirements.txt

# Install dependencies (already assumes venv is activated)
install:
	source venv/bin/activate && pip install -r requirements.txt

# Run Streamlit app
run:
	python3 -m venv venv && \
	source venv/bin/activate && \
	python -m streamlit run images/streamlit/src/resume_chatbot/streamlit_app.py

# Clean all build-related files and directories
clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache venv .streamlit persist

# Build Docker image for the Streamlit app
docker-build:
	docker build -t resume-streamlit .

# Run Docker container for Streamlit app
docker-run:
	docker run -p 8501:8501 -v $(PWD)/persist:/app/persist resume-streamlit

# Test using pytest
test:
	python3 -m venv venv && \
	source venv/bin/activate && \
	pip install -r images/streamlit/requirements.txt && \
	PYTHONPATH=$(pwd)/images/streamlit/src pytest tests/unit
