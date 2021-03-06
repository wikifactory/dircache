import sys
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


BUSY_LOOP_WAIT = 2


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
                time.sleep(BUSY_LOOP_WAIT)
        except KeyboardInterrupt:
            self.observer.stop()
        except Exception as e:
            self.observer.stop()
            sys.exit("Error", e)

        self.observer.join()


class Handler(FileSystemEventHandler):

    def __init__(self, cache):
        self.cache = cache
        super().__init__()

    def on_any_event(self, event):
        if event.is_directory or event.event_type == "deleted":
            return

        self.cache.new_file_event(event)
