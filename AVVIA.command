#!/bin/bash
# Doppio click su questo file per avviare Palmari Manager su Mac.
set -e

# Posizionati nella cartella dello script
cd "$(dirname "$0")"

echo ""
echo "==========================================="
echo "   PALMARI MANAGER - AVVIO"
echo "==========================================="
echo ""

# --- 1. Homebrew ---
if ! command -v brew >/dev/null 2>&1; then
    echo "[1/4] Installazione Homebrew (potrebbe chiedere la password del Mac)..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Aggiungi brew al PATH della sessione corrente
if [ -x /opt/homebrew/bin/brew ]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
elif [ -x /usr/local/bin/brew ]; then
    eval "$(/usr/local/bin/brew shellenv)"
fi

# --- 2. Python ---
if ! command -v python3 >/dev/null 2>&1; then
    echo "[2/4] Installazione Python..."
    brew install python
else
    echo "[2/4] Python gia' presente."
fi

# --- 3. Ambiente virtuale + dipendenze ---
if [ ! -d "venv" ]; then
    echo "[3/4] Preparazione ambiente..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "[3/4] Dipendenze pronte."

# --- 4. Avvio app + apertura browser ---
echo "[4/4] Avvio applicazione..."
echo ""
echo "L'app si aprira' nel browser tra pochi secondi."
echo "Per fermare l'app: chiudi questa finestra."
echo ""

(sleep 3 && open "http://127.0.0.1:5000") &
python app.py
