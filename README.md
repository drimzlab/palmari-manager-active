# Palmari Manager – Meccanismi® Smart Event Optimizer

App locale per la gestione dei palmari durante un evento (check-in/check-out, import CSV, dashboard).

---

## Avvio veloce — per chi non è sviluppatore

Il blocco di comandi qui sotto **installa Python da solo** se non ce l'hai già, poi scarica e avvia l'app. Durante l'installazione di Python il sistema potrebbe chiederti la **password del tuo Mac** o di premere **Invio** per confermare: è normale, vai avanti.

### 1. Scarica il progetto

- Vai su **https://github.com/drimzlab/palmari-manager-active**
- Clicca il bottone verde **Code → Download ZIP**
- Scompatta lo ZIP (doppio click sul file scaricato). Otterrai una cartella tipo `palmari-manager-active-main`.

### 2a. Su macOS

1. Apri **Terminale** (⌘+Spazio → scrivi "Terminale" → Invio).
2. Trascina la cartella scompattata nel Terminale, dopo aver scritto `cd ` (con uno spazio). Esempio:
   ```bash
   cd /Users/tuonome/Downloads/palmari-manager-active-main
   ```
   Premi Invio.
3. Copia e incolla **tutto questo blocco** nel Terminale e premi Invio:
   ```bash
   # Installa Homebrew + Python se mancano
   command -v brew >/dev/null 2>&1 || /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   command -v python3 >/dev/null 2>&1 || brew install python
   # Prepara ambiente e avvia l'app
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python app.py
   ```
4. Apri il browser su **http://127.0.0.1:5000**

### 2b. Su Windows

1. Apri **PowerShell** (tasto Windows → scrivi "PowerShell" → Invio).
2. Spostati nella cartella scompattata. Esempio:
   ```powershell
   cd C:\Users\TuoNome\Downloads\palmari-manager-active-main
   ```
3. Copia e incolla **tutto questo blocco** in PowerShell e premi Invio:
   ```powershell
   # Installa Python se manca (tramite winget, già presente su Windows 10/11)
   if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
     winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
   }
   # Prepara ambiente e avvia l'app
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python app.py
   ```
   > Se PowerShell blocca l'attivazione di `venv` con un errore di "execution policy", lancia una volta questo comando e ripeti il blocco:
   > ```powershell
   > Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
   > ```
4. Apri il browser su **http://127.0.0.1:5000**

Per **fermare** l'app: nel terminale premi `Ctrl+C`.

---

## Avvii successivi (dopo la prima volta)

L'installazione di Python e delle dipendenze **non va rifatta**. Ti basta rientrare nella cartella e riavviare:

**macOS:**
```bash
cd /percorso/della/cartella
source venv/bin/activate
python app.py
```

**Windows:**
```powershell
cd C:\percorso\della\cartella
.\venv\Scripts\Activate.ps1
python app.py
```

Poi apri **http://127.0.0.1:5000**.

---

## Note

- Il database SQLite (`palmari.db`) viene creato automaticamente al primo avvio nella cartella del progetto.
- I backup vengono salvati nella cartella `backups/` (ultimi 10).
- Per importare i palmari usa il CSV di esempio `sample_import.csv` (colonna `codice_dispositivo`, opzionale `esercente`).
