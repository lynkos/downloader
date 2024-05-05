# Minecraft `.mp3` Downloader
Simple Python script to download `.mp3` files from [minecraft.wiki](https://minecraft.wiki)

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

## Installation
1. Open terminal
   * Mac
      * Press `⌘` + `Space` keys
      * Type `terminal` **OR** (if applicable) your preferred terminal (e.g. `iterm`, etc.)
      * Press `Enter` key
   * Linux
      * Press `Ctrl` + `Alt` + `T` keys
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
1. Run [`dl.py`](dl.py)
   ```
   python dl.py
   ```
2. Deactivate virtual environment (`dl_env`) when finished
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
      Ctrl + Shift + P
      ```
2. Search and select `Python: Select Interpreter`
3. Select the virtual environment (`dl_env`)
4. Open [`dl.py`](dl.py)
5. Run [`dl.py`](dl.py) by clicking `▷` (i.e. `Play` button) in the upper-right corner
6. Deactivate virtual environment (`dl_env`) when finished
   ```
   conda deactivate
   ```

## [Optional] Conda Shortcut Commands
> [!TIP]
> Instead of manually typing out entire conda commands, you can save time with shortcuts.
> 
> Add [`conda_shortcuts.sh`](conda_shortcuts.sh) then source shell startup file (e.g., `.bashrc`) or restart terminal to apply changes.
> * POSIX
>   ```sh
>   cat conda_shortcuts.sh >> ~/.bashrc
>   source ~/.bashrc
>   ```
> * Windows
>   ```sh
>   type conda_shortcuts.sh >> C:\Users\user\path\to\.bashrc
>   source C:\Users\user\path\to\.bashrc
>   ```

<table>
   <thead>
     <tr>
       <th><center>Command</center></th>
       <th><center>Description</center></th>
       <th><center>Usage</center></th>
     </tr>
   </thead>
   <tbody>
     <tr>
       <td align="center"><a target="_blank" href="conda_shortcuts.sh#L94"><code>act</code></a></td>
       <td align="center">Activate conda environment</td>
       <td><p><pre>act [env_name]</pre></p></td>
     </tr>
     <tr>
       <td align="center"><a target="_blank" href="conda_shortcuts.sh#L3"><code>dac</code></a></td>
       <td align="center">Deactivate conda environment</td>
       <td><p><pre>dac</pre></p></td>
     </tr>
     <tr>
       <td align="center" rowspan="2"><a target="_blank" href="conda_shortcuts.sh#L21"><code>mkenv</code></a></td>
       <td rowspan="2" align="center">Create conda environment(s)</td>
       <td><p><pre>mkenv [yaml_file1] [yaml_file2] ... [yaml_fileN]</pre></p></td>
     </tr>
     <tr>
       <td><p><pre>mkenv [env_name] [package1] [package2] ... [packageN]</pre></p></td>
     </tr>
     <tr>
       <td align="center"><a target="_blank" href="conda_shortcuts.sh#L47"><code>rmenv</code></a></td>
       <td align="center">Remove conda environment(s)</td>
       <td><p><pre>rmenv [env1] [env2] ... [envN]</pre></p></td>
     </tr>
     <tr>
       <td align="center"><a target="_blank" href="conda_shortcuts.sh#L61"><code>rnenv</code></a></td>
       <td align="center">Rename conda environment</td>
       <td><p><pre>rnenv [curr_name] [new_name]</pre></p></td>
     </tr>
     <tr>
       <td align="center"><a target="_blank" href="conda_shortcuts.sh#L81"><code>cpenv</code></a></td>
       <td align="center">Copy conda environment</td>
       <td><p><pre>cpenv [env_name] [copy's_name]</pre></p></td>
     </tr>
     <tr>
       <td align="center"><a target="_blank" href="conda_shortcuts.sh#L108"><code>exp</code></a></td>
       <td align="center">Export conda environment</td>
       <td><p><pre>exp [out_file]</pre></p></td>
     </tr>
     <tr>
       <td align="center"><a target="_blank" href="conda_shortcuts.sh#L132"><code>lsenv</code></a></td>
       <td align="center">List conda environment</td>
       <td><p><pre>lsenv</pre></p></td>
     </tr>
   </tbody>
</table>

> [!WARNING]
> Conda shortcut commands have **ONLY** been tested on `bash v5.2.26(1)-release` with `aarch64-apple-darwin23.2.0` architecture, so — just to be safe — test and make changes as needed.
> 
> E.g., [`rmenv`](conda_shortcuts.sh#L47) assumes the path delimeter is forward slash `/` (POSIX systems); if you use Windows (path delimeter is backslash `\`), replace forward slashes `/` in [`env_path`](conda_shortcuts.sh#L50) with backslashes `\`.