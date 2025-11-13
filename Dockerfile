FROM python:3.12-slim

# Update image
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      procps \
      net-tools \
      curl \
      netcat-openbsd

WORKDIR /app
COPY app.py .
RUN pip install --no-cache-dir flask requests

EXPOSE 5000
CMD ["python", "app.py"]
