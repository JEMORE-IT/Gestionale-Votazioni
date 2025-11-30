# 🗳️ Sistema Gestione Votazioni

Applicazione web per la gestione automatizzata delle votazioni, integrata con SharePoint e Excel.

## 🚀 Funzionalità

-   **Interfaccia Web Moderna**: Dashboard intuitiva con aggiornamenti in tempo reale (WebSocket/Polling).
-   **Integrazione SharePoint**:
    -   Elenco automatico dei file di votazione (`.xlsx`) da una cartella remota.
    -   Ordinamento per data (più recenti in alto).
    -   **Login Interattivo**: Supporto per autenticazione Microsoft Device Flow direttamente dall'interfaccia.
    -   **Fallback Locale**: Se SharePoint non è raggiungibile, utilizza una cartella locale.
-   **Calcolo Voti**:
    -   Conteggio voti pesati (Favorevole, Contrario, Astenuto).
    -   Gestione deleghe (max 3 per votante).
    -   Verifica integrità dei dati.

## 🛠️ Requisiti

-   Python 3.10+
-   Account Microsoft (per accesso SharePoint)

## 📦 Installazione

1.  Clona il repository:
    ```bash
    git clone https://github.com/AngeLorenzo04/Gestionale-Votazioni.git
    cd Gestionale-Votazioni
    ```

2.  Installa le dipendenze:
    ```bash
    pip install -r requirements.txt
    ```

3.  Configura le variabili d'ambiente (opzionale, crea un file `.env`):
    ```env
    SHAREPOINT_SITE_URL=https://tuo-tenant.sharepoint.com/sites/tuo-sito
    SHAREPOINT_CLIENT_ID=tuo-client-id
    SHAREPOINT_CLIENT_SECRET=tuo-client-secret
    SHAREPOINT_TENANT_ID=tuo-tenant-id
    ```

## ▶️ Utilizzo

Avvia l'applicazione:

```bash
python3 main.py
```

Apri il browser all'indirizzo: **http://localhost:8000**

### Flusso di Lavoro
1.  **Seleziona File**: Scegli il file di votazione dalla lista.
2.  **Login (se necessario)**: Se i file SharePoint non appaiono, clicca su "🔑 Login SharePoint" e segui le istruzioni a schermo.
3.  **Monitoraggio**: La dashboard mostrerà i risultati in tempo reale. Ogni modifica al file Excel (locale o remoto) aggiornerà i grafici.
4.  **Termina**: Usa il pulsante "🛑 Spegni Server" per chiudere l'applicazione.

## 📂 Struttura del Progetto

```
app/
├── application/       # Logica applicativa (Sessioni, Selettori)
├── core/             # Logica di dominio (Gestione Voti, Entità)
├── infrastructure/   # Adattatori esterni (SharePoint, Excel, Config)
├── interface/        # Interfaccia Web (FastAPI)
├── static/           # Assets (CSS, JS)
└── templates/        # Template HTML
data/                 # Dati locali (Deleghe, Mock SharePoint)
main.py               # Entry point
```

## 👨‍💻 Sviluppo

Il progetto segue i principi della Clean Architecture per garantire manutenibilità e scalabilità.
-   **Backend**: FastAPI, Office365-REST-Python-Client
-   **Frontend**: HTML5, CSS3 (Glassmorphism), Vanilla JS