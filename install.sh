#!/bin/bash
export CURRENT_DIR="$(pwd)"
export SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Script is located in: $SCRIPT_DIR"

rm -rf ./venv ./output
mkdir output

# sudo apt-get install build-essential autoconf automake libtool pkg-config espeak-ng libespeak-ng-dev mbrola mbrola-en1 speech-dispatcher speech-dispatcher-espeak-ng

if [ ! -d ~/espeak-ng ]; then
    rm -rf "$SCRIPT_DIR/espeak-ng"
    cd ~/
    git clone https://github.com/espeak-ng/espeak-ng    
    cd "$SCRIPT_DIR"
fi
if [ ! -d "$SCRIPT_DIR/espeak-ng" ]; then
    ls "$SCRIPT_DIR/espeak-ng"
    rsync -a ~/espeak-ng/ "$SCRIPT_DIR/espeak-ng"
    echo "Install espeak-nh and then re-run this script:"
    echo "$ cd espeak-ng"
    echo "$ ./autogen.sh && ./configure --prefix="/home/jordi/Projects/R-lang/playground4tts/espeak-ng" && make && make install"
    echo "$ cd .."
    echo "$ bash install.sh"
    exit 1
fi
cd "$SCRIPT_DIR"

python3.10 -m venv venv
source "./venv/bin/activate"

rm -rf "$SCRIPT_DIR/Matcha-TTS"
git clone -b dev-cat https://github.com/langtech-bsc/Matcha-TTS.git
cd "Matcha-TTS"
pip install -e .
pip install -r requirements.txt

cd "$SCRIPT_DIR"
pip install -r requirements.txt

cd "$CURRENT_DIR"