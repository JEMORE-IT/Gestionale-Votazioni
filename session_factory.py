from voting_session import VotingSession

class VotingSessionFactory:
    def __init__(self, delegation_file_path: str):
        self.delegation_file_path = delegation_file_path

    def create_session(self, file_path: str) -> VotingSession:
        return VotingSession(file_path, self.delegation_file_path)
