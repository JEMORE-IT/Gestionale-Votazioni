from .voting_session import VotingSession
from app.infrastructure.sharepoint_client import SharePointClient

class VotingSessionFactory:
    def __init__(self, delegation_file_path: str, sp_client: SharePointClient = None):
        self.delegation_file_path = delegation_file_path
        self.sp_client = sp_client

    def create_session(self, file_info: dict) -> VotingSession:
        return VotingSession(file_info, self.delegation_file_path, self.sp_client)
