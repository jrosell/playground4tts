#!/bin/bash
rm -rf ./venv ./espeak-ng ./Matcha-TTS ./output
mkdir output
python3 -m venv venv
source "./venv/bin/activate"
git clone https://github.com/espeak-ng/espeak-ng
export CURRENT_DIR="$(pwd)"
export PYTHON="$CURRENT_DIR/venv/bin/python"
cd "$CURRENT_DIR/espeak-ng" && \
    ./autogen.sh && \\
    ./configure --prefix="$CURRENT_DIR/espeak-ng" && \
    make && \
    make install
cd "$CURRENT_DIR"
git clone -b dev-cat https://github.com/langtech-bsc/Matcha-TTS.git
cd "Matcha-TTS"
pip install -e .
cd "$CURRENT_DIR"
pip install -r requirements.txt
