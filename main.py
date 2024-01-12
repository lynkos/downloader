from bs4 import BeautifulSoup, Tag
from concurrent.futures import ProcessPoolExecutor
from os import getcwd, makedirs, path
from re import findall
from requests import get, exceptions, Response
from time import perf_counter

BASE_URL: str = "https://minecraft.wiki"
URL_SUBDIRECTORY: list[str] = [ "/w/Villager", "/w/Pillager" ]
FOLDER_NAME: str = "files"
CSS_SELECTOR: str = "[data-title=\"MP3\"]"
TIMEOUT: int = 10

def connect(relative_path: str) -> Response:
    """
    Connect to `{BASE_URL}{relative_path}`

    Args:
        relative_path (str): Relative path (i.e. anything after `{BASE_URL}`) of URL to connect to
        
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
        print(f"{BASE_URL}{relative_path} is not a valid URL")
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

    except Exception as error:
        print("Error occurred:", error)
        raise SystemExit(error) from None

    return response

def download(relative_path: str) -> None:
    """
    Download file from `{BASE_URL}{relative_path}` and save to `{FOLDER_NAME}{relative_path}`

    Args:
        relative_path (str): Relative path (i.e. anything after `{BASE_URL}`) of file to download
    """
    response = connect(relative_path)
    
    if response.status_code == 200:
        with open(path.join(FOLDER_NAME, path.basename(relative_path)), "wb") as file:
            file.write(response.content)

    else:
        print(f"Failed to download file from {BASE_URL}{relative_path}... Status code: {response.status_code}\n")

def get_file_path(html: Tag, extension: str = "") -> str:
    """
    Extract file path (with given extension, if applicable) from HTML `src` tag

    Args:
        html (Tag): HTML to search
        extension (str, optional): File extension; defaults to empty string ""

    Returns:
        str: File path (with given extension, if applicable) within HTML `src` tag
    """
    return findall(rf"src=\"(.*?){extension}\"", str(html).strip())[0]

if __name__ == "__main__":
    print("Starting script...\n")
    start = perf_counter()
    
    for url in URL_SUBDIRECTORY:
        response = connect(url)

        if response.status_code == 200:
            print(f"Successfully connected to {BASE_URL}{url}\n")
            relative_paths = [ ]
            
            for html_chunk in BeautifulSoup(response.text, "html.parser").select(CSS_SELECTOR):
                if get_file_path(html_chunk, ".mp3"):
                    relative_paths.append(get_file_path(html_chunk))

            if not path.isdir(FOLDER_NAME):
                makedirs(FOLDER_NAME)

            with ProcessPoolExecutor() as executor:
                print(f"Downloading .mp3 file(s) from {BASE_URL}{url} to {path.join(getcwd(), FOLDER_NAME)}\n")
                executor.map(download, relative_paths)

        else:
            print(f"Failed to connect to {BASE_URL}{url}")
            continue

    end = perf_counter()
    print(f"Completed file download(s) in {(end - start):.2f} second(s)")