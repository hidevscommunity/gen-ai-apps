# Stage 1: Install dependencies
FROM python:3.10 AS builder

WORKDIR /app

RUN python -m venv venv
RUN . venv/bin/activate

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Stage 2: Copy application code and configure Streamlit
FROM python:3.10-slim

ENV mode=production

EXPOSE 8501

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /app/venv /app/venv

RUN . venv/bin/activate

RUN if [ "$mode" = "testing" ]; then pip install -r requirements-test.txt; fi

COPY . .

RUN sed -i 's/\(runOnSave =\).*/\1 false/' .streamlit/config.toml

CMD ["python", "-m","streamlit", "run", "app.py"]
