import os
import time
from typing import List, Optional

class FileSelector:
    def __init__(self, directory: str):
        self.directory = directory

    def list_files(self) -> List[str]:
        """Returns a list of .xlsx files sorted by last modified (descending)."""
        if not os.path.exists(self.directory):
            print(f"Directory non trovata: {self.directory}")
            return []

        files = [f for f in os.listdir(self.directory) if f.endswith('.xlsx') and not f.startswith('~$')]
        
        # Sort by modification time (newest first)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(self.directory, x)), reverse=True)
        return files

    def select_file(self) -> Optional[str]:
        """Interactive file selection."""
        files = self.list_files()
        
        if not files:
            print("Nessun file di votazione trovato.")
            return None

        print("\n--- Seleziona Votazione ---")
        for i, f in enumerate(files):
            mod_time = os.path.getmtime(os.path.join(self.directory, f))
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mod_time))
            print(f"{i + 1}. {f} (Ultima modifica: {time_str})")
        
        print("0. Esci")

        while True:
            try:
                choice = input("\nInserisci il numero del file: ")
                if choice == '0':
                    return None
                
                idx = int(choice) - 1
                if 0 <= idx < len(files):
                    return os.path.join(self.directory, files[idx])
                else:
                    print("Numero non valido.")
            except ValueError:
                print("Inserisci un numero valido.")
