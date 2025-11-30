from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from typing import Optional
from app.application.file_selector import FileSelector
from app.application.session_factory import VotingSessionFactory
from app.infrastructure.sharepoint_client import SharePointClient
from app.infrastructure import config
import threading
import time

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Global State
class AppState:
    def __init__(self):
        self.selector = None
        self.factory = None
        self.current_session = None
        self.current_file = None
        self.delegation_path = config.DELEGHE_FILE_PATH
        self.sharepoint_path = os.path.join(config.MOCK_SHAREPOINT_DIR, "sites/board9")

state = AppState()

def init_app_state():
    """Initialize SharePoint and FileSelector"""
    sp_client = None
    try:
        sp_client = SharePointClient()
        sp_client.connect(interactive=False)
        print(f"☁️  Modalità SharePoint Attiva: {config.SHAREPOINT_SITE_URL}")
        source = sp_client
    except Exception as e:
        print(f"⚠️  Impossibile connettersi a SharePoint: {e}")
        print(f"📂 Fallback su cartella locale: {state.sharepoint_path}")
        source = state.sharepoint_path
        sp_client = None

    state.selector = FileSelector(source)
    state.factory = VotingSessionFactory(state.delegation_path, sp_client)

@app.on_event("startup")
async def startup_event():
    init_app_state()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/files")
async def get_files():
    if not state.selector:
        return []
    files = state.selector.list_files()
    # Serialize for JSON
    return files

@app.post("/api/session")
async def start_session(file_data: dict):
    """Start a voting session with the selected file"""
    try:
        if state.current_file and state.current_file['name'] == file_data['name']:
             return {"status": "active", "message": "Session already active"}

        # Stop previous session if running
        if state.current_session and state.current_session.running:
            state.current_session.stop()

        state.current_file = file_data
        state.current_session = state.factory.create_session(file_data)
        
        # Start session in a separate DAEMON thread to not block API and allow shutdown
        thread = threading.Thread(target=state.current_session.start, daemon=True)
        thread.start()
        
        return {"status": "started", "file": file_data['name']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    """Get current voting stats"""
    if not state.current_session:
        return {"status": "idle"}
    
    if hasattr(state.current_session, 'vote_manager'):
        vm = state.current_session.vote_manager
        try:
            votes = vm.adapter.get_votes()
            from collections import defaultdict
            counts = defaultdict(int)
            total_votes = 0
            
            for vote in votes:
                weight = vote.get_weight()
                counts[vote.choice] += weight
                total_votes += weight
            
            return {
                "status": "active",
                "total": total_votes,
                "approvo": counts['Approvo'],
                "contro": counts['Contro'],
                "astenuto": counts['Astenuto'],
                "file": state.current_file['name'] if state.current_file else "Unknown"
            }
        except Exception as e:
            return {"status": "error", "detail": str(e)}
            
    return {"status": "active", "message": "No stats available"}

@app.post("/api/shutdown")
async def shutdown():
    """Shutdown the server"""
    import os, signal
    
    def kill():
        time.sleep(1)
        os.kill(os.getpid(), signal.SIGINT)
    
    threading.Thread(target=kill, daemon=True).start()
    return {"status": "shutting_down"}

# SharePoint Login State
login_state = {
    "status": "idle", # idle, waiting_for_user, success, error
    "user_code": None,
    "verification_uri": None,
    "message": None
}

@app.post("/api/login/sharepoint")
async def login_sharepoint():
    """Initiate SharePoint Device Login"""
    try:
        sp_client = SharePointClient()
        app_msal, flow = sp_client.initiate_device_flow()
        
        login_state["status"] = "waiting_for_user"
        login_state["user_code"] = flow["user_code"]
        login_state["verification_uri"] = flow["verification_uri"]
        login_state["message"] = flow.get("message")
        
        def wait_for_login():
            try:
                sp_client.finalize_device_flow(app_msal, flow)
                # Update global state
                state.selector = FileSelector(sp_client)
                state.factory = VotingSessionFactory(state.delegation_path, sp_client)
                login_state["status"] = "success"
            except Exception as e:
                login_state["status"] = "error"
                login_state["message"] = str(e)

        threading.Thread(target=wait_for_login, daemon=True).start()
        
        return {
            "status": "initiated",
            "user_code": flow["user_code"],
            "verification_uri": flow["verification_uri"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/login/status")
async def login_status():
    return login_state
