import os
import sys
from file_selector import FileSelector
from session_factory import VotingSessionFactory

# Configurazione
MOCK_SHAREPOINT_DIR = "mock_sharepoint/sites/board9"
DELEGATION_FILE = "deleghe.xlsx"
CURRENT_DIR = os.getcwd()
SHAREPOINT_PATH = os.path.join(CURRENT_DIR, MOCK_SHAREPOINT_DIR)
DELEGATION_PATH = os.path.join(CURRENT_DIR, DELEGATION_FILE)

def main():
    print(f"🚀 Avvio App Votazioni - Selector Mode")
    print(f"📂 Cartella Votazioni: {SHAREPOINT_PATH}")
    print(f"📂 File Deleghe: {DELEGATION_PATH}")

    selector = FileSelector(SHAREPOINT_PATH)
    factory = VotingSessionFactory(DELEGATION_PATH)

    while True:
        selected_file = selector.select_file()
        
        if not selected_file:
            print("👋 Uscita...")
            break

        # Crea e avvia la sessione
        session = factory.create_session(selected_file)
        session.start()
        # Quando session.start() ritorna (dopo Ctrl+C), il loop continua e ripropone la lista

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Uscita forzata...")
        sys.exit(0)