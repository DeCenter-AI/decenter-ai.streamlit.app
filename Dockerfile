# Stage 1: Install dependencies
FROM python:3.10 AS builder

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy only the dependency-related files
COPY pyproject.toml poetry.lock ./

# Install project dependencies using Poetry
RUN poetry install --no-root

# Stage 2: Copy application code and configure Streamlit
FROM python:3.10-slim

ENV mode=production

EXPOSE 8501

WORKDIR /app

# Copy dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /app/venv /app/venv

# Activate the virtual environment
RUN . venv/bin/activate

# If you have a separate requirements-test.txt for testing, you can install it here.
# RUN if [ "$mode" = "testing" ]; then pip install -r requirements-test.txt; fi

# Copy the rest of your application code
COPY . .

# Modify Streamlit config if needed
RUN sed -i 's/\(runOnSave =\).*/\1 false/' .streamlit/config.toml

CMD ["python", "-m", "streamlit", "run", "main.py"]
