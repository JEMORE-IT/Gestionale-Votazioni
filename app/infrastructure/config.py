import os
from dotenv import load_dotenv

# Calculate Project Root
# app/infrastructure/config.py -> app/infrastructure -> app -> root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from .env file
load_dotenv(os.path.join(BASE_DIR, ".env"))

# SharePoint Configuration
SHAREPOINT_SITE_URL = os.getenv("SHAREPOINT_SITE_URL", "https://jemore.sharepoint.com/sites/board9")
SHAREPOINT_CLIENT_ID = os.getenv("SHAREPOINT_CLIENT_ID", "")
SHAREPOINT_CLIENT_SECRET = os.getenv("SHAREPOINT_CLIENT_SECRET", "")
SHAREPOINT_TENANT_ID = os.getenv("SHAREPOINT_TENANT_ID", "jemore.onmicrosoft.com")

# Local paths
DATA_DIR = os.path.join(BASE_DIR, "data")
DELEGHE_FILE_PATH = os.path.join(DATA_DIR, "deleghe.xlsx")
MOCK_SHAREPOINT_DIR = os.path.join(DATA_DIR, "mock_sharepoint")
TEMP_DOWNLOAD_DIR = os.path.join(BASE_DIR, "temp_downloads")
