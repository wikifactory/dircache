import os
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class Cache:
    def __init__(self, path, maxsize):
        self.path = path
        self.maxsize = int(maxsize)

    def get_path_size(self):
        total_size = 0
        for filename in self.filenames():
            total_size += os.path.getsize(filename)

        return total_size

    def get_files_stats(self):
        stats = []
        for f in self.filenames():
            stats.append((f, os.stat(f)))

        return stats

    def filenames(self):
        for dirpath, dirnames, filenames in os.walk(self.path):
            for f in filenames:
                yield os.path.join(dirpath, f)


class LRUCache(Cache):

    def new_file_event(self, event=None):
        current_size = self.get_path_size()
        if current_size <= self.maxsize:
            logging.info("New file added. Space limit not reached.")
            return

        file_stats = self.get_files_stats()
        file_stats = sorted(
            file_stats,
            key=lambda x: x[1].st_atime,
            reverse=True)

        while current_size > self.maxsize:
            logging.info("Over size limit, looking for eviction candidates")
            candidate_filename, candidate_stats = file_stats.pop()

            logging.info(
                f"Deleting {candidate_filename}."
                f"Last accessed {candidate_stats.st_atime}."
                f"Claiming {candidate_stats.st_size}B back.")
            os.remove(candidate_filename)

            current_size -= candidate_stats.st_size

        logging.info(
            f"No more evictions needed."
            f"Current size {current_size} max allowed {self.maxsize}")
