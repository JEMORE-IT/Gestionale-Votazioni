import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, filename, callback):
        self.filename = filename
        self.callback = callback
        self.last_modified = 0
    
    def on_modified(self, event):
        #Controlliamo che non sia una cartella e che sia il file giusto
        if not event.is_directory and event.src_path.endswith(self.filename):
            # Debounce: evitiamo doppi eventi ravvicinati
            current_time = time.time()
            if current_time - self.last_modified > 1:
                self.last_modified = current_time
                self.callback()
    
class VoteObserver:
    def __init__(self, path, filename, callback):
        self.path = path
        self.filename = filename
        self.callback = callback
        self.observer = Observer()
    
    def start(self):
        print(f"Inizio osservaizone di: {self.path}/{self.filename}")
        event_handler = FileChangeHandler(self.filename, self.callback)
        self.observer.schedule(event_handler, self.path, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()