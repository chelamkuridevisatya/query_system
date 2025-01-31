# Backend Dockerfile (backend/Dockerfile)

FROM python:3.9-alpine as backend-build

WORKDIR /app

# Copy requirements and install dependencies
COPY ./query_system/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY ./query_system /app/

# Expose port for Django (Gunicorn will run on this port)
EXPOSE 8000

# Run Gunicorn with Django (make sure `query_system.wsgi:application` is correct)
CMD ["gunicorn", "query_system.wsgi:application", "--bind", "0.0.0.0:8000"]
