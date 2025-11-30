from collections import Counter, defaultdict
from data_adapter import ExcelAdapter

class VoteManager:
    def __init__(self, file_path: str, delegation_file_path: str):
        self.adapter = ExcelAdapter(file_path, delegation_file_path)
        
    def calculate_results(self):
        print("--Elaborazione Voti (Pesata)--")
        votes = self.adapter.get_votes()
        
        # Conta i voti pesati
        counts = defaultdict(int)
        total_votes = 0
        
        for vote in votes:
            weight = vote.get_weight()
            counts[vote.choice] += weight
            total_votes += weight
            
            # Debug info per vedere chi ha deleghe
            if weight > 1:
                print(f"  > {vote.name} ha peso {weight} (Deleghe)")

        print(f"Totale voti (pesati): {total_votes}")
        print(f"Approvati: {counts['Approvo']}")
        print(f"Contro: {counts['Contro']}")
        print(f"Astensioni: {counts['Astenuto']}")

        # Integrity Check
        total_voters = len(votes)
        total_proxies = sum(v.get_proxy_count() for v in votes)
        expected_votes = total_voters + total_proxies
        
        print("-" * 30)
        print(f"Verifica Integrità: Votanti ({total_voters}) + Deleghe ({total_proxies}) = {expected_votes}")
        
        if expected_votes == total_votes:
            print("✅ VERIFICA OK: Il numero di voti corrisponde alle deleghe assegnate.")
        else:
            diff = expected_votes - total_votes
            print(f"⚠️ ATTENZIONE: Mancano {diff} voti nel conteggio finale!")
            print("   Possibile causa: Alcuni votanti hanno superato il limite di 3 deleghe.")