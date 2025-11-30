import os
import sys
from app.application.file_selector import FileSelector
from app.application.session_factory import VotingSessionFactory
from app.infrastructure.sharepoint_client import SharePointClient
from app.infrastructure import config

# Configurazione
SHAREPOINT_PATH = os.path.join(config.MOCK_SHAREPOINT_DIR, "sites/board9")
DELEGATION_PATH = config.DELEGHE_FILE_PATH

import uvicorn
from app.interface.web import app

def main():
    print(f"🚀 Avvio App Votazioni - Web Mode")
    print(f"🌐 Interfaccia disponibile su: http://localhost:8000")
    
    # Run FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Uscita forzata...")
        sys.exit(0)