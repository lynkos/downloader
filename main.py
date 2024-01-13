from bs4 import BeautifulSoup, Tag
from concurrent.futures import ProcessPoolExecutor
from os import getcwd, listdir, makedirs, path, rmdir
from re import findall
from requests import get, exceptions, Response
from time import perf_counter
from urllib.parse import urljoin

BASE_URL: str = "https://minecraft.wiki"
"""Base URL of page(s) to download from"""

RELATIVE_URLS: list[str] = [ "/w/Villager", "/w/Pillager", "/w/Minecraft_Dungeons:Mage" ]
"""Relative URL(s) (i.e. anything after {BASE_URL}) of page(s) to download from"""

FOLDER_NAME: str = "minecraft_downloads"
"""Name of folder to save downloads to"""

FOLDER_PATH: str = path.join(getcwd(), FOLDER_NAME)
"""Absolute path of folder to save downloads to"""

CSS_SELECTOR: str = "[data-title=\"MP3\"]"
"""Pattern used to select certain HTML element(s)"""

TIMEOUT: int = 10
"""Number of seconds till request times out"""

def connect(url: str) -> Response | None:
    """
    Connect to `{url}`

    Args:
        url (str): URL to connect to
        
    Returns:
        Response | None: HTTP request response if applicable, else None
    """
    try:
        return get(url, allow_redirects = True, stream = True, timeout = TIMEOUT)

    except exceptions.ConnectTimeout:
        print(f"Request to {url} timed out after {TIMEOUT} seconds")

    except exceptions.ReadTimeout:
        print(f"{url} failed to send data within {TIMEOUT} seconds")

    except exceptions.TooManyRedirects:
        print(f"{url} has too many redirects")

    except (exceptions.URLRequired, exceptions.InvalidURL):
        print(f"{url} is not a valid URL")

    except exceptions.HTTPError:
        print(f"HTTP error while connecting to {url}")

    except exceptions.SSLError:
        print(f"SSL error while connecting to {url}")

    except exceptions.ProxyError:
        print(f"Proxy error while connecting to {url}")

    except exceptions.ConnectionError:
        print(f"Connection error while connecting to {url}")

    except exceptions.RequestException:
        print(f"Unable to handle request to {url}")

    except Exception as error:
        print(f"Unexpected error while connecting to {url} ({error})")

def download(url: str) -> None:
    """
    Download file from `{url}`

    Args:
        url (str): URL of file to download
    """
    response = connect(url)
    
    if response and response.status_code == 200:         
        try:
            with open(path.join(FOLDER_PATH, path.basename(url)), "wb") as file:
                file.write(response.content)

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

    else:
        print(f"Failed to connect to {url}\n")

def get_file_url(html: Tag, extension: str = "") -> str:
    """
    Extract file URL (with given extension, if applicable) from HTML `src` tag

    Args:
        html (Tag): HTML to search
        extension (str, optional): File extension; defaults to empty string ""

    Returns:
        str: File URL
    """
    return absolute_url(findall(rf"src=\"(.*?){extension}\"", str(html).strip())[0])

def absolute_url(url: str) -> str:
    """
    Convert URL to absolute URL

    Args:
        url (str): URL

    Returns:
        str: Absolute URL
    """
    return urljoin(BASE_URL, url)

def work(url: str) -> None:
    """
    Get URL(s) of .mp3 file(s) from `{url}` and download to `{FOLDER_PATH}`

    Args:
        url (str): URL of file(s) to download
    """
    response = connect(url)

    if response and response.status_code == 200:
        print(f"Successfully connected to {url}\n")
        
        with ProcessPoolExecutor() as executor:
            print(f"Attempting to download .mp3 file(s) from {url} to {FOLDER_PATH}\n")
            
            for html_chunk in BeautifulSoup(response.text, "html.parser").select(CSS_SELECTOR):
                if get_file_url(html_chunk, ".mp3"):
                    executor.submit(download, get_file_url(html_chunk))

    else:
        print(f"Failed to connect to {url}\n")

if __name__ == "__main__":
    print("Starting script...\n")
    start = perf_counter()

    if not path.isdir(FOLDER_PATH):
        makedirs(FOLDER_PATH)

    for relative_url in RELATIVE_URLS:
        work(absolute_url(relative_url))

    if not listdir(FOLDER_PATH): 
        rmdir(FOLDER_PATH)

    end = perf_counter()
    print(f"Total runtime: {(end - start):.2f} second(s)")