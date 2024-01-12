from bs4 import BeautifulSoup, Tag
from concurrent.futures import ProcessPoolExecutor
from os import getcwd, listdir, makedirs, path, rmdir
from re import findall
from requests import get, exceptions, Response
from time import perf_counter
from urllib.parse import urljoin

BASE_URL: str = "https://minecraft.wiki"
RELATIVE_URLS: list[str] = [ "/w/Villager", "/w/Pillager" ]
FOLDER_NAME: str = "files"
CSS_SELECTOR: str = "[data-title=\"MP3\"]"
TIMEOUT: int = 10

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
        print("Too many redirects")

    except exceptions.URLRequired:
        print("URL is required to make a request")

    except exceptions.InvalidURL:
        print(f"{url} is not a valid URL")

    except exceptions.HTTPError:
        print("HTTP error")

    except exceptions.SSLError:
        print("SSL error")

    except exceptions.ProxyError:
        print("Proxy error")

    except exceptions.ConnectionError:
        print("Connection error")

    except exceptions.RequestException:
        print("Unable to handle request")

    except Exception as error:
        print(f"Error occurred: {error}")

def download(url: str) -> None:
    """
    Download file from `{url}`

    Args:
        url (str): URL of file to download
    """
    response = connect(url)
    
    if response and response.status_code == 200:
        with open(path.join(FOLDER_NAME, path.basename(url)), "wb") as file:
            file.write(response.content)

    else:
        print(f"Failed to download file from {url}\n")

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
    if url.startswith(("https://", "http://", "www.")):
        return url

    return urljoin(BASE_URL, url)

def work(url: str) -> None:
    """
    Get URL(s) of .mp3 file(s) from `{url}` and download to `{FOLDER_NAME}`

    Args:
        url (str): URL of file(s) to download
    """
    response = connect(url)

    if response and response.status_code == 200:
        print(f"Successfully connected to {url}\n")
        file_urls = [ ]
        
        for html_chunk in BeautifulSoup(response.text, "html.parser").select(CSS_SELECTOR):
            if get_file_url(html_chunk, ".mp3"):
                file_urls.append(get_file_url(html_chunk))

        with ProcessPoolExecutor() as executor:
            print(f"Downloading .mp3 file(s) from {url} to {path.join(getcwd(), FOLDER_NAME)}\n")
            executor.map(download, file_urls)

    else:
        print(f"Failed to connect to {url}\n")
    
if __name__ == "__main__":
    print("Starting script...\n")
    start = perf_counter()

    if not path.isdir(FOLDER_NAME):
        makedirs(FOLDER_NAME)

    for relative_url in RELATIVE_URLS:
        work(absolute_url(relative_url))

    if not listdir(FOLDER_NAME): 
        rmdir(FOLDER_NAME)

    end = perf_counter()
    print(f"Total runtime: {(end - start):.2f} second(s)")