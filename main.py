import os
import sys
from app.application.file_selector import FileSelector
from app.application.session_factory import VotingSessionFactory
from app.infrastructure.sharepoint_client import SharePointClient
from app.infrastructure import config

# Configurazione
SHAREPOINT_PATH = os.path.join(config.MOCK_SHAREPOINT_DIR, "sites/board9")
DELEGATION_PATH = config.DELEGHE_FILE_PATH

def main():
    print(f"🚀 Avvio App Votazioni - Selector Mode")
    print(f"📂 File Deleghe: {DELEGATION_PATH}")

    # Initialize SharePoint Client
    sp_client = None
    try:
        sp_client = SharePointClient()
        # Try to connect to verify credentials
        # If credentials are empty, connect() raises ValueError
        sp_client.connect()
        print(f"☁️  Modalità SharePoint Attiva: {config.SHAREPOINT_SITE_URL}")
        source = sp_client
    except Exception as e:
        print(f"⚠️  Impossibile connettersi a SharePoint: {e}")
        print(f"📂 Fallback su cartella locale: {SHAREPOINT_PATH}")
        source = SHAREPOINT_PATH
        sp_client = None

    selector = FileSelector(source)
    factory = VotingSessionFactory(DELEGATION_PATH, sp_client)

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