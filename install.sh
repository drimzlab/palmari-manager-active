#!/bin/bash
# Installer bootstrap per Palmari Manager su macOS.
# Uso: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/drimzlab/palmari-manager-active/main/install.sh)"
set -e

INSTALL_DIR="$HOME/palmari-manager-active"
REPO_TARBALL="https://github.com/drimzlab/palmari-manager-active/archive/refs/heads/main.tar.gz"

printf "\n===========================================\n"
printf "   PALMARI MANAGER - INSTALLAZIONE\n"
printf "===========================================\n\n"

# --- 1. Scarica (o aggiorna) il progetto ---
echo "[1/4] Scarico il progetto in $INSTALL_DIR ..."
mkdir -p "$INSTALL_DIR"
curl -fsSL "$REPO_TARBALL" | tar -xz --strip-components=1 -C "$INSTALL_DIR"
cd "$INSTALL_DIR"

# --- 2. Homebrew ---
if ! command -v brew >/dev/null 2>&1; then
    echo "[2/4] Installazione Homebrew (ti chiedera' la password del Mac)..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "[2/4] Homebrew gia' presente."
fi
if [ -x /opt/homebrew/bin/brew ]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
elif [ -x /usr/local/bin/brew ]; then
    eval "$(/usr/local/bin/brew shellenv)"
fi

# --- 3. Python ---
if ! command -v python3 >/dev/null 2>&1; then
    echo "[3/4] Installazione Python..."
    brew install python
else
    echo "[3/4] Python gia' presente."
fi

# --- 4. Ambiente virtuale + dipendenze ---
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "[4/4] Dipendenze pronte."

# Assicura che AVVIA.command sia eseguibile e senza quarantena
chmod +x AVVIA.command 2>/dev/null || true
xattr -dr com.apple.quarantine . 2>/dev/null || true

printf "\n===========================================\n"
printf "   TUTTO PRONTO!\n"
printf "===========================================\n\n"
printf "L'app si aprira' tra pochi secondi nel browser.\n"
printf "Per fermarla: chiudi questa finestra o premi Ctrl+C.\n\n"
printf "DA OGGI IN POI, PER RIAVVIARE L'APP:\n"
printf "  1. Apri il Finder\n"
printf "  2. Vai nella cartella: %s\n" "$INSTALL_DIR"
printf "  3. Doppio click su AVVIA.command\n\n"

(sleep 3 && open "http://127.0.0.1:5000") &
python app.py
