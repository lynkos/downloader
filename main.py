from bs4 import BeautifulSoup, Tag
from requests import get, Response, exceptions
from concurrent.futures import ProcessPoolExecutor
from re import findall
from os import getcwd, path, makedirs
from time import time

BASE_URL = "https://minecraft.wiki"
URL_SUBDIRECTORY = "/w/Villager"
FOLDER_NAME = "files"
CSS_SELECTOR = "[data-title=\"MP3\"]"
FILE_EXTENSION = ".mp3"
TIMEOUT = 10

def connect(relative_path: str) -> Response:
    """
    Connect to {BASE_URL}{relative_path}

    Args:
        relative_path (str): Relative path (i.e. anything after {BASE_URL}) of URL to connect to
        
    Raises:
        SystemExit: Exit from interpreter if a request exception/error occurs

    Returns:
        Response: Request response
    """
    try:
        response = get(f"{BASE_URL}{relative_path}", allow_redirects = True, stream = True, timeout = TIMEOUT)
        response.raise_for_status()

    except exceptions.ConnectTimeout as error:
        print(f"Request to {BASE_URL}{relative_path} timed out after {TIMEOUT} seconds")
        raise SystemExit(error) from None

    except exceptions.ReadTimeout as error:
        print(f"{BASE_URL}{relative_path} failed to send data within {TIMEOUT} seconds")
        raise SystemExit(error) from None

    except exceptions.TooManyRedirects as error:
        print("Too many redirects")
        raise SystemExit(error) from None

    except exceptions.URLRequired as error:
        print("URL is required to make a request")
        raise SystemExit(error) from None

    except exceptions.InvalidURL as error:
        print(f"{BASE_URL}{relative_path} is invalid")
        raise SystemExit(error) from None

    except exceptions.HTTPError as error:
        print("HTTP error")
        raise SystemExit(error) from None

    except exceptions.SSLError as error:
        print("SSL error")
        raise SystemExit(error) from None

    except exceptions.ProxyError as error:
        print("Proxy error")
        raise SystemExit(error) from None

    except exceptions.ConnectionError as error:
        print("Connection error")
        raise SystemExit(error) from None

    except exceptions.RequestException as error:
        print("Unable to handle request")
        raise SystemExit(error) from None

    except Exception as exception:
        print("Error occurred:", exception)
        raise SystemExit(exception) from None

    return response

def download(relative_path: str) -> None:
    """
    Download file from {BASE_URL}{relative_path} and save to {FOLDER_NAME}{relative_path}

    Args:
        relative_path (str): Relative path (i.e. anything after {BASE_URL}) of file to download
    """
    response = connect(relative_path)
    
    if response.status_code == 200:
        with open(path.join(FOLDER_NAME, path.basename(relative_path)), "wb") as file:
            file.write(response.content)

def find_path(html: Tag, extension: str = "") -> list[str]:
    """
    Find path(s) of desired file(s) within HTML src tags

    Args:
        html (Tag): Chunk of HTML to search
        extension (str, optional): File extension; defaults to empty string ""

    Returns:
        list[str]: List of strings of file path(s) (with given extension, if applicable) within HTML src tags
    """
    return findall(rf"src=\"(.*?){extension}\"", str(html).strip())

if __name__ == "__main__":
    print("Starting script...\n")
    response = connect(URL_SUBDIRECTORY)

    if response.status_code == 200:
        print(f"Successfully connected to {BASE_URL}{URL_SUBDIRECTORY}\n")
        relative_paths = [ ]
        
        for chunk in BeautifulSoup(response.text, "html.parser").select(CSS_SELECTOR):
            if find_path(chunk, FILE_EXTENSION):
                relative_paths.append(find_path(chunk)[0])

        if not path.isdir(FOLDER_NAME):
            makedirs(FOLDER_NAME)

        start = time()
        with ProcessPoolExecutor() as executor:
            print(f"Downloading {FILE_EXTENSION} file(s) to {path.join(getcwd(), FOLDER_NAME)}\n")
            executor.map(download, relative_paths)
        end = time()

        print(f"Download(s) completed after {(end - start):.2f} second(s)")

    else:
        print("Failed to retrieve the webpage; status code:", response.status_code)
        raise SystemExit(response.status_code) from None