#!/bin/bash
source "./venv/bin/activate"
cd microsoft-tts-catala

echo "Running inference-simple.py"
python3 inference-simple.py

echo "Running inference-embeddings.py"
python3 inference-embeddings.py