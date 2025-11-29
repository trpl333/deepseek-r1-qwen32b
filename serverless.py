import runpod

# import the handler from the same directory (absolute import when running as a script)
from handler import handler

runpod.serverless.start({"handler": handler})
