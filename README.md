# Gestionale Votazioni

Applicazione Python per l'automazione del conteggio delle votazioni, sviluppata con un approccio incrementale.

## Stato Attuale: Iterazione 4 (Integrazione SharePoint) ☁️
Il sistema è integrato con SharePoint Online per recuperare le votazioni dal cloud.

### Funzionalità
- **Cloud Sync**: Connessione a SharePoint (`sites/board9`) per listare e scaricare votazioni.
- **Fallback**: Se la connessione fallisce (es. credenziali mancanti), usa automaticamente la cartella locale `mock_sharepoint`.
- **Navigazione**: Interfaccia unificata per scegliere file locali o remoti.
- **Motore Deleghe**: Calcolo pesato e vincoli sempre attivi.

## Installazione

1.  **Prerequisiti**:
    - Python 3.x
    - Pipx (consigliato)

2.  **Dipendenze**:
    ```bash
    sudo apt install python3-pandas python3-openpyxl python3-watchdog -y
    pip install Office365-REST-Python-Client --break-system-packages
    ```

## Configurazione SharePoint
Per abilitare l'accesso al cloud, imposta le variabili d'ambiente o modifica `config.py`:
- `SHAREPOINT_CLIENT_ID`
- `SHAREPOINT_CLIENT_SECRET`

## Utilizzo

1.  **Avvio**:
    ```bash
    python3 main.py
    ```

2.  **Flusso**:
    - L'app tenterà di connettersi a SharePoint.
    - Se riuscito, vedrai i file remoti. Altrimenti, vedrai i file locali.
    - Seleziona una votazione per iniziare.

## Struttura del Progetto
- `main.py`: Entry point.
- `sharepoint_client.py`: Adattatore per API SharePoint.
- `config.py`: Configurazione credenziali.
- `file_selector.py`: Gestione lista file (Locale/Remoto).
- `voting_session.py`: Gestione sessione (Download/Monitoraggio).
- `vote_manager.py`: Core logic.