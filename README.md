# Gestionale Votazioni

Applicazione Python per l'automazione del conteggio delle votazioni, sviluppata con un approccio incrementale.

## Stato Attuale: Iterazione 2 (Motore delle Deleghe) ⚖️
Il sistema implementa il calcolo pesato dei voti basato sulle deleghe.

### Funzionalità
- **Lettura Dati**: Importa voti da `votazioni.xlsx` e deleghe da `deleghe.xlsx`.
- **Conteggio Pesato**: Calcola i voti applicando la formula $Voto = 1 + N_{deleghe}$.
- **Vincoli**: Applica il limite massimo di 3 deleghe per votante ($N \le 3$).
- **Controllo Integrità**: Verifica se voti vengono persi a causa del limite deleghe e avvisa l'utente.
- **Real-time**: Monitora il file `votazioni.xlsx` per aggiornamenti immediati.

## Installazione

1.  **Prerequisiti**:
    - Python 3.x
    - Pipx (consigliato)

2.  **Dipendenze**:
    ```bash
    sudo apt install python3-pandas python3-openpyxl python3-watchdog -y
    ```

## Utilizzo

1.  **File Votazioni (`votazioni.xlsx`)**:
    Colonne: `Nome`, `Scelta` (Approvo, Contro, Astenuto).

2.  **File Deleghe (`deleghe.xlsx`)**:
    Colonne: `Delegante`, `Delegato`.
    *Nota: Se un delegato accumula più di 3 deleghe, quelle in eccesso non vengono contate.*

3.  **Avvio**:
    ```bash
    python3 main.py
    ```

4.  **Live Update**:
    Modifica `votazioni.xlsx` per vedere i risultati aggiornarsi in tempo reale.

## Struttura del Progetto
- `main.py`: Entry point e configurazione.
- `data_adapter.py`: Gestione lettura Excel (`ExcelAdapter`).
- `vote_manager.py`: Logica di business, calcolo pesato e integrity check.
- `delegation_service.py`: Gestione caricamento deleghe (`DelegationManager`).
- `voter_model.py`: Modelli di dominio (`Voter`, `SimpleVoter`, `ProxyVoter`) e regole (`MaxThreeProxiesSpec`).
- `observer.py`: Gestione eventi file system.