from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
import os
from app.infrastructure import config
from datetime import datetime, timedelta, timezone

class SharePointClient:
    def __init__(self):
        self.site_url = config.SHAREPOINT_SITE_URL
        self.client_id = config.SHAREPOINT_CLIENT_ID
        self.client_secret = config.SHAREPOINT_CLIENT_SECRET
        self.ctx = None

    def connect(self):
        if not self.client_id or not self.client_secret:
            raise ValueError("Credenziali SharePoint mancanti in config.py o variabili d'ambiente.")
        
        try:
            # Use MSAL to acquire token
            import msal
            from urllib.parse import urlparse
            
            # Determine authority (Tenant specific)
            # If we have a tenant ID in env, use it. Otherwise try to infer from domain or use common (which failed before)
            # Based on previous tests, we need 'jemore.onmicrosoft.com'
            tenant = os.getenv("SHAREPOINT_TENANT_ID", "jemore.onmicrosoft.com")
            authority_url = f"https://login.microsoftonline.com/{tenant}"
            
            app = msal.ConfidentialClientApplication(
                self.client_id,
                authority=authority_url,
                client_credential=self.client_secret
            )
            
            # Determine scope (Root site)
            parsed = urlparse(self.site_url)
            root_url = f"{parsed.scheme}://{parsed.netloc}"
            scopes = [f"{root_url}/.default"]
            
            result = app.acquire_token_for_client(scopes=scopes)
            
            if "access_token" not in result:
                raise Exception(f"Failed to acquire token: {result.get('error_description')}")
            
            token = result['access_token']
            
            # Connect with token
            # The library expects an object with accessToken and tokenType properties
            class TokenWrapper:
                def __init__(self, token):
                    self.accessToken = token
                    self.tokenType = "Bearer"
                    self.token_type = "Bearer" # Add snake_case just in case
            
            self.ctx = ClientContext(self.site_url).with_access_token(lambda: TokenWrapper(token))
            # Fix for TypeError: can't compare offset-naive and offset-aware datetimes
            # Force expiration to be timezone-aware UTC
            self.ctx.authentication_context._token_expires = datetime.now(timezone.utc) + timedelta(hours=1)
            
            # Add User-Agent to avoid some blocks
            self.ctx.pending_request().beforeExecute += lambda request: request.headers.update({'User-Agent': 'Python/3.13'})
            
            web = self.ctx.web
            self.ctx.load(web)
            self.ctx.execute_query()
            print(f"✅ Connesso a SharePoint: {web.properties['Title']}")
            
        except Exception as e:
            print(f"❌ Errore connessione SharePoint (App-Only): {e}")
            print("⚠️  Tentativo con Device Login (Interattivo)...")
            self.connect_with_device_flow()

    def connect_with_device_flow(self):
        """Authenticates using Device Code Flow (Interactive)."""
        import msal
        import sys
        
        # Public Client (no secret needed for device flow usually, but we use the same app id)
        # Note: Ensure "Allow public client flows" is YES in Azure AD -> Authentication
        # Use specific tenant domain to avoid AADSTS50059
        tenant = os.getenv("SHAREPOINT_TENANT_ID", "jemore.onmicrosoft.com")
        authority_url = f"https://login.microsoftonline.com/{tenant}"
        
        app = msal.PublicClientApplication(
            self.client_id,
            authority=authority_url
        )
        
        # Better: use the specific resource scope
        from urllib.parse import urlparse
        parsed = urlparse(self.site_url)
        root_url = f"{parsed.scheme}://{parsed.netloc}"
        scopes = [f"{root_url}/.default"]

        flow = app.initiate_device_flow(scopes=scopes)
        if "user_code" not in flow:
            raise ValueError(f"Impossibile avviare Device Flow: {flow.get('error_description')}")
        
        print(f"\n🚨 AZIONE RICHIESTA: Vai su {flow['verification_uri']} e inserisci il codice: {flow['user_code']}")
        print("In attesa di login...")
        sys.stdout.flush()
        
        result = app.acquire_token_by_device_flow(flow)
        
        if "access_token" in result:
            token = result['access_token']
            print("✅ Login effettuato!")
            
            class TokenWrapper:
                def __init__(self, token):
                    self.accessToken = token
                    self.tokenType = "Bearer"
            
            self.ctx = ClientContext(self.site_url).with_access_token(lambda: TokenWrapper(token))
            # Fix for TypeError: can't compare offset-naive and offset-aware datetimes
            self.ctx.authentication_context._token_expires = datetime.now(timezone.utc) + timedelta(hours=1)
            web = self.ctx.web
            self.ctx.load(web)
            self.ctx.execute_query()
            print(f"✅ Connesso a SharePoint come Utente: {web.properties['Title']}")
        else:
            raise Exception(f"Login fallito: {result.get('error_description')}")

    def list_files(self, relative_folder_url: str = "Shared Documents"):
        """Lists .xlsx files in the specified relative folder URL."""
        if not self.ctx:
            self.connect()

        try:
            # Ottieni la cartella relativa al server
            # Se relative_folder_url è "Shared Documents", la libreria cercherà in /sites/board9/Shared Documents
            folder = self.ctx.web.get_folder_by_server_relative_url(relative_folder_url)
            files = folder.files
            self.ctx.load(files)
            self.ctx.execute_query()

            xlsx_files = []
            for file in files:
                if file.name.endswith('.xlsx') and not file.name.startswith('~$'):
                    xlsx_files.append({
                        'name': file.name,
                        'serverRelativeUrl': file.serverRelativeUrl,
                        'timeLastModified': file.time_last_modified
                    })
            
            # Sort by modification date (newest to oldest)
            xlsx_files.sort(key=lambda x: x['timeLastModified'], reverse=True)
            return xlsx_files

        except Exception as e:
            import traceback
            print(f"Errore listing files da SharePoint: {e}")
            traceback.print_exc()
            return []

    def download_file(self, server_relative_url: str, local_path: str):
        if not self.ctx:
            self.connect()
        
        try:
            with open(local_path, "wb") as local_file:
                file = self.ctx.web.get_file_by_server_relative_url(server_relative_url)
                file.download(local_file)
                self.ctx.execute_query()
            print(f"Scaricato: {local_path}")
        except Exception as e:
            print(f"Errore download file: {e}")
            raise
