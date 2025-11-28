FROM runpod/worker-pytorch:latest

# Copy RunPod serverless handler files
COPY .runpod /runpod

# Copy handler logic to /src
COPY handler.py /src/handler.py
COPY serverless.py /src/serverless.py

WORKDIR /src

# Install model + inference dependencies
RUN pip install torch transformers accelerate runpod

# Start serverless worker
CMD ["python3", "-u", "serverless.py"]
