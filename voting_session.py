from vote_manager import VoteManager
from observer import VoteObserver
import os
import time

class VotingSession:
    def __init__(self, file_path: str, delegation_file_path: str):
        self.file_path = file_path
        self.delegation_file_path = delegation_file_path
        self.manager = VoteManager(file_path, delegation_file_path)
        self.observer = None
        self.running = False

    def start(self):
        print(f"\n🚀 Avvio sessione per: {os.path.basename(self.file_path)}")
        
        # Primo calcolo
        self.manager.calculate_results()

        # Callback per modifiche
        def on_change():
            print("\n🔄 Rilevata modifica! Ricalcolo...")
            self.manager.calculate_results()

        # Setup observer
        directory = os.path.dirname(self.file_path)
        filename = os.path.basename(self.file_path)
        self.observer = VoteObserver(directory, filename, on_change)
        self.observer.start()
        self.running = True
        
        print("Premere Ctrl+C per tornare al menu (o attendere aggiornamenti)...")
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        if self.observer:
            print("\n🛑 Arresto monitoraggio...")
            self.observer.stop()
            self.observer = None
        self.running = False
