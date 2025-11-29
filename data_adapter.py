import pandas as pd 
import dataclasses as dc 
import os 


@dc.dataclass
class Vote:
    name: str
    choice: str

class ExcelAdapter:
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def get_votes(self) -> list[Vote]:
        #Controllo se il file esiste
        if not os.path.exists(self.file_path):
            print(f"Attenzione: il file {self.file_path} non esiste")
            return []
        
        try:
            #Leggo il file
            df = pd.read_excel(self.file_path)

            # Converto le righe in oggetti Vote
            # Nota: Uso 'Scelta' come nome colonna, assicurati che l'Excel sia uguale!
            votes = []
            for index, row in df.iterrows():
                votes.append(Vote(name=str(row['Nome']), choice=str(row['Scelta'])))
            return votes
        
        except Exception as e:
            print(f"Errore durante la lettura del file: {e}")
            return [] 

        
            