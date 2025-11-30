# Gestionale Votazioni JEMORE 🗳️

Applicazione Python per l'automazione del conteggio delle votazioni durante le Assemblee Generali, integrata con SharePoint Online e dotata di un sistema di gestione deleghe.

## 🌟 Funzionalità Principali

### 1. Gestione Voti e Deleghe
- **Conteggio Pesato**: Calcola automaticamente i voti (Favorevoli, Contrari, Astenuti) tenendo conto delle deleghe.
- **Sistema Deleghe**:
    - Supporta fino a **3 deleghe** per persona (come da statuto).
    - **Integrity Check**: Verifica che il numero totale di voti corrisponda alla somma di presenti + deleghe.
    - Segnala se un votante supera il limite di deleghe.

### 2. Integrazione SharePoint (Cloud)
- **Connessione Diretta**: Si collega al sito SharePoint `sites/board9` per leggere i file di votazione.
- **Autenticazione Sicura**: Utilizza il **Device Code Flow** (Login Interattivo Microsoft) per garantire l'accesso sicuro anche con MFA.
- **Download Automatico**: Scarica e processa i file `.xlsx` direttamente dal cloud.

### 3. Monitoraggio Real-Time
- **Observer Locale**: Se si modifica il file scaricato (o un file locale), il conteggio si aggiorna in tempo reale senza riavviare l'app.

---

## 📂 Struttura del Progetto

Il progetto segue un'architettura modulare divisa in layer:

```
Gestionale-Votazioni/
├── app/
│   ├── core/                  # Logica di Business (Modelli, Regole)
│   │   ├── voter_model.py     # Modelli Votante (Semplice, Proxy)
│   │   ├── vote_manager.py    # Motore di calcolo voti
│   │   └── delegation_service.py # Gestione file deleghe
│   ├── infrastructure/        # Adattatori Esterni
│   │   ├── sharepoint_client.py # Client API SharePoint
│   │   ├── data_adapter.py    # Lettura Excel (Pandas)
│   │   └── config.py          # Configurazione centralizzata
│   └── application/           # Logica Applicativa
│       ├── voting_session.py  # Gestione sessione di voto
│       ├── file_selector.py   # Menu selezione file
│       └── observer.py        # Monitoraggio file system
├── data/                      # Dati statici
│   ├── deleghe.xlsx           # File mappatura deleghe
│   └── mock_sharepoint/       # Cartella per test offline
├── main.py                    # Punto di ingresso
└── requirements.txt           # Dipendenze
```

---

## 🚀 Installazione

1.  **Prerequisiti**: Python 3.10+
2.  **Installazione Dipendenze**:
    ```bash
    pip install -r requirements.txt
    # Oppure manualmente:
    # pip install pandas openpyxl watchdog msal Office365-REST-Python-Client python-dotenv
    ```

## ⚙️ Configurazione

Crea un file `.env` nella root del progetto con le seguenti variabili:

```env
SHAREPOINT_SITE_URL=https://jemore.sharepoint.com/sites/board9
SHAREPOINT_CLIENT_ID=<IL_TUO_CLIENT_ID_AZURE>
SHAREPOINT_TENANT_ID=jemore.onmicrosoft.com
```
*Nota: Il `CLIENT_SECRET` non è necessario per il Device Flow.*

---

## 📖 Guida all'Uso

### 1. Avvio
Esegui il comando:
```bash
python3 main.py
```

### 2. Login (Primo Accesso)
Se richiesto, l'app mostrerà un codice e un link:
> 🚨 AZIONE RICHIESTA: Vai su https://microsoft.com/devicelogin e inserisci il codice: XXXXXXXX

1.  Apri il link nel browser.
2.  Inserisci il codice mostrato nel terminale.
3.  Fai login con il tuo account Microsoft (JEMORE).
4.  Torna al terminale: vedrai `✅ Login effettuato!`.

### 3. Selezione Votazione
L'app mostrerà l'elenco dei file `.xlsx` trovati su SharePoint:
```text
--- Seleziona Votazione ---
1. Approvazione Bilancio.xlsx
2. Modifica Statuto.xlsx
...
```
Inserisci il numero corrispondente al file da analizzare.

### 4. Risultati
L'app scaricherà il file e mostrerà il conteggio:
```text
--Elaborazione Voti (Pesata)--
Totale voti (pesati): 45
Approvati: 40
Contro: 2
Astensioni: 3
✅ VERIFICA OK: Il numero di voti corrisponde alle deleghe assegnate.
```

---

## 🧪 Esempi di Testing

### Test 1: Verifica Deleghe
1.  Apri il file `data/deleghe.xlsx`.
2.  Assegna a "Mario Rossi" 4 deleganti (es. Luca, Paolo, Anna, Marco).
3.  Avvia l'app e seleziona una votazione.
4.  **Risultato Atteso**: L'app mostrerà un avviso di integrità o limiterà il peso a 4 (1 + 3 deleghe max).

### Test 2: Modifica Real-Time
1.  Avvia una sessione su un file.
2.  Mentre l'app è in esecuzione ("Premere Ctrl+C per tornare al menu"), apri il file Excel scaricato (in `temp_downloads/`).
3.  Cambia il voto di una persona da "Approvo" a "Contro" e salva.
4.  **Risultato Atteso**: Il terminale mostrerà `🔄 Rilevata modifica locale! Ricalcolo...` e aggiornerà i numeri immediatamente.

### Test 3: Fallback Offline
1.  Disconnetti internet o rinomina `.env` in `.env.bak`.
2.  Avvia `python3 main.py`.
3.  **Risultato Atteso**: L'app dirà `⚠️ Impossibile connettersi a SharePoint` e userà la cartella locale `data/mock_sharepoint`.