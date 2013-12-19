import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from count_stat import TXT_DIR_PATH, get_page_html


class EventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        get_page_html()

if __name__ == "__main__":
    event_handler = EventHandler()
    watch_path = TXT_DIR_PATH

    observer = Observer()
    observer.schedule(event_handler, path=watch_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
