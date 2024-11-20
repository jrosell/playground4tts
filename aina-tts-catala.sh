#!/bin/bash
export CURRENT_DIR="$(pwd)"
source "./venv/bin/activate"
PYTHON="$CURRENT_DIR/venv/bin/python"
export ESPEAK_DATA_PATH="$CURRENT_DIR/espeak-ng/espeak-ng-data"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:"$CURRENT_DIR/espeak-ng/lib"
export PATH="$CURRENT_DIR/espeak-ng/bin:$PATH"
cd "Matcha-TTS"
python3 matcha_vocos_inference.py --output_path="$CURRENT_DIR/output" \
  --text_input="Bon dia Manel, avui anem a la muntanya." \
  --length_scale=0.8 --temperature=0.7 \
  --speaker_id 3
mv -f "$CURRENT_DIR/output/spk_3/synth.wav" "$CURRENT_DIR/output/aina-tts-catala.wav"
rm -rf "$CURRENT_DIR/output/spk_3"