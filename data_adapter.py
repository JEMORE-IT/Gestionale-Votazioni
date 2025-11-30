import pandas as pd 
import os 
from voter_model import Voter, SimpleVoter, ProxyVoter
from delegation_service import DelegationManager

class ExcelAdapter:
    def __init__(self, file_path: str, delegation_file_path: str):
        self.file_path = file_path
        self.delegation_manager = DelegationManager(delegation_file_path)
    
    def get_votes(self) -> list[Voter]:
        #Controllo se il file esiste
        if not os.path.exists(self.file_path):
            print(f"Attenzione: il file {self.file_path} non esiste")
            return []
        
        try:
            #Leggo il file
            df = pd.read_excel(self.file_path)

            # Converto le righe in oggetti Voter
            votes = []
            for index, row in df.iterrows():
                name = str(row['Nome'])
                choice = str(row['Scelta'])
                
                # Crea il votante base
                principal = SimpleVoter(name=name, choice=choice)
                
                # Controlla deleghe
                delegators = self.delegation_manager.get_delegations_for(name)
                
                if delegators:
                    # Crea oggetti Voter per i deleganti (la loro scelta è irrilevante qui, conta il peso)
                    proxies = [SimpleVoter(name=d, choice="DELEGATED") for d in delegators]
                    # Crea un ProxyVoter che avvolge il principale
                    vote = ProxyVoter(principal=principal, proxies=proxies)
                else:
                    vote = principal
                    
                votes.append(vote)
            return votes
        
        except Exception as e:
            print(f"Errore durante la lettura del file: {e}")
            return [] 

        
            