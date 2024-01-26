from bs4 import BeautifulSoup, Tag
from concurrent.futures import ProcessPoolExecutor
from os import getcwd, listdir, makedirs, path, rmdir
from re import findall
from requests import get, exceptions, Response
from shutil import get_terminal_size
from time import perf_counter
from urllib.parse import urljoin

BASE_URL: str = "https://minecraft.wiki"
"""Website to download from"""

RELATIVE_URLS: list[str] = [ "/w/Villager", "/w/Pillager", "/w/Minecraft_Dungeons:Mage" ]
"""Relative URL(s) (i.e. anything after `BASE_URL`) of web page(s) to download from"""

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
    Connect to URL

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

def download(file_url: str) -> None:
    """
    Save file to `FOLDER_PATH`

    Args:
        file_url (str): URL of file to download
    """
    response = connect(file_url)
    
    if response and response.status_code == 200:         
        try:
            with open(path.join(FOLDER_PATH, path.basename(file_url)), "wb") as file:
                file.write(response.content)

        except ChildProcessError:
            print(f"Child process error while downloading {file_url}\n")

        except InterruptedError:
            print(f"Interrupted while downloading {file_url}\n")

        except ProcessLookupError:
            print(f"Process lookup error while downloading {file_url}\n")

        except MemoryError:
            print(f"Memory error while downloading {file_url}\n")

        except TimeoutError:
            print(f"Timeout error while downloading {file_url}\n")

        except PermissionError:
            print(f"Permission error while downloading {file_url}\n")

        except (IOError, OSError):
            print(f"I/O error while downloading {file_url}\n")

        except Exception as error:
            print(f"Unexpected error while downloading {file_url} ({error})\n")

    else:
        print(f"Failed to connect to {file_url}\n")

def get_url(html: Tag, extension: str = "") -> str:
    """
    Get URL from HTML tag

    Args:
        html (Tag): HTML tag to search
        extension (str, optional): File extension; defaults to empty string

    Returns:
        str: URL in HTML tag
    """
    return findall(rf"src=\"(.*?){extension}\"", str(html).strip())[0]

def absolute_url(url: str) -> str:
    """
    Convert URL to absolute URL

    Args:
        url (str): URL to convert

    Returns:
        str: Absolute URL
    """
    return urljoin(BASE_URL, url)

def work(web_page: str) -> None:
    """
    Download all .mp3 file(s) from web page to `FOLDER_PATH`

    Args:
        web_page (str): URL of web page containing file(s) to download
    """
    response = connect(web_page)

    if response and response.status_code == 200:
        print(f"Successfully connected to {web_page}\n")
        
        with ProcessPoolExecutor() as executor:
            print(f"Attempting to download .mp3 file(s) from {web_page} to {FOLDER_PATH}\n")
            
            for html_tag in BeautifulSoup(response.text, "html.parser").select(CSS_SELECTOR):
                if get_url(html_tag, ".mp3"):                    
                    executor.submit(download, absolute_url(get_url(html_tag)))

        print(f"Completed download(s) from {web_page} to {FOLDER_PATH}\n")

    else:
        print(f"Failed to connect to {web_page}\n")

if __name__ == "__main__":
    print("Starting script...\n")
    start = perf_counter()

    if not path.isdir(FOLDER_PATH):
        makedirs(FOLDER_PATH)

    for relative_url in RELATIVE_URLS:
        print(f"{'=' * get_terminal_size().columns}\n")
        work(absolute_url(relative_url))

    if not listdir(FOLDER_PATH): 
        rmdir(FOLDER_PATH)

    end = perf_counter()
    print(f"{'=' * get_terminal_size().columns}\n")
    print(f"Total runtime: {(end - start):.2f} second(s)")
