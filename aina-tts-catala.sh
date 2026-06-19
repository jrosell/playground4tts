#!/bin/bash
export SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export CURRENT_DIR="$(pwd)"
source "./venv/bin/activate"
PYTHON="$SCRIPT_DIR/venv/bin/python"
export ESPEAK_DATA_PATH="$SCRIPT_DIR/espeak-ng/espeak-ng-data"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:"$SCRIPT_DIR/espeak-ng/lib"
export PATH="$SCRIPT_DIR/espeak-ng/bin:$PATH"
cd "Matcha-TTS"

python3 aina-tts-catala/matcha_vocos_inference.py --output_path="$CURRENT_DIR/output" \
  --text_input="Bon dia Manel, avui anem a la muntanya." \
  --length_scale=0.8 --temperature=0.7 \
  --speaker_id 3
mv -f "$SCRIPT_DIR/output/spk_3/synth.wav" "$SCRIPT_DIR/output/aina-tts-catala-multiaccent.wav"
rm -rf "$SCRIPT_DIR/output/spk_3"


python3 aina-tts-catala/matcha_vocos_inference-multispeaker.py --output_path="$SCRIPT_DIR/output" \
  --text_input="Bon dia Manel, avui anem a la muntanya." \
  --length_scale=0.8 --temperature=0.7 \
  --speaker_id 3
mv -f "$SCRIPT_DIR/output/spk_3/synth.wav" "$SCRIPT_DIR/output/aina-tts-catala-multispeaker.wav"
rm -rf "$SCRIPT_DIR/output/spk_3"

