# Palmari Manager – Meccanismi® Smart Event Optimizer

App per la gestione dei palmari durante un evento (check-in/check-out, import CSV, dashboard).

---

## Come si avvia (3 passaggi)

### 1. Scarica il progetto
In alto in questa pagina clicca il bottone verde **`Code`** → **`Download ZIP`**.

### 2. Scompatta
Fai doppio click sul file ZIP scaricato. Si creerà una cartella `palmari-manager-active-main`.

### 3. Fai doppio click sul file di avvio
Dentro la cartella trovi due file. Usa quello giusto per il tuo computer:

| Computer | File da aprire con doppio click |
|---|---|
| 🍎 Mac | **`AVVIA.command`** |
| 🪟 Windows | **`AVVIA.bat`** |

Si aprirà una finestra nera che prepara tutto da sola e dopo qualche secondo l'app si apre nel browser sull'indirizzo `http://127.0.0.1:5000`.

**Per fermare l'app**: chiudi la finestra nera.

---

## Prima volta: cosa aspettarsi

- La **prima volta** può metterci qualche minuto: scarica e installa Python da solo.
- Potrebbe chiederti la **password del computer** o una **conferma**: accetta e vai avanti.
- **Dalla seconda volta in poi** è istantaneo: doppio click e via.

### Se su Mac dice "Impossibile aprire, sviluppatore non identificato"

1. **Tasto destro** (o `Ctrl`+click) sul file `AVVIA.command`
2. Scegli **`Apri`**
3. Nella finestra che appare clicca di nuovo **`Apri`**

Da quel momento funzionerà sempre con il doppio click normale.

### Se su Windows dice "Windows ha protetto il PC"

1. Clicca **`Ulteriori informazioni`**
2. Clicca **`Esegui comunque`**

---

## Note tecniche

- Il database (`palmari.db`) viene creato in automatico al primo avvio e resta nella cartella del progetto.
- I backup vengono salvati nella cartella `backups/` (ultimi 10).
- Per importare i palmari usa il CSV di esempio `sample_import.csv` (colonna `codice_dispositivo`, opzionale `esercente`).
