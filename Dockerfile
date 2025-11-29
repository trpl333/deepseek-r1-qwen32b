FROM pytorch/pytorch:2.2.0-cuda11.8-cudnn8-runtime

# Copy RunPod serverless metadata
COPY .runpod /runpod

# Copy handler files to /handler
COPY handler.py /handler/handler.py
COPY serverless.py /handler/serverless.py

# Set working directory
WORKDIR /handler

# Install your dependencies
RUN pip install --upgrade pip && \
    pip install torch transformers accelerate runpod

# Start the serverless worker
CMD ["python3", "-u", "serverless.py"]
