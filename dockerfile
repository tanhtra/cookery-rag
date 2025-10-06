# Use the official Python image
FROM python:3.11-slim

# Set a working directory
WORKDIR /app

# Copy requirements (if you have one) first for Docker layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY cookery ./cookery

# Expose Streamlit default port
EXPOSE 8501

# Set environment variables
ENV STREAMLIT_SERVER_ENABLECORS=false
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV PYTHONUNBUFFERED=1

# Command to run the Streamlit app
CMD ["streamlit", "run", "cookery/appcore.py", "--server.port=8501", "--server.address=0.0.0.0"]
