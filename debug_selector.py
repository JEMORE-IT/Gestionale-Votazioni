import os
from app.infrastructure import config
from app.application.file_selector import FileSelector

def test_selector():
    path = os.path.join(config.MOCK_SHAREPOINT_DIR, "sites/board9")
    print(f"Testing path: {path}")
    
    if not os.path.exists(path):
        print("Path does not exist!")
        return

    print(f"Contents: {os.listdir(path)}")
    
    selector = FileSelector(path)
    files = selector.list_files()
    print(f"Selector found: {files}")

if __name__ == "__main__":
    test_selector()
