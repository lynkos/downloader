from abc import ABC, abstractmethod
from contextlib import contextmanager
from bs4 import BeautifulSoup, Tag
from concurrent.futures import ProcessPoolExecutor
from os import makedirs
from os.path import getsize, isdir, isfile, join
from random import choices
from re import findall
from requests import get, Response
from requests.exceptions import (ConnectTimeout, HTTPError, InvalidURL, ProxyError, ReadTimeout,
                                 RequestException, SSLError, TooManyRedirects, URLRequired)
from shutil import get_terminal_size
from string import ascii_lowercase, digits

# TODO Make CLI tool

IGNORE: list[str] = [ "" ]
"""List of filenames to ignore (i.e. won't save files containing these strings in their name)"""

URL_FILENAME: str = "urls.txt"
"""Name of file containing relative URL(s) (i.e. anything after `BASE_URL`) of web page(s) to download from"""

SAVE_PATH: str = "."
"""Absolute path of directory to save downloads to"""

TIMEOUT: int = 5
"""Number of seconds till request times out"""

class Downloader(ABC):
    def __init__(self, save_path: str = SAVE_PATH, url_filename: str = URL_FILENAME):
        super().__init__()

        if not isdir(save_path): makedirs(save_path, exist_ok = True)

        self._save_path = save_path
        self._url_filename = url_filename

    def _connect(self, url: str) -> Response | None:
        """
        Connect to URL

        Args:
            url (str): URL to connect to
            
        Returns:
            Response | None: HTTP request response if applicable, else None
        """    
        try:
            return get(url, allow_redirects = True, stream = True, timeout = TIMEOUT)

        except ConnectTimeout:
            print(f"Request to {url} timed out after {TIMEOUT} seconds")

        except ReadTimeout:
            print(f"{url} failed to send data within {TIMEOUT} seconds")

        except TooManyRedirects:
            print(f"{url} has too many redirects")

        except (URLRequired, InvalidURL):
            print(f"{url} is not a valid URL")

        except HTTPError:
            print(f"HTTP error while connecting to {url}")

        except SSLError:
            print(f"SSL error while connecting to {url}")

        except ProxyError:
            print(f"Proxy error while connecting to {url}")

        except ConnectionError:
            print(f"Connection error while connecting to {url}")

        except RequestException:
            print(f"Unable to handle request to {url}")

        except Exception as error:
            print(f"Unexpected error while connecting to {url} ({error})")

    def _abs_save_path(self, obj: str) -> str:
        """
        _summary_

        Args:
            obj (str): Can be a file or directory

        Returns:
            str: _description_
        """
        return join(self._save_path, obj)

    def _generate_random_id(self) -> str:
        """
        Generate random, 8-character ID

        Returns:
            str: Randomly generated, 8-character ID
        """
        return "".join(choices(ascii_lowercase + digits, k = 8))

    def _random_filename(self, ext: str, save_name: str | None = None) -> str:
        ext = f".{ext}" if not ext.startswith(".") else ext
        save_name = f"{save_name}{ext}" if save_name and not save_name.endswith(ext) else save_name
        return f"{type(self).__name__}_{self._generate_random_id()}{ext}" if not save_name else save_name

    def _get_url(self, html: Tag, extension: str = "") -> str:
        """
        Get URL from HTML tag

        Args:
            html (Tag): HTML tag to search
            extension (str, optional): File extension; defaults to empty string

        Returns:
            str: URL in HTML tag
        """
        return findall(rf"src=\"(.*?){extension}\"", str(html).strip())[0]

    @abstractmethod
    def _download(self, url: str) -> None:
        raise NotImplementedError("Must override _download()")
    
    def work(self, url: str, css_selector: str, ext: str, ignore: list[str] = IGNORE) -> list:
        """
        Get list of all [applicable] file(s) from URL

        Args:
            url (str): URL of web page containing file(s) to download

        Returns:
            list: List of files from URL
        """
        response, files = self._connect(url), [ ]

        if response and response.status_code == 200:
            self._divider()
            print(f"Successfully connected to {url}\n")
            
            with ProcessPoolExecutor() as executor:                
                for html_tag in BeautifulSoup(response.text, "html.parser").select(css_selector):
                    file_url = self._get_url(html_tag, ext)
                    
                    if file_url and not any(ignore in file_url for ignore in ignore):
                        future = executor.submit(self._download, file_url)
                        result = future.result()
                        if result: files.append(result)

            print(f"Completed download(s) from {url}\n")
            
        else: print(f"Skipping: Unable to connect to {url}\n")
        self._divider()
        return files

    @abstractmethod
    def _run(self, url: str, **kwargs) -> None:
        raise NotImplementedError("Must override _run()")

    def run(self, **kwargs) -> None:
        """
        Run script
        """
        try:
            if isfile(self._url_filename) and getsize(self._url_filename) > 0:
                with open(self._url_filename, "r") as file:
                    for url in file.read().splitlines():
                        try: self._run(url, **kwargs)

                        except Exception as error:
                            print(f"Skipping: Unable to get file(s) from {url} ({error})\n")

                        self._divider()

        except Exception as error:
            print(f"Unexpected error while reading URLs from {self._url_filename} ({error})\n")

    def _divider(self) -> None:
        print(f"{'=' * get_terminal_size().columns}\n")

    @contextmanager
    def handle_download(self, url: str):
        try:
            yield

        except ChildProcessError:
            print(f"Child process error while downloading {url}\n")

        except InterruptedError:
            print(f"Interrupted while downloading {url}\n")

        except ProcessLookupError:
            print(f"Process lookup error while downloading {url}\n")

        except MemoryError:
            print(f"Memory error while downloading {url}\n")

        except TimeoutError:
            print(f"Timeout error while downloading {url}\n")

        except PermissionError:
            print(f"Permission error while downloading {url}\n")

        except (IOError, OSError):
            print(f"I/O error while downloading {url}\n")

        except Exception as error:
            print(f"Unexpected error while downloading {url} ({error})\n")
