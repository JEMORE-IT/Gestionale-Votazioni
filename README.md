# Gestionale Votazioni

Applicazione Python per l'automazione del conteggio delle votazioni, sviluppata con un approccio incrementale.

## Stato Attuale: Iterazione 3 (Selettore di Votazioni) 📂
Il sistema permette di navigare tra diverse votazioni presenti in una cartella specifica.

### Funzionalità
- **Navigazione**: Lista interattiva dei file Excel presenti nella cartella `mock_sharepoint`.
- **Ordinamento**: I file sono ordinati per "Ultima modifica" per trovare subito la votazione corrente.
- **Sessioni**: Caricamento dinamico della votazione scelta senza riavviare l'app.
- **Motore Deleghe**: Supporto completo al calcolo pesato e vincoli (Iterazione 2).
- **Real-time**: Monitoraggio attivo del file selezionato.

## Installazione

1.  **Prerequisiti**:
    - Python 3.x
    - Pipx (consigliato)

2.  **Dipendenze**:
    ```bash
    sudo apt install python3-pandas python3-openpyxl python3-watchdog -y
    ```

## Utilizzo

1.  **Preparazione**:
    - I file di votazione vanno in `mock_sharepoint/sites/board9`.
    - Il file `deleghe.xlsx` va nella root.

2.  **Avvio**:
    ```bash
    python3 main.py
    ```

3.  **Flusso**:
    - Seleziona il file dalla lista numerata.
    - L'app mostrerà i risultati in tempo reale.
    - Premi `Ctrl+C` per tornare al menu e scegliere un altro file.

## Struttura del Progetto
- `main.py`: Entry point e loop di navigazione.
- `file_selector.py`: Gestione lista e ordinamento file.
- `session_factory.py`: Factory per creare sessioni di voto.
- `voting_session.py`: Gestione del ciclo di vita di una sessione.
- `vote_manager.py`: Logica di business (Core).
- `delegation_service.py`: Gestione deleghe.
- `voter_model.py`: Modelli di dominio.
- `observer.py`: Monitoraggio file system.