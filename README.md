# Palmari Manager – Meccanismi® Smart Event Optimizer

App per la gestione dei palmari durante un evento (check-in/check-out, import CSV, dashboard).

---

## Come si avvia (3 passaggi)

### 1. Scarica il progetto
In alto in questa pagina clicca il bottone verde **`Code`** → **`Download ZIP`**.

### 2. Scompatta
Fai doppio click sul file ZIP scaricato. Si creerà una cartella `palmari-manager-active-main`.

### 3. Avvia l'app

Dentro la cartella trovi due file. Usa quello giusto per il tuo computer:

| Computer | File da aprire |
|---|---|
| 🍎 Mac | **`AVVIA.command`** → leggi prima "Sul Mac la prima volta" qui sotto |
| 🪟 Windows | **`AVVIA.bat`** → doppio click |

Si aprirà una finestra nera che prepara tutto da sola e dopo qualche secondo l'app si apre nel browser sull'indirizzo `http://127.0.0.1:5000`.

**Per fermare l'app**: chiudi la finestra nera.

---

## ⚠️ Sul Mac la prima volta: NON fare doppio click

Se fai doppio click subito ti esce questo errore e non parte niente:

> *"AVVIA.command" cannot be opened because it is from an unidentified developer.*

È normale: macOS blocca i file scaricati da internet. Devi sbloccarlo **una volta sola**, così:

1. **Tasto destro** (o `Ctrl`+click) sul file `AVVIA.command`
2. Nel menu clicca **`Apri`**
3. Nella finestrella grigia che compare clicca di nuovo **`Apri`**

Da quel momento l'app parte e **le volte successive basta il doppio click normale**.

### Se dopo quei 3 click non parte lo stesso (macOS Sonoma/Sequoia)

1. Fai doppio click normale sul file (verrà bloccato, è ok).
2. Apri **Impostazioni di Sistema → Privacy e Sicurezza**.
3. Scorri in basso: troverai scritto *"AVVIA.command è stato bloccato…"* con accanto il bottone **`Apri comunque`**. Cliccalo.
4. Ti chiederà la password del Mac e ti farà vedere ancora una finestrella: clicca **`Apri`**.

---

## ⚠️ Su Windows la prima volta

Se compare la schermata blu **"Windows ha protetto il PC"**:

1. Clicca la scritta **`Ulteriori informazioni`**
2. Clicca il bottone **`Esegui comunque`** che appare in basso

---

## Prima volta: cosa aspettarsi

- La **prima volta** può metterci qualche minuto: scarica e installa Python da solo.
- Potrebbe chiederti la **password del computer** o una **conferma**: accetta e vai avanti.
- **Dalla seconda volta in poi** è istantaneo: doppio click e via.

---

## Note tecniche

- Il database (`palmari.db`) viene creato in automatico al primo avvio e resta nella cartella del progetto.
- I backup vengono salvati nella cartella `backups/` (ultimi 10).
- Per importare i palmari usa il CSV di esempio `sample_import.csv` (colonna `codice_dispositivo`, opzionale `esercente`).
