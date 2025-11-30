import pandas as pd
import os
from typing import List, Dict

class DelegationManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._delegations: Dict[str, List[str]] = {}
        self.load_delegations()

    def load_delegations(self):
        if not os.path.exists(self.file_path):
            print(f"Attenzione: file deleghe {self.file_path} non trovato. Nessuna delega caricata.")
            return

        try:
            df = pd.read_excel(self.file_path)
            # Raggruppa per Delegato e crea liste di Deleganti
            # Assumiamo colonne 'Delegante' e 'Delegato'
            grouped = df.groupby('Delegato')['Delegante'].apply(list).to_dict()
            self._delegations = grouped
            print(f"Deleghe caricate da {self.file_path}")
        except Exception as e:
            print(f"Errore caricamento deleghe: {e}")
            self._delegations = {}

    def get_delegations_for(self, delegate_name: str) -> List[str]:
        """Restituisce la lista dei nomi delle persone che hanno delegato il votante."""
        return self._delegations.get(delegate_name, [])
