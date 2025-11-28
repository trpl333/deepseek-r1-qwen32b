FROM runpod/worker-base:latest

# Copy RunPod serverless handler files into the container
COPY .runpod /handler

# Set handler directory
WORKDIR /handler

# Install your dependencies
RUN pip install torch transformers runpod accelerate

# Start RunPod Serverless worker
CMD ["python", "-u", "serverless.py"]
