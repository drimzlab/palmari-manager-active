# Palmari Manager – Meccanismi® Smart Event Optimizer

App per la gestione dei palmari durante un evento (check-in/check-out, import CSV, dashboard).

---

## 🍎 Avvio su Mac

### La prima volta (unica "seccatura", 2 minuti)

macOS blocca i file `.command` scaricati da internet. Per aggirare il problema in modo pulito si usa un **comando unico nel Terminale** (è il metodo standard, lo stesso che si usa per installare Homebrew).

1. **Apri il Terminale**
   - Premi `⌘` + `Spazio` (apre la ricerca Spotlight)
   - Scrivi `Terminale` e premi Invio

2. **Copia la riga qui sotto, incollala nel Terminale e premi Invio**:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/drimzlab/palmari-manager-active/main/install.sh)"
   ```

3. **Segui le richieste**:
   - Se chiede la **password del Mac**: scrivila e premi Invio (i caratteri non si vedono mentre digiti, è normale).
   - Se chiede di premere Invio per confermare: premi Invio.

4. **Aspetta qualche minuto**. Scarica e installa automaticamente Python e tutte le dipendenze. Quando ha finito, l'app si apre da sola nel browser su `http://127.0.0.1:5000`.

> Per **fermare l'app**: chiudi la finestra del Terminale (oppure `Ctrl`+`C`).

### Le volte successive → doppio click

Dalla seconda volta in poi **non serve più il Terminale**:

1. Apri il **Finder**
2. Vai nella cartella **`palmari-manager-active`** (è dentro la tua cartella utente)
3. **Doppio click** sul file **`AVVIA.command`**

Funziona senza errori perché è stato creato dall'installer, non scaricato da Safari/Chrome.

### Per aggiornare l'app in futuro

Rilancia lo stesso comando del punto 2 della "prima volta": scarica la versione aggiornata, conserva il database e i backup, riavvia l'app.

---

## 🪟 Avvio su Windows

### La prima volta

1. In alto in questa pagina clicca il bottone verde **`Code`** → **`Download ZIP`**.
2. Doppio click sullo ZIP scaricato per scompattarlo.
3. Entra nella cartella e **doppio click su `AVVIA.bat`**.

Se compare la schermata blu **"Windows ha protetto il PC"**:
- Clicca **`Ulteriori informazioni`**
- Clicca il bottone **`Esegui comunque`**

Lo script installa Python da solo (tramite `winget`, incluso in Windows 10/11), prepara l'ambiente e avvia l'app. La prima volta può metterci qualche minuto.

### Le volte successive

Doppio click su **`AVVIA.bat`** nella stessa cartella. Basta.

---

## Cosa aspettarsi la prima volta

- **Scarica e installa Python** se non ce l'hai: richiede qualche minuto e connessione internet.
- Potrebbe chiedere la **password del computer** o una **conferma**: accetta e vai avanti.
- **Le volte successive** è quasi immediato.

---

## Note tecniche

- Il database (`palmari.db`) viene creato in automatico al primo avvio e resta nella cartella del progetto.
- I backup vengono salvati nella cartella `backups/` (ultimi 10).
- Per importare i palmari usa il CSV di esempio `sample_import.csv` (colonna `codice_dispositivo`, opzionale `esercente`).
- Su Mac l'installer mette la cartella in `~/palmari-manager-active`.
