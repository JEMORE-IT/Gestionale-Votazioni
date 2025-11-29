# Gestionale Votazioni

Applicazione Python per l'automazione del conteggio delle votazioni, sviluppata con un approccio incrementale.

## Stato Attuale: Iterazione 1 (Walking Skeleton) 💀
Il sistema è attualmente in fase di "Scheletro Funzionante". È in grado di leggere voti da un file Excel locale e mostrare i risultati in tempo reale.

### Funzionalità
- **Lettura Dati**: Importa voti da un file Excel (`votazioni.xlsx`).
- **Conteggio**: Calcola automaticamente Favorevoli, Contrari e Astenuti.
- **Real-time**: Monitora il file Excel e aggiorna la dashboard appena vengono salvate modifiche (Pattern Observer).
- **Interfaccia**: Dashboard testuale su console.

## Installazione

1.  **Prerequisiti**:
    - Python 3.x
    - Pipx (consigliato per i tool di sviluppo)

2.  **Dipendenze**:
    ```bash
    # Installazione librerie necessarie
    sudo apt install python3-pandas python3-openpyxl python3-watchdog -y
    
    # (Opzionale) Tool di sviluppo
    sudo apt install pipx -y
    pipx install black isort
    ```

## Utilizzo

1.  **Preparazione Dati**:
    Crea un file `votazioni.xlsx` nella root del progetto con le colonne:
    - `Nome` (es. `Mario Rossi`)
    - `Scelta` (Valori ammessi: `Favorevole`, `Contrario`, `Astenuto`)

2.  **Avvio**:
    ```bash
    python3 main.py
    ```

3.  **Live Update**:
    Lascia l'app aperta e modifica il file Excel. Al salvataggio, i conteggi si aggiorneranno automaticamente.

## Struttura del Progetto
- `main.py`: Entry point e configurazione.
- `data_adapter.py`: Gestione lettura Excel (`ExcelAdapter`).
- `vote_manager.py`: Logica di business e conteggio (`VoteManager`).
- `observer.py`: Gestione eventi file system (`VoteObserver`).