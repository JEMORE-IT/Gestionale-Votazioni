import os
import time
from typing import List, Optional, Union
from app.infrastructure.sharepoint_client import SharePointClient

class FileSelector:
    def __init__(self, source: Union[str, SharePointClient]):
        self.source = source
        self.is_remote = isinstance(source, SharePointClient)

    def list_files(self) -> List[dict]:
        """Returns a list of .xlsx files sorted by last modified (descending)."""
        if self.is_remote:
            # SharePoint
            # Assumiamo che la cartella target sia "Shared Documents" o configurabile
            # Per ora hardcodiamo o passiamo come parametro?
            # Usiamo "Shared Documents" come default
            return self.source.list_files("Shared Documents")
        else:
            # Local Directory
            if not os.path.exists(self.source):
                print(f"Directory non trovata: {self.source}")
                return []

            files = []
            for f in os.listdir(self.source):
                if f.endswith('.xlsx') and not f.startswith('~$'):
                    full_path = os.path.join(self.source, f)
                    files.append({
                        'name': f,
                        'path': full_path,
                        'timeLastModified': os.path.getmtime(full_path)
                    })
            
            # Sort by modification time (newest first)
            files.sort(key=lambda x: x['timeLastModified'], reverse=True)
            return files

    def select_file(self) -> Optional[dict]:
        """Interactive file selection."""
        files = self.list_files()
        
        if not files:
            print("Nessun file di votazione trovato.")
            return None

        print("\n--- Seleziona Votazione ---")
        for i, f in enumerate(files):
            # Format time
            # Note: SharePoint returns datetime object usually, local returns timestamp
            # We need to handle both or just print as is
            mod_time = f['timeLastModified']
            if isinstance(mod_time, (int, float)):
                time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mod_time))
            else:
                time_str = str(mod_time)

            print(f"{i + 1}. {f['name']} (Ultima modifica: {time_str})")
        
        print("0. Esci")

        while True:
            try:
                choice = input("\nInserisci il numero del file: ")
                if choice == '0':
                    return None
                
                idx = int(choice) - 1
                if 0 <= idx < len(files):
                    return files[idx]
                else:
                    print("Numero non valido.")
            except ValueError:
                print("Inserisci un numero valido.")
