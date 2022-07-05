# TODO move to ovos_utils

import time
from os.path import dirname

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FileWatcher:
    def __init__(self, files, callback, recursive=False, ignore_creation=False):
        self.observer = Observer()
        self.handlers = []
        for file_path in files:
            watch_dir = dirname(file_path)
            self.observer.schedule(FileEventHandler(file_path, callback, ignore_creation),
                                   watch_dir, recursive=recursive)
        self.observer.start()

    def shutdown(self):
        self.observer.unschedule_all()
        self.observer.stop()


class FileEventHandler(FileSystemEventHandler):
    def __init__(self, file_path, callback, ignore_creation=False):
        super().__init__()
        self._callback = callback
        self._file_path = file_path
        self._debounce = 1
        self._last_update = 0
        if ignore_creation:
            self._events = ('modified')
        else:
            self._events = ('created', 'modified')

    def on_any_event(self, event):
        if event.is_directory:
            return
        elif event.event_type in self._events:
            if event.src_path == self._file_path:
                if time.time() - self._last_update >= self._debounce:
                    self._callback(event.src_path)
                    self._last_update = time.time()
