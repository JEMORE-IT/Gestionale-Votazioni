from collections import Counter
from data_adapter import ExcelAdapter

class VoteManager:
    def __init__(self, file_path: str):
        self.adapter = ExcelAdapter(file_path)
        
    def calculate_results(self):
        print("--Elaborazione Voti--")
        votes = self.adapter.get_votes()
        
        #Conta le scelte
        counts = Counter([v.choice for v in votes])

        print(f"Totale voti: {len(votes)}")
        print(f"Approvati: {counts['Approvo']}")
        print(f"Contro: {counts['Contro']}")
        print(f"Astensioni: {counts['Astenuto']}")