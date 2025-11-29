import os
import sys
from vote_manager import VoteManager 
from observer import VoteObserver

# Configurazione
EXCEL_FILE = "votazioni.xlsx"
CURRENT_DIR = os.getcwd()
EXCEL_PATH = os.path.join(CURRENT_DIR, EXCEL_FILE)

def main():
    print(f"🚀 Avvio App Votazioni...")
    print(f"📂 Monitoraggio file: {EXCEL_PATH}")

    # 1. Inizializza il Manager
    manager = VoteManager(EXCEL_PATH)
    
    # 2. Fai il primo calcolo (se il file esiste già)
    manager.calculate_results()

    # 3. Definisci cosa fare quando il file cambia
    def on_change():
        print("\n🔄 Rilevata modifica! Ricalcolo...")
        manager.calculate_results()

    # 4. Avvia la sentinella
    observer = VoteObserver(CURRENT_DIR, EXCEL_FILE, on_change)
    observer.start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Uscita...")
        sys.exit(0)