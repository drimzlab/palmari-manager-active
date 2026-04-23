"""
Palmari Manager - Meccanismi(R) Smart Event Optimizer
Software locale per gestione palmari evento

Avvio: python app.py
Apri: http://127.0.0.1:5000
"""

import os
import csv
import io
import shutil
import sqlite3
import webbrowser
import threading
from datetime import datetime
from flask import Flask, render_template, request, jsonify, Response, send_from_directory

app = Flask(__name__)

# --- CONFIGURAZIONE ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'palmari.db')
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')


# --- DATABASE ---

def get_db():
    """Restituisce una connessione al database SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Crea le tabelle se non esistono."""
    conn = get_db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codice_completo TEXT UNIQUE NOT NULL,
            prefisso TEXT NOT NULL,
            numero INTEGER NOT NULL,
            stato TEXT DEFAULT 'DISPONIBILE'
                CHECK(stato IN ('DISPONIBILE', 'ASSEGNATO')),
            esercente TEXT,
            data_checkin TEXT,
            data_checkout TEXT
        );

        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codice_completo TEXT NOT NULL,
            operazione TEXT NOT NULL
                CHECK(operazione IN ('CHECKIN', 'CHECKOUT')),
            esercente TEXT,
            timestamp TEXT DEFAULT (datetime('now', 'localtime'))
        );

        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        INSERT OR IGNORE INTO settings (key, value)
            VALUES ('prefisso_default', 'A');
        INSERT OR IGNORE INTO settings (key, value)
            VALUES ('nome_evento', 'Evento');
    ''')
    conn.commit()
    conn.close()


def backup_db():
    """Crea un backup del database, mantiene gli ultimi 10."""
    if not os.path.exists(DB_PATH):
        return
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    shutil.copy2(DB_PATH, os.path.join(BACKUP_DIR, f'palmari_backup_{ts}.db'))
    # Pulizia vecchi backup
    backups = sorted([
        os.path.join(BACKUP_DIR, f)
        for f in os.listdir(BACKUP_DIR)
        if f.startswith('palmari_backup_') and f.endswith('.db')
    ])
    while len(backups) > 10:
        os.remove(backups.pop(0))


# --- ROUTES ---

@app.route('/')
def index():
    """Pagina principale."""
    return render_template('index.html')


@app.route('/sample_import.csv')
def sample_csv():
    """Serve il file CSV di esempio per il download."""
    return send_from_directory(BASE_DIR, 'sample_import.csv', as_attachment=True)


@app.route('/api/dashboard')
def dashboard():
    """Dati dashboard: totali, esercenti con palmari fuori, ultimi movimenti."""
    conn = get_db()

    totale = conn.execute('SELECT COUNT(*) FROM devices').fetchone()[0]
    disponibili = conn.execute(
        "SELECT COUNT(*) FROM devices WHERE stato='DISPONIBILE'"
    ).fetchone()[0]
    assegnati = conn.execute(
        "SELECT COUNT(*) FROM devices WHERE stato='ASSEGNATO'"
    ).fetchone()[0]

    oggi = datetime.now().strftime('%Y-%m-%d')
    rientrati_oggi = conn.execute(
        "SELECT COUNT(*) FROM logs WHERE operazione='CHECKOUT' AND timestamp LIKE ?",
        (f'{oggi}%',)
    ).fetchone()[0]

    esercenti = conn.execute('''
        SELECT esercente, COUNT(*) as count
        FROM devices
        WHERE stato='ASSEGNATO' AND esercente IS NOT NULL AND esercente != ''
        GROUP BY esercente ORDER BY count DESC
    ''').fetchall()

    # Dettaglio palmari ancora fuori (da ritirare)
    palmari_fuori = conn.execute('''
        SELECT codice_completo, esercente, data_checkin
        FROM devices
        WHERE stato='ASSEGNATO'
        ORDER BY esercente, numero
    ''').fetchall()

    # Palmari rientrati oggi (dettaglio)
    palmari_rientrati = conn.execute('''
        SELECT l.codice_completo, l.esercente, l.timestamp
        FROM logs l
        WHERE l.operazione='CHECKOUT' AND l.timestamp LIKE ?
        ORDER BY l.id DESC
    ''', (f'{oggi}%',)).fetchall()

    ultimi = conn.execute('''
        SELECT codice_completo, operazione, esercente, timestamp
        FROM logs ORDER BY id DESC LIMIT 20
    ''').fetchall()

    conn.close()

    return jsonify({
        'totale': totale,
        'disponibili': disponibili,
        'assegnati': assegnati,
        'rientrati_oggi': rientrati_oggi,
        'esercenti': [
            {'esercente': e['esercente'], 'count': e['count']}
            for e in esercenti
        ],
        'palmari_fuori': [
            {
                'codice': p['codice_completo'],
                'esercente': p['esercente'] or 'N/D',
                'data_checkin': p['data_checkin'] or ''
            }
            for p in palmari_fuori
        ],
        'palmari_rientrati': [
            {
                'codice': p['codice_completo'],
                'esercente': p['esercente'] or '',
                'timestamp': p['timestamp'] or ''
            }
            for p in palmari_rientrati
        ],
        'ultimi_movimenti': [
            {
                'codice': u['codice_completo'],
                'operazione': u['operazione'],
                'esercente': u['esercente'] or '',
                'timestamp': u['timestamp']
            }
            for u in ultimi
        ]
    })


@app.route('/api/checkin', methods=['POST'])
def checkin():
    """Check-in: assegna palmare a esercente."""
    data = request.json
    prefisso = data.get('prefisso', 'A').upper().strip()
    numero = data.get('numero', '').strip()
    esercente = data.get('esercente', '').strip()

    if not numero:
        return jsonify({'ok': False, 'errore': 'Numero palmare obbligatorio'}), 400
    if not esercente:
        return jsonify({'ok': False, 'errore': 'Nome esercente obbligatorio'}), 400

    codice = f'{prefisso}-{numero}'
    conn = get_db()
    device = conn.execute(
        'SELECT * FROM devices WHERE codice_completo=?', (codice,)
    ).fetchone()

    if not device:
        conn.close()
        return jsonify({
            'ok': False,
            'errore': f'Dispositivo {codice} non trovato nel database'
        }), 404

    if device['stato'] == 'ASSEGNATO':
        conn.close()
        return jsonify({
            'ok': False,
            'warning': True,
            'errore': f'Dispositivo {codice} gia\u0300 assegnato a: {device["esercente"]}'
        }), 409

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.execute(
        "UPDATE devices SET stato='ASSEGNATO', esercente=?, data_checkin=? "
        "WHERE codice_completo=?",
        (esercente, now, codice)
    )
    conn.execute(
        "INSERT INTO logs (codice_completo, operazione, esercente) VALUES (?, 'CHECKIN', ?)",
        (codice, esercente)
    )
    conn.commit()
    conn.close()

    return jsonify({
        'ok': True,
        'messaggio': f'CHECK-IN OK \u2014 {codice} \u2192 {esercente}'
    })


@app.route('/api/checkout', methods=['POST'])
def checkout():
    """Check-out: rientro palmare, stato torna DISPONIBILE."""
    data = request.json
    prefisso = data.get('prefisso', 'A').upper().strip()
    numero = data.get('numero', '').strip()

    if not numero:
        return jsonify({'ok': False, 'errore': 'Numero palmare obbligatorio'}), 400

    codice = f'{prefisso}-{numero}'
    conn = get_db()
    device = conn.execute(
        'SELECT * FROM devices WHERE codice_completo=?', (codice,)
    ).fetchone()

    if not device:
        conn.close()
        return jsonify({
            'ok': False,
            'errore': f'Dispositivo {codice} non trovato'
        }), 404

    if device['stato'] == 'DISPONIBILE':
        conn.close()
        return jsonify({
            'ok': False,
            'warning': True,
            'errore': f'Dispositivo {codice} e\u0300 gia\u0300 disponibile (non assegnato)'
        }), 409

    esercente_prec = device['esercente']
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn.execute(
        "UPDATE devices SET stato='DISPONIBILE', esercente=NULL, data_checkout=? "
        "WHERE codice_completo=?",
        (now, codice)
    )
    conn.execute(
        "INSERT INTO logs (codice_completo, operazione, esercente) VALUES (?, 'CHECKOUT', ?)",
        (codice, esercente_prec)
    )
    conn.commit()
    conn.close()

    return jsonify({
        'ok': True,
        'messaggio': f'CHECK-OUT OK \u2014 {codice} \u2190 {esercente_prec or "N/D"}'
    })


@app.route('/api/bulk-checkin', methods=['POST'])
def bulk_checkin():
    """Check-in massivo: segna dispositivi come ASSEGNATO.

    Modalita' (JSON body):
      mode='con_esercente' (default) -> solo palmari con esercente assegnato
      mode='tutti'                   -> tutti i palmari DISPONIBILI
    """
    data = request.get_json(silent=True) or {}
    mode = data.get('mode', 'con_esercente')

    conn = get_db()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if mode == 'tutti':
        devices = conn.execute(
            "SELECT codice_completo, esercente FROM devices "
            "WHERE stato='DISPONIBILE'"
        ).fetchall()
        msg_vuoto = 'Nessun dispositivo disponibile da assegnare'
    else:
        devices = conn.execute(
            "SELECT codice_completo, esercente FROM devices "
            "WHERE stato='DISPONIBILE' AND esercente IS NOT NULL AND esercente != ''"
        ).fetchall()
        msg_vuoto = 'Nessun dispositivo disponibile con esercente da assegnare'

    if not devices:
        conn.close()
        return jsonify({'ok': False, 'errore': msg_vuoto}), 404

    count = 0
    for d in devices:
        conn.execute(
            "UPDATE devices SET stato='ASSEGNATO', data_checkin=? WHERE codice_completo=?",
            (now, d['codice_completo'])
        )
        conn.execute(
            "INSERT INTO logs (codice_completo, operazione, esercente) VALUES (?, 'CHECKIN', ?)",
            (d['codice_completo'], d['esercente'])
        )
        count += 1

    conn.commit()
    conn.close()
    return jsonify({
        'ok': True,
        'messaggio': f'Check-in massivo completato: {count} palmari assegnati'
    })


@app.route('/api/bulk-checkout', methods=['POST'])
def bulk_checkout():
    """Check-out massivo: tutti i palmari assegnati tornano DISPONIBILE."""
    conn = get_db()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    devices = conn.execute(
        "SELECT codice_completo, esercente FROM devices WHERE stato='ASSEGNATO'"
    ).fetchall()

    if not devices:
        conn.close()
        return jsonify({
            'ok': False,
            'errore': 'Nessun dispositivo assegnato da rientrare'
        }), 404

    count = 0
    for d in devices:
        conn.execute(
            "UPDATE devices SET stato='DISPONIBILE', esercente=NULL, data_checkout=? "
            "WHERE codice_completo=?",
            (now, d['codice_completo'])
        )
        conn.execute(
            "INSERT INTO logs (codice_completo, operazione, esercente) VALUES (?, 'CHECKOUT', ?)",
            (d['codice_completo'], d['esercente'])
        )
        count += 1

    conn.commit()
    conn.close()
    return jsonify({
        'ok': True,
        'messaggio': f'Check-out massivo completato: {count} palmari rientrati'
    })


@app.route('/api/import', methods=['POST'])
def import_csv_route():
    """Importa dispositivi da file CSV."""
    if 'file' not in request.files:
        return jsonify({'ok': False, 'errore': 'Nessun file selezionato'}), 400

    file = request.files['file']
    if not file.filename:
        return jsonify({'ok': False, 'errore': 'Nessun file selezionato'}), 400

    try:
        content = file.read().decode('utf-8-sig')  # Gestisce BOM Excel

        # Rileva delimitatore (virgola o punto e virgola)
        delimiter = ','
        first_line = content.split('\n')[0]
        if ';' in first_line and ',' not in first_line:
            delimiter = ';'

        reader = csv.DictReader(io.StringIO(content), delimiter=delimiter)

        if not reader.fieldnames:
            return jsonify({'ok': False, 'errore': 'CSV vuoto'}), 400

        # Normalizza nomi colonne
        normalized_fields = [f.strip().lower() for f in reader.fieldnames]
        if 'codice_dispositivo' not in normalized_fields:
            return jsonify({
                'ok': False,
                'errore': 'Colonna "codice_dispositivo" non trovata nel CSV'
            }), 400

        # Opzione: segna come gia' assegnati i palmari con esercente
        auto_assign = request.form.get('auto_assign', 'false') == 'true'

        conn = get_db()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        inseriti = 0
        aggiornati = 0
        assegnati_auto = 0
        errori = 0

        for row in reader:
            row_clean = {
                k.strip().lower(): (v.strip() if v else '')
                for k, v in row.items()
            }

            codice = row_clean.get('codice_dispositivo', '').strip()
            if not codice or '-' not in codice:
                errori += 1
                continue

            parti = codice.split('-', 1)
            prefisso = parti[0].upper()
            try:
                numero = int(parti[1])
            except ValueError:
                errori += 1
                continue

            esercente = row_clean.get('esercente', '').strip() or None

            existing = conn.execute(
                'SELECT id, stato FROM devices WHERE codice_completo=?', (codice,)
            ).fetchone()

            if existing:
                if auto_assign and esercente and existing['stato'] == 'DISPONIBILE':
                    conn.execute(
                        "UPDATE devices SET esercente=?, stato='ASSEGNATO', data_checkin=? "
                        "WHERE codice_completo=?",
                        (esercente, now, codice)
                    )
                    conn.execute(
                        "INSERT INTO logs (codice_completo, operazione, esercente) "
                        "VALUES (?, 'CHECKIN', ?)",
                        (codice, esercente)
                    )
                    assegnati_auto += 1
                elif esercente:
                    conn.execute(
                        'UPDATE devices SET esercente=? WHERE codice_completo=?',
                        (esercente, codice)
                    )
                aggiornati += 1
            else:
                if auto_assign and esercente:
                    conn.execute(
                        'INSERT INTO devices (codice_completo, prefisso, numero, stato, esercente, data_checkin) '
                        'VALUES (?, ?, ?, ?, ?, ?)',
                        (codice, prefisso, numero, 'ASSEGNATO', esercente, now)
                    )
                    conn.execute(
                        "INSERT INTO logs (codice_completo, operazione, esercente) "
                        "VALUES (?, 'CHECKIN', ?)",
                        (codice, esercente)
                    )
                    assegnati_auto += 1
                else:
                    conn.execute(
                        'INSERT INTO devices (codice_completo, prefisso, numero, stato, esercente) '
                        'VALUES (?, ?, ?, ?, ?)',
                        (codice, prefisso, numero, 'DISPONIBILE', None)
                    )
                inseriti += 1

        conn.commit()
        conn.close()

        msg = f'Import completato: {inseriti} nuovi, {aggiornati} aggiornati'
        if assegnati_auto:
            msg += f', {assegnati_auto} auto-assegnati'
        if errori:
            msg += f', {errori} errori'
        return jsonify({'ok': True, 'messaggio': msg})

    except Exception as e:
        return jsonify({'ok': False, 'errore': f'Errore import: {str(e)}'}), 500


@app.route('/api/add-devices', methods=['POST'])
def add_devices_text():
    """Aggiunge dispositivi da testo libero (formato CSV inline)."""
    data = request.json
    testo = data.get('testo', '').strip()

    if not testo:
        return jsonify({'ok': False, 'errore': 'Nessun testo inserito'}), 400

    conn = get_db()
    inseriti = 0
    aggiornati = 0
    errori = 0
    righe_errore = []

    for i, riga in enumerate(testo.strip().split('\n'), 1):
        riga = riga.strip()
        if not riga:
            continue

        # Salta intestazione se presente
        if riga.lower().startswith('codice'):
            continue

        # Supporta virgola o punto e virgola
        sep = ';' if ';' in riga and ',' not in riga else ','
        parti = [p.strip() for p in riga.split(sep)]

        codice = parti[0].strip().upper() if parti else ''
        esercente = parti[1].strip() if len(parti) > 1 and parti[1].strip() else None

        if not codice or '-' not in codice:
            errori += 1
            righe_errore.append(f'Riga {i}: "{riga}" — formato non valido')
            continue

        codice_parti = codice.split('-', 1)
        prefisso = codice_parti[0]
        try:
            numero = int(codice_parti[1])
        except ValueError:
            errori += 1
            righe_errore.append(f'Riga {i}: "{riga}" — numero non valido')
            continue

        existing = conn.execute(
            'SELECT id FROM devices WHERE codice_completo=?', (codice,)
        ).fetchone()

        if existing:
            if esercente:
                conn.execute(
                    'UPDATE devices SET esercente=? WHERE codice_completo=?',
                    (esercente, codice)
                )
            aggiornati += 1
        else:
            conn.execute(
                'INSERT INTO devices (codice_completo, prefisso, numero, stato, esercente) '
                'VALUES (?, ?, ?, ?, ?)',
                (codice, prefisso, numero, 'DISPONIBILE', esercente)
            )
            inseriti += 1

    conn.commit()
    conn.close()

    msg = f'{inseriti} nuovi'
    if aggiornati:
        msg += f', {aggiornati} aggiornati'
    if errori:
        msg += f', {errori} errori'

    return jsonify({
        'ok': True,
        'messaggio': msg,
        'inseriti': inseriti,
        'aggiornati': aggiornati,
        'errori': errori,
        'righe_errore': righe_errore
    })


@app.route('/api/devices')
def devices_list():
    """Lista tutti i dispositivi, filtro opzionale per stato."""
    conn = get_db()
    stato = request.args.get('stato', '')

    if stato:
        rows = conn.execute(
            'SELECT * FROM devices WHERE stato=? ORDER BY prefisso, numero',
            (stato,)
        ).fetchall()
    else:
        rows = conn.execute(
            'SELECT * FROM devices ORDER BY prefisso, numero'
        ).fetchall()

    conn.close()
    return jsonify([{
        'id': d['id'],
        'codice': d['codice_completo'],
        'prefisso': d['prefisso'],
        'numero': d['numero'],
        'stato': d['stato'],
        'esercente': d['esercente'] or '',
        'data_checkin': d['data_checkin'] or '',
        'data_checkout': d['data_checkout'] or ''
    } for d in rows])


@app.route('/api/export')
def export_csv_route():
    """Esporta stato attuale dispositivi in CSV."""
    conn = get_db()
    rows = conn.execute(
        'SELECT * FROM devices ORDER BY prefisso, numero'
    ).fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'codice_dispositivo', 'stato', 'esercente',
        'data_checkin', 'data_checkout'
    ])
    for d in rows:
        writer.writerow([
            d['codice_completo'], d['stato'],
            d['esercente'] or '',
            d['data_checkin'] or '',
            d['data_checkout'] or ''
        ])

    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': f'attachment; filename=palmari_export_{ts}.csv'
        }
    )


@app.route('/api/reset', methods=['POST'])
def reset_evento():
    """Resetta tutti i dispositivi a DISPONIBILE e cancella i log."""
    backup_db()
    conn = get_db()
    conn.execute(
        "UPDATE devices SET stato='DISPONIBILE', esercente=NULL, "
        "data_checkin=NULL, data_checkout=NULL"
    )
    conn.execute("DELETE FROM logs")
    conn.commit()
    conn.close()
    return jsonify({
        'ok': True,
        'messaggio': 'Evento resettato. Backup creato automaticamente.'
    })


@app.route('/api/settings', methods=['GET', 'POST'])
def settings_route():
    """Legge o aggiorna le impostazioni."""
    conn = get_db()

    if request.method == 'POST':
        data = request.json
        for key, value in data.items():
            conn.execute(
                'INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)',
                (key, str(value))
            )
        conn.commit()
        conn.close()
        return jsonify({'ok': True})

    rows = conn.execute('SELECT key, value FROM settings').fetchall()
    conn.close()
    return jsonify({r['key']: r['value'] for r in rows})


@app.route('/api/logs')
def logs_route():
    """Ultimi log operazioni."""
    conn = get_db()
    limit = request.args.get('limit', 50, type=int)
    rows = conn.execute(
        'SELECT codice_completo, operazione, esercente, timestamp '
        'FROM logs ORDER BY id DESC LIMIT ?',
        (limit,)
    ).fetchall()
    conn.close()
    return jsonify([{
        'codice': r['codice_completo'],
        'operazione': r['operazione'],
        'esercente': r['esercente'] or '',
        'timestamp': r['timestamp']
    } for r in rows])


# --- AVVIO ---

if __name__ == '__main__':
    init_db()
    backup_db()

    port = int(os.environ.get('PORT', 5000))

    def open_browser():
        webbrowser.open(f'http://127.0.0.1:{port}')

    print()
    print('=' * 52)
    print('   PALMARI MANAGER - Meccanismi (R)')
    print(f'   Server avviato su http://127.0.0.1:{port}')
    print('   Apri il browser per iniziare')
    print('   Premi Ctrl+C per chiudere')
    print('=' * 52)
    print()

    # Apri browser automaticamente
    threading.Timer(1.5, open_browser).start()

    app.run(host='127.0.0.1', port=port, debug=False)
