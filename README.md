# Palmari Manager – Meccanismi® Smart Event Optimizer

App locale per la gestione dei palmari durante un evento (check-in/check-out, import CSV, dashboard).

---

## Avvio veloce (copia-incolla)

### Su macOS / Linux

Apri il **Terminale** e incolla questi comandi uno alla volta:

```bash
git clone https://github.com/drimzlab/palmari-meccanismi.git
cd palmari-meccanismi
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Poi apri nel browser: **http://127.0.0.1:5000**

### Su Windows

Apri **PowerShell** e incolla:

```powershell
git clone https://github.com/drimzlab/palmari-meccanismi.git
cd palmari-meccanismi
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Poi apri nel browser: **http://127.0.0.1:5000**

Per **fermare** l'app: nel terminale premi `Ctrl+C`.

---

## Non hai `git`? Scarica lo ZIP

1. Vai sulla pagina della repo su GitHub.
2. Clicca il bottone verde **Code → Download ZIP**.
3. Scompatta lo ZIP dove vuoi.
4. Apri il Terminale dentro la cartella scompattata e parti dal comando `python3 -m venv venv` della sezione sopra.

---

## Requisiti

- **Python 3.8+** ([python.org/downloads](https://www.python.org/downloads/) oppure `brew install python3` su Mac)
- Verifica con:
  ```bash
  python3 --version
  ```

---

## Note

- Il database SQLite (`palmari.db`) viene creato automaticamente al primo avvio nella cartella del progetto.
- I backup vengono salvati nella cartella `backups/` (ultimi 10).
- Per importare i palmari usa il CSV di esempio `sample_import.csv` (colonna `codice_dispositivo`, opzionale `esercente`).
- Avvii successivi: basta entrare nella cartella, fare `source venv/bin/activate` (Mac/Linux) o `venv\Scripts\activate` (Windows) e rilanciare `python app.py`.
