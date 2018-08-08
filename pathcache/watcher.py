import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Watcher:
    def __init__(self, path, cache):
        self.path = path
        self.observer = Observer()
        self.cache = cache

    def run(self):
        event_handler = Handler(self.cache)
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    def __init__(self, cache):
        self.cache = cache
        super().__init__()

    def on_any_event(self, event):
        if event.is_directory or event.event_type == "deleted":
            return

        self.cache.new_file_event(event)

        return
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print("Received modified event - %s." % event.src_path)
