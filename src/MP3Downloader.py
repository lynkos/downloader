from Downloader import Downloader, IGNORE, SAVE_PATH, URL_FILENAME
from os import listdir, makedirs, rmdir
from os.path import basename, isdir, join
from time import perf_counter

CSS_SELECTOR: str = f"[data-title=\"MP3\"]"
"""Pattern used to select certain HTML element(s)"""

EXTENSION: str = ".mp3"
"""File extension"""

class MP3Downloader(Downloader):
    def __init__(self, save_path: str = SAVE_PATH, url_filename: str = URL_FILENAME):
        super().__init__(save_path, url_filename)

    def _download(self, file_url: str) -> None:
        """
        Save file to specified folder

        Args:
            file_url (str): URL of MP3 file to download
        """
        response = self._connect(file_url)
        
        if response and response.status_code == 200:
            with self.handle_download(file_url):
                with open(join(self._save_path, basename(file_url)), "wb") as file:
                    file.write(response.content)

        else: print(f"Failed to connect to {file_url}\n")

    def _run(self, url: str) -> None:
        """
        Run script

        Args:
            url (str): URL containing MP3s to download
        """
        folder = self._abs_save_path(url[1:].replace("/", "_"))
        
        if not isdir(folder): makedirs(folder, exist_ok = True)
        
        self._divider()
        self.work(url, CSS_SELECTOR, EXTENSION, IGNORE)

        if not listdir(folder): rmdir(folder)

if __name__ == "__main__":
    print(f"Starting script...\n")
    start = perf_counter()

    mp3 = MP3Downloader()
    mp3.run()
    
    end = perf_counter()
    print(f"Total runtime: {(end - start):.2f} second(s)")
    exit(0)