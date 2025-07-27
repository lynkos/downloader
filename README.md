# Basic Web Scraper
Python script to download images and mp3 files from [some] websites.

Downloaded images can be concatenated and saved as a single pdf or a(n) [vertically stacked] image; useful for downloading manga, comics, etc.

(Fun Fact: This project was originally created to help someone else download mp3 files from Minecraft wiki!)

## Requirements
- [x] [Anaconda](https://docs.continuum.io/free/anaconda/install) **OR** [Miniconda](https://docs.conda.io/projects/miniconda/en/latest)
> [!TIP]
> If you have trouble deciding between Anaconda and Miniconda, please refer to the table below:
> <table>
>  <thead>
>   <tr>
>    <th><center>Anaconda</center></th>
>    <th><center>Miniconda</center></th>
>   </tr>
>  </thead>
>  <tbody>
>   <tr>
>    <td>New to conda and/or Python</td>
>    <td>Familiar with conda and/or Python</td>
>   </tr>
>   <tr>
>    <td>Not familiar with using terminal and prefer GUI</td>
>    <td>Comfortable using terminal</td>
>   </tr>
>   <tr>
>    <td>Like the convenience of having Python and 1,500+ scientific packages automatically installed at once</td>
>    <td>Want fast access to Python and the conda commands and plan to sort out the other programs later</td>
>   </tr>
>   <tr>
>    <td>Have the time and space (a few minutes and 3 GB)</td>
>    <td>Don't have the time or space to install 1,500+ packages</td>
>   </tr>
>   <tr>
>    <td>Don't want to individually install each package</td>
>    <td>Don't mind individually installing each package</td>
>   </tr>
>  </tbody>
> </table>
>
> Typing out entire Conda commands can sometimes be tedious, so I wrote a shell script ([`conda_shortcuts.sh` on GitHub Gist](https://gist.github.com/lynkos/7a4ce7f9e38bb56174360648461a3dc8)) to define shortcuts for commonly used Conda commands.
> <details>
>   <summary>Example: Delete/remove a conda environment named <code>test_env</code></summary>
>
> * Shortcut command
>     ```
>     rmenv test_env
>     ```
> * Manually typing out the entire command
>     ```sh
>     conda env remove -n test_env && rm -rf $(conda info --base)/envs/test_env
>     ```
>
> The shortcut has 80.8% fewer characters!
> </details>

## Installation
1. Open terminal
   * Mac
      * Press <kbd>⌘</kbd> + <kbd>Space</kbd> keys
      * Type `terminal` **OR** (if applicable) your preferred terminal (e.g. `iterm`, etc.)
      * Press <kbd>Enter</kbd> key
   * Linux
      * Press <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>T</kbd> keys
   * Windows
      * Click search box **OR** open Start menu
      * Type `cmd`
      * Click `Command Prompt`, `Open`, **OR** (if needed) `Run as administrator`
2. Verify that conda is installed
   ```
   conda --version
   ```
3. Ensure conda is up to date
   ```
   conda update conda
   ```
4. If necessary, enter the directory where you want the repository (`downloader`) to be cloned
   ```sh
   cd path/to/directory
   ```
5. Clone the repository (`downloader`), then enter its directory
   ```sh
   git clone https://github.com/lynkos/downloader && cd downloader
   ```
6. Create a conda virtual environment from [`environment.yml`](environment.yml)
   ```
   conda env create -f environment.yml
   ```
7. Activate the virtual environment (`dl_env`)
   ```
   conda activate dl_env
   ```
8. Confirm that the virtual environment (`dl_env`) is active
   * If active, the virtual environment's name should be in parentheses `()` or brackets `[]` before your command prompt, e.g.
      ```
      (dl_env) $
      ```
   * If necessary, see which environments are available and/or currently active (active environment denoted with asterisk `*`)
      ```
      conda info --envs
      ```
      **OR**
      ```
      conda env list
      ```

## Usage
### Terminal
1. Run downloader(s)
   * [`ImageDownloader.py`](src/ImageDownloader.py)
     ```
     python src/ImageDownloader.py
     ```
   * [`MP3Downloader.py`](src/MP3Downloader.py)
     ```
     python src/MP3Downloader.py
     ```
2. Deactivate virtual environment (`dl_env`) when finished
   ```
   conda deactivate
   ```

### [Visual Studio Code](https://code.visualstudio.com/download)
1. Open the Command Palette in Visual Studio Code with the relevant keyboard shortcut
    * Mac: <kbd>⌘</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>
    * PC: <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>
2. Search and select `Python: Select Interpreter`
3. Select the virtual environment (`dl_env`)
4. Open [`ImageDownloader.py`](src/ImageDownloader.py) or [`MP3Downloader.py`](src/MP3Downloader.py)
5. Run file by clicking `▷` (i.e. `Play` button) in the upper-right corner
6. Deactivate virtual environment (`dl_env`) when finished
   ```
   conda deactivate
   ```
