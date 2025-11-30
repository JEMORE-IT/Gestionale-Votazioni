from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential
import os
from dotenv import load_dotenv
import sys

# Load env
load_dotenv()

site_url = os.getenv("SHAREPOINT_SITE_URL")
client_id = os.getenv("SHAREPOINT_CLIENT_ID")
client_secret = os.getenv("SHAREPOINT_CLIENT_SECRET")

print(f"Testing connection to: {site_url}")
print(f"Client ID: {client_id[:5]}..." if client_id else "Client ID: MISSING")
print(f"Client Secret: {'*' * 5}" if client_secret else "Client Secret: MISSING")

if not all([site_url, client_id, client_secret]):
    print("❌ Missing configuration in .env")
    sys.exit(1)

try:
    # Use MSAL to get token directly for inspection
    import msal
    print("🔄 Acquiring Access Token via MSAL...")
    # Use specific tenant domain instead of 'common'
    authority_url = f"https://login.microsoftonline.com/jemore.onmicrosoft.com"
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=authority_url,
        client_credential=client_secret
    )
    # Scope for SharePoint
    # The resource identifier is usually the root site URL, not the specific site collection URL
    # Extract root url from site_url
    from urllib.parse import urlparse
    parsed = urlparse(site_url)
    root_url = f"{parsed.scheme}://{parsed.netloc}"
    
    result = app.acquire_token_for_client(scopes=[f"{root_url}/.default"])
    
    if "access_token" in result:
        token = result['access_token']
        print("✅ Token acquired.")
        # Decode token (no verification, just debug)
        import json
        import base64
        try:
            # JWT parts: header.payload.signature
            payload_part = token.split('.')[1]
            # Add padding if needed
            payload_part += '=' * (-len(payload_part) % 4)
            decoded = base64.b64decode(payload_part)
            claims = json.loads(decoded)
            
            print("\n🧐 TOKEN INSPECTION:")
            print(f"Audience (aud): {claims.get('aud')}")
            print(f"Roles (permissions): {claims.get('roles', 'NONE')}")
            print(f"Issuer (iss): {claims.get('iss')}")
            
            if 'Sites.FullControl.All' not in claims.get('roles', []) and 'Sites.Read.All' not in claims.get('roles', []):
                 print("\n⚠️  WARNING: 'Sites.FullControl.All' (or Read) is MISSING from the token roles!")
                 print("   This confirms the Azure AD permissions are NOT correctly configured/granted.")
        except Exception as e:
            print(f"⚠️ Could not decode token: {e}")
    else:
        print(f"❌ Failed to acquire token: {result.get('error_description')}")

    # Proceed with ClientContext (it will re-acquire token internally but that's fine)
    ctx = ClientContext(site_url).with_credentials(ClientCredential(client_id, client_secret))

    web = ctx.web
    ctx.load(web)
    ctx.execute_query()
    print(f"✅ SUCCESS! Connected to site: {web.properties.get('Title')}")
except Exception as e:
    print("\n❌ CONNECTION FAILED")
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Details: {e}")
    
    if "401" in str(e):
        print("\n💡 SUGGESTION FOR 401 UNAUTHORIZED:")
        print("1. Go to Azure Portal > App Registrations > [Your App] > API Permissions")
        print("2. Ensure you have 'Sites.FullControl.All' (or Read.All) under **APPLICATION** permissions (not Delegated).")
        print("3. **CRITICAL**: Click 'Grant admin consent' button.")
