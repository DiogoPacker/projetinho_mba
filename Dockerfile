FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY apps ./apps
COPY .streamlit ./.streamlit
RUN pip install --no-cache-dir .
EXPOSE 8501 8000
CMD ["python", "-m", "streamlit", "run", "apps/dashboard.py", "--server.address", "0.0.0.0"]
