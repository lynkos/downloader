# Website File Downloader
Simple python script to download certain files from specified URL

## Requirements
- [x] [Anaconda](https://docs.continuum.io/free/anaconda/install) **OR** [Miniconda](https://docs.conda.io/projects/miniconda/en/latest)
> [!NOTE]
> If you have trouble deciding between Anaconda and Miniconda, please refer to the table below
> <table>
> <thead>
> <tr>
> <th><center>Anaconda</center></th>
> <th><center>Miniconda</center></th>
> </tr>
> </thead>
> <tbody>
> <tr>
> <td>New to conda and/or Python</td>
> <td>Familiar with conda and/or Python</td>
> </tr>
> <tr>
> <td>Like the convenience of having Python and 1,500+ scientific packages automatically installed at once</td>
> <td>Want fast access to Python and the conda commands and plan to sort out the other programs later</td>
> </tr>
> <tr>
> <td>Have the time and space (a few minutes and 3 GB)</td>
> <td>Don't have the time or space to install 1,500+ packages</td>
> </tr>
> <tr>
> <td>Don't want to individually install each package</td>
> <td>Don't mind individually installing each package</td>
> </tr>
> </tbody>
> </table>

## Installation
1. Verify that conda is installed
   ```
   conda --version
   ```
2. Ensure conda is up to date
   ```
   conda update conda
   ```
3. Enter the directory where you want the repository (`downloader`) to be cloned
     * Unix
       ```
       cd ~/relative/path/to/directory
       ```
     * Windows
       ```
       cd absolute\path\to\directory
       ```
4. Clone the repository (`downloader`), then enter its directory
   ```
   git clone https://github.com/lynkos/downloader && cd downloader
   ```
5. Create a conda virtual environment from `environment.yml`
   ```
   conda env create -f environment.yml
   ```
6. Activate the virtual environment (`dl_env`)
   ```
   conda activate dl_env
   ```
7. Confirm that the virtual environment (`dl_env`) is active
     * If active, the virtual environment's name should be in parentheses () or brackets [] before your command prompt, e.g.
       ```
       (dl_env) $
       ```
     * If necessary, see which environments are available and/or currently active (active environment denoted with asterisk (*))
       ```
       conda info --envs
       ```
       **OR**
       ```
       conda env list
       ```

## Usage
### Command Line
1. Run `main.py`
   * UNIX
      ```
      $(which python) main.py
      ```
   * Windows
      ```
      $(where python) main.py
      ```
2. Deactivate the virtual environment (`dl_env`) when you're finished
   ```
   conda deactivate
   ```

### [Visual Studio Code](https://code.visualstudio.com/download)
1. Open the Command Palette in Visual Studio Code with the relevant keyboard shortcut
    * Mac
      ```
      ⌘ + Shift + P
      ```
    * PC
      ```
      CTRL + Shift + P
      ```
2. Search and select `Python: Select Interpreter`
3. Select the virtual environment (`dl_env`)
4. Open `main.py`
5. Run `main.py` by clicking `▷` (i.e. `Play` button) in the upper-right corner
6. Deactivate the virtual environment (`dl_env`) when you're finished
   ```
   conda deactivate
   ```